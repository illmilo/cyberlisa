from django.urls import path
from . import views

urlpatterns = [
    path('', views.servers, name='servers'),
    path('api/create/', views.create_server, name='create_server'),
]