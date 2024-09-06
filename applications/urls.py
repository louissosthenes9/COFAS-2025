from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('applications/',views.form, name='form'),
    path('', views.index, name='index'),
    path('success/',views.success, name='success'),
    path('analytics',views.analytics_view, name='error')
    

]
