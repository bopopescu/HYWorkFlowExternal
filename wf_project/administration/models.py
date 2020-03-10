from django.db import models
from django.contrib import admin

class BranchMaintenance(models.Model):
    branch_code = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.branch_code, self.branch_name)

class BranchMaintenanceScreen(admin.ModelAdmin):
    list_display = ('branch_code', 'branch_name','is_active' )
    search_fields = ('branch_code', 'branch_name',)

class CompanyMaintenance(models.Model):
    company_name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=250)        
    business_registration_no = models.CharField(max_length=30)
    tax_id_1 = models.CharField(max_length=100)
    tax_id_2 = models.CharField(max_length=100)
    is_active = models.BooleanField()
    currency = models.ForeignKey('CurrencyMaintenance', default=0, verbose_name="Currency",on_delete=models.CASCADE)
    region = models.ForeignKey('RegionMaintenance', default=0, verbose_name="Region",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()
    def __str__(self):
        return self.company_name

class CompanyMaintenanceScreen(admin.ModelAdmin):
    list_display = ('short_name', 'company_name', 'currency','region','is_active')
    list_filter = ('is_active',)
    search_fields = ('short_name', 'company_name','currency__currency_name','currency__currency_code',)

class CountryMaintenance(models.Model):
    country_code = models.CharField(max_length=3)
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
        return self.country_code

class CountryMaintenanceScreen(admin.ModelAdmin):
    list_display = ('country_code', 'country_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('country_code', 'country_name',)

class CurrencyMaintenance(models.Model):
    currency_code = models.CharField(max_length=100)
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

class CurrencyMaintenanceScreen(admin.ModelAdmin):
    list_display = ('currency_code', 'currency_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('currency_code', 'currency_name',)

class DepartmentMaintenance(models.Model):
    department_code = models.CharField(max_length=100)
    department_name = models.CharField(max_length=250)
    is_active = models.BooleanField()

    def __str__(self):
        return "%s - %s" % (self.department_code, self.department_name)

class DepartmentMaintenanceScreen(admin.ModelAdmin):
    list_display = ('department_code', 'department_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('department_code', 'department_name',)

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

class DocumentTypeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('document_type_code', 'document_type_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('document_type_code', 'document_type_name',)

class EmployeeBranchMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    branch = models.ForeignKey('BranchMaintenance', default=0, verbose_name="Branch",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

class EmployeeBranchMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'branch')
    search_fields = ('employee__employee_name','employee__nick_name' ,'branch__branch_name','branch__branch_code')

class EmployeeDepartmentMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    department = models.ForeignKey('DepartmentMaintenance', default=0, verbose_name="Department",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

class EmployeeDepartmentMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'department')
    search_fields = ('employee__employee_name','employee__nick_name' ,'department__department_name','department__department_code')

class EmployeeGroupMaintenance(models.Model):
    group_code = models.CharField(max_length=100)
    group_name = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.group_code, self.group_name)

class EmployeeGroupMaintenanceScreen(admin.ModelAdmin):
    list_display = ('group_code', 'group_name',)
    search_fields = ('group_code', 'group_name',)

class EmployeeMaintenance(models.Model):
    gender_option = [('M','MALE'),('F','FEMALE')]
    employee_name = models.CharField(max_length=250)
    nick_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=25,choices=gender_option)
    dob = models.DateField(verbose_name="Date of Birth")
    position_id = models.ForeignKey('EmployeePositionMaintenance',default=0,verbose_name="Position",on_delete=models.CASCADE)
    reporting_officer_id = models.ForeignKey('self',default=0,verbose_name="Reporting Officer",on_delete=models.CASCADE)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)

    def __str__(self):
        return self.employee_name

class EmployeeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('nick_name', 'employee_name','position_id')
    list_filter = ('is_active',)
    search_fields = ('nick_name', 'employee_name','position_id__position_name')

class EmployeeProjectMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    project = models.ForeignKey('ProjectMaintenance', default=0, verbose_name="Project",on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

class EmployeeProjectMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'project')
    search_fields = ('employee__employee_name','employee__nick_name' ,'project__project_code','project__project_name','project__phase_name','project__sub_phase_name')

class EmployeePositionMaintenance(models.Model):
    position_name = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.position_name

class EmployeePositionMaintenanceScreen(admin.ModelAdmin):
    list_display = ('position_name',)
    search_fields = ('position_name',)

class ItemClassesMaintenance(models.Model):
    item_class_code = models.CharField(max_length=100)
    item_class_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.item_class_code, self.item_class_name)

class ItemClassesMaintenanceScreen(admin.ModelAdmin):
    list_display = ('item_class_code', 'item_class_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('item_class_code', 'item_class_name',)

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
        return "%s - %s" % (self.item_group_code, self.item_group_name)

class ItemGroupsMaintenanceScreen(admin.ModelAdmin):
    list_display = ('item_group_code', 'item_group_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('item_group_code', 'item_group_name',)

class LocationMaintenance(models.Model):
    loc_code = models.CharField(max_length=100)
    loc_name = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.loc_code, self.loc_name)

class LocationMaintenanceScreen(admin.ModelAdmin):
    list_display = ('loc_code', 'loc_name')
    search_fields = ('loc_code', 'loc_name',)

class PaymentTermMaintenance(models.Model):
    term_code = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    days = models.IntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.description

class PaymentTermMaintenanceScreen(admin.ModelAdmin):
    list_display = ('term_code', 'description','is_active')
    list_filter = ('is_active',)
    search_fields = ('term_code', 'description',)

class ProjectMaintenance(models.Model):
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    project_code = models.CharField(max_length=100)
    project_name = models.CharField(max_length=250)
    phase_name = models.CharField(max_length=250)
    sub_phase_name = models.CharField(max_length=250)
    effect_start_date = models.DateField()
    effect_end_date = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.project_code, self.project_name)

class ProjectMaintenanceScreen(admin.ModelAdmin):
    list_display = ('project_code','company','project_name','phase_name','sub_phase_name')
    search_fields = ('company__company_name', 'company__short_name','project_code','project_name','phase_name','sub_phase_name',)

class RegionMaintenance(models.Model):
    region_code = models.CharField(max_length=100)
    region_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.region_code, self.region_name)

class RegionMaintenanceScreen(admin.ModelAdmin):
    list_display = ('region_code', 'region_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('region_code', 'region_name',)

class StatusMaintenance(models.Model):
    document_type = models.ForeignKey('DocumentTypeMaintenance', default=0, verbose_name="Document Type",on_delete=models.CASCADE)
    status_code = models.IntegerField()
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return "%s - %s" % (self.status_code, self.status_name)

class StatusMaintenanceScreen(admin.ModelAdmin):
    list_display = ('status_code','status_name','document_type')
    search_fields = ('status_code', 'status_name','document_type__document_type_name')

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

class WorkflowApprovalRuleScreen(admin.ModelAdmin):
    list_display = ('ApprovalLevel', 'Description','Condition')
    search_fields = ('ApprovalLevel', 'Description','Condition')

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
    group_code = models.CharField(max_length=15)
    group_name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)

    def __str__(self):
        return self.group_name

class VendorGroupMaintenanceScreen(admin.ModelAdmin):
    list_display = ('group_code', 'group_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('group_code', 'group_name')

class SystemFlagMaintenance(models.Model):
    flag_name= models.CharField(max_length=250)
    table_id = models.IntegerField()
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)

    def __str__(self):
        return self.flag_name

class SystemFlagMaintenanceScreen(admin.ModelAdmin):
    list_display = ('flag_name', 'table_id')
    search_fields = ('flag_name', 'table_id')

class TaxMaintenance(models.Model):
    tax_code= models.CharField(max_length=100)
    tax_name= models.CharField(max_length=250)
    rate= models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.tax_name

class TaxMaintenanceScreen(admin.ModelAdmin):
    list_display = ('tax_code', 'tax_name', 'rate','is_active')
    list_filter = ('is_active',)
    search_fields = ('tax_code', 'tax_name','rate',)
