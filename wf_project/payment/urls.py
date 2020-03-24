from django.urls import path
from . import views

urlpatterns = [    
    path('py/list/', views.pylist, name='pylist'),
    path('py/create/', views.pycreate, name='pycreate'),
]