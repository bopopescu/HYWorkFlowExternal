from rest_framework import serializers
from .models import PurchaseOrder

class POSerializer(serializers.ModelSerializer):
    submit_by = serializers.StringRelatedField(many=False)
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    approval = serializers.StringRelatedField(many=False)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project', 'submit_by', 'approval']
