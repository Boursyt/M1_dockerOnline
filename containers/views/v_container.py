from django.shortcuts import render
# on va utiliser les fonction de la class DockerService /services/s_docker.py pour les utiliser depuis une interface web
#le tout dans la même page web

from containers.services.s_docker import DockerService
from django.http import JsonResponse
# #bouton qui utilise la fonction docker_run de la class DockerService
def start_container(request):
    return render(request, 'start.html')
def bouton_start(request):
    if request.method == 'POST':
        docker_service = DockerService(name='container1', image='hello-world')
        docker_create = docker_service.docker_create()
        container = docker_service.docker_run()

        # On renvoie le conteneur ou l'erreur sous forme de JSON
        return JsonResponse({'container': str(container)})
    return JsonResponse({'error': 'Invalid request'}, status=400)


