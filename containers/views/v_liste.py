from django.shortcuts import render
from containers.services.s_docker import DockerService
from django.http import JsonResponse


def liste_page(request):
    return render(request, 'liste.html')

def bouton_list(request):
    if request.method == 'POST':
        list_container = DockerService().docker_list()
        containers = [container.name for container in list_container]
        return render(request, 'liste.html', {'containers': containers})
    return JsonResponse({'error': 'Invalid request'}, status=400)
