from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('pydata', views.PYViewSet)

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('list/', views.pylist, name='pylist'),
    path('create/', views.py_create, name='pycreate'),
    path('<int:pk>/', views.py_detail, name='py_detail'),    
    path('delete/<int:pk>/', views.py_delete, name='py_delete'),
    path('update/<int:pk>/', views.py_update, name='py_update'),
]