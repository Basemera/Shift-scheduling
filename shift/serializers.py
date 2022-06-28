from datetime import datetime
from rest_framework import serializers
from .models import Shift, WorkerSchedule

class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = ('assigned_by', 'completed', 'shift_day', 'time', 'full')

    def validate_shift_day(self, value):
        if value < datetime.date(datetime.now()):
            message = 'date must be in the future'
            raise serializers.ValidationError(message)
        return value

        
class WorkerScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift')
