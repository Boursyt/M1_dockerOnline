from django.shortcuts import render, redirect
from admin_customs.services.s_prometheus import prometheus
from django.shortcuts import render, redirect
from django.http import JsonResponse

def allmetrics(request):
    """
    Fetches and renders system metrics including CPU, RAM, and DISK for an authenticated user.

    This function checks if the user making the request is authenticated. If authenticated, it retrieves
    CPU, RAM, and DISK usage metrics from the Prometheus monitoring system and organizes the data into
    a context dictionary. Subsequently, the function renders and returns a metrics page with the
    retrieved data. If the user is not authenticated, it redirects them to the home page.

    :param request: The HTTP request object containing metadata about the user making the request.
    :type request: HttpRequest
    :return: Renders a metrics page populated with retrieved system metrics if the user is authenticated,
        or redirects to the home page if not.
    :rtype: HttpResponse
    """
    user = request.user
    if user.is_authenticated:
        prometheus_instance = prometheus()
        CPUjson = prometheus_instance.get_metrics_cpu()
        RAMjson = prometheus_instance.get_metrics_ram()
        DISKjson = prometheus_instance.get_metrics_disk()

        context = {
            'menu': {'page': 'metrics'},
            'cpu': CPUjson,
            'RAM': RAMjson,
            'DISK': DISKjson
        }

        return render(request, 'metrics.html', context)
    else:
        return redirect('/home')

def CPU(request):
    """
    Fetches CPU metrics using a Prometheus instance.

    :param request: Input data or context provided to fetch CPU metrics.
                    The request parameter specifies any necessary
                    information needed for the Prometheus instance.
    :return: The CPU metrics retrieved from the Prometheus instance.
    :rtype: Any
    """
    prometheus_instance = prometheus()
    return prometheus_instance.get_metrics_cpu()
def RAM(request):
    """
    Fetches the RAM metrics using the Prometheus instance.

    :param request: The incoming HTTP or API request object
        containing the payload necessary to handle the RAM metric
        retrieval process.
    :return: Returns the RAM metrics obtained from the Prometheus
        instance.
    :rtype: Any
    """
    prometheus_instance = prometheus()
    return prometheus_instance.get_metrics_ram()

def DISK(request):
    """
    Retrieves disk metrics using the Prometheus instance.

    This function acts as a wrapper to fetch disk-related metrics
    from a Prometheus monitoring instance. It initializes a Prometheus
    instance and retrieves disk metrics by invoking the appropriate
    method.

    :param request: Incoming request object that triggered the invocation.
                    This can contain contextual data or parameters.
    :return: Disk metrics fetched from Prometheus as defined by
             the `get_metrics_disk` response.
    :rtype: Dict
    """
    prometheus_instance = prometheus()
    return prometheus_instance.get_metrics_disk()
