from django.db import models
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import DocumentTypeMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData

class PaymentRequest(models.Model):
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    vendor = models.ForeignKey(VendorMasterData, verbose_name="Vendor", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    currency = models.ForeignKey(CurrencyMaintenance, verbose_name="Currency", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    document_source = models.ForeignKey(DocumentTypeMaintenance, verbose_name="Document Source", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Payment Request'
        verbose_name_plural = 'Payment Requests'

    def __str__(self):
        return self.document_number