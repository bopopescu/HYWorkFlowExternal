from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('mypodata', views.MyPOViewSet)
router.register('teampodata', views.TeamPOViewSet)
router.register('poattachment', views.POAttachmentViewSet)
router.register('pocomparison2attachment', views.POComparison2AttachmentViewSet)
router.register('pocomparison3attachment', views.POComparison3AttachmentViewSet)
router.register('podetail', views.PODetailViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
    path('po/', views.po_index, name='po_index'),
    path('po/list/', views.po_list, name='po_list'),
    
    path('po/create/', views.po_init, name='po_create'),
    path('po/create/<int:pk>/', views.po_create, name='po_create_edit'),
    
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
]