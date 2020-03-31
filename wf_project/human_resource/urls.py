from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('staffdata', views.StaffViewSet)
router.register('mystaffdata', views.MyStaffViewSet)
router.register('teamstaffdata', views.TeamStaffViewSet)
router.register('staffjobrequirement',views.StaffJobRequirementViewSet)
router.register('staffjobresponsible',views.StaffJobResponsibleViewSet)

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('list/', views.staff_list, name='staff_list'),
    path('create/', views.staff_create, name='staff_create'),
    path('<int:pk>/', views.staff_detail, name='staff_detail'),    
    path('delete/<int:pk>/', views.staff_delete, name='staff_delete'),
    path('update/<int:pk>/', views.staff_update, name='staff_update'),
    path('createrequirement/<int:pk>/', views.staff_requirement_create, name='staff_requirement_create'),
    path('deleterequirement/<int:pk>/', views.staff_requirement_delete, name='staff_requirement_delete'),
    path('createresponsible/<int:pk>/', views.staff_responsible_create, name='staff_responsible_create'),
    path('deleteresponsible/<int:pk>/', views.staff_responsible_delete, name='staff_responsible_delete'),
]