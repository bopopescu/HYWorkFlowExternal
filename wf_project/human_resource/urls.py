from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('staffdata', views.StaffViewSet)

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('list/', views.staff_list, name='staff_list'),
    path('create/', views.staff_create, name='staff_create'),
    path('<int:pk>/', views.staff_detail, name='staff_detail'),    
    path('delete/<int:pk>/', views.staff_delete, name='staff_delete'),
    path('update/<int:pk>/', views.staff_update, name='staff_update'),
]