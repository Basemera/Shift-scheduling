import json
from django.db import models
from datetime import datetime, timedelta, date
from users.models import User
from worker.models import Worker
# Create your models here.

class ShiftTime(models.Model):
    time = models.CharField('Shift Time', max_length=30, unique=True)
    def get_shift_time(self):
        if self.time == '0-8':
            return 8
        elif self.time == '8-16':
            return 16
        else:
            return 24
    def __str__(self) -> str:
        return '%d: %s'%(self.id, self.time)


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

    def shift_start_time(self):        
        shift_day = self.shift_day
        previous_day = shift_day - timedelta(days=1)
        midnight = datetime.combine(previous_day, datetime.min.time())
        if self.time.time == '0-8':
            return midnight + timedelta(hours=0)
        elif self.time.time == '8-16':
            return midnight + timedelta(hours=8)
        elif self.time.time == '16-24':
            return midnight + timedelta(hours=16)

    def __str__(self) -> str:
        d = {
            'id': self.id,
            'shift_day': self.shift_day,
            'time': self.time,
            'assigned_by':self.assigned_by,
            'completed':self.completed
        }
        return '%s'% (json.dumps(d, indent = 4, sort_keys = True, default = str))


class WorkerSchedule(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, blank=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=False)
    clocked_in = models.DateTimeField(blank=True, null=True)
    clocked_out = models.DateTimeField(blank=True, null=True)

    def clocked_in_time(self):
        current_time = datetime.now()

        if current_time < self.shift.shift_start_time():
            return False
        return self.shift.shift_start_time()

    def clockout_time(self):
        current_time = datetime.now()

        if current_time < self.shift.shift_start_time() + timedelta(hours=8) or self.clocked_in == None:
            return False
        return self.shift.shift_start_time() + timedelta(hours=8)
