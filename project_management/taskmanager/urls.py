from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects_list, name='projects_list'),
    path('project/<int:project_id>', views.show_project, name='project'),
    path('task/<int:task_id>', views.show_task, name='task'),
    path('task/<int:task_id>/new_journal', views.new_journal, name='new_journal'),
    path('project/<int:project_id>/new_task', views.new_task, name="new_task"),
    path('task/<int:task_id>/edit_task', views.edit_task, name="edit_task"),
]
