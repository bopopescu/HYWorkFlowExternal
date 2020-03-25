from django import forms
from .models import PaymentRequest
import datetime
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import TaxMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import PaymentmodeMaintenance

class NewPaymentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned")
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned")
    payment_mode = forms.ModelChoiceField(queryset=PaymentmodeMaintenance.objects.all(), empty_label="Not Assigned")
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)

    class Meta:
        model = PaymentRequest
        fields = ['revision','document_number','status','submit_date','subject','reference',
        'sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks','attachment','attachment_date']