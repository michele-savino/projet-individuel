from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=30, unique=True)  # je veux de status unique

    class Meta:
        verbose_name_plural = 'status'  # pour ne pas avoir 2 s au plural

    def __str__(self):
        return self.name


# valeurs de default
DEFAULT_STATUS_ID = 1
DEFAULT_PRIORITY = 1


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Assigned to")
    start_date = models.DateField(default=date.today)
    due_date = models.DateField(default=date.today)
    priority = models.SmallIntegerField(default=DEFAULT_PRIORITY, help_text="Between 1 and 10")
    # si le status est supprimé, la tache n'est pas supprimé
    status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default=DEFAULT_STATUS_ID)

    '''
    # A decommenter si on veut aussi valider les choix de l'administrateur,
    # en faisant le filtrage des dates et de la prioritè directement sur le models et pas seulement du form
    def clean(self):
        if self.priority < 1 or self.priority > 10:
            raise ValidationError('Ensure this value is in the range')
        if self.due_date < self.start_date:
            raise ValidationError('The due date cannot follow the start date')
    '''

    # Pour controler si l'user selectionné est membre du projet.
    # Je suis pas arriver à limiter les choix montrés dans la page administrateur comme j'ai fait dans la view new_task,
    # parce que je n'ai pas access à la view de l'admininistration, mais au moins j'empeche l'admin de faire un mauvais choix
    def clean(self):
        if self.assignee not in self.project.members.all():
            raise ValidationError({'assignee': 'This user is not a member of the chosen project.'})

    def __str__(self):
        return self.name


class Journal(models.Model):
    # date et heure fixées au moment de la création
    date = models.DateTimeField(auto_now_add=True)
    entry = models.CharField(max_length=240)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.entry
