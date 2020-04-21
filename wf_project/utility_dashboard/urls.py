from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('utilityapprovaldata', views.ApprovalViewSet, basename='utilityapprovaldata')
router.register('utilityapproverdata', views.ApproverViewSet, basename='utilityapproverdata')
router.register('utilityallapproverdata', views.AllApproverViewSet, basename='utilityallapproverdata')
router.register('utilityccdata', views.CCViewSet, basename='utilityccdata')
router.register('accountselection', views.AccountViewSet, basename='accountselection')

urlpatterns = [    
    path('api/', include(router.urls)),
    path('accountselection/', views.account_selection_list, name='account_selection_list'),
    path('list/<int:pk>/', views.approval_list, name='utility_approval_list'),
    path('detail/<int:pk>/', views.approval_detail, name='utility_approval_detail'),    
    path('history/<int:pk>/', views.approval_history, name='utility_approval_history'),
    path('update/<int:pk>/', views.approval_update, name='utility_approval_update'),
    path('approver/create/<int:pk>/', views.approver_create, name='utility_approver_create'),    
    path('approver/delete/', views.approver_delete, name='utility_approver_delete'),
    path('cc/create/<int:pk>/', views.cc_create, name='utility_cc_create'),    
    path('cc/delete/', views.cc_delete, name='utility_cc_delete'),
    path('approve/', views.approve, name='utility_approve'),
    path('reject/', views.reject, name='utility_reject'),
    path('count/<int:pk>', views.utility_bill_count, name='utility_bill_count'),
    path('approve_all/<int:pk>', views.approve_all, name='utility_approve_all'),
    path('reject_all/<int:pk>', views.reject_all, name='utility_reject_all'),
]