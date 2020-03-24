from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator
from datetime import datetime
from django.contrib.auth.models import User

class BranchMaintenance(models.Model):
    branch_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='branchcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='branchmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.branch_name

class CompanyMaintenance(models.Model):
    company_name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=250)        
    business_registration_no = models.CharField(max_length=30)
    tax_id_1 = models.CharField(max_length=100)
    tax_id_2 = models.CharField(max_length=100)
    is_active = models.BooleanField()
    currency = models.ForeignKey('CurrencyMaintenance', default=0, verbose_name="Currency",on_delete=models.CASCADE)
    region = models.ForeignKey('RegionMaintenance', default=0, verbose_name="Region",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='companycreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='companymodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.company_name

class CountryMaintenance(models.Model):
    country_name = models.CharField(max_length=250)
    alpha_2 = models.CharField(max_length=2)
    alpha_3 = models.CharField(max_length=3)
    iso3166_2 = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='countrycreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='countrymodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country_name


class CurrencyMaintenance(models.Model):
    currency_name = models.CharField(max_length=250)
    alphabet = models.CharField(max_length=100)
    country = models.ForeignKey('CountryMaintenance', default=0, verbose_name="Country",on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='currencycreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='currencymodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency_name

class DepartmentMaintenance(models.Model):
    department_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='departmentcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='departmentmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name

class DocumentTypeMaintenance(models.Model):
    document_type_name = models.CharField(max_length=250)
    attachment_path = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='documenttypecreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='documenttypemodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document_type_name

class EmployeeBranchMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    branch = models.ForeignKey('BranchMaintenance', default=0, verbose_name="Branch",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='employeebranchcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='employeebranchmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

class EmployeeDepartmentMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    department = models.ForeignKey('DepartmentMaintenance', default=0, verbose_name="Department",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='employeedepartmentcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='employeedepartmentmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

class EmployeeDepartmentMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'department')
    search_fields = ('employee__employee_name','employee__nick_name' ,'department__department_name','department__department_code')

class EmployeeGroupMaintenance(models.Model):
    group_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='employeegroupcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='employeegroupmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

class EmployeeMaintenance(models.Model):
    gender_option = [('M','MALE'),('F','FEMALE')]
    employee_name = models.CharField(max_length=250)
    nick_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=25,choices=gender_option)
    dob = models.DateField(verbose_name="Date of Birth")
    position_id = models.ForeignKey('EmployeePositionMaintenance',default=0,verbose_name="Position",on_delete=models.CASCADE)
    employee_group = models.ForeignKey('EmployeeGroupMaintenance',default=0,verbose_name="Employee Group",on_delete=models.CASCADE)
    reporting_officer_id = models.ForeignKey('self',default=0,verbose_name="Reporting Officer",null=True, blank=True,on_delete=models.CASCADE)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='employeecreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='employeemodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee_name


class EmployeeProjectMaintenance(models.Model):
    employee = models.ForeignKey('EmployeeMaintenance', default=0, verbose_name="Employee",on_delete=models.CASCADE)
    project = models.ForeignKey('ProjectMaintenance', default=0, verbose_name="Project",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='employeeprojectcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='employeeprojectmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

class EmployeeProjectMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'project')
    search_fields = ('employee__employee_name','employee__nick_name' ,'project__project_code','project__project_name','project__phase_name','project__sub_phase_name')

class EmployeePositionMaintenance(models.Model):
    position_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='employeepositioncreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='employeepositionmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_name

class ItemClassesMaintenance(models.Model):
    item_class_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='itemclassescreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='itemclassesmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_class_name

class ItemGroupsMaintenance(models.Model):
    parent_id = models.ForeignKey('self', verbose_name="Parent Group", on_delete=models.CASCADE,  blank=True, null=True)
    item_group_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='created_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='modified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_group_name
    
class LocationMaintenance(models.Model):
    loc_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='locationcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='locationmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loc_name

class PaymentTermMaintenance(models.Model):
    description = models.CharField(max_length=250)
    days = models.IntegerField()
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='paymenttermcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='paymenttermmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

class ProjectMaintenance(models.Model):
    company = models.ForeignKey('CompanyMaintenance', default=0, verbose_name="Company Name",on_delete=models.CASCADE)
    project_code = models.CharField(max_length=100)
    project_name = models.CharField(max_length=250)
    phase_name = models.CharField(max_length=250)
    sub_phase_name = models.CharField(max_length=250)
    effect_start_date = models.DateField(default=datetime.now)
    effect_end_date = models.DateField(default=datetime.now)
    created_by = models.ForeignKey(User, related_name='projectcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='projectmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

class RegionMaintenance(models.Model):
    region_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='regioncreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='regionmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.region_name

class StatusMaintenance(models.Model):
    document_type = models.ForeignKey('DocumentTypeMaintenance', default=0, verbose_name="Document Type",on_delete=models.CASCADE)
    status_code = models.IntegerField()
    status_name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='statuscreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='statusmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

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
    approval_level = models.IntegerField(unique=True,verbose_name="Approval Level")
    approval_rule_name = models.CharField(max_length=250)
    document_amount_range= models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Document Amount Range From (RM)")
    document_amount_range2= models.DecimalField(max_digits=10, decimal_places=2,verbose_name="To")
    supervisor_approve = models.BooleanField(verbose_name="Supervisor Approve?")
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='workflowapprovalrulecreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='workflowapprovalrulemodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Level %s - %s" % (self.approval_level, self.approval_rule_name)    

class WorkflowApprovalGroup(models.Model):
    approval_group_name = models.CharField(max_length=250)
    no_of_person = models.PositiveIntegerField(verbose_name="No of person",validators=[MinValueValidator(0)]) 
    user_group = models.ForeignKey('EmployeeGroupMaintenance',default=0,verbose_name="User Group",on_delete=models.CASCADE)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='workflowapprovalgroupcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='workflowapprovalgroupmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.approval_group_name


class WorkflowApprovalRuleGroupMaintenance(models.Model):
    condition_option = [('And','And'),('Or','Or')]
    approval_rule = models.ForeignKey('WorkflowApprovalRule',default=0,verbose_name="Approval Level",on_delete=models.CASCADE)
    approval_group = models.ForeignKey('WorkflowApprovalGroup',default=0,verbose_name="Approval Group",on_delete=models.CASCADE)
    next_condition = models.CharField(max_length=15,choices=condition_option,null=True)
    created_by = models.ForeignKey(User, related_name='workflowapprovalrulegroupcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='workflowapprovalrulegroupmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

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
    created_by = models.ForeignKey(User, related_name='vendorgroupcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='vendorgroupmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

class VendorMasterData(models.Model):
    vendor_name = models.CharField(max_length=100)
    currency = models.ForeignKey('CurrencyMaintenance', default=0, verbose_name="Currency",on_delete=models.CASCADE)
    business_registration_no = models.CharField(max_length=30)
    tax_id_1 = models.CharField(max_length=100)
    tax_id_2 = models.CharField(max_length=100,blank=True,null=True)
    vendor_group = models.ForeignKey('VendorGroupMaintenance', default=0, verbose_name="Vendor Group",on_delete=models.CASCADE)
    is_company = models.BooleanField()
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='vendorcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='vendormodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
class SystemFlagMaintenance(models.Model):
    flag_name= models.CharField(max_length=250)
    table_id = models.IntegerField()
    created_by = models.ForeignKey(User, related_name='systemflagcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='systemflagmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.flag_name

class TaxMaintenance(models.Model):
    tax_code= models.CharField(max_length=100)
    tax_name= models.CharField(max_length=250)
    rate= models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='taxcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='taxmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tax_name

class DrawerMaintenance(models.Model):
    status_option = [('O','Open'),('C','Closed')]
    month_option = [('1','January'),('2','February'),('3','March'),('4','April'),
                    ('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),
                    ('10','October'),('11','November'),('12','December')]
    drawer_name = models.CharField(max_length=250)
    branch = models.ForeignKey('BranchMaintenance', default=0,on_delete=models.CASCADE)
    open_year = models.PositiveIntegerField()
    open_month = models.CharField(choices=month_option,max_length=20)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    drawer_status = models.CharField(max_length=10,choices=status_option)
    created_by = models.ForeignKey(User, related_name='drawercreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='drawermodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.drawer_name

class TransactiontypeMaintenance(models.Model):
    transaction_type_name = models.CharField(max_length=250)
    document_type = models.ForeignKey('DocumentTypeMaintenance', default=0, verbose_name="Document Type",on_delete=models.CASCADE)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='transactiontypecreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='transactiontypemodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_type_name

class PaymentmodeMaintenance(models.Model):
    payment_mode_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='paymentmodecreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='paymentmodemodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_mode_name

class MemoTemplateMaintenance(models.Model):
    memo_template_name = models.CharField(max_length=250,verbose_name='Memo Template Name')
    template_htmldesign = models.CharField(max_length=4000,verbose_name='HTML design')
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='memotemplatecreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='memotemplatemodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.memo_template_name
