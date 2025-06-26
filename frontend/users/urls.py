from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .api import UserViewSet

from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', views.users, name='users'),
    path('api', include(router.urls)),
]