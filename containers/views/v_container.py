from lib2to3.fixes.fix_input import context
from django.shortcuts import render, redirect
from containers.services.s_docker import DockerService
from filemanager.views.v_file import listeFile
from django.http import JsonResponse
import yaml
# #bouton qui utilise la fonction docker_run de la class DockerService
def start_container(request):
    """
    Fonction pour rendre la page de creation de conteneur /container/
    :param request:
    :return: render de la page de creation de conteneur
    """
    user = request.user
    fileListe = listeFile(request)

    if user.is_authenticated:
        context = {
            'menu': {
                'page': 'create'
            },
            'files':fileListe
        }
        return render(request, 'start.html', context)
    else:
        return redirect('/home')



def container(request):
    """
    Fonction qui permet de creer un conteneur avec les info du formulaire. redirect sur la page de liste de conteneur
    :param request:
    :return: redirect sur la page de liste de conteneur
    """
    if request.method == 'POST':

        try:
            #on recupere les info du formulaire
            name = request.POST.get('name')
            image = request.POST.get('image')
            command = request.POST.get('command')
            ports_hote = request.POST.get('ports_hote')
            ports_rediriger = DockerService().counter()
            volume = request.POST.get('volume')
            user = (request.user)
            name=name.lower()
            name=(f'{user}-{name}')
            if volume:
                volume = {volume: {'bind': f'/volume/{user}/', 'mode': 'rw'}}
            ports = {ports_hote: ports_rediriger}


            #on crée un dictionnaire avec les info du formulaire
            fields = {
                'command': command,
                'ports': ports,
                'volumes': volume,
            }
            # Filter out empty fields
            filtered_fields = {k: v for k, v in fields.items() if v}
            docker_service = DockerService(name, image, **filtered_fields)
            docker_create = docker_service.docker_create(request)
            container = docker_service.docker_run(name)

            # On renvoie le conteneur ou l'erreur sous forme de JSON
            return redirect('/container/liste/')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def dockerfile(request):
    """
    Fonction qui permet de creer un conteneur avec un Dockerfile. redirect sur la page de liste de conteneur
    :param request:
    :return: redirect sur la page de liste de conteneur
    """

    if request.method == 'POST':
        if 'filepath' in request.POST:
            #build un dockerfile a partir du fichier existant
            filepath = request.POST.get('filepath')
            dockerfile = open(filepath, 'rb')
            try:
                name = request.POST.get('name')
                user = request.user
                name = name.lower()
                name = (f'{user}-{name}')
                print(dockerfile.read().decode('utf-8'))
                dockerfile.seek(0)
                if dockerfile is None:
                    return JsonResponse({'error': 'Invalid or empty Dockerfile'}, status=400)
                image = DockerService().run_dockerfile(request, dockerfile, name)

                return JsonResponse({'image': str(image)})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        else :
            #si on upload un fichier
            if 'dockerfile' not in request.FILES:
                return JsonResponse({'error': 'No file provided'}, status=400)
            dockerfile = request.FILES['dockerfile']
            try:
                name = request.POST.get('name')
                user = request.user
                name=name.lower()
                name=(f'{user}-{name}')
                print(dockerfile.read().decode('utf-8'))
                dockerfile.seek(0)
                if dockerfile is None:
                    return JsonResponse({'error': 'Invalid or empty Dockerfile'}, status=400)
                image = DockerService().run_dockerfile(request,dockerfile,name)

                return JsonResponse({'image': str(image)})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def compose(request):
    """
    Fonction qui permet de creer un conteneur avec un fichier docker-compose.yml. redirect sur la page de liste de conteneur
    :param request:
    :return: redirect sur la page de liste de conteneur
    """
    if request.method == 'POST':

        if 'filepath' in request.POST:
            filepath = request.POST.get('filepath')
            composefile = open(filepath, 'rb')
            try:
                user = request.user
                name = request.POST.get('name')
                user = request.user
                name = name.lower()
                name = f'{user}-{name}'
                # Lire le contenu du fichier YAML
                compose_data = yaml.safe_load(composefile.read())
                # Vérifier si compose_data est None
                if compose_data is None:
                    return JsonResponse({'error': 'Invalid or empty YAML file'}, status=400)
                compose_result = DockerService().run_compose(request, compose_data, name)
                return JsonResponse({'compose': compose_result})
            except yaml.YAMLError as e:
                return JsonResponse({'error': f'Invalid YAML format: {str(e)}'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        else:
        # Vérifie si le fichier a été fourni
            if 'composefile' not in request.FILES:
                return JsonResponse({'error': 'No file provided'}, status=400)
            composefile = request.FILES['composefile']
            try:
                user = request.user
                name = request.POST.get('name')
                user = request.user
                name=name.lower()
                name=f'{user}-{name}'
                # Lire le contenu du fichier YAML
                compose_data = yaml.safe_load(composefile.read())
                # Vérifier si compose_data est None
                if compose_data is None:
                    return JsonResponse({'error': 'Invalid or empty YAML file'}, status=400)
                compose_result = DockerService().run_compose(request,compose_data, name)
                return JsonResponse({'compose': compose_result})
            except yaml.YAMLError as e:
                return JsonResponse({'error': f'Invalid YAML format: {str(e)}'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

