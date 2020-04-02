from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewMemoForm, DetailMemoForm, UpdateMemoForm, NewMemoAttachmentForm
from django.contrib.auth.decorators import login_required
from .models import Memo, MemoAttachment
from administration.models import CompanyMaintenance, DepartmentMaintenance, ProjectMaintenance, MemoTemplateMaintenance
from rest_framework import viewsets
from .serializers import MemoSerializer, MemoAttachmentSerializer
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from django.contrib.auth.models import User
from approval.models import ApprovalItem

class MemoAttachmentViewSet(viewsets.ModelViewSet):
    queryset = MemoAttachment.objects.all()
    serializer_class = MemoAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        memo = get_object_or_404(Memo,pk=self.request.query_params.get('pk', None))
        return MemoAttachment.objects.filter(memo=memo)

class MyMemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all().order_by('-id')
    serializer_class = MemoSerializer
    
    def get_queryset(self):
        return Memo.objects.filter(submit_by=self.request.user.id)

class TeamMemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all().order_by('-id')    
    serializer_class = MemoSerializer

    def get_queryset(self):
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return Memo.objects.filter(submit_by__in=users)

@login_required
def memo_create(request):    
    memo = Memo.objects.create(submit_by=request.user)
    return redirect(memo_create_edit, memo.pk)

@login_required
def memo_create_edit(request, pk):    
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        form = NewMemoForm(request.POST, instance=memo)
        if form.is_valid():

            memo_type = DocumentTypeMaintenance.objects.filter(document_type_name="Memo")[0]
            document_number = memo_type.running_number + 1
            memo_type.running_number = document_number 
            memo_type.save()

            company = form.cleaned_data['company']
            department = form.cleaned_data['department']
            project = form.cleaned_data['project']
            template = form.cleaned_data['template']
            memo.document_number = '{0}-{1:05d}'.format(memo_type.document_type_code,document_number)
            memo.company = company
            memo.department = department
            memo.project = project
            memo.template = template
            memo.submit_by = request.user
            memo.save()

            transaction_type = get_object_or_404(TransactiontypeMaintenance,transaction_type_name="BLANK", document_type=memo_type)
            approval_level = get_object_or_404(WorkflowApprovalRule,approval_level=2)

            approval_item = ApprovalItem()        
            approval_item.document_number = memo.document_number
            approval_item.document_pk = memo.pk
            approval_item.document_type = memo_type
            approval_item.transaction_type = transaction_type
            approval_item.approval_level = approval_level
            approval_item.notification = ""
            approval_item.status = "D"
            approval_item.save()

            memo.approval = approval_item
            memo.save()

            return redirect(memo_list)
    else:
        form = NewMemoForm(instance=memo)
    form_attachment = NewMemoAttachmentForm()
    return render(request, 'memo/create.html', {'memo': memo, 'form': form, 'form_attachment': form_attachment})

@login_required
def memo_attachment_create_fromcreate(request, pk):    
    form = NewMemoAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        memo_attachment = form.save(commit=False)
        memo = get_object_or_404(Memo, pk=pk)
        memo_attachment.memo = memo
        memo_attachment.save()
    
    return redirect(memo_create_edit, pk=pk) 

@login_required
def memo_attachment_delete_fromcreate(request, pk):
    memoattachment =  get_object_or_404(MemoAttachment, pk=pk)
    memo = get_object_or_404(Memo, pk=memoattachment.memo.pk)
    memoattachment.delete()
    return redirect(memo_create_edit, pk=memo.pk)

@login_required
def memo_delete(request, pk):
    memo =  get_object_or_404(Memo, pk=pk)
    memo.delete()
    return redirect(memo_list)

@login_required
def memo_detail(request, pk):
    memo =  get_object_or_404(Memo, pk=pk)
    form = DetailMemoForm(instance=memo)
    return render(request, 'memo/detail.html', {'memo': memo, 'form': form})

@login_required
def memo_index(request):
    return redirect(memo_list)

@login_required
def memo_list(request):
    return render(request, 'memo/list.html')

@login_required
def memo_update(request, pk): 
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        form = UpdateMemoForm(request.POST, instance=memo)
        if form.is_valid():
            memo = form.save()
            memo.revision = memo.revision + 1
            memo.submit_by = request.user
            memo.save()
            return redirect(memo_detail, pk=memo.pk)
        else:
            print(form.errors)
    else:
        #project = get_object_or_404(ProjectMaintenance, pk=2)
        #memo.project = project
        #memo.save()
        form = UpdateMemoForm(instance=memo)
    form_attachment = NewMemoAttachmentForm()
    return render(request, 'memo/update.html', {'memo': memo, 'form': form, 'form_attachment': form_attachment})
    
@login_required
def memo_attachment_create(request, pk):    
    form = NewMemoAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        memo_attachment = form.save(commit=False)
        memo = get_object_or_404(Memo, pk=pk)
        memo_attachment.memo = memo
        memo_attachment.save()
    
    return redirect(memo_update, pk=pk) 

@login_required
def memo_attachment_delete(request, pk):
    memoattachment =  get_object_or_404(MemoAttachment, pk=pk)
    memo = get_object_or_404(Memo, pk=memoattachment.memo.pk)
    memoattachment.delete()
    return redirect(memo_update, pk=memo.pk)