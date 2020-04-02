from django.db import models
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import ProjectMaintenance
from administration.models import MemoTemplateMaintenance
from administration.models import DocumentTypeMaintenance
from approval.models import ApprovalItem
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

def documenttype_document_number():
    memo_type = DocumentTypeMaintenance.objects.filter(document_type_name="Memo")[0]
    document_number = memo_type.running_number + 1
    #memo_type.running_number = document_number 
    #memo_type.save()
    
    return '{0}-{1:05d}'.format(memo_type.document_type_code,document_number)

class Memo(models.Model):
    revision = models.IntegerField(default=1)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE, blank=True, null=True)
    approval = models.ForeignKey(ApprovalItem, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(default="D",max_length=1, blank=True, null=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    submit_date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    details = RichTextUploadingField(config_name='details_memo', blank=True, null=True)
    template = models.ForeignKey(MemoTemplateMaintenance, verbose_name="Project", on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Memo'
        verbose_name_plural = 'Memos'

    def __str__(self):
        return self.document_number

def documenttype_directory_path(instance, filename):
    memo_type = DocumentTypeMaintenance.objects.filter(document_type_name="Memo")[0]
    return '{0}/{1}'.format(memo_type.attachment_path,filename)

class MemoAttachment(models.Model):
    attachment = models.FileField(upload_to=documenttype_directory_path,verbose_name="File Name", blank=True, null=True)
    attachment_date = models.DateField(auto_now_add=True)
    memo = models.ForeignKey('Memo', verbose_name="Memo", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Attachment'