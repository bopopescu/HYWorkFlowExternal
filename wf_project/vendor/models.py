from django.db import models
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import DocumentTypeMaintenance
from administration.models import VendorMasterData

class VendorQualification(models.Model):
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    vendor = models.ForeignKey(VendorMasterData, verbose_name="Vendor", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    document_type = models.ForeignKey(DocumentTypeMaintenance, verbose_name="Document Type", on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Vendor Qualification'
        verbose_name_plural = 'Vendor Qualifications'

    def __str__(self):
        return self.document_number

class VendorEvaluation(models.Model):
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    vendor = models.ForeignKey(VendorMasterData, verbose_name="Vendor", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    document_type = models.ForeignKey(DocumentTypeMaintenance, verbose_name="Document Type", on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)
    posting_date = models.DateField()
    due_date = models.DateField()
    doc_date = models.DateField()

    class Meta:
        verbose_name = 'Vendor Evaluation'
        verbose_name_plural = 'Vendor Evaluations'

    def __str__(self):
        return self.document_number