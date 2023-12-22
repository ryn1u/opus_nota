from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Project, Task, Track
from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectModelSerializer, UserSafeReadSerializer, TaskDetailSerializer, TrackDetailSerializer
from django.contrib.auth.models import User


@api_view(['GET'])
def api_root(request):
    return Response({
        'projects': reverse('project-list', request=request, format=None)
    })


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectModelSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return User.objects.none()

        queryset = self.request.user.projects.all()
        return queryset


class UserDetailViewSet(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSafeReadSerializer


class TaskDetailViewSet(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TrackDetailViewSet(RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackDetailSerializer
