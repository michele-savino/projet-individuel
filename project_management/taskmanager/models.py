from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


## aggiustare gli attributi dei caratteri in funzione del risultato finale
# negli attributi data timezone.now non va bene perchè non tiene in conto dei fusi
# AGGIUNGERE SLUUUUUG

class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'status'

    def __str__(self):
        return self.name


DEFAULT_STATUS_ID = 1
DEFAULT_PRIORITY = 1


class Task(models.Model):
    # fare in modo che solo i membri del progetto possano essere assegnati al task e non tutti

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Assigned to")
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    priority = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=DEFAULT_PRIORITY)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=DEFAULT_STATUS_ID)

    def __str__(self):
        return self.name


class Journal(models.Model):
    date = models.DateField(default=timezone.now)
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.entry
