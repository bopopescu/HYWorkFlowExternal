"""wf_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard.views import IndexView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),         
    path('admin/', admin.site.urls, name='admin'), 
    path('approval/', include('approval.urls')),   
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('memo/', include('memo.urls')),
    path('payment/', include('payment.urls')),
    path('purchasing/', include('purchasing.urls')),
    path('staffrecruitment/', include('human_resource.urls')),
    path('report_builder/', include('report_builder.urls')),
    path('drawer_disbursement/', include('drawer_disbursement.urls')),
    path('fixed_asset/', include('fixed_asset.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)