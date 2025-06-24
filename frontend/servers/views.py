from django.shortcuts import render

# Create your views here.
def servers(request):
    return render(request, 'servers/servers.html')
