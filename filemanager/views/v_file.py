from django.views.decorators.http import require_GET
from httmock import response

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
            'page': 'file'
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
            "type": fileList["type"][i],
            "content": fileList["content"][i],
            "path":fileList["path"][i]
        })
    return files

def supprimer_fichier(request, file_name):
    """
    Delete file in the user directory and send it to the template
    """
    user = request.user
    result = File().deleteFile('filedir', user, file_name)
    if 'error' in result:
        print(result['error'])
    return redirect('file')
@require_GET
def telecharger_fichier(request, file_name):
    """
    Download file in the user directory and send it to the template
    """
    user = request.user
    response = File().exportFile('filedir', user, file_name)
    if isinstance(response, dict) and 'error' in response:
        return JsonResponse(response)

    return response

def upload_file(request):
    """
    Upload file in the user directory and send it to the template
    """
    user = request.user
    if request.method == 'POST':
        file = request.FILES['file']
        result = File().importFile('filedir', user, file)
        if 'error' in result:
            print(result['error'])
    return redirect('file')