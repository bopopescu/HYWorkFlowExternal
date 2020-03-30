from django.db import models
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import EmployeeMaintenance
from administration.models import TaxMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import PaymentmodeMaintenance
from administration.models import DocumentTypeMaintenance
from approval.models import ApprovalItem
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

def documenttype_document_number():
    document_type = DocumentTypeMaintenance.objects.filter(document_type_name="Payment Request")[0]
    return '{0}-{1:05d}'.format(document_type.document_type_code,document_type.running_number)

class PaymentRequest(models.Model):
    revision = models.IntegerField()
    document_number = models.CharField(default=documenttype_document_number,max_length=100,verbose_name="Document No")
    vendor = models.ForeignKey(VendorMasterData,null=True, blank=True,verbose_name="Vendor", on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeMaintenance,null=True, blank=True, verbose_name="Vendor", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    currency = models.ForeignKey(CurrencyMaintenance, verbose_name="Currency", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance,verbose_name="Trans. Type", on_delete=models.CASCADE)
    approval = models.ForeignKey(ApprovalItem, verbose_name="Approval", on_delete=models.CASCADE, blank=True, null=True)
    payment_mode = models.ForeignKey(PaymentmodeMaintenance, verbose_name="Payment Mode", on_delete=models.CASCADE)
    status = models.CharField(max_length=1,default="D", blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(null=True, blank=True)
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Discount")
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = RichTextUploadingField(config_name='remarks_py',null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='paymentcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='paymentmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment Request'
        verbose_name_plural = 'Payment Requests'

    def __str__(self):
        return self.subject

def documenttype_directory_path(instance, filename):
    py_type = DocumentTypeMaintenance.objects.filter(document_type_name="Payment Request")[0]
    return '{0}/{1}'.format(py_type.attachment_path,filename)

class PaymentAttachment(models.Model):
    attachment = models.FileField(upload_to=documenttype_directory_path,verbose_name="File Name")
    attachment_date = models.DateField(auto_now_add=True)
    py = models.ForeignKey('PaymentRequest', verbose_name="PaymentRequest",blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Attachment'

class PaymentRequestDetail(models.Model):
    py = models.ForeignKey('PaymentRequest',on_delete=models.CASCADE,blank=True, null=True)
    linenum = models.IntegerField(null=True, blank=True)
    item_description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey(TaxMaintenance,default=0,on_delete=models.CASCADE)
    line_taxamount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    line_total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    class Meta:
        verbose_name = 'Payment Detail'

    def __str__(self):
        return self.item_description