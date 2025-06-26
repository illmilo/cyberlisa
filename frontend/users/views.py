from django.shortcuts import render
from django.middleware.csrf import get_token
from .models import Role, Action
from servers.models import Server  # Import Server model

def users(request):
    roles = Role.objects.all()
    actions = Action.objects.all()
    servers = Server.objects.all()  # Get all servers
    
    response = render(request, 'users/users.html', {
        'roles': roles,
        'actions': actions,
        'servers': servers  # Pass servers to template
    })

    response.set_cookie('csrftoken', get_token(request))
    
    return response