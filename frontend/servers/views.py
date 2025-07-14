from django.shortcuts import render
def servers(request):
    print("hello")
    return render(request, 'servers/servers.html')
