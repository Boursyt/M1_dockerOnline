from django.urls import path
from . import views
from .views import v_login, v_register, v_logout


urlpatterns = [

    path('login/', v_login.loginForm, name='login'),
    path('register/', v_register.registerForm, name='register'),
    path('logout/', v_logout.Userlogout, name='logout'),

]