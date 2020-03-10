from django.db import models

class BranchMaintenance(models.Model):
    branch_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.branch_name

class CompanyMaintenance(models.Model):
    company_name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=250)        
    business_registration_no = models.CharField(max_length=30)
    tax_id_1 = models.CharField(max_length=100)
    tax_id_2 = models.CharField(max_length=100)
    currency = models.ForeignKey('CurrencyMaintenance', default=0, verbose_name="Currency",on_delete=models.CASCADE)
    region = models.ForeignKey('RegionMaintenance', default=0, verbose_name="Region",on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name

class CountryMaintenance(models.Model):
    country_name = models.CharField(max_length=250)
    alpha_2 = models.CharField(max_length=2)
    alpha_3 = models.CharField(max_length=3)
    iso3166_2 = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.country_name

class CurrencyMaintenance(models.Model):
    currency_name = models.CharField(max_length=250)
    alphabet = models.CharField(max_length=100)
    country = models.ForeignKey('CountryMaintenance', default=0, verbose_name="Country",on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.currency_name

class DepartmentMaintenance(models.Model):
    department_name = models.CharField(max_length=250)
    is_active = models.BooleanField()

    def __str__(self):
        return self.department_name

class DocumentTypeMaintenance(models.Model):
    document_type_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.document_type_name

class EmployeeBranchMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    branch = models.ForeignKey('BranchMaintenance', default=0, verbose_name="Branch",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

class EmployeeDepartmentMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    department = models.ForeignKey('DepartmentMaintenance', default=0, verbose_name="Department",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

class EmployeeGroupMaintenance(models.Model):
    group_name = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.group_name

class EmployeeMaintenance(models.Model):
    gender_option = [('M','MALE'),('F','FEMALE')]
    
    employee_name = models.CharField(max_length=250)
    nick_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=25,choices=gender_option)
    dob = models.DateField(verbose_name="Date of Birth")
    position_id = models.ForeignKey('EmployeePositionMaintenance',default=0,verbose_name="Position",on_delete=models.CASCADE)
    reporting_officer_id = models.ForeignKey('self',default=0,verbose_name="Reporting Officer",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)

    def __str__(self):
        return self.employee_name

class EmployeeProjectMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    project = models.ForeignKey('ProjectMaintenance', default=0, verbose_name="Project",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

class EmployeePositionMaintenance(models.Model):
    position_name = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.position_name

class ItemClassesMaintenance(models.Model):
    item_class_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.item_class_name

class ItemGroupsMaintenance(models.Model):
    parent_id = models.ForeignKey('self', default=0, verbose_name="Parent Group", on_delete=models.CASCADE)
    item_group_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.item_group_name

class LocationMaintenance(models.Model):
    loc_name = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.loc_name

class PaymentTermMaintenance(models.Model):
    term_code = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    days = models.IntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.term_code

class ProjectMaintenance(models.Model):
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    project_code = models.CharField(max_length=100)
    project_name = models.CharField(max_length=250)
    phase_name = models.CharField(max_length=250)
    sub_phase_name = models.CharField(max_length=250)
    effect_start_date = models.DateField()
    effect_end_date = models.DateField()

    def __str__(self):
        return self.project_name

class RegionMaintenance(models.Model):
    region_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.region_name

class StatusMaintenance(models.Model):
    document_type = models.ForeignKey('DocumentTypeMaintenance', default=0, verbose_name="Document Type",on_delete=models.CASCADE)
    status_code = models.IntegerField()
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return "%s - %s" % (self.status_code, self.status_name)

class UserMaintenance(models.Model):
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    user_code = models.CharField(max_length=100)
    user_name = models.CharField(max_length=250)
    user_group = models.CharField(max_length=250)
    signature = models.FileField()

    def __str__(self):
        return self.user_code

class WorkflowApprovalRule(models.Model):
    ApprovalLevel = models.IntegerField(unique=True,verbose_name="Approval Level")
    Description = models.CharField(max_length=250)
    Condition = models.CharField(max_length=250)

    def __str__(self):
        return "Level %s - %s" % (self.ApprovalLevel, self.Description)

class WorkflowInstance(models.Model):
    template_code = models.CharField(max_length=100)
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    document_type = models.ForeignKey('DocumentTypeMaintenance', default=0, verbose_name="Document Type",on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=100)
    ceo_required = models.BooleanField()

    def __str__(self):
        return self.template_code

class WorkflowPattern(models.Model):
    pattern_code = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField()

    def __str__(self):
        return self.pattern_code

class VendorGroupMaintenance(models.Model):
    group_name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)

class VendorMasterData(models.Model):
    vendor_name = models.CharField(max_length=100)
    currency = models.ForeignKey('CurrencyMaintenance', default=0, verbose_name="Currency",on_delete=models.CASCADE)
    business_registration_no = models.CharField(max_length=30)
    tax_id_1 = models.CharField(max_length=100)
    tax_id_2 = models.CharField(max_length=100)
    vendor_group = models.ForeignKey('VendorGroupMaintenance', default=0, verbose_name="Vendor Group",on_delete=models.CASCADE)
    is_company = models.BooleanField()
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)

class SystemFlagMaintenance(models.Model):
    flag_name= models.CharField(max_length=250)
    table_id = models.IntegerField()
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)