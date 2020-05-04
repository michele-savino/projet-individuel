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


# pour s'assurer que la priorité de la tache soit comprise entre 1 et 10
def validate_priority(value):
    if value < 1 or value > 10:
        raise ValidationError('Ensure this value is between 1 and 10')


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Assigned to")
    start_date = models.DateField(default=date.today)
    due_date = models.DateField(default=date.today)
    priority = models.SmallIntegerField(validators=[validate_priority],
                                        default=DEFAULT_PRIORITY)
    # si le status est supprimé, la tache n'est pas supprimé
    status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default=DEFAULT_STATUS_ID)

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
