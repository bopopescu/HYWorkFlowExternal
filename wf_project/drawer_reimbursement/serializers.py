from rest_framework import serializers
from .models import ReimbursementRequest

class POSerializer(serializers.ModelSerializer):
    submit_by = serializers.StringRelatedField(many=False)
    drawer = serializers.StringRelatedField(many=False)
    submit_date = serializers.DateField(format='%d/%m/%Y')

    class Meta:
        model = ReimbursementRequest
        fields = ['id', 'document_number','drawer','description', 'request_amount'
        'submit_date','submit_by', 
        'approval', 'approval_status']

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