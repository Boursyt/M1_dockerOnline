from filemanager.services.s_gestionFile import file
from django.shortcuts import render, redirect
from django.http import JsonResponse


def file(request):

    return render(request, 'file.html')