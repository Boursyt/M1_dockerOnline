from django.contrib.auth.models import User
from user.services.s_auth import authentification


class manageUser:

    def getUser(self):
        '''
        Recuperer la liste de tous les utilisateurs et les infos

        return: dict listUser(username[], firstname[], lastname[], email[], is_superuser[])
        '''
        listUser= {
            'username': [],
            'firstname': [],
            'lastname': [],
            'email': [],
            'is_superuser': []
        }
        users = User.objects.all()
        for user in users:
            listUser['username'].append(user.username)
            listUser['firstname'].append(user.first_name)
            listUser['lastname'].append(user.last_name)
            listUser['email'].append(user.email)
            listUser['is_superuser'].append(user.is_superuser)

        return listUser

    def deleteUser(self, username):
        '''
        Supprimer un utilisateur

        param: username
        return: bool
        '''
        try:
            user = User.objects.get(username=username)
            user.delete()
            return True
        except:
            return False

    def updateUser(self, username, firstname, lastname, email, is_superuser):
        '''
        Mettre a jour les informations d'un utilisateur

        param: username, firstname, lastname, email, is_superuser
        return: bool
        '''
        try:
            user = User.objects.get(username=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.is_superuser = is_superuser
            user.save()
            return True
        except:
            return False

    def createUser(self, username, firstname, lastname, email, password, is_superuser):
        authentification.register_user(username, firstname, lastname, email, password)
        user = User.objects.get(username=username)
        user.is_superuser = is_superuser
