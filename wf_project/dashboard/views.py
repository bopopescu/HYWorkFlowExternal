from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from drawer_reimbursement.models import DrawerReimbursement
from drawer_disbursement.models import DrawerDisbursement
from administration.models import DrawerMaintenance
from administration.models import DrawerUserMaintenance,DocumentTypeMaintenance,StatusMaintenance
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import decimal

class IndexView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts/login/'
    redirect_field_name = '/'
    template_name="home.html"

@login_required
def count_drawer_amount(request,pk):
    drawer = DrawerMaintenance.objects.get(pk=pk)
    total_disbursed_amount = decimal.Decimal(0.00)
    total_reimbursed_amount = decimal.Decimal(0.00)
    total_drawer_amount = decimal.Decimal(0.00)
    disbursed_type = DocumentTypeMaintenance.objects.get(document_type_code='402')
    reimburse_type = DocumentTypeMaintenance.objects.get(document_type_code='401')
    document_status_disbursed = StatusMaintenance.objects.get(document_type=disbursed_type,status_code='700')
    document_status_reimburse = StatusMaintenance.objects.get(document_type=reimburse_type,status_code='700')
    #Count for Disbursed
    drawer_disbursements = DrawerDisbursement.objects.filter(drawer=drawer,status=document_status_disbursed)
    for drawer_disbursed in drawer_disbursements:
        total_disbursed = drawer_disbursed.total_disbursed
        total_disbursed_amount = total_disbursed_amount + total_disbursed

    drawer_reimbursements = DrawerReimbursement.objects.filter(drawer=drawer,status=document_status_reimburse)
    for drawer_reimburse in drawer_reimbursements:
        total_reimbursed = drawer_reimburse.total_reimburse
        total_reimbursed_amount = total_reimbursed_amount + total_reimbursed

    total_drawer_amount = total_reimbursed_amount - total_disbursed_amount

    return JsonResponse({'total_drawer_amount': total_drawer_amount})