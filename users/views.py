from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes as permission_class_decorator

from .serializers import UserSerializer
from .models import User
# Create your views here.

class UsersApiCreateListView(ListCreateAPIView):
    """Create and view users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @permission_class_decorator([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
