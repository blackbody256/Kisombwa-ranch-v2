from datetime import date, timedelta

from django.core.management.base import BaseCommand

from apps.analytics.models import SystemMetric
from apps.animals.models import Animal
from apps.breeding.models import BreedingEvent
from apps.core.models import Ranch, Staff, User
from apps.health.models import Mortality, Treatment, Vaccination
from apps.operations.models import HerdCount, MovementLog


class Command(BaseCommand):
    help = "Seed database with realistic KRIS demo data (idempotent)"

    def _upsert_user(self, username, email, password, role, is_superuser=False):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "role": role},
        )
        if created:
            user.email = email
            user.role = role
            user.is_staff = is_superuser or role in {"admin", "manager"}
            user.is_superuser = is_superuser
            user.set_password(password)
            user.save()
        return user

    def _upsert_animal(self, ranch, tag, source, sex, birth_year):
        defaults = {
            "ranch": ranch,
            "species": "cattle",
            "breed": "Boran",
            "sex": sex,
            "date_of_birth": date(birth_year, 3, 1),
            "source": source,
            "status": "active",
        }
        animal, _ = Animal.objects.update_or_create(tag_number=tag, defaults=defaults)
        return animal

    def handle(self, *args, **kwargs):
        today = date.today()

        admin = self._upsert_user("admin", "admin@kisombwa.com", "admin123", "admin", True)
        manager = self._upsert_user("manager", "manager@kisombwa.com", "manager123", "manager")
        vet_user = self._upsert_user("vet", "vet@kisombwa.com", "vet12345", "vet")

        ranch, _ = Ranch.objects.update_or_create(
            name="Kisombwa Ranching Scheme",
            defaults={
                "location": "Kitenga Sub County, Mubende District, Uganda",
                "size_hectares": 2400,
                "owner": admin,
            },
        )

        herdsman, _ = Staff.objects.update_or_create(
            ranch=ranch,
            name="John Mugisha",
            defaults={"role": "herdsman", "phone_number": "+256700123456", "user": None},
        )
        vet_staff, _ = Staff.objects.update_or_create(
            ranch=ranch,
            name="Sarah Namukasa",
            defaults={"role": "vet", "phone_number": "+256700222333", "user": vet_user},
        )

        # Build a balanced herd with clear local vs imported cohorts for analytics.
        local_females = [
            self._upsert_animal(ranch, f"LOCF{i:03d}", "born", "female", 2022) for i in range(1, 9)
        ]
        imported_females = [
            self._upsert_animal(ranch, f"IMPF{i:03d}", "imported", "female", 2021)
            for i in range(1, 9)
        ]
        for i in range(1, 5):
            self._upsert_animal(ranch, f"LOCM{i:03d}", "born", "male", 2021)
            self._upsert_animal(ranch, f"IMPM{i:03d}", "imported", "male", 2020)
        bull = self._upsert_animal(ranch, "BULL001", "born", "male", 2020)

        def ensure_vaccination(animal, offset_days, overdue=False):
            administered = today - timedelta(days=offset_days)
            due_date = today - timedelta(days=7) if overdue else today + timedelta(days=120)
            Vaccination.objects.get_or_create(
                animal_tag=animal,
                vaccine_type="FMD",
                date_administered=administered,
                defaults={
                    "disease_targeted": "Foot and Mouth Disease",
                    "administered_by": vet_staff,
                    "next_due_date": due_date,
                    "batch_number": "FMD-2026-A",
                    "location": "Neck",
                    "cost": 4.50,
                    "recorded_by": manager,
                },
            )

        def ensure_breeding_event(female, service_offset, confirmed):
            service_date = today - timedelta(days=service_offset)
            BreedingEvent.objects.get_or_create(
                female_tag=female,
                service_date=service_date,
                defaults={
                    "male_tag": bull,
                    "method": "natural",
                    "pregnancy_confirmed": confirmed,
                    "pregnancy_check_date": service_date + timedelta(days=45),
                    "recorded_by": manager,
                    "notes": "Seeded demo breeding event",
                },
            )

        # Local animals: high vaccination coverage and higher conception.
        for idx, female in enumerate(local_females, start=1):
            ensure_vaccination(female, offset_days=120 + idx, overdue=False)
            ensure_breeding_event(
                female=female,
                service_offset=260 - (idx * 4),
                confirmed="yes" if idx <= 6 else "no",
            )

        # Imported animals: lower vaccination coverage and weaker conception.
        for idx, female in enumerate(imported_females, start=1):
            if idx <= 2:
                ensure_vaccination(female, offset_days=180 + idx, overdue=True)
            ensure_breeding_event(
                female=female,
                service_offset=255 - (idx * 3),
                confirmed="yes" if idx <= 3 else "no",
            )

        # Health/treatment records.
        for animal, diagnosis, days_ago in [
            (local_females[0], "Mastitis", 25),
            (imported_females[3], "Tick fever", 16),
            (imported_females[6], "Respiratory infection", 9),
        ]:
            Treatment.objects.get_or_create(
                animal_tag=animal,
                treatment_date=today - timedelta(days=days_ago),
                defaults={
                    "diagnosis": diagnosis,
                    "medication_given": "Broad-spectrum antibiotic",
                    "dosage": "20ml",
                    "treated_by": vet_staff,
                    "follow_up_required": True,
                    "follow_up_date": today - timedelta(days=days_ago - 7),
                    "cost": 12.00,
                    "notes": "Seeded demo treatment",
                    "recorded_by": manager,
                },
            )

        # One recent mortality to power dashboard KPI.
        Mortality.objects.get_or_create(
            animal_tag=imported_females[7],
            death_date=today - timedelta(days=11),
            defaults={
                "cause": "Complications after illness",
                "vet_confirmed": True,
                "carcass_disposed": True,
                "estimated_value": 380.00,
                "notes": "Seeded demo mortality",
                "recorded_by": manager,
            },
        )

        for days_ago, expected, actual in [(4, 24, 23), (2, 24, 24), (1, 24, 22)]:
            HerdCount.objects.get_or_create(
                ranch=ranch,
                count_date=today - timedelta(days=days_ago),
                species="cattle",
                defaults={
                    "expected_count": expected,
                    "actual_count": actual,
                    "difference": actual - expected,
                    "grazing_zone": "North paddock",
                    "notes": "Seeded demo herd count",
                    "counted_by": herdsman,
                    "recorded_by": manager,
                },
            )

        for animal, from_zone, to_zone, days_ago in [
            (local_females[1], "Zone A", "Zone B", 6),
            (imported_females[1], "Quarantine", "Zone C", 5),
            (local_females[4], "Zone B", "Milking area", 2),
        ]:
            MovementLog.objects.get_or_create(
                animal_tag=animal,
                movement_date=today - timedelta(days=days_ago),
                to_zone=to_zone,
                defaults={
                    "group_name": "Main Herd",
                    "from_zone": from_zone,
                    "reason": "Scheduled rotation",
                    "moved_by": herdsman,
                    "recorded_by": manager,
                },
            )

        SystemMetric.objects.update_or_create(
            ranch=ranch,
            metric_type="conception_rate_local",
            calculation_date=today,
            defaults={"metric_value": 75.0, "metadata": {"source": "seed_data"}},
        )
        SystemMetric.objects.update_or_create(
            ranch=ranch,
            metric_type="conception_rate_imported",
            calculation_date=today,
            defaults={"metric_value": 37.5, "metadata": {"source": "seed_data"}},
        )
        SystemMetric.objects.update_or_create(
            ranch=ranch,
            metric_type="overdue_vaccinations",
            calculation_date=today,
            defaults={"metric_value": 2, "metadata": {"source": "seed_data"}},
        )

        self.stdout.write(self.style.SUCCESS("Database seeded with realistic KRIS demo data."))
