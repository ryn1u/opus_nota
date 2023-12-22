from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Now


class Stage(models.IntegerChoices):
    STARTED = 1
    IN_PROGRESS = 2
    FINISHED = 3


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(db_default=Now())
    assigned_users = models.ManyToManyField(User, related_name="projects")

    def __str__(self):
        return f"PROJECT-{self.name}"


class Track(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(db_default=Now())
    color = models.CharField(max_length=7)
    project = models.ForeignKey(Project, related_name="tracks", on_delete=models.CASCADE)

    def __str__(self):
        return f"TRACK-{self.name}"


class Task(models.Model):
    title = models.CharField(max_length=100)
    notes = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(db_default=Now(), blank=True)
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name="tasks", on_delete=models.CASCADE, blank=True, null=True)
    stage = models.IntegerField(choices=Stage, default=Stage.STARTED)
    assigned_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.title}-{Stage(self.stage).name}"


class Objective(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)
    task = models.ForeignKey(Task, related_name="objectives", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}-{'COMPLETED' if self.completed else 'INCOMPLETE'}"
