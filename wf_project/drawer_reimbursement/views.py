from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewReimbursementForm,UpdateReimbursementForm,DetailReimbursementForm
from django.contrib.auth.decorators import login_required
from .models import ReimbursementRequest
from rest_framework import viewsets
from .serializers import ReimbursementRequestSerializer
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import StatusMaintenance
from administration.models import EmployeeMaintenance
from administration.models import DrawerMaintenance
from approval.models import ApprovalItem
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
        return ReimbursementRequest.objects.filter(submit_by=self.request.user.id)

class TeamReimbursementRequestViewSet(viewsets.ModelViewSet):

    serializer_class = ReimbursementRequestSerializer

    def get_queryset(self):
        document_type = get_object_or_404(DocumentTypeMaintenance,document_type_code="504")
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return ReimbursementRequest.objects.filter(submit_by__in=users)

@login_required
def reimbursement_request_init(request):    
    # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    reimburement_request = ReimbursementRequest.objects.create(submit_by=request.user)
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
    return render(request, 'reimbursement_request/detail.html', {'reimburse': reimbursement_request, 'form': form})

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