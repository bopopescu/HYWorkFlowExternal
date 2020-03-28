from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApprovalForm
from .models import ApprovalItem
from django.contrib.auth.decorators import login_required
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from memo.models import Memo

@login_required
def approval_detail(request, pk):
    approval_item =  get_object_or_404(ApprovalItem, pk=pk)
    form = ApprovalForm(instance=approval_item)
    return render(request, 'approval/detail.html', {'approval_item': approval_item, 'form': form})

@login_required
def approval_list(request):
    return render(request, 'approval/list.html')

@login_required
def approval_update(request, pk):
    approval_item =  get_object_or_404(WorkflowApprovalRule, pk=pk)
    approval_item.status = "IP"
    approval_item.save()
    return redirect(approval_list)