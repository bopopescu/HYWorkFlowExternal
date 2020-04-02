from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('mypydata', views.MyPYViewSet)
router.register('teampydata', views.TeamPYViewSet)
router.register('pydata', views.PYViewSet)
router.register('pyitem', views.PYItemViewSet)
router.register('pyattachment',views.PYAttachmentViewSet)

urlpatterns = [ 
    path('api/', include(router.urls)), 
    path('list/', views.pylist, name='pylist'),


    path('create/', views.py_create, name='pycreate'),
    path('create/<int:pk>/', views.py_create_edit, name='py_create_edit'),
    path('createattachment_create/<int:pk>/', views.py_attachment_create_formcreate, name='py_attachment_create_formcreate'),
    path('deleteattachment_create/<int:pk>/', views.py_attachment_delete_formcreate, name='py_attachment_delete_formcreate'),
    path('createitem_create/<int:pk>/', views.py_item_create_formcreate, name='py_item_create_formcreate'),
    path('deleteitem_create/<int:pk>/', views.py_item_delete_formcreate, name='py_item_delete_formcreate'),

    path('<int:pk>/', views.py_detail, name='py_detail'),    
    path('delete/<int:pk>/', views.py_delete, name='py_delete'),
    path('update/<int:pk>/', views.py_update, name='py_update'),
    path('createitem/<int:pk>/', views.py_item_create, name='py_item_create'),
    path('deleteitem/<int:pk>/', views.py_item_delete, name='py_item_delete'),
    path('createattachment/<int:pk>/', views.py_attachment_create, name='py_attachment_create'),
    path('deleteattachment/<int:pk>/', views.py_attachment_delete, name='py_attachment_delete'),
]