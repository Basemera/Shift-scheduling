from codecs import ignore_errors
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from shift.models import Shift, WorkerSchedule
from worker.models import Worker
from worker.permissions import SupervisorAllActions
from .serializers import ShiftSerializer, ShiftSerializerWithoutAssignedByField, WorkerScheduleCreateSerializer, WorkerScheduleSerializer, WorkerScheduleUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes as permission_class_decorator

# Create your views here.
class ShiftCreateApiView(ListCreateAPIView):
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

class ShiftRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()

    @permission_class_decorator([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ["update", "PUT", "PATCH"]:
            return ShiftSerializerWithoutAssignedByField
        return self.serializer_class

class WorkerShceduleCreateListApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = WorkerScheduleSerializer
    queryset = WorkerSchedule.objects.all()
    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method in ["POST"]:
            return WorkerScheduleCreateSerializer
        return self.serializer_class

    @permission_class_decorator([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        shift_id = request.data.get('shift')
        l = []
        if isinstance(request.data.get('worker'), list):
            d = {}
            print(request.data.get('worker'))
            for i in request.data.get('worker'):
                l.append(
                    {
                        "worker": i,
                        "shift": shift_id
                    }
                )
            serializer = self.get_serializer(data=l, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return super().create(request, *args, **kwargs)

class WorkScheduleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = WorkerScheduleUpdateSerializer
    queryset = WorkerSchedule.objects.all()

    @permission_class_decorator([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        schedule = WorkerSchedule.objects.get(pk=kwargs['pk'])
        if schedule:
            shift = schedule.shift
            if shift.completed:
                return Response({"message":"Cannot delete an entry from a completed shift"})
        return super().delete(request, *args, **kwargs)