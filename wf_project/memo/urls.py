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

    path('create/', views.memo_init, name='memo_init'),
    path('create/<int:pk>/', views.memo_create, name='memo_create'),
    path('createattachment/<int:pk>/', views.memo_attachment_create, name='memo_attachment_create'),
    path('deleteattachment/', views.memo_attachment_delete, name='memo_attachment_delete'),

    path('<int:pk>/', views.memo_detail, name='memo_detail'),      
    path('delete/', views.memo_delete, name='memo_delete'),
    path('update/<int:pk>/', views.memo_update, name='memo_update'),

    path('ajax/load-template/', views.load_template, name='ajax_load_template'),
    
]