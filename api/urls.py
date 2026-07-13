from django.urls import path
from .views import validator_view

urlpatterns = [
    path('validator/', validator_view, name='validator'),
]