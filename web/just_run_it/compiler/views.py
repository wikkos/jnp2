import json
import time

import pika as pika
from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from rest_framework import status
from rest_framework.response import Response
import json


from .sub import Sub, Exe
from .models import Submission
from .forms import SubmissionForm, LoginForm, RegistrationForm

from rest_framework.decorators import api_view


@api_view()
def api_get_done_count(request, login):
    print("got request from: " + str(login))
    user = User.objects.all().filter(username=login)[0]
    data = dict()
    data['count'] = len(Submission.objects.all().filter(user=user).filter(status=Submission.OK))
    data['count_all'] = len(Submission.objects.all().filter(user=user))
    #json.dumps(data, safe=False)
    return JsonResponse(data)


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
    response = json.loads(response)
    exe = Exe(response)
    return render(request, 'select_submission.html', locals())


@login_required
def addProgram(request):
    if request.method == 'POST':
        print("submitting")
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            print(request.POST)

            post_data = dict(request.POST)
            post_data['username'] = request.user.username
            post_data['id'] = submission.id
            del post_data['csrfmiddlewaretoken']
            response = requests.post('http://programs:9000/submit/', data=post_data)
            print("http sent")
            content = response.content
            return HttpResponseRedirect(reverse('add_program'))
    else:
        # if a GET (or any other method) we'll create a blank form
        form = SubmissionForm()

    return render(request, 'submit.html', locals())
