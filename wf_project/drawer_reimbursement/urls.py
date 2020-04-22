from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('myreimbursementrequestdata', views.MyReimbursementRequestViewSet, basename='myreimbursementrequestdata')
router.register('teamreimbursementrequestdata', views.TeamReimbursementRequestViewSet, basename='teamreimbursementrequestdata')
router.register('reimbursedrawerdata', views.DrawerViewSet,basename="reimbursedrawerdata")
router.register('reimsbursementlistdata',views.ReimbursementListViewSet,basename="reimsbursementlistdata")
router.register('reimburseddata',views.ReimbursedViewSet,basename="reimburseddata")
router.register('cancelleddata',views.CancelledViewSet,basename="cancelleddata")

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('list/', views.reimbursement_request_list, name='reimbursement_request_list'),

    path('init/', views.reimbursement_request_init, name='reimbursement_request_init'),
    path('initamount/<str:amount>/', views.reimbursement_request_init_amount, name='reimbursement_request_init_amount'),
    path('create/<int:pk>/', views.reimbursement_request_create, name='reimbursement_request_create'),

    path('sendapproval/<int:pk>/', views.reimbursement_request_send_approval, name='reimbursement_request_send_approval'),
    path('<int:pk>/', views.reimbursement_request_detail, name='reimbursement_request_detail'),    
    path('delete/', views.reimbursement_request_delete, name='reimbursement_request_delete'),
    path('update/<int:pk>/', views.reimbursement_request_update, name='reimbursement_request_update'),

    #drawer Reimbursement
    path('drawerselection/', views.drawer_list, name='reimbursedrawer_selection'),
    path('reimbursement_list/<int:drawerpk>/', views.drawer_reimbursement_list, name='drawer_reimbursement_list'),
    path('reimbursement_reimbursed/<int:pk>&<int:drawerpk>/', views.drawer_reimbursement_reimbursed, name='drawer_reimbursement_reimbursed'),
    path('reimbursement_cancelled/<int:pk>&<int:drawerpk>/', views.drawer_reimbursement_cancel, name='drawer_reimbursement_cancel'),
]