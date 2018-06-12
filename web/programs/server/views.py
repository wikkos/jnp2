import os
import threading
from pathlib import Path

import docker
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from rest_framework.decorators import api_view

from .forms import SendCodeForm
from django.views.decorators.csrf import csrf_exempt

from .forms import SendCodeForm


def _spawn_runner():
    client = docker.from_env()
    container = client.containers.run('jnp2_runner', 'python run.py', detach=True)
    os.system("docker cp file.c " + container.name + ":/runner")
    os.system("docker cp input " + container.name + ":/runner")

    try:
        container.wait(timeout=60)
    except:
        container.kill()

    response = container.logs()
    container.remove()

    print(response)
    #try:
    #    response = json.loads(response)
    #    print(response)
    #except:
    #    print("failed to parse json")

@csrf_exempt
def send(request):
    if request.method == "POST":
        form = SendCodeForm(request.POST)
        if form.is_valid():
            filePath = Path("file.c")
            filePath.touch()
            file = open("file.c", "w")
            file.write(request.POST['code'])
            file.close()

            filePath = Path("input")
            filePath.touch()
            file = open("input", "w")
            file.write(request.POST['input'])
            file.close()

            threading.Thread(target=_spawn_runner).start()

    # TODO for some reason this template is not loading properly
    return render(request, 'ok.html')


@api_view(['POST'])
def submit(request):
    print("Inside submit")
    print(request.POST)
    print(request.user)

    return HttpResponse(status=201)
