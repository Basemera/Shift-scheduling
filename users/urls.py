from django.urls import path
from .views import UsersApiCreateListView

urlpatterns = [
    path('', UsersApiCreateListView.as_view())
]