from django import forms
from .models import PurchaseOrder, PurchaseOrderAttachment, PurchaseOrderComparison2Attachment, PurchaseOrderComparison3Attachment, PurchaseOrderDetail
from administration.models import CompanyMaintenance, CompanyAddressDetail, CurrencyMaintenance, DepartmentMaintenance
from administration.models import ProjectMaintenance, VendorMasterData, TransactiontypeMaintenance, UOMMaintenance
from Inventory.models import Item
import datetime

class NewPOForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned")
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned")
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned")
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    revision = forms.IntegerField(initial=1)
    delivery_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), label="Delivery Address", empty_label="Not Assigned")
    billing_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), label="Billing Address", empty_label="Not Assigned")
    
    class Meta:
        model = PurchaseOrder
        fields = ['document_number', 'status', 'subject', 'remarks', 'reference', 
        'sub_total','discount','tax_amount','total_amount','payment_term',
        'payment_schedule', 'delivery_instruction', 'delivery_address', 'billing_address']

class DetailPOForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.vendor, disabled=True)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.currency, disabled=True)
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.company, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.project, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.transaction_type, disabled=True)
    submit_date = forms.DateField(initial=datetime.date.today,widget=forms.DateInput, disabled=True)
    delivery_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), label="Delivery Address", empty_label="Not Assigned", initial=PurchaseOrder.delivery_receiver, disabled=True)
    billing_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), label="Billing Address", empty_label="Not Assigned", initial=PurchaseOrder.billing_receiver, disabled=True)
    comparison_vendor_2 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_2, disabled=True)
    comparison_vendor_3 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_3, disabled=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['document_number', 'status','subject', 'remarks', 'reference', 'revision',
        'sub_total','discount','tax_amount','total_amount','payment_term',
        'payment_schedule', 'delivery_instruction', 'delivery_address', 'billing_address','comparison_vendor_2_amount', 'comparison_vendor_3_amount']

class UpdatePOForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.vendor)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.currency)
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.company)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.all(), empty_label="Not Assigned", initial=PurchaseOrder.transaction_type)
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    delivery_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), label="Delivery Address", empty_label="Not Assigned", initial=PurchaseOrder.delivery_receiver)
    billing_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), label="Billing Address", empty_label="Not Assigned", initial=PurchaseOrder.billing_receiver)
    comparison_vendor_2 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_2)
    comparison_vendor_3 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all(), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_3)
    
    class Meta:
        model = PurchaseOrder
        fields = ['document_number', 'status','subject', 'remarks', 'reference', 'revision',
        'sub_total','discount','tax_amount','total_amount','payment_term',
        'payment_schedule', 'delivery_instruction', 'delivery_address', 'billing_address','comparison_vendor_2_amount', 'comparison_vendor_3_amount']

class NewPOAttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = PurchaseOrderAttachment
        fields = ['po', 'attachment']   

class NewPOComparison2AttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = PurchaseOrderComparison2Attachment
        fields = ['po', 'attachment']

class NewPOComparison3AttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = PurchaseOrderComparison3Attachment
        fields = ['po', 'attachment']

class NewPODetailForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label="Not Assigned")
    uom = forms.ModelChoiceField(queryset=UOMMaintenance.objects.all(), empty_label="Not Assigned")

    class Meta:
        model = PurchaseOrderDetail
        fields = ['po', 'additional_description', 'quantity',
        'unit_price','remarks']