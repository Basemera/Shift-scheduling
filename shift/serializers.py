from datetime import datetime
from rest_framework import serializers
from .models import Shift, WorkerSchedule

class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = ('assigned_by', 'completed', 'shift_day', 'time', 'full','id')

    def validate_shift_day(self, value):
        if value < datetime.date(datetime.now()):
            message = 'date must be in the future'
            raise serializers.ValidationError(message)
        return value

        
class WorkerScheduleSerializer(serializers.ModelSerializer):
    shift = serializers.StringRelatedField()
    worker = serializers.StringRelatedField()
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift', 'clocked_in', 'clocked_out')
        read_only_fields = ('shift__assigned_by',)
        depth = 3

class ShiftSerializerWithoutAssignedByField(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = ('completed', 'shift_day', 'time', 'full','id')

class WorkerScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift')
        read_only_fields = ('clocked_in', 'clocked_out')
class WorkerScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift', 'clocked_in', 'clocked_out')
    def validate(self, data):
        if data['clocked_in'] and data['clocked_out']:
            if data['clocked_out'] < data['clocked_in']:
                message = 'Clocking out cannot happen before clocking in.'
                raise serializers.ValidationError(message)
        elif data['clocked_out'] and not data['clocked_in']:
            message = 'Clocking out cannot happen before clocking in.'
            raise serializers.ValidationError(message)
        return data

class WorkerScheduleClockinSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSchedule
        extra_kwargs = {
            'clocked_in': {'required': False},
            'clocked_out': {'required': False},
            'shift': {'required': False},
            'worker': {'required': False}
            }
        fields = ['shift', 'worker','clocked_in', 'clocked_out']
        read_only_fields = ['shift', 'worker']
 
class WorkerScheduleWorkerLogHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift', 'clocked_in', 'clocked_out')
        read_only_fields = ('shift__assigned_by',)
        depth = 1

    def validate(self, data):
        if data['end'] < data['start']:
            message = 'Clocking out cannot happen before clocking in.'
            raise serializers.ValidationError(message)
        return data