import uuid
from django.db import models
from datetime import timedelta
from apps.animals.models import Animal
from apps.core.models import User

class BreedingEvent(models.Model):
    METHOD_CHOICES = [
        ('natural', 'Natural Service'),
        ('artificial_insemination', 'Artificial Insemination'),
    ]
    PREGNANCY_CHOICES = [
        ('pending', 'Pending'),
        ('yes', 'Confirmed Pregnant'),
        ('no', 'Not Pregnant'),
    ]
    OUTCOME_CHOICES = [
        ('live_birth', 'Live Birth'),
        ('stillbirth', 'Stillbirth'),
        ('abortion', 'Abortion'),
        ('failed_conception', 'Failed Conception'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    female_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='breeding_as_dam')
    male_tag = models.ForeignKey(Animal, on_delete=models.SET_NULL, to_field='tag_number', null=True, blank=True, related_name='breeding_as_sire')
    semen_batch_id = models.CharField(max_length=100, blank=True)
    
    # Breeding timeline
    heat_detected_date = models.DateField(null=True, blank=True)
    service_date = models.DateField(db_index=True)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    
    # Pregnancy tracking
    pregnancy_confirmed = models.CharField(max_length=20, choices=PREGNANCY_CHOICES, default='pending')
    pregnancy_check_date = models.DateField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True, db_index=True)
    
    # Outcome tracking
    actual_delivery_date = models.DateField(null=True, blank=True)
    outcome = models.CharField(max_length=30, choices=OUTCOME_CHOICES, blank=True)
    number_of_offspring = models.IntegerField(default=1)
    offspring_tags = models.TextField(blank=True)  # Comma-separated
    
    # Metadata
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='breeding_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'breeding_events'
        ordering = ['-service_date']
        indexes = [
            models.Index(fields=['female_tag', '-service_date']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-calculate expected delivery date based on species
        if self.service_date and not self.expected_delivery_date:
            gestation_days = {
                'cattle': 283,
                'goat': 150,
                'sheep': 147,
            }
            days = gestation_days.get(self.female_tag.species, 283)
            self.expected_delivery_date = self.service_date + timedelta(days=days)
        
        super().save(*args, **kwargs)
