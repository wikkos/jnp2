from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import SubmissionForm

""" 
def index(request):
    return render(request, 'compiler/submit_code.html')
"""

def index(request):
    """User error handling:
        If given flight does not exist: return 404
        If flight don't have spare seats: redirect to flight-detail
        If user is not authenticated: redirect to login page
        If form is valid: save and return to flight-detail
        In flight-detail user sees why they can't add reservation
        or sees new passenger on the list.
    """
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            #submission.user = flight_id
            submission.save()
            return HttpResponseRedirect(reverse('index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'compiler/submit_code.html', {'form': form})
