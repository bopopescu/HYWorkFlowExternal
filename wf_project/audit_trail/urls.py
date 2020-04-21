from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('auditdrawerdata', views.DrawerViewSet,basename="auditdrawerdata")
router.register('auditdisburseddata', views.DisbursedViewSet,basename="auditdisburseddata")

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('drawerselection/', views.drawer_list, name='audit_trail_drawer_selection'),
    path('audit_trail_report/<int:pk>/', views.audit_trail_report, name='audit_trail_report'),
]