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
    shift = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='shift_day'
    )
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift', 'clocked_in', 'clocked_out')

class ShiftSerializerWithoutAssignedByField(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = ('completed', 'shift_day', 'time', 'full','id')

class WorkerScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift')
        read_only_fields = ('clocked_in', 'clocked_out')

# def validate_clocked_out(clocked_in, clocked_out):
#         if clocked_out < clocked_in:
#             message = 'Clocking out cannot happen before clocking in.' % clocked_in
#             raise serializers.ValidationError(message)
class WorkerScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSchedule
        fields = ('worker', 'shift', 'clocked_in', 'clocked_out')
        # validator = [
        #     validate_clocked_out('clocked_in', 'clocked_out')
        # ]
    def validate(self, data):
        if data['clocked_in'] and data['clocked_out']:
            if data['clocked_out'] < data['clocked_in']:
                message = 'Clocking out cannot happen before clocking in.'
                raise serializers.ValidationError(message)
        elif data['clocked_out'] and not data['clocked_in']:
            message = 'Clocking out cannot happen before clocking in.'
            raise serializers.ValidationError(message)
        return data
    
