from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import DrawerDisbursementSerializer,DrawerSelectionSerializer,ApprovedPaymentRequest
from administration.models import DrawerMaintenance
from administration.models import DrawerUserMaintenance
from django.contrib.auth.hashers import check_password
from administration.models import TransactiontypeMaintenance
from administration.models import DocumentTypeMaintenance
from administration.models import StatusMaintenance
from .models import DrawerDisbursement
from payment.models import PaymentRequest
from django.http import JsonResponse

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
        return DrawerMaintenance.objects.filter(id__in=drawer_user,drawer_status='O').order_by('-id')

class DisbursementListViewSet(viewsets.ModelViewSet):
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='301')
    document_status_approve = StatusMaintenance.objects.get(document_type=document_type,status_code='400')
    transaction = TransactiontypeMaintenance.objects.get(transaction_type_name="Petty Cash")
    queryset = PaymentRequest.objects.filter(status=document_status_approve,transaction_type=transaction)
    serializer_class = ApprovedPaymentRequest

class DisbursedViewSet(viewsets.ModelViewSet):
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='402')
    document_status_disburse = StatusMaintenance.objects.get(document_type=document_type,status_code='700')
    queryset = DrawerDisbursement.objects.filter(status=document_status_disburse)
    serializer_class = DrawerDisbursementSerializer

class CancelledViewSet(viewsets.ModelViewSet):
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='402')
    document_status_cancel = StatusMaintenance.objects.get(document_type=document_type,status_code='999')
    queryset = DrawerDisbursement.objects.filter(status=document_status_cancel)
    serializer_class = DrawerDisbursementSerializer

@login_required
def drawer_list(request):
    return render(request, 'drawer_selection.html')

@login_required
def drawer_disbursement_list(request,drawerpk):
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    return render(request, 'disbursement_list.html', {'drawer': drawer})

@login_required
def drawer_disbursement_disbursed(request,pk,drawerpk,userid,password):
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='301')
    document_status_closed = StatusMaintenance.objects.get(document_type=document_type,status_code='600')
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    payment = PaymentRequest.objects.get(pk=pk)
    user = User.objects.filter(username=userid)
    uservalidation = False
    process = False
    if user.count() == 0:
        return JsonResponse({'message': 'User Login ID or Password invalid','valid':False})
    else:
        user = user.first()
        if payment.submit_by == user:
            if user.check_password(password) == True:
                process = True
            else:
                return JsonResponse({'message': 'User Login ID or Password invalid','valid':False})
        else:
            return JsonResponse({'message': 'User ID is not matched the user submit this petty cash','valid':False})
        

    if process == True:
        payment.status = document_status_closed

        document_type_disburse = DocumentTypeMaintenance.objects.get(document_type_code='402')
        document_status_disburse = StatusMaintenance.objects.get(document_type=document_type_disburse,status_code='700')

        disbursedrecord = DrawerDisbursement()
        disbursedrecord.payment = payment
        disbursedrecord.total_disbursed = payment.total_amount
        disbursedrecord.status = document_status_disburse
        disbursedrecord.drawer = drawer
        disbursedrecord.save()
        payment.save()
        return JsonResponse({'message': 'Success','valid' : True})

@login_required
def drawer_disbursement_cancel(request,pk,drawerpk):
    
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='301')
    document_status_closed = StatusMaintenance.objects.get(document_type=document_type,status_code='600')
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    payment = PaymentRequest.objects.get(pk=pk)
    payment.status = document_status_closed

    document_type_disburse = DocumentTypeMaintenance.objects.get(document_type_code='402')
    document_status_disbursecancel = StatusMaintenance.objects.get(document_type=document_type_disburse,status_code='999')

    disbursedrecord = DrawerDisbursement()
    disbursedrecord.payment = payment
    disbursedrecord.total_disbursed = payment.total_amount
    disbursedrecord.status = document_status_disbursecancel
    disbursedrecord.drawer = drawer
    disbursedrecord.save()
    payment.save()

    return JsonResponse({'message': 'Success'})
