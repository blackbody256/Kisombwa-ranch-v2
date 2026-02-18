from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.animals.models import Animal
from apps.breeding.models import BreedingEvent
from apps.core.models import SyncQueue
from apps.health.models import Mortality, Treatment, Vaccination
from apps.operations.models import HerdCount, MovementLog, RFIDScanLog
from apps.analytics.services import build_dashboard_data

from .serializers import (
    AnimalSerializer,
    BreedingEventSerializer,
    HerdCountSerializer,
    MortalitySerializer,
    MovementLogSerializer,
    RFIDScanLogSerializer,
    SyncRequestSerializer,
    TreatmentSerializer,
    VaccinationSerializer,
)


class BaseQueryParamFilterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        for field in self.filter_fields:
            value = self.request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
        return queryset


class AnimalViewSet(BaseQueryParamFilterViewSet):
    queryset = Animal.objects.all().select_related("ranch", "dam_tag", "sire_tag")
    serializer_class = AnimalSerializer
    lookup_field = "tag_number"
    filter_fields = ["species", "status", "ranch"]


class BreedingEventViewSet(BaseQueryParamFilterViewSet):
    queryset = BreedingEvent.objects.all().select_related("female_tag", "male_tag")
    serializer_class = BreedingEventSerializer
    filter_fields = ["female_tag", "pregnancy_confirmed"]


class VaccinationViewSet(BaseQueryParamFilterViewSet):
    queryset = Vaccination.objects.all().select_related("animal_tag", "administered_by")
    serializer_class = VaccinationSerializer
    filter_fields = ["animal_tag", "vaccine_type"]


class TreatmentViewSet(BaseQueryParamFilterViewSet):
    queryset = Treatment.objects.all().select_related("animal_tag", "treated_by")
    serializer_class = TreatmentSerializer
    filter_fields = ["animal_tag"]


class MortalityViewSet(BaseQueryParamFilterViewSet):
    queryset = Mortality.objects.all().select_related("animal_tag")
    serializer_class = MortalitySerializer
    filter_fields = ["animal_tag"]


class HerdCountViewSet(BaseQueryParamFilterViewSet):
    queryset = HerdCount.objects.all().select_related("ranch")
    serializer_class = HerdCountSerializer
    filter_fields = ["ranch", "species", "count_date"]


class MovementLogViewSet(BaseQueryParamFilterViewSet):
    queryset = MovementLog.objects.all().select_related("animal_tag")
    serializer_class = MovementLogSerializer
    filter_fields = ["animal_tag", "movement_date"]


class RFIDScanLogViewSet(BaseQueryParamFilterViewSet):
    queryset = RFIDScanLog.objects.all().select_related("animal_tag")
    serializer_class = RFIDScanLogSerializer
    filter_fields = ["rfid_code", "gate_id"]


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(build_dashboard_data())


SYNC_TABLES = {
    "animals": (Animal, AnimalSerializer, "tag_number"),
    "breeding_events": (BreedingEvent, BreedingEventSerializer, "id"),
    "vaccinations": (Vaccination, VaccinationSerializer, "id"),
    "treatments": (Treatment, TreatmentSerializer, "id"),
    "mortality": (Mortality, MortalitySerializer, "id"),
    "herd_counts": (HerdCount, HerdCountSerializer, "id"),
    "movement_logs": (MovementLog, MovementLogSerializer, "id"),
    "rfid_scan_logs": (RFIDScanLog, RFIDScanLogSerializer, "id"),
}


class SyncAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = SyncRequestSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        device_id = payload.validated_data["device_id"]
        operations = payload.validated_data["operations"]

        synced = 0
        failed = 0
        errors = []

        for entry in operations:
            operation = entry["operation"]
            table_name = entry["table_name"]
            record_data = entry["record_data"]
            timestamp = entry["timestamp"]

            queue_row = SyncQueue.objects.create(
                device_id=device_id,
                user=request.user,
                operation=operation,
                table_name=table_name,
                record_data=record_data,
                timestamp=timestamp,
                synced=False,
            )

            try:
                if table_name not in SYNC_TABLES:
                    raise ValueError(f"Unsupported table_name '{table_name}'.")

                model_class, serializer_class, pk_field = SYNC_TABLES[table_name]

                if operation == "create":
                    serializer = serializer_class(
                        data=record_data,
                        context={"request": request},
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                else:
                    pk_value = record_data.get(pk_field)
                    if pk_value is None:
                        raise ValueError(
                            f"Missing primary key field '{pk_field}' for {operation}."
                        )

                    instance = model_class.objects.get(pk=pk_value)

                    if operation == "update":
                        serializer = serializer_class(
                            instance,
                            data=record_data,
                            partial=True,
                            context={"request": request},
                        )
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                    elif operation == "delete":
                        instance.delete()

                queue_row.synced = True
                queue_row.synced_at = timezone.now()
                queue_row.error_message = ""
                queue_row.save(update_fields=["synced", "synced_at", "error_message"])
                synced += 1
            except Exception as exc:
                queue_row.error_message = str(exc)
                queue_row.save(update_fields=["error_message"])
                failed += 1
                errors.append(
                    {
                        "table_name": table_name,
                        "operation": operation,
                        "error": str(exc),
                    }
                )

        return Response({"synced": synced, "failed": failed, "errors": errors})
