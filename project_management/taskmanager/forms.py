from django import forms

from .models import Journal, Task


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['entry']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "assignee", "start_date", "due_date", "priority", "status"]
