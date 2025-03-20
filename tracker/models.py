from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SupplementRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    supplement_name = models.CharField(max_length=200)
    intake_datetime = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    local_id = models.CharField(max_length=100, null=True, blank=True)  # For tracking local storage IDs

    class Meta:
        ordering = ['-intake_datetime']
