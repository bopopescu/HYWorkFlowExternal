from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('drawerdata', views.DrawerViewSet)
router.register('disbursementdata',views.DisbursementListViewSet)

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('drawerselection/', views.drawer_list, name='drawer_selection'),
    path('disbursement_list/<int:drawerpk>/', views.drawer_disbursement_list, name='disbursement_list'),
]