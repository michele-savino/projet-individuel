from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from .forms import JournalForm, TaskForm
from .models import Project, Task, Journal, Status


# fonction utilisé pour vérifier si l'user authentifié a access à la resource qu'il demande:
# par example, s'il n'est pas membre du project 5 et s'il écrit dans la barre des URLs /project/5
# il va recevoir une page "error 403 permission denied"
# meme chose pour les tache qui ne font pas partie de ses projets (mais il peut voir les tache assignée
# à autres users qui font partie de ses projets

# J'avais pensé de faire une chose similaire en creant un group pour chaque projet, mais je en faisant comme décrit
# ci-dessus j'ai besoin de moins de ligne de code, meme si je ne peux pas utiliser les decorateurs de Group
def limit_access(user, project_members):
    if user not in project_members.all():
        raise PermissionDenied


@login_required()
def projects_list(request):
    current_user = request.user
    user_projects = current_user.project_set.all().order_by('name')

    return render(request, 'taskmanager/projects_list.html', locals())


@login_required()
def show_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # voir la description de cette fonction ci-dessus
    limit_access(request.user, project.members)
    tasks = project.task_set.all().order_by('-start_date', 'name')

    return render(request, 'taskmanager/project.html', locals())


@login_required()
def show_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    limit_access(request.user, task.project.members)
    journals = task.journal_set.all().order_by('-date')

    # j'ai besoin que de la structure (affichage) du form pour la création des journal dans cette view
    form = JournalForm

    return render(request, 'taskmanager/task.html', locals())


# vue qui gère la crèation des journals.
# args:
#       task_id:    j'ai besoin de sélectionner la tache pour savoir où créer le journal
@login_required()
def new_journal(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    limit_access(request.user, task.project.members)

    form = JournalForm(request.POST or None)
    if form.is_valid():
        # crée une nouvelle instance de Journal
        journal = Journal()
        journal.entry = form.cleaned_data["entry"]
        # le journal est assigné à sa tache et a l'utilisateur courant automatiquement
        journal.task = task
        journal.author = request.user
        journal.save()

    # finalemnt on est redirigé sur la page de visualization de la meme tache
    return redirect(show_task, task_id=task_id)


# vue qui gère la crèation des taches'.
# args:
#       project_id:    j'ai besoin de sélectionner le projet pour savoir où créer la tache
@login_required()
def new_task(request, project_id):
    form = TaskForm(request.POST or None)
    project = get_object_or_404(Project, id=project_id)
    limit_access(request.user, project.members)

    # essentiel pour limiter les membres à ceux qui font partie du projet dans le formulaire du template
    form.fields['assignee'].queryset = project.members

    if form.is_valid():
        task = form.save(commit=False)
        task.project = project  # on attribue la tache au projet automatiquement
        task.status = Status.objects.get(name="New")  # ligne probablement redondant avec le modèle
        task.save()

        # si tuot a marché, on est redirigé sur la page de visualization de la tache
        return redirect(show_task, task_id=task.id)

    # sinon il faut la modifier selon les erreurs qui sont apparus
    return render(request, 'taskmanager/edit_task.html', locals())


@login_required()
def edit_task(request, task_id):
    # du moment qu'on utilise le meme template pour gerer la modification et la création des taches, ce flag sert
    # au template pour savoir quoi afficher
    edit_flag = True
    task = get_object_or_404(Task, id=task_id)
    limit_access(request.user, task.project.members)

    # instance de tache à mettre à jours
    form = TaskForm(request.POST or None, instance=task)
    project = task.project  # utilisé dans le template

    # meme chose qui ci-dessus
    form.fields['assignee'].queryset = project.members

    if form.is_valid():
        form.save()

        # si tout s'est bien passé, on voit la tache
        return redirect(show_task, task_id=task_id)

    # sinon il faut la modifier selon les erreurs qui sont apparus
    return render(request, 'taskmanager/edit_task.html', locals())
