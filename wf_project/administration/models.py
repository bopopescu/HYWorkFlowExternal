from django.db import models

class WorkflowPattern(models.Model):
    pattern_code = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField()

    def __str__(self):
        return self.pattern_code

class WorkflowInstance(models.Model):
    template_code = models.CharField(max_length=100)
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    document_type = models.ForeignKey('DocumentTypeMaintenance', default=0, verbose_name="Document Type",on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=100)
    ceo_required = models.BooleanField()

    def __str__(self):
        return self.template_code

class WorkflowApprovalRule(models.Model):
    ApprovalLevel = models.IntegerField(unique=True,verbose_name="Approval Level")
    Description = models.CharField(max_length=250)
    Condition = models.CharField(max_length=250)

    def __str__(self):
        return "Level %s - %s" % (self.ApprovalLevel, self.Description)

class ProjectMaintenance(models.Model):
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    project_code = models.CharField(max_length=100)
    project_name = models.CharField(max_length=250)
    phase_name = models.CharField(max_length=250)
    sub_phase_name = models.CharField(max_length=250)
    effect_start_date = models.DateField()
    effect_end_date = models.DateField()

    def __str__(self):
        return self.project_code

class StatusMaintenance(models.Model):
    document_type = models.ForeignKey('DocumentTypeMaintenance', default=0, verbose_name="Document Type",on_delete=models.CASCADE)
    status_code = models.IntegerField()
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return self.status_code

class DepartmentMaintenance(models.Model):
    department_code = models.CharField(max_length=100)
    department_name = models.CharField(max_length=250)
    is_active = models.BooleanField()

    def __str__(self):
        return self.department_code

class CompanyMaintenance(models.Model):
    company_code = models.CharField(max_length=100)
    short_name = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    currency = models.ForeignKey('CurrencyMaintenance', default=0, verbose_name="Currency",on_delete=models.CASCADE)
    business_registration_no = models.CharField(max_length=100)
    tax_registration_no = models.CharField(max_length=100)
    tax_registration_no_2 = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class EmployeeMaintenance(models.Model):
    gender_option = [('M','MALE'),('F','FEMALE')]
    employee_code = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=250)
    nick_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=25,choices=gender_option)
    date_of_birth = models.DateField()
    tax_registration_no_2 = models.CharField(max_length=100)
    position = models.CharField(max_length=250)
    email = models.CharField(max_length=250)

    def __str__(self):
        return self.employee_code

class UserMaintenance(models.Model):
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    user_code = models.CharField(max_length=100)
    user_name = models.CharField(max_length=250)
    user_group = models.CharField(max_length=250)
    signature = models.FileField()

    def __str__(self):
        return self.user_code

class PaymentTermMaintenance(models.Model):
    term_code = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    days = models.IntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.term_code

class LocationMaintenance(models.Model):
    loc_code = models.CharField(max_length=100)
    loc_name = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.loc_code

class ItemClassesMaintenance(models.Model):
    item_class_code = models.CharField(max_length=100)
    item_class_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.item_class_code

class ItemGroupsMaintenance(models.Model):
    parent_id = models.ForeignKey('self', default=0, verbose_name="Parent Group", on_delete=models.CASCADE)
    item_group_code = models.CharField(max_length=100)
    item_group_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.item_group_code

class DocumentTypeMaintenance(models.Model):
    document_type_code = models.CharField(max_length=100)
    document_type_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.document_type_code, self.document_type_name)

class CurrencyMaintenance(models.Model):
    currency_code = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=250)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.currency_code


