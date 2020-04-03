from rest_framework import serializers
from .models import PaymentRequest
from .models import PaymentRequestDetail
from .models import PaymentAttachment

class PYSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    approval = serializers.StringRelatedField(many=False)
    submit_by = serializers.StringRelatedField(many=False)
    approval_status = serializers.SerializerMethodField()
    approval_id = serializers.SerializerMethodField()

    class Meta:
        model = PaymentRequest
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project','submit_by', 'approval','approval_status','approval_id']
    
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
            return "Draft"

    def get_approval_id(self, obj):  
        if obj.approval is None:
            return ""
        else:       
            return obj.approval.id

class PYItemSerializer(serializers.ModelSerializer):
    tax = serializers.StringRelatedField(many=False)
    class Meta:
        model = PaymentRequestDetail
        fields = ['id', 'py', 'item_description', 'price','tax','line_total']

class PYAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()
    class Meta:
        model = PaymentAttachment
        fields = ['id', 'py', 'attachment', 'attachment_date']