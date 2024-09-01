from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('applications/',views.form, name='form'),
    path('', views.index, name='index'),
]
