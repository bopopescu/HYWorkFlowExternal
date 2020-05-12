from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from drawer_reimbursement.models import DrawerReimbursement
from drawer_disbursement.models import DrawerDisbursement
from administration.models import DrawerMaintenance
from administration.models import DrawerUserMaintenance,DocumentTypeMaintenance,StatusMaintenance
from approval.models import ApprovalItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import decimal

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

@login_required
def home_index(request):
    in_progress = ApprovalItem.objects.filter(status='IP').count()
    approved = ApprovalItem.objects.filter(status='A').count()
    rejected = ApprovalItem.objects.filter(status='R').count()
    all_approval = ApprovalItem.objects.count()

    in_progress = (in_progress/all_approval) * 100
    approved = (approved/all_approval) * 100
    rejected = (rejected/all_approval) * 100

    return render(request, 'home.html', {'in_progress': in_progress, 'approved': approved, 'rejected': rejected})
