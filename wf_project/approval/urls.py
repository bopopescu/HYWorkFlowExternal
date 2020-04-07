from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('approvaldata', views.ApprovalViewSet, basename='approvaldata')
router.register('approverdata', views.ApproverViewSet, basename='approverdata')
router.register('allapproverdata', views.AllApproverViewSet, basename='allapproverdata')
router.register('ccdata', views.CCViewSet, basename='ccdata')

urlpatterns = [    
    path('api/', include(router.urls)),
    path('list/', views.approval_list, name='approval_list'),
    path('detail/<int:pk>/', views.approval_detail, name='approval_detail'),    
    path('history/<int:pk>/', views.approval_history, name='approval_history'),
    path('update/<int:pk>/', views.approval_update, name='approval_update'),
    path('approver/create/<int:pk>/', views.approver_create, name='approver_create'),    
    path('approver/delete/', views.approver_delete, name='approver_delete'),
    path('cc/create/<int:pk>/', views.cc_create, name='cc_create'),    
    path('cc/delete/', views.cc_delete, name='cc_delete'),
    path('approve/', views.approve, name='approve'),
    path('reject/', views.reject, name='reject'),
]