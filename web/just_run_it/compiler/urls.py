from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('submit', views.submit, name='submit'),
    path('api/test_submit', views.api_test_submit, name='api_test_submit'),
]