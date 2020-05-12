from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewReimbursementForm,UpdateReimbursementForm,DetailReimbursementForm
from django.contrib.auth.decorators import login_required
from .models import ReimbursementRequest,DrawerReimbursement
from rest_framework import viewsets
from .serializers import ReimbursementRequestSerializer,DrawerSelectionSerializer,DrawerReimbursedSerializer,ApprovedReimburserdRequest
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import StatusMaintenance
from administration.models import EmployeeMaintenance
from administration.models import DrawerMaintenance
from administration.models import DrawerUserMaintenance
from approval.models import ApprovalItem
from approval.forms import RejectForm
from django.contrib.auth.models import User
import datetime
from django.http import JsonResponse
from django.utils.datetime_safe import date
import decimal

# Create your views here.
class MyReimbursementRequestViewSet(viewsets.ModelViewSet):

    serializer_class = ReimbursementRequestSerializer
    
    def get_queryset(self):
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return ReimbursementRequest.objects.filter(submit_by=self.request.user.id).order_by("-id")

class TeamReimbursementRequestViewSet(viewsets.ModelViewSet):

    serializer_class = ReimbursementRequestSerializer

    def get_queryset(self):
        document_type = get_object_or_404(DocumentTypeMaintenance,document_type_code="504")
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return ReimbursementRequest.objects.filter(submit_by__in=users)

class DrawerViewSet(viewsets.ModelViewSet):
    queryset = DrawerMaintenance.objects.all().order_by('-id')
    serializer_class = DrawerSelectionSerializer

    def get_queryset(self):
        drawer_user = DrawerUserMaintenance.objects.filter(user=self.request.user).values_list('drawer', flat=True)
        return DrawerMaintenance.objects.filter(id__in=drawer_user,drawer_status='O').order_by('-id')

class ReimbursementListViewSet(viewsets.ModelViewSet):
    serializer_class = ApprovedReimburserdRequest
    
    def get_queryset(self):
        document_type = DocumentTypeMaintenance.objects.get(document_type_code='403')
        document_status_approve = StatusMaintenance.objects.get(document_type=document_type,status_code='400')
        drawer = get_object_or_404(DrawerMaintenance, pk=self.request.query_params.get('drawerpk', None))
        return ReimbursementRequest.objects.filter(status=document_status_approve,drawer=drawer)


class ReimbursedViewSet(viewsets.ModelViewSet):
    serializer_class = DrawerReimbursedSerializer

    def get_queryset(self):
        drawer = get_object_or_404(DrawerMaintenance, pk=self.request.query_params.get('drawerpk', None))
        document_type = DocumentTypeMaintenance.objects.get(document_type_code='401')
        document_status_reimburse = StatusMaintenance.objects.get(document_type=document_type,status_code='700')
        return DrawerReimbursement.objects.filter(status=document_status_reimburse,drawer=drawer)

class CancelledViewSet(viewsets.ModelViewSet):
    serializer_class = DrawerReimbursedSerializer
    
    def get_queryset(self):
        drawer = get_object_or_404(DrawerMaintenance, pk=self.request.query_params.get('drawerpk', None))
        document_type = DocumentTypeMaintenance.objects.get(document_type_code='401')
        document_status_reimburse = StatusMaintenance.objects.get(document_type=document_type,status_code='999')
        return DrawerReimbursement.objects.filter(status=document_status_reimburse,drawer=drawer)

@login_required
def reimbursement_request_init(request):    
    # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    reimburement_request = ReimbursementRequest.objects.create(submit_by=request.user)
    return redirect(reimbursement_request_create, reimburement_request.pk)

@login_required
def reimbursement_request_init_amount(request,amount):    
    reimburse_request = get_object_or_404(TransactiontypeMaintenance,transaction_type_name="Reimbursement Request")
    reimburement_request = ReimbursementRequest.objects.create(submit_by=request.user,request_amount=amount,transaction_type=reimburse_request)
    return redirect(reimbursement_request_create, reimburement_request.pk)

@login_required
def reimbursement_request_create(request, pk):    
    reimburement_request = get_object_or_404(ReimbursementRequest, pk=pk)
    if request.method == 'POST':
        form = NewReimbursementForm(request.POST, instance=reimburement_request)
        if form.is_valid():

            reimburement_request_type = DocumentTypeMaintenance.objects.filter(document_type_code="403")[0]
            document_number = reimburement_request_type.running_number + 1
            reimburement_request_type.running_number = document_number 
            reimburement_request_type.save()

            drawer = form.cleaned_data['drawer']
            transaction_type = form.cleaned_data['transaction_type']

            status = get_object_or_404(StatusMaintenance, document_type=reimburement_request_type, status_code="100")

            reimburement_request.document_number = '{0}-{1:05d}'.format(reimburement_request_type.document_type_code,document_number)
            reimburement_request.drawer = drawer
            reimburement_request.status = status
            reimburement_request.submit_by = request.user
            reimburement_request.transaction_type = transaction_type
            reimburement_request.save()

            # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=transaction_type.pk ,document_type=staff_ot_type)

            approval_item = ApprovalItem()        
            approval_item.document_number = reimburement_request.document_number
            approval_item.document_pk = reimburement_request.pk
            approval_item.document_type = reimburement_request_type
            approval_item.transaction_type = transaction_type
            approval_item.status = "D"
            approval_item.save()

            reimburement_request.approval = approval_item
            reimburement_request.save()

            return redirect(reimbursement_request_update, pk=reimburement_request.pk)
        else:
            print(form.errors)
            form = NewReimbursementForm(instance=reimburement_request)
    else:
        form = NewReimbursementForm(instance=reimburement_request)
    return render(request, 'reimbursement_request/create.html', {'reimburse': reimburement_request, 'form': form})

@login_required
def reimbursement_request_send_approval(request,pk):
    reimbursement_request = get_object_or_404(ReimbursementRequest, pk=pk)
    approval_level = WorkflowApprovalRule.objects.filter(document_amount_range2__gte=reimbursement_request.request_amount, document_amount_range__lte=reimbursement_request.request_amount)[0]
    approval_item = get_object_or_404(ApprovalItem, pk=reimbursement_request.approval.pk)       
    approval_item.approval_level = approval_level
    if approval_level.ceo_approve == True:
        approval_item.notification = "CEO will added by default"

    approval_item.save()

    return redirect('approval_detail', pk=approval_item.pk)

@login_required
def reimbursement_request_detail(request, pk):
    reimbursement_request =  get_object_or_404(ReimbursementRequest, pk=pk)
    form = DetailReimbursementForm(instance=reimbursement_request)
    form_reject = RejectForm()
    return render(request, 'reimbursement_request/detail.html', {'reimburse': reimbursement_request, 'form': form, 'form_reject': form_reject})

@login_required
def reimbursement_request_list(request):
    # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'reimbursement_request/list.html')

@login_required
def reimbursement_request_update(request, pk):
    reimburement_request = get_object_or_404(ReimbursementRequest, pk=pk)
    if request.method == 'POST':
        form = UpdateReimbursementForm(request.POST, instance=reimburement_request)
        status = reimburement_request.status
        reimburement_request = form.save()
        reimburement_request.status = status
        reimburement_request.save()
        return redirect('reimbursement_request_detail', pk=reimburement_request.pk)
    else:
        form = UpdateReimbursementForm(instance=reimburement_request)
    return render(request, 'reimbursement_request/update.html', {'reimburse': reimburement_request, 'form': form})

@login_required
def reimbursement_request_delete(request):
    reimburement_request =  get_object_or_404(ReimbursementRequest, pk=request.POST['hiddenValue'])
    reimburement_request.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def drawer_list(request):
    return render(request, 'drawer_reimbursement/reimbursement_drawer_selection.html')

@login_required
def drawer_reimbursement_list(request,drawerpk):
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    return render(request, 'drawer_reimbursement/reimbursement_list.html', {'drawer': drawer})


@login_required
def drawer_reimbursement_reimbursed(request,pk,drawerpk):
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='403')
    document_status_closed = StatusMaintenance.objects.get(document_type=document_type,status_code='600')
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    reimbursed_request = ReimbursementRequest.objects.get(pk=pk)

    reimbursed_request.status = document_status_closed

    document_type_reimbursed = DocumentTypeMaintenance.objects.get(document_type_code='401')
    document_status_reimbursed = StatusMaintenance.objects.get(document_type=document_type_reimbursed,status_code='700')

    reimbursedrecord = DrawerReimbursement()
    reimbursedrecord.reimbursement_request = reimbursed_request
    reimbursedrecord.total_reimburse = reimbursed_request.request_amount
    reimbursedrecord.status = document_status_reimbursed
    reimbursedrecord.drawer = drawer
    reimbursedrecord.save()
    reimbursed_request.save()
    return JsonResponse({'message': 'Success'})

@login_required
def drawer_reimbursement_cancel(request,pk,drawerpk):
    
    document_type = DocumentTypeMaintenance.objects.get(document_type_code='403')
    document_status_closed = StatusMaintenance.objects.get(document_type=document_type,status_code='600')
    drawer = DrawerMaintenance.objects.get(pk=drawerpk)
    reimbursed_request = ReimbursementRequest.objects.get(pk=pk)

    reimbursed_request.status = document_status_closed

    document_type_reimbursed = DocumentTypeMaintenance.objects.get(document_type_code='401')
    document_status_cancel = StatusMaintenance.objects.get(document_type=document_type_reimbursed,status_code='999')

    reimbursedrecord = DrawerReimbursement()
    reimbursedrecord.reimbursement_request = reimbursed_request
    reimbursedrecord.total_reimburse = reimbursed_request.request_amount
    reimbursedrecord.status = document_status_cancel
    reimbursedrecord.drawer = drawer
    reimbursedrecord.save()
    return JsonResponse({'message': 'Success'})