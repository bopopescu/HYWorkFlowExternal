from rest_framework import serializers
from .models import ReimbursementRequest,DrawerReimbursement
from administration.models import DrawerMaintenance

class ReimbursementRequestSerializer(serializers.ModelSerializer):
    submit_by = serializers.StringRelatedField(many=False)
    drawer = serializers.StringRelatedField(many=False)
    submit_date = serializers.DateField(format='%d/%m/%Y')
    approval_status = serializers.SerializerMethodField()
    approval_id = serializers.SerializerMethodField()

    class Meta:
        model = ReimbursementRequest
        fields = ['id', 'document_number','drawer','description', 'request_amount',
        'submit_date','submit_by', 
        'approval', 'approval_status','approval_id']

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
            return "Draft (New)"

    def get_approval_id(self, obj):  
        if obj.approval is None:
            return ""
        else:       
            return obj.approval.id

class DrawerReimbursedSerializer(serializers.ModelSerializer):
    reimbursed_date = serializers.DateField(format='%d/%m/%Y')
    reimbursement_request = serializers.StringRelatedField(many=False)

    class Meta:
        model = DrawerReimbursement
        fields = ['id','reimbursed_by','status','total_reimburse','reimbursement_request','reimbursed_date']

class DrawerSelectionSerializer(serializers.ModelSerializer):
    branch = serializers.StringRelatedField(many=False)

    class Meta:
        model = DrawerMaintenance
        fields = ['id','drawer_name','branch','open_year','open_month','limit','drawer_status']

class ApprovedReimburserdRequest(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    approval = serializers.StringRelatedField(many=False)
    submit_by = serializers.StringRelatedField(many=False)

    class Meta:
        model = ReimbursementRequest
        fields = ['id', 'document_number', 'description', 'submit_date','submit_by','request_amount','approval']