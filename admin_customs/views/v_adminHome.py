from django.shortcuts import render, redirect

def home (request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            context = {
                'menu': {
                    'page': 'home_admin'
                }
            }
            return render(request, 'home_admin.html', context)
    else:
        return redirect('/home')
