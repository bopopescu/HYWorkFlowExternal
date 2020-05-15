from django.db import models
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule,UtiliyAccountTypeMaintenance
from django.contrib.auth.models import User

class UtilityApprovalItem(models.Model):
    approval_code = models.CharField(max_length=100,verbose_name="Approval Code", blank=True, null=True)
    document_number = models.CharField(max_length=100,verbose_name="Doc. No.")
    document_type = models.ForeignKey(DocumentTypeMaintenance, verbose_name="Doc.Type", on_delete=models.CASCADE,  blank=True, null=True)
    document_pk = models.IntegerField(default=0)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance, verbose_name="Trans. Type", on_delete=models.CASCADE,  blank=True, null=True)
    utility_account = models.ForeignKey(UtiliyAccountTypeMaintenance, verbose_name="Utility Account", on_delete=models.CASCADE,  blank=True, null=True)
    approval_level = models.ForeignKey(WorkflowApprovalRule, verbose_name="Approval Level", on_delete=models.CASCADE,  blank=True, null=True)
    notification = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    submit_by = models.ForeignKey(User, verbose_name="Approver", on_delete=models.CASCADE,  blank=True, null=True)
    approved_date = models.DateField(blank=True, null=True)
    
    def __str__(self):        
        if self.status == "D":
            return "Draft"
        elif self.status == "IP":
            return "In Progress"
        elif self.status == "A":
            return "Approved"
        else:
            return "Rejected"

class UtilityApprovalItemApprover(models.Model):
    stage = models.IntegerField(default=1)
    user = models.ForeignKey(User, verbose_name="Approver", on_delete=models.CASCADE, blank=True, null=True)
    utility_approval_item = models.ForeignKey('UtilityApprovalItem', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)

class UtilityApprovalItemCC(models.Model):
    user = models.ForeignKey(User, verbose_name="CC", on_delete=models.CASCADE,  blank=True, null=True)
    utility_approval_item = models.ForeignKey('UtilityApprovalItem', on_delete=models.CASCADE)