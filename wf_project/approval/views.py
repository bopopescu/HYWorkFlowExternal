from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApprovalForm, ApproverForm, CCForm, RejectForm
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from django.contrib.auth.decorators import login_required
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule, WorkflowApprovalGroup, WorkflowApprovalRuleGroupMaintenance
from administration.models import StatusMaintenance
from .serializers import ApprovalItemSerializer, ApprovalApproverSerializer, ApprovalCCSerializer
from rest_framework import viewsets
from memo.models import Memo
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest
from django.http import JsonResponse

class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItem.objects.all().order_by('-id')
    serializer_class = ApprovalItemSerializer

    def get_queryset(self):
        approvers = ApprovalItemApprover.objects.filter(user=self.request.user,status='P').values_list('approval_item', flat=True)
        return ApprovalItem.objects.filter(id__in=approvers)

class ApproverViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemApprover.objects.all()
    serializer_class = ApprovalApproverSerializer

class CCViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemCC.objects.all()  
    serializer_class = ApprovalCCSerializer

@login_required
def approval_detail(request, pk):
    approval_item = get_object_or_404(ApprovalItem, pk=pk)
    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=approval_item.approval_level.pk)
    approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule).order_by('id')
    first_tab_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)[0]
    
    form = ApprovalForm(instance=approval_item)
    form_approver = ApproverForm()
    form_cc = CCForm()

    return render(request, 'approval/detail.html', {'approval_item': approval_item, 'approval_rule': approval_rule, 'first_tab': first_tab_group,
    'approval_rule_group': approval_rule_group, 'form': form, 'form_approver': form_approver, 'form_cc': form_cc})

@login_required
def approval_history(request, pk):
    approval_item =  get_object_or_404(ApprovalItem, pk=pk)
    form = ApprovalForm(instance=approval_item)
    return render(request, 'approval/history.html', {'approval_item': approval_item, 'form': form})

@login_required
def approval_list(request):
    form_reject = RejectForm()
    return render(request, 'approval/list.html', {'form_reject': form_reject})

@login_required
def approval_update(request, pk):
    approval_item =  get_object_or_404(ApprovalItem, pk=pk)
    approval_item.status = "IP"
    approval_item.save()

    document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
    if document_type.document_type_name == "Memo":
        memo = get_object_or_404(Memo, pk=approval_item.document_pk)
        memo.status = "P"
        memo.save()
        return redirect('memo_list')
    if document_type.document_type_name == "Payment Request":
        payment = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
        document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
        status = StatusMaintenance.objects.filter(document_type=document_type,status_code='300')[0]
        payment.status = status
        payment.save()
        trans_name = payment.transaction_type.transaction_type_name
        if trans_name == "Other":
            return redirect('pylist')
        elif trans_name == "Petty Cash":
            return redirect('pylist_pettycash')
        elif trans_name == "CashBack n Rebates":
            return redirect('pylist_cashback')
        elif trans_name == "Sales Commission":
            return redirect('pylist_salescommission')
        return redirect('pylist')
    if document_type.document_type_name == "Staff Recruitment Request":
        staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
        staff.status = "P"
        staff.save()
        return redirect('staff_list')

    return redirect(approval_list)

@login_required
def approve(request, pk):
    approver_item = get_object_or_404(ApprovalItemApprover, user=request.user.id, approval_item=pk)
    approver_item.status = "A"
    approver_item.save()

    approvers = ApprovalItemApprover.objects.filter(approval_item=pk).count()
    approvers_approve = ApprovalItemApprover.objects.filter(approval_item=pk, status="A").count()

    if approvers == approvers_approve:
        approval_item =  get_object_or_404(ApprovalItem, pk=pk)
        approval_item.status = "A"
        approval_item.save()

        document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
        if document_type.document_type_name == "Memo":
            memo = get_object_or_404(Memo, pk=approval_item.document_pk)
            memo.status = "A"
            memo.save()
        if document_type.document_type_name == "Payment Request":
            payment = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
            status = StatusMaintenance.objects.filter(document_type=document_type,status_code='400')[0]
            payment.status = status
            payment.save()
        if document_type.document_type_name == "Staff Recruitment Request":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
            staff.status = "A"
            staff.save()

    return redirect(approval_list)

@login_required
def approver_create(request, pk):
    form = ApproverForm(request.POST)
    if form.is_valid():
        approver = form.save(commit=False)
        approval_item = get_object_or_404(ApprovalItem, pk=pk)
        approver.approval_item = approval_item
        approver.status = "P"
        approver.save()
    
    return JsonResponse({'message': 'Success'})

@login_required
def approver_delete(request):
    approver =  get_object_or_404(ApprovalItemApprover, pk=request.POST['hiddenValueApprover'])
    approver.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def cc_create(request, pk):
    form = CCForm(request.POST)
    if form.is_valid():
        cc= form.save(commit=False)
        approval_item = get_object_or_404(ApprovalItem, pk=pk)
        cc.approval_item = approval_item
        cc.save()

    return JsonResponse({'message': 'Success'})

@login_required
def cc_delete(request):
    cc =  get_object_or_404(ApprovalItemCC, pk=request.POST['hiddenValueCC'])
    cc.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def reject(request):
    form = RejectForm(request.POST)
    if form.is_valid():
        approver_item = get_object_or_404(ApprovalItemApprover, user=request.user.id, approval_item=form.cleaned_data['hiddenValueReject'])
        approver_item.status = "R"
        approver_item.reason = form.cleaned_data['reason']
        approver_item.save()

        approval_item = get_object_or_404(ApprovalItem, pk=form.cleaned_data['hiddenValueReject'])
        approval_item.status = "R"
        approval_item.save()

    document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
    if document_type.document_type_name == "Memo":
        memo = get_object_or_404(Memo, pk=approval_item.document_pk)
        memo.status = "R"
        memo.save()
    if document_type.document_type_name == "Payment Request":
        payment = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
        document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
        status = StatusMaintenance.objects.filter(document_type=document_type,status_code='500')[0]
        payment.status = status
        payment.save()
    if document_type.document_type_name == "Staff Recruitment Request":
        staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
        staff.status = "R"
        staff.save()

    return redirect(approval_list)