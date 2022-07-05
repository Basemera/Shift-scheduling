from django.shortcuts import render
import csv
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from shift.models import Shift, WorkerSchedule
from worker.models import Worker
from worker.permissions import SupervisorAllActions
from .serializers import ShiftSerializer, ShiftSerializerWithoutAssignedByField, WorkerScheduleCreateSerializer, WorkerScheduleSerializer, WorkerScheduleUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes as permission_class_decorator
from .filters import WorkerScheduleFilter 
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
            shift = Shift.objects.get(pk=shift_id)
            schedule = WorkerSchedule.objects.filter(shift_shift_day=shift.shift_day)
            for i in request.data.get('worker'):
                shift = Shift.objects.get(pk=shift_id)
                schedule = WorkerSchedule.objects.filter(shift__shift_day=shift.shift_day, worker=i)
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

        shift = Shift.objects.get(pk=shift_id)
        schedule = WorkerSchedule.objects.filter(shift__shift_day=shift.shift_day, worker=request.data.get('worker'))
        if len(schedule) != 0:
            return Response({"message":"User already has assigned shift"}, status=status.HTTP_400_BAD_REQUEST)
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

class WorkerScheduleSearchApiView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = WorkerScheduleSerializer
    filterset_class = WorkerScheduleFilter

    queryset = WorkerSchedule.objects.all()
    def get_queryset(self):
        # print(self.request.GET)

        if not bool(self.request.GET):
            return WorkerSchedule.objects.none()
        query_params = self.request.GET
        non_supported_field = []
        for i in query_params:
            if i not in self.filterset_class.get_filters():
                non_supported_field.append(i)
                # return WorkerSchedule.objects.none()
        if len(query_params) == len(non_supported_field):
            return WorkerSchedule.objects.none()
        return WorkerSchedule.objects.all()

class WorkerScheduleDownloadApiView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = WorkerScheduleSerializer
    filterset_class = WorkerScheduleFilter

    queryset = WorkerSchedule.objects.all()
    def get_queryset(self):
        # print(self.request.GET)

        if not bool(self.request.GET):
            return WorkerSchedule.objects.none()
        query_params = self.request.GET
        non_supported_field = []
        for i in query_params:
            if i not in self.filterset_class.get_filters():
                non_supported_field.append(i)
                # return WorkerSchedule.objects.none()
        if len(query_params) == len(non_supported_field):
            return WorkerSchedule.objects.none()
        return WorkerSchedule.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="worker_schedule.csv"'},
            )
        writer = csv.writer(response)
        k = (list(queryset.values()))
        row_1 = (list(k[0].keys()))
        writer.writerow(row_1)
        for i in (queryset.values()):
            print(type(i.values()))
            print(list(i.values()))
            row = []
            for p in list(i.values()):
                if (isinstance(p, int)):
                    row.append(str(p))
                else:
                    row.append(p)
            writer.writerow(
                row
            )            
        return response