from django.contrib import admin
from .models import Item

#class PODetailInline(admin.StackedInline):
#    model = PurchaseOrderDetail
#    extra = 1

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'item_class','item_description','is_active')
    list_filter = ('is_active',)
    search_fields = ('item_type', 'item_class','item_description')
    fieldsets = [
        (None, {'fields': ['item_type', 'item_class','item_group', 'item_description','item_uom', 'is_active']}),
        ('Quantity', {'fields': ['minimum_quantity','minimum_order_quantity','standard_packing_quantity','leadtime']}),
        ('Other Information', {'fields': ['origin','specification','hs_code','remarks']}),
    ]
    exclude = ['created_by','modified_by']
    #inlines = [PODetailInline, POAddressInline, POCCInline]
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(Item, ItemAdmin)