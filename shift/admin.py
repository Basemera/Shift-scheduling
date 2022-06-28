from django.contrib import admin

from shift.models import Shift, ShiftTime, WorkerSchedule

# Register your models here.
admin.site.register(Shift)
admin.site.register(ShiftTime)
admin.site.register(WorkerSchedule)
