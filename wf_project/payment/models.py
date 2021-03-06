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
from administration.models import StatusMaintenance
from administration.models import UtiliyAccountTypeMaintenance 
from utility_dashboard.models import UtilityApprovalItem
from approval.models import ApprovalItem
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import datetime

def documenttype_document_number():
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
    return '{0}-{1:05d}'.format(document_type.document_type_code,document_type.running_number)

def default_status():
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
    return StatusMaintenance.objects.filter(document_type=document_type,status_code='100')[0]

class PaymentRequest(models.Model):
    revision = models.IntegerField(default=1)
    document_number = models.CharField(max_length=100,verbose_name="Document No",blank=True, null=True)
    vendor = models.ForeignKey(VendorMasterData,null=True, blank=True,verbose_name="Vendor", on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeMaintenance,null=True, blank=True, verbose_name="Employee", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE,blank=True, null=True)
    currency = models.ForeignKey(CurrencyMaintenance, verbose_name="Currency", on_delete=models.CASCADE,blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE,blank=True, null=True)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance,verbose_name="Trans. Type", on_delete=models.CASCADE,blank=True, null=True)
    utility_account = models.ForeignKey(UtiliyAccountTypeMaintenance,verbose_name="Utility Account", on_delete=models.CASCADE,blank=True, null=True)
    approval = models.ForeignKey(ApprovalItem, verbose_name="Approval", on_delete=models.CASCADE, blank=True, null=True)
    utility_account_approval = models.ForeignKey(UtilityApprovalItem,verbose_name="Utility Approval", on_delete=models.CASCADE, blank=True, null=True)
    payment_mode = models.ForeignKey(PaymentmodeMaintenance, verbose_name="Payment Mode", on_delete=models.CASCADE,blank=True, null=True)
    document_pk = models.IntegerField(blank=True,null=True)
    document_type= models.ForeignKey(DocumentTypeMaintenance,on_delete=models.CASCADE,blank=True, null=True)
    status = models.ForeignKey(StatusMaintenance,default=default_status,verbose_name="Status", on_delete=models.CASCADE,blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(null=True, blank=True,default=datetime.date.today)
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Discount", default=0.00)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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