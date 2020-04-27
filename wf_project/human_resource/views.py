from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewStaffRecruimentForm,UpdateStaffRecruimentForm,DetailStaffRecruimentForm,NewStaffJobRequirementForm,NewStaffJobResponsibleForm,NewStaffPlatformForm,NewStaffCandidateForm
from django.contrib.auth.decorators import login_required
from .models import StaffRecruitmentRequest,StaffJobRequirement,StaffJobResponsibilities,StaffPlatform,StaffCandidate
from rest_framework import viewsets
from .serializers import StaffRecruitmentSerializer,StaffJobRequirementSerializer,StaffJobResponsibilitiesSerializer,StaffPlatformSerializer,StaffCandidateSerializer
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from approval.models import ApprovalItem
from django.contrib.auth.models import User
from django.http import JsonResponse

class StaffViewSet(viewsets.ModelViewSet):
    queryset = StaffRecruitmentRequest.objects.all() #.order_by('rank')
    serializer_class = StaffRecruitmentSerializer

class MyStaffViewSet(viewsets.ModelViewSet):
    queryset = StaffRecruitmentRequest.objects.all().order_by('-id')
    serializer_class = StaffRecruitmentSerializer
    
    def get_queryset(self):
        return StaffRecruitmentRequest.objects.filter(submit_by=self.request.user.id).order_by('-id')

class TeamStaffViewSet(viewsets.ModelViewSet):
    queryset = StaffRecruitmentRequest.objects.all().order_by('-id')    
    serializer_class = StaffRecruitmentSerializer

    def get_queryset(self):
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return StaffRecruitmentRequest.objects.filter(submit_by__in=users).order_by('-id')

class StaffJobRequirementViewSet(viewsets.ModelViewSet):
    queryset = StaffJobRequirement.objects.all()
    serializer_class = StaffJobRequirementSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        staff = get_object_or_404(StaffRecruitmentRequest,pk=self.request.query_params.get('pk', None))
        return StaffJobRequirement.objects.filter(staff_recruitment=staff)

class StaffJobResponsibleViewSet(viewsets.ModelViewSet):
    queryset = StaffJobResponsibilities.objects.all()
    serializer_class = StaffJobResponsibilitiesSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        staff = get_object_or_404(StaffRecruitmentRequest,pk=self.request.query_params.get('pk', None))
        return StaffJobResponsibilities.objects.filter(staff_recruitment=staff)

class StaffPlatformViewSet(viewsets.ModelViewSet):
    serializer_class = StaffPlatformSerializer

    def get_queryset(self):
        staff = get_object_or_404(StaffRecruitmentRequest,pk=self.request.query_params.get('pk', None))
        return StaffPlatform.objects.filter(staff_recruitment=staff)

class StaffCandidateViewSet(viewsets.ModelViewSet):
    serializer_class = StaffCandidateSerializer

    def get_queryset(self):
        staff = get_object_or_404(StaffRecruitmentRequest,pk=self.request.query_params.get('pk', None))
        return StaffCandidate.objects.filter(staff_recruitment=staff)

@login_required
def staff_init(request):    
    staff = StaffRecruitmentRequest.objects.create(submit_by=request.user)
    return redirect(staff_create, staff.pk)

@login_required
def staff_create(request,pk):    
    staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
    if request.method == 'POST':
        form = NewStaffRecruimentForm(request.POST,instance=staff)
        if form.is_valid():
            staff_type = DocumentTypeMaintenance.objects.filter(document_type_code="501")[0]
            document_number = staff_type.running_number + 1
            staff_type.running_number = document_number 
            staff_type.save()

            company = form.cleaned_data['company']
            reporting_to = form.cleaned_data['reporting_to']
            department = form.cleaned_data['department']
            position_title = form.cleaned_data['position_title']
            employment_type = form.cleaned_data['employment_type']
            position_grade = form.cleaned_data['position_grade']
            staff = form.save(commit=False)
            staff.reporting_to = reporting_to
            staff.department = department
            staff.document_number = '{0}-{1:05d}'.format(staff_type.document_type_code,document_number)
            staff.company = company
            staff.submit_by = request.user
            staff.position_title = position_title
            staff.employment_type = employment_type
            staff.position_grade = position_grade
            staff.save()

            document_type = get_object_or_404(DocumentTypeMaintenance,document_type_code="501")
            transaction_type = get_object_or_404(TransactiontypeMaintenance,transaction_type_name="Staff Requisition", document_type=document_type)
            approval_level = get_object_or_404(WorkflowApprovalRule,approval_level=2)

            approval_item = ApprovalItem()        
            approval_item.document_number = staff.document_number
            approval_item.document_pk = staff.pk
            approval_item.document_type = document_type
            approval_item.transaction_type = transaction_type
            approval_item.approval_level = approval_level
            approval_item.notification = ""
            approval_item.status = "D"
            approval_item.save()

            staff.approval = approval_item
            staff.save()
            return redirect(staff_update,staff.pk)
        else:
            print(form.errors)
            return redirect(staff_list)
    else:
        form = NewStaffRecruimentForm(instance=staff)
        form_requirement = NewStaffJobRequirementForm()
        form_responsible = NewStaffJobResponsibleForm()
    return render(request, 'human_resource/create.html', {'staff': staff, 'form': form,'form_requirement': form_requirement,'form_responsible':form_responsible})

@login_required
def staff_delete(request, pk):
    staff =  get_object_or_404(StaffRecruitmentRequest, pk=pk)
    staff.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def staff_detail(request, pk):
    staff =  get_object_or_404(StaffRecruitmentRequest, pk=pk)
    form = DetailStaffRecruimentForm(instance=staff)
    return render(request, 'human_resource/detail.html', {'staff': staff, 'form': form})

@login_required
def staff_list(request):
    return render(request, 'human_resource/list.html')

@login_required
def staff_update(request, pk): 
    staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
    if request.method == 'POST':
        form = UpdateStaffRecruimentForm(request.POST, instance=staff)
        if form.is_valid():
            staff = form.save()
            staff.revision = staff.revision + 1
            staff.save()
            return redirect('staff_detail', pk=staff.pk)
        else:
            print(form.errors)
    else:
        form = UpdateStaffRecruimentForm(instance=staff)
        form_requirement = NewStaffJobRequirementForm()
        form_responsible = NewStaffJobResponsibleForm()
    return render(request, 'human_resource/update.html', {'staff': staff, 'form': form,'form_requirement': form_requirement,'form_responsible':form_responsible})

def staff_requirement_create(request,pk):  
    form = NewStaffJobRequirementForm(request.POST)
    if form.is_valid():
        staff_job_requirement = form.save(commit=False)
        staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
        staff_job_requirement.staff_recruitment = staff
        staff_job_requirement.save()
    else: 
        print(form.errors)
    
    return JsonResponse({'message': 'Success'})

@login_required
def staff_requirement_delete(request, pk):
    staff_requirement =  get_object_or_404(StaffJobRequirement, pk=pk)
    staff = get_object_or_404(StaffRecruitmentRequest, pk=staff_requirement.staff_recruitment.pk)
    staff_requirement.delete()
    return JsonResponse({'message': 'Success'})

def staff_responsible_create(request, pk):
    form = NewStaffJobResponsibleForm(request.POST)
    if form.is_valid():
        staff_job_responsible = form.save(commit=False)
        staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
        staff_job_responsible.staff_recruitment = staff
        staff_job_responsible.save()
    else:
        print(form.errors)
    
    return JsonResponse({'message': 'Success'})

def staff_responsible_delete(request, pk):
    staff_responsible = get_object_or_404(StaffJobResponsibilities, pk=pk)
    staff = get_object_or_404(StaffRecruitmentRequest, pk=staff_responsible.staff_recruitment.pk)
    staff_responsible.delete()
    return JsonResponse({'message': 'Success'})

def staff_platform_create(request, pk):
    form = NewStaffPlatformForm(request.POST)
    if form.is_valid():
        staff_platform = form.save(commit=False)
        staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
        staff_platform.staff_recruitment = staff
        staff_platform.save()
    else:
        print(form.errors)
    
    return JsonResponse({'message': 'Success'})

def staff_platform_delete(request, pk):
    staff_platform =  get_object_or_404(StaffPlatform, pk=pk)
    staff_platform.delete()
    return JsonResponse({'message': 'Success'})

def staff_candidate_create(request, pk):
    form = NewStaffCandidateForm(request.POST)
    if form.is_valid():
        staff_candidate = form.save(commit=False)
        staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
        staff_candidate.staff_recruitment = staff
        staff_candidate.save()
    else:
        print(form.errors)
    
    return JsonResponse({'message': 'Success'})

def staff_candidate_delete(request, pk):
    staff_candidate = get_object_or_404(StaffCandidate, pk=pk)
    staff_candidate.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def staff_send_approval(request, pk):
    staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
    document_type = get_object_or_404(DocumentTypeMaintenance,document_type_code="501")
    transaction_type = get_object_or_404(TransactiontypeMaintenance,transaction_type_name="Staff Requisition", document_type=document_type)
           
    approval_level = WorkflowApprovalRule.objects.filter(transaction_type=transaction_type)[0]
    approval_item = get_object_or_404(ApprovalItem, pk=staff.approval.pk)
    approval_item.approval_level = approval_level
    
    if approval_level.ceo_approve == True:
            approval_item.notification = "CEO will added by default"
    approval_item.save()

    return redirect('approval_detail', pk=approval_item.pk)


@login_required
def staff_after_approve(request, pk):
    staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
    form = DetailStaffRecruimentForm(instance=staff)
    form_platform = NewStaffPlatformForm()
    form_candidate = NewStaffCandidateForm()

    return render(request, 'human_resource/afterapprove.html', {'staff': staff, 'form': form,'form_platform':form_platform,'form_candidate':form_candidate})