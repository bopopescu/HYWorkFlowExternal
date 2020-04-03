from django import forms
from .models import Memo, MemoAttachment
from django.shortcuts import get_object_or_404
import datetime
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import MemoTemplateMaintenance
from administration.models import ProjectMaintenance

class DetailMemoForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.company, disabled=True)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.department, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.project, disabled=True)
    template = forms.ModelChoiceField(queryset=MemoTemplateMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.template, disabled=True)
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    subject = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Memo
        fields = ['revision', 'details', 'status', 'document_number']

class NewMemoForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned")
    template = forms.ModelChoiceField(queryset=MemoTemplateMaintenance.objects.all(), empty_label="Not Assigned")
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    revision = forms.IntegerField(initial=1)
    subject = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Memo
        fields = ['details', 'status', 'document_number']

class UpdateMemoForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.company)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.department)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.project)
    template = forms.ModelChoiceField(queryset=MemoTemplateMaintenance.objects.all(), empty_label="Not Assigned", initial=Memo.template)
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    subject = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Memo
        fields = ['revision', 'details', 'status', 'document_number']

class NewMemoAttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = MemoAttachment
        fields = ['memo', 'attachment']