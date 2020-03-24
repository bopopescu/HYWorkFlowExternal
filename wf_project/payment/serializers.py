from rest_framework import serializers
from .models import PaymentRequest

class PYSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = ['revision', 'document_number', 'status','subject']