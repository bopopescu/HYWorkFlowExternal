"""URL logic to control Account Task module"""

from django.urls import path, include
from rest_framework import routers
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register('unprocesseddata', views.UnprocessedViewSet, basename='unprocessed')
ROUTER.register('processeddata', views.ProcessedViewSet, basename='processed')
ROUTER.register('completeddata', views.CompletedViewSet, basename='completed')

urlpatterns = [
    path('api/', include(ROUTER.urls)),
    path('list/', views.task_list, name='task_list'),
    path('process_all/<int:pk>', views.task_process_all, name='task_process_all'),
    path('complete_all/<int:pk>', views.task_complete_all, name='task_complete_all'),
]
