from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApprovalForm, ApproverGroupAForm, ApproverGroupBForm, CCForm, RejectForm,ApproverGroupAAndBForm
from .models import ApprovalItem, ApprovalItemApprover, ApprovalItemCC
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
from administration.models import DocumentTypeMaintenance, EmployeeMaintenance, EmployeePositionMaintenance
from administration.models import TransactiontypeMaintenance, EmployeeGroupMaintenance
from administration.models import WorkflowApprovalRule, WorkflowApprovalGroup, WorkflowApprovalRuleGroupMaintenance
from administration.models import StatusMaintenance
from .serializers import ApprovalItemSerializer, ApprovalApproverSerializer, ApprovalCCSerializer
from rest_framework import viewsets
from memo.models import Memo
from purchasing.models import PurchaseOrder
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest
from staff_overtime.models import StaffOT
from drawer_reimbursement.models import ReimbursementRequest
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
import datetime

class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItem.objects.all().order_by('-id')
    serializer_class = ApprovalItemSerializer

    def get_queryset(self):
        approvers = ApprovalItemApprover.objects.filter(user=self.request.user, status='P').values_list('approval_item', flat=True)
        return ApprovalItem.objects.filter(id__in=approvers,status="IP").annotate(row_number=Window(expression=RowNumber(), order_by=F('id').desc())).order_by('-id')

class ApproverViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemApprover.objects.all().order_by('stage')
    serializer_class = ApprovalApproverSerializer

    def get_queryset(self):
        emp_group = get_object_or_404(EmployeeGroupMaintenance, id=self.request.query_params.get('group', None))
        groups = Group.objects.filter(name=emp_group.group_name).values_list('id', flat=True)
        users = User.objects.filter(groups__in=groups).values_list('id', flat=True)        
        approval_item = get_object_or_404(ApprovalItem, pk=self.request.query_params.get('pk', None))
        return ApprovalItemApprover.objects.filter(user__in=users, approval_item=approval_item).order_by('stage')

class ApproverSupervisorViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemApprover.objects.all().order_by('stage')
    serializer_class = ApprovalApproverSerializer

    def get_queryset(self):        
        approval_item = get_object_or_404(ApprovalItem, pk=self.request.query_params.get('pk', None))
        return ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('stage')

class AllApproverViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemApprover.objects.all().order_by('stage')
    serializer_class = ApprovalApproverSerializer

    def get_queryset(self):      
        approval_item = get_object_or_404(ApprovalItem, pk=self.request.query_params.get('pk', None))
        return ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('stage')

class CCViewSet(viewsets.ModelViewSet):
    queryset = ApprovalItemCC.objects.all()
    serializer_class = ApprovalCCSerializer

    def get_queryset(self):
        approval_item = get_object_or_404(ApprovalItem, pk=self.request.query_params.get('pk', None))
        return ApprovalItemCC.objects.filter(approval_item=approval_item)

@login_required
def approval_detail(request, pk):
    approval_item = get_object_or_404(ApprovalItem, pk=pk)
    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=approval_item.approval_level.pk)
    approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule).order_by('id')

    if approval_item != 'D':
        approvers =  ApprovalItemApprover.objects.filter(approval_item=approval_item)
        approval_item.status = 'D'
        approval_item.save()

        for approver in approvers:
            approver.delete()
        
        #insert supervisor detail before go into approval detail screen
        if approval_rule.supervisor_approve:
            submiter = get_object_or_404(EmployeeMaintenance, user=request.user)
            supervisor = get_object_or_404(EmployeeMaintenance, id=submiter.reporting_officer_id.id)
            supervisor_included = ApprovalItemApprover.objects.filter(approval_item=approval_item, user=supervisor.user).count()

            # if approval_rule_group.count() > 0:
            if approval_rule.ceo_approve_overwrite == True:
                if supervisor_included == 0:
                    ApprovalItemApprover.objects.create(stage=1, user=supervisor.user, approval_item=approval_item, status="P")
                    if supervisor.employee_group.group_name != "Group A":
                        last_approver = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('-stage')[0]
                        stage_count = last_approver.stage + 1
                        supervisor_employee = get_object_or_404(EmployeeMaintenance, user=request.user)
                        supervisor_of_reporting_manager = get_object_or_404(EmployeeMaintenance, id=supervisor_employee.reporting_officer_id.id)
                        second_approver = supervisor_of_reporting_manager
                        
                        while True:
                            if second_approver.employee_group.group_name == "Group A":
                                second_approver = second_approver
                                break
                            else: 
                                supervisor_employee = get_object_or_404(EmployeeMaintenance, user=request.user)
                                supervisor_of_reporting_manager = get_object_or_404(EmployeeMaintenance, id=second_approver.reporting_officer_id.id)
                                second_approver = supervisor_of_reporting_manager

                        ApprovalItemApprover.objects.create(stage=stage_count, user=second_approver.user, approval_item=approval_item, status="Q") 
            else:
                if supervisor_included == 0:
                    stage_count = 1
                    ApprovalItemApprover.objects.create(stage=stage_count, user=supervisor.user, approval_item=approval_item, status="P")
                

        document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
        if document_type.document_type_code == "601":
            memo = get_object_or_404(Memo, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='100')[0]
            memo.status = status
            memo.save()
        elif document_type.document_type_code == "205":
            po = get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='100')[0]
            po.status = status
            po.save()
        elif document_type.document_type_code == "301":
            payment = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='100')[0]
            payment.status = status
            payment.save()
        elif document_type.document_type_code == "501":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='100')[0]
            staff.status = status
            staff.save()
        elif document_type.document_type_code == "504":
            staff_ot = get_object_or_404(StaffOT, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='100')[0]
            staff_ot.status = status
            staff_ot.save()

    form = ApprovalForm(instance=approval_item)
    form_approver_a = ApproverGroupAForm()
    form_approver_b = ApproverGroupBForm()
    form_approver_a_b = ApproverGroupAAndBForm(request.user)
    form_cc = CCForm()

    if approval_rule_group.count() > 0:
        first_tab_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)[0]
        if first_tab_group.next_condition == 'Or':
            submitter_as_emp = get_object_or_404(EmployeeMaintenance, user=request.user)
            approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group,approval_rule=approval_rule)
            first_tab_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group,approval_rule=approval_rule)[0]

    if approval_rule_group.count() > 0:
        return render(request, 'approval/detail.html', {'approval_item': approval_item, 'approval_rule': approval_rule, 'first_tab': first_tab_group, 
        'approval_rule_group': approval_rule_group, 'form': form, 'form_approver_a': form_approver_a, 'form_approver_b': form_approver_b,'form_approver_a_b':form_approver_a_b, 'form_cc': form_cc})
    else:
        return render(request, 'approval/detail.html', {'approval_item': approval_item, 'approval_rule': approval_rule, 
        'approval_rule_group': approval_rule_group, 'form': form, 'form_approver_a': form_approver_a, 'form_approver_b': form_approver_b,'form_approver_a_b':form_approver_a_b,'form_cc': form_cc})

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
    approval_rule_valid = approval_item.approval_level
    if approval_rule_valid.supervisor_approve == False:
        # print(approval_rule_valid.approval_level)
        # print(count_approver_needed(request,approval_rule_valid.pk))
        approver_needed = int(count_approver_needed(request,approval_rule_valid.pk))
        validation_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()
        if validation_count < approver_needed:
            urls = "/approval/detail/"+str(approval_item.pk)+"/?error=True"
            return redirect(urls)
    else:
        validation_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()
        if validation_count <= 0:
            urls = "/approval/detail/"+str(approval_item.pk)+"/?error=True"
            return redirect(urls)

    approval_item.status = "IP"
    approval_item.submit_by = request.user
    approval_item.save()

    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=approval_item.approval_level.pk)
    approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)
    
    # if approval_rule.supervisor_approve:
    #     submiter = get_object_or_404(EmployeeMaintenance, user=request.user)
    #     supervisor = get_object_or_404(EmployeeMaintenance, id=submiter.reporting_officer_id.id)
    #     supervisor_included = ApprovalItemApprover.objects.filter(approval_item=approval_item, user=supervisor.user).count()

    #     # if approval_rule_group.count() > 0:
    #     if approval_rule.ceo_approve_overwrite == True:
    #         if supervisor_included == 0:
    #             # validation_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()
    #             # if validation_count <= 0:
    #             #     urls = "/approval/detail/"+str(approval_item.pk)+"/?error=True"
    #             #     return redirect(urls)
    #             ApprovalItemApprover.objects.create(stage=1, user=supervisor.user, approval_item=approval_item, status="P")
    #             if supervisor.employee_group.group_name != "Group A":
    #                 last_approver = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('-stage')[0]
    #                 stage_count = last_approver.stage + 1
    #                 supervisor_employee = get_object_or_404(EmployeeMaintenance, user=request.user)
    #                 supervisor_of_reporting_manager = get_object_or_404(EmployeeMaintenance, id=supervisor_employee.reporting_officer_id.id)
    #                 second_approver = supervisor_of_reporting_manager
                    
    #                 while True:
    #                     if second_approver.employee_group.group_name == "Group A":
    #                         second_approver = second_approver
    #                         break
    #                     else: 
    #                         supervisor_employee = get_object_or_404(EmployeeMaintenance, user=request.user)
    #                         supervisor_of_reporting_manager = get_object_or_404(EmployeeMaintenance, id=second_approver.reporting_officer_id.id)
    #                         second_approver = supervisor_of_reporting_manager

    #                 ApprovalItemApprover.objects.create(stage=stage_count, user=second_approver.user, approval_item=approval_item, status="Q") 
    #         else:
    #             return redirect('approval_detail', pk=pk)
    #     else:
    #         if supervisor_included == 0:
    #             stage_count = 1
    #             ApprovalItemApprover.objects.create(stage=stage_count, user=supervisor.user, approval_item=approval_item, status="P")
    #         else:
    #             return redirect('approval_detail', pk=pk)
   
    if approval_rule.ceo_approve:
        ceo_position = get_object_or_404(EmployeePositionMaintenance, position_name='CHIEF EXECUTIVE OFFICER')
        ceo = get_object_or_404(EmployeeMaintenance, position_id=ceo_position)
        ceo_included = ApprovalItemApprover.objects.filter(approval_item=approval_item, user=ceo.user).count()

        if ceo_included == 0:
            last_approver = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('-stage')[0]
            stage_count = last_approver.stage + 1
            ApprovalItemApprover.objects.create(stage=stage_count, user=ceo.user, approval_item=approval_item, status="Q") 

    document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
    if document_type.document_type_code == "601":
        memo = get_object_or_404(Memo, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='300')[0]
        memo.status = status
        memo.save()
        return redirect('memo_list')
    elif document_type.document_type_code == "205":
        po = get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='300')[0]
        po.status = status
        po.save()
        return redirect('po_list', po.transaction_type.pk)
    elif document_type.document_type_code == "301":
        payment = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='300')[0]
        payment.status = status
        payment.save()
        trans_name = payment.transaction_type.transaction_type_name
        return redirect('pylist', payment.transaction_type.pk)
    elif document_type.document_type_code == "501":
        staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='300')[0]
        staff.status = status
        staff.save()
        return redirect('staff_list')
    elif document_type.document_type_code == "504":
        staff_ot = get_object_or_404(StaffOT, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='300')[0]
        staff_ot.status = status
        staff_ot.save()
        return redirect('staff_ot_list', staff_ot.transaction_type.pk)

    elif document_type.document_type_code == "403":
        reimbursement_request = get_object_or_404(ReimbursementRequest, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='300')[0]
        reimbursement_request.status = status
        reimbursement_request.save()
        return redirect('reimbursement_request_list')
    
    return redirect(approval_list)

@login_required
def approve(request):
    return redirect(approve_item, request.POST['hiddenValueApprove'])

@login_required
def approve_item(request, pk):
    approver_item = get_object_or_404(ApprovalItemApprover, user=request.user.id, approval_item=pk)
    approver_item.status = "A"
    approver_item.approved_date = datetime.datetime.now()
    approver_item.save()

    approvers = ApprovalItemApprover.objects.filter(approval_item=pk).count()
    approvers_approve = ApprovalItemApprover.objects.filter(approval_item=pk, status="A").count()

    if approvers == approvers_approve:   
        approval_type = DocumentTypeMaintenance.objects.filter(document_type_code="901")[0]
        document_number = approval_type.running_number + 1
        approval_type.running_number = document_number
        approval_type.save()

        approval_item = get_object_or_404(ApprovalItem, pk=pk)
        approval_item.approval_code = '{0}-{1:05d}'.format(
            approval_type.document_type_code, document_number
            )
        approval_item.status = "A"
        approval_item.approved_date = datetime.datetime.now()
        approval_item.save()

        document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
        if document_type.document_type_code == "601":
            memo = get_object_or_404(Memo, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            memo.status = status
            memo.save()
        elif document_type.document_type_code == "205":
            po = get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            po.status = status
            po.save()
        elif document_type.document_type_code == "301":
            payment = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            payment.status = status
            payment.save()
        elif document_type.document_type_code == "501":
            staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            staff.status = status
            staff.save()
        elif document_type.document_type_code == "504":
            staff_ot = get_object_or_404(StaffOT, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            staff_ot.status = status
            staff_ot.save()
        elif document_type.document_type_code == "403":
            reimbursement_request = get_object_or_404(ReimbursementRequest, pk=approval_item.document_pk)
            status = StatusMaintenance.objects.filter(document_type=document_type, status_code='400')[0]
            reimbursement_request.status = status
            reimbursement_request.save()
    else:
        next_approver = get_object_or_404(ApprovalItemApprover, stage=approver_item.stage + 1, approval_item=pk)
        next_approver.status = "P"
        next_approver.save()

    return JsonResponse({'message': 'Success'})

@login_required
def stage_count(approval_item, previous_approval_group, approval_group):    
    if previous_approval_group.id != approval_group.id:
        previous_groups = Group.objects.filter(name=previous_approval_group.user_group.group_name).values_list('id', flat=True)
        previous_users = User.objects.filter(groups__in=previous_groups).values_list('id', flat=True)
        return ApprovalItemApprover.objects.filter(approval_item=approval_item, user__in=previous_users).count()
    else:
        return 0

@login_required
def approver_create(request, pk):
    group_name = request.POST['hiddenGroupName']

    if group_name == 'Group A':
        form = ApproverGroupAForm(request.POST)
    else:
        form = ApproverGroupBForm(request.POST)

    approval_item = get_object_or_404(ApprovalItem, pk=pk)
    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=approval_item.approval_level.pk)
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
    previous_approver_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()
    
    if first_tab_rule_group.next_condition == 'Or':
        submitter_as_emp = get_object_or_404(EmployeeMaintenance, user=request.user)
        first_tab_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group,approval_rule=approval_rule)[0]
    else:
        if previous_approver_count == 0 and previous_approval_group.user_group.group_name != group_name:
            return JsonResponse({'message': 'Need ' + previous_approval_group.approval_group_name + ' approver(s) to proceed'})
       
    groups = Group.objects.filter(name=group_name).values_list('id', flat=True)
    users = User.objects.filter(groups__in=groups).values_list('id', flat=True)
    current_approvers = ApprovalItemApprover.objects.filter(approval_item=approval_item, user__in=users).count()

    if first_tab_rule_group.next_condition == 'Or':
        if approval_item.document_type.document_type_code != "601":
            previous_approver_count = 0
        else:
            previous_approver_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()

    if previous_approver_count > 0 and previous_approval_group.user_group.group_name == group_name:
        if approval_item.document_type.document_type_code != "601":
            previous_approvers = ApprovalItemApprover.objects.filter(approval_item=approval_item)    
            previous_approvers_same_group_count = 0

            for approver in previous_approvers:
                employee = get_object_or_404(EmployeeMaintenance, user_id=approver.user.id)
                employee_group = get_object_or_404(EmployeeGroupMaintenance, pk=employee.employee_group.id)

                if employee_group.group_name == group_name:
                    previous_approvers_same_group_count = previous_approvers_same_group_count + 1

            previous_approver_count = previous_approvers_same_group_count
        else:
            previous_approver_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()

    if current_approvers < approval_group.no_of_person:
        if form.is_valid():
            user = get_object_or_404(User, pk=request.POST['user'])
            approver_count_stage = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()
            approver = form.save(commit=False)
            approver.approval_item = approval_item
            # approver.stage = previous_approver_count + current_approvers + 1
            approver.stage = approver_count_stage + 1
            approver.user = user
            approver.save()

            group_order = Group.objects.all().values_list('id', flat=True)
            users_order = User.objects.filter(groups__in = groups).values_list('id', flat=True).order_by('group.id')
            approvers = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('stage')
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
def supervisor_approver_create(request, pk):
    # group_name = request.POST['hiddenGroupName']

    form = ApproverGroupAAndBForm(request.user,request.POST)

    approval_item = get_object_or_404(ApprovalItem, pk=pk)
    approval_rule = get_object_or_404(WorkflowApprovalRule, pk=approval_item.approval_level.pk)
    # approval_group = get_object_or_404(WorkflowApprovalGroup, pk=request.POST['hiddenGroupId'])
    # first_tab_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)[0]
    
    # if approval_rule.supervisor_approve:
    #     selected_user = get_object_or_404(User, pk=request.POST['user'])
    #     submiter = get_object_or_404(EmployeeMaintenance, user=request.user)
    #     supervisor = get_object_or_404(EmployeeMaintenance, id=submiter.reporting_officer_id.id)
    #     supervisor_user = get_object_or_404(User, pk=supervisor.user.id)
    #     if supervisor_user == selected_user:
    #         return JsonResponse({'message': 'The selected approver cannot be your reporting officer.'})

    # previous_approval_group = first_tab_rule_group.approval_group
    # previous_groups = Group.objects.filter(name=previous_approval_group.user_group.group_name).values_list('id', flat=True)
    # previous_users = User.objects.filter(groups__in=previous_groups).values_list('id', flat=True)
    # previous_approver_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()
    
    # if first_tab_rule_group.next_condition == 'Or':
    #     submitter_as_emp = get_object_or_404(EmployeeMaintenance, user=request.user)
    #     first_tab_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group,approval_rule=approval_rule)[0]
    # else:
    #     if previous_approver_count == 0 and previous_approval_group.user_group.group_name != group_name:
    #         return JsonResponse({'message': 'Need ' + previous_approval_group.approval_group_name + ' approver(s) to proceed'})
       
    # groups = Group.objects.filter(name=group_name).values_list('id', flat=True)
    # users = User.objects.filter(groups__in=groups).values_list('id', flat=True)
    # current_approvers = ApprovalItemApprover.objects.filter(approval_item=approval_item, user__in=users).count()

    # if first_tab_rule_group.next_condition == 'Or':
    #     if approval_item.document_type.document_type_code != "601":
    #         previous_approver_count = 0
    #     else:
    #         previous_approver_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()

    # if previous_approver_count > 0 and previous_approval_group.user_group.group_name == group_name:
    #     if approval_item.document_type.document_type_code != "601":
    #         previous_approvers = ApprovalItemApprover.objects.filter(approval_item=approval_item)    
    #         previous_approvers_same_group_count = 0

    #         for approver in previous_approvers:
    #             employee = get_object_or_404(EmployeeMaintenance, user_id=approver.user.id)
    #             employee_group = get_object_or_404(EmployeeGroupMaintenance, pk=employee.employee_group.id)

    #             if employee_group.group_name == group_name:
    #                 previous_approvers_same_group_count = previous_approvers_same_group_count + 1

    #         previous_approver_count = previous_approvers_same_group_count
    #     else:
    #         previous_approver_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()

    
    if form.is_valid():
        # user = get_object_or_404(User, pk=request.POST['supervisor_user'])
        user = form.cleaned_data['supervisor_user']
        validation_count = ApprovalItemApprover.objects.filter(approval_item=approval_item,user=user).count()
        if validation_count > 0 :
            return JsonResponse({'message': 'The selected user already inside approver list'})
        else:
            previous_approver_count = ApprovalItemApprover.objects.filter(approval_item=approval_item).count()
            approver = form.save(commit=False)
            approver.approval_item = approval_item
            approver.stage = previous_approver_count + 1
            approver.user = user
            approver.save()

            # group_order = Group.objects.all().values_list('id', flat=True)
            # users_order = User.objects.filter(groups__in = groups).values_list('id', flat=True).order_by('group.id')
            approvers = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('stage')
            count = 1

            for approver in approvers:
                if count == 1:
                    approver.status = "P"
                else:
                    approver.status = "Q"
                
                approver.save()
                count = count + 1

        return JsonResponse({'message': 'Success'})
    

@login_required
def approver_delete(request):
    approver = get_object_or_404(ApprovalItemApprover, pk=request.POST['hiddenValueApprover' + request.POST['hiddenDeleteGroupId']])
    approver.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def supervisor_approver_delete(request):
    approver = get_object_or_404(ApprovalItemApprover, pk=request.POST['hiddenValueApproverSupervisor'])
    approval_item = approver.approval_item
    approver.delete()
    approvers = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('stage')
    count = 1

    for approver in approvers:
        if count == 1:
            approver.status = "P"
            approver.stage = count
        else:
            approver.status = "Q"
            approver.stage = count
        
        approver.save()
        count = count + 1
    return JsonResponse({'message': 'Success'})

@login_required
def cc_create(request, pk):
    form = CCForm(request.POST)
    if form.is_valid():
        approval_item = get_object_or_404(ApprovalItem, pk=pk)
        user = get_object_or_404(User, pk=request.POST['user'])

        cc = form.save(commit=False)
        cc.user = user
        cc.approval_item = approval_item
        cc.save()

    return JsonResponse({'message': 'Success'})

@login_required
def cc_delete(request):
    cc = get_object_or_404(ApprovalItemCC, pk=request.POST['hiddenValueCC'])
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

        approvers = ApprovalItemApprover.objects.filter(approval_item=form.cleaned_data['hiddenValueReject'])
        for approver in approvers:
            approver.status = "R"
            approver.save()

        approval_item = get_object_or_404(ApprovalItem, pk=form.cleaned_data['hiddenValueReject'])
        approval_item.status = "R"
        approval_item.save()

    document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
    if document_type.document_type_code == "601":
        memo = get_object_or_404(Memo, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        memo.status = status
        memo.save()
    elif document_type.document_type_code == "205":
        po= get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        po.status = status
        po.save()
    if document_type.document_type_code == "301":
        payment = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
        document_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        payment.status = status
        payment.save()
    if document_type.document_type_code == "501":
        staff = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        staff.status = status
        staff.save()
    if document_type.document_type_code == "504":
        staff_ot = get_object_or_404(StaffOT, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        staff_ot.status = status
        staff_ot.save()
    elif document_type.document_type_code == "403":
        reimbursement_request = get_object_or_404(ReimbursementRequest, pk=approval_item.document_pk)
        status = StatusMaintenance.objects.filter(document_type=document_type, status_code='500')[0]
        reimbursement_request.status = status
        reimbursement_request.save()

    return JsonResponse({'message': 'Success'})

@login_required
def count_approver_needed(request,pk):
    approval_rule = get_object_or_404(WorkflowApprovalRule,pk=pk)
    approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule).order_by('id')

    if approval_rule_group.count() > 0:
        first_tab_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)[0]
        if first_tab_group.next_condition == 'Or':
            approver_needed = 0 
            submitter_as_emp = get_object_or_404(EmployeeMaintenance, user=request.user)
            approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(submitter_group=submitter_as_emp.employee_group,approval_rule=approval_rule)
            for approval_no in approval_rule_group:
                approver_needed = approver_needed + approval_no.approval_group.no_of_person

            return approver_needed
        else:
            approver_needed = 0
            approval_rule_group = WorkflowApprovalRuleGroupMaintenance.objects.filter(approval_rule=approval_rule)
            for approval_no in approval_rule_group:
                approver_needed = approver_needed + approval_no.approval_group.no_of_person

            return approver_needed
