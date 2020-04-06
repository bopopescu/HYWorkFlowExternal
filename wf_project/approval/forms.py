from django import forms
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import UserMaintenance
from administration.models import EmployeeMaintenance

class ApprovalForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(queryset=DocumentTypeMaintenance.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.document_type)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.transaction_type)
    approval_level = forms.ModelChoiceField(queryset=WorkflowApprovalRule.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.approval_level)

    class Meta:
        model = ApprovalItem
        fields = ['document_number', 'notification','document_type','transaction_type','approval_level']

class ApproverForm(forms.ModelForm):
    class Meta:
        model = ApprovalItemApprover
        fields = ['user']

class CCForm(forms.ModelForm):
    class Meta:
        model = ApprovalItemCC
        fields = ['user']

class RejectForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea())
    hiddenValueReject = forms.IntegerField()

    class Meta:
        model = ApprovalItemApprover
        fields = ['id']