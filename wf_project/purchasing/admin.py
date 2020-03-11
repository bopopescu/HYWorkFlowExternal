from django.contrib import admin
from .models import GoodsReceiptNote
from .models import PurchaseOrder
from .models import PurchaseQuotation
from .models import PurchaseRequest
from .models import RequestForQuotation

admin.site.register(GoodsReceiptNote)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseQuotation)
admin.site.register(PurchaseRequest)
admin.site.register(RequestForQuotation)