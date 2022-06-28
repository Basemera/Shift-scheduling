from django.urls import path
from .views import ShiftCreateApiView

urlpatterns = [
    path('shift/', ShiftCreateApiView.as_view())
]