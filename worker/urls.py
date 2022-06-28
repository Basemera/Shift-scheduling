from django.urls import path
from .views import WorkersApiCreateListView, WorkersRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', WorkersApiCreateListView.as_view()),
    path('<pk>', WorkersRetrieveUpdateDestroyAPIView.as_view())
]