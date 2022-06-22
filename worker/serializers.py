from rest_framework import serializers

from .models import Worker

class WorkersSerializer(serializers.ModelSerializer):
    def validate_manager(self, value):
        pass
    class Meta:
        model = Worker
        fields = ('user', 'department')
        extra_kwargs = {
            'user': {'required': True},
            'department': {'required': True}
        }