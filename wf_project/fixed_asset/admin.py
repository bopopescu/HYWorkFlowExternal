from django.contrib import admin
from .models import AssetMaster, ClassType, AssetCategory, Tax, AssetType

# Register your models here.
class AssetCategoryScreen(admin.ModelAdmin):
    list_display = ('category_type', 'description', 'status', 'created_date', 'modify_date')
    search_fields = ('description', 'status', 'is_deleted')
    fieldsets = [
        (None, {'fields': ['category_type','description', 'status', 'is_deleted']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(AssetCategory, AssetCategoryScreen)

class AssetMasterScreen(admin.ModelAdmin):
    list_display = ('asset_number', 'company', 'description', 'asset_type_id', 'asset_category_id', 'is_deleted')
    search_fields = ('company', 'description', 'asset_type_id', 'asset_category_id')
    fieldsets = [
        (None, {'fields': ['asset_number','description','asset_type_id','asset_category_id',
            'tax_id','class_type_id','floor_plan_ref','trustees',
            'cost_value','net_book_value','proceeds_on_disposal','historical_cost',
            'active_lifetime','active_res_value','tax_cost','current_tax_percentage', 'is_deleted']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(AssetMaster, AssetMasterScreen)

class AssetTypeScreen(admin.ModelAdmin):
    list_display = ('asset_type', 'description', 'status', 'created_date', 'modify_date')
    search_fields = ('description', 'status', 'is_deleted')
    fieldsets = [
        (None, {'fields': ['asset_type','description', 'status', 'is_deleted']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(AssetType, AssetTypeScreen)

class ClassTypeScreen(admin.ModelAdmin):
    list_display = ('class_type', 'description', 'status', 'created_date', 'modify_date')
    search_fields = ('description', 'status', 'is_deleted')
    fieldsets = [
        (None, {'fields': ['class_type','description', 'status', 'is_deleted']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(ClassType, ClassTypeScreen)

class TaxScreen(admin.ModelAdmin):
    list_display = ('tax_code', 'description', 'status', 'created_date', 'modify_date')
    search_fields = ('description', 'status', 'is_deleted')
    fieldsets = [
        (None, {'fields': ['tax_code','description', 'status', 'is_deleted']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(Tax, TaxScreen)

