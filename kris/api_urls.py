from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    AnimalViewSet,
    BreedingEventViewSet,
    DashboardAPIView,
    HerdCountViewSet,
    LoginAPIView,
    LogoutAPIView,
    MortalityViewSet,
    MovementLogViewSet,
    RFIDScanLogViewSet,
    SyncAPIView,
    TreatmentViewSet,
    VaccinationViewSet,
)

router = DefaultRouter()
router.register("animals", AnimalViewSet, basename="animals")
router.register("breeding", BreedingEventViewSet, basename="breeding")
router.register("vaccinations", VaccinationViewSet, basename="vaccinations")
router.register("treatments", TreatmentViewSet, basename="treatments")
router.register("mortality", MortalityViewSet, basename="mortality")
router.register("herd-counts", HerdCountViewSet, basename="herd-counts")
router.register("movements", MovementLogViewSet, basename="movements")
router.register("rfid/scans", RFIDScanLogViewSet, basename="rfid-scans")

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name="api-login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="api-logout"),
    path("sync/", SyncAPIView.as_view(), name="api-sync"),
    path("analytics/dashboard/", DashboardAPIView.as_view(), name="api-dashboard"),
    path("", include(router.urls)),
]
