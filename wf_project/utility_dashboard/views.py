from django.shortcuts import render, redirect, get_object_or_404
from .forms import UtilityApprovalForm, UtilityApproverGroupAForm, UtilityApproverGroupBForm, UtilityCCForm, UtilityRejectForm
from .models import UtilityApprovalItem, UtilityApprovalItemApprover, UtilityApprovalItemCC
from django.contrib.auth.decorators import login_required
from administration.models import DocumentTypeMaintenance, EmployeeMaintenance, EmployeePositionMaintenance
from administration.models import TransactiontypeMaintenance, EmployeeGroupMaintenance
from administration.models import WorkflowApprovalRule, WorkflowApprovalGroup, WorkflowApprovalRuleGroupMaintenance
from administration.models import StatusMaintenance,UtiliyAccountTypeMaintenance,UtiliyGroupMaintenance
from .serializers import UtilityApprovalItemSerializer, UtilityApprovalApproverSerializer, UtilityApprovalCCSerializer,AccountSelectionSerializer
from rest_framework import viewsets
from payment.models import PaymentRequest
from django.contrib.auth.models import User, Group
from django.http import JsonResponse

class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = UtilityApprovalItem.objects.all().order_by('-id')
    serializer_class = UtilityApprovalItemSerializer

    def get_queryset(self):
        approvers = UtilityApprovalItemApprover.objects.filter(user=self.request.user, status='P').values_list('utility_approval_item', flat=True)
        utility_group = get_object_or_404(UtiliyGroupMaintenance,pk=self.request.query_params.get('accountpk', None))
        utility_account = UtiliyAccountTypeMaintenance.objects.filter(utility_group=utility_group)
        return UtilityApprovalItem.objects.filter(id__in=approvers,utility_account__in=utility_account)

class ApproverViewSet(viewsets.ModelViewSet):
    queryset = UtilityApprovalItemApprover.objects.all().order_by('stage')
    serializer_class = UtilityApprovalApproverSerializer

    def get_queryset(self):
        emp_group = get_object_or_404(EmployeeGroupMaintenance, id=self.request.query_params.get('group', None))
        groups = Group.objects.filter(name=emp_group.group_name).values_list('id', flat=True)
        users = User.objects.filter(groups__in=groups).values_list('id', flat=True)        
        utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=self.request.query_params.get('pk', None))
        return UtilityApprovalItemApprover.objects.filter(user__in=users, utility_approval_item=utility_approval_item).order_by('stage')

class AllApproverViewSet(viewsets.ModelViewSet):
    queryset = UtilityApprovalItemApprover.objects.all().order_by('stage')
    serializer_class = UtilityApprovalApproverSerializer

    def get_queryset(self):      
        utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=self.request.query_params.get('pk', None))
        return UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item).order_by('stage')

class CCViewSet(viewsets.ModelViewSet):
    queryset = UtilityApprovalItemCC.objects.all()
    serializer_class = UtilityApprovalCCSerializer

    def get_queryset(self):
        utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=self.request.query_params.get('pk', None))
        return UtilityApprovalItemCC.objects.filter(utility_approval_item=utility_approval_item)

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSelectionSerializer

    def get_queryset(self):
        return UtiliyGroupMaintenance.objects.filter(is_active=True).order_by('account_group_name')

@login_required
def approval_detail(request, pk):
    utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=pk)
    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=utility_approval_item.approval_level.pk)
    approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule).order_by('id')

    if utility_approval_item != 'D':
        approvers =  UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item)
        utility_approval_item.status = 'D'
        utility_approval_item.save()

        for approver in approvers:
            approver.delete()

        document_type = get_object_or_404(DocumentTypeMaintenance, pk=utility_approval_item.document_type.pk)
        if document_type.document_type_code == "301":
            payment = get_object_or_404(PaymentRequest, pk=utility_approval_item.document_pk)
            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='100')[0]
            payment.status = status
            payment.save()

    form = UtilityApprovalForm(instance=utility_approval_item)
    form_approver_a = UtilityApproverGroupAForm()
    form_approver_b = UtilityApproverGroupBForm()
    form_cc = UtilityCCForm()

    if approval_rule_group.count() > 0:
        first_tab_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)[0]
        if first_tab_group.next_condition == 'Or':
            submitter_as_emp = get_object_or_404(EmployeeMaintenance, user=request.user)
            approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group)
            first_tab_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group)[0]

    if approval_rule_group.count() > 0:
        return render(request, 'utility_dashboard/detail.html', {'utility_approval_item': utility_approval_item, 'approval_rule': approval_rule, 'first_tab': first_tab_group,
        'approval_rule_group': approval_rule_group, 'form': form, 'form_approver_a': form_approver_a, 'form_approver_b': form_approver_b, 'form_cc': form_cc})
    else:
        return render(request, 'utility_dashboard/detail.html', {'utility_approval_item': utility_approval_item, 'approval_rule': approval_rule,
        'approval_rule_group': approval_rule_group, 'form': form, 'form_approver_a': form_approver_a, 'form_approver_b': form_approver_b, 'form_cc': form_cc})

@login_required
def approval_history(request, pk):
    utility_approval_item =  get_object_or_404(UtilityApprovalItem, pk=pk)
    # utility_account = UtiliyAccountTypeMaintenance.objects.filter(pk=accountpk)[0] 
    form = UtilityApprovalForm(instance=utility_approval_item)
    return render(request, 'utility_dashboard/history.html', {'utility_approval_item': utility_approval_item, 'form': form})

@login_required
def approval_list(request,pk):
    utility_account = UtiliyGroupMaintenance.objects.filter(pk=pk)[0] 
    form_reject = UtilityRejectForm()
    return render(request, 'utility_dashboard/list.html', {'form_reject': form_reject ,'utility_account':utility_account})

@login_required
def account_selection_list(request):
    utility_group = UtiliyGroupMaintenance.objects.filter(is_active=True)
    return render(request, 'utility_dashboard/utility_selection.html',{'utility_group':utility_group})

@login_required
def utility_bill_count(request,pk):
    utility_group = get_object_or_404(UtiliyGroupMaintenance,pk=pk)

    utility_account = UtiliyAccountTypeMaintenance.objects.filter(utility_group=utility_group).values_list('id',flat=True)

    payment_request = PaymentRequest.objects.filter(utility_account__in = utility_account).values_list('id',flat=True)

    utility_apprval_item_approver = UtilityApprovalItemApprover.objects.filter(user=request.user, status='P').values_list('utility_approval_item_id', flat=True)

    utility_approval_item = UtilityApprovalItem.objects.filter(document_pk__in=payment_request,id__in=utility_apprval_item_approver)


    return JsonResponse({'count': utility_approval_item.count()})



@login_required
def approval_update(request, pk):
    utility_approval_item =  get_object_or_404(UtilityApprovalItem, pk=pk)
    utility_approval_item.status = "IP"
    utility_approval_item.submit_by = request.user
    utility_approval_item.save()

    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=utility_approval_item.approval_level.pk)
    approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)
    
    if approval_rule.supervisor_approve:
        submiter = get_object_or_404(EmployeeMaintenance, user=request.user)
        supervisor = get_object_or_404(EmployeeMaintenance, id=submiter.reporting_officer_id.id)
        supervisor_included = UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item, user=supervisor.user).count()

        if approval_rule_group.count() > 0:
            if supervisor_included == 0:
                last_approver = UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item).order_by('-stage')[0]
                stage_count = last_approver.stage + 1
                UtilityApprovalItemApprover.objects.create(stage=stage_count, user=supervisor.user, utility_approval_item=utility_approval_item, status="Q") 
            else:
                return redirect('utility_approval_detail', pk=pk)
        else:
            if supervisor_included == 0:
                stage_count = 1
                UtilityApprovalItemApprover.objects.create(stage=stage_count, user=supervisor.user, utility_approval_item=utility_approval_item, status="P")
            else:
                return redirect('utility_approval_detail', pk=pk)
   
    if approval_rule.ceo_approve:
        ceo_position = get_object_or_404(EmployeePositionMaintenance, position_name='CHIEF EXECUTIVE OFFICER')
        ceo = get_object_or_404(EmployeeMaintenance, position_id=ceo_position)
        ceo_included = UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item, user=ceo.user).count()

        if ceo_included == 0:
            last_approver = UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item).order_by('-stage')[0]
            stage_count = last_approver.stage + 1
            UtilityApprovalItemApprover.objects.create(stage=stage_count, user=ceo.user, utility_approval_item=utility_approval_item, status="Q") 

    document_type = get_object_or_404(DocumentTypeMaintenance, pk=utility_approval_item.document_type.pk)
    if document_type.document_type_code == "301":
        payment = get_object_or_404(PaymentRequest, pk=utility_approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='300')[0]
        payment.status = status
        payment.save()
        trans_name = payment.transaction_type.transaction_type_name
        return redirect('pylist',payment.transaction_type.pk)
    
    return redirect(approval_list)

@login_required
def approve(request):
    approver_item = get_object_or_404(UtilityApprovalItemApprover, user=request.user.id, utility_approval_item=request.POST['hiddenValueApprove'])
    approver_item.status = "A"
    approver_item.save()

    approvers = UtilityApprovalItemApprover.objects.filter(utility_approval_item=request.POST['hiddenValueApprove']).count()
    approvers_approve = UtilityApprovalItemApprover.objects.filter(utility_approval_item=request.POST['hiddenValueApprove'], status="A").count()

    if approvers == approvers_approve:
        utility_approval_item =  get_object_or_404(UtilityApprovalItem, pk=request.POST['hiddenValueApprove'])
        utility_approval_item.status = "A"
        utility_approval_item.save()

        document_type = get_object_or_404(DocumentTypeMaintenance, pk=utility_approval_item.document_type.pk)
        if document_type.document_type_code == "301":
            payment = get_object_or_404(PaymentRequest, pk=utility_approval_item.document_pk)
            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            payment.status = status
            payment.save()
    else:
        next_approver = get_object_or_404(UtilityApprovalItemApprover, stage=approver_item.stage + 1, utility_approval_item=request.POST['hiddenValueApprove'])
        next_approver.status = "P"
        next_approver.save()

    return JsonResponse({'message': 'Success'})

@login_required
def approve_all(request,pk):
    approver_item = get_object_or_404(UtilityApprovalItemApprover, user=request.user.id, utility_approval_item=pk)
    approver_item.status = "A"
    approver_item.save()

    approvers = UtilityApprovalItemApprover.objects.filter(utility_approval_item=pk).count()
    approvers_approve = UtilityApprovalItemApprover.objects.filter(utility_approval_item=pk, status="A").count()

    if approvers == approvers_approve:
        utility_approval_item =  get_object_or_404(UtilityApprovalItem, pk=pk)
        utility_approval_item.status = "A"
        utility_approval_item.save()

        document_type = get_object_or_404(DocumentTypeMaintenance, pk=utility_approval_item.document_type.pk)
        if document_type.document_type_code == "301":
            payment = get_object_or_404(PaymentRequest, pk=utility_approval_item.document_pk)
            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            payment.status = status
            payment.save()
    else:
        next_approver = get_object_or_404(UtilityApprovalItemApprover, stage=approver_item.stage + 1, utility_approval_item=pk)
        next_approver.status = "P"
        next_approver.save()

    return JsonResponse({'message': 'Success'})


@login_required
def stage_count(utility_approval_item, previous_approval_group, approval_group):    
    if previous_approval_group.id != approval_group.id:
        previous_groups = Group.objects.filter(name=previous_approval_group.user_group.group_name).values_list('id', flat=True)
        previous_users = User.objects.filter(groups__in=previous_groups).values_list('id', flat=True)
        return UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item, user__in=previous_users).count()
    else:
        return 0

@login_required
def approver_create(request, pk):
    group_name = request.POST['hiddenGroupName']

    if group_name == 'Group A':
        form = UtilityApproverGroupAForm(request.POST)
    else:
        form = UtilityApproverGroupBForm(request.POST)

    utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=pk)
    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=utility_approval_item.approval_level.pk)
    approval_group = get_object_or_404(WorkflowApprovalGroup, pk=request.POST['hiddenGroupId'])
    first_tab_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)[0]
    
    if approval_rule.supervisor_approve:
        selected_user = get_object_or_404(User, pk=request.POST['user'])
        submiter = get_object_or_404(EmployeeMaintenance, user=request.user)
        supervisor = get_object_or_404(EmployeeMaintenance, id=submiter.reporting_officer_id.id)
        supervisor_user = get_object_or_404(User, pk=supervisor.user.id)
        if supervisor_user == selected_user:
            return JsonResponse({'message': 'The selected approver cannot be your reporting officer.'})

    previous_approval_group = first_tab_rule_group.approval_group
    previous_groups = Group.objects.filter(name=previous_approval_group.user_group.group_name).values_list('id', flat=True)
    previous_users = User.objects.filter(groups__in=previous_groups).values_list('id', flat=True)
    previous_approver_count = UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item).count()
    
    if first_tab_rule_group.next_condition == 'Or':
        submitter_as_emp = get_object_or_404(EmployeeMaintenance, user=request.user)
        first_tab_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group)[0]
    else:
        if previous_approver_count == 0 and previous_approval_group.user_group.group_name != group_name:
            return JsonResponse({'message': 'Need ' + previous_approval_group.approval_group_name + ' approver(s) to proceed'})
       
    groups = Group.objects.filter(name=group_name).values_list('id', flat=True)
    users = User.objects.filter(groups__in=groups).values_list('id', flat=True)
    current_approvers = UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item, user__in=users).count()

    if first_tab_rule_group.next_condition == 'Or':
        previous_approver_count = 0

    if previous_approver_count > 0 and previous_approval_group.user_group.group_name == group_name:
        previous_approvers = UtilityApprovalItemApprover.objects.filter(approval_item=utility_approval_item)    
        previous_approvers_same_group_count = 0

        for approver in previous_approvers:
            employee = get_object_or_404(EmployeeMaintenance, user_id=approver.user.id)
            employee_group = get_object_or_404(EmployeeGroupMaintenance, pk=employee.employee_group.id)

            if employee_group.group_name == group_name:
                previous_approvers_same_group_count = previous_approvers_same_group_count + 1

        previous_approver_count = previous_approvers_same_group_count

    if current_approvers < approval_group.no_of_person:
        if form.is_valid():
            user = get_object_or_404(User, pk=request.POST['user'])

            approver = form.save(commit=False)
            approver.utility_approval_item = utility_approval_item
            approver.stage = previous_approver_count + current_approvers + 1
            approver.user = user
            approver.save()

            group_order = Group.objects.all().values_list('id', flat=True)
            users_order = User.objects.filter(groups__in = groups).values_list('id', flat=True).order_by('group.id')
            approvers = UtilityApprovalItemApprover.objects.filter(utility_approval_item=utility_approval_item).order_by('stage')
            count = 1

            for approver in approvers:
                if count == 1:
                    approver.status = "P"
                else:
                    approver.status = "Q"
                
                approver.save()
                count = count + 1

        return JsonResponse({'message': 'Success'})
    else:
        return JsonResponse({'message': 'Only ' + approval_group.approval_group_name + ' approver(s) needed for approval'})

@login_required
def approver_delete(request):
    approver = get_object_or_404(UtilityApprovalItemApprover, pk=request.POST['hiddenValueApprover' + request.POST['hiddenDeleteGroupId']])
    approver.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def cc_create(request, pk):
    form = UtilityCCForm(request.POST)
    if form.is_valid():
        utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=pk)
        user = get_object_or_404(User, pk=request.POST['user'])

        cc = form.save(commit=False)
        cc.user = user
        cc.utility_approval_item = utility_approval_item
        cc.save()

    return JsonResponse({'message': 'Success'})

@login_required
def cc_delete(request):
    cc = get_object_or_404(UtilityApprovalItemCC, pk=request.POST['hiddenValueCC'])
    cc.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def reject(request):
    form = UtilityRejectForm(request.POST)
    if form.is_valid():
        approver_item = get_object_or_404(UtilityApprovalItemApprover, user=request.user.id, utility_approval_item=form.cleaned_data['hiddenValueReject'])
        approver_item.status = "R"
        approver_item.reason = form.cleaned_data['reason']
        approver_item.save()

        approvers = UtilityApprovalItemApprover.objects.filter(utility_approval_item=form.cleaned_data['hiddenValueReject'])
        for approver in approvers:
            approver.status = "R"
            approver.save()

    utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=form.cleaned_data['hiddenValueReject'])
    utility_approval_item.status = "R"
    utility_approval_item.save()

    document_type = get_object_or_404(DocumentTypeMaintenance, pk=utility_approval_item.document_type.pk)
    if document_type.document_type_code == "301":
        payment = get_object_or_404(PaymentRequest, pk=utility_approval_item.document_pk)
        document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        payment.status = status
        payment.save()

    return JsonResponse({'message': 'Success'})

@login_required
def reject_all(request,pk):
    
    approver_item = get_object_or_404(UtilityApprovalItemApprover, user=request.user.id, utility_approval_item=pk)
    approver_item.status = "R"
    # approver_item.reason = form.cleaned_data['reason']
    approver_item.save()

    approvers = UtilityApprovalItemApprover.objects.filter(utility_approval_item=pk)
    for approver in approvers:
        approver.status = "R"
        approver.save()

    utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=pk)
    utility_approval_item.status = "R"
    utility_approval_item.save()

    document_type = get_object_or_404(DocumentTypeMaintenance, pk=utility_approval_item.document_type.pk)

    if document_type.document_type_code == "301":
        payment = get_object_or_404(PaymentRequest, pk=utility_approval_item.document_pk)
        document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        payment.status = status
        payment.save()

    return JsonResponse({'message': 'Success'})