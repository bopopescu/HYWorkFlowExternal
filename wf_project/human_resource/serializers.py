from rest_framework import serializers
from .models import StaffRecruitmentRequest,StaffJobRequirement,StaffJobResponsibilities

class StaffRecruitmentSerializer(serializers.ModelSerializer):
    request_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)
    approval = serializers.StringRelatedField(many=False)
    submit_by = serializers.StringRelatedField(many=False)
    approval_status = serializers.SerializerMethodField()
    approval_id = serializers.SerializerMethodField()

    class Meta:
        model = StaffRecruitmentRequest
        fields = ['id', 'revision', 'document_number', 'request_date', 'company', 'department','approval','submit_by','approval_status','approval_id']

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

class StaffJobRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffJobRequirement
        fields = ['id','staff_recruitment','requirement_description']

class StaffJobResponsibilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffJobResponsibilities
        fields = ['id','staff_recruitment' ,'responsible_description']