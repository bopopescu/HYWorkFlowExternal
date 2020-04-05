from django.contrib import admin
from .models import AssetMaster, ClassType, AssetCategory, Tax, AssetType

# Register your models here.
admin.site.register(AssetMaster)
admin.site.register(AssetCategory)
admin.site.register(Tax)
admin.site.register(ClassType)
admin.site.register(AssetType)