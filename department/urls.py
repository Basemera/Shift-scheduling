from django.urls import path
from .views import DepartmentApiCreateListView, DepartmentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', DepartmentApiCreateListView.as_view()),
    path('<pk>/', DepartmentRetrieveUpdateDestroyAPIView.as_view())
]
