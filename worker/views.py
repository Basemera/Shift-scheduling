from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import WorkersSerializer
from .models import Worker
from .permissions import SupervisorAllActions
# Create your views here.
class WorkersApiCreateListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = WorkersSerializer
    queryset = Worker.objects.all()
