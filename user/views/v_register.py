from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms.f_register import CustomUserCreationForm
from ..services.s_auth import authentification
from user.services.s_volume import volume
def registerForm(request):
    """
    Fonction d'inscription de l'utilisateur. Formulaire d'inscription personnalisé
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            linuxuser = volume().creat_linux_user(user.username)
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('home')  # Redirection vers la page d'accueil
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
