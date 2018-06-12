from django.urls import path, re_path

from . import views

urlpatterns = [
    path('submit/', views.submit),
    re_path(r'^get/(?P<username>.+)/', views.getPrograms, name="get_programs"),
]
