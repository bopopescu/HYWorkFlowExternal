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
from .models import VendorGroupMaintenance
from .models import SystemFlagMaintenance
from .models import EmployeePositionMaintenance
from .models import BranchMaintenance
from .models import CountryMaintenance
from .models import EmployeeBranchMaintenance
from .models import EmployeeDepartmentMaintenance
from .models import EmployeeGroupMaintenance
from .models import EmployeeProjectMaintenance
from .models import RegionMaintenance
from .models import CompanyMaintenanceScreen
from .models import TaxMaintenance
from .models import TaxMaintenanceScreen

admin.site.register(WorkflowPattern)
admin.site.register(WorkflowInstance)
admin.site.register(ProjectMaintenance)
admin.site.register(StatusMaintenance)
admin.site.register(DepartmentMaintenance)
admin.site.register(DocumentTypeMaintenance)
admin.site.register(CompanyMaintenance,CompanyMaintenanceScreen)
admin.site.register(CurrencyMaintenance)
admin.site.register(EmployeeMaintenance)
admin.site.register(UserMaintenance)
admin.site.register(PaymentTermMaintenance)
admin.site.register(LocationMaintenance)
admin.site.register(ItemClassesMaintenance)
admin.site.register(ItemGroupsMaintenance)
admin.site.register(WorkflowApprovalRule)
admin.site.register(VendorGroupMaintenance)
admin.site.register(SystemFlagMaintenance)
admin.site.register(EmployeePositionMaintenance)
admin.site.register(BranchMaintenance)
admin.site.register(CountryMaintenance)
admin.site.register(EmployeeBranchMaintenance)
admin.site.register(EmployeeDepartmentMaintenance)
admin.site.register(EmployeeGroupMaintenance)
admin.site.register(EmployeeProjectMaintenance)
admin.site.register(RegionMaintenance)
admin.site.register(TaxMaintenance,TaxMaintenanceScreen)
