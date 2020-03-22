from django.contrib import admin
from .models import Item

#class PODetailInline(admin.StackedInline):
#    model = PurchaseOrderDetail
#    extra = 1

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['item_type', 'item_class','item_group', 'Item_description', 'is_active']}),
        ('Quantity', {'fields': ['minimum_quantity','minimum_order_quantity','standard_packing_quantity','leadtime']}),
        ('Other Information', {'fields': ['origin','specification','hs_code','submit_date','remarks']}),
    ]
    #inlines = [PODetailInline, POAddressInline, POCCInline]

admin.site.register(Item, ItemAdmin)