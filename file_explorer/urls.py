from django.urls import path, include
from .view.v_elfinder import connector, ui
#from .views import


urlpatterns = [
    path('elfinder/connector/', connector, name='elfinder_connector'),
    path('elfinder/', ui, name='elfinder_ui'),
]