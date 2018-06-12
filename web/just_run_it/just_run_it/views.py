from django.http import HttpResponseRedirect
from django.contrib.auth import logout


def redirect_root(request):
    return HttpResponseRedirect('/compiler/')