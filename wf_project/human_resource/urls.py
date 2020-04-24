from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('staffdata', views.StaffViewSet,basename="staffdata")
router.register('mystaffdata', views.MyStaffViewSet,basename="mystaffdata")
router.register('teamstaffdata', views.TeamStaffViewSet,basename="teamstaffdata")
router.register('staffjobrequirement',views.StaffJobRequirementViewSet,basename="staffjobrequirement")
router.register('staffjobresponsible',views.StaffJobResponsibleViewSet,basename="staffjobresponsible")
router.register('staffplatform',views.StaffPlatformViewSet,basename="staffplatform")
router.register('staffcandidate',views.StaffCandidateViewSet,basename="staffcandidate")

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('list/', views.staff_list, name='staff_list'),


    path('create/', views.staff_init, name='staff_init'),
    path('create/<int:pk>/', views.staff_create, name='staff_create'),
    path('<int:pk>/', views.staff_detail, name='staff_detail'),    
    path('afterapprove/<int:pk>/', views.staff_after_approve, name='staff_after_approve'),
    path('delete/<int:pk>/', views.staff_delete, name='staff_delete'),
    path('update/<int:pk>/', views.staff_update, name='staff_update'),
    path('sendapproval/<int:pk>/', views.staff_send_approval, name='staff_send_approval'),

    path('createrequirement/<int:pk>/', views.staff_requirement_create, name='staff_requirement_create'),
    path('deleterequirement/<int:pk>/', views.staff_requirement_delete, name='staff_requirement_delete'),

    path('createresponsible/<int:pk>/', views.staff_responsible_create, name='staff_responsible_create'),
    path('deleteresponsible/<int:pk>/', views.staff_responsible_delete, name='staff_responsible_delete'),

    path('createplatform/<int:pk>/', views.staff_platform_create, name='staff_platform_create'),
    path('deleteplatform/<int:pk>/', views.staff_platform_delete, name='staff_platform_delete'),

    path('createcandidate/<int:pk>/', views.staff_candidate_create, name='staff_candidate_create'),
    path('deletecandidate/<int:pk>/', views.staff_candidate_delete, name='staff_candidate_delete'),
]