from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('drawerdata', views.DrawerViewSet)
router.register('disbursementdata',views.DisbursementListViewSet,basename="disbursementdata")
router.register('disburseddata',views.DisbursedViewSet,basename="disburseddata")
router.register('disbursementcancelleddata',views.CancelledViewSet,basename="disbursementcancelleddata")

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('drawerselection/', views.drawer_list, name='drawer_selection'),
    path('disbursement_list/<int:drawerpk>/', views.drawer_disbursement_list, name='disbursement_list'),
    path('disbursement_disbursed/<int:pk>&<int:drawerpk>&<str:userid>&<str:password>/', views.drawer_disbursement_disbursed, name='disbursement_disburse'),
    path('disbursement_cancelled/<int:pk>&<int:drawerpk>/', views.drawer_disbursement_cancel, name='disbursement_cancel'),
    path('print/<int:pk>/', views.payment_voucher_print, name='payment_voucher_print'),
]