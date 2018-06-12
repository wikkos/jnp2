import datetime
import os
import threading
from pathlib import Path

import docker
import time
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .models import Execution
from .languages_map import languages_map
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
    return folderName, now


def _spawnRunner(request, folderName, executionId):
    client = docker.from_env()
    container = client.containers.run(
        languages_map[request.POST['language']]['image'],
        'python run.py ' + request.POST['language'],
        detach=True
    )
    os.system('docker cp ' + folderName + '/file' + languages_map[request.POST['language']]['ext'] +
              ' ' + container.name + ':/runner')
    os.system('docker cp ' + folderName + '/input ' + container.name + ':/runner')

    try:
        container.wait(timeout=300)
        response = container.logs().decode('utf-8')
        print("runner exited correctly")
        print(response)
        _saveFile(response, folderName + '/output.json')
        Execution.objects.filter(id=executionId).update(status=Execution.EXECUTED)
    except:
        print("runner failed to exit on time")
        try:
            container.kill()
        except:
            pass
        Execution.objects.filter(id=executionId).update(status=Execution.FAILED)

    # TODO add message on RabbitMQ
    container.remove()


@api_view(['POST'])
def submit(request):
    print("Inside submit")
    print(request.POST)
    print(request.user)

    form = SubmitForm(request.POST)
    if form.is_valid():
        folderName, now = _saveFiles(request)
        now = datetime.datetime.fromtimestamp(now / 1000, tz=datetime.timezone.utc)
        execution = Execution.objects.create(
            username=request.POST['username'],
            folderName=folderName,
            timeExecuted=now,
            status=Execution.RUNNING
        )
        threading.Thread(target=_spawnRunner, args=[request, folderName, execution.id]).start()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
