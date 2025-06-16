# example/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('servers/', views.servers, name='servers'),
    path('activity/', views.activity, name='activity'),
]