from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import DrawerDisbursementSerializer, DrawerSelectionSerializer, ApprovedPaymentRequest
from administration.models import DrawerMaintenance, EmployeeMaintenance
from administration.models import DrawerUserMaintenance
from django.contrib.auth.hashers import check_password
from administration.models import TransactiontypeMaintenance, DocumentTypeMaintenance
from administration.models import StatusMaintenance,CompanyAddressDetail,CompanyContactDetail
from approval.models import ApprovalItem, ApprovalItemApprover
from utility_dashboard.models import UtilityApprovalItem, UtilityApprovalItemApprover
from drawer_reimbursement.models import DrawerReimbursement
from .models import DrawerDisbursement
from payment.models import PaymentRequest, PaymentRequestDetail
from django.http import HttpResponse, JsonResponse
from PDFreport.render import Render
import decimal

# class TeamStaffViewSet(viewsets.ModelViewSet):
#     queryset = StaffRecruitmentRequest.objects.all().order_by('-id')    
#     serializer_class = StaffRecruitmentSerializer

#     def get_queryset(self):
#         groups = self.request.user.groups.values_list('id', flat=True)
#         users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
#         return StaffRecruitmentRequest.objects.filter(submit_by__in=users)

class DrawerViewSet(viewsets.ModelViewSet):
    queryset = DrawerMaintenance.objects.all().order_by('-id')
    serializer_class = DrawerSelectionSerializer

    def get_queryset(self):
        drawer_user = DrawerUserMaintenance.objects.filter(user=self.request.user).values_list('drawer', flat=True)
        return DrawerMaintenance.objects.filter(id__in=drawer_user, drawer_status='O').order_by('-id')

class DisbursementListViewSet(viewsets.ModelViewSet):
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='301')
    document_status_approve = StatusMaintenance.objects.get(document_type=document_type, status_code='400')
    transaction = TransactiontypeMaintenance.objects.get(transaction_type_name="Petty Cash")
    queryset = PaymentRequest.objects.filter(status=document_status_approve, transaction_type=transaction)
    serializer_class = ApprovedPaymentRequest

class DisbursedViewSet(viewsets.ModelViewSet):
    serializer_class = DrawerDisbursementSerializer

    def get_queryset(self):
        drawer = get_object_or_404(DrawerMaintenance, pk=self.request.query_params.get('drawerpk', None))
        document_type = DocumentTypeMaintenance.objects.get(document_type_code='402')
        document_status_disburse = StatusMaintenance.objects.get(document_type=document_type, status_code='700')
        return DrawerDisbursement.objects.filter(status=document_status_disburse,drawer=drawer)


class CancelledViewSet(viewsets.ModelViewSet):
    serializer_class = DrawerDisbursementSerializer

    def get_queryset(self):
        drawer = get_object_or_404(DrawerMaintenance, pk=self.request.query_params.get('drawerpk', None))
        document_type = DocumentTypeMaintenance.objects.get(document_type_code='402')
        document_status_cancel = StatusMaintenance.objects.get(document_type=document_type, status_code='999')
        return DrawerDisbursement.objects.filter(status=document_status_cancel,drawer=drawer)

@login_required
def drawer_list(request):
    return render(request, 'drawer_selection.html')

@login_required
def drawer_disbursement_list(request, drawerpk):
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    return render(request, 'disbursement_list.html', {'drawer': drawer})

@login_required
def drawer_disbursement_disbursed(request, pk, drawerpk, userid, password):
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='301')
    document_status_closed = StatusMaintenance.objects.get(document_type=document_type, status_code='600')
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    payment = PaymentRequest.objects.get(pk=pk)
    user = User.objects.filter(username=userid)
    uservalidation = False
    process = False
    if user.count() == 0:
        return JsonResponse({'message': 'User Login ID or Password invalid', 'valid':False, 'validbalance':True})
    else:
        user = user.first()
        if payment.submit_by == user:
            if user.check_password(password) == True:
                process = True
            else:
                return JsonResponse({'message': 'User Login ID or Password invalid', 'valid':False, 'validbalance':True})
        else:
            return JsonResponse({'message': 'User ID is not matched the user submit this petty cash', 'valid':False, 'validbalance':True})
    
    total_drawer_amount = drawer_amount(drawerpk)
    drawer_amount_after = total_drawer_amount - payment.total_amount
    drawer_amount_lack = payment.total_amount -total_drawer_amount 
    print(total_drawer_amount)
    print(drawer_amount_after)

    if drawer_amount_after < 0:
        return JsonResponse({'message': 'This drawer balance is not enough', 'valid':False, 'validbalance':False, 'amount':drawer_amount_lack})
    
    else:
        if process == True:

            payment.status = document_status_closed

            document_type_disburse = DocumentTypeMaintenance.objects.get(document_type_code='402')
            document_status_disburse = StatusMaintenance.objects.get(document_type=document_type_disburse, status_code='700')

            disbursedrecord = DrawerDisbursement()
            disbursedrecord.payment = payment
            disbursedrecord.total_disbursed = payment.total_amount
            disbursedrecord.status = document_status_disburse
            disbursedrecord.drawer = drawer
            disbursedrecord.save()
            payment.save()
            return JsonResponse({'message': 'Success', 'valid' : True, 'validbalance':True})

@login_required
def drawer_disbursement_cancel(request, pk, drawerpk):
    
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='301')
    document_status_closed = StatusMaintenance.objects.get(document_type=document_type, status_code='600')
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    payment = PaymentRequest.objects.get(pk=pk)
    payment.status = document_status_closed

    document_type_disburse = DocumentTypeMaintenance.objects.get(document_type_code='402')
    document_status_disbursecancel = StatusMaintenance.objects.get(document_type=document_type_disburse, status_code='999')

    disbursedrecord = DrawerDisbursement()
    disbursedrecord.payment = payment
    disbursedrecord.total_disbursed = payment.total_amount
    disbursedrecord.status = document_status_disbursecancel
    disbursedrecord.drawer = drawer
    disbursedrecord.save()
    payment.save()

    return JsonResponse({'message': 'Success'})

def drawer_amount(drawerpk):
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
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
    return total_drawer_amount

@login_required
def payment_voucher_print(request, pk): 
    py = get_object_or_404(PaymentRequest, pk=pk)
    py_item = PaymentRequestDetail.objects.filter(py=py).order_by("linenum")
    if py.transaction_type.is_utility:
        approval_item = get_object_or_404(UtilityApprovalItem, pk=py.utility_account_approval.pk)
        approver = UtilityApprovalItemApprover.objects.filter(utility_approval_item=approval_item).order_by('-stage')[0]
    else:
        approval_item = get_object_or_404(ApprovalItem, pk=py.approval.pk)
        approver = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('-stage')[0]

    requester = get_object_or_404(User, pk=py.submit_by.pk)
    approver_employee = get_object_or_404(EmployeeMaintenance, user=approver.user)
    
    company_address = CompanyAddressDetail.objects.filter(company=py.company,default=True)
    if company_address.count() > 0:
        company_address = company_address[0]
    else:
        company_address = CompanyAddressDetail.objects.filter(company=py.company)
        if company_address.count() > 0:
            company_address = company_address[0]

    company_contact = CompanyContactDetail.objects.filter(company=py.company,default=True)
    if company_contact.count() > 0:
        company_contact = company_contact[0]
    else:
        company_contact = CompanyContactDetail.objects.filter(company=py.company)
        if company_contact.count() > 0:
            company_contact = company_contact[0]
    # return render(request, 'PR/print.html', {'py': py, 'py_item':py_item})
    
    params = {
        'py': py, 
        'py_item': py_item, 
        'request': request, 
        'approval_item': approval_item, 
        'requester': requester, 
        'approver_employee': approver_employee, 
        'company_address': company_address,
        'company_contact': company_contact,
    }
    
    pdf = Render.render('PV/print.html', params)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "PaymentVoucher_%s.pdf" %(py.document_number)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return response("errors")
