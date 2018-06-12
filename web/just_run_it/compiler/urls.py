from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('submit/', views.submit, name='submit'),
    path('api/test_submit/', views.api_test_submit, name='api_test_submit'),
    path('get/', views.getPrograms, name='get_programs'),
    re_path(r'^get/([0-9]+)/', views.getProgram, name='get_program'),
    path('new/', views.addProgram, name='add_program'),
]