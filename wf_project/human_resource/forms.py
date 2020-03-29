from django import forms
from .models import StaffRecruitmentRequest
from django.shortcuts import get_object_or_404
import datetime
from administration.models import EmployeeMaintenance
from administration.models import CompanyMaintenance
from administration.models import DepartmentMaintenance
from administration.models import StaffPositionTitleMaintenance
from administration.models import StaffHireTypeMaintenance


class DetailStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.company, disabled=True)
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.reporting_to, disabled=True)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.department, disabled=True)
    position_title = forms.ModelChoiceField(queryset=StaffPositionTitleMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.position_title, disabled=True)
    hire_type = forms.ModelChoiceField(queryset=StaffHireTypeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.hire_type, disabled=True)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['revision','position_title','status','document_number','request_date','subject','reporting_to',
        'budgeted','no_of_pax','month_to_be_filled']

class NewStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned")
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.all(), empty_label="Not Assigned")
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned")
    position_title = forms.ModelChoiceField(queryset=StaffPositionTitleMaintenance.objects.all(), empty_label="Not Assigned")
    hire_type = forms.ModelChoiceField(queryset=StaffHireTypeMaintenance.objects.all(), empty_label="Not Assigned")
    request_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    revision = forms.IntegerField(initial=0)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['revision','position_title','status','request_date','document_number','subject','reporting_to',
        'budgeted','no_of_pax','month_to_be_filled']

class UpdateStaffRecruimentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.company)
    reporting_to = forms.ModelChoiceField(queryset=EmployeeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.reporting_to)
    department = forms.ModelChoiceField(queryset=DepartmentMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.department)
    position_title = forms.ModelChoiceField(queryset=StaffPositionTitleMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.position_title)
    hire_type = forms.ModelChoiceField(queryset=StaffHireTypeMaintenance.objects.all(), empty_label="Not Assigned",initial=StaffRecruitmentRequest.hire_type)
    class Meta:
        model = StaffRecruitmentRequest
        fields = ['revision','position_title','status','document_number','request_date','subject','reporting_to',
        'budgeted','no_of_pax','month_to_be_filled']