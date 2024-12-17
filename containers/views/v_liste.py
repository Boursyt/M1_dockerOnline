from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from containers.services.s_docker import DockerService
from django.http import JsonResponse

def liste_page(request):
    """
    Page de la liste des containers. render /container/liste
    :param request:
    :return:
    """
    user = request.user

    if user.is_authenticated:
        containers = listeContainer(request)
        context = {
            'menu': {
                'page': 'liste'
            },
            'containers': containers
        }
        return render(request, 'liste.html', context)
    else:
        return redirect('/home')

def listeContainer(request):
    """
    Liste des containers pour le user login. utilisé par liste_page; appelle DockerService().docker_list_user
    :param request:
    :return:
    """
    docker_list_user_name = DockerService().docker_list_user(request)
    containers = []
    for container in docker_list_user_name:
        containers.append({
            "id": container["id"],
            "name": container["name"],
            "status": container["status"],
            "image": container["image"]
        })
    return containers

def supprimer_container(request, container_name):
    """
    Supprimer un container. appelé par liste.html. appelle DockerService().docker_remove
    :param request:
    :param container_name:
    :return:
    """
    if request.method == 'POST':
        DockerService().docker_remove(container_name)
        return redirect('liste_page')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def run_container(request, container_name):
    """
    Run un container. appelé par liste.html. appelle DockerService().docker_run
    :param request:
    :param container_name:
    :return:
    """
    if request.method == 'POST':
        DockerService().docker_run(container_name)
        return redirect('liste_page')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def stop_container(request,container_name):
    """
    Stop un container. appelé par liste.html. appelle DockerService().docker_stop
    :param request:
    :param container_name:
    :return:
    """
    if request.method == 'POST':
        DockerService().docker_stop(container_name)
        return redirect('liste_page')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def logs_container(request,container_name):
    """
    Logs et erreurs d'un container. appelé par liste.html. appelle DockerService().get_logs & get_Docker_error
    :param request:
    :param container_name:
    :return:
    """
    if request.method == 'POST':
        logs=DockerService().get_logs(container_name)
        error=DockerService().get_Docker_error(container_name)
        context = {
            'menu': {
                'page': 'liste'
            },
            'name': container_name,

            'logs' : logs,

            'dockerError' : {
                'state': error.get('state','N/A'),
                'exit_code': error.get('exit_code','N/A'),
                'error_message': error.get('error_message','N/A')
            }

        }
        return render(request, 'logs.html', context)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

