from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from rest_framework.decorators import api_view

from .forms import SendCodeForm


def send(request):
    if request.method == "POST":
        form = SendCodeForm(request.method)
        # TODO spawn new docker container
    return render(request, "")


@api_view(['POST'])
def submit(request):
    print("Inside submit")
    print(request.POST)
    print(request.user)

    return HttpResponse(status=201)
