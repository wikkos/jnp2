import datetime
import json
import os
import threading
from pathlib import Path

import docker
import time

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from .models import Execution
from .languages_map import languages_map
from .forms import SubmitForm

import pika as pika


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
    _saveFile(request.POST.get('input', ''), folderName + '/input')
    return folderName, now


def _spawnRunner(request, folderName, executionId):
    client = docker.from_env()
    container = client.containers.run(
        languages_map[request.POST['language']]['image'],
        'python run.py ' + request.POST['language'],
        detach=True
    )
    # docker API for python does not support copy operation :(
    os.system('docker cp ' + folderName + '/file' + languages_map[request.POST['language']]['ext'] +
              ' ' + container.name + ':/runner')
    os.system('docker cp ' + folderName + '/input ' + container.name + ':/runner')

    try:
        container.wait(timeout=300)
        response = container.logs().decode('utf-8')
        print("runner exited correctly")
        _saveFile(response, folderName + '/output.json')
        Execution.objects.filter(id=executionId).update(status=Execution.EXECUTED)
    except:
        print("runner failed to exit on time")
        try:
            container.kill()
        except:
            pass
        Execution.objects.filter(id=executionId).update(status=Execution.FAILED)

    # Wiadomości trafiają do Exchange (można to zobaczyć z panelu RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='message-broker'))
    channel = connection.channel()
    channel.exchange_declare(exchange='exec_results',
                             exchange_type='fanout')

    channel.basic_publish(exchange='exec_results',
                          routing_key='',
                          body=str(Execution.objects.get(id=executionId).sid))
    print(" [x] Sent exec_results message")
    connection.close()

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
            userName=request.POST['username'],
            folderName=folderName,
            timeExecuted=now,
            status=Execution.RUNNING,
            language=request.POST['language'],
            sid=request.POST['id']
        )
        threading.Thread(target=_spawnRunner, args=[request, folderName, execution.id]).start()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)


def getPrograms(request, username):
    executions = list(Execution.objects.filter(userName=username).values('id', 'timeExecuted', 'status', 'language'))
    for exe in executions:
        exe['timeExecuted'] = exe['timeExecuted'].strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(json.dumps(executions), content_type='application/json')

def getProgram(request, id):
    try:
        exe = Execution.objects.values('id', 'timeExecuted', 'language', 'folderName').get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(status=400)

    with open(exe['folderName'] + '/output.json', 'r') as file:
        content = file.read()
    content = json.loads(content)
    content['id'] = exe['id']
    content['timeExecuted'] = exe['timeExecuted'].strftime('%Y-%m-%d %H:%M:%S')
    content['language'] = exe['language']
    return HttpResponse(json.dumps(content), content_type='application/json')
