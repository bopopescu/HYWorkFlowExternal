from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('mystaffotdata', views.MyStaffOTViewSet, basename='mystaffot')
router.register('teamstaffotdata', views.TeamStaffOTViewSet, basename='teamstaffot')
router.register('staffotdetail', views.StaffOTDetailViewSet, basename='staffotdetail')

urlpatterns = [
    path('api/', include(router.urls)), 
    path('list/<int:pk>/', views.staff_ot_list, name='staff_ot_list'),

    path('init/<int:pk>/', views.staff_ot_init, name='staff_ot_init'),
    path('create/<int:pk>/', views.staff_ot_create, name='staff_ot_create'),

    path('sendapproval/<int:pk>/', views.staff_ot_send_approval, name='staff_ot_send_approval'),
    path('<int:pk>/', views.staff_ot_detail, name='staff_ot_detail'),
    path('delete/', views.staff_ot_delete, name='staff_ot_delete'),
    path('update/<int:pk>/', views.staff_ot_update, name='staff_ot_update'),
    path('createdetail/<int:pk>/', views.staff_ot_detail_create, name='staff_ot_detail_create'),
    path('deletedetail/', views.staff_ot_detail_delete, name='staff_ot_detail_delete'),
]
