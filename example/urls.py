# example/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard),
    path('users', views.users),
    path('servers', views.servers),
    path('activity', views.activity),
]