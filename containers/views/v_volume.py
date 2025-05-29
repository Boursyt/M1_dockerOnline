from django.shortcuts import render, redirect
from containers.services.s_docker import DockerService
from django.http import JsonResponse

def list_volumes(request):
    """
    List all Docker volumes. Called by the 'volumes' view.
    :param request:
    :return: JSON response with volume details.
    """
    user = request.user

    if user.is_authenticated:
        volumes = volume_list(request)
        context = {
            'menu': {
                'page': 'volumes'
            },
            'volumes': volumes,
        }
        return render(request, 'volume_liste.html', context)
    else:
        return redirect('/home')

def volume_list(request):
    """
    Get a list of all Docker volumes.
    :param request:
    :return: LIST response with volume details.
    """
    user = request.user
    volumes_list = DockerService().list_volumes(user)
    volumes=[]
    for volume in volumes_list:
        volumes.append({
            "name": volume["name"],
            "path": volume["path"],
            "date": volume["date"]
        })
    return volumes

def delete_volume(request, volume_name):
    """
    Delete a Docker volume. Called by the 'volumes' view.
    :param request:
    :param volume_name: Name of the volume to delete.
    :return: Redirect to the volumes list page.
    """
    print("coucous")
    user = request.user
    if request.method == 'POST':
        DockerService().delete_volumes(user,volume_name)
        return redirect('volumes')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

