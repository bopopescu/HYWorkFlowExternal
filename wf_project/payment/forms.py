from django import forms
from .models import PaymentRequest,PaymentRequestDetail,PaymentAttachment
from django.shortcuts import get_object_or_404
import datetime
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import TaxMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import PaymentmodeMaintenance
from administration.models import EmployeeMaintenance
from administration.models import DocumentTypeMaintenance
from administration.models import UtiliyAccountTypeMaintenance 


class DetailPaymentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=PaymentRequest.company, disabled=True)
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.filter(is_active=True).order_by('vendor_name'), empty_label="Not Assigned",initial=PaymentRequest.vendor, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=PaymentRequest.project, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]), empty_label="Not Assigned",initial=PaymentRequest.transaction_type, disabled=True)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.filter(is_active=True), empty_label="Not Assigned",initial=PaymentRequest.currency, disabled=True)
    payment_mode = forms.ModelChoiceField(queryset=PaymentmodeMaintenance.objects.filter(is_active=True), empty_label="Not Assigned",initial=PaymentRequest.payment_mode, disabled=True)
    employee = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True), empty_label="Not Assigned",initial=PaymentRequest.employee, disabled=True)
    utility_account = forms.ModelChoiceField(queryset=UtiliyAccountTypeMaintenance.objects.filter(is_active=True), empty_label="Not Assigned",initial=PaymentRequest.utility_account, disabled=True)
    subject = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PaymentRequest
        fields = ['company','vendor','project','transaction_type','currency','payment_mode','utility_account',
        'employee','revision','document_number','status','submit_date','subject','reference',
        'sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks']


class NewPaymentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned")
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.filter(is_active=True).order_by('vendor_name'), empty_label="Not Assigned",required=False)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]), empty_label="Not Assigned")
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.filter(is_active=True).order_by('currency_name'), empty_label="Not Assigned")
    payment_mode = forms.ModelChoiceField(queryset=PaymentmodeMaintenance.objects.filter(is_active=True).order_by('payment_mode_name'), empty_label="Not Assigned")
    employee = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True).order_by('employee_name'), empty_label="Not Assigned",required=False)
    utility_account = forms.ModelChoiceField(queryset=UtiliyAccountTypeMaintenance.objects.filter(is_active=True).order_by('account_name'), empty_label="Not Assigned",required=False)
    revision = forms.IntegerField(initial=0)
    sub_total = forms.DecimalField(initial=0.00)
    discount_amount = forms.DecimalField(initial=0.00)
    discount_rate = forms.DecimalField(initial=0.00)
    tax_amount = forms.DecimalField(initial=0.00)
    total_amount = forms.DecimalField(initial=0.00)
    subject = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PaymentRequest
        fields = ['company','vendor','project','transaction_type','payment_mode','employee','utility_account',
        'revision','document_number','status','submit_date','subject','reference',
        'sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks']

class UpdatePaymentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=PaymentRequest.company)
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.filter(is_active=True).order_by('vendor_name'), empty_label="Not Assigned",initial=PaymentRequest.vendor,required=False)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=PaymentRequest.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]), empty_label="Not Assigned",initial=PaymentRequest.transaction_type)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.filter(is_active=True).order_by('currency_name'), empty_label="Not Assigned",initial=PaymentRequest.currency)
    payment_mode = forms.ModelChoiceField(queryset=PaymentmodeMaintenance.objects.filter(is_active=True).order_by('payment_mode_name'), empty_label="Not Assigned",initial=PaymentRequest.payment_mode)
    employee = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True).order_by('employee_name'), empty_label="Not Assigned",initial=PaymentRequest.employee,required=False)
    utility_account = forms.ModelChoiceField(queryset=UtiliyAccountTypeMaintenance.objects.filter(is_active=True).order_by('account_name'), empty_label="Not Assigned",initial=PaymentRequest.utility_account,required=False)
    sub_total = forms.DecimalField(initial=PaymentRequest.sub_total)
    discount_amount = forms.DecimalField(initial=PaymentRequest.discount_amount)
    discount_rate = forms.DecimalField(initial=PaymentRequest.discount_rate)
    tax_amount = forms.DecimalField(initial=PaymentRequest.tax_amount)
    total_amount = forms.DecimalField(initial=PaymentRequest.total_amount)
    subject = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = PaymentRequest
        fields = ['company','vendor','project','transaction_type','currency','payment_mode','employee','utility_account',
        'revision','document_number','status','submit_date','subject','reference',
        'sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks']

class NewPYItemForm(forms.ModelForm):
    tax = forms.ModelChoiceField(queryset=TaxMaintenance.objects.all(), empty_label="Not Assigned")

    class Meta:
        model = PaymentRequestDetail
        fields = ['py', 'item_description', 'price','line_total']

class NewPYAttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = PaymentAttachment
        fields = ['py', 'attachment']