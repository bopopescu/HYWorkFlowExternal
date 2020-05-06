from django.db import models
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import EmployeeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import PaymentmodeMaintenance
from administration.models import DocumentTypeMaintenance
from administration.models import StatusMaintenance
from Inventory.models import Item
from administration.models import LocationMaintenance,UOMMaintenance,DepartmentMaintenance
from approval.models import ApprovalItem
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import datetime

def stock_transfer_default_status():
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]
    return StatusMaintenance.objects.filter(document_type=document_type,status_code='100')[0]

class StockTransfer(models.Model):
    revision = models.IntegerField(default=1)
    document_number = models.CharField(max_length=100,verbose_name="Document No",blank=True, null=True)
    from_location = models.ForeignKey(LocationMaintenance, verbose_name="From Location",related_name="stocktransferfromlocation", on_delete=models.CASCADE,blank=True, null=True)
    to_location = models.ForeignKey(LocationMaintenance, verbose_name="To Location",related_name="stocktransfertolocation", on_delete=models.CASCADE,blank=True, null=True)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE,blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE,blank=True, null=True)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance,verbose_name="Trans. Type", on_delete=models.CASCADE,blank=True, null=True)
    status = models.ForeignKey(StatusMaintenance,default=stock_transfer_default_status,verbose_name="Status", on_delete=models.CASCADE,blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(null=True, blank=True,default=datetime.date.today)
    attention = models.CharField(max_length=250)
    reference = models.CharField(max_length=100,null=True, blank=True)
    remarks = RichTextUploadingField(config_name='remarks_py',null=True, blank=True)

    class Meta:
        verbose_name = 'Stock Transfer'
        verbose_name_plural = 'Stock Transfer'

    def __str__(self):
        return self.attention

class StockTransferDetail(models.Model):
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE, blank=True, null=True)
    stock_transfer = models.ForeignKey('StockTransfer', on_delete=models.CASCADE,blank=True, null=True)
    additional_description = models.CharField(verbose_name="Additional Description",max_length=250, blank=True, null=True)
    quantity = models.DecimalField(verbose_name="Qty", default=0.0, decimal_places=3, max_digits=15)
    uom = models.ForeignKey(UOMMaintenance, verbose_name="UOM", on_delete=models.CASCADE, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'Stock Transfer Detail'
        verbose_name_plural = 'Stock Transfer Detail'

    def __str__(self):
        return self.additional_description

def stock_transfer_directory_path(instance, filename):
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]
    return '{0}/{1}'.format(document_type.attachment_path,filename)

class StockTransferAttachment(models.Model):
    attachment = models.FileField(upload_to=stock_transfer_directory_path,verbose_name="File Name", blank=True, null=True)
    attachment_date = models.DateField()
    stock_transfer = models.ForeignKey('StockTransfer', on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name = 'Stock Transfer Attachment'

def stock_adjustment_default_status():
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]
    return StatusMaintenance.objects.filter(document_type=document_type,status_code='100')[0]

class StockAdjustment(models.Model):
    revision = models.IntegerField(default=1)
    document_number = models.CharField(max_length=100,verbose_name="Document No",blank=True, null=True)
    location = models.ForeignKey(LocationMaintenance, verbose_name="Location", on_delete=models.CASCADE,blank=True, null=True)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE,blank=True, null=True)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE,blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE,blank=True, null=True)
    document_type = models.ForeignKey(DocumentTypeMaintenance, verbose_name="Document Type", on_delete=models.CASCADE,blank=True, null=True)
    document_pk = models.IntegerField(blank=True, null=True)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance,verbose_name="Trans. Type", on_delete=models.CASCADE,blank=True, null=True)
    status = models.ForeignKey(StatusMaintenance,default=stock_adjustment_default_status,verbose_name="Status", on_delete=models.CASCADE,blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(null=True, blank=True,default=datetime.date.today)
    attention = models.CharField(max_length=250)
    reference = models.CharField(max_length=100,null=True, blank=True)
    remarks = RichTextUploadingField(config_name='remarks_py',null=True, blank=True)

    class Meta:
        verbose_name = 'Stock Adjustment'
        verbose_name_plural = 'Stock Adjustment'

    def __str__(self):
        return self.attention

class StockAdjustmentDetail(models.Model):
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE, blank=True, null=True)
    stock_adjustment = models.ForeignKey('StockAdjustment', on_delete=models.CASCADE,blank=True, null=True)
    additional_description = models.CharField(verbose_name="Additional Description",max_length=250, blank=True, null=True)
    quantity = models.DecimalField(verbose_name="Qty", default=0.0, decimal_places=3, max_digits=15)
    uom = models.ForeignKey(UOMMaintenance, verbose_name="UOM", on_delete=models.CASCADE, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Stock Adjustment Detail'
        verbose_name_plural = 'Stock Adjustment Detail'

    def __str__(self):
        return self.additional_description

def stock_adjustment_directory_path(instance, filename):
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]
    return '{0}/{1}'.format(document_type.attachment_path,filename)

class StockAdjustmentAttachment(models.Model):
    attachment = models.FileField(upload_to=stock_adjustment_directory_path,verbose_name="File Name", blank=True, null=True)
    attachment_date = models.DateField()
    stock_adjustment = models.ForeignKey('StockAdjustment', on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name = 'Stock Adjustment Attachment'


def stock_issuing_default_status():
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]
    return StatusMaintenance.objects.filter(document_type=document_type,status_code='100')[0]

class StockIssuing(models.Model):
    revision = models.IntegerField(default=1)
    document_number = models.CharField(max_length=100,verbose_name="Document No",blank=True, null=True)
    location = models.ForeignKey(LocationMaintenance, verbose_name="Location", on_delete=models.CASCADE,blank=True, null=True)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE,blank=True, null=True)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE,blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE,blank=True, null=True)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance,verbose_name="Trans. Type", on_delete=models.CASCADE,blank=True, null=True)
    status = models.ForeignKey(StatusMaintenance,default=stock_issuing_default_status,verbose_name="Status", on_delete=models.CASCADE,blank=True, null=True)
    delivery_to = models.ForeignKey(CompanyMaintenance,verbose_name="Delivery Address",related_name="stocktransferdeliveryto", null=True, blank=True, on_delete=models.SET_NULL)
    delivery_address =  models.CharField(max_length=250, blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(null=True, blank=True,default=datetime.date.today)
    attention = models.CharField(max_length=250)
    reference = models.CharField(max_length=100,null=True, blank=True)
    remarks = RichTextUploadingField(config_name='remarks_py',null=True, blank=True)

    class Meta:
        verbose_name = 'Stock Issuing'
        verbose_name_plural = 'Stock Issuing'

    def __str__(self):
        return self.attention

class StockIssuingDetail(models.Model):
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE, blank=True, null=True)
    stock_issuing = models.ForeignKey('StockIssuing', on_delete=models.CASCADE,blank=True, null=True)
    additional_description = models.CharField(verbose_name="Additional Description",max_length=250, blank=True, null=True)
    quantity = models.DecimalField(verbose_name="Qty", default=0.0, decimal_places=3, max_digits=15)
    uom = models.ForeignKey(UOMMaintenance, verbose_name="UOM", on_delete=models.CASCADE, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Stock Issuing Detail'
        verbose_name_plural = 'Stock Issuing Detail'

    def __str__(self):
        return self.additional_description

def stock_issuing_directory_path(instance, filename):
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]
    return '{0}/{1}'.format(document_type.attachment_path,filename)

class StockIssuingAttachment(models.Model):
    attachment = models.FileField(upload_to=stock_issuing_directory_path,verbose_name="File Name", blank=True, null=True)
    attachment_date = models.DateField()
    stock_issuing = models.ForeignKey('StockIssuing', on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name = 'Stock Issuing Attachment'

class ItemMovement(models.Model):
    location = models.ForeignKey(LocationMaintenance, verbose_name="Location", on_delete=models.CASCADE,blank=True, null=True)
    document_type = models.ForeignKey(DocumentTypeMaintenance, verbose_name="Document Type", on_delete=models.CASCADE,blank=True, null=True)
    document_pk = models.IntegerField()
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE, blank=True, null=True)
    stock_in = models.DecimalField(default=0.0, decimal_places=3, max_digits=15)
    stock_out = models.DecimalField(default=0.0, decimal_places=3, max_digits=15)
