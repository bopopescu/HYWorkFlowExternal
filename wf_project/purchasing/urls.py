from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('mypodata', views.MyPOViewSet)
router.register('teampodata', views.TeamPOViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
     path('po/', views.po_index, name='po_index'),
    path('po/list/', views.po_list, name='po_list'),
    path('po/create/', views.po_create, name='po_create'),
    #path('po/<int:pk>/', views.po_detail, name='po_detail'), 
    path('po/delete/<int:pk>/', views.po_delete, name='po_delete'), 
    #path('po/update/<int:pk>/', views.po_update, name='po_update'),
]