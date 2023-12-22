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
]
