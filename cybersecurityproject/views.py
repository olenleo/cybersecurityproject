from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def redirect(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('accounts/login')
    return HttpResponseRedirect('messages/')

