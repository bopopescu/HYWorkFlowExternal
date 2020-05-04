from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('mystocktransfer', views.MyStockTransferViewSet,basename="mystocktransfer")
router.register('teamstocktransfer', views.TeamStockTransferViewSet,basename="teamstocktransfer")
router.register('mystockadjustment', views.MyStockAdjustmentViewSet,basename="mystockadjustment")
router.register('teamstockadjustment', views.TeamStockAdjustmentViewSet,basename="teamstockadjustment")
router.register('mystockissuing', views.MyStockIssuingViewSet,basename="mystockissuing")
router.register('teamstockissuing', views.TeamStockIssuingViewSet,basename="teamstockissuing")

#item & attachment
router.register('stocktransferdetail', views.StockTransferDetailViewSet,basename="stocktransferdetail")
router.register('stocktransferattachment',views.StockTransferAttachmentViewSet,basename="stocktransferattachment")
router.register('stockadjustmentdetail', views.StockAdjustmentDetailViewSet,basename="stockadjustmentdetail")
router.register('stockadjustmentattachment',views.StockAdjustmentAttachmentViewSet,basename="stockadjustmentattachment")
router.register('stockissuingdetail', views.StockIssuingDetailViewSet,basename="stockissuingdetail")
router.register('stockissuingattachment',views.StockIssuingAttachmentViewSet,basename="stockissuingattachment")

urlpatterns = [ 
    path('api/', include(router.urls)), 
    #stock transfer
    path('stock_transfer_list/', views.stock_transfer_list, name='stock_transfer_list'),

    path('stock_transfer_create/init/', views.stock_transfer_init, name='stock_transfer_init'),
    path('stock_transfer_create/<int:pk>/', views.stock_transfer_create, name='stock_transfer_create'),

    path('stock_transfer_submit/<int:pk>/', views.stock_transfer_submit, name='stock_transfer_submit'),
    path('stock_transfer/<int:pk>/', views.stock_transfer_detail, name='stock_transfer_detail'),    
    path('stock_transfer_delete/', views.stock_transfer_delete, name='stock_transfer_delete'),
    path('stock_transfer_update/<int:pk>/', views.stock_transfer_update, name='stock_transfer_update'),
    path('createstocktransferitem/<int:pk>/', views.stock_transfer_detail_create, name='stock_transfer_detail_create'),
    path('deletestocktransferitem/', views.stock_transfer_detail_delete, name='stock_transfer_detail_delete'),
    path('createstocktransferattachment/<int:pk>/', views.stock_transfer_attachment_create, name='stock_transfer_attachment_create'),
    path('deletestocktransferattachment/<int:pk>/', views.stock_transfer_attachment_delete, name='stock_transfer_attachment_delete'),

    #stock adjustment
    path('stock_adjustment_list/', views.stock_adjustment_list, name='stock_adjustment_list'),

    path('stock_adjustment_create/init/', views.stock_adjustment_init, name='stock_adjustment_init'),
    path('stock_adjustment_create/<int:pk>/', views.stock_adjustment_create, name='stock_adjustment_create'),

    path('stock_adjustment_submit/<int:pk>/', views.stock_adjustment_submit, name='stock_adjustment_submit'),
    path('stock_adjustment/<int:pk>/', views.stock_adjustment_detail, name='stock_adjustment_detail'),    
    path('stock_adjustment_delete/', views.stock_adjustment_delete, name='stock_adjustment_delete'),
    path('stock_adjustment_update/<int:pk>/', views.stock_adjustment_update, name='stock_adjustment_update'),
    path('createstockadjustmentitem/<int:pk>/', views.stock_adjustment_detail_create, name='stock_adjustment_detail_create'),
    path('deletestockadjustmentitem/', views.stock_adjustment_detail_delete, name='stock_adjustment_detail_delete'),
    path('createstockadjustmentattachment/<int:pk>/', views.stock_adjustment_attachment_create, name='stock_adjustment_attachment_create'),
    path('deletestockadjustmentattachment/<int:pk>/', views.stock_adjustment_attachment_delete, name='stock_adjustment_attachment_delete'),

    #stock issuing
    path('stock_issuing_list/', views.stock_issuing_list, name='stock_issuing_list'),

    path('stock_issuing_create/init/', views.stock_issuing_init, name='stock_issuing_init'),
    path('stock_issuing_create/<int:pk>/', views.stock_issuing_create, name='stock_issuing_create'),

    path('ajax/stock-load-delivery-address/', views.load_delivery_address, name='ajax_stock_load_delivery'),

    path('stock_issuing_submit/<int:pk>/', views.stock_issuing_submit, name='stock_issuing_submit'),
    path('stock_issuing/<int:pk>/', views.stock_issuing_detail, name='stock_issuing_detail'),    
    path('stock_issuing_delete/', views.stock_issuing_delete, name='stock_issuing_delete'),
    path('stock_issuing_update/<int:pk>/', views.stock_issuing_update, name='stock_issuing_update'),
    path('createstockissuingitem/<int:pk>/', views.stock_issuing_detail_create, name='stock_issuing_detail_create'),
    path('deletestockissuingitem/', views.stock_issuing_detail_delete, name='stock_issuing_detail_delete'),
    path('createstockissuingattachment/<int:pk>/', views.stock_issuing_attachment_create, name='stock_issuing_attachment_create'),
    path('deletestockissuingattachment/<int:pk>/', views.stock_issuing_attachment_delete, name='stock_issuing_attachment_delete'),
]