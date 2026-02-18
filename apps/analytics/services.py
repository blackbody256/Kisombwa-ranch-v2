from datetime import timedelta

from django.db.models import Count, Q, Sum
from django.utils import timezone

from apps.animals.models import Animal
from apps.breeding.models import BreedingEvent
from apps.health.models import Mortality, Treatment, Vaccination
from apps.operations.models import HerdCount


def _pct(numerator, denominator):
    if not denominator:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def _money(value):
    return float(value or 0)


def _by_source_metrics(source):
    label_map = {"born": "Local", "imported": "Imported"}
    breeding_qs = BreedingEvent.objects.filter(female_tag__source=source)
    total_events = breeding_qs.count()
    conceived = breeding_qs.filter(pregnancy_confirmed="yes").count()
    stillbirths = breeding_qs.filter(outcome="stillbirth").count()

    animals_in_source = Animal.objects.filter(source=source).count()
    source_deaths = Mortality.objects.filter(animal_tag__source=source).count()

    return {
        "source": source,
        "label": label_map.get(source, source.capitalize()),
        "total_events": total_events,
        "conceived": conceived,
        "conception_rate": _pct(conceived, total_events),
        "stillbirth_rate": _pct(stillbirths, total_events),
        "calf_survival_rate": round(100 - _pct(source_deaths, animals_in_source), 2),
    }


def build_dashboard_data():
    today = timezone.now().date()

    total_animals = Animal.objects.count()
    active_animals = Animal.objects.filter(status="active").count()
    overdue_vaccinations = Vaccination.objects.filter(next_due_date__lt=today).count()
    recent_mortality_30_days = Mortality.objects.filter(
        death_date__gte=today - timedelta(days=30)
    ).count()

    animals_by_species = list(
        Animal.objects.values("species").annotate(total=Count("tag_number")).order_by("species")
    )

    imported = _by_source_metrics("imported")
    local = _by_source_metrics("born")

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

    animals_with_treatment = BreedingEvent.objects.filter(
        female_tag__treatments__isnull=False
    ).distinct()
    animals_without_treatment = BreedingEvent.objects.filter(
        female_tag__treatments__isnull=True
    ).distinct()

    with_treatment_total = animals_with_treatment.count()
    with_treatment_yes = animals_with_treatment.filter(pregnancy_confirmed="yes").count()
    without_treatment_total = animals_without_treatment.count()
    without_treatment_yes = animals_without_treatment.filter(pregnancy_confirmed="yes").count()

    imported_female_count = Animal.objects.filter(source="imported", sex="female").count()
    imported_overdue = Animal.objects.filter(
        source="imported", sex="female", vaccinations__next_due_date__lt=today
    ).distinct().count()

    gap = round(local["conception_rate"] - imported["conception_rate"], 2)
    estimated_recoverable_pregnancies = round((gap / 100) * imported["total_events"], 1)

    vaccine_cost = _money(Vaccination.objects.aggregate(total=Sum("cost"))["total"])
    treatment_cost = _money(Treatment.objects.aggregate(total=Sum("cost"))["total"])
    mortality_loss = _money(Mortality.objects.aggregate(total=Sum("estimated_value"))["total"])

    live_birth_events = BreedingEvent.objects.filter(outcome="live_birth").count()
    assumed_calf_value = 320.0
    estimated_revenue = round(live_birth_events * assumed_calf_value, 2)
    total_costs = round(vaccine_cost + treatment_cost + mortality_loss, 2)
    roi_percent = _pct(estimated_revenue - total_costs, total_costs) if total_costs else 0.0

    latest_herd_count = (
        HerdCount.objects.order_by("-count_date").values(
            "count_date", "expected_count", "actual_count", "difference"
        ).first()
    )

    recent_breeding = list(
        BreedingEvent.objects.select_related("female_tag", "male_tag")
        .order_by("-service_date")
        .values("female_tag_id", "male_tag_id", "service_date", "pregnancy_confirmed")[:10]
    )
    recent_vaccinations = list(
        Vaccination.objects.select_related("animal_tag")
        .order_by("-date_administered")
        .values("animal_tag_id", "vaccine_type", "date_administered", "next_due_date")[:10]
    )
    recent_mortality = list(
        Mortality.objects.select_related("animal_tag")
        .order_by("-death_date")
        .values("animal_tag_id", "death_date", "cause", "estimated_value")[:10]
    )

    return {
        "kpis": {
            "total_animals": total_animals,
            "active_animals": active_animals,
            "overdue_vaccinations": overdue_vaccinations,
            "recent_mortality_30_days": recent_mortality_30_days,
            "last_count_difference": latest_herd_count["difference"] if latest_herd_count else 0,
        },
        "breeding_analyzer": {
            "comparison": [imported, local],
            "root_cause": {
                "message": f"{imported_overdue}/{imported_female_count or 1} imported females have overdue vaccination schedules.",
                "correlation_impact": gap,
            },
            "recommendation": {
                "action": "Complete imported cohort vaccination and repeat pregnancy checks after 45 days.",
                "estimated_recoverable_pregnancies": estimated_recoverable_pregnancies,
            },
        },
        "health_correlation": {
            "vaccination_vs_conception": {
                "complete": {
                    "total_events": complete_total,
                    "conception_rate": _pct(complete_yes, complete_total),
                },
                "incomplete": {
                    "total_events": incomplete_total,
                    "conception_rate": _pct(incomplete_yes, incomplete_total),
                },
            },
            "treatment_history_vs_conception": {
                "with_treatment": {
                    "total_events": with_treatment_total,
                    "conception_rate": _pct(with_treatment_yes, with_treatment_total),
                },
                "without_treatment": {
                    "total_events": without_treatment_total,
                    "conception_rate": _pct(without_treatment_yes, without_treatment_total),
                },
            },
        },
        "herd_overview": {
            "animals_by_species": animals_by_species,
            "latest_count": latest_herd_count,
        },
        "financial_performance": {
            "vaccine_cost": round(vaccine_cost, 2),
            "treatment_cost": round(treatment_cost, 2),
            "mortality_loss": round(mortality_loss, 2),
            "total_costs": total_costs,
            "estimated_revenue": estimated_revenue,
            "roi_percent": roi_percent,
        },
        "chart_data": {
            "breeding_comparison": {
                "labels": ["Imported", "Local"],
                "conception_rate": [imported["conception_rate"], local["conception_rate"]],
                "stillbirth_rate": [imported["stillbirth_rate"], local["stillbirth_rate"]],
                "calf_survival_rate": [imported["calf_survival_rate"], local["calf_survival_rate"]],
            },
            "health_correlation": {
                "labels": [
                    "Complete Vaccination",
                    "Incomplete Vaccination",
                    "With Treatment History",
                    "No Treatment History",
                ],
                "conception_rate": [
                    _pct(complete_yes, complete_total),
                    _pct(incomplete_yes, incomplete_total),
                    _pct(with_treatment_yes, with_treatment_total),
                    _pct(without_treatment_yes, without_treatment_total),
                ],
            },
        },
        "recent": {
            "breeding": recent_breeding,
            "vaccinations": recent_vaccinations,
            "mortality": recent_mortality,
        },
    }
