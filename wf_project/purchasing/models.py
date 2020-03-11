from django.db import models
from administration.models import EmployeeMaintenance
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import ProjectMaintenance

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

class PurchaseOrder(models.Model):
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    vendor = models.ForeignKey(EmployeeMaintenance, verbose_name="Vendor", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Purchase Order'

    def __str__(self):
        return self.document_number

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

    class Meta:
        verbose_name = 'Purchase Request'
        verbose_name_plural = 'Purchase Requests'

    def __str__(self):
        return self.document_number

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