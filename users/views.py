from django.shortcuts import render

from .models import Roles

# Create your views here.
def users(request):
    roles = Roles.objects.all()
    return render(request, 'users/users.html', {'roles': roles})
