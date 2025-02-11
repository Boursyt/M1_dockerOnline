import os
class file:

    def __init__(self, name, size, date, type, owner):
        self.name = name
        self.path = "../filedir"
        self.size = size
        self.date = date
        self.type = type
        self.owner = owner


    def getFile(self, path, user):
        """
        Get every file in the path
        """
        try:
            files = os.listdir(f'{path}/{user}')
            return files
        except Exception as e:
            return {'error': str(e)}


    def importFile(self, path, user, file):
        """
        Import file in the path
        """
        try:
            with open(f'{path}/{user}/{file.name}', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return {'success': 'File imported'}
        except Exception as e:
            return {'error': str(e)}

    def exportFile(self, path, user, file):
        pass

    def deleteFile(self, path, user, file):
        """
        Delete file in the path
        """
        try:
            os.remove(f'{path}/{user}/{file}')
            return {'success': 'File deleted'}
        except Exception as e:
            return {'error': str(e)}

