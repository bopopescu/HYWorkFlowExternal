from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApprovalForm, ApproverForm, CCForm
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from django.contrib.auth.decorators import login_required
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from .serializers import ApprovalApproverSerializer, ApprovalCCSerializer
from rest_framework import viewsets
from memo.models import Memo

class ApproverViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemApprover.objects.all()
    serializer_class = ApprovalApproverSerializer
    
class CCViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemCC.objects.all()  
    serializer_class = ApprovalCCSerializer

@login_required
def approval_detail(request, pk):
    approval_item =  get_object_or_404(ApprovalItem, pk=pk)
    form = ApprovalForm(instance=approval_item)
    form_approver = ApproverForm()
    form_cc = CCForm()
    return render(request, 'approval/detail.html', {'approval_item': approval_item, 'form': form, 'form_approver': form_approver, 'form_cc': form_cc})

@login_required
def approval_list(request):
    return render(request, 'approval/list.html')

@login_required
def approval_update(request, pk):
    approval_item =  get_object_or_404(WorkflowApprovalRule, pk=pk)
    approval_item.status = "IP"
    approval_item.save()
    return redirect(approval_list)

@login_required
def approver_create(request, pk):
    form = ApproverForm(request.POST)
    if form.is_valid():
        approver = form.save(commit=False)
        approval_item = get_object_or_404(ApprovalItem, pk=pk)
        approver.approval_item = approval_item
        approver.save()
    
    return redirect(approval_detail, pk)

@login_required
def cc_create(request, pk):
    form = CCForm(request.POST)
    if form.is_valid():
        cc= form.save(commit=False)
        approval_item = get_object_or_404(ApprovalItem, pk=pk)
        cc.approval_item = approval_item
        cc.save()

    return redirect(approval_detail, pk)