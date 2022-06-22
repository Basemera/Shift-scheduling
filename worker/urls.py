from django.urls import path
from .views import WorkersApiCreateListView

urlpatterns = [
    path('', WorkersApiCreateListView.as_view())
]