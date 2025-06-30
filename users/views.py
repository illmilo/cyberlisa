from django.shortcuts import render
from django.middleware.csrf import get_token
from .models import Role, Action, User
from servers.models import Server

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .api import UserSerializer

from rest_framework import status


def users(request):
    roles = Role.objects.all()
    actions = Action.objects.all()
    servers = Server.objects.all()
    users = User.objects.all()

    response = render(request, 'users/users.html', {
        'roles': roles,
        'actions': actions,
        'servers': servers,
        'users': users,
    })

    response.set_cookie('csrftoken', get_token(request))

    return response

@api_view(['GET'])
def user_json_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def user_json_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)