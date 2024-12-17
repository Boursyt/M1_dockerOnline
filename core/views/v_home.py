from django.shortcuts import render


def homepage(request):
    """
    Vue de base pour la page d'accueil render /home
    :param request:
    :return:
    """
    context = {
        'menu': {
            'page': 'home'
        }
    }
    return render(request, 'home.html',context)