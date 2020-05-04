from django import forms

from .models import Journal, Task


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['entry']


#controllare se la data di fine è dopo quella di inizio

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "assignee", "description", "start_date", "due_date", "priority", "status"]
        widgets = {'description': forms.Textarea(attrs={'rows': 4}),
                   'start_date': forms.SelectDateWidget,
                   'due_date': forms.SelectDateWidget,}
