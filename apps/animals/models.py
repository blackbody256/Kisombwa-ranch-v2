import uuid
from django.db import models
from apps.core.models import Ranch

class Animal(models.Model):
    SPECIES_CHOICES = [
        ('cattle', 'Cattle'),
        ('goat', 'Goat'),
        ('sheep', 'Sheep'),
    ]
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    SOURCE_CHOICES = [
        ('born', 'Born on Ranch'),
        ('purchased', 'Purchased'),
        ('imported', 'Imported'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('dead', 'Dead'),
        ('missing', 'Missing'),
    ]
    
    # NATURAL PRIMARY KEY - Ranch's tag number
    tag_number = models.CharField(max_length=50, primary_key=True)
    
    # Optional identification methods
    rfid_code = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    qr_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # Core attributes
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='animals')
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    
    # Lineage (self-referencing)
    dam_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring_as_dam')
    sire_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring_as_sire')
    
    # Status & metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    photo = models.ImageField(upload_to='animals/', blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'animals'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['species', 'status']),
        ]
    
    def __str__(self):
        return f"{self.tag_number} ({self.species})"
    
    @property
    def age_months(self):
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        return (today.year - self.date_of_birth.year) * 12 + today.month - self.date_of_birth.month
