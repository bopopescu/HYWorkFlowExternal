from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('myreimbursementrequestdata', views.MyReimbursementRequestViewSet, basename='myreimbursementrequestdata')
router.register('teamreimbursementrequestdata', views.TeamReimbursementRequestViewSet, basename='teamreimbursementrequestdata')

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('list/', views.reimbursement_request_list, name='reimbursement_request_list'),

    path('init/', views.reimbursement_request_init, name='reimbursement_request_init'),
    path('create/<int:pk>/', views.reimbursement_request_create, name='reimbursement_request_create'),

    path('sendapproval/<int:pk>/', views.reimbursement_request_send_approval, name='reimbursement_request_send_approval'),
    path('<int:pk>/', views.reimbursement_request_detail, name='reimbursement_request_detail'),    
    path('delete/', views.reimbursement_request_delete, name='reimbursement_request_delete'),
    path('update/<int:pk>/', views.reimbursement_request_update, name='reimbursement_request_update'),
]