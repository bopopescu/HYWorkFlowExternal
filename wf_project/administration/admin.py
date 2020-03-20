from django.contrib import admin
from .models import WorkflowPattern
from .models import WorkflowInstance
from .models import ProjectMaintenance
from .models import ProjectMaintenanceScreen
from .models import StatusMaintenance
from .models import StatusMaintenanceScreen
from .models import DepartmentMaintenance
from .models import DepartmentMaintenanceScreen
from .models import DocumentTypeMaintenance
from .models import DocumentTypeMaintenanceScreen
from .models import CompanyMaintenance
from .models import CompanyMaintenanceScreen
from .models import CurrencyMaintenance
from .models import CurrencyMaintenanceScreen
from .models import EmployeeMaintenance
from .models import EmployeeMaintenanceScreen
from .models import UserMaintenance
from .models import PaymentTermMaintenance
from .models import PaymentTermMaintenanceScreen
from .models import LocationMaintenance
from .models import LocationMaintenanceScreen
from .models import ItemClassesMaintenance
from .models import ItemClassesMaintenanceScreen
from .models import ItemGroupsMaintenance
from .models import ItemGroupsMaintenanceScreen
from .models import WorkflowApprovalRule
from .models import WorkflowApprovalRuleScreen
from .models import WorkflowApprovalGroup
from .models import WorkflowApprovalGroupScreen
from .models import WorkflowApprovalRuleGroupMaintenance
from .models import WorkflowApprovalRuleGroupMaintenanceScreen
from .models import VendorGroupMaintenance
from .models import VendorGroupMaintenanceScreen
from .models import SystemFlagMaintenance
from .models import SystemFlagMaintenanceScreen
from .models import EmployeePositionMaintenance
from .models import EmployeePositionMaintenanceScreen
from .models import BranchMaintenance
from .models import BranchMaintenanceScreen
from .models import CountryMaintenance
from .models import CountryMaintenanceScreen
from .models import EmployeeBranchMaintenance
from .models import EmployeeBranchMaintenanceScreen
from .models import EmployeeDepartmentMaintenance
from .models import EmployeeDepartmentMaintenanceScreen
from .models import EmployeeGroupMaintenance
from .models import EmployeeGroupMaintenanceScreen
from .models import EmployeeProjectMaintenance
from .models import EmployeeProjectMaintenanceScreen
from .models import RegionMaintenance
from .models import RegionMaintenanceScreen
from .models import TaxMaintenance
from .models import TaxMaintenanceScreen
from .models import DrawerMaintenance
from .models import DrawerMaintenanceScreen

admin.site.register(WorkflowPattern)
admin.site.register(WorkflowInstance)
admin.site.register(ProjectMaintenance,ProjectMaintenanceScreen)
admin.site.register(StatusMaintenance,StatusMaintenanceScreen)
admin.site.register(DepartmentMaintenance,DepartmentMaintenanceScreen)
admin.site.register(DocumentTypeMaintenance,DocumentTypeMaintenanceScreen)
admin.site.register(CompanyMaintenance,CompanyMaintenanceScreen)
admin.site.register(CurrencyMaintenance,CurrencyMaintenanceScreen)
admin.site.register(EmployeeMaintenance,EmployeeMaintenanceScreen)
admin.site.register(UserMaintenance)
admin.site.register(PaymentTermMaintenance,PaymentTermMaintenanceScreen)
admin.site.register(LocationMaintenance,LocationMaintenanceScreen)
admin.site.register(ItemClassesMaintenance,ItemClassesMaintenanceScreen)
admin.site.register(ItemGroupsMaintenance,ItemGroupsMaintenanceScreen)
admin.site.register(WorkflowApprovalRule,WorkflowApprovalRuleScreen)
admin.site.register(WorkflowApprovalGroup,WorkflowApprovalGroupScreen)
admin.site.register(WorkflowApprovalRuleGroupMaintenance,WorkflowApprovalRuleGroupMaintenanceScreen)
admin.site.register(VendorGroupMaintenance,VendorGroupMaintenanceScreen)
admin.site.register(SystemFlagMaintenance,SystemFlagMaintenanceScreen)
admin.site.register(EmployeePositionMaintenance,EmployeePositionMaintenanceScreen)
admin.site.register(BranchMaintenance,BranchMaintenanceScreen)
admin.site.register(CountryMaintenance,CountryMaintenanceScreen)
admin.site.register(EmployeeBranchMaintenance,EmployeeBranchMaintenanceScreen)
admin.site.register(EmployeeDepartmentMaintenance,EmployeeDepartmentMaintenanceScreen)
admin.site.register(EmployeeGroupMaintenance,EmployeeGroupMaintenanceScreen)
admin.site.register(EmployeeProjectMaintenance,EmployeeProjectMaintenanceScreen)
admin.site.register(RegionMaintenance,RegionMaintenanceScreen)
admin.site.register(TaxMaintenance,TaxMaintenanceScreen)
admin.site.register(DrawerMaintenance,DrawerMaintenanceScreen)
