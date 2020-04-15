from django.db import models
from administration.models import CompanyMaintenance,EmployeeMaintenance, EmployeePositionMaintenance, ProjectMaintenance
from administration.models import DepartmentMaintenance, TransactiontypeMaintenance
from administration.models import StatusMaintenance
import datetime
from django.contrib.auth.models import User
from approval.models import ApprovalItem

class StaffOT(models.Model):
    revision = models.IntegerField(default=0)
    document_number = models.CharField(max_length=100,verbose_name="Document No",blank=True, null=True)
    employee = models.ForeignKey(EmployeeMaintenance, verbose_name="Employee",blank=True,null=True, on_delete=models.CASCADE)
    employee_position = models.ForeignKey(EmployeePositionMaintenance,blank=True,null=True, verbose_name="Position", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company",blank=True,null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaintenance, verbose_name="Project",blank=True,null=True, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactiontypeMaintenance, verbose_name="Trans Type.",blank=True,null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department",blank=True,null=True, on_delete=models.CASCADE)
    approval = models.ForeignKey(ApprovalItem, verbose_name="Approval", on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(StatusMaintenance, verbose_name="Status",blank=True,null=True, on_delete=models.CASCADE)
    submit_date = models.DateField(default=datetime.date.today)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Staff OT'

    def __str__(self):
        return self.document_number

class StaffOTDetail(models.Model):
    staff_ot = models.ForeignKey('StaffOT', verbose_name="Staff OT",blank=True,null=True, on_delete=models.CASCADE)
    ot_date = models.DateField()
    ot_time_in = models.TimeField()
    ot_time_out = models.TimeField()
    total_ot_time = models.IntegerField()
    meal_allowance = models.BooleanField()
    is_holiday = models.BooleanField()
    ot_rate_per_hours = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=True)
    total_ot_rate = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    remark = models.CharField(max_length=200)
