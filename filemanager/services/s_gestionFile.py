import math
import os
from datetime import datetime
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
            files = os.listdir(f'/home/theo/PycharmProjects/M1_dockerOnline/{path}/{user}')
            filesList = {
                'name': [],
                'size': [],
                'date': [],
                'type': [],
            }
            for file in files:
                filesList['name'].append(file)
                size=os.path.getsize(f'{path}/{user}/{file}')
                filesList['size'].append(self.convert_size(size))
                filesList['date'].append(datetime.fromtimestamp(os.path.getctime(f'{path}/{user}/{file}')))
                filesList['type'].append(os.path.splitext(file)[1])
            print(filesList)
            return filesList
        except Exception as e:
            print("no file")
            print(e)
            return {'error': str(e)}


    def importFile(self, path, user,name,file):
        """
        Import file in the path
        """
        try:
            with open(f'{path}/{user}/{file.name}', 'wb+') as destination:
                if name in os.listdir(f'{path}/{user}'):
                    return {'error': 'File already exists'}
                else:
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

