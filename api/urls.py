from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet, basename="project")

urlpatterns = [
    path('', views.api_root),
    path('', include(router.urls)),
    path('users/<int:pk>/', views.UserDetailViewSet.as_view(), name='user-detail'),
    path('tasks/<int:pk>/', views.TaskDetailViewSet.as_view(), name='task-detail'),
    path('tracks/<int:pk>/', views.TrackDetailViewSet.as_view(), name='track-detail'),
    path('objective/<int:pk>/', views.ObjectiveDetailViewSet.as_view(), name='objective-detail'),
    path('tasks/<int:task_id>/objectives', views.ListCreateObjectiveView.as_view(), name='objective-create'),
    path('projects/<int:project_id>/tasks', views.ListCreateTaskView.as_view(), name='task-create'),
    path('projects/<int:project_id>/tracks', views.ListCreateTrackView.as_view(), name='track-create'),
    path('tracks/<int:track_id>/tasks', views.ListCreateForTrackTaskView.as_view(), name='track-task-create'),
]
