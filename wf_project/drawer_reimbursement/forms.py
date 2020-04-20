from django import forms
from .models import ReimbursementRequest
from administration.models import DrawerMaintenance
import datetime

class DetailReimbursementForm(forms.ModelForm):
    drawer = forms.ModelChoiceField(queryset=DrawerMaintenance.objects.filter(is_active=True).order_by('drawer_name'), empty_label="Not Assigned",initial=ReimbursementRequest.drawer, disabled=True)

    class Meta:
        model = ReimbursementRequest
        fields = ['drawer','request_amount','submit_date','description','status','document_number']

class NewReimbursementForm(forms.ModelForm):
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    drawer = forms.ModelChoiceField(queryset=DrawerMaintenance.objects.filter(is_active=True).order_by('drawer_name'), empty_label="Not Assigned",initial=ReimbursementRequest.drawer)

    class Meta:
        model = ReimbursementRequest
        fields = ['drawer','request_amount','submit_date','description','status','document_number']

class UpdateReimbursementForm(forms.ModelForm):
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    drawer = forms.ModelChoiceField(queryset=DrawerMaintenance.objects.filter(is_active=True).order_by('drawer_name'), empty_label="Not Assigned",initial=ReimbursementRequest.drawer)

    class Meta:
        model = ReimbursementRequest
        fields = ['drawer','request_amount','submit_date','description','status','document_number']
