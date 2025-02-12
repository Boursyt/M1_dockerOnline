from django.urls import path
from . import views
from .views import v_file

urlpatterns = [

    path('', v_file.Showfile , name='file'),
]