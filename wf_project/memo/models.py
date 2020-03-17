from django.db import models
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import ProjectMaintenance

class Memo(models.Model):
    revision = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    submit_date = models.DateField()
    subject = models.CharField(max_length=250)
    details = models.TextField(default="")
    attachment = models.FileField(verbose_name="File Name")
    attachment_date = models.DateField()

    class Meta:
        verbose_name = 'Memo'
        verbose_name_plural = 'Memos'

    def __str__(self):
        return self.document_number

class MemoCC(models.Model):
    name = models.CharField(verbose_name="Name",max_length=150)
    email = models.CharField(verbose_name="Email",max_length=250)
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'CC'