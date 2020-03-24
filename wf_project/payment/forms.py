from django import forms
from .models import PaymentRequest

class NewPaymentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = PaymentRequest
        fields = ['revision','document_number','vendor','company','currency','project','transaction_type','payment_mode','status',
        'submit_date','subject','reference','sub_total','discount_amount','discount_rate','tax_amount','total_amount',
        'remarks','attachment','attachment_date']