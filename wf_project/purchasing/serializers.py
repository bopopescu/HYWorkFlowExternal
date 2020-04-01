from rest_framework import serializers
from .models import PurchaseOrder, PurchaseOrderDetail, PurchaseOrderAttachment, PurchaseOrderComparison2Attachment, PurchaseOrderComparison3Attachment

class POSerializer(serializers.ModelSerializer):
    submit_by = serializers.StringRelatedField(many=False)
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    approval_status = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'revision', 'document_number', 'subject', 
        'submit_date', 'company', 'project', 'submit_by', 
        'approval', 'approval_status']

    def get_approval_status(self, obj):     
        if obj.approval.status == "D":
            return "Draft"
        elif obj.approval.status == "IP":
            return "In Progress"
        elif obj.approval.status == "A":
            return "Approved"
        else:
            return "Rejected"

class PODetailSerializer(serializers.ModelSerializer):
    item_code =  serializers.SerializerMethodField()
    item_description = serializers.SerializerMethodField()
    uom = serializers.StringRelatedField(many=False)

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id', 'item_code', 'item_description',
        'additional_description', 'po','quantity', 'uom',
        'unit_price','amount','remarks']

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