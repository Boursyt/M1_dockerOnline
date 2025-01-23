from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import time
import base64


def generate_hash(path):
    """Génère un hash simple pour chaque fichier/dossier"""
    return base64.urlsafe_b64encode(path.encode()).decode().rstrip('=')


def decode_hash(hash_value):
    """Décode un hash en chemin relatif"""
    try:
        return base64.urlsafe_b64decode(hash_value + "==").decode()
    except Exception:
        return ""


def connector(request):
    user = request.user.username
    root_path = os.path.join(settings.MEDIA_ROOT, f'elfinder/{user}')
    os.makedirs(root_path, exist_ok=True)

    action = request.GET.get('cmd', '')
    target = request.GET.get('target', '')

    if not target or target == "Lw":
        current_dir = root_path
        rel_path = ""
    else:
        rel_path = decode_hash(target)
        current_dir = os.path.join(root_path, rel_path)

    if not os.path.exists(current_dir):
        return JsonResponse({"error": "Path not found"}, status=404)

    if action == 'open':
        try:
            files = os.listdir(current_dir)
            file_list = [
                {
                    "hash": generate_hash(os.path.join(rel_path, file)),
                    "name": file,
                    "mime": "directory" if os.path.isdir(os.path.join(current_dir, file)) else "file",
                    "ts": int(os.path.getmtime(os.path.join(current_dir, file))),
                    "size": os.path.getsize(os.path.join(current_dir, file)),
                    "dirs": 1 if os.path.isdir(os.path.join(current_dir, file)) else 0,
                }
                for file in files
            ]
            response = {
                "cwd": {
                    "hash": "Lw",
                    "name": "Root",
                    "mime": "directory",
                    "rel": "Root",
                    "ts": int(time.time()),
                    "size": 0,
                    "dirs": 1,
                    "volumeid": 1
                },
                "files": [
                             {
                                 "hash": "Lw",
                                 "name": "Root",
                                 "mime": "directory",
                                 "ts": int(time.time()),
                                 "size": 0,
                                 "dirs": 1,
                             }
                         ] + file_list,
                "options": {
                    "path": "Root",
                    "url": f'/media/elfinder/{user}/',
                    "tmbUrl": "",
                    "separator": "/",
                    "disabled": [],
                    "archivers": {},
                },
            }
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({"error": f"Erreur lors de l'ouverture du dossier: {str(e)}"}, status=500)

    return JsonResponse({"error": "Commande inconnue"}, status=400)


def ui(request):
    return render(request, 'elfinder.html')
