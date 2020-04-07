from django.shortcuts import get_object_or_404
from django import forms
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import UserMaintenance
from administration.models import EmployeeMaintenance, EmployeePositionMaintenance
from django.contrib.auth.models import User, Group

class ApprovalForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(queryset=DocumentTypeMaintenance.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.document_type)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.transaction_type)
    approval_level = forms.ModelChoiceField(queryset=WorkflowApprovalRule.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.approval_level)

    class Meta:
        model = ApprovalItem
        fields = ['document_number', 'notification','document_type','transaction_type','approval_level']

class ApproverModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}: {} {}".format(obj.username, obj.first_name, obj.last_name)        

class ApproverGroupAForm(forms.ModelForm):
    user = ApproverModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.document_type)

    class Meta:
        model = ApprovalItemApprover
        fields = []

    def __init__(self, *args, **kwargs):
        super(ApproverGroupAForm, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name='Group A').values_list('id', flat=True)
        
        ceo_position = get_object_or_404(EmployeePositionMaintenance, position_name='CHIEF EXECUTIVE OFFICER')
        ceo_user = get_object_or_404(EmployeeMaintenance, position_id=ceo_position)
        
        users = User.objects.filter(groups__in = groups).order_by('username')
        users = users.exclude(id=ceo_user.user.id)
        
        self.fields['user'].queryset = users
        
class ApproverGroupBForm(forms.ModelForm):
    user = ApproverModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.document_type)
    
    class Meta:
        model = ApprovalItemApprover
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(ApproverGroupBForm, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name='Group B').values_list('id', flat=True)
        self.fields['user'].queryset = User.objects.filter(groups__in = groups).order_by('username')

class CCForm(forms.ModelForm):
    user = ApproverModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.document_type)
    
    class Meta:
        model = ApprovalItemCC
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(CCForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all().order_by('username')

class RejectForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea())
    hiddenValueReject = forms.IntegerField()

    class Meta:
        model = ApprovalItemApprover
        fields = ['id']