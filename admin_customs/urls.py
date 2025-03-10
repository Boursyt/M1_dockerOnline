from django.urls import path
from . import views
from .views import v_adminHome, v_prometheuse, v_container_list,v_dns_list,v_user_liste

urlpatterns = [

    path('', v_adminHome.home_redirect, name='home_admin_redirect'),
    path('overwiews', v_adminHome.home, name='overviews'),
    path("metrics",v_prometheuse.allmetrics, name='metrics'),
    path("metrics/cpu",v_prometheuse.CPU, name='cpu'),
    path("metrics/ram",v_prometheuse.RAM, name='ram'),
    path("metrics/disk",v_prometheuse.DISK, name='disk'),
    path("container",v_container_list.admin_liste_page, name='containerListe'),
    path("dns",v_dns_list.admin_dns_liste_page, name='dnsListe'),
    path("user", v_user_liste.admin_user_liste_page, name='userListe'),

    path("user/delete/<str:username>", v_user_liste.admin_user_liste_page, name='update_user'),
    path("user/update/<str:username>", v_user_liste.admin_supprimer_user, name='delete_user'),

]