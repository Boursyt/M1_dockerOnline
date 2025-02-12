from filemanager.services.s_gestionFile import File
from django.shortcuts import render, redirect
from django.http import JsonResponse


def Showfile(request):
    """
    Show file in the user directory and send it to the template
    """
    user = request.user
    fileListe=listeFile(request)
    context = {
        'menu': {
            'page': 'home'
        },
        'files':fileListe
    }
    return render(request, 'file.html', context)

def listeFile(request):
    """
    Show file in the user directory and send it to the template
    """
    user = request.user
    fileList = File().getFile('filedir', user)

    # Vérifiez si fileList contient une erreur
    if 'error' in fileList:
        print(fileList['error'])
        return []

    files = []
    for i in range(len(fileList['name'])):
        files.append({
            "name": fileList["name"][i],
            "size": fileList["size"][i],
            "date": fileList["date"][i],
            "type": fileList["type"][i]
        })

    print(files)
    return files
