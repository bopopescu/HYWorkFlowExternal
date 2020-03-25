from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('memodata', views.MemoViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
    path('list/', views.memo_list, name='memo_list'),
    path('create/', views.memo_create, name='memo_create'),
    path('<int:pk>/', views.memo_detail, name='memo_detail'),    
    path('delete/<int:pk>/', views.memo_delete, name='memo_delete'),
    path('update/<int:pk>/', views.memo_update, name='memo_update'),
]