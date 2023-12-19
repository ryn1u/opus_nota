from django.db import models
from django.contrib.auth.models import User


class Stage(models.IntegerChoices):
    STARTED = 1
    IN_PROGRESS = 2
    FINISHED = 3


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField("created at")
    # assigned_users = models.ManyToManyField(User)


class Track(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField("created at")
    color = models.CharField(max_length=7)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=100)
    notes = models.TextField()
    created_at = models.DateTimeField("created at")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True, null=True)
    stage = models.IntegerField(choices=Stage, default=Stage.STARTED)
    # assigned_users = models.ManyToManyField(User)
