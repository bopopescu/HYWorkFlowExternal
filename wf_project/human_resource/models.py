from django.db import models
from administration.models import EmployeeMaintenance
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import StaffPositionTitleMaintenance
from administration.models import StaffemploymentTypeMaintenance
from administration.models import StaffPositionGradeMaintenance
from administration.models import DocumentTypeMaintenance
from django.contrib.auth.models import User
from approval.models import ApprovalItem

def documenttype_document_number():
    document_type = DocumentTypeMaintenance.objects.filter(document_type_name="Staff Recruitment Request")[0]
    return '{0}-{1:05d}'.format(document_type.document_type_code,document_type.running_number)

class StaffRecruitmentRequest(models.Model):
    position_title = models.ForeignKey(StaffPositionTitleMaintenance, verbose_name="Position Title", on_delete=models.CASCADE)
    revision = models.IntegerField()
    position_grade = models.ForeignKey(StaffPositionGradeMaintenance, verbose_name="Position Grade", on_delete=models.CASCADE)
    document_number = models.CharField(max_length=100,verbose_name="Document No.", default=documenttype_document_number)
    reporting_to = models.ForeignKey(EmployeeMaintenance, verbose_name="Reporting To", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaintenance, verbose_name="Department", on_delete=models.CASCADE)
    budgeted = models.BooleanField()
    status = models.CharField(max_length=1,null=True, blank=True,default="D")
    employment_type = models.ForeignKey(StaffemploymentTypeMaintenance, verbose_name="Employment Type", on_delete=models.CASCADE)
    request_date = models.DateField(null=True, blank=True)
    submit_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    approval = models.ForeignKey(ApprovalItem, verbose_name="Approval", on_delete=models.CASCADE, blank=True, null=True) 
    no_of_pax = models.IntegerField()
    month_to_be_filled = models.IntegerField() 
    created_by = models.ForeignKey(User, related_name='staffrecruitmentcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='staffrecruitmentmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Staff Recruitment Request'
        verbose_name_plural = 'Staff Recruitment Requests'

    def __str__(self):
        return self.document_number

class StaffJobRequirement(models.Model):
    staff_recruitment = models.ForeignKey('StaffRecruitmentRequest',null=True, blank=True, on_delete=models.CASCADE)
    requirement_description = models.CharField(max_length=250,verbose_name="Requirement")

    def __str__(self):
        return self.requirement_description

class StaffJobResponsibilities(models.Model):
    staff_recruitment = models.ForeignKey('StaffRecruitmentRequest',null=True, blank=True, on_delete=models.CASCADE)
    responsible_description = models.CharField(max_length=250,verbose_name="Responsible")

    def __str__(self):
        return self.reponsible_description

