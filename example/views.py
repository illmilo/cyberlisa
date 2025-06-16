# example/views.py
from django.shortcuts import render

def dashboard(request):
    return render(request, 'example/dashboard.html')
def users(request):
    return render(request, 'example/users.html')
def servers(request):
    return render(request, 'example/servers.html')
def activity(request):
    return render(request, 'example/activity.html')