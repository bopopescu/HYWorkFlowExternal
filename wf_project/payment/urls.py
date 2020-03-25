from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('pydata', views.PYViewSet)

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('py/list/', views.pylist, name='pylist'),
    path('py/create/', views.pycreate, name='pycreate'),
]