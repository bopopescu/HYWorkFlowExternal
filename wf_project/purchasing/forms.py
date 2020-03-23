from django import forms
from .models import PurchaseOrder

class NewPOForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = PurchaseOrder
        fields = ['remarks']