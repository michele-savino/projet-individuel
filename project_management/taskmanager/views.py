from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from .forms import JournalForm, TaskForm
from .models import Project, Task, Journal, Status


# limitare accesso alle pagine show_project e show_task
def limit_access(user, project_members):
    if user not in project_members.all():
        raise PermissionDenied


@login_required()
def projects_list(request):
    current_user = request.user
    user_projects = current_user.project_set.all()

    return render(request, 'taskmanager/projects_list.html', locals())


@login_required()
def show_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    limit_access(request.user, project.members)
    tasks = project.task_set.all().order_by('start_date', '-priority')

    return render(request, 'taskmanager/project.html', locals())


# risolvere il bug che mi farebbe richiedere anche una task non associata a quel progetto
#ordinare task per data

@login_required()
def show_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    limit_access(request.user, task.project.members)
    journals = task.journal_set.all().order_by('date')
    form = JournalForm
    return render(request, 'taskmanager/task.html', locals())


@login_required()
def new_journal(request, task_id):
    task = Task.objects.get(id=task_id)
    limit_access(request.user, task.project.members)
    form = JournalForm(request.POST or None)
    if form.is_valid():
        journal = Journal()
        journal.entry = form.cleaned_data["entry"]
        journal.task = task
        journal.author = request.user
        journal.save()

    return redirect(show_task, task_id=task_id)


@login_required()
def new_task(request, project_id):
    form = TaskForm(request.POST or None)
    project = Project.objects.get(id=project_id)
    limit_access(request.user, project.members)
    form.fields['assignee'].queryset = project.members
    if form.is_valid():
        task = form.save(commit=False)
        task.project = Project.objects.get(id=project_id)
        task.status = Status.objects.get(name="New")
        task.save()
        return redirect(show_task, task_id=task.id)

    return render(request, 'taskmanager/edit_task.html', locals())

# risolvere il fatto che il form salva un nuovo task anziché modificare il vecchio


@login_required()
def edit_task(request, task_id):
    edit_flag = True
    task = Task.objects.get(id=task_id)
    limit_access(request.user, task.project.members)
    form = TaskForm(request.POST or None, instance=task)
    project = task.project
    form.fields['assignee'].queryset = project.members
    if form.is_valid():
        form.save()
        return redirect(show_task, task_id=task_id)

    return render(request, 'taskmanager/edit_task.html', locals())
