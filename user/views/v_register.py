from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms.f_register import CustomUserCreationForm
from ..services.s_auth import authentification

def registerForm(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('home')  # Redirection vers la page d'accueil
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
