"""URL logic to control Memo module"""

from django.urls import path, include
from rest_framework import routers
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register('mymemodata', views.MyMemoViewSet, basename='mymemo')
ROUTER.register('teammemodata', views.TeamMemoViewSet, basename='teammemo')
ROUTER.register('memoattachment', views.MemoAttachmentViewSet, basename='memoattachment')

urlpatterns = [
    path('api/', include(ROUTER.urls)),
    path('', views.memo_index, name='memo_index'),
    path('list/', views.memo_list, name='memo_list'),

    path('create/', views.memo_init, name='memo_init'),
    path('create/<int:pk_value>/', views.memo_create, name='memo_create'),
    path('createattachment/<int:pk_value>/', views.memo_attachment_create, name='memo_attachment_create'),
    path('deleteattachment/', views.memo_attachment_delete, name='memo_attachment_delete'),

    path('<int:pk_value>/', views.memo_detail, name='memo_detail'),
    path('delete/', views.memo_delete, name='memo_delete'),
    path('update/<int:pk_value>/', views.memo_update, name='memo_update'),
    path('send_approval/<int:pk>/',views.memo_send_approval,name='memo_send_approval'),

    path('ajax/load-template/', views.load_template, name='ajax_load_template'),
    path('print/<int:pk>/', views.memo_print, name='memo_print'),
]
