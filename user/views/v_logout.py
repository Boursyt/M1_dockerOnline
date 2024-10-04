from django.shortcuts import redirect
from django.contrib.auth import logout
from urllib3 import request


def Userlogout(request):
    logout(request)
    return redirect('home')
