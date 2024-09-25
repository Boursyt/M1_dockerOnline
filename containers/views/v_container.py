from django.shortcuts import render
from containers.services.s_docker import DockerService
from django.http import JsonResponse
# #bouton qui utilise la fonction docker_run de la class DockerService
def start_container(request):
    return render(request, 'start.html')
def bouton_start(request):
    if request.method == 'POST':
        #on recupere les info du formulaire
        name=request.POST.get('container')
        image=request.POST.get('image')
        command=request.POST.get('command')
        environment=request.POST.get('env')
        ports_hote=request.POST.get('ports_hote')
        ports_rediriger=request.POST.get('ports_rediriger')
        volume=request.POST.get('volume')
        network=request.POST.get('network')
        if volume:
            volume = {volume: {'bind': '/path/in/container', 'mode': 'rw'}}
        ports = {ports_hote: ports_rediriger}
        if network:
            network = network
        #on crée un dictionnaire avec les info du formulaire

        fields = {
            'command': command,
            'environment': environment,
            'ports': ports,
            'volumes': volume,
            'network': network
        }
        # Filter out empty fields
        filtered_fields = {k: v for k, v in fields.items() if v}
        docker_service = DockerService(name, image, **filtered_fields)
        docker_create = docker_service.docker_create()
        container = docker_service.docker_run()

        # On renvoie le conteneur ou l'erreur sous forme de JSON
        return JsonResponse({'container': str(container)})
    return JsonResponse({'error': 'Invalid request'}, status=400)
