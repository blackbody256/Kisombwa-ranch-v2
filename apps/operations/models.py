import uuid
from django.db import models
from apps.core.models import Ranch, User, Staff
from apps.animals.models import Animal

class HerdCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='herd_counts')
    count_date = models.DateField(db_index=True)
    species = models.CharField(max_length=20)
    expected_count = models.IntegerField()
    actual_count = models.IntegerField()
    difference = models.IntegerField()
    grazing_zone = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    counted_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='counts_performed')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='count_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'herd_counts'
        ordering = ['-count_date']
        indexes = [
            models.Index(fields=['ranch', '-count_date']),
        ]
    
    def save(self, *args, **kwargs):
        self.difference = self.actual_count - self.expected_count
        super().save(*args, **kwargs)

class RFIDScanLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfid_code = models.CharField(max_length=100, db_index=True)
    animal_tag = models.ForeignKey(Animal, on_delete=models.SET_NULL, to_field='tag_number', null=True, blank=True, related_name='rfid_scans')
    gate_id = models.CharField(max_length=50, blank=True)
    scan_timestamp = models.DateTimeField(db_index=True)
    direction = models.CharField(max_length=10, blank=True)  # in/out
    signal_strength = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rfid_scan_logs'
        ordering = ['-scan_timestamp']
        indexes = [
            models.Index(fields=['gate_id', '-scan_timestamp']),
        ]

class MovementLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', null=True, blank=True, related_name='movements')
    group_name = models.CharField(max_length=100, blank=True)
    from_zone = models.CharField(max_length=100, blank=True)
    to_zone = models.CharField(max_length=100)
    movement_date = models.DateField(db_index=True)
    reason = models.CharField(max_length=200, blank=True)
    moved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements_performed')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movement_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movement_logs'
        ordering = ['-movement_date']
