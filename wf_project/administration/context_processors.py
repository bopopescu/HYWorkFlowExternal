from django.shortcuts import get_object_or_404
from .models import DepartmentMaintenance, EmployeeMaintenance, EmployeeDepartmentMaintenance

def access_type(request):
    user_as_employee = get_object_or_404(EmployeeMaintenance, user=request.user)
    employee_department = get_object_or_404(EmployeeDepartmentMaintenance, employee=user_as_employee)
    access_type = get_object_or_404(DepartmentMaintenance, pk=employee_department.department.pk)
    return {
        'access_type': access_type
    }