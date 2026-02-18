import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Ranch Manager'),
        ('vet', 'Veterinarian'),
        ('herdsman', 'Herdsman'),
        ('admin', 'System Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='herdsman')
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

class Ranch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    size_hectares = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_ranches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ranches'
        verbose_name_plural = 'Ranches'
    
    def __str__(self):
        return self.name

class Staff(models.Model):
    ROLE_CHOICES = [
        ('herdsman', 'Herdsman'),
        ('vet', 'Veterinarian'),
        ('supervisor', 'Supervisor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_profile')
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='staff')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    hire_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff'
    
    def __str__(self):
        return f"{self.name} ({self.role})"

class SyncQueue(models.Model):
    OPERATION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sync_operations')
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    table_name = models.CharField(max_length=100)
    record_data = models.JSONField()
    timestamp = models.DateTimeField()
    synced = models.BooleanField(default=False)
    synced_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sync_queue'
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['device_id', 'synced', 'timestamp']),
        ]
