from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework import status

from .models import Project, Task, Track, Objective
from rest_framework.viewsets import ModelViewSet
from . import serializers
from django.contrib.auth.models import User


@api_view(['GET'])
def api_root(request: Request):
    return Response({
        'projects': reverse('project-list', request=request, format=None)
    })


class ListCreateObjectiveView(generics.ListCreateAPIView):
    serializer_class = serializers.ListCreateObjectiveSerializer

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Objective.objects.filter(task_id=task_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['task_id'] = kwargs['task_id']
            serializer.validated_data['completed'] = False

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)


class ListCreateTaskView(generics.ListCreateAPIView):
    serializer_class = serializers.ListCreateTaskSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project_id=project_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['project_id'] = kwargs['project_id']

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)


class ListCreateForTrackTaskView(generics.ListCreateAPIView):
    serializer_class = serializers.ListCreateTaskSerializer

    def get_queryset(self):
        track_id = self.kwargs['track_id']
        return Task.objects.filter(track_id=track_id)

    def post(self, request, *args, **kwargs):
        track = Track.objects.get(pk=kwargs['track_id'])
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['track_id'] = kwargs['track_id']
            serializer.validated_data['project_id'] = track.project_id

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectViewSet(ModelViewSet):
    serializer_class = serializers.ProjectModelSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return User.objects.none()

        queryset = self.request.user.projects.all()
        return queryset


class UserDetailViewSet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSafeReadSerializer


class TaskDetailViewSet(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskDetailSerializer


class TrackDetailViewSet(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = serializers.TrackDetailSerializer


class ObjectiveDetailViewSet(generics.RetrieveAPIView):
    queryset = Objective.objects.all()
    serializer_class = serializers.ObjectiveDetailSerializer
