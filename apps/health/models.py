import uuid
from django.db import models
from apps.animals.models import Animal
from apps.core.models import User, Staff

class Vaccination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='vaccinations')
    vaccine_type = models.CharField(max_length=100)
    disease_targeted = models.CharField(max_length=100, blank=True)
    date_administered = models.DateField(db_index=True)
    administered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='vaccinations_administered')
    next_due_date = models.DateField(null=True, blank=True, db_index=True)
    batch_number = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vaccination_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vaccinations'
        ordering = ['-date_administered']
        indexes = [
            models.Index(fields=['animal_tag', '-date_administered']),
        ]

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='treatments')
    diagnosis = models.CharField(max_length=200, blank=True)
    symptoms = models.TextField(blank=True)
    medication_given = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    treatment_date = models.DateField(db_index=True)
    treated_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='treatments_administered')
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='treatment_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'treatments'
        ordering = ['-treatment_date']
        indexes = [
            models.Index(fields=['animal_tag', '-treatment_date']),
        ]

class Mortality(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='mortality_record')
    death_date = models.DateField(db_index=True)
    age_at_death_months = models.IntegerField(null=True, blank=True)
    cause = models.CharField(max_length=200, blank=True)
    vet_confirmed = models.BooleanField(default=False)
    carcass_disposed = models.BooleanField(default=False)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mortality_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mortality'
        ordering = ['-death_date']
    
    def save(self, *args, **kwargs):
        # Auto-calculate age at death
        if self.animal_tag.date_of_birth:
            from dateutil.relativedelta import relativedelta
            delta = relativedelta(self.death_date, self.animal_tag.date_of_birth)
            self.age_at_death_months = delta.years * 12 + delta.months
        
        # Update animal status
        self.animal_tag.status = 'dead'
        self.animal_tag.save()
        
        super().save(*args, **kwargs)
