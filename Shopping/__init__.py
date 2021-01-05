from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


# making login_required decorator
def login_required(f):
    @wraps(f)
    def wrap(Ag1, request):
        try:
            if request.session['user']:
                return f(Ag1, request)
        except:
            messages.error(request, 'You Need To Login First')
            return redirect('login')
    return wrap
