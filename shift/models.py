from operator import mod
from django.db import models
from enum import Enum

from users.models import User
# Create your models here.

class ShiftTime(models.Model):
    time = models.CharField('Shift Time', max_length=30, unique=True)
class Shift(models.Model):
    assigned_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, related_name='Supervisor')
    completed = models.BooleanField(blank=True, default=False)
    full = models.BooleanField(blank=True, default=False)
    shift_day = models.DateField(blank=False)
    time = models.ForeignKey(ShiftTime, on_delete=models.DO_NOTHING, blank=False)

    def completion_status(self):
        return self.completed

    def shift_time(self):
        return self.time.time

class WorkerSchedule(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, blank=False)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    clocked_in = models.DateTimeField(blank=True, null=True)
    clocked_out = models.DateTimeField(blank=True, null=True)

