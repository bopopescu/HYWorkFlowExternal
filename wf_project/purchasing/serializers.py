from rest_framework import serializers
from .models import PurchaseOrder

class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['revision', 'document_number', 'status','subject']