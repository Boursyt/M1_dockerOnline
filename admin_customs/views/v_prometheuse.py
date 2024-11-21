from django.shortcuts import render, redirect
from admin_customs.services.s_prometheus import prometheus
from django.shortcuts import render, redirect
from django.http import JsonResponse

def allmetrics(request):
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
    prometheus_instance = prometheus()
    return prometheus_instance.get_metrics_cpu()
def RAM(request):
    prometheus_instance = prometheus()
    return prometheus_instance.get_metrics_ram()

def DISK(request):
    prometheus_instance = prometheus()
    return prometheus_instance.get_metrics_disk()
