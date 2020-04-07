from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('myassetdata', views.MyAssetViewSet, basename='myasset')

urlpatterns = [
    path('api/', include(router.urls)),
    path('list/', views.fixed_asset_list, name='fixed_asset_list'),
    path('create/', views.fixed_asset_create, name='fixed_asset_create'),
    path('update/<int:pk>/', views.fixed_asset_update, name='fixed_asset_update'),
    path('<int:pk>/', views.fixed_asset_detail, name='fixed_asset_detail'),
    path('delete/', views.fixed_asset_delete, name='fixed_asset_delete'),
]