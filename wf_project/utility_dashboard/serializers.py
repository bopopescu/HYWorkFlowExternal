from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import UtilityApprovalItem, UtilityApprovalItemApprover, UtilityApprovalItemCC
from administration.models import EmployeeMaintenance, EmployeeGroupMaintenance
from administration.models import DocumentTypeMaintenance,UtiliyAccountTypeMaintenance,UtiliyGroupMaintenance
from memo.models import Memo
from django.utils.formats import number_format
from django.contrib.auth.models import User
from payment.models import PaymentRequest

class AccountSelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UtiliyGroupMaintenance
        fields = ['id','account_group_name']

class UtilityApprovalApproverSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    user_name = serializers.SerializerMethodField()
    user_group = serializers.SerializerMethodField()

    class Meta:
        model = UtilityApprovalItemApprover
        fields = ['id', 'stage', 'user', 'user_name', 'user_group', 'status', 'reason']

    def get_user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_user_group(self, obj):
        employee = get_object_or_404(EmployeeMaintenance, user=obj.user)
        employee_group = get_object_or_404(EmployeeGroupMaintenance, pk=employee.employee_group.pk)
        return employee_group.group_name

class UtilityApprovalCCSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = UtilityApprovalItemCC
        fields = ['id', 'user', 'user_email']

    def get_user_email(self, obj):
        employee = get_object_or_404(EmployeeMaintenance, user=obj.user)
        return employee.email

class UtilityApprovalItemSerializer(serializers.ModelSerializer):
    #document_amount =  serializers.SerializerMethodField()
    document_type = serializers.StringRelatedField(many=False)
    attachment_path = serializers.SerializerMethodField()
    request_by = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    submit_date = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = UtilityApprovalItem
        fields = ['id', 'attachment_path', 'document_number', 'document_pk', 'document_type', 'request_by', 'subject', 'submit_date','total_amount']

    def get_request_by(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            user = get_object_or_404(User, pk=py.submit_by.id)
            return user.username
        
    def get_attachment_path(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        return document_type.attachment_path

    def get_subject(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            return py.subject

    def get_submit_date(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            return py.submit_date
    
    def get_total_amount(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            return number_format(py.total_amount)