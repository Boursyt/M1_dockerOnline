from django.shortcuts import render
from containers.services.s_docker import DockerService
from django.http import JsonResponse


def liste_page(request):
    user = request.user

    if user.is_authenticated:
        context = {
            'menu': {
                'page': 'liste'
            }
        }
        return render(request, 'liste.html', context)
    else:
        return render(request, 'home.html')

def bouton_list(request):
    if request.method == 'POST':
        list_container = DockerService().docker_list()
        containers = [container.name for container in list_container]
        return render(request, 'liste.html', {'containers': containers})
    return JsonResponse({'error': 'Invalid request'}, status=400)
