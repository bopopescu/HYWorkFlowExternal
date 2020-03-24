from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('podata', views.POViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
    path('po/list/', views.po_list, name='po_list'),
    path('po/create/', views.po_create, name='po_create'),
]