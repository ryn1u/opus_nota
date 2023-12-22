from django.contrib import admin
from .models import Task, Track, Project, Objective


admin.site.register(Task)
admin.site.register(Track)
admin.site.register(Project)
admin.site.register(Objective)
