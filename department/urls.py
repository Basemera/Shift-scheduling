from django.urls import path
from .views import DepartmentApiCreateListView

urlpatterns = [
    path('', DepartmentApiCreateListView.as_view())
]