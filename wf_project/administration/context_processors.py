from django.shortcuts import get_object_or_404
from .models import DepartmentMaintenance, EmployeeMaintenance, EmployeeDepartmentMaintenance

def access_accounts_dashboard(request):
    if request.user.is_anonymous:
        return {
            'access_accounts_dashboard': False
        }
    else:
        try:
            user_as_employee = get_object_or_404(EmployeeMaintenance, user=request.user)
            employee_department = get_object_or_404(EmployeeDepartmentMaintenance, employee=user_as_employee)
            access_type = get_object_or_404(DepartmentMaintenance, pk=employee_department.department.pk)
            return {
                'access_accounts_dashboard': access_type.access_accounts_dashboard
            }
        except:
            return {
                'access_accounts_dashboard': False
            }