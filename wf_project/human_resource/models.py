from django.db import models
from administration.models import EmployeeMaintenance
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import StaffPositionTitleMaintenance
from administration.models import StaffHireTypeMaintenance
from django.contrib.auth.models import User

class StaffRecruitmentRequest(models.Model):
    position_title = models.ForeignKey(StaffPositionTitleMaintenance, verbose_name="Position Title", on_delete=models.CASCADE)
    revision = models.IntegerField()
    document_number = models.CharField(max_length=100,verbose_name="Document No.")
    reporting_to = models.ForeignKey(EmployeeMaintenance, verbose_name="Reporting To", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
    budgeted = models.BooleanField()
    status = models.CharField(max_length=1)
    hire_type = models.ForeignKey(StaffHireTypeMaintenance, verbose_name="Hire Type", on_delete=models.CASCADE)
    request_date = models.DateField(null=True, blank=True)
    no_of_pax = models.IntegerField()
    month_to_be_filled = models.IntegerField() 
    subject = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, related_name='staffrecruitmentcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='staffrecruitmentmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Staff Recruitment Request'
        verbose_name_plural = 'Staff Recruitment Requests'

    def __str__(self):
        return self.subject

class StaffJobRequirement(models.Model):
    staff_recruiment_id = models.ForeignKey('StaffRecruitmentRequest', on_delete=models.CASCADE)
    requirement_description = models.CharField(max_length=250)

    def __str__(self):
        return self.requirement_description

class StaffJobResponsibilities(models.Model):
    staff_recruiment_id = models.ForeignKey('StaffRecruitmentRequest', on_delete=models.CASCADE)
    reponsible_description = models.CharField(max_length=250)

    def __str__(self):
        return self.reponsible_description

