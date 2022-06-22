from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'manager']
        extra_kwargs = {
            'name': {'required': True},
            'manager': {'required': True}
        }