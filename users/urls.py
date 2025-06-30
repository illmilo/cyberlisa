from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UserViewSet
from . import views

router = DefaultRouter()
# basename is singular
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', views.users, name='users'),
    path('api/', include(router.urls)),

    # json handling
    path('json/', views.user_json_list, name='user-json-list'),
    path('json/create/', views.user_json_create, name='user-json-create'),
]
