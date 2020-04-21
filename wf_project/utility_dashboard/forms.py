from django.shortcuts import get_object_or_404
from django import forms
from .models import UtilityApprovalItem, UtilityApprovalItemApprover, UtilityApprovalItemCC
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import EmployeeMaintenance, EmployeePositionMaintenance
from django.contrib.auth.models import User, Group

class UtilityApprovalForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(queryset=DocumentTypeMaintenance.objects.all(), label="Doc. Type", empty_label="Not Assigned", initial=UtilityApprovalItem.document_type)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), label="Trans. Type", empty_label="Not Assigned", initial=UtilityApprovalItem.transaction_type)
    approval_level = forms.ModelChoiceField(queryset=WorkflowApprovalRule.objects.all(), empty_label="Not Assigned", initial=UtilityApprovalItem.approval_level)

    class Meta:
        model = UtilityApprovalItem
        fields = ['document_number', 'notification', 'document_type', 'transaction_type', 'approval_level']

class UtilityApproverModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}: {} {}".format(obj.username, obj.first_name, obj.last_name)        

class UtilityApproverGroupAForm(forms.ModelForm):
    user = UtilityApproverModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=UtilityApprovalItem.document_type)

    class Meta:
        model = UtilityApprovalItemApprover
        fields = []

    def __init__(self, *args, **kwargs):
        super(UtilityApproverGroupAForm, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name='Group A').values_list('id', flat=True)
        users = User.objects.filter(groups__in=groups).order_by('username')
        self.fields['user'].queryset = users
        
class UtilityApproverGroupBForm(forms.ModelForm):
    user = UtilityApproverModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=UtilityApprovalItem.document_type)

    class Meta:
        model = UtilityApprovalItemApprover
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(UtilityApproverGroupBForm, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name='Group B').values_list('id', flat=True)
        self.fields['user'].queryset = User.objects.filter(groups__in=groups).order_by('username')

class UtilityCCForm(forms.ModelForm):
    user = UtilityApproverModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=UtilityApprovalItem.document_type)

    class Meta:
        model = UtilityApprovalItemCC
        fields = []

    def __init__(self, *args, **kwargs):
        super(UtilityCCForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all().order_by('username')

class UtilityRejectForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea())
    hiddenValueReject = forms.IntegerField()

    class Meta:
        model = UtilityApprovalItemApprover
        fields = ['id']
