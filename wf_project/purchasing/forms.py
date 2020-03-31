from django import forms
from .models import PurchaseOrder
from administration.models import CompanyMaintenance, CurrencyMaintenance, DepartmentMaintenance
from administration.models import ProjectMaintenance, VendorMasterData, TransactiontypeMaintenance
import datetime

class NewPOForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned")
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned")
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned")
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    status = forms.CharField(initial="D")
    revision = forms.IntegerField(initial=1)

    class Meta:
        model = PurchaseOrder
        fields = ['document_number', 'subject']