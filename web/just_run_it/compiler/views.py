from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from .models import Submission
from .forms import SubmissionForm

""" 
def index(request):
    return render(request, 'compiler/submit_code.html')
"""

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


@login_required
def submit(request):
    if request.method == 'POST':
        print("submitting")
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            #submission.status = Submission.SU
            submission.save()
            print("submission saved")
            return HttpResponseRedirect(reverse('submit'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'compiler/submit_code.html', {'form': form})
