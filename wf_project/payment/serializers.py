from rest_framework import serializers
from .models import PaymentRequest
from .models import PaymentRequestDetail
from .models import PaymentAttachment

class PYSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)

    class Meta:
        model = PaymentRequest
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project']

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