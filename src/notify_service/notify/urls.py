from django.urls import path
from .views import create_notify
urlpatterns = [
    path('create/', create_notify),
]