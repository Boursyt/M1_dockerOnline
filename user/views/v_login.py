from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def loginForm(request):
    """
    Vue de connexion de l'utilisateur. Utilise le formulaire d'authentification Django.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or dashboard
            else:
                return HttpResponse('Erreur de connexion, essayez encore.')
        else:
            return HttpResponse('Formulaire invalide, essayez encore.')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})