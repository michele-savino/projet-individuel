from django.contrib import admin

from .models import Project, Task, Status


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ['members']
    ordering = ['name']
    search_fields = ['name']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task)
admin.site.register(Status)
