from django import forms
from .models import DrawerDisbursement
from payment.models import PaymentRequest

class DetailDisbursementForm(forms.ModelForm):

    payment = forms.ModelChoiceField(queryset=PaymentRequest.objects.all(), empty_label="Not Assigned", initial=DrawerDisbursement.payment, disabled=True)

    class Meta:
        model = DrawerDisbursement
        fields = ['disbursed_by', 'status','total_disbursed','payment','disbursed_date']

