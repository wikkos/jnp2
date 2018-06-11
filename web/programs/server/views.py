from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from web.programs.server.forms import SendCodeForm


def send(request):
    if request.method == "POST":
        form = SendCodeForm(request.method)
        # TODO spawn new docker container
    return render(request, "")