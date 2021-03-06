from django.db import models
from administration.models import EmployeeMaintenance, CompanyMaintenance, CompanyAddressDetail, CurrencyMaintenance, StatusMaintenance
from administration.models import DepartmentMaintenance, DocumentTypeMaintenance, ProjectMaintenance, UOMMaintenance, TaxMaintenance
from administration.models import PaymentTermMaintenance, VendorMasterData, VendorAddressDetail, TransactiontypeMaintenance
from Inventory.models import Item
from approval.models import ApprovalItem
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

def documenttype_document_number():
    po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
    document_number = po_type.running_number + 1
    po_type.running_number = document_number
    po_type.save()

    return '{0}-{1:05d}'.format(po_type.document_type_code,document_number)

class PurchaseOrder(models.Model):
    revision = models.IntegerField(default=1)
    document_number = models.CharField(verbose_name="Doc. No.", max_length=100, blank=True, null=True)
    vendor = models.ForeignKey(VendorMasterData, verbose_name="Vendor", on_delete=models.CASCADE, blank=True, null=True)
    vendor_address = models.CharField(max_length=250, blank=True, null=True)
    currency = models.ForeignKey(CurrencyMaintenance, verbose_name="Vendor", on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE, blank=True, null=True)
    approval = models.ForeignKey(ApprovalItem, verbose_name="Approval", on_delete=models.CASCADE, blank=True, null=True)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance, verbose_name="Transaction Type", on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(StatusMaintenance, on_delete=models.CASCADE, blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    sub_total = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    discount = models.DecimalField(verbose_name="Discount (%)",default=0.0, decimal_places=2, max_digits=15)
    discount_amount = models.DecimalField(default=0.0, decimal_places=2 ,max_digits=15)
    tax_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    total_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    payment_term = models.ForeignKey(PaymentTermMaintenance, verbose_name="Payment Terms", on_delete=models.CASCADE, blank=True, null=True)
    payment_schedule = models.CharField(max_length=100, blank=True, null=True)
    remarks = RichTextUploadingField(config_name='remarks_po', blank=True, null=True)
    delivery_instruction = RichTextUploadingField(config_name='del_ins_po', blank=True, null=True)
    delivery_receiver = models.ForeignKey(CompanyMaintenance, related_name='delivery',verbose_name="Delivery Address", null=True, blank=True, on_delete=models.SET_NULL)
    delivery_address =  models.CharField(max_length=250, blank=True, null=True)
    billing_receiver = models.ForeignKey(CompanyMaintenance, related_name='billing', verbose_name='Billing Address', null=True, blank=True, on_delete=models.SET_NULL)
    billing_address = models.CharField(max_length=250, blank=True, null=True)
    comparison_vendor_2 = models.ForeignKey(VendorMasterData, related_name="comparison2", verbose_name="Vendor", on_delete=models.CASCADE, blank=True, null=True)
    comparison_vendor_2_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, verbose_name="Total Amount")
    comparison_vendor_3 = models.ForeignKey(VendorMasterData, related_name="comparison3", verbose_name="Vendor", on_delete=models.CASCADE, blank=True, null=True)
    comparison_vendor_3_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, verbose_name="Total Amount")

    class Meta:
        verbose_name = 'Purchase Order'

    def __str__(self):
        return self.document_number

class PurchaseOrderDetail(models.Model):
    additional_description = models.CharField(verbose_name="Additional Description",max_length=250, blank=True, null=True)
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE, blank=True, null=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(verbose_name="Qty", default=0.0, decimal_places=3, max_digits=15)
    uom = models.ForeignKey(UOMMaintenance, verbose_name="Item", on_delete=models.CASCADE, blank=True, null=True)
    unit_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    tax = models.ForeignKey(TaxMaintenance, blank=True, null=True, on_delete=models.CASCADE)
    line_taxamount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_exclude = models.BooleanField(verbose_name="exclude tax", default=True, blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'Detail'

def documenttype_directory_path(instance, filename):
    po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
    return '{0}/{1}'.format(po_type.attachment_path,filename)

class PurchaseOrderAttachment(models.Model):
    attachment = models.FileField(upload_to=documenttype_directory_path,verbose_name="File Name", blank=True, null=True)
    attachment_date = models.DateField()
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Attachment'

class PurchaseOrderComparison2Attachment(models.Model):
    attachment = models.FileField(upload_to=documenttype_directory_path,verbose_name="File Name", blank=True, null=True)
    attachment_date = models.DateField()
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Attachment'

class PurchaseOrderComparison3Attachment(models.Model):
    attachment = models.FileField(upload_to=documenttype_directory_path, verbose_name="File Name", blank=True, null=True)
    attachment_date = models.DateField()
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Attachment'

class GoodsReceiptNote(models.Model):
    document_number = models.CharField(max_length=100, blank=True, null=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)
    receive_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    receive_date = models.DateField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Goods Receipt Note'

    def __str__(self):
        return self.document_number

class PurchaseInvoice(models.Model):
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=True, blank=True, null=True)    
    receive_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Purchase Invoice'

    def __str__(self):
        return self.invoice_number

class PurchaseCreditNote(models.Model):
    document_number = models.CharField(max_length=100, blank=True, null=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Credit Note'

    def __str__(self):
        return self.document_number

class PurchaseDebitNote(models.Model):
    document_number = models.CharField(max_length=100, blank=True, null=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Credit Note'

    def __str__(self):
        return self.document_number