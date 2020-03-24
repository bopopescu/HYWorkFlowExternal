from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('memodata', views.MemoViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
    path('memo/list/', views.memo_list, name='memo_list'),
    path('memo/create/', views.memo_create, name='memo_create'),
]