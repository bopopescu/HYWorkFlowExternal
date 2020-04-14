from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewStaffOTForm,NewStaffOTDetailForm,UpdateStaffOTForm,DetailStaffOTForm
from django.contrib.auth.decorators import login_required
from .models import StaffOT,StaffOTDetail
from rest_framework import viewsets
from .serializers import StaffOTSerializer,StaffOTDetailSerializer
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import StatusMaintenance
from administration.models import EmployeeMaintenance
from administration.models import HolidayEventMaintenance
from approval.models import ApprovalItem
from django.contrib.auth.models import User
import datetime
from django.http import JsonResponse
from django.utils.datetime_safe import date

class MyStaffOTViewSet(viewsets.ModelViewSet):

    serializer_class = StaffOTSerializer
    
    def get_queryset(self):
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return StaffOT.objects.filter(submit_by=self.request.user.id, transaction_type=transaction_type)

class TeamStaffOTViewSet(viewsets.ModelViewSet):

    serializer_class = StaffOTSerializer

    def get_queryset(self):
        document_type = get_object_or_404(DocumentTypeMaintenance,document_type_code="504")
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return StaffOT.objects.filter(submit_by__in=users,transaction_type=transaction_type)

class StaffOTDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StaffOTDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        staff_ot = get_object_or_404(StaffOT,pk=self.request.query_params.get('pk', None))
        return StaffOTDetail.objects.filter(staff_ot=staff_ot)

@login_required
def staff_ot_init(request ,pk):    
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    employee = get_object_or_404(EmployeeMaintenance, user=request.user)
    employee_position = employee.position_id
    staff_ot = StaffOT.objects.create(submit_by=request.user, transaction_type=transaction_type,employee=employee,employee_position =employee_position)
    return redirect(staff_ot_create, staff_ot.pk)

@login_required
def staff_ot_create(request, pk):    
    staff_ot = get_object_or_404(StaffOT, pk=pk)
    if request.method == 'POST':
        form = NewStaffOTForm(request.POST, instance=staff_ot)
        if form.is_valid():

            staff_ot_type = DocumentTypeMaintenance.objects.filter(document_type_code="504")[0]
            document_number = staff_ot_type.running_number + 1
            staff_ot_type.running_number = document_number 
            staff_ot_type.save()

            company = form.cleaned_data['company']
            department = form.cleaned_data['department']
            transaction_type = form.cleaned_data['transaction_type']
            project = form.cleaned_data['project']
            employee = form.cleaned_data['employee']

            status = get_object_or_404(StatusMaintenance, document_type=staff_ot_type, status_code="100")

            staff_ot.document_number = '{0}-{1:05d}'.format(staff_ot_type.document_type_code,document_number)
            staff_ot.company = company
            staff_ot.department = department
            staff_ot.project = project
            staff_ot.employee = employee
            staff_ot.status = status
            staff_ot.submit_by = request.user
            staff_ot.transaction_type = transaction_type
            staff_ot.save()

            # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=transaction_type.pk ,document_type=staff_ot_type)

            approval_item = ApprovalItem()        
            approval_item.document_number = staff_ot.document_number
            approval_item.document_pk = staff_ot.pk
            approval_item.document_type = staff_ot_type
            approval_item.transaction_type = transaction_type
            approval_item.status = "D"
            approval_item.save()

            staff_ot.approval = approval_item
            staff_ot.save()

            return redirect(staff_ot_update, pk=staff_ot.pk)
        else:
            print(form.errors)
            form = NewStaffOTForm(instance=staff_ot)
            form_detail = NewStaffOTDetailForm()
    else:
        form = NewStaffOTForm(instance=staff_ot)
        form_detail = NewStaffOTDetailForm()
    return render(request, 'staff_overtime/create.html', {'staff_ot': staff_ot, 'form': form, 'form_detail': form_detail})

@login_required
def staff_ot_send_approval(request,pk):
    staff_ot = get_object_or_404(StaffOT, pk=pk)
    approval_level = WorkflowApprovalRule.objects.filter(approval_level=0)[0]
    approval_item = get_object_or_404(ApprovalItem, pk=staff_ot.approval.pk)       
    approval_item.approval_level = approval_level
    if approval_level.ceo_approve == True:
        approval_item.notification = "CEO will added by default"

    approval_item.save()

    return redirect('approval_detail', pk=approval_item.pk)

@login_required
def staff_ot_detail(request, pk):
    staff_ot =  get_object_or_404(StaffOT, pk=pk)
    form = DetailStaffOTForm(instance=staff_ot)
    return render(request, 'staff_overtime/detail.html', {'staff_ot': staff_ot, 'form': form})

@login_required
def staff_ot_list(request,pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'staff_overtime/list.html', {'trans_type': transaction_type})

@login_required
def staff_ot_update(request, pk):
    staff_ot = get_object_or_404(StaffOT, pk=pk)
    if request.method == 'POST':
        form = UpdateStaffOTForm(request.POST, instance=staff_ot)
        status = staff_ot.status
        staff_ot = form.save()
        staff_ot.revision = staff_ot.revision + 1
        staff_ot.status = status
        staff_ot.save()
        return redirect('staff_ot_detail', pk=staff_ot.pk)
    else:
        form = UpdateStaffOTForm(instance=staff_ot)
        form_detail = NewStaffOTDetailForm()
    return render(request, 'staff_overtime/update.html', {'staff_ot': staff_ot, 'form': form,'form_detail':form_detail})

@login_required
def staff_ot_delete(request):
    staff_ot =  get_object_or_404(StaffOT, pk=request.POST['hiddenValue'])
    staff_ot.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def staff_ot_detail_create(request, pk):    
    form = NewStaffOTDetailForm(request.POST, request.FILES)
    if form.is_valid():
        staff_ot_detail = form.save(commit=False)
        staff_ot = get_object_or_404(StaffOT, pk=pk)

        
        time_out = datetime.datetime.combine(date.today(),staff_ot_detail.ot_time_out)
        time_in = datetime.datetime.combine(date.today(),staff_ot_detail.ot_time_in)
        total_ot_time = time_out - time_in
        total_ot_hours = 0
        holiday_event = HolidayEventMaintenance.objects.filter(event_date=staff_ot_detail.ot_date)
        if(holiday_event.count() == 0):
            is_holiday = False
        else:
            is_holiday = True
            total_ot_hours = total_ot_time.days * 24 + total_ot_time.seconds // 3600

        print(total_ot_hours)
        staff_ot_detail.staff_ot = staff_ot
        staff_ot_detail.is_holiday = is_holiday
        # staff_ot_detail.total_ot_time = total_ot_time
        staff_ot_detail.total_ot_time = total_ot_time.seconds / 60
        staff_ot_detail.save()
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success'}) 

@login_required
def staff_ot_detail_delete(request):
    staff_ot_detail =  get_object_or_404(StaffOTDetail, pk=request.POST['hiddenValue'])
    staff_ot = get_object_or_404(StaffOT, pk=staff_ot_detail.staff_ot.pk)
    staff_ot_detail.delete()
    return JsonResponse({'message': 'Success'})

    
