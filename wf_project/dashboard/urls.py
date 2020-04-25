from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [ 
    path('drawer_amount/<int:pk>/', views.count_drawer_amount, name='count_drawer_amount'),
]