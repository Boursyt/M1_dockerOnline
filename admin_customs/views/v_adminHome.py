from django.shortcuts import render, redirect
from containers.services.s_docker import DockerService
def home (request):
    """
    Page d'accueil de l'admin pannel /admin/overviews
    :param request:
    :return:
    """
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            containers = admin_listeContainer(request)
            context = {
                'menu': {
                    'page': 'overviews'
                },
                'containers': containers
            }
            return render(request, 'home_admin.html', context)
    else:
        return redirect('/home')
def home_redirect(request):
    """
    Redirection vers la page d'accueil de l'admin pannel
    :param request:
    :return:
    """
    return redirect('/admin/overwiews')


def admin_listeContainer(request):
    """
    Liste des containers docker. Seuls les 5 premiers sont affichés
    :param request:
    :return:
    """
    docker_service = DockerService()
    docker_list = docker_service.docker_list()
    containers = []

    for container in docker_list[:5]:
        containers.append({
            "id": container["id"],
            "name": container["name"],
            "status": container["status"],
            "image": container["image"]
        })
    return containers