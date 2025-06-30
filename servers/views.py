from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Server
from .serializers import ServerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

def servers(request):
    servers = Server.objects.all()  # Get all servers for the template
    return render(request, 'servers/servers.html', {'servers': servers})

@api_view(['POST'])
def create_server(request):
    serializer = ServerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)