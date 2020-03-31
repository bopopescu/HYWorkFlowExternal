from rest_framework import serializers
from .models import StaffRecruitmentRequest,StaffJobRequirement,StaffJobResponsibilities

class StaffRecruitmentSerializer(serializers.ModelSerializer):
    request_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)
    approval = serializers.StringRelatedField(many=False)
    submit_by = serializers.StringRelatedField(many=False)

    class Meta:
        model = StaffRecruitmentRequest
        fields = ['id', 'revision', 'document_number', 'request_date', 'company', 'department','approval','submit_by']

class StaffJobRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffJobRequirement
        fields = ['id','staff_recruitment','requirement_description']

class StaffJobResponsibilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffJobResponsibilities
        fields = ['id','staff_recruitment' ,'responsible_description']