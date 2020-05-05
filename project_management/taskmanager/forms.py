from django import forms
from django.core.exceptions import ValidationError

from .models import Journal, Task


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        # je veux editer que le field entry, les autres sont fixés (date et heure actuelles et utilisateur courant)
        fields = ['entry']
        # attributs du widget
        widgets = {'entry': forms.TextInput(attrs={'cols': 10, 'placeholder': "Write here..."})
                   }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # le field project est rempli automatiquement
        fields = ["name", "assignee", "description", "start_date", "due_date", "priority", "status"]
        # attributs du widget
        widgets = {'description': forms.Textarea(attrs={'rows': 4, 'placeholder': "Describe the task..."}),
                   'start_date': forms.SelectDateWidget,
                   'due_date': forms.SelectDateWidget
                   }

    # pour s'assurer que la priorité de la tache soit comprise entre 1 et 10
    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if priority < 1 or priority > 10:
            raise ValidationError('Ensure this value is in the range.')

        return priority  # Ne pas oublier de renvoyer le contenu du champ traité

    # pour s'assurer que la due_date soit successive à la start_date
    def clean_due_date(self):
        start_date = self.cleaned_data['start_date']
        due_date = self.cleaned_data['due_date']
        if due_date < start_date:
            raise ValidationError('The due date must be posterior to the start date.')

        return due_date


# form utilisé à niveau de l'administration pour filtrer les choix de l'admin
class TaskFormAdmin(forms.ModelForm):
    class Meta:
        model = Task
        exclude = []

    # COMMENTE' CAR CA MARCHE PAS DANS TOUS LES CAS
    # # ça permet d'avoir un erreur si l'admin essaye d'assigner une tache à un projet et au meme temps a un user qui
    # # n'est pas membre du projet
    # # On ne peut pas filtrer directement le queryset comme j'ai fait dans la view new_task parce que ici on ne sait pas
    # # encore à quel projet la tache sera assignée. Les deux champs projet et membres depends entre eux et donc je crois
    # # qu'il faut utiliser de l'ajax pour filtrer les choix en temps réel
    # def clean_assignee(self):
    #     assignee = self.cleaned_data['assignee']
    #     project = self.cleaned_data['project']
    #     if assignee not in project.members.all():
    #         raise ValidationError('This user is not a member of the chosen project.')

    # pour s'assurer que la priorité de la tache soit comprise entre 1 et 10
    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if priority < 1 or priority > 10:
            raise ValidationError('Ensure this value is in the range.')

        return priority  # Ne pas oublier de renvoyer le contenu du champ traité

    # pour s'assurer que la due_date soit successive à la start_date
    def clean_due_date(self):
        start_date = self.cleaned_data['start_date']
        due_date = self.cleaned_data['due_date']
        if due_date < start_date:
            raise ValidationError('The due date must be posterior to the start date.')

        return due_date
