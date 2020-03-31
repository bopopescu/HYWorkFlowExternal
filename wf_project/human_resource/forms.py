from django import forms
from .models import StaffRecruitmentRequest,StaffJobRequirement,StaffJobResponsibilities
from django.shortcuts import get_object_or_404
import datetime
from administration.models import EmployeeMaintenance
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import StaffPositionTitleMaintenance
from administration.models import StaffemploymentTypeMaintenance
from administration.models import StaffPositionGradeMaintenance


class DetailStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.company, disabled=True)
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.reporting_to, disabled=True)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.department, disabled=True)
    position_title = forms.ModelChoiceField(queryset=StaffPositionTitleMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.position_title, disabled=True)
    employment_type = forms.ModelChoiceField(queryset=StaffemploymentTypeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.employment_type, disabled=True)
    position_grade = forms.ModelChoiceField(queryset=StaffPositionGradeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.position_grade, disabled=True)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['position_title','company','reporting_to','department','employment_type','position_grade',
        'revision','status','document_number','request_date','reporting_to',
        'budgeted','no_of_pax','month_to_be_filled']

class NewStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.all(), empty_label="Not Assigned")
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned")
    position_title = forms.ModelChoiceField(queryset=StaffPositionTitleMaintenance.objects.all(), empty_label="Not Assigned")
    employment_type = forms.ModelChoiceField(queryset=StaffemploymentTypeMaintenance.objects.all(), empty_label="Not Assigned")
    request_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    position_grade = forms.ModelChoiceField(queryset=StaffPositionGradeMaintenance.objects.all(), empty_label="Not Assigned")
    revision = forms.IntegerField(initial=0)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['revision','position_title','status','request_date','document_number','reporting_to',
        'budgeted','no_of_pax','month_to_be_filled']

class UpdateStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.company)
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.reporting_to)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.department)
    position_title = forms.ModelChoiceField(queryset=StaffPositionTitleMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.position_title)
    employment_type = forms.ModelChoiceField(queryset=StaffemploymentTypeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.employment_type)
    position_grade = forms.ModelChoiceField(queryset=StaffPositionGradeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.position_grade)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['position_title','company','reporting_to','department','employment_type','position_grade',
        'revision','status','document_number','request_date','reporting_to',
        'budgeted','no_of_pax','month_to_be_filled']

class NewStaffJobRequirementForm(forms.ModelForm):

    class Meta:
        model = StaffJobRequirement
        fields = ['staff_recruitment', 'requirement_description']

class NewStaffJobResponsibleForm(forms.ModelForm):

    class Meta:
        model = StaffJobResponsibilities
        fields = ['staff_recruitment', 'responsible_description']
