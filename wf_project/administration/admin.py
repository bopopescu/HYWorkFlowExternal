from django.contrib import admin
from .models import WorkflowPattern
from .models import WorkflowInstance
from .models import ProjectMaintenance
from .models import StatusMaintenance
from .models import DepartmentMaintenance
from .models import DocumentTypeMaintenance
from .models import CompanyMaintenance
from .models import CompanyContactDetail
from .models import CompanyAddressDetail
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
from .models import VendorCategoryMaintenance
from .models import VendorMasterData
from .models import VendorContactDetail
from .models import VendorAddressDetail
from .models import SystemFlagMaintenance
from .models import EmployeePositionMaintenance
from .models import BranchMaintenance
from .models import CountryMaintenance
from .models import StateMaintenance
from .models import EmployeeBranchMaintenance
from .models import EmployeeDepartmentMaintenance
from .models import EmployeeGroupMaintenance
from .models import EmployeeProjectMaintenance
from .models import EmployeeCompanyMaintenance
from .models import RegionMaintenance
from .models import TaxMaintenance
from datetime import datetime
from .models import DrawerMaintenance
from .models import DrawerUserMaintenance
from .models import TransactiontypeMaintenance
from .models import PaymentmodeMaintenance
from .models import MemoTemplateMaintenance
from .models import UOMMaintenance
from .models import StaffemploymentTypeMaintenance
from .models import StaffPositionTitleMaintenance
from .models import StaffPositionGradeMaintenance
from .models import UtiliyAccountTypeMaintenance
from .models import OTRateMaintenance
from .models import HolidayEventMaintenance
from .models import HRPlatformMaintenance
from .models import UtiliyGroupMaintenance


admin.site.register(WorkflowPattern)
admin.site.register(WorkflowInstance)

class ProjectMaintenanceScreen(admin.ModelAdmin):
    list_display = ('project_code', 'company', 'project_name', 'phase_name', 'sub_phase_name')
    search_fields = ('company__company_name', 'company__short_name', 'project_code', 'project_name', 'phase_name', 'sub_phase_name', )
    fieldsets = [
        (None, {'fields': ['company', 'project_code', 'project_name', 'phase_name', 'sub_phase_name', 'effect_start_date', 'effect_end_date']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(ProjectMaintenance, ProjectMaintenanceScreen)

class StatusMaintenanceScreen(admin.ModelAdmin):
    list_display = ('status_code', 'status_name', 'document_type', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('status_code', 'status_name', 'document_type__document_type_name')
    fieldsets = [
        (None, {'fields': ['document_type', 'status_code', 'status_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(StatusMaintenance, StatusMaintenanceScreen)

class StaffemploymentTypeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employment_type_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('employment_type_name', )
    fieldsets = [
        (None, {'fields': ['employment_type_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(StaffemploymentTypeMaintenance, StaffemploymentTypeMaintenanceScreen)

class StaffPositionTitleMaintenanceScreen(admin.ModelAdmin):
    list_display = ('position_title_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('position_title_name', )
    fieldsets = [
        (None, {'fields': ['position_title_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(StaffPositionTitleMaintenance, StaffPositionTitleMaintenanceScreen)

class StaffPositionGradeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('position_grade_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('position_grade_name', )
    fieldsets = [
        (None, {'fields': ['position_grade_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(StaffPositionGradeMaintenance, StaffPositionGradeMaintenanceScreen)

class DepartmentMaintenanceScreen(admin.ModelAdmin):
    list_display = ('department_name', 'is_active', 'access_accounts_dashboard',)
    list_filter = ('is_active', 'access_accounts_dashboard',)
    search_fields = ('department_name', )
    fieldsets = [
        (None, {'fields': ['department_name', 'is_active', 'access_accounts_dashboard']}),
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(DepartmentMaintenance, DepartmentMaintenanceScreen)

class DocumentTypeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('document_type_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('document_type_name', )
    fieldsets = [
        (None, {'fields': ['document_type_name', 'document_type_code', 'running_number', 'attachment_path', 'is_active']}),
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(DocumentTypeMaintenance, DocumentTypeMaintenanceScreen)

class CompanyContactInline(admin.StackedInline):
    model = CompanyContactDetail
    fieldsets = [
        (None, {'fields': [('personal_title', 'contact_person'), ('tel_no1', 'tel_no2'), ('mobile', 'email'), ('fax', 'ic_or_passport_no'), ('position', 'dob')]}), 
    ]
    exclude = ['created_by', 'modified_by']
    extra = 0
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class CompanyAddressInline(admin.StackedInline):
    model = CompanyAddressDetail
    fieldsets = [
        (None, {'fields': ['address_name', 'address1', 'address2', 'address3', 'address4', ('address_zip', 'state', 'country')]}), 
    ]
    exclude = ['created_by', 'modified_by']
    extra = 0
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class CompanyMaintenanceScreen(admin.ModelAdmin):
    list_display = ('short_name', 'company_name', 'currency', 'region', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('short_name', 'company_name', 'currency__currency_name', 'currency__currency_code', )
    fieldsets = [
        (None, {'fields': ['branch', 'short_name', 'company_name', 'business_registration_no', 'tax_id_1', 'tax_id_2', 'is_active', 'currency', 'region']}), 
    ]
    exclude = ['created_by', 'modified_by']
    inlines = [CompanyContactInline, CompanyAddressInline]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(CompanyMaintenance, CompanyMaintenanceScreen)

class CurrencyMaintenanceScreen(admin.ModelAdmin):
    list_display = ('currency_name', 'is_active', )
    list_filter = ('is_active', )
    search_fields = ('currency_name', )
    fieldsets = [
        (None, {'fields': ['currency_name', 'alphabet', 'rate', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(CurrencyMaintenance, CurrencyMaintenanceScreen)

class EmployeeDepartmentInline(admin.StackedInline):
    model = EmployeeDepartmentMaintenance
    exclude = ['created_by', 'modified_by']
    extra = 0
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)
     

class EmployeeBranchInline(admin.StackedInline):
    model = EmployeeBranchMaintenance
    exclude = ['created_by', 'modified_by']
    extra = 0
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class EmployeeCompanyInline(admin.StackedInline):
    model = EmployeeCompanyMaintenance
    fieldsets = [
        (None, {'fields': ['company']}), 
    ]
    extra = 0

class EmployeeProjectInline(admin.StackedInline):
    model = EmployeeProjectMaintenance
    exclude = ['created_by', 'modified_by']
    extra = 0

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class EmployeeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('employee_name', 'nick_name', 'position_id')
    list_filter = ('is_active', )
    search_fields = ('nick_name', 'employee_name', 'position_id__position_name')
    fieldsets = [
        (None, {'fields': ['employee_name', 'nick_name', 'gender', 'email', 'user', 'dob', 'position_id', 'employee_group', 'reporting_officer_id', 'employee_signature', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']
    inlines = [EmployeeDepartmentInline, EmployeeBranchInline, EmployeeProjectInline, EmployeeCompanyInline]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(EmployeeMaintenance, EmployeeMaintenanceScreen)
#admin.site.register(UserMaintenance)
class HolidayEventMaintenanceScreen(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'ot_rate', 'is_public_holiday', 'is_active')
    list_filter = ('is_active', 'is_public_holiday', )
    search_fields = ('event_name', 'event_date')
    fieldsets = [
        (None, {'fields': ['event_name', 'event_date', 'is_public_holiday', 'ot_rate', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(HolidayEventMaintenance, HolidayEventMaintenanceScreen)

class OTRateMaintenanceScreen(admin.ModelAdmin):
    list_display = ('ot_rate_name', 'ot_rate', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('ot_rate_name', 'ot_rate')
    fieldsets = [
        (None, {'fields': ['ot_rate_name', 'ot_rate', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(OTRateMaintenance, OTRateMaintenanceScreen)

class PaymentTermMaintenanceScreen(admin.ModelAdmin):
    list_display = ('description', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('description', )
    fieldsets = [
        (None, {'fields': ['description', 'days', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(PaymentTermMaintenance, PaymentTermMaintenanceScreen)

class LocationMaintenanceScreen(admin.ModelAdmin):
    list_display = ('loc_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('loc_name', )
    fieldsets = [
        (None, {'fields': ['loc_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(LocationMaintenance, LocationMaintenanceScreen)

class ItemClassesMaintenanceScreen(admin.ModelAdmin):
    list_display = ('item_class_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('item_class_name', )
    fieldsets = [
        (None, {'fields': ['item_class_name', 'is_active']}), 
    ]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(ItemClassesMaintenance, ItemClassesMaintenanceScreen)
   
class ItemGroupsMaintenanceScreen(admin.ModelAdmin):
    list_display = ('item_group_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('item_group_name', )
    fieldsets = [
        (None, {'fields': ['parent_id', 'item_group_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)


admin.site.register(ItemGroupsMaintenance, ItemGroupsMaintenanceScreen)

class WorkflowApprovalRuleGroupMaintenanceInline(admin.StackedInline):
    model = WorkflowApprovalRuleGroupMaintenance
    exclude = ['created_by', 'modified_by']
    extra = 0

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class WorkflowApprovalRuleScreen(admin.ModelAdmin):
    list_display = ('approval_level', 'approval_rule_name', 'ceo_approve', 'ceo_approve_overwrite', 'supervisor_approve', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('approval_level', 'approval_rule_name')
    fieldsets = [
        (None, {'fields': ['approval_level', 'approval_rule_name', ('document_amount_range', 'document_amount_range2'), 'ceo_approve', 'ceo_approve_overwrite', 'supervisor_approve', 'transaction_type', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']
    inlines = [WorkflowApprovalRuleGroupMaintenanceInline]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)
    
admin.site.register(WorkflowApprovalRule, WorkflowApprovalRuleScreen)

class WorkflowApprovalGroupScreen(admin.ModelAdmin):
    list_display = ('approval_group_name', 'no_of_person', 'user_group', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('approval_group_name', )
    fieldsets = [
        (None, {'fields': ['approval_group_name', 'no_of_person', 'user_group', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(WorkflowApprovalGroup, WorkflowApprovalGroupScreen)

# class WorkflowApprovalRuleGroupMaintenanceScreen(admin.ModelAdmin):
#     list_display = ('approval_rule', 'approval_group', )
#     list_filter = ('approval_rule', )
#     search_fields = ('approval_rule__approval_rule_name', 'approval_rule__approval_approval_level', 'approval_group__approval_group_name')
#     fieldsets = [
#         (None, {'fields': ['approval_rule', 'approval_group', 'next_condition']}), 
#     ]
#     exclude = ['created_by', 'modified_by']

#     def save_model(self, request, obj, form, change):
#         self.request = request
#         if not obj.pk:
#             # Only set added_by during the first save.
#             obj.created_by = self.request.user
#         else:
#             obj.modified_by = self.request.user
#         return super().save_model(request, obj, form, change)

# admin.site.register(WorkflowApprovalRuleGroupMaintenance, WorkflowApprovalRuleGroupMaintenanceScreen)

class VendorGroupMaintenanceScreen(admin.ModelAdmin):
    list_display = ('group_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('group_name', )
    fieldsets = [
        (None, {'fields': ['group_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(VendorGroupMaintenance, VendorGroupMaintenanceScreen)

class VendorContactInline(admin.StackedInline):
    model = VendorContactDetail
    fieldsets = [
        (None, {'fields': [('personal_title', 'contact_person'), ('tel_no1', 'tel_no2'), ('mobile', 'email'), ('fax', 'ic_or_passport_no'), ('position', 'dob')]}), 
    ]
    exclude = ['created_by', 'modified_by']
    extra = 0
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class VendorAddressInline(admin.StackedInline):
    model = VendorAddressDetail
    fieldsets = [
        (None, {'fields': ['address_name', 'address1', 'address2', 'address3', 'address4', ('address_zip', 'state', 'country')]}), 
    ]
    exclude = ['created_by', 'modified_by']
    extra = 0
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class VendorMasterDataScreen(admin.ModelAdmin):
    list_display = ('vendor_name', 'currency', 'vendor_group', 'is_company', 'is_active')
    list_filter = ('is_active', 'is_company')
    search_fields = ('vendor_name', )
    fieldsets = [
        (None, {'fields': ['vendor_name', 'currency', 'business_registration_no', 'tax_id_1', 'tax_id_2', 'vendor_group', 'vendor_category', 'is_company', 'is_active', 'is_qualified']}), 
    ]
    readonly_fields = ['is_qualified']
    exclude = ['created_by', 'modified_by']
    inlines = [VendorContactInline, VendorAddressInline]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(VendorMasterData, VendorMasterDataScreen)

class VendorCategoryMaintenceScreen(admin.ModelAdmin):
    list_display = ('vendor_category_name', 'is_active', )
    list_filter = ('is_active', )
    search_fields = ('vendor_category_name', )
    fieldsets = [
        (None, {'fields': ['vendor_category_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(VendorCategoryMaintenance, VendorCategoryMaintenceScreen)

class SystemFlagMaintenanceScreen(admin.ModelAdmin):
    list_display = ('flag_name', 'table_id')
    search_fields = ('flag_name', 'table_id')
    fieldsets = [
        (None, {'fields': ['flag_name', 'table_id']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(SystemFlagMaintenance, SystemFlagMaintenanceScreen)


class EmployeePositionMaintenanceScreen(admin.ModelAdmin):
    list_display = ('position_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('position_name', )
    fieldsets = [
        (None, {'fields': ['position_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

    

admin.site.register(EmployeePositionMaintenance, EmployeePositionMaintenanceScreen)

class BranchMaintenanceScreen(admin.ModelAdmin):
    list_display = ('branch_name', 'is_active' )
    list_filter = ('is_active', )
    search_fields = ('branch_name', )
    fieldsets = [
        (None, {'fields': ['branch_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(BranchMaintenance, BranchMaintenanceScreen)

class CountryMaintenanceScreen(admin.ModelAdmin):
    list_display = ('country_name', 'is_active', )
    list_filter = ('is_active', )
    search_fields = ('country_name', )
    fieldsets = [
        (None, {'fields': ['country_name', 'currency', 'alpha_2', 'alpha_3', 'iso3166_2', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(CountryMaintenance, CountryMaintenanceScreen)

class StateMaintenanceScreen(admin.ModelAdmin):
    list_display = ('state_name', 'capital', 'country', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('country__country_name', 'state_name', 'capital', )
    fieldsets = [
        (None, {'fields': ['state_name', 'capital', 'country', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(StateMaintenance, StateMaintenanceScreen)

# class EmployeeBranchMaintenanceScreen(admin.ModelAdmin):
#     list_display = ('employee', 'branch')
#     search_fields = ('employee__employee_name', 'employee__nick_name' , 'branch__branch_name', 'branch__branch_code')
#     fieldsets = [
#         (None, {'fields': ['employee', 'branch']}), 
#     ]
#     exclude = ['created_by', 'modified_by']

#     def save_model(self, request, obj, form, change):
#         self.request = request
#         if not obj.pk:
#             # Only set added_by during the first save.
#             obj.created_by = self.request.user
#         else:
#             obj.modified_by = self.request.user
#         return super().save_model(request, obj, form, change)

# admin.site.register(EmployeeBranchMaintenance, EmployeeBranchMaintenanceScreen)

# class EmployeeDepartmentMaintenanceScreen(admin.ModelAdmin):
#     list_display = ('employee', 'department')
#     search_fields = ('employee__employee_name', 'employee__nick_name' , 'department__department_name')
#     fieldsets = [
#         (None, {'fields': ['employee', 'department']}), 
#     ]
#     exclude = ['created_by', 'modified_by']

#     def save_model(self, request, obj, form, change):
#         self.request = request
#         if not obj.pk:
#             # Only set added_by during the first save.
#             obj.created_by = self.request.user
#         else:
#             obj.modified_by = self.request.user
#         return super().save_model(request, obj, form, change)

# admin.site.register(EmployeeDepartmentMaintenance, EmployeeDepartmentMaintenanceScreen)

class EmployeeGroupMaintenanceScreen(admin.ModelAdmin):
    list_display = ('group_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('group_name', )
    fieldsets = [
        (None, {'fields': ['group_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(EmployeeGroupMaintenance, EmployeeGroupMaintenanceScreen)

# class EmployeeProjectMaintenanceScreen(admin.ModelAdmin):
#     list_display = ('employee', 'project')
#     search_fields = ('employee__employee_name', 'employee__nick_name' , 'project__project_code', 'project__project_name', 'project__phase_name', 'project__sub_phase_name')
#     fieldsets = [
#         (None, {'fields': ['employee', 'project']}), 
#     ]
#     exclude = ['created_by', 'modified_by']

#     def save_model(self, request, obj, form, change):
#         self.request = request
#         if not obj.pk:
#             # Only set added_by during the first save.
#             obj.created_by = self.request.user
#         else:
#             obj.modified_by = self.request.user
#         return super().save_model(request, obj, form, change)

# admin.site.register(EmployeeProjectMaintenance, EmployeeProjectMaintenanceScreen)

class RegionMaintenanceScreen(admin.ModelAdmin):
    list_display = ('region_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('region_name', )
    fieldsets = [
        (None, {'fields': ['region_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(RegionMaintenance, RegionMaintenanceScreen)

class TaxMaintenanceScreen(admin.ModelAdmin):
    list_display = ('tax_code', 'tax_name', 'rate', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('tax_code', 'tax_name', 'rate', )
    fieldsets = [
        (None, {'fields': ['tax_code', 'tax_name', 'rate', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(TaxMaintenance, TaxMaintenanceScreen)

class DrawerUserInline(admin.StackedInline):
    model = DrawerUserMaintenance
    fieldsets = [
        (None, {'fields': ['user']}), 
    ]
    extra = 0

class DrawerMaintenanceScreen(admin.ModelAdmin):
    list_display = ('drawer_name', 'open_year', 'open_month', 'drawer_status')
    list_filter = ('drawer_status', )
    search_fields = ('drawer_name', )
    fieldsets = [
        (None, {'fields': ['drawer_name', 'branch', 'open_year', 'open_month', 'limit', 'drawer_status']}), 
    ]
    exclude = ['created_by', 'modified_by']
    inlines = [DrawerUserInline]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(DrawerMaintenance, DrawerMaintenanceScreen)

class PaymentmodeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('payment_mode_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('payment_mode_name', )
    fieldsets = [
        (None, {'fields': ['payment_mode_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(PaymentmodeMaintenance, PaymentmodeMaintenanceScreen)

class TransactiontypeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('transaction_type_name', 'document_type', 'is_active', 'is_utility', 'send_to_account')
    list_filter = ('is_active', 'is_utility', 'send_to_account')
    search_fields = ('transaction_type_name', 'document_type__document_type_name')
    fieldsets = [
        (None, {'fields': ['transaction_type_name', 'document_type', 'is_active', 'is_utility', 'send_to_account']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(TransactiontypeMaintenance, TransactiontypeMaintenanceScreen)

class MemoTemplateMaintenanceScreen(admin.ModelAdmin):
    list_display = ('memo_template_name', 'template_htmldesign', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('memo_template_name', 'template_htmldesign')
    fieldsets = [
        (None, {'fields': ['memo_template_name', 'template_htmldesign', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(MemoTemplateMaintenance, MemoTemplateMaintenanceScreen)

class UOMMaintenanceScreen(admin.ModelAdmin):
    list_display = ('uom_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('uom_name', )
    fieldsets = [
        (None, {'fields': ['uom_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(UOMMaintenance, UOMMaintenanceScreen)

class UtilityAccountInline(admin.StackedInline):
    model = UtiliyAccountTypeMaintenance
    fieldsets = [
        (None, {'fields': ['account_short_name', 'account_name', 'account_no', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']
    extra = 0
    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            #Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
           obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

class UtilityGroupTypeMaintenanceScreen(admin.ModelAdmin):
    list_display = ('account_group_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('account_group_name', )
    fieldsets = [
        (None, {'fields': ['account_group_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']
    inlines = [UtilityAccountInline]

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(UtiliyGroupMaintenance, UtilityGroupTypeMaintenanceScreen)

class HRPlatformMaintenanceScreen(admin.ModelAdmin):
    list_display = ('platform_name', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('platform_name', )
    fieldsets = [
        (None, {'fields': ['platform_name', 'is_active']}), 
    ]
    exclude = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        self.request = request
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = self.request.user
        else:
            obj.modified_by = self.request.user
        return super().save_model(request, obj, form, change)

admin.site.register(HRPlatformMaintenance, HRPlatformMaintenanceScreen)

# class UtiliyAccountTypeMaintenanceScreen(admin.ModelAdmin):
#     list_display = ('account_short_name', 'account_name', 'is_active')
#     list_filter = ('is_active', )
#     search_fields = ('account_short_name', 'account_name', )
#     fieldsets = [
#         (None, {'fields': ['account_short_name', 'account_name', 'account_no', 'is_active']}), 
#     ]
#     exclude = ['created_by', 'modified_by']

#     def save_model(self, request, obj, form, change):
#         self.request = request
#         if not obj.pk:
#             # Only set added_by during the first save.
#             obj.created_by = self.request.user
#         else:
#             obj.modified_by = self.request.user
#         return super().save_model(request, obj, form, change)

# admin.site.register(UtiliyAccountTypeMaintenance, UtiliyAccountTypeMaintenanceScreen)