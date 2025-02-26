import math
import os
from datetime import datetime

from django.http import HttpResponse, FileResponse
global src
src = 'C:/Users/hypto/PycharmProjects/M1_dockerOnline'

class File:

    def convert_size(self, size_bytes):
        """
        Convert a size in bytes to a human-readable format
        """
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def getFile(self, path, user):
        """
        Get every file in the path and return some informations about it

        """
        try:
            files = os.listdir(f'{src}/{path}/{user}')
            filesList = {
                'name': [],
                'size': [],
                'date': [],
                'type': [],
                'content': [],
                'path': []
            }
            for file in files:
                filesList['name'].append(file)
                size=os.path.getsize(f'{path}/{user}/{file}')
                filesList['size'].append(self.convert_size(size))
                filesList['date'].append(datetime.fromtimestamp(os.path.getctime(f'{path}/{user}/{file}')))
                filesList['type'].append(os.path.splitext(file)[1])
                filesList['content'].append(open(f'{src}/{path}/{user}/{file}').read())
                filesList['path'].append(f'{src}/{path}/{user}/{file}')
            return filesList
        except Exception as e:
            return {'error': str(e)}


    def importFile(self, path, user,file):
        """
        Import file in the path
        """
        try:
            name = file.name
            file_path = os.path.join(f'{src}/{path}/{user}/{name}')

            # Vérifiez si le fichier existe avant d'ouvrir le fichier en écriture
            if os.path.exists(file_path):
                return {'error': 'File already exists'}

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return {'success': 'File imported'}
        except Exception as e:
            return {'error': str(e)}

    def exportFile(self, path, user, file):
        """
        Export file in the path for download
        """
        try:
            file_path = f'{src}/{path}/{user}/{file}'
            if not os.path.exists(file_path):
                return {'error': 'File not found'}

            # Utiliser FileResponse pour envoyer le fichier en réponse HTTP
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{file}"'
            response['Content-Type'] = 'application/octet-stream'  # Forcer le téléchargement
            print(response)
            return response
        except Exception as e:
            print(e)
            return {'error': str(e)}

    def deleteFile(self, path, user, file):
        """
        Delete file in the path
        """
        try:
            os.remove(f'{src}/{path}/{user}/{file}')
            return {'success': 'File deleted'}
        except Exception as e:
            return {'error': str(e)}

    def creatUserDir(self, path,user):
        """
        Create a directory for the user
        """
        try:
            os.makedirs(f'{src}/{path}/{user}')
            return {'success': 'Directory created'}
        except Exception as e:
            return {'error': str(e)}

    def existUserDir(self, path,user):
        """
        Check if the user directory exist, return True if it exist
        """
        try:
            return os.path.exists(f'{src}/{path}/{user}')
        except Exception as e:
            return {'error': str(e)}
