from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import DrawerDisbursementSerializer,DrawerSelectionSerializer,ApprovedPaymentRequest
from administration.models import DrawerMaintenance
from administration.models import DrawerUserMaintenance
from administration.models import TransactiontypeMaintenance
from payment.models import PaymentRequest

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
    transaction = TransactiontypeMaintenance.objects.get(transaction_type_name="Petty Cash")
    queryset = PaymentRequest.objects.filter(status='A',transaction_type=transaction)
    serializer_class = ApprovedPaymentRequest

@login_required
def drawer_list(request):
    return render(request, 'drawer_selection.html')

@login_required
def drawer_disbursement_list(request,drawerpk):
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    return render(request, 'disbursement_list.html', {'drawer': drawer})
