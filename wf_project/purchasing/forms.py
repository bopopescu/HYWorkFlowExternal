from django import forms
from .models import PurchaseOrder, PurchaseOrderAttachment, PurchaseOrderComparison2Attachment, PurchaseOrderComparison3Attachment, PurchaseOrderDetail
from administration.models import CompanyMaintenance, CompanyAddressDetail, CurrencyMaintenance, DepartmentMaintenance, DocumentTypeMaintenance
from administration.models import ProjectMaintenance, VendorMasterData, TransactiontypeMaintenance, UOMMaintenance
from Inventory.models import Item
import datetime

class NewPOForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), empty_label="Not Assigned")
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.filter(is_active=True).order_by('currency_name'), empty_label="Not Assigned")
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]).order_by('transaction_type_name'), empty_label="Not Assigned")
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    revision = forms.IntegerField(initial=1)
    delivery_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), label="Delivery Address", empty_label="Not Assigned")
    billing_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), label="Billing Address", empty_label="Not Assigned")
    comparison_vendor_2 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_2)
    comparison_vendor_3 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_3)
    delivery_address = forms.CharField(widget=forms.Textarea)
    vendor_address = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PurchaseOrder
        fields = ['document_number', 'status', 'remarks', 'reference', 
        'sub_total','discount','discount_amount','tax_amount','total_amount','payment_term',
        'payment_schedule', 'delivery_instruction', 'billing_address','comparison_vendor_2_amount', 'comparison_vendor_3_amount']

class DetailPOForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), empty_label="Not Assigned", initial=PurchaseOrder.vendor, disabled=True)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.filter(is_active=True).order_by('currency_name'), empty_label="Not Assigned", initial=PurchaseOrder.currency, disabled=True)
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), empty_label="Not Assigned", initial=PurchaseOrder.company, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned", initial=PurchaseOrder.project, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]).order_by('transaction_type_name'), empty_label="Not Assigned", initial=PurchaseOrder.transaction_type, disabled=True)
    submit_date = forms.DateField(initial=datetime.date.today,widget=forms.DateInput, disabled=True)
    delivery_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), label="Delivery Address", empty_label="Not Assigned", initial=PurchaseOrder.delivery_receiver, disabled=True)
    billing_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), label="Billing Address", empty_label="Not Assigned", initial=PurchaseOrder.billing_receiver, disabled=True)
    comparison_vendor_2 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_2, disabled=True)
    comparison_vendor_3 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_3, disabled=True)
    delivery_address = forms.CharField(widget=forms.Textarea)
    vendor_address = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PurchaseOrder
        fields = ['document_number', 'status', 'remarks', 'reference', 'revision',
        'sub_total','discount','discount_amount','tax_amount','total_amount','payment_term',
        'payment_schedule', 'delivery_instruction', 'delivery_address', 'billing_address','comparison_vendor_2_amount', 'comparison_vendor_3_amount']

class UpdatePOForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), empty_label="Not Assigned", initial=PurchaseOrder.vendor)
    currency = forms.ModelChoiceField(queryset=CurrencyMaintenance.objects.filter(is_active=True).order_by('currency_name'), empty_label="Not Assigned", initial=PurchaseOrder.currency)
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), empty_label="Not Assigned", initial=PurchaseOrder.company)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned", initial=PurchaseOrder.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]).order_by('transaction_type_name'), empty_label="Not Assigned", initial=PurchaseOrder.transaction_type)
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, disabled=True)
    delivery_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), label="Delivery Address", empty_label="Not Assigned", initial=PurchaseOrder.delivery_receiver)
    billing_receiver = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all().order_by('company_name'), label="Billing Address", empty_label="Not Assigned", initial=PurchaseOrder.billing_receiver)
    comparison_vendor_2 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_2)
    comparison_vendor_3 = forms.ModelChoiceField(queryset=VendorMasterData.objects.all().order_by('vendor_name'), label="Vendor", empty_label="Not Assigned", initial=PurchaseOrder.comparison_vendor_3)
    delivery_address = forms.CharField(widget=forms.Textarea)
    vendor_address = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PurchaseOrder
        fields = ['document_number', 'status', 'remarks', 'reference', 'revision',
        'sub_total','discount','discount_amount','tax_amount','total_amount','payment_term',
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
    item = forms.ModelChoiceField(queryset=Item.objects.all().order_by('item_code'), empty_label="Not Assigned")
    uom = forms.ModelChoiceField(queryset=UOMMaintenance.objects.all().order_by('uom_name'), empty_label="Not Assigned")

    class Meta:
        model = PurchaseOrderDetail
        fields = ['po', 'additional_description', 'quantity',
        'unit_price','remarks']