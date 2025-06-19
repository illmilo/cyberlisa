from django.shortcuts import render

from .models import Roles, Actions

# Create your views here.
def users(request):
    roles = Roles.objects.all()
    actions = Actions.objects.all()
    return render(request, 'users/users.html', {'roles': roles, 'actions': actions})
