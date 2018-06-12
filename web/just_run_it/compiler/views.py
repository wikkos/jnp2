import json
import time

import pika as pika
from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from rest_framework import status
from rest_framework.response import Response

from .sub import Sub, Exe
from .models import Submission
from .forms import SubmissionForm, LoginForm, RegistrationForm

""" 
def index(request):
    return render(request, 'compiler/submit_code.html')
"""

from rest_framework.decorators import api_view

class Index(LoginRequiredMixin, ListView):
    model = Submission
    paginate_by = 10

    def get_queryset(self):
        new_context = Submission.objects

        new_context = new_context.filter(user=self.request.user)

        return new_context.all()

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        #context['filter_source'] = self.request.GET.get('source', 'Warsaw Chopin')
        return context



def submit(request):
    if request.method == 'POST':
        print("submitting")
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()

            print("Sending")
            time.sleep(2)

            ## Publishing message to "exec_results" exchange
            ## TODO: exchange initialisation in message_broker
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='message-broker'))
            channel = connection.channel()
            channel.exchange_declare(exchange='exec_results',
                                     exchange_type='fanout')

            channel.basic_publish(exchange='exec_results',
                                  routing_key='',
                                  body='Hello World!')
            print(" [x] Sent exec_results message")

            connection.close()


            time.sleep(2)
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='message-broker'))
            channel = connection.channel()

            channel.exchange_declare(exchange='exec_results',
                                     exchange_type='fanout')

            result = channel.queue_declare(exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange='exec_results',
                               queue=queue_name)

            def callback(ch, method, properties, body):
                print("Received!")
                print(" [x] %r" % body)

            channel.basic_consume(callback,
                                  queue=queue_name,
                                  no_ack=True)


            channel.basic_publish(exchange='exec_results',
                                  routing_key='',
                                  body='Hello World!')


            print("Listening")
            channel.start_consuming()



            """print(request.POST)
            print(request.user)

            post_data = dict(request.POST)
            post_data['user'] = request.user.username
            del post_data['csrfmiddlewaretoken']
            response = requests.post('http://programs:9000/submit/', data=post_data)
            print("http sent")
            content = response.content
            print(response.status_code)
            print(content)

            return HttpResponseRedirect(reverse('submit'))"""

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'compiler/submit_code.html', {'form': form})


@api_view(['POST'])
def api_test_submit(request):
    print("Inside api_test_submit")
    print(request.POST)
    print(request.user)

    return HttpResponse(status=201)


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login_user(request, user)
                return redirect('home')
            else:
                wrong_username = True
    else:
        form = LoginForm()
    return render(request, 'login.html', locals())


def logout(request):
    return render(request, 'logout.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            login_user(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', locals())


@login_required
def getPrograms(request):
    response = requests.get('http://programs:9000/get/' + request.user.username + '/').content.decode('utf-8')
    response = json.loads(response)
    submissions = [Sub(submission) for submission in response]
    return render(request, 'submissions.html', locals())


@login_required
def getProgram(request, id):
    response = requests.get('http://programs:9000/get_by_id/' + id + '/').content.decode('utf-8')
    print("~~~" + response + "~~~")
    response = json.loads(response)
    exe = Exe(response)
    return render(request, 'select_submission.html', locals())
