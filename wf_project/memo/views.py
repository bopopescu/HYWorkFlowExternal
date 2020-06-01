"""View logic to control Memo module"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from administration.models import MemoTemplateMaintenance, WorkflowApprovalRule
from administration.models import DocumentTypeMaintenance, TransactiontypeMaintenance
from administration.models import StatusMaintenance, EmployeeMaintenance
from administration.models import EmployeeDepartmentMaintenance,EmployeeCompanyMaintenance,EmployeeBranchMaintenance,EmployeeProjectMaintenance
from approval.forms import RejectForm
from approval.models import ApprovalItem, ApprovalItemApprover
from purchasing.models import PurchaseOrder
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest
from staff_overtime.models import StaffOT
from drawer_reimbursement.models import ReimbursementRequest
from PDFreport.render import Render
from .models import Memo, MemoAttachment
from .serializers import MemoSerializer, MemoAttachmentSerializer
from .forms import NewMemoForm, DetailMemoForm, UpdateMemoForm, NewMemoAttachmentForm
from django.db.models import Q

class MemoAttachmentViewSet(viewsets.ModelViewSet):
    """Handles Attachement datatable"""

    queryset = MemoAttachment.objects.all()
    serializer_class = MemoAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        memo = get_object_or_404(Memo, pk=self.request.query_params.get('pk', None))
        return MemoAttachment.objects.filter(memo=memo).order_by('-id')

class MyMemoViewSet(viewsets.ModelViewSet):
    """Handles My Task datatable"""

    queryset = Memo.objects.all().order_by('-id')
    serializer_class = MemoSerializer

    def get_queryset(self):
        return Memo.objects.filter(submit_by=self.request.user.id).order_by('-id')

class TeamMemoViewSet(viewsets.ModelViewSet):
    """Handles Team Task datatable"""

    queryset = Memo.objects.all().order_by('-id')
    serializer_class = MemoSerializer

    def get_queryset(self):
        employee = get_object_or_404(EmployeeMaintenance, user=self.request.user)
        depts = EmployeeDepartmentMaintenance.objects.filter(employee=employee).values_list('department_id', flat=True)
        comps = EmployeeCompanyMaintenance.objects.filter(employee=employee).values_list('company_id', flat=True)
        projects = EmployeeProjectMaintenance.objects.filter(employee=employee).values_list('project_id', flat=True)
        branchs = EmployeeBranchMaintenance.objects.filter(employee=employee).values_list('branch_id', flat=True)
        
        employees_indept = EmployeeDepartmentMaintenance.objects.filter(department_id__in=depts).values_list('employee_id', flat=True)
        employees_incomp = EmployeeCompanyMaintenance.objects.filter(company_id__in=comps).values_list('employee_id', flat=True)
        employees_inproject = EmployeeProjectMaintenance.objects.filter(project_id__in=projects).values_list('employee_id',flat=True)
        employees_inbranch = EmployeeBranchMaintenance.objects.filter(branch_id__in=branchs).values_list('employee_id', flat=True)
        
        # employee_id_list = employees_indept.intersection(employees_incomp,employees_inproject,employees_inbranch)
        employee_id_list = EmployeeMaintenance.objects.filter(Q(id__in=employees_indept) & Q(id__in=employees_incomp) & Q(id__in=employees_inproject) & Q(id__in=employees_inbranch)).values_list('id', flat=True)
        employees_as_user = EmployeeMaintenance.objects.filter(
            id__in=employee_id_list
            ).values_list('user_id', flat=True)
        users = User.objects.filter(
            id__in=employees_as_user
            ).exclude(
                id=self.request.user.id
                ).values_list('id', flat=True)
        return Memo.objects.filter(submit_by__in=users).exclude(document_number__isnull=True).order_by('-id')

@login_required
def memo_init(request):
    """Initializa a Memo"""

    memo = Memo.objects.create(submit_by=request.user)
    return redirect(memo_create, memo.pk)

@login_required
def memo_create(request, pk_value):
    """Creates a Memo into a document"""

    memo = get_object_or_404(Memo, pk=pk_value)
    if request.method == 'POST':
        form = NewMemoForm(request.POST, instance=memo)
        if form.is_valid():

            memo_type = DocumentTypeMaintenance.objects.filter(document_type_code="601")[0]
            document_number = memo_type.running_number + 1
            memo_type.running_number = document_number
            memo_type.save()

            company = form.cleaned_data['company']
            department = form.cleaned_data['department']
            project = form.cleaned_data['project']
            template = form.cleaned_data['template']
            status = get_object_or_404(
                StatusMaintenance, document_type=memo_type, status_code="100"
                )

            memo.document_number = '{0}-{1:05d}'.format(
                memo_type.document_type_code, document_number
                )
            memo.company = company
            memo.department = department
            memo.project = project
            memo.template = template
            memo.status = status
            memo.submit_by = request.user
            memo.subject = form.cleaned_data['subject']
            memo.save()

            transaction_type = TransactiontypeMaintenance.objects.filter(document_type=memo_type).order_by('transaction_type_name')[0]
            approval_level = get_object_or_404(WorkflowApprovalRule, document_amount_range=0,document_amount_range2=0, supervisor_approve=False)

            approval_item = ApprovalItem()
            approval_item.document_number = memo.document_number
            approval_item.document_pk = memo.pk
            approval_item.document_type = memo_type
            approval_item.transaction_type = transaction_type
            approval_item.approval_level = approval_level

            if approval_level.ceo_approve:
                approval_item.notification = "CEO will added by default"
            else:
                approval_item.notification = ""

            approval_item.status = "D"
            approval_item.save()

            memo.approval = approval_item
            memo.save()

            return redirect(memo_update, pk_value=memo.pk)
    else:
        form = NewMemoForm(instance=memo)
    form_attachment = NewMemoAttachmentForm()
    return render(request, 'memo/create.html', {
        'memo': memo, 'form': form,
        'form_attachment': form_attachment})

@login_required
def memo_attachment_create(request, pk_value):
    """Create an Attachment"""

    form = NewMemoAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        memo_attachment = form.save(commit=False)
        memo = get_object_or_404(Memo, pk=pk_value)
        memo_attachment.memo = memo
        memo_attachment.attachment_date = request.POST['attachment_date']
        memo_attachment.save()
    return JsonResponse({'message': 'Success'})

@login_required
def memo_attachment_delete(request):
    """Delete an Attachment"""

    memo_attachment = get_object_or_404(MemoAttachment, pk=request.POST['hiddenValue'])
    memo_attachment.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def memo_delete(request):
    """Delete a Memo"""

    memo = get_object_or_404(Memo, pk=request.POST['hiddenValue'])
    memo.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def memo_detail(request, pk_value):
    """Handles to view a Memo"""

    if request.GET.get('from', None) == 'approval':
        approvers = ApprovalItemApprover.objects.filter(user=request.user, status='P').values_list('approval_item', flat=True)
        approval_items = ApprovalItem.objects.filter(id__in=approvers,status="IP").order_by('-id')
        found = False
        next_link = reverse('approval_list')
        
        for approval_item in approval_items:
            if approval_item.document_pk == pk_value:
                found = True
            elif found:
                found = False
                document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)

                if document_type.document_type_code == "601":
                    document = get_object_or_404(Memo, pk=approval_item.document_pk)
                    next_link = reverse('memo_detail', args=(approval_item.document_pk, ))
                elif document_type.document_type_code == "205":
                    document = get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
                    next_link = reverse('po_detail', args=(approval_item.document_pk, ))
                elif document_type.document_type_code == "301":
                    document = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
                    next_link = reverse('py_detail', args=(approval_item.document_pk, ))
                elif document_type.document_type_code == "501":
                    document = get_object_or_404(StaffRecruitmentRequest, pk=approval_item.document_pk)
                    next_link = reverse('staff_detail', args=(approval_item.document_pk, ))
                elif document_type.document_type_code == "504":
                    document = get_object_or_404(StaffOT, pk=approval_item.document_pk)
                    next_link = reverse('staff_ot_detail', args=(approval_item.document_pk, ))
                elif document_type.document_type_code == "403":
                    document = get_object_or_404(ReimbursementRequest, pk=approval_item.document_pk)
                    next_link = reverse('reimbursement_request_detail', args=(approval_item.document_pk, ))
                    
        next_link = next_link + '?from=approval'
    else:
        next_link = reverse('approval_list')

    memo = get_object_or_404(Memo, pk=pk_value)
    form = DetailMemoForm(instance=memo)
    form.fields['company'].initial = memo.company
    form.fields['department'].initial = memo.department
    form.fields['project'].initial = memo.project
    form.fields['template'].initial = memo.template
    form.fields['subject'].initial = memo.subject
    form_reject = RejectForm()
    return render(request, 'memo/detail.html', {'memo': memo, 'form': form, 'form_reject': form_reject, 'next_link': next_link})

@login_required
def memo_index(request):
    """Redirect to Memo list"""

    return redirect(memo_list)

@login_required
def memo_list(request):
    """Handles a list of Memo"""

    return render(request, 'memo/list.html')

@login_required
def memo_update(request, pk_value):
    """Updates a Memo"""

    memo = get_object_or_404(Memo, pk=pk_value)
    if request.method == 'POST':
        form = UpdateMemoForm(request.POST, instance=memo)
        memo.revision = memo.revision + 1
        memo.submit_by = request.user
        memo.subject = request.POST['subject']
        memo.details = request.POST['details']
        memo.save()
        return redirect(memo_detail, pk_value=memo.pk)

    form = UpdateMemoForm(instance=memo)
    form.fields['company'].initial = memo.company
    form.fields['department'].initial = memo.department
    form.fields['project'].initial = memo.project
    form.fields['template'].initial = memo.template
    form.fields['subject'].initial = memo.subject
    form_attachment = NewMemoAttachmentForm()
    return render(request, 'memo/update.html', {
        'memo': memo, 'form': form,
        'form_attachment': form_attachment
        })

@login_required
def load_template(request):
    """Load dropdown for Memo Template"""

    template = get_object_or_404(MemoTemplateMaintenance, pk=request.GET.get('template'))
    return HttpResponse(template.template_htmldesign)

@login_required
def memo_print(request, pk): 
    memo = get_object_or_404(Memo, pk=pk)
    approval_item = get_object_or_404(ApprovalItem, pk=memo.approval.pk)
    requester = get_object_or_404(User, pk=memo.submit_by.pk)
    approver = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('-stage')[0]
    approver_employee = get_object_or_404(EmployeeMaintenance, user=approver.user)
    
    params = {
        'memo': memo,
        'approval_item': approval_item,
        'requester': requester,
        'approver_employee': approver_employee,
    }
    
    pdf = Render.render('report/Memo/print.html', params)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Memo_%s.pdf" %(memo.document_number)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return response("errors")
    #return render(request, 'report/Memo/print.html')
