from django.shortcuts import render
from django.conf import settings

def users(request):
    """Render the HTML page only"""
    return render(request, "users/users.html")
