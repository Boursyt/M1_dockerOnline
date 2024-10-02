

from django.urls import path
from . import views
from .views import v_container, v_liste

urlpatterns = [


    path('creat/', v_container.start_container, name='start_container'),
    path('start-container/', v_container.bouton_start, name='bouton_start'),
    path('dockerfile/', v_container.dockerfile, name='dockerfile'),
    path('compose/', v_container.compose, name='compose'),

    path('liste/', v_liste.liste_page, name='liste_page'),
    path('liste/user', v_liste.bouton_list, name='bouton_list'),
]