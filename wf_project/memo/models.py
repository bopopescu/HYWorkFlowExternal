from django.db import models
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import ProjectMaintenance
from administration.models import MemoTemplateMaintenance
from ckeditor_uploader.fields import RichTextUploadingField

class Memo(models.Model):
    revision = models.IntegerField(default=0)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, blank=True, null=True)
    submit_date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    details = RichTextUploadingField(config_name='details_memo', blank=True, null=True)
    template = models.ForeignKey(MemoTemplateMaintenance, verbose_name="Project", on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Memo'
        verbose_name_plural = 'Memos'

    def __str__(self):
        return self.document_number

class MemoAttachment(models.Model):
    attachment = models.FileField(verbose_name="File Name")
    attachment_date = models.DateField(auto_now_add=True)
    memo = models.ForeignKey('Memo', verbose_name="Memo", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Attachment'