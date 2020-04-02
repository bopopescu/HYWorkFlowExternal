from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('drawerdata', views.DrawerViewSet)
router.register('disbursementdata',views.DisbursementListViewSet)
router.register('disburseddata',views.DisbursedViewSet)
router.register('cancelleddata',views.CancelledViewSet)

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('drawerselection/', views.drawer_list, name='drawer_selection'),
    path('disbursement_list/<int:drawerpk>/', views.drawer_disbursement_list, name='disbursement_list'),
    path('disbursement_disbursed/<int:pk>&<int:drawerpk>/', views.drawer_disbursement_disbursed, name='disbursement_list'),
    path('disbursement_cancelled/<int:pk>&<int:drawerpk>/', views.drawer_disbursement_cancel, name='disbursement_list'),
]