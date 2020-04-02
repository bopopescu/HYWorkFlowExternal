from rest_framework import serializers
from .models import Memo, MemoAttachment

class MemoSerializer(serializers.ModelSerializer):
    submit_by = serializers.StringRelatedField(many=False)
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    approval_status = serializers.SerializerMethodField()

    class Meta:
        model = Memo
        fields = ['id', 'revision', 'document_number', 'subject', 
        'submit_date', 'company', 'project', 'submit_by', 
        'approval','approval_status']
    
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

class MemoAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()
    class Meta:
        model = MemoAttachment
        fields = ['id', 'memo', 'attachment', 'attachment_date']