from rest_framework import serializers

from apps.animals.models import Animal
from apps.breeding.models import BreedingEvent
from apps.health.models import Mortality, Treatment, Vaccination
from apps.operations.models import HerdCount, MovementLog, RFIDScanLog


class AnimalSerializer(serializers.ModelSerializer):
    age_months = serializers.IntegerField(read_only=True)

    class Meta:
        model = Animal
        fields = [
            "tag_number",
            "rfid_code",
            "qr_code",
            "ranch",
            "species",
            "breed",
            "sex",
            "date_of_birth",
            "source",
            "dam_tag",
            "sire_tag",
            "status",
            "photo",
            "purchase_price",
            "purchase_date",
            "notes",
            "age_months",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "age_months"]


class BreedingEventSerializer(serializers.ModelSerializer):
    recorded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BreedingEvent
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "expected_delivery_date"]


class VaccinationSerializer(serializers.ModelSerializer):
    recorded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vaccination
        fields = "__all__"
        read_only_fields = ["created_at"]


class TreatmentSerializer(serializers.ModelSerializer):
    recorded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Treatment
        fields = "__all__"
        read_only_fields = ["created_at"]


class MortalitySerializer(serializers.ModelSerializer):
    recorded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Mortality
        fields = "__all__"
        read_only_fields = ["created_at", "age_at_death_months"]


class HerdCountSerializer(serializers.ModelSerializer):
    recorded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = HerdCount
        fields = "__all__"
        read_only_fields = ["created_at", "difference"]


class MovementLogSerializer(serializers.ModelSerializer):
    recorded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MovementLog
        fields = "__all__"
        read_only_fields = ["created_at"]


class RFIDScanLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFIDScanLog
        fields = "__all__"
        read_only_fields = ["created_at"]


class SyncOperationSerializer(serializers.Serializer):
    operation = serializers.ChoiceField(choices=["create", "update", "delete"])
    table_name = serializers.CharField(max_length=100)
    record_data = serializers.JSONField()
    timestamp = serializers.DateTimeField()


class SyncRequestSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=100)
    operations = SyncOperationSerializer(many=True)
