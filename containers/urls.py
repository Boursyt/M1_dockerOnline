

from django.urls import path
from . import views
from .views import v_container, v_liste, v_home

urlpatterns = [
    path('', v_home.homepage, name='home'),
    path("home/", v_home.homepage, name="home"),
    path('hello/', views.hello_world, name='hello'),

    path('container/creat/', v_container.start_container, name='start_container'),
    path('container/start-container/', v_container.bouton_start, name='bouton_start'),
    path('container/dockerfile/', v_container.dockerfile, name='dockerfile'),
    path('container/compose', v_container.compose, name='compose'),


    path('container/liste/', v_liste.liste_page, name='liste_page'),
    path('container/liste/user', v_liste.bouton_list, name='bouton_list'),
]