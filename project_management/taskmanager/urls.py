from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects, name='user_projects')
]
