from django.shortcuts import render, redirect
from containers.services.s_docker import DockerService
from django.http import JsonResponse

def admin_liste_page(request):
    """
    Page de liste des containers qui render /admin/container
    :param request:
    :return:
    """
    user = request.user
    if user.is_authenticated:
        containers = admin_listeContainer(request)
        context = {
            'menu': {
                'page': 'container'
            },
            'containers': containers
        }
        return render(request, 'admin_list_container.html', context)
    else:
        return redirect('/home')

def admin_listeContainer(request):
    """
    Liste des containers de tous les utilisateurs
    :param request:
    :return:
    """
    docker_service = DockerService()
    docker_list = docker_service.docker_list()
    containers = []
    for container in docker_list:
        containers.append({
            "id": container["id"],
            "name": container["name"],
            "status": container["status"],
            "image": container["image"]
        })
    return containers

def admin_supprimer_container(request, container_name):
    """
    Handles the deletion of a Docker container through an HTTP POST request. If the request method
    is POST, the specified container is removed, and the user is redirected to the container list page.
    If the request method is not POST, an error response is returned in JSON format with a 400
    status code.

    :param request: The HTTP request object containing metadata about the request and its method.
    :type request: HttpRequest
    :param container_name: The name of the Docker container to be removed.
    :type container_name: str
    :return: A redirect to the container list page if the request is valid; otherwise, a JSON response
        containing an error message with HTTP status 400.
    :rtype: HttpResponse or JsonResponse
    """
    if request.method == 'POST':
        DockerService().docker_remove(container_name)
        return redirect('liste_page')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def admin_run_container(request, container_name):
    """
    Runs a Docker container based on the given container name if the request
    method is POST. If the method is not POST, returns an error response.

    :param request: The HTTP request object containing metadata and method
        information.
    :type request: HttpRequest
    :param container_name: The name of the Docker container that should be run.
    :type container_name: str
    :return: A redirect response if the operation is successful or a JSON response
        indicating an invalid request.
    :rtype: HttpResponse or JsonResponse
    """
    if request.method == 'POST':
        DockerService().docker_run(container_name)
        return redirect('liste_page')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def admin_stop_container(request,container_name):
    """
    Stops a running Docker container specified by the provided container name through
    a POST request. If the request method is not POST, an error response is returned.

    :param request: The HTTP request object. It specifies the method and additional
       context for the request.
    :param container_name: The name of the Docker container to stop. It is passed
       as a string to the Docker service.
    :return: A redirect to the 'liste_page' page upon successful stopping, or a JSON
        response containing an error message and a 400 status code if the request
        method is not POST.
    """
    if request.method == 'POST':
        DockerService().docker_stop(container_name)
        return redirect('liste_page')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def admin_logs_container(request, container_name):
    """
    Handles the retrieval and presentation of logs and error information for a
    specified Docker container. This function processes HTTP POST requests to
    provide logs and Docker error details of a given container and renders the
    response in an HTML or JSON format based on the method and request status.

    :param request: The HTTP request object containing request method and metadata.
    :type request: HttpRequest
    :param container_name: The name of the Docker container whose logs are to
        be fetched.
    :type container_name: str
    :return: Renders an HTML page with container logs and error details for
        POST requests, or returns a JSON error message for other request methods.
    :rtype: HttpResponse or JsonResponse
    """
    if request.method == 'POST':
        logs = DockerService().get_logs(container_name)
        error = DockerService().get_Docker_error(container_name)

        if not isinstance(error, dict):
            error = {}

        context = {
            'menu': {
                'page': 'liste'
            },
            'name': container_name,
            'logs': logs,
            'dockerError': {
                'state': error.get('state', 'N/A'),
                'exit_code': error.get('exit_code', 'N/A'),
                'error_message': error.get('error_message', 'N/A')
            }
        }
        return render(request, 'logs.html', context)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

