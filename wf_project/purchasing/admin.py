from django.contrib import admin
from .models import GoodsReceiptNote
from .models import PurchaseOrder, PurchaseOrderDetail, PurchaseOrderAddress, PurchaseOrderCC
from .models import PurchaseQuotation
from .models import PurchaseRequest, PurchaseRequestDetail, PurchaseRequestAddress, PurchaseRequestCC
from .models import RequestForQuotation

admin.site.register(GoodsReceiptNote)

class POAddressInline(admin.StackedInline):
    model = PurchaseOrderAddress
    extra = 1

class POCCInline(admin.StackedInline):
    model = PurchaseOrderCC
    extra = 1

class PODetailInline(admin.StackedInline):
    model = PurchaseOrderDetail
    extra = 1

class POAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['vendor', 'company','project', 'subject', 'reference']}),
        ('Document Information', {'fields': ['revision','document_number','status','submit_date']}),
        ('Summary', {'fields': ['sub_total','discount','tax_amount','total_amount', 'payment_term','payment_schedule']}),
        ('Remarks', {'fields': ['remarks']}),
        ('Attachments', {'fields': ['attachment','attachment_date']}),
    ]
    inlines = [PODetailInline, POAddressInline, POCCInline]

admin.site.register(PurchaseOrder, POAdmin)
admin.site.register(PurchaseQuotation)

class PRAddressInline(admin.StackedInline):
    model = PurchaseRequestAddress
    extra = 1

class PRCCInline(admin.StackedInline):
    model = PurchaseRequestCC
    extra = 1

class PRDetailInline(admin.StackedInline):
    model = PurchaseRequestDetail
    extra = 1

class PRAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['is_interdepartmental','company', 'department', 'project', 'subject', 'reference']}),
        ('Document Information', {'fields': ['revision','document_number','status','submit_date']}),
        ('Summary', {'fields': ['sub_total']}),
        ('Remarks', {'fields': ['remarks']}),
        ('Attachments', {'fields': ['attachment','attachment_date']}),
    ]
    inlines = [PRDetailInline, PRAddressInline, PRCCInline]

admin.site.register(PurchaseRequest, PRAdmin)
admin.site.register(RequestForQuotation)