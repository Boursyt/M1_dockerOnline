from django.urls import path
from . import views
from .views import v_file

urlpatterns = [

    path('', v_file.Showfile , name='file'),
    path('delete/<str:file_name>/', v_file.supprimer_fichier, name='supprimer_container'),
    path('download/<str:file_name>/', v_file.telecharger_fichier, name='telecharger_fichier'),
    path('upload/', v_file.upload_file, name='upload'),
    ]