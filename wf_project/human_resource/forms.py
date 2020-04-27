from django import forms
from .models import StaffRecruitmentRequest, StaffJobRequirement, StaffJobResponsibilities, StaffPlatform, StaffCandidate
from django.shortcuts import get_object_or_404
import datetime
from administration.models import EmployeeMaintenance, EmployeePositionMaintenance
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import StaffPositionTitleMaintenance
from administration.models import StaffemploymentTypeMaintenance
from administration.models import StaffPositionGradeMaintenance, HRPlatformMaintenance


class DetailStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True), empty_label="Not Assigned", initial=StaffRecruitmentRequest.company, disabled=True)
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True), empty_label="Not Assigned", initial=StaffRecruitmentRequest.reporting_to, disabled=True)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True), empty_label="Not Assigned", initial=StaffRecruitmentRequest.department, disabled=True)
    position_title = forms.ModelChoiceField(queryset=EmployeePositionMaintenance.objects.filter(is_active=True), empty_label="Not Assigned", initial=StaffRecruitmentRequest.position_title, disabled=True)
    employment_type = forms.ModelChoiceField(queryset=StaffemploymentTypeMaintenance.objects.filter(is_active=True), empty_label="Not Assigned", initial=StaffRecruitmentRequest.employment_type, disabled=True)
    position_grade = forms.ModelChoiceField(queryset=StaffPositionGradeMaintenance.objects.filter(is_active=True), empty_label="Not Assigned", initial=StaffRecruitmentRequest.position_grade, disabled=True)
    budgeted = forms.BooleanField(initial=StaffRecruitmentRequest.budgeted)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['position_title', 'company', 'reporting_to', 'department', 'employment_type', 'position_grade', 
        'revision', 'status', 'document_number', 'request_date', 'reporting_to', 
        'budgeted', 'no_of_pax', 'month_to_be_filled']

class NewStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned")
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True).order_by('employee_name'), empty_label="Not Assigned")
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned")
    position_title = forms.ModelChoiceField(queryset=EmployeePositionMaintenance.objects.filter(is_active=True).order_by('position_name'), empty_label="Not Assigned")
    employment_type = forms.ModelChoiceField(queryset=StaffemploymentTypeMaintenance.objects.filter(is_active=True).order_by('employment_type_name'), empty_label="Not Assigned")
    request_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    position_grade = forms.ModelChoiceField(queryset=StaffPositionGradeMaintenance.objects.filter(is_active=True).order_by('position_grade_name'), empty_label="Not Assigned")
    revision = forms.IntegerField(initial=0)
    budgeted = forms.BooleanField(initial=False)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['revision', 'position_title', 'status', 'request_date', 'document_number', 'reporting_to', 
        'budgeted', 'no_of_pax', 'month_to_be_filled']

class UpdateStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned", initial=StaffRecruitmentRequest.company)
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.filter(is_active=True).order_by('employee_name'), empty_label="Not Assigned", initial=StaffRecruitmentRequest.reporting_to)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.filter(is_active=True).order_by('department_name'), empty_label="Not Assigned", initial=StaffRecruitmentRequest.department)
    position_title = forms.ModelChoiceField(queryset=EmployeePositionMaintenance.objects.filter(is_active=True).order_by('position_name'), empty_label="Not Assigned", initial=StaffRecruitmentRequest.position_title)
    employment_type = forms.ModelChoiceField(queryset=StaffemploymentTypeMaintenance.objects.filter(is_active=True).order_by('employment_type_name'), empty_label="Not Assigned", initial=StaffRecruitmentRequest.employment_type)
    position_grade = forms.ModelChoiceField(queryset=StaffPositionGradeMaintenance.objects.filter(is_active=True).order_by('position_grade_name'), empty_label="Not Assigned", initial=StaffRecruitmentRequest.position_grade)
    budgeted = forms.BooleanField(initial=StaffRecruitmentRequest.budgeted)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['position_title', 'company', 'reporting_to', 'department', 'employment_type', 'position_grade', 
        'revision', 'status', 'document_number', 'request_date', 'reporting_to', 
        'budgeted', 'no_of_pax', 'month_to_be_filled']

class NewStaffJobRequirementForm(forms.ModelForm):

    class Meta:
        model = StaffJobRequirement
        fields = ['staff_recruitment', 'requirement_description']

class NewStaffJobResponsibleForm(forms.ModelForm):

    class Meta:
        model = StaffJobResponsibilities
        fields = ['staff_recruitment', 'responsible_description']

class NewStaffPlatformForm(forms.ModelForm):
    platform_name = forms.ModelChoiceField(queryset=HRPlatformMaintenance.objects.filter(is_active=True).order_by('platform_name'), empty_label="Not Assigned")

    class Meta:
        model = StaffPlatform
        fields = ['staff_recruitment', 'platform_name', 'success_platform']

class NewStaffCandidateForm(forms.ModelForm):

    class Meta:
        model = StaffCandidate
        fields = ['staff_recruitment', 'candidate_name', 'date_of_join']
