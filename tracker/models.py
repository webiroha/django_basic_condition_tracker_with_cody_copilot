from django.db import models
from django.utils import timezone

class SupplementRecord(models.Model):
    supplement_name = models.CharField(max_length=200)
    intake_datetime = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()

    class Meta:
        ordering = ['-intake_datetime']
