from django.db import models
from administration.models import EmployeeMaintenance, CompanyMaintenance, CurrencyMaintenance, TransactiontypeMaintenance
from administration.models import DepartmentMaintenance, DocumentTypeMaintenance, ProjectMaintenance
from Inventory.models import Item
from approval.models import ApprovalItem
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class GoodsReceiptNote(models.Model):
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    supplier = models.ForeignKey(EmployeeMaintenance, verbose_name="Vendor", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    currency = models.ForeignKey(CurrencyMaintenance, verbose_name="Currency", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Goods Receipt Note'

    def __str__(self):
        return self.document_number

def documenttype_document_number():
    po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
    return '{0}-{1:05d}'.format(po_type.document_type_code,po_type.running_number)

class PurchaseOrder(models.Model):
    revision = models.IntegerField(default=1)
    document_number = models.CharField(default=documenttype_document_number, max_length=100, blank=True, null=True)
    vendor = models.ForeignKey(EmployeeMaintenance, verbose_name="Vendor", on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    approval = models.ForeignKey(ApprovalItem, verbose_name="Approval", on_delete=models.CASCADE, blank=True, null=True)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance, verbose_name="Transaction Type", on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(default="D",max_length=1, blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    sub_total = models.DecimalField(default=0.0,decimal_places=2,max_digits=6)
    discount = models.DecimalField(default=0.0,decimal_places=2,max_digits=6)
    tax_amount = models.DecimalField(default=0.0,decimal_places=2,max_digits=6)
    total_amount = models.DecimalField(default=0.0,decimal_places=2,max_digits=6)
    payment_term = models.CharField(max_length=100, blank=True, null=True)
    payment_schedule = models.CharField(max_length=100, blank=True, null=True)
    remarks = RichTextUploadingField(config_name='remarks_po', blank=True, null=True)
    attachment = models.FileField(verbose_name="File Name")
    attachment_date = models.DateField()

    class Meta:
        verbose_name = 'Purchase Order'

    def __str__(self):
        return self.document_number

class PurchaseOrderAddress(models.Model):
    name = models.CharField(verbose_name="Pay To",max_length=150)
    address = models.CharField(verbose_name="Address",max_length=250)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Address'    
        verbose_name_plural = 'Addresses'    

class PurchaseOrderCC(models.Model):
    name = models.CharField(verbose_name="Name",max_length=150)
    email = models.CharField(verbose_name="Email",max_length=250)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'CC'

class PurchaseOrderDetail(models.Model):
    description = models.CharField(verbose_name="Additional Description",max_length=250)
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Qty")
    amount = models.IntegerField()
    discount = models.DecimalField(decimal_places=2,max_digits=6)

    class Meta:
        verbose_name = 'Detail'

class PurchaseQuotation(models.Model):    
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    vendor = models.ForeignKey(EmployeeMaintenance, verbose_name="Vendor", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)
    recommended = models.BooleanField()

    class Meta:
        verbose_name = 'Purchase Quotation'

    def __str__(self):
        return self.document_number

class PurchaseRequest(models.Model):
    is_interdepartmental = models.BooleanField()    
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    requester = models.ForeignKey(EmployeeMaintenance, verbose_name="Requester", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)
    sub_total = models.DecimalField(decimal_places=2,max_digits=6)
    remarks = models.CharField(max_length=250)
    attachment = models.FileField(verbose_name="File Name")
    attachment_date = models.DateField()

    class Meta:
        verbose_name = 'Purchase Request'
        verbose_name_plural = 'Purchase Requests'

    def __str__(self):
        return self.document_number

class PurchaseRequestAddress(models.Model):
    name = models.CharField(verbose_name="To",max_length=150)
    address = models.CharField(verbose_name="Address",max_length=250)
    pr = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Address'    
        verbose_name_plural = 'Addresses'    

class PurchaseRequestCC(models.Model):
    name = models.CharField(verbose_name="Name",max_length=150)
    email = models.CharField(verbose_name="Email",max_length=250)
    pr = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'CC'

class PurchaseRequestDetail(models.Model):
    description = models.CharField(verbose_name="Additional Description",max_length=250)
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE)
    pr = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
    eta = models.DateTimeField(verbose_name="ETA Date")
    quantity = models.IntegerField(verbose_name="Qty")
    amount = models.IntegerField()
    remark = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Detail'

class PurchaseRequestPettyCash(models.Model):
    is_employee = models.BooleanField(verbose_name="Pay To")    
    revision = models.CharField(max_length=100)
    employee = models.ForeignKey(EmployeeMaintenance, verbose_name="Requester", on_delete=models.CASCADE)
    currency = models.ForeignKey(CurrencyMaintenance, verbose_name="Currency", on_delete=models.CASCADE)    
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    payment_mode = models.CharField(max_length=100)
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)
    sub_total = models.DecimalField(decimal_places=2,max_digits=6)
    discount = models.DecimalField(decimal_places=2,max_digits=6)
    tax_amount = models.DecimalField(decimal_places=2,max_digits=6)
    total_amount = models.DecimalField(decimal_places=2,max_digits=6)
    remarks = models.CharField(max_length=250)
    attachment = models.FileField(verbose_name="File Name")
    attachment_date = models.DateField()

    class Meta:
        verbose_name = 'Purchase Request (Petty Cash)'
        verbose_name_plural = 'Purchase Request (Petty Cash)'

    def __str__(self):
        return self.reference

class PurchaseRequestPettyCashItems(models.Model):
    description = models.CharField(verbose_name="Item Description",max_length=250)
    prpc = models.ForeignKey(PurchaseRequestPettyCash, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2,max_digits=6)
    tax_amount = models.DecimalField(decimal_places=2,max_digits=6)
    line_total = models.DecimalField(decimal_places=2,max_digits=6)

    class Meta:
        verbose_name = 'Item'

class RequestForQuotation(models.Model):    
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    requester = models.ForeignKey(EmployeeMaintenance, verbose_name="Requester", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    doc_date = models.DateField()
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Request For Quotation'

    def __str__(self):
        return self.document_number