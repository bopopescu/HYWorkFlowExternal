from rest_framework import serializers
from django.shortcuts import get_object_or_404
from accounts_task.models import AccountTask
from django.utils.formats import number_format
from administration.models import StatusMaintenance
from .models import PaymentRequest
from .models import PaymentRequestDetail
from .models import PaymentAttachment

class PYSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    utility_account_approval = serializers.StringRelatedField(many=False)
    approval = serializers.StringRelatedField(many=False)
    submit_by = serializers.StringRelatedField(many=False)
    approval_status = serializers.SerializerMethodField()
    approval_id = serializers.SerializerMethodField()
    # accounts_status = serializers.SerializerMethodField()

    class Meta:
        model = PaymentRequest
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project', 'submit_by', 'approval', 'approval_status', 'approval_id', 'utility_account_approval']
    
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
        elif obj.utility_account_approval != None:
            if obj.utility_account_approval.status == "D":
                return "Draft"
            elif obj.utility_account_approval.status == "IP":
                return "In Progress"
            elif obj.utility_account_approval.status == "A":
                return "Approved"
            else:
                return "Rejected"
        else:
            if obj.status != None:
                status = StatusMaintenance.objects.filter(pk=obj.status.pk)
                if status.count() > 0:
                    if status[0].status_code == 999:
                        return "Cancel"
                    else:
                        return "Draft(New)"
                else:
                    return "Draft(New)"
            else:
                return "Draft(New)"

    def get_approval_id(self, obj):  
        if obj.approval != None:
            return obj.approval.id
        elif obj.utility_account_approval != None:
            return obj.utility_account_approval.id
        else:       
            ""
    
    # def get_accounts_status(self, obj):
    #     task_exist = AccountTask.objects.filter(approval_item=obj.approval).count()

    #     if task_exist > 0:
    #         account_task = get_object_or_404(AccountTask, approval_item=obj.approval)

    #         if account_task.process:
    #             if account_task.completed:
    #                 return "Completed"
    #             else:
    #                 return "In Process"
    #         else:
    #             return "Pending Process"
    #     else:
    #         return "Not Applicable"

class PYItemSerializer(serializers.ModelSerializer):
    tax = serializers.StringRelatedField(many=False)
    line_total = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = PaymentRequestDetail
        fields = ['id', 'py', 'item_description', 'price', 'tax', 'line_total', 'linenum']

    def get_line_total(self, obj):
        return number_format(obj.line_total)

    def get_price(self, obj):
        return number_format(obj.price)


class PYAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()
    class Meta:
        model = PaymentAttachment
        fields = ['id', 'py', 'attachment', 'attachment_date']