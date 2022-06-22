from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import DepartmentSerializer
from .models import Department
from worker.permissions import SupervisorAllActions
# Create your views here.
class DepartmentApiCreateListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()