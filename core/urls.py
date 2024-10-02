from django.urls import path
from . import views
from .views import v_home, v_helloworld

urlpatterns = [
    path('', v_home.homepage, name='default'),
    path('home/', v_home.homepage, name='home'),
    path('helloworld/', v_helloworld.hello_world, name='helloworld'),

]