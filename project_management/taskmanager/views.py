from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Project


@login_required(redirect_field_name='redirected_to')
def projects(request):
    current_user = request.user
    user_projects = current_user.project_set.all()

    return render(request, 'taskmanager/projects.html', locals())
