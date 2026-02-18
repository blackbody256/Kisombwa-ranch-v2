from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone

from apps.animals.models import Animal
from apps.breeding.models import BreedingEvent
from apps.health.models import Mortality, Vaccination


def build_dashboard_data():
    today = timezone.now().date()

    animals_by_species = list(
        Animal.objects.values("species").annotate(total=Count("tag_number")).order_by("species")
    )

    breeding_by_source_raw = Animal.objects.values("source").annotate(
        total_events=Count("breeding_as_dam"),
        conceived=Count(
            "breeding_as_dam",
            filter=Q(breeding_as_dam__pregnancy_confirmed="yes"),
        ),
    )

    breeding_by_source = []
    for row in breeding_by_source_raw:
        total_events = row["total_events"]
        conceived = row["conceived"]
        conception_rate = round((conceived / total_events) * 100, 2) if total_events else 0
        breeding_by_source.append(
            {
                "source": row["source"],
                "total_events": total_events,
                "conceived": conceived,
                "conception_rate": conception_rate,
            }
        )

    complete_group = BreedingEvent.objects.filter(
        female_tag__vaccinations__isnull=False
    ).distinct()
    incomplete_group = BreedingEvent.objects.filter(
        female_tag__vaccinations__isnull=True
    ).distinct()

    complete_total = complete_group.count()
    complete_yes = complete_group.filter(pregnancy_confirmed="yes").count()
    incomplete_total = incomplete_group.count()
    incomplete_yes = incomplete_group.filter(pregnancy_confirmed="yes").count()

    recent_breeding = BreedingEvent.objects.select_related("female_tag", "male_tag").order_by(
        "-service_date"
    )[:8]
    recent_vaccinations = Vaccination.objects.select_related("animal_tag").order_by(
        "-date_administered"
    )[:8]
    recent_mortality = Mortality.objects.select_related("animal_tag").order_by("-death_date")[:8]

    return {
        "kpis": {
            "total_animals": Animal.objects.count(),
            "active_animals": Animal.objects.filter(status="active").count(),
            "overdue_vaccinations": Vaccination.objects.filter(next_due_date__lt=today).count(),
            "recent_mortality_30_days": Mortality.objects.filter(
                death_date__gte=today - timedelta(days=30)
            ).count(),
        },
        "animals_by_species": animals_by_species,
        "breeding_by_source": breeding_by_source,
        "vaccination_correlation": {
            "complete_vaccination": {
                "total_events": complete_total,
                "conception_rate": round((complete_yes / complete_total) * 100, 2)
                if complete_total
                else 0,
            },
            "incomplete_vaccination": {
                "total_events": incomplete_total,
                "conception_rate": round((incomplete_yes / incomplete_total) * 100, 2)
                if incomplete_total
                else 0,
            },
        },
        "recent": {
            "breeding": recent_breeding,
            "vaccinations": recent_vaccinations,
            "mortality": recent_mortality,
        },
    }
