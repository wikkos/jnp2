from django.urls import path, re_path

from . import views

urlpatterns = [
    path('submit/', views.submit),
    re_path(r'^get/(?P<username>.+)/', views.getPrograms, name="get_programs"),
    re_path(r'^get_by_id/([0-9]+)/', views.getProgram, name='get_program'),
]
