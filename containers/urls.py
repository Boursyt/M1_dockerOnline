

from django.urls import path
from . import views
from .views import v_container, v_liste

urlpatterns = [

    path('', v_container.start_container, name='homepage de container'),
    path('creat/', v_container.start_container, name='start_container'),
    path('container/', v_container.container, name='container'),
    path('dockerfile/', v_container.dockerfile, name='dockerfile'),
    path('compose/', v_container.compose, name='compose'),

    path('liste/', v_liste.liste_page, name='liste_page'),
    path('containers/delete/<str:container_name>/', v_liste.supprimer_container, name='supprimer_container'),
    path('containers/start/<str:container_name>/', v_liste.run_container, name='run_container'),
    path('containers/stop/<str:container_name>/', v_liste.stop_container, name='stop_container'),
    path('containers/logs/<str:container_name>/', v_liste.logs_container, name='logs_container')

]