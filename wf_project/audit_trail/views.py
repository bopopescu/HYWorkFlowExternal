from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import DrawerSelectionSerializer,DrawerDisbursementSerializer
from administration.models import DrawerMaintenance,TransactiontypeMaintenance
from administration.models import DrawerUserMaintenance
from drawer_reimbursement.models import DrawerReimbursement,ReimbursementRequest
from drawer_disbursement.models import DrawerDisbursement
from payment.models import PaymentRequest
from django.http import JsonResponse
from administration.models import DocumentTypeMaintenance,StatusMaintenance
import decimal

# Create your views here.
class DrawerViewSet(viewsets.ModelViewSet):
    queryset = DrawerMaintenance.objects.all().order_by('-id')
    serializer_class = DrawerSelectionSerializer

    def get_queryset(self):
        drawer_user = DrawerUserMaintenance.objects.filter(user=self.request.user).values_list('drawer', flat=True)
        return DrawerMaintenance.objects.filter(id__in=drawer_user,drawer_status='O').order_by('-id')

class DisbursedViewSet(viewsets.ModelViewSet):
    serializer_class = DrawerDisbursementSerializer

    def get_queryset(self):
        document_type = DocumentTypeMaintenance.objects.get(document_type_code='402')
        document_status_disburse = StatusMaintenance.objects.get(document_type=document_type,status_code='700')
        drawer = get_object_or_404(DrawerMaintenance, pk=self.request.query_params.get('pk', None))
        return DrawerDisbursement.objects.filter(status=document_status_disburse,drawer=drawer).order_by('-id')

@login_required
def drawer_list(request):
    return render(request, 'audit_trails/audit_drawer_selection.html')

@login_required
def audit_trail_report(request,pk):
    drawer = DrawerMaintenance.objects.get(pk=pk)
    reimburse_type = get_object_or_404(DocumentTypeMaintenance,document_type_code="403")
    opening_transaction_type = TransactiontypeMaintenance.objects.filter(transaction_type_name="Opening Balance")[0]
    opening_balance = decimal.Decimal(0.00)
    reimburse_balance = decimal.Decimal(0.00)
    current_balance = decimal.Decimal(0.00)
    status = get_object_or_404(StatusMaintenance,status_code="600",document_type=reimburse_type)
    reimburse_request = ReimbursementRequest.objects.filter(status=status,transaction_type=opening_transaction_type).values_list("id",flat=True)
    opening_drawer_reimburse = DrawerReimbursement.objects.filter(reimbursement_request_id__in=reimburse_request)
    
    for opening_drawer in opening_drawer_reimburse:
        opening_balance = opening_balance + opening_drawer.total_reimburse
    
    reimburse_transaction_type = TransactiontypeMaintenance.objects.filter(transaction_type_name="Reimbursement Request")[0]
    reimburse_request_balance = ReimbursementRequest.objects.filter(status=status,transaction_type=reimburse_transaction_type).values_list("id",flat=True)
    reimburse_request_drawer_reimburse = DrawerReimbursement.objects.filter(reimbursement_request_id__in=reimburse_request_balance)
    current_balance = drawer_amount(drawer.pk)

    for reimburse_request_drawer in reimburse_request_drawer_reimburse:
        reimburse_balance = reimburse_balance + reimburse_request_drawer.total_reimburse

    reimbursementbalance = current_balance + reimburse_balance + opening_balance

    return render(request, 'audit_trails/audit_trails.html',{'drawer': drawer,'openbalance':opening_balance,'reimbursebalance':reimburse_balance,'currenctbalance':current_balance,'reimbursementbalance':reimbursementbalance})

def drawer_amount(drawerpk):
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    total_disbursed_amount = decimal.Decimal(0.00)
    total_reimbursed_amount = decimal.Decimal(0.00)
    total_drawer_amount = decimal.Decimal(0.00)

    #Count for Disbursed
    drawer_disbursements = DrawerDisbursement.objects.filter(drawer=drawer)
    for drawer_disbursed in drawer_disbursements:
        total_disbursed = drawer_disbursed.total_disbursed
        total_disbursed_amount = total_disbursed_amount + total_disbursed

    drawer_reimbursements = DrawerReimbursement.objects.filter(drawer=drawer)
    for drawer_reimburse in drawer_reimbursements:
        total_reimbursed = drawer_reimburse.total_reimburse
        total_reimbursed_amount = total_reimbursed_amount + total_reimbursed

    total_drawer_amount = total_reimbursed_amount - total_disbursed_amount

    return total_drawer_amount