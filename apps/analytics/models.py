import uuid
from django.db import models
from apps.core.models import Ranch

class SystemMetric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='metrics')
    metric_type = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=10, decimal_places=2)
    calculation_date = models.DateField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'system_metrics'
        ordering = ['-calculation_date']
        indexes = [
            models.Index(fields=['ranch', 'metric_type', '-calculation_date']),
        ]
