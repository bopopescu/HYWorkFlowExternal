from django import forms
from .models import ReimbursementRequest
from administration.models import DrawerMaintenance,TransactiontypeMaintenance,DocumentTypeMaintenance
import datetime

class DetailReimbursementForm(forms.ModelForm):
    drawer = forms.ModelChoiceField(queryset=DrawerMaintenance.objects.filter(drawer_status="O").order_by('drawer_name'), empty_label="Not Assigned",initial=ReimbursementRequest.drawer, disabled=True)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="403")[0]), empty_label="Not Assigned",initial=ReimbursementRequest.transaction_type, disabled=True)

    class Meta:
        model = ReimbursementRequest
        fields = ['drawer','request_amount','submit_date','transaction_type','description','status','document_number']

class NewReimbursementForm(forms.ModelForm):
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    drawer = forms.ModelChoiceField(queryset=DrawerMaintenance.objects.filter(drawer_status="O").order_by('drawer_name'), empty_label="Not Assigned",initial=ReimbursementRequest.drawer)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="403")[0]), empty_label="Not Assigned")

    class Meta:
        model = ReimbursementRequest
        fields = ['drawer','request_amount','transaction_type','submit_date','description','status','document_number']

class UpdateReimbursementForm(forms.ModelForm):
    submit_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput)
    drawer = forms.ModelChoiceField(queryset=DrawerMaintenance.objects.filter(drawer_status="O").order_by('drawer_name'), empty_label="Not Assigned",initial=ReimbursementRequest.drawer)
    transaction_type = forms.ModelChoiceField(queryset=TransactiontypeMaintenance.objects.filter(document_type=DocumentTypeMaintenance.objects.filter(document_type_code="403")[0]), empty_label="Not Assigned",initial=ReimbursementRequest.transaction_type)
    
    class Meta:
        model = ReimbursementRequest
        fields = ['drawer','request_amount','submit_date','transaction_type','description','status','document_number']
