from datetime import date

from django.test import TestCase

from apps.animals.models import Animal
from apps.breeding.models import BreedingEvent
from apps.health.models import Mortality, Treatment, Vaccination
from apps.operations.models import HerdCount, MovementLog

from .models import Ranch, Staff, User


class RecordingWithoutRFIDTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="pass12345",
            role="manager",
        )
        self.ranch = Ranch.objects.create(
            name="Kisombwa Ranch",
            location="Mubende",
            owner=self.owner,
        )
        self.staff = Staff.objects.create(
            ranch=self.ranch,
            name="Test Herdsman",
            role="herdsman",
        )
        self.female = Animal.objects.create(
            tag_number="BORAN001",
            ranch=self.ranch,
            species="cattle",
            breed="Boran",
            sex="female",
            date_of_birth=date(2022, 1, 1),
            source="born",
        )
        self.male = Animal.objects.create(
            tag_number="BORAN002",
            ranch=self.ranch,
            species="cattle",
            breed="Boran",
            sex="male",
            date_of_birth=date(2021, 1, 1),
            source="born",
        )

    def test_animal_recording_does_not_require_rfid(self):
        self.assertIsNone(self.female.rfid_code)
        self.assertEqual(self.female.status, "active")

    def test_breeding_health_and_operations_events_work_without_rfid(self):
        breeding = BreedingEvent.objects.create(
            female_tag=self.female,
            male_tag=self.male,
            service_date=date(2025, 1, 15),
            method="natural",
            recorded_by=self.owner,
        )
        vaccination = Vaccination.objects.create(
            animal_tag=self.female,
            vaccine_type="FMD",
            date_administered=date(2025, 2, 1),
            administered_by=self.staff,
            recorded_by=self.owner,
        )
        treatment = Treatment.objects.create(
            animal_tag=self.female,
            diagnosis="Mild infection",
            treatment_date=date(2025, 2, 2),
            treated_by=self.staff,
            recorded_by=self.owner,
        )
        herd_count = HerdCount.objects.create(
            ranch=self.ranch,
            count_date=date(2025, 2, 3),
            species="cattle",
            expected_count=20,
            actual_count=19,
            difference=0,
            counted_by=self.staff,
            recorded_by=self.owner,
        )
        movement = MovementLog.objects.create(
            animal_tag=self.female,
            to_zone="North pasture",
            movement_date=date(2025, 2, 4),
            moved_by=self.staff,
            recorded_by=self.owner,
        )

        self.assertEqual(breeding.expected_delivery_date, date(2025, 10, 25))
        self.assertEqual(vaccination.animal_tag_id, "BORAN001")
        self.assertEqual(treatment.animal_tag_id, "BORAN001")
        self.assertEqual(herd_count.difference, -1)
        self.assertEqual(movement.animal_tag_id, "BORAN001")

    def test_mortality_event_updates_animal_status_without_rfid(self):
        mortality = Mortality.objects.create(
            animal_tag=self.female,
            death_date=date(2025, 2, 5),
            cause="Illness",
            recorded_by=self.owner,
        )
        self.female.refresh_from_db()

        self.assertEqual(self.female.status, "dead")
        self.assertIsNotNone(mortality.age_at_death_months)
