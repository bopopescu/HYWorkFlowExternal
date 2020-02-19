from django.contrib import admin
from .models import WorkflowPattern
from .models import WorkflowInstance
from .models import ProjectMaintenance
from .models import StatusMaintenance
from .models import DepartmentMaintenance
from .models import CompanyMaintenance
from .models import EmployeeMaintenance
from .models import UserMaintenance
from .models import PaymentTermMaintenance

admin.site.register(WorkflowPattern)
admin.site.register(WorkflowInstance)
admin.site.register(ProjectMaintenance)
admin.site.register(StatusMaintenance)
admin.site.register(DepartmentMaintenance)
admin.site.register(CompanyMaintenance)
admin.site.register(EmployeeMaintenance)
admin.site.register(UserMaintenance)
admin.site.register(PaymentTermMaintenance)
