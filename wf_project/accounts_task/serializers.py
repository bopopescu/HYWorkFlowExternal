from rest_framework import serializers
from django.shortcuts import get_object_or_404
from administration.models import EmployeeMaintenance, EmployeeGroupMaintenance
from administration.models import DocumentTypeMaintenance
from approval.models import ApprovalItem
from memo.models import Memo
from django.contrib.auth.models import User
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest
from purchasing.models import PurchaseOrder
from staff_overtime.models import StaffOT
from drawer_reimbursement.models import ReimbursementRequest
from .models import AccountTask

class TaskSerializer(serializers.ModelSerializer):
    approval_item = serializers.StringRelatedField(many=False)
    attachment_path = serializers.SerializerMethodField()
    request_by = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    document_pk = serializers.SerializerMethodField()
    document_type = serializers.SerializerMethodField()
    approval_code = serializers.SerializerMethodField()
    approval_id = serializers.SerializerMethodField()

    class Meta:
        model = AccountTask
        fields = ['id',
            'approval_item',
            'approval_id',
            'process',
            'process_date',
            'process_by',
            'completed',
            'completed_date',
            'completed_by',
            'attachment_path',
            'document_pk',
            'document_type',
            'request_by',
            'subject',
            'approval_code']

    def get_request_by(self, obj):
        approval_item = get_object_or_404(ApprovalItem, pk=obj.approval_item.pk)
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
        if document_type.document_type_code == "601":
            memo = get_object_or_404(Memo, pk=approval_item.document_pk)
            user = get_object_or_404(User, pk=memo.submit_by.id)
            return user.username
        elif document_type.document_type_code == "205":
            po = get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
            user = get_object_or_404(User, pk=po.submit_by.id)
            return user.username
        elif document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
            user = get_object_or_404(User, pk=py.submit_by.id)
            return user.username
        elif document_type.document_type_code == "501":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
            user = get_object_or_404(User, pk=staff.submit_by.id)
            return user.username
        elif document_type.document_type_code == "504":
            staff_ot = get_object_or_404(StaffOT, pk=approval_item.document_pk)
            user = get_object_or_404(User, pk=staff_ot.submit_by.id)
            return user.username
        elif document_type.document_type_code == "403":
            reimbursed_request = get_object_or_404(ReimbursementRequest, pk=approval_item.document_pk)
            user = get_object_or_404(User, pk=reimbursed_request.submit_by.id)
            return user.username

    def get_subject(self, obj):
        approval_item = get_object_or_404(ApprovalItem, pk=obj.approval_item.pk)
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
        if document_type.document_type_code == "601":
            memo = get_object_or_404(Memo, pk=approval_item.document_pk)
            return memo.subject
        elif document_type.document_type_code == "205":
            po = get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
            return po.subject
        elif document_type.document_type_code == "301":
            py = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
            return py.subject
        elif document_type.document_type_code == "501":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
            return '{0}: {1}'.format("Staff Recruiment Request for Position", staff.position_title)
        elif document_type.document_type_code == "504":
            staff_ot = get_object_or_404(StaffOT, pk=approval_item.document_pk)
            return '{0}: {1}'.format("Staff Overtime -", staff_ot.transaction_type)
        elif document_type.document_type_code == "403":
            reimbursed_request = get_object_or_404(ReimbursementRequest, pk=approval_item.document_pk)
            return reimbursed_request.description
       
    def get_attachment_path(self, obj):
        approval_item = get_object_or_404(ApprovalItem, pk=obj.approval_item.pk)        
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
        return document_type.attachment_path

    def get_document_pk(self, obj):
        return obj.approval_item.document_pk

    def get_document_type(self, obj):
        approval_item = get_object_or_404(ApprovalItem, pk=obj.approval_item.pk)
        document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
        return document_type.document_type_name

    def get_approval_code(self, obj):
        approval_item = get_object_or_404(ApprovalItem, pk=obj.approval_item.pk)
        return approval_item.approval_code

    def get_approval_id(self, obj):
        approval_item = get_object_or_404(ApprovalItem, pk=obj.approval_item.pk)
        return approval_item.id
