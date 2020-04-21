from django.db import models
from django.contrib.auth.models import User
from administration.models import EmployeeMaintenance
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import ProjectMaintenance
from administration.models import DrawerMaintenance
from administration.models import StatusMaintenance,TransactiontypeMaintenance 
from approval.models import ApprovalItem
import datetime

# class AdvanceRefund(models.Model):
#     revision = models.CharField(max_length=100)
#     document_number = models.CharField(max_length=100)
#     pay_to = models.ForeignKey(EmployeeMaintenance, verbose_name="Pay To", on_delete=models.CASCADE)
#     company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
#     department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
#     project = models.ForeignKey(ProjectMaintenance, verbose_name="Project", on_delete=models.CASCADE)
#     submit_date = models.DateField()
#     subject = models.CharField(max_length=250)
#     reference = models.CharField(max_length=100)

#     class Meta:
#         verbose_name = 'Advance Refund'
#         verbose_name_plural = 'Advance Refunds'

#     def __str__(self):
#         return self.document_number
        
class ReimbursementRequest(models.Model):
    drawer = models.ForeignKey(DrawerMaintenance, verbose_name="Drawer",blank=True,null=True,on_delete=models.CASCADE)
    request_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    submit_date = models.DateField(default=datetime.date.today)
    submit_by = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    approval = models.ForeignKey(ApprovalItem, verbose_name="Approval", on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=301)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance,blank=True,null=True,on_delete=models.CASCADE)
    document_number = models.CharField(max_length=100,verbose_name="Document No",blank=True, null=True)
    status = models.ForeignKey(StatusMaintenance,verbose_name="Status",blank=True,null=True,on_delete=models.CASCADE)
