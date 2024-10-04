from django.contrib.auth.models import User
from ..models.m_user import UserProfile
from django.contrib.auth import logout


class authentification:

    def __init__(self):
        self.username = None
        self.firstname = None
        self.lastname = None
        self.password = None
        self.email = None
        self.token = None
        self.issuperuser = None
    def logout_user(self, request):
        logout(request)  # Déconnexion de l'utilisateur
    def register_user(username, first_name, last_name, email, password):
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        # Créer un profil utilisateur, si nécessaire
        UserProfile.objects.create(user=user)
        return user


