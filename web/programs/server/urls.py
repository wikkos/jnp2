from django.urls import path

from web.programs.server import views

urlpatterns = [
    path('send/', views.send),
]
