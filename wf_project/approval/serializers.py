from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from administration.models import EmployeeMaintenance, EmployeeGroupMaintenance
from administration.models import DocumentTypeMaintenance
from memo.models import Memo
from django.contrib.auth.models import User
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest

class ApprovalApproverSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    user_name = serializers.SerializerMethodField()
    user_group =  serializers.SerializerMethodField()

    class Meta:
        model = ApprovalItemApprover
        fields = ['id','stage','user', 'user_name', 'user_group', 'status', 'reason']

    def get_user_name(self, obj):        
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_user_group(self, obj):    
        employee = get_object_or_404(EmployeeMaintenance, nick_name=obj.user.username)
        employee_group = get_object_or_404(EmployeeGroupMaintenance, pk=employee.employee_group.pk)
        return employee_group.group_name

class ApprovalCCSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = ApprovalItemCC
        fields = ['id','user','user_email']

    def get_user_email(self, obj):        
        return obj.user.email

class ApprovalItemSerializer(serializers.ModelSerializer):    
    #document_amount =  serializers.SerializerMethodField()
    document_type = serializers.StringRelatedField(many=False)
    request_by = serializers.SerializerMethodField()
    subject =  serializers.SerializerMethodField()
    submit_date =  serializers.SerializerMethodField()

    class Meta:
        model = ApprovalItem
        fields = ['id','document_number','document_pk','document_type','request_by','subject','submit_date']

    def get_request_by(self, obj):  
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_name == "Memo":
            memo = get_object_or_404(Memo, pk=obj.document_pk)
            user = get_object_or_404(User, pk=memo.submit_by.id)
            return user.username
        elif document_type.document_type_name == "Payment Request":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            user = get_object_or_404(User, pk=py.submit_by.id)
            return user.username
        elif document_type.document_type_name == "Staff Recruitment Request":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=obj.document_pk)
            user = get_object_or_404(User, pk=staff.submit_by.id)
            return user.username

    def get_subject(self, obj):  
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_name == "Memo":
            memo = get_object_or_404(Memo, pk=obj.document_pk)
            return memo.subject
        if document_type.document_type_name == "Payment Request":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            return py.subject
        if document_type.document_type_name == "Staff Recruitment Request":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=obj.document_pk)
            return '{0}: {1}'.format("Staff Recruiment Request for Position",staff.position_title)

    def get_submit_date(self, obj):  
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_name == "Memo":
            memo = get_object_or_404(Memo, pk=obj.document_pk)
            return memo.submit_date
        if document_type.document_type_name == "Payment Request":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            return py.submit_date
        if document_type.document_type_name == "Staff Recruitment Request":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=obj.document_pk)
            return staff.request_date