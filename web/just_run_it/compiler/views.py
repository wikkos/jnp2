from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from rest_framework import status
from rest_framework.response import Response

from .models import Submission
from .forms import SubmissionForm

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

            print(request.POST)
            print(request.user)

            post_data = dict(request.POST)
            post_data['user'] = request.user.username
            del post_data['csrfmiddlewaretoken']
            response = requests.post('http://programs:9000/server/submit/', data=post_data)
            print("http sent")
            content = response.content
            print(response.status_code)
            print(content)

            return HttpResponseRedirect(reverse('submit'))

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

