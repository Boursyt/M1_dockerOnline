from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from admin_customs.services.s_userAdmin import manageUser
from django.http import JsonResponse
from django.contrib.auth.models import User
from filemanager.services.s_gestionFile import File
from user.forms.f_register import CustomUserCreationForm


def admin_user_liste_page(request):
    """
    Page de liste des containers qui render /admin/container
    :param request:
    :return:
    """
    user = request.user
    if user.is_authenticated:
        users = admin_listeUser(request)
        context = {
            'menu': {
                'page': 'user'
            },
            'users': users
        }
        return render(request, 'admin_list_user.html', context)
    else:
        return redirect('/home')



def admin_listeUser(request):
    """
    Liste des containers de tous les utilisateurs
    :param request:
    :return:
    """
    manage_user = manageUser()
    users_data = manage_user.getUser()
    users = []
    for i in range(len(users_data['username'])):
        users.append({
            "username": users_data["username"][i],
            "firstname": users_data["firstname"][i],
            "lastname": users_data["lastname"][i],
            "email": users_data["email"][i],
            "is_superuser": users_data["is_superuser"][i]
        })
    return users

def admin_supprimer_user(request, username):
    """
        supprimer un utilisateur
    """
    if request.method == 'POST':
        manageUser().deleteUser(username)
        return redirect('userListe')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# formulaire de modification d'un utilisateur, dans un menu qui ce superpose
def edit_user(request, username):
    """
    Modifier un utilisateur ou récupérer ses informations
    """
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        is_superuser = request.POST.get('is_superuser') == 'on'  # Convertir en booléen
        manageUser().updateUser(username, firstname, lastname, email, is_superuser)
        return redirect('userListe')

    elif request.method == 'GET':
        user = get_object_or_404(User, username=username)
        user_data = {
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'is_superuser': user.is_superuser,
        }
        return JsonResponse(user_data)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def registerFormAdmin(request):
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
            File().creatUserDir('filedir', user.username)
            return redirect('userListe')  # Redirection vers la page d'accueil
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return redirect('userListe')
