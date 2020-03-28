from django.db import models
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import UserMaintenance
from administration.models import EmployeeMaintenance

class ApprovalItem(models.Model):
    document_number = models.CharField(max_length=100)
    document_type = models.ForeignKey(DocumentTypeMaintenance, verbose_name="Document Type", on_delete=models.CASCADE,  blank=True, null=True)
    document_pk = models.IntegerField(default=0)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance, verbose_name="Transaction Type", on_delete=models.CASCADE,  blank=True, null=True)
    approval_level = models.ForeignKey(WorkflowApprovalRule, verbose_name="Approval Level", on_delete=models.CASCADE,  blank=True, null=True)
    notification = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)

class ApprovalItemApprover(models.Model):
    stage = models.IntegerField(default=0)
    user = models.ForeignKey(UserMaintenance, verbose_name="User", on_delete=models.CASCADE,  blank=True, null=True)
    approval_item = models.ForeignKey('ApprovalItem', on_delete=models.CASCADE)

class ApprovalItemCC(models.Model):
    employee = models.ForeignKey(EmployeeMaintenance, verbose_name="CC", on_delete=models.CASCADE,  blank=True, null=True)
    approval_item = models.ForeignKey('ApprovalItem', on_delete=models.CASCADE)