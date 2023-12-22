from .models import Project, Task, Stage, Track, Objective
from rest_framework import serializers
from django.contrib.auth.models import User


class TaskUrlSerializer(serializers.HyperlinkedModelSerializer):
    stage = serializers.SerializerMethodField(method_name="get_stage")

    def get_stage(self, obj):
        return Stage(obj.stage).name

    class Meta:
        model = Task
        fields = ('url', 'id', 'title', 'stage')


class TrackUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('url', 'id', 'name')


class ObjectiveUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Objective
        fields = ('name', 'completed')


class ProjectModelSerializer(serializers.ModelSerializer):
    assigned_users = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')
    tracks = TrackUrlSerializer(many=True, read_only=True)
    tasks = TaskUrlSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'created_at', 'assigned_users', 'tracks', 'tasks')


class UserSafeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class TrackDetailSerializer(serializers.ModelSerializer):
    tasks = TaskUrlSerializer(many=True, read_only=True)
    project = serializers.HyperlinkedRelatedField(read_only=True, view_name='project-detail')
    objectives = ObjectiveUrlSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = ('name', 'created_at', 'color', 'project', 'tasks', 'objectives')


class TaskDetailSerializer(serializers.ModelSerializer):
    stage_name = serializers.SerializerMethodField(method_name="get_stage")
    track = serializers.HyperlinkedRelatedField(read_only=True, view_name='track-detail')
    project = serializers.HyperlinkedRelatedField(read_only=True, view_name='project-detail')
    assigned_users = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')

    def get_stage(self, obj):
        return Stage(obj.stage).name

    class Meta:
        model = Task
        fields = ('title', 'notes', 'created_at', 'project', 'track', 'stage', 'stage_name', 'assigned_users',)

