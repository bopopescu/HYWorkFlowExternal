from django.urls import path
from . import views

urlpatterns = [    
    path('po/list/', views.polist, name='polist'),
    path('po/create/', views.pocreate, name='pocreate'),
]