from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('mymemodata', views.MyMemoViewSet)
router.register('teammemodata', views.TeamMemoViewSet)
router.register('memoattachment', views.MemoAttachmentViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
    path('', views.memo_index, name='memo_index'),
    path('list/', views.memo_list, name='memo_list'),

    path('create/', views.memo_create, name='memo_create'),
    path('create/<int:pk>', views.memo_create_edit, name='memo_create_edit'),
    path('createattachment_create/<int:pk>/', views.memo_attachment_create_fromcreate, name='memo_attachment_create_fromcreate'),
    path('deleteattachment_create/<int:pk>/', views.memo_attachment_delete_fromcreate, name='memo_attachment_delete_fromcreate'),

    path('<int:pk>/', views.memo_detail, name='memo_detail'),      
    path('createattachment/<int:pk>/', views.memo_attachment_create, name='memo_attachment_create'),
    path('delete/<int:pk>/', views.memo_delete, name='memo_delete'),
    path('deleteattachment/<int:pk>/', views.memo_attachment_delete, name='memo_attachment_delete'),
    path('update/<int:pk>/', views.memo_update, name='memo_update'),
]