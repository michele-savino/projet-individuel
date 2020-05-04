from django.contrib import admin
from django.utils.text import Truncator

from .models import Project, Task, Status, Journal


# je utilise le decorator .register car il est plus compact


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ['members']
    ordering = ['name']
    search_fields = ['name']


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['apercu_entry', 'author', 'task', 'get_project', 'date']
    list_filter = ['author', ]
    date_hierarchy = 'date'
    ordering = ['date']
    search_fields = ['entry']

    def apercu_entry(self, journal):
        """
        Retourne les 40 premiers caractères du contenu du Journal,
        """
        return Truncator(journal.entry).chars(40, truncate='...')

    # pour permettre d'afficher le project auquel la tache du journal appartient
    def get_project(self, journal):
        return journal.task.project

    get_project.short_description = "project"
    apercu_entry.short_description = "entry"


class JournalInline(admin.TabularInline):
    '''
    Pour ajouter des journals directement de la page de la task (mon expérimentation)
    '''
    model = Journal


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'assignee', 'status', 'start_date', 'due_date']
    list_filter = ['project', 'assignee', 'status', 'priority']
    date_hierarchy = 'start_date'
    ordering = ['start_date']
    search_fields = ['name', 'description']

    # Configuration du formulaire d'édition
    fieldsets = (
        ('General', {
            'fields': ['name', 'project', 'assignee'],
        }),
        ('Details', {
            'fields': ['start_date', 'due_date', 'status', 'priority'],
        }),
        ('Optional', {
            'classes': ['collapse', ],
            'fields': ['description']
        }),
    )

    inlines = [JournalInline]  # pour inclure les journal dans la page de la tache


# finalement on registre le status
admin.site.register(Status)
