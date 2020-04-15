from rest_framework import serializers
from .models import StaffOT
from .models import StaffOTDetail

class StaffOTSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    approval = serializers.StringRelatedField(many=False)
    submit_by = serializers.StringRelatedField(many=False)
    approval_status = serializers.SerializerMethodField()
    approval_id = serializers.SerializerMethodField()

    class Meta:
        model = StaffOT
        fields = ['id', 'revision', 'document_number', 'submit_date', 'company', 'project','submit_by', 'approval','approval_status','approval_id']
    
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
            return "Draft(New)"

    def get_approval_id(self, obj):  
        if obj.approval is None:
            return ""
        else:       
            return obj.approval.id

class StaffOTDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StaffOTDetail
        fields = ['id', 'staff_ot', 'ot_date', 'ot_time_in','ot_time_out','total_ot_time','meal_allowance','is_holiday','remark','ot_rate_per_hours','total_ot_rate']

