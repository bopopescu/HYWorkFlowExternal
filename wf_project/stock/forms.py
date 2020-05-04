from django import forms
from django.forms import ModelChoiceField
from .models import StockTransfer,StockTransferDetail,StockTransferAttachment
from .models import StockAdjustment,StockAdjustmentDetail,StockAdjustmentAttachment
from .models import StockIssuing,StockIssuingDetail,StockIssuingAttachment
from django.shortcuts import get_object_or_404
import datetime
from Inventory.models import Item
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import TransactiontypeMaintenance,DepartmentMaintenance
from administration.models import DocumentTypeMaintenance,LocationMaintenance

class ItemNewChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s (%s)" % (obj.item_code, obj.item_description,obj.item_uom)

# Stock Transfer
class DetailStockTransferForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StockTransfer.company, disabled=True)
    from_location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockTransfer.from_location, disabled=True)
    to_location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockTransfer.to_location, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StockTransfer.project, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]), empty_label="Not Assigned",initial=StockTransfer.transaction_type, disabled=True)

    class Meta:
        model = StockTransfer
        fields = ['company','from_location','to_location','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']


class NewStockTransferForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned")
    from_location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned")
    to_location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]), empty_label="Not Assigned")
    revision = forms.IntegerField(initial=0)

    class Meta:
        model = StockTransfer
        fields = ['company','from_location','to_location','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']

class UpdateStockTransferForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StockTransfer.company)
    from_location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockTransfer.from_location)
    to_location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockTransfer.to_location)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StockTransfer.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]), empty_label="Not Assigned",initial=StockTransfer.transaction_type)

    class Meta:
        model = StockTransfer
        fields = ['company','from_location','to_location','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']

class NewStockTransferDetailForm(forms.ModelForm):
    item = ItemNewChoiceField(queryset=Item.objects.all(), empty_label="Not Assigned")

    class Meta:
        model = StockTransferDetail
        fields = ['stock_transfer','quantity','uom','additional_description','reason','remarks']

class NewStockTransferAttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = StockTransferAttachment
        fields = ['stock_transfer', 'attachment']

# Stock Adjustment
class DetailStockAdjustmentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StockAdjustment.company, disabled=True)
    location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockAdjustment.location, disabled=True)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned", initial=StockAdjustment.department, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StockAdjustment.project, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]), empty_label="Not Assigned",initial=StockAdjustment.transaction_type, disabled=True)

    class Meta:
        model = StockAdjustment
        fields = ['company','location','department','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']


class NewStockAdjustmentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned")
    location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned")
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]), empty_label="Not Assigned")
    revision = forms.IntegerField(initial=0)

    class Meta:
        model = StockAdjustment
        fields = ['company','location','department','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']

class UpdateStockAdjustmentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StockAdjustment.company)
    location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockAdjustment.location)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned", initial=StockAdjustment.department)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StockAdjustment.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]), empty_label="Not Assigned",initial=StockAdjustment.transaction_type)

    class Meta:
        model = StockAdjustment
        fields = ['company','location','department','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']

class NewStockAdjustmentDetailForm(forms.ModelForm):
    item = ItemNewChoiceField(queryset=Item.objects.all(), empty_label="Not Assigned")

    class Meta:
        model = StockAdjustmentDetail
        fields = ['stock_adjustment','quantity','uom','additional_description','reason','remarks']

class NewStockAdjustmentAttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = StockAdjustmentAttachment
        fields = ['stock_adjustment', 'attachment']

# Stock Issuing
class DetailStockIssuingForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StockIssuing.company, disabled=True)
    location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockIssuing.location, disabled=True)
    delivery_to = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), label="Delivery Address", empty_label="Not Assigned", initial=StockIssuing.delivery_to, disabled=True)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned", initial=StockIssuing.department, disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StockIssuing.project, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]), empty_label="Not Assigned",initial=StockIssuing.transaction_type, disabled=True)
    delivery_address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = StockIssuing
        fields = ['company','location','delivery_to','delivery_address','department','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']


class NewStockIssuingForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned")
    location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned")
    delivery_to = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), label="Delivery Address", empty_label="Not Assigned")
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]), empty_label="Not Assigned")
    revision = forms.IntegerField(initial=0)
    delivery_address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = StockIssuing
        fields = ['company','location','delivery_to','delivery_address','department','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']

class UpdateStockIssuingForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StockIssuing.company)
    location = forms.ModelChoiceField(queryset=LocationMaintenance.objects.filter(is_active=True).order_by('loc_name'), empty_label="Not Assigned",initial=StockIssuing.location)
    delivery_to = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), label="Delivery Address", empty_label="Not Assigned", initial=StockIssuing.delivery_to)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned", initial=StockIssuing.department)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StockIssuing.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]), empty_label="Not Assigned",initial=StockIssuing.transaction_type)
    delivery_address = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = StockIssuing
        fields = ['company','location','delivery_to','delivery_address','department','project','transaction_type','revision',
        'document_number','status','submit_date','attention','reference','remarks']

class NewStockIssuingDetailForm(forms.ModelForm):
    item = ItemNewChoiceField(queryset=Item.objects.all(), empty_label="Not Assigned")

    class Meta:
        model = StockIssuingDetail
        fields = ['stock_issuing','quantity','uom','additional_description','reason','remarks']

class NewStockIssuingAttachmentForm(forms.ModelForm):
    attachment_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    
    class Meta:
        model = StockIssuingAttachment
        fields = ['stock_issuing', 'attachment']
