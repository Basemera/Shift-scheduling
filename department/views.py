from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes as permission_class_decorator
from .serializers import DepartmentSerializer
from .models import Department
from worker.permissions import SupervisorAllActions
# Create your views here.
class DepartmentApiCreateListView(ListCreateAPIView):
    """Create department and list departments"""
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class DepartmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve single department instance, update and delete department"""
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    @permission_class_decorator([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
