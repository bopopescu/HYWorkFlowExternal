from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from administration.models import EmployeeMaintenance, EmployeeGroupMaintenance
from administration.models import DocumentTypeMaintenance
from memo.models import Memo
from django.contrib.auth.models import User
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest
from payment.models import PaymentRequest
from purchasing.models import PurchaseOrder
from staff_overtime.models import StaffOT
from drawer_reimbursement.models import ReimbursementRequest

class ApprovalApproverSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    user_name = serializers.SerializerMethodField()
    user_group = serializers.SerializerMethodField()
    approved_date = serializers.SerializerMethodField()
    class Meta:
        model = ApprovalItemApprover
        fields = ['id', 'stage', 'user', 'user_name', 'user_group', 'status', 'reason','approved_date']

    def get_user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_user_group(self, obj):
        employee = get_object_or_404(EmployeeMaintenance, user=obj.user)
        employee_group = get_object_or_404(EmployeeGroupMaintenance, pk=employee.employee_group.pk)
        return employee_group.group_name
    
    def get_approved_date(self,obj):
        if obj.approved_date == None:
            return ""
        else:
            return obj.approved_date

class ApprovalCCSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = ApprovalItemCC
        fields = ['id', 'user', 'user_email']

    def get_user_email(self, obj):
        employee = get_object_or_404(EmployeeMaintenance, user=obj.user)
        return employee.email

class ApprovalItemSerializer(serializers.ModelSerializer):
    #document_amount =  serializers.SerializerMethodField()
    document_type = serializers.SerializerMethodField()
    attachment_path = serializers.SerializerMethodField()
    request_by = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    submit_date = serializers.SerializerMethodField()
    row_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = ApprovalItem
        fields = ['row_number', 'id', 'attachment_path', 'document_number', 'document_pk', 'document_type', 'request_by', 'subject', 'submit_date']

    def get_document_type(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "301":
            py = PaymentRequest.objects.filter(pk=obj.document_pk)[0]
            return obj.document_type.document_type_name +"-"+ py.transaction_type.transaction_type_name
        else:
            return obj.document_type.document_type_name

    def get_request_by(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "601":
            memo = get_object_or_404(Memo, pk=obj.document_pk)
            user = get_object_or_404(User, pk=memo.submit_by.id)
            return user.username
        elif document_type.document_type_code == "205":
            po = get_object_or_404(PurchaseOrder, pk=obj.document_pk)
            user = get_object_or_404(User, pk=po.submit_by.id)
            return user.username
        elif document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            user = get_object_or_404(User, pk=py.submit_by.id)
            return user.username
        elif document_type.document_type_code == "501":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=obj.document_pk)
            user = get_object_or_404(User, pk=staff.submit_by.id)
            return user.username
        elif document_type.document_type_code == "504":
            staff_ot = get_object_or_404(StaffOT, pk=obj.document_pk)
            user = get_object_or_404(User, pk=staff_ot.submit_by.id)
            return user.username
        elif document_type.document_type_code == "403":
            reimbursed_request = get_object_or_404(ReimbursementRequest, pk=obj.document_pk)
            user = get_object_or_404(User, pk=reimbursed_request.submit_by.id)
            return user.username

    def get_attachment_path(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        return document_type.attachment_path

    def get_subject(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "601":
            memo = get_object_or_404(Memo, pk=obj.document_pk)
            return memo.subject
        elif document_type.document_type_code == "205":
            po = get_object_or_404(PurchaseOrder, pk=obj.document_pk)
            return po.subject
        elif document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            return py.subject
        elif document_type.document_type_code == "501":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=obj.document_pk)
            return '{0}: {1}'.format("Staff Recruiment Request for Position", staff.position_title)
        elif document_type.document_type_code == "504":
            staff_ot = get_object_or_404(StaffOT, pk=obj.document_pk)
            return '{0}: {1}'.format("Staff Overtime -", staff_ot.transaction_type)
        elif document_type.document_type_code == "403":
            reimbursed_request = get_object_or_404(ReimbursementRequest, pk=obj.document_pk)
            return reimbursed_request.description
        

    def get_submit_date(self, obj):
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=obj.document_type.pk)
        if document_type.document_type_code == "601":
            memo = get_object_or_404(Memo, pk=obj.document_pk)
            return memo.submit_date
        elif document_type.document_type_code == "205":
            po = get_object_or_404(PurchaseOrder, pk=obj.document_pk)
            return po.submit_date
        elif document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=obj.document_pk)
            return py.submit_date
        elif document_type.document_type_code == "501":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=obj.document_pk)
            return staff.request_date
        elif document_type.document_type_code == "504":
            staff_ot = get_object_or_404(StaffOT, pk=obj.document_pk)
            return staff_ot.submit_date
        elif document_type.document_type_code == "403":
            reimbursed_request = get_object_or_404(ReimbursementRequest, pk=obj.document_pk)
            return reimbursed_request.submit_date