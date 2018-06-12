import os
import threading
from pathlib import Path

import docker
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from rest_framework.decorators import api_view

from .languages_map import languages_map
from .forms import SubmitForm
from django.views.decorators.csrf import csrf_exempt

from .forms import SubmitForm

def _saveFile(content, fileName):
    path = Path(fileName)
    path.touch()
    with path.open('w') as file:
        file.write(content)

def _saveFiles(request):
    now = round(time.time() * 1000) # time in ms

    folderName = 'files/' + request.POST['username']
    path = Path(folderName)
    path.mkdir(exist_ok=True)

    folderName += '/' + str(now)
    path = Path(folderName)
    path.mkdir(exist_ok=False)

    _saveFile(request.POST['content'], folderName + '/file' + languages_map[request.POST['language']]['ext'])
    _saveFile(request.POST['input'], folderName + '/input')
    return folderName

def _spawnRunner(request, folderName):
    client = docker.from_env()
    container = client.containers.run(languages_map[request.POST['language']]['image'], 'python run.py', detach=True)
    os.system("docker cp file" + languages_map[request.POST['language']]['ext'] + ' ' + container.name + ":/runner")
    os.system("docker cp input " + container.name + ":/runner")

    try:
        container.wait(timeout=300)
        response = container.logs()
        print("runner exited correctly")
        print(response)
        _saveFile(response, folderName + '/output.json')
    except:
        print("runner failed to exit on time")
        container.kill()

    container.remove()

@api_view(['POST'])
def submit(request):
    print("Inside submit")
    print(request.POST)
    print(request.user)

    form = SubmitForm(request.POST)
    if form.is_valid():
        folderName = _saveFiles(request)
        # TODO add to database
        threading.Thread(target=_spawnRunner, args=[request, folderName]).start()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
