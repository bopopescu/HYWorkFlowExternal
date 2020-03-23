from django.contrib import admin
from .models import WorkflowPattern
from .models import WorkflowInstance
from .models import ProjectMaintenance
from .models import StatusMaintenance
from .models import DepartmentMaintenance
from .models import DocumentTypeMaintenance
from .models import CompanyMaintenance
from .models import CurrencyMaintenance
from .models import EmployeeMaintenance
from .models import UserMaintenance
from .models import PaymentTermMaintenance
from .models import LocationMaintenance
from .models import ItemClassesMaintenance
from .models import ItemGroupsMaintenance
from .models import WorkflowApprovalRule
from .models import WorkflowApprovalGroup
from .models import WorkflowApprovalRuleGroupMaintenance
from .models import VendorGroupMaintenance
from .models import VendorMasterData
from .models import SystemFlagMaintenance
from .models import EmployeePositionMaintenance
from .models import BranchMaintenance
from .models import CountryMaintenance
from .models import EmployeeBranchMaintenance
from .models import EmployeeDepartmentMaintenance
from .models import EmployeeGroupMaintenance
from .models import EmployeeProjectMaintenance
from .models import RegionMaintenance
from .models import TaxMaintenance
from datetime import datetime
from .models import DrawerMaintenance

admin.site.register(WorkflowPattern)
admin.site.register(WorkflowInstance)

class ProjectMaintenanceScreen(admin.ModelAdmin):
    list_display = ('project_code','company','project_name','phase_name','sub_phase_name')
    search_fields = ('company__company_name', 'company__short_name','project_code','project_name','phase_name','sub_phase_name',)
    fieldsets = [
        (None, {'fields': ['company','project_code','project_name','phase_name','sub_phase_name','effect_start_date','effect_end_date']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(ProjectMaintenance,ProjectMaintenanceScreen)

class StatusMaintenanceScreen(admin.ModelAdmin):
    list_display = ('status_code','status_name','document_type','is_active')
    list_filter = ('is_active',)
    search_fields = ('status_code', 'status_name','document_type__document_type_name')
    fieldsets = [
        (None, {'fields': ['document_type','status_code','status_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(StatusMaintenance,StatusMaintenanceScreen)

class DepartmentMaintenanceScreen(admin.ModelAdmin):
    list_display = ('department_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('department_name',)
    fieldsets = [
        (None, {'fields': ['department_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(DepartmentMaintenance,DepartmentMaintenanceScreen)

class DocumentTypeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('document_type_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('document_type_name',)
    fieldsets = [
        (None, {'fields': ['document_type_name','attachment_path','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(DocumentTypeMaintenance,DocumentTypeMaintenanceScreen)

class CompanyMaintenanceScreen(admin.ModelAdmin):
    list_display = ('short_name', 'company_name', 'currency','region','is_active')
    list_filter = ('is_active',)
    search_fields = ('short_name', 'company_name','currency__currency_name','currency__currency_code',)
    fieldsets = [
        (None, {'fields': ['short_name','company_name','business_registration_no','tax_id_1','tax_id_2','is_active','currency','region']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(CompanyMaintenance,CompanyMaintenanceScreen)

class CurrencyMaintenanceScreen(admin.ModelAdmin):
    list_display = ('currency_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('currency_name',)
    fieldsets = [
        (None, {'fields': ['currency_name','alphabet','country','rate','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(CurrencyMaintenance,CurrencyMaintenanceScreen)

class EmployeeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('nick_name', 'employee_name','position_id')
    list_filter = ('is_active',)
    search_fields = ('nick_name', 'employee_name','position_id__position_name')
    fieldsets = [
        (None, {'fields': ['employee_name','nick_name','gender','dob','position_id','reporting_officer_id','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(EmployeeMaintenance,EmployeeMaintenanceScreen)
admin.site.register(UserMaintenance)

class PaymentTermMaintenanceScreen(admin.ModelAdmin):
    list_display = ('description','is_active')
    list_filter = ('is_active',)
    search_fields = ('description',)
    fieldsets = [
        (None, {'fields': ['description','days','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(PaymentTermMaintenance,PaymentTermMaintenanceScreen)

class LocationMaintenanceScreen(admin.ModelAdmin):
    list_display = ('loc_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('loc_name',)
    fieldsets = [
        (None, {'fields': ['loc_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(LocationMaintenance,LocationMaintenanceScreen)

class ItemClassesMaintenanceScreen(admin.ModelAdmin):
    list_display = ('item_class_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('item_class_name',)
    fieldsets = [
        (None, {'fields': ['item_class_name','is_active']}),
    ]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(ItemClassesMaintenance,ItemClassesMaintenanceScreen)
   
class ItemGroupsMaintenanceScreen(admin.ModelAdmin):
    list_display = ('item_group_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('item_group_name',)
    fieldsets = [
        (None, {'fields': ['parent_id', 'item_group_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)


admin.site.register(ItemGroupsMaintenance,ItemGroupsMaintenanceScreen)

class WorkflowApprovalRuleScreen(admin.ModelAdmin):
    list_display = ('approval_level', 'approval_rule_name','supervisor_approve','is_active')
    list_filter = ('is_active',)
    search_fields = ('approval_level', 'approval_rule_name')
    fieldsets = [
        (None, {'fields': ['approval_level', 'approval_rule_name', ('document_amount_range', 'document_amount_range2'),'supervisor_approve','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)
    
admin.site.register(WorkflowApprovalRule,WorkflowApprovalRuleScreen)

class WorkflowApprovalGroupScreen(admin.ModelAdmin):
    list_display = ('approval_group_name', 'no_of_person','user_group','is_active')
    list_filter = ('is_active',)
    search_fields = ('approval_group_name',)
    fieldsets = [
        (None, {'fields': ['approval_group_name', 'no_of_person','user_group','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(WorkflowApprovalGroup,WorkflowApprovalGroupScreen)

class WorkflowApprovalRuleGroupMaintenanceScreen(admin.ModelAdmin):
    list_display = ('approval_rule', 'approval_group',)
    list_filter = ('approval_rule',)
    search_fields = ('approval_rule__approval_rule_name','approval_rule__approval_approval_level','approval_group__approval_group_name')
    fieldsets = [
        (None, {'fields': ['approval_rule', 'approval_group','next_condition']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(WorkflowApprovalRuleGroupMaintenance,WorkflowApprovalRuleGroupMaintenanceScreen)

class VendorGroupMaintenanceScreen(admin.ModelAdmin):
    list_display = ('group_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('group_name',)
    fieldsets = [
        (None, {'fields': ['group_name', 'is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(VendorGroupMaintenance,VendorGroupMaintenanceScreen)

class VendorMasterDataScreen(admin.ModelAdmin):
    list_display = ('vendor_name','currency','vendor_group','is_company','is_active')
    list_filter = ('is_active','is_company')
    search_fields = ('vendor_name','vendor_group')
    fieldsets = [
        (None, {'fields': ['vendor_name', 'currency','business_registration_no','tax_id_1','tax_id_2','vendor_group','is_company','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(VendorMasterData,VendorMasterDataScreen)

class SystemFlagMaintenanceScreen(admin.ModelAdmin):
    list_display = ('flag_name', 'table_id')
    search_fields = ('flag_name', 'table_id')
    fieldsets = [
        (None, {'fields': ['flag_name', 'table_id']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(SystemFlagMaintenance,SystemFlagMaintenanceScreen)


class EmployeePositionMaintenanceScreen(admin.ModelAdmin):
    list_display = ('position_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('position_name',)
    fieldsets = [
        (None, {'fields': ['position_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

    

admin.site.register(EmployeePositionMaintenance,EmployeePositionMaintenanceScreen)

class BranchMaintenanceScreen(admin.ModelAdmin):
    list_display = ('branch_name','is_active' )
    list_filter = ('is_active',)
    search_fields = ('branch_name',)
    fieldsets = [
        (None, {'fields': ['branch_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(BranchMaintenance,BranchMaintenanceScreen)

class CountryMaintenanceScreen(admin.ModelAdmin):
    list_display = ('country_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('country_name',)
    fieldsets = [
        (None, {'fields': ['country_name','alpha_2','alpha_3','iso3166_2','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(CountryMaintenance,CountryMaintenanceScreen)

class EmployeeBranchMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'branch')
    search_fields = ('employee__employee_name','employee__nick_name' ,'branch__branch_name','branch__branch_code')
    fieldsets = [
        (None, {'fields': ['employee','branch']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(EmployeeBranchMaintenance,EmployeeBranchMaintenanceScreen)

class EmployeeDepartmentMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'department')
    search_fields = ('employee__employee_name','employee__nick_name' ,'department__department_name','department__department_code')
    fieldsets = [
        (None, {'fields': ['employee','department']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(EmployeeDepartmentMaintenance,EmployeeDepartmentMaintenanceScreen)

class EmployeeGroupMaintenanceScreen(admin.ModelAdmin):
    list_display = ('group_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('group_name',)
    fieldsets = [
        (None, {'fields': ['group_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(EmployeeGroupMaintenance,EmployeeGroupMaintenanceScreen)

class EmployeeProjectMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee', 'project')
    search_fields = ('employee__employee_name','employee__nick_name' ,'project__project_code','project__project_name','project__phase_name','project__sub_phase_name')
    fieldsets = [
        (None, {'fields': ['employee','project']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(EmployeeProjectMaintenance,EmployeeProjectMaintenanceScreen)

class RegionMaintenanceScreen(admin.ModelAdmin):
    list_display = ('region_name','is_active')
    list_filter = ('is_active',)
    search_fields = ('region_name',)
    fieldsets = [
        (None, {'fields': ['region_name','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(RegionMaintenance,RegionMaintenanceScreen)

class TaxMaintenanceScreen(admin.ModelAdmin):
    list_display = ('tax_code', 'tax_name', 'rate','is_active')
    list_filter = ('is_active',)
    search_fields = ('tax_code', 'tax_name','rate',)
    fieldsets = [
        (None, {'fields': ['tax_code','tax_name','rate','is_active']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(TaxMaintenance,TaxMaintenanceScreen)

class DrawerMaintenanceScreen(admin.ModelAdmin):
    list_display = ('drawer_name', 'open_year', 'open_month','drawer_status')
    list_filter = ('drawer_status',)
    search_fields = ('drawer_name',)
    fieldsets = [
        (None, {'fields': ['drawer_name','branch','open_year','open_month','limit','drawer_status']}),
    ]
    exclude = ['created_by','modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(DrawerMaintenance,DrawerMaintenanceScreen)
