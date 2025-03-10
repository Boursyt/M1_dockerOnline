from django.shortcuts import render, redirect
from admin_customs.services.s_userAdmin import manageUser
from django.http import JsonResponse

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

    """
    if request.method == 'POST':
        manageUser().deleteUser(username)
        return redirect('userListe')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

