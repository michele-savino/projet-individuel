from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .models import Project, Task


#limitare accesso alle pagine show_project e show_task

@login_required()
def projects_list(request):
    current_user = request.user
    user_projects = current_user.project_set.all()

    return render(request, 'taskmanager/projects_list.html', locals())


@login_required()
def show_project(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = project.task_set.all()

    return render(request, 'taskmanager/project.html', locals())


@login_required()
def show_task(request, id):
    task = get_object_or_404(Task, id=id)
    journals = task.journal_set.all()

    return render(request, 'taskmanager/task.html', locals())
