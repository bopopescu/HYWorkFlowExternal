from django import forms
from .models import Memo
import datetime
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import MemoTemplateMaintenance
from administration.models import ProjectMaintenance

class NewMemoForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned")
    template = forms.ModelChoiceField(queryset=MemoTemplateMaintenance.objects.all(), empty_label="Not Assigned")
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)

    class Meta:
        model = Memo
        fields = ['revision', 'details', 'status', 'document_number', 'subject']