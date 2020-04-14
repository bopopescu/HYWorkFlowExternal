from django import forms
from .models import StaffOT,StaffOTDetail
from django.shortcuts import get_object_or_404
import datetime
from administration.models import CompanyMaintenance
from administration.models import CurrencyMaintenance
from administration.models import ProjectMaintenance
from administration.models import VendorMasterData
from administration.models import TaxMaintenance,DepartmentMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import PaymentmodeMaintenance
from administration.models import EmployeeMaintenance,EmployeePositionMaintenance
from administration.models import DocumentTypeMaintenance


class DetailStaffOTForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StaffOT.company,disabled=True)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StaffOT.project,disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="504")[0]), empty_label="Not Assigned",initial=StaffOT.transaction_type,disabled=True)
    employee = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True).order_by('employee_name'), empty_label="Not Assigned",required=False,initial=StaffOT.employee,disabled=True)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned",required=False,initial=StaffOT.department,disabled=True)
    # employee_position = forms.ModelChoiceField(queryset=EmployeePositionMaintenance.objects.filter(is_active=True).order_by('position_name'), empty_label="Not Assigned",required=False)
    class Meta:
        model = StaffOT
        fields = ['company','project','transaction_type','employee','department','revision','document_number','employee_position','status','submit_date']


class NewStaffOTForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned")
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned")
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="504")[0]), empty_label="Not Assigned",required=False)
    employee = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True).order_by('employee_name'), empty_label="Not Assigned",required=False)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned",required=False)
    revision = forms.IntegerField(initial=0)
    # employee_position = forms.ModelChoiceField(queryset=EmployeePositionMaintenance.objects.filter(is_active=True).order_by('position_name'), empty_label="Not Assigned",required=False)
    class Meta:
        model = StaffOT
        fields = ['company','project','revision','transaction_type','employee','employee_position','department','document_number','status','submit_date']

class UpdateStaffOTForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned",initial=StaffOT.company)
    project = forms.ModelChoiceField(queryset=ProjectMaintenance.objects.all().order_by('project_name'), empty_label="Not Assigned",initial=StaffOT.project)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="504")[0]), empty_label="Not Assigned",initial=StaffOT.transaction_type,required=False)
    employee = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True).order_by('employee_name'), empty_label="Not Assigned",required=False,initial=StaffOT.employee)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned",required=False,initial=StaffOT.department)

    class Meta:
        model = StaffOT
        fields = ['company','project','transaction_type','revision','employee','employee_position','department','document_number','status','submit_date']


class NewStaffOTDetailForm(forms.ModelForm):
    
    class Meta:
        model = StaffOTDetail
        fields = ['staff_ot', 'ot_date', 'ot_time_in','ot_time_out','meal_allowance','is_holiday','remark']
