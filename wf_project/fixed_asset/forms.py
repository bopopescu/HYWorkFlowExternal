from django import forms
from .models import *
from administration.models import CompanyMaintenance

class AssetMasterForm(forms.ModelForm):
    remark = forms.CharField(widget=forms.Textarea)
    company = forms.ModelChoiceField(queryset=CompanyMaintenance.objects.filter(is_active=True).order_by('company_name'), empty_label="Not Assigned", initial=AssetMaster.company)
    
    class Meta:
        model = AssetMaster
        fields = (
            'asset_number',
            'description',
            'asset_type_id',
            'asset_category_id',
            'tax_id',
            'class_type_id',
            'floor_plan_ref',
            'trustees',
            'cost_value',
            'net_book_value',
            'proceeds_on_disposal',
            'historical_cost',
            'active_lifetime',
            'active_res_value',
            'tax_cost',
            'current_tax_percentage'
        )