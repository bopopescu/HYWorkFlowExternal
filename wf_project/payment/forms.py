from django import forms
from .models import PaymentRequest
from django.shortcuts import get_object_or_404
import datetime
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import TaxMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import PaymentmodeMaintenance


class DetailPaymentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.company, disabled=True)
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.vendor, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.project, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.transaction_type, disabled=True)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.currency, disabled=True)
    payment_mode = forms.ModelChoiceField(queryset=PaymentmodeMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.payment_mode, disabled=True)

    class Meta:
        model = PaymentRequest
        fields = ['revision','document_number','status','submit_date','subject','reference',
        'sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks']

class NewPaymentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned")
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned")
    payment_mode = forms.ModelChoiceField(queryset=PaymentmodeMaintenance.objects.all(), empty_label="Not Assigned")
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    revision = forms.IntegerField(initial=0)

    class Meta:
        model = PaymentRequest
        fields = ['revision','document_number','status','submit_date','subject','reference',
        'sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks']

class UpdatePaymentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.company)
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.vendor)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.transaction_type)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.currency)
    payment_mode = forms.ModelChoiceField(queryset=PaymentmodeMaintenance.objects.all(), empty_label="Not Assigned",initial=PaymentRequest.payment_mode)

    class Meta:
        model = PaymentRequest
        fields = ['revision','document_number','status','submit_date','subject','reference',
        'sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks']