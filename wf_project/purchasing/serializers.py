from rest_framework import serializers
from .models import PurchaseOrder, PurchaseOrderDetail, PurchaseOrderAttachment
from .models import PurchaseOrderComparison2Attachment, PurchaseOrderComparison3Attachment
from .models import GoodsReceiptNote, PurchaseInvoice, PurchaseDebitNote, PurchaseCreditNote

class POSerializer(serializers.ModelSerializer):
    submit_by = serializers.StringRelatedField(many=False)
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    approval_status = serializers.SerializerMethodField()
    grn = serializers.SerializerMethodField()
    receive_date = serializers.SerializerMethodField()
    grn_doc_no = serializers.SerializerMethodField()
    inv = serializers.SerializerMethodField()
    inv_date = serializers.SerializerMethodField()
    inv_doc_no = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'revision', 'document_number', 'subject', 
        'submit_date', 'company', 'project', 'submit_by', 
        'approval', 'approval_status', 'grn', 'receive_date', 'grn_doc_no',
        'inv', 'inv_date', 'inv_doc_no']

    def get_approval_status(self, obj):    
        if obj.approval != None:  
            if obj.approval.status == "D":
                return "Draft"
            elif obj.approval.status == "IP":
                return "In Progress"
            elif obj.approval.status == "A":
                return "Approved"
            else:
                return "Rejected"
        else:
            return "Draft (New)"

    def get_grn(self, obj):
        grn_exist = GoodsReceiptNote.objects.filter(po=obj).count()

        if grn_exist > 0:
            grn = GoodsReceiptNote.objects.filter(po=obj)[0]
            return grn.id
        else:
            return 0

    def get_receive_date(self, obj):
        grn_exist = GoodsReceiptNote.objects.filter(po=obj).count()

        if grn_exist > 0:
            grn = GoodsReceiptNote.objects.filter(po=obj)[0]
            return grn.receive_date
        else:
            return 0

    def get_grn_doc_no(self, obj):
        grn_exist = GoodsReceiptNote.objects.filter(po=obj).count()

        if grn_exist > 0:
            grn = GoodsReceiptNote.objects.filter(po=obj)[0]
            return grn.document_number
        else:
            return 0

    def get_inv(self, obj):
        inv_exist = PurchaseInvoice.objects.filter(po=obj).count()

        if inv_exist > 0:
            inv = PurchaseInvoice.objects.filter(po=obj)[0]
            return inv.id
        else:
            return 0

    def get_inv_date(self, obj):
        inv_exist = PurchaseInvoice.objects.filter(po=obj).count()

        if inv_exist > 0:
            inv = PurchaseInvoice.objects.filter(po=obj)[0]
            return inv.invoice_date
        else:
            return 0

    def get_inv_doc_no(self, obj):
        inv_exist = PurchaseInvoice.objects.filter(po=obj).count()

        if inv_exist > 0:
            inv = PurchaseInvoice.objects.filter(po=obj)[0]
            return inv.invoice_number
        else:
            return 0

class PODetailSerializer(serializers.ModelSerializer):
    item_code =  serializers.SerializerMethodField()
    item_description = serializers.SerializerMethodField()
    uom = serializers.StringRelatedField(many=False)

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id', 'item_code', 'item_description',
        'additional_description', 'po', 'quantity', 'uom',
        'unit_price', 'amount', 'line_taxamount', 'line_total', 'remarks', ]

    def get_item_code(self, obj):                
        return obj.item.item_code

    def get_item_description(self, obj):    
        return obj.item.item_description

class POAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()
    class Meta:
        model = PurchaseOrderAttachment
        fields = ['id', 'po', 'attachment', 'attachment_date']

class POComparison2AttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()
    class Meta:
        model = PurchaseOrderComparison2Attachment
        fields = ['id', 'po', 'attachment', 'attachment_date']

class POComparison3AttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()
    class Meta:
        model = PurchaseOrderComparison2Attachment
        fields = ['id', 'po', 'attachment', 'attachment_date']