from django.shortcuts import get_object_or_404
from django import forms
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import EmployeeMaintenance, EmployeePositionMaintenance
from django.contrib.auth.models import User, Group
import django.http.request as request
from django.db.models import Q

class ApprovalForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(queryset=DocumentTypeMaintenance.objects.all(), label="Doc. Type", empty_label="Not Assigned", initial=ApprovalItem.document_type)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), label="Trans. Type", empty_label="Not Assigned", initial=ApprovalItem.transaction_type)
    approval_level = forms.ModelChoiceField(queryset=WorkflowApprovalRule.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.approval_level)

    class Meta:
        model = ApprovalItem
        fields = ['document_number', 'notification', 'document_type', 'transaction_type', 'approval_level']

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
        users = User.objects.filter(groups__in=groups).order_by('username')
        self.fields['user'].queryset = users
        
class ApproverGroupBForm(forms.ModelForm):
    user = ApproverModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.document_type)

    class Meta:
        model = ApprovalItemApprover
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(ApproverGroupBForm, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name='Group B').values_list('id', flat=True)
        self.fields['user'].queryset = User.objects.filter(groups__in=groups).order_by('username')


class ApproverAandBModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        employee = EmployeeMaintenance.objects.filter(user_id=obj.id)
        if employee.count() > 0 :
            return "{}: {} {} - {}".format(obj.username, obj.first_name, obj.last_name,employee[0].employee_group)        
        else:
            return "{}: {} {}".format(obj.username, obj.first_name, obj.last_name)

class ApproverGroupAAndBForm(forms.ModelForm):
    supervisor_user = ApproverAandBModelChoiceField(queryset=User.objects.all(), empty_label="Not Assigned", initial=ApprovalItem.document_type)

    class Meta:
        model = ApprovalItemApprover
        fields = []
    
    def __init__(self,user ,*args, **kwargs):
        super(ApproverGroupAAndBForm, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(Q(name='Group B') | Q(name='Group A')).values_list('id', flat=True)
        self.fields['supervisor_user'].queryset = User.objects.filter(groups__in=groups).exclude(id=user.id).order_by('username')

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
