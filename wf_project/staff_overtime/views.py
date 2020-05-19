from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewStaffOTForm, NewStaffOTDetailForm, UpdateStaffOTForm, DetailStaffOTForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .models import StaffOT, StaffOTDetail
from rest_framework import viewsets
from .serializers import StaffOTSerializer, StaffOTDetailSerializer
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import StatusMaintenance
from administration.models import EmployeeMaintenance
from administration.models import EmployeeDepartmentMaintenance,EmployeeCompanyMaintenance,EmployeeBranchMaintenance,EmployeeProjectMaintenance
from administration.models import HolidayEventMaintenance
from administration.models import OTRateMaintenance
from approval.models import ApprovalItem, ApprovalItemApprover
from approval.forms import RejectForm
from memo.models import Memo
from purchasing.models import PurchaseOrder
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest
from drawer_reimbursement.models import ReimbursementRequest
import datetime
from django.http import JsonResponse
from django.utils.datetime_safe import date
import decimal

class MyStaffOTViewSet(viewsets.ModelViewSet):

    serializer_class = StaffOTSerializer
    
    def get_queryset(self):
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return StaffOT.objects.filter(submit_by=self.request.user.id, transaction_type=transaction_type).order_by('-id')

class TeamStaffOTViewSet(viewsets.ModelViewSet):

    serializer_class = StaffOTSerializer

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
        
        employee_id_list = employees_indept.union(employees_incomp,employees_inproject,employees_inbranch)

        employees_as_user = EmployeeMaintenance.objects.filter(id__in=employee_id_list).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=employees_as_user).exclude(id=self.request.user.id).values_list('id', flat=True)   
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return StaffOT.objects.filter(submit_by__in=users, transaction_type=transaction_type).exclude(document_number__isnull=True).order_by('-id')

class StaffOTDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StaffOTDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        staff_ot = get_object_or_404(StaffOT, pk=self.request.query_params.get('pk', None))
        return StaffOTDetail.objects.filter(staff_ot=staff_ot).order_by("ot_date")

@login_required
def staff_ot_init(request , pk):    
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    employee = get_object_or_404(EmployeeMaintenance, user=request.user)
    employee_position = employee.position_id
    staff_ot = StaffOT.objects.create(submit_by=request.user, transaction_type=transaction_type, employee=employee, employee_position =employee_position)
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

            staff_ot.document_number = '{0}-{1:05d}'.format(staff_ot_type.document_type_code, document_number)
            staff_ot.company = company
            staff_ot.department = department
            staff_ot.project = project
            staff_ot.employee = employee
            staff_ot.status = status
            staff_ot.submit_by = request.user
            staff_ot.transaction_type = transaction_type
            staff_ot.save()

            # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=transaction_type.pk , document_type=staff_ot_type)

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
def staff_ot_send_approval(request, pk):
    staff_ot = get_object_or_404(StaffOT, pk=pk)
    staff_employee = get_object_or_404(EmployeeMaintenance, user=request.user)
    reporting_officer = get_object_or_404(EmployeeMaintenance, pk=staff_employee.reporting_officer_id.pk)
    print(staff_ot.transaction_type)
    approval_level = WorkflowApprovalRule.objects.filter(transaction_type=staff_ot.transaction_type)[0]
    approval_item = get_object_or_404(ApprovalItem, pk=staff_ot.approval.pk)
    approval_item.approval_level = approval_level
    approval_item.notification = reporting_officer.employee_name + " will be added by default"
    approval_item.save()

    return redirect('approval_detail', pk=approval_item.pk)

@login_required
def staff_ot_detail(request, pk):
    if request.GET.get('from', None) == 'approval':
        approvers = ApprovalItemApprover.objects.filter(user=request.user, status='P').values_list('approval_item', flat=True)
        approval_items = ApprovalItem.objects.filter(id__in=approvers,status="IP").order_by('id')
        found = False
        next_link = reverse('approval_list')

        for approval_item in approval_items:
            if approval_item.document_pk == pk:
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

    staff_ot = get_object_or_404(StaffOT, pk=pk)
    form = DetailStaffOTForm(instance=staff_ot)
    form_reject = RejectForm()
    return render(request, 'staff_overtime/detail.html', {'staff_ot': staff_ot, 'form': form, 'form_reject': form_reject, 'next_link': next_link})

@login_required
def staff_ot_list(request, pk):
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
    return render(request, 'staff_overtime/update.html', {'staff_ot': staff_ot, 'form': form, 'form_detail':form_detail})

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

        time_out = datetime.datetime.combine(date.today(), staff_ot_detail.ot_time_out)
        time_in = datetime.datetime.combine(date.today(), staff_ot_detail.ot_time_in)
        total_ot_time = time_out - time_in
        total_ot_hours = 0
        ot_rate = 0.0
        total_ot_rate = 0.0
        holiday_event = HolidayEventMaintenance.objects.filter(event_date=staff_ot_detail.ot_date)
        total_ot_hours = total_ot_time.days * 24 + total_ot_time.seconds // 3600

        if(holiday_event.count() == 0):
            is_holiday = False
            ot_rate_object = OTRateMaintenance.objects.filter(ot_rate_name="Normal Working Day")[0]
            ot_rate = ot_rate_object.ot_rate
            total_ot_rate = total_ot_hours * ot_rate
        else:
            is_holiday = True
            ot_rate_object = holiday_event.first().ot_rate
            ot_rate = ot_rate_object.ot_rate
            total_ot_rate = total_ot_hours * ot_rate
            
        staff_ot_detail.staff_ot = staff_ot
        staff_ot_detail.is_holiday = is_holiday
        staff_ot_detail.total_ot_time = total_ot_time.seconds / 60
        staff_ot_detail.ot_rate_per_hours = ot_rate
        staff_ot_detail.total_ot_rate = total_ot_rate
        staff_ot_detail.save()
        staff_ot_rate = 0.00
        staff_ot_hours = 0

        staff_ot_detail_items = StaffOTDetail.objects.filter(staff_ot=staff_ot)
        for staff_ot_detail_item in staff_ot_detail_items:
            staff_ot_rate = decimal.Decimal(staff_ot_rate) + staff_ot_detail_item.total_ot_rate
            staff_ot_hours = staff_ot_hours + (staff_ot_detail_item.total_ot_time // 60)

        staff_ot.total_ot_hours = staff_ot_hours
        staff_ot.total_ot_rate = staff_ot_rate
        staff_ot.save()
        
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success', 'total_ot_hours': staff_ot_hours, 'total_ot_rate':staff_ot_rate}) 

@login_required
def staff_ot_detail_delete(request):
    staff_ot_detail =  get_object_or_404(StaffOTDetail, pk=request.POST['hiddenValue'])
    staff_ot = get_object_or_404(StaffOT, pk=staff_ot_detail.staff_ot.pk)
    staff_ot_detail.delete()

    staff_ot_items = StaffOTDetail.objects.filter(staff_ot=staff_ot)
    staff_ot_rate = 0.0
    staff_ot_hours = 0
    if(staff_ot_items.count() !=0):
        for staff_ot_detail_item in staff_ot_detail:
            staff_ot_rate = staff_ot_rate + staff_ot_detail_item.total_ot_rate
            staff_ot_hours = staff_ot_hours + (staff_ot_detail_item.total_ot_time // 60)

        staff_ot.total_ot_hours = staff_ot_hours
        staff_ot.total_ot_rate = staff_ot_rate
        staff_ot.save()
    else:
        staff_ot_rate = 0.0
        staff_ot_hours = 0
        staff_ot.total_ot_hours = staff_ot_hours
        staff_ot.total_ot_rate = staff_ot_rate
        staff_ot.save()
    return JsonResponse({'message': 'Success', 'total_ot_hours': staff_ot_hours, 'total_ot_rate':staff_ot_rate})