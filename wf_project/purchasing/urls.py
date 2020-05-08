from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('mypodata', views.MyPOViewSet, basename='mypo')
router.register('teampodata', views.TeamPOViewSet, basename='teampo')
router.register('poattachment', views.POAttachmentViewSet, basename='poattachment')
router.register('pocomparison2attachment', views.POComparison2AttachmentViewSet, basename='pocv2attachment')
router.register('pocomparison3attachment', views.POComparison3AttachmentViewSet, basename='pocv3attachment')
router.register('podetail', views.PODetailViewSet, basename='podetail')
router.register('awaitgrndata', views.AwaitGRNViewSet, basename='awaitgrn')
router.register('receivedgrndata', views.ReceivedGRNViewSet, basename='receivedgrn')
router.register('awaitpidata', views.AwaitPIViewSet, basename='awaitpi')
router.register('receivedpidata', views.ReceivedPIViewSet, basename='receivedpi')
router.register('awaitpcndata', views.MyPOViewSet, basename='awaitpcn')
router.register('receivedpcndata', views.MyPOViewSet, basename='receivedpcn')
router.register('awaitpdndata', views.MyPOViewSet, basename='awaitpdn')
router.register('receivedpdndata', views.MyPOViewSet, basename='receivedpdn')

urlpatterns = [    
    path('api/', include(router.urls)),
    path('po/list/<int:pk>/', views.po_list, name='po_list'),
    
    path('po/init/<int:pk>/', views.po_init, name='po_init'),
    path('po/create/<int:pk>/', views.po_create, name='po_create'),
    
    path('po/sendapproval/<int:pk>', views.po_send_approval, name='po_send_approval'),
    path('po/<int:pk>/', views.po_detail, name='po_detail'), 
    path('po/delete/', views.po_delete, name='po_delete'), 
    path('po/update/<int:pk>/', views.po_update, name='po_update'),

    path('po/createattachment/<int:pk>/', views.po_attachment_create, name='po_attachment_create'),
    path('po/createcov2attachment/<int:pk>/', views.po_cov2_attachment_create, name='po_cov2_attachment_create'),
    path('po/createcov3attachment/<int:pk>/', views.po_cov3_attachment_create, name='po_cov3_attachment_create'),
    
    path('po/deleteattachment/<int:pk>/', views.po_attachment_delete, name='po_attachment_delete'),
    path('po/deletecov2attachment/<int:pk>/', views.po_cov2_attachment_delete, name='po_cov2_attachment_delete'),
    path('po/deletecov3attachment/<int:pk>/', views.po_cov3_attachment_delete, name='po_cov3_attachment_delete'),
    
    path('po/createdetail/<int:pk>/', views.po_detail_create, name='po_detail_create'),
    path('po/deletedetail/<int:pk>/', views.po_detail_delete, name='po_detail_delete'),
    
    path('ajax/load-delivery-address/', views.load_delivery_address, name='ajax_load_delivery'),
    path('ajax/load-vendor-address/', views.load_vendor_address, name='ajax_load_vendor'),

    path('grn/list/<int:pk>/', views.grn_list, name='grn_list'),
    path('grn/init/<int:pk>/', views.grn_init, name='grn_init'),
    path('grn/create/<int:pk>/', views.grn_create, name='grn_create'),
    path('grn/<int:pk>/', views.grn_detail, name='grn_detail'),
    path('grn/sendtostock/<int:pk>/', views.grn_send_to_stock, name='grn_send_to_stock'),

    path('pi/list/<int:pk>/', views.pi_list, name='pi_list'),
    path('pi/init/<int:pk>/', views.pi_init, name='pi_init'),
    path('pi/create/<int:pk>/', views.pi_create, name='pi_create'),
    path('pi/<int:pk>/', views.pi_detail, name='pi_detail'),
    path('pi/sendtopr/<int:pk>/', views.pi_send_to_pr, name='pi_send_to_pr'),

    path('pcn/list/<int:pk>/', views.pcn_list, name='pcn_list'),    
    path('pcn/<int:pk>/', views.pcn_detail, name='pcn_detail'), 

    path('pdn/list/<int:pk>/', views.pdn_list, name='pdn_list'),   
    path('pdn/<int:pk>/', views.pdn_detail, name='pdn_detail'),

    path('po/print/<int:pk>/', views.po_print, name='po_print'),
    path('grn/print/<int:pk>/', views.grn_print, name='grn_print'),
    path('pi/print/<int:pk>/', views.pi_print, name='pi_print'),
]