from django.shortcuts import render

def hello_world(request):
    """
    Vu de base pour tester le fonctionnement de Django
    :param request:
    :return:
    """
    return render(request, 'hello.html')

