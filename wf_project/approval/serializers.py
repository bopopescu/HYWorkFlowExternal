from rest_framework import serializers
from .models import ApprovalItemApprover, ApprovalItemCC

class ApprovalApproverSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = ApprovalItemApprover
        fields = ['stage','user']

class ApprovalCCSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = ApprovalItemCC
        fields = ['user']