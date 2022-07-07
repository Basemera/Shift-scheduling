from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes as permission_class_decorator
from .serializers import WorkersSerializer
from .models import Worker
from .permissions import SupervisorAllActions
# Create your views here.

class WorkersApiCreateListView(ListCreateAPIView):
    """Create and list workers"""
    permission_classes = [IsAuthenticated, SupervisorAllActions]
    serializer_class = WorkersSerializer
    queryset = Worker.objects.all()


class WorkersRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve single worker instance, update and delete worker instance"""
    permission_classes = [IsAuthenticated]
    serializer_class = WorkersSerializer
    queryset = Worker.objects.all()

    @permission_class_decorator([SupervisorAllActions])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
