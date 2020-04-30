from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .models import Project


@login_required(redirect_field_name='redirected_to')
def projects_list(request):
    current_user = request.user
    user_projects = current_user.project_set.all()

    return render(request, 'taskmanager/projects_list.html', locals())


@login_required(redirect_field_name='redirected_to')
def show_project(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = project.task_set.all()

    return render(request, 'taskmanager/project.html', locals())
