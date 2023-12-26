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
    tasks = TaskUrlSerializer(many=True, read_only=True)
    class Meta:
        model = Track
        fields = ('url', 'id', 'name', 'tasks')


class ObjectiveUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Objective
        fields = ('url', 'name', 'completed')


class ProjectModelSerializer(serializers.ModelSerializer):
    assigned_users = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')
    tracks = TrackUrlSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField('get_tasks_without_tracks')
    tasks_url = serializers.HyperlinkedIdentityField(view_name='task-create', lookup_url_kwarg='project_id')
    tracks_url = serializers.HyperlinkedIdentityField(view_name='track-create', lookup_url_kwarg='project_id')

    def get_tasks_without_tracks(self, obj):
        queryset = Task.objects.filter(project_id=obj.id).filter(track_id__isnull=True).select_related()
        serializer = TaskUrlSerializer(instance=queryset, many=True, read_only=True, context=self.context)
        return serializer.data

    class Meta:
        model = Project
        fields = ('name', 'created_at', 'assigned_users', 'tracks', 'tasks', 'tasks_url', 'tracks_url')


class UserSafeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class TrackDetailSerializer(serializers.ModelSerializer):
    tasks = TaskUrlSerializer(many=True, read_only=True)
    project = serializers.HyperlinkedRelatedField(view_name='project-detail', queryset=Project.objects.all())
    tasks_url = serializers.HyperlinkedIdentityField(view_name='track-task-create', lookup_url_kwarg='track_id')
    name = serializers.CharField(max_length=30)
    color = serializers.CharField(max_length=7)

    class Meta:
        model = Track
        fields = ('name', 'created_at', 'color', 'project', 'tasks', 'tasks_url', 'color')


class ListCreateObjectiveSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True)
    completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Objective
        fields = ('url', 'id', 'name', 'description', 'completed')


class ListCreateTaskSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(max_length=100)
    notes = serializers.CharField(allow_blank=True)
    stage_name = serializers.SerializerMethodField(read_only=True, method_name="get_stage")

    def get_stage(self, obj):
        return Stage(obj.stage).name

    class Meta:
        model = Task
        fields = ('url', 'id', 'title', 'notes', 'stage_name')


class ListCreateTrackSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=30)
    color = serializers.CharField(max_length=7)
    tasks = TaskUrlSerializer(read_only=True, many=True)

    class Meta:
        model = Track
        fields = ('url', 'name', 'color', 'tasks', 'color')


class ObjectiveDetailSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(view_name='task-detail', queryset=Task.objects.all())
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True)
    
    class Meta:
        model = Objective
        fields = ('name', 'description', 'task', 'completed')


class TaskDetailSerializer(serializers.ModelSerializer):
    stage_name = serializers.SerializerMethodField(method_name="get_stage")
    track = serializers.HyperlinkedRelatedField(view_name='track-detail', allow_null=True, queryset=Track.objects.all())
    project = serializers.HyperlinkedRelatedField(view_name='project-detail', queryset=Project.objects.all())
    assigned_users = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail') # add assigned users url
    objectives = ObjectiveUrlSerializer(many=True, read_only=True)
    objectives_url = serializers.HyperlinkedIdentityField(view_name='objective-create', lookup_url_kwarg='task_id')

    def get_stage(self, obj):
        return Stage(obj.stage).name

    class Meta:
        model = Task
        fields = ('title', 'notes', 'created_at', 'project', 'track', 'stage', 'stage_name', 'assigned_users',
                  'objectives', 'objectives_url')

