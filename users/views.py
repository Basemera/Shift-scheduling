from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User

# Create your views here.
class UsersApiCreateListView(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()