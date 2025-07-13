from django.urls import path
from . import views

urlpatterns = [
    path('', views.servers, name='servers'),
]