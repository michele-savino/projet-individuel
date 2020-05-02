from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import JournalForm
from .models import Project, Task, Journal


# limitare accesso alle pagine show_project e show_task

@login_required()
def projects_list(request):
    current_user = request.user
    user_projects = current_user.project_set.all()

    return render(request, 'taskmanager/projects_list.html', locals())


@login_required()
def show_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.task_set.all()

    return render(request, 'taskmanager/project.html', locals())


@login_required()
def show_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    journals = task.journal_set.all()
    return render(request, 'taskmanager/task.html', locals())


@login_required()
def add_journal(request, task_id):
    form = JournalForm(request.POST or None)
    if form.is_valid():
        journal = Journal()
        journal.entry = form.cleaned_data["entry"]
        journal.task = Task.objects.get(id=task_id)
        journal.author = request.user
        journal.save()

    return redirect(show_task, task_id=task_id)
