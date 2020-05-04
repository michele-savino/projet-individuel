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

    # le meme methode peuvent etre activé à niveau du model pour filtrer aussi les choix de l'admin,
    # mais j'ai preferé le faire ici comme dans le tutoriel
