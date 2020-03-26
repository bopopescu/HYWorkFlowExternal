from rest_framework import serializers
from .models import PaymentRequest

class PYSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)

    class Meta:
        model = PaymentRequest
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project']