from rest_framework import serializers
from .models import StaffRecruitmentRequest

class StaffRecruitmentSerializer(serializers.ModelSerializer):
    request_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)

    class Meta:
        model = StaffRecruitmentRequest
        fields = ['id', 'revision', 'document_number', 'subject', 'request_date', 'company', 'department']