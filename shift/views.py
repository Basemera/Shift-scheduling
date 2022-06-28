from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from shift.models import Shift
from worker.models import Worker
from worker.permissions import SupervisorAllActions
from .serializers import ShiftSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ShiftCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()

    def create(self, request, *args, **kwargs):
        assigned_by = request.user
        data = {
            "assigned_by": assigned_by.id,
            **request.data
        }
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
