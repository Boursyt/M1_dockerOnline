from django.shortcuts import render


def homepage(request):
    context = {
        'menu': {
            'page': 'home'
        }
    }
    return render(request, 'home.html',context)