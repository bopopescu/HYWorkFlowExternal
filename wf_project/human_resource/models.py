from django.db import models
from administration.models import EmployeeMaintenance
from administration.models import CompanyMaintenance

class StaffRecruitmentRequest(models.Model):
    position_title = models.CharField(max_length=100)
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    reporting_to = models.ForeignKey(EmployeeMaintenance, verbose_name="Reporting To", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    budgeted = models.BooleanField()
    status = models.CharField(max_length=1)
    hire_type = models.CharField(max_length=1)
    request_date = models.DateField()
    subject = models.CharField(max_length=250)
    reference = models.CharField(max_length=100)
    headcounts = models.IntegerField()

    class Meta:
        verbose_name = 'Staff Recruitment Request'
        verbose_name_plural = 'Staff Recruitment Requests'

    def __str__(self):
        return self.document_number