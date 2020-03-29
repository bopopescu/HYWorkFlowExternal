from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('approverdata', views.ApproverViewSet)
router.register('ccdata', views.CCViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
    path('list/', views.approval_list, name='approval_list'),
    path('detail/<int:pk>/', views.approval_detail, name='approval_detail'),    
    path('update/<int:pk>/', views.approval_update, name='approval_update'),
    path('approver/create/<int:pk>/', views.approver_create, name='approver_create'),
    path('cc/create/<int:pk>/', views.cc_create, name='cc_create'),
]