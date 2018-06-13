from django.urls import path, re_path

from . import views

urlpatterns = [
    path('get/', views.getPrograms, name='get_programs'),
    re_path(r'^get/([0-9]+)/', views.getProgram, name='get_program'),
    path('new/', views.addProgram, name='add_program'),
    path('api/done_count/<str:login>', views.api_get_done_count, name='api_get_done_count'),
]