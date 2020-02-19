from django.db import models

class WorkflowPattern(models.Model):
    pattern_code = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField()

class WorkflowInstance(models.Model):
    template_code = models.CharField(max_length=100)
    trans_type = models.CharField(max_length=100)
    ceo_required = models.BooleanField()

class ProjectMaintenance(models.Model):
    project_code = models.CharField(max_length=100)
    project_name = models.CharField(max_length=250)
    phase_name = models.CharField(max_length=250)
    sub_phase_name = models.CharField(max_length=250)
    effect_start_date = models.DateField()
    effect_end_date = models.DateField()

class StatusMaintenance(models.Model):
    status_code = models.IntegerField()
    status_name = models.CharField(max_length=100)

class DepartmentMaintenance(models.Model):
    department_code = models.CharField(max_length=100)
    department_name = models.CharField(max_length=250)
    is_active = models.BooleanField()

class CompanyMaintenance(models.Model):
    company_code = models.CharField(max_length=100)
    short_name = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    business_registration_no = models.CharField(max_length=100)
    tax_registration_no = models.CharField(max_length=100)
    tax_registration_no_2 = models.CharField(max_length=100)

class EmployeeMaintenance(models.Model):
    employee_code = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=250)
    nick_name = models.CharField(max_length=250)
    gender = models.BooleanField()
    date_of_birth = models.DateField()
    tax_registration_no_2 = models.CharField(max_length=100)
    position = models.CharField(max_length=250)
    email = models.CharField(max_length=250)

class UserMaintenance(models.Model):
    user_code = models.CharField(max_length=100)
    user_name = models.CharField(max_length=250)
    user_group = models.CharField(max_length=250)
    signature = models.FileField()

class PaymentTermMaintenance(models.Model):
    term_code = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    days = models.IntegerField()
    is_active = models.BooleanField()