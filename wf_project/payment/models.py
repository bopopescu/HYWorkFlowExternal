from django.db import models
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import DocumentTypeMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import TaxMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import PaymentmodeMaintenance
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class PaymentRequest(models.Model):
    revision = models.IntegerField()
    document_number = models.CharField(max_length=100,verbose_name="Document No")
    vendor = models.ForeignKey(VendorMasterData, verbose_name="Vendor", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    currency = models.ForeignKey(CurrencyMaintenance, verbose_name="Currency", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance,verbose_name="Trans. Type", on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentmodeMaintenance, verbose_name="Payment Mode", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField(null=True, blank=True)
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Discount")
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = RichTextUploadingField(config_name='remarks_py')
    attachment = models.FileField(verbose_name="File Name")
    attachment_date = models.DateField()
    created_by = models.ForeignKey(User, related_name='paymentcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='paymentmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment Request'
        verbose_name_plural = 'Payment Requests'

    def __str__(self):
        return self.subject

class PaymentRequestDetail(models.Model):
    parent_id = models.ForeignKey('PaymentRequest', default=0,on_delete=models.CASCADE)
    linenum = models.IntegerField()
    item_description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey(TaxMaintenance,default=0,on_delete=models.CASCADE)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Payment Detail'

    def __str__(self):
        return self.document_number