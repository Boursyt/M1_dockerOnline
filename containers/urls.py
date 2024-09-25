

from django.urls import path
from . import views
from .views import v_container

urlpatterns = [
    path('hello/', views.hello_world, name='hello'),
    path('container/', v_container.start_container, name='start_container'),
    path('start-container/', v_container.bouton_start, name='bouton_start'),

]