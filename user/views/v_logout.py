from django.shortcuts import redirect
from django.contrib.auth import logout
from urllib3 import request


def Userlogout(request):
    """
    Fonction de déconnexion de l'utilisateur
    :param request:
    :return:
    """
    logout(request)
    return redirect('home')
