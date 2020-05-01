from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects_list, name='projects_list'),
    path('project/<int:id>', views.show_project, name='project'),
    path('task/<int:id>', views.show_task, name='task'),
]
