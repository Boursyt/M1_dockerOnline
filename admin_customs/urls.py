from django.urls import path
from . import views
from .views import v_adminHome, v_prometheuse

urlpatterns = [

    path('', v_adminHome.home, name='home_admin'),
    path("metrics",v_prometheuse.allmetrics, name='metrics'),
    path("metrics/cpu",v_prometheuse.CPU, name='cpu'),
    path("metrics/ram",v_prometheuse.RAM, name='ram'),
    path("metrics/disk",v_prometheuse.DISK, name='disk')


]