from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import datetime
from rest_framework import viewsets
from administration.models import CurrencyMaintenance, DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from administration.models import PaymentmodeMaintenance, EmployeeMaintenance
from administration.models import EmployeeDepartmentMaintenance,EmployeeCompanyMaintenance,EmployeeBranchMaintenance,EmployeeProjectMaintenance
from administration.models import CompanyAddressDetail,CompanyContactDetail
from approval.forms import RejectForm
from approval.models import ApprovalItem, ApprovalItemApprover
from memo.models import Memo
from purchasing.models import PurchaseOrder
from human_resource.models import StaffRecruitmentRequest
from staff_overtime.models import StaffOT
from drawer_reimbursement.models import ReimbursementRequest
from utility_dashboard.forms import UtilityRejectForm
from utility_dashboard.models import UtilityApprovalItem, UtilityApprovalItemApprover
from PDFreport.render import Render
from .forms import NewPaymentForm, UpdatePaymentForm, DetailPaymentForm, NewPYItemForm, NewPYAttachmentForm
from .models import PaymentRequest, PaymentRequestDetail, PaymentAttachment
from .serializers import PYSerializer, PYItemSerializer, PYAttachmentSerializer
from django.db.models import Q

class PYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all() #.order_by('rank')
    serializer_class = PYSerializer

class MyPYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all().order_by('-id')
    serializer_class = PYSerializer
    
    def get_queryset(self):
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return PaymentRequest.objects.filter(submit_by=self.request.user.id, transaction_type=transaction_type).order_by('-id')  

class TeamPYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all().order_by('-id')    
    serializer_class = PYSerializer

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
        #fix for my sql cannot use intersection problem
        employee_id_list = EmployeeMaintenance.objects.filter(Q(id__in=employees_indept) & Q(id__in=employees_incomp) & Q(id__in=employees_inproject) & Q(id__in=employees_inbranch)).values_list('id', flat=True)

        employees_as_user = EmployeeMaintenance.objects.filter(id__in=employee_id_list).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=employees_as_user).exclude(id=self.request.user.id).values_list('id', flat=True)   
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return PaymentRequest.objects.filter(submit_by__in=users, transaction_type=transaction_type).exclude(document_number__isnull=True).order_by('-id')  

class PYItemViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequestDetail.objects.all()
    serializer_class = PYItemSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        py = get_object_or_404(PaymentRequest, pk=self.request.query_params.get('pk', None))
        return PaymentRequestDetail.objects.filter(py=py)

class PYAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PaymentAttachment.objects.all()
    serializer_class = PYAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        py = get_object_or_404(PaymentRequest, pk=self.request.query_params.get('pk', None))
        return PaymentAttachment.objects.filter(py=py)

@login_required
def py_create(request, TransType):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=TransType)
    
    if transaction_type.transaction_type_name == "Petty Cash":
        payment_mode = get_object_or_404(PaymentmodeMaintenance, payment_mode_name="Petty Cash")
        py = PaymentRequest.objects.create(submit_by=request.user, transaction_type=transaction_type, payment_mode=payment_mode)
    else:
        py = PaymentRequest.objects.create(submit_by=request.user, transaction_type=transaction_type)
    return redirect(py_create_edit, py.pk)

@login_required
def py_create_edit(request, pk):    
    py = get_object_or_404(PaymentRequest, pk=pk)
    if request.method == 'POST':
        form = NewPaymentForm(request.POST, instance=py)
        if form.is_valid():
            payment_type = DocumentTypeMaintenance.objects.filter(document_type_code="301")[0]
            document_number = payment_type.running_number + 1
            payment_type.running_number = document_number 
            payment_type.save()

            vendor = form.cleaned_data['vendor']
            currency = form.cleaned_data['currency']
            company = form.cleaned_data['company']
            transaction_type = form.cleaned_data['transaction_type']
            project = form.cleaned_data['project']
            employee = form.cleaned_data['employee']
            payment_mode = form.cleaned_data['payment_mode']
            py = form.save(commit=False)
            py.document_number = '{0}-{1:05d}'.format(payment_type.document_type_code, document_number)
            py.currency = currency
            py.vendor = vendor
            py.employee = employee
            py.company = company
            py.transaction_type = transaction_type
            py.project = project
            py.payment_mode = payment_mode
            py.submit_by = request.user
            py.save()

            document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="301")
            transaction_type = get_object_or_404(TransactiontypeMaintenance, pk = transaction_type.pk, document_type=document_type)
       
            if py.transaction_type.is_utility == False:
                approval_item = ApprovalItem()        
                approval_item.document_number = py.document_number
                approval_item.document_pk = py.pk
                approval_item.document_type = document_type
                approval_item.transaction_type = transaction_type
                approval_item.notification = ""
                approval_item.status = "D"
                approval_item.save()

                py.approval = approval_item
                py.save()
            else:
                print("1234")
                utililty_approval_item = UtilityApprovalItem()        
                utililty_approval_item.document_number = py.document_number
                utililty_approval_item.document_pk = py.pk
                utililty_approval_item.utility_account = py.utility_account
                utililty_approval_item.document_type = document_type
                utililty_approval_item.transaction_type = transaction_type
                utililty_approval_item.notification = ""
                utililty_approval_item.status = "D"
                utililty_approval_item.save()

                py.utility_account_approval = utililty_approval_item
                py.save()

            return redirect(py_update, py.pk)
        else:
            print(form.errors)
    else:
        form = NewPaymentForm(instance=py)
        form.fields['currency'].initial = get_object_or_404(CurrencyMaintenance, alphabet="MYR")
        form_attachment = NewPYAttachmentForm()
        form_item = NewPYItemForm()
    return render(request, 'payment/create.html', {'py': py, 'form': form, 'form_item':form_item , 'form_attachment': form_attachment})


@login_required
def py_initupdate(request, pk): 
    py = get_object_or_404(PaymentRequest, pk=pk)
    if request.method == 'POST':
        form = UpdatePaymentForm(request.POST, instance=py)
        if form.is_valid():
            py = form.save()
            py.save()
        else:
            print(form.errors)


@login_required
def py_send_approval(request, pk):
    if request.method == 'POST':
        py_initupdate(request,pk)
        
    py = get_object_or_404(PaymentRequest, pk=pk)
    if py.transaction_type.is_utility == True:
        approval_level = WorkflowApprovalRule.objects.filter(document_amount_range2__gte=py.total_amount, document_amount_range__lte=py.total_amount)[0]
        utility_approval_item = get_object_or_404(UtilityApprovalItem, pk=py.utility_account_approval.pk)       
        utility_approval_item.approval_level = approval_level
        if approval_level.ceo_approve == True:
            utility_approval_item.notification = "CEO will added by default"

        utility_approval_item.save()
        return redirect('utility_approval_detail', pk=utility_approval_item.pk)
    else: 
        if py.transaction_type.transaction_type_name == "Petty Cash":
            approval_level = WorkflowApprovalRule.objects.filter(document_amount_range2__gte=py.total_amount, document_amount_range__lte=py.total_amount, transaction_type=py.transaction_type)[0]
            approval_item = get_object_or_404(ApprovalItem, pk=py.approval.pk)       
            approval_item.approval_level = approval_level
            if approval_level.supervisor_approve:
                submiter = get_object_or_404(EmployeeMaintenance, user=request.user)
                supervisor = get_object_or_404(EmployeeMaintenance, id=submiter.reporting_officer_id.id)
                notification = supervisor.employee_name
                # if approval_rule_group.count() > 0:
                print(approval_level.ceo_approve_overwrite)
                if approval_level.ceo_approve_overwrite == True:
                    print(notification)
                    if supervisor.employee_group.group_name != "Group A":
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

                        approval_item.notification = notification + " and " + second_approver.employee_name + " will added by default"
                    else:
                        approval_item.notification = notification +" will be added by default"
                        
                elif approval_level.ceo_approve == True:
                    approval_item.notification = "CEO will added by default"
                else:
                    approval_item.notification = notification + " will added by default"

            elif approval_level.ceo_approve == True:
                approval_item.notification = "CEO will added by default"


            approval_item.save()
            return redirect('approval_detail', pk=approval_item.pk)
        else:
            approval_level = WorkflowApprovalRule.objects.filter(document_amount_range2__gte=py.total_amount, document_amount_range__lte= py.total_amount)[0]
            approval_item = get_object_or_404(ApprovalItem, pk=py.approval.pk)       
            approval_item.approval_level = approval_level
            if approval_level.ceo_approve == True:
                approval_item.notification = "CEO will added by default"
            approval_item.save()
            return redirect('approval_detail', pk=approval_item.pk)

    return redirect('approval_detail', pk=approval_item.pk)

@login_required
def py_item_create_formcreate(request, pk):    
    form = NewPYItemForm(request.POST)
    if form.is_valid():
        py_item = form.save(commit=False)
        tax = form.cleaned_data['tax']
        py = get_object_or_404(PaymentRequest, pk=pk)
        payment_items = PaymentRequestDetail.objects.filter(py=py)
        py_item.py = py
        py_item.tax= tax
        line_total = 0
        taxamount = py_item.price * tax.rate / 100
        py_item.line_taxamount = taxamount
        line_total = py_item.price + taxamount
        py_item.line_total = line_total
        py_item.linenum = payment_items.count() + 1
        py_item.save()
        
        sub_total = 0
        price = 0
        total_tax_amount = 0
        payment_items = PaymentRequestDetail.objects.filter(py=py)
        for payment_item in payment_items:
            sub_total += payment_item.price
            price += payment_item.line_total
            total_tax_amount += payment_item.line_taxamount

        py.sub_total = sub_total
        py.tax_amount = total_tax_amount
        py.total_amount = price
        py.save()

    else:
        print(form.errors)
    return JsonResponse({'message': 'Success', 'sub_total': sub_total, 'tax_amount':total_tax_amount})

@login_required
def py_item_delete_formcreate(request, pk):
    py_item = get_object_or_404(PaymentRequestDetail, pk=pk)
    py = get_object_or_404(PaymentRequest, pk=py_item.py.pk)
    py_item.delete()

    sub_total = 0
    price = 0
    total_tax_amount = 0
    payment_items = PaymentRequestDetail.objects.filter(py=py)
    if(payment_items.count() !=0):
        for payment_item in payment_items:
            sub_total += payment_item.price
            price += payment_item.line_total
            total_tax_amount += payment_item.line_taxamount

        # total_amount_afterdiscount = (sub_total - discount_amount)
        # after_add_taxamount = total_amount_afterdiscount + total_tax_amount
        # discount_rate = (discount_amount / sub_total) * 100 
        py.sub_total = sub_total
        py.tax_amount = total_tax_amount
        py.total_amount = price
        py.save()
        
    else:
        sub_total = 0.00
        total_tax_amount = 0.00
        price=0.00
        py.sub_total = sub_total
        py.tax_amount = total_tax_amount
        py.total_amount = price
        py.save()

    return JsonResponse({'message': 'Success', 'sub_total': sub_total, 'tax_amount':total_tax_amount})

@login_required
def py_attachment_create_formcreate(request, pk):    
    form = NewPYAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        py_attachment = form.save(commit=False)
        py = get_object_or_404(PaymentRequest, pk=pk)
        py_attachment.py = py
        py_attachment.save()
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success'}) 

@login_required
def py_attachment_delete_formcreate(request, pk):
    py_attachment = get_object_or_404(PaymentAttachment, pk=pk)
    py = get_object_or_404(PaymentRequest, pk=py_attachment.py.pk)
    py_attachment.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def py_delete(request, pk):
    py = get_object_or_404(PaymentRequest, pk=pk)
    py.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def py_detail(request, pk):
    if request.GET.get('from', None) == 'approval':
        approvers = ApprovalItemApprover.objects.filter(user=request.user, status='P').values_list('approval_item', flat=True)
        approval_items = ApprovalItem.objects.filter(id__in=approvers,status="IP").order_by('-id')
        found = False
        next_link = reverse('approval_list')
        utility_account_id ="1"
        utility_next_link =""
        # n = 0
        for approval_item in approval_items:
            # n+=1
            if approval_item.document_pk == pk:
                found = True
                # print(found)
                # print(n)
            elif found:
                # print(n)
                found = False
                document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
                # print(approval_item.document_pk)
                if document_type.document_type_code == "601":
                    document = get_object_or_404(Memo, pk=approval_item.document_pk)
                    next_link = reverse('memo_detail', args=(approval_item.document_pk, ))
                elif document_type.document_type_code == "205":
                    document = get_object_or_404(PurchaseOrder, pk=approval_item.document_pk)
                    next_link = reverse('po_detail', args=(approval_item.document_pk, ))
                elif document_type.document_type_code == "301":
                    document = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
                    next_link = reverse('py_detail', args=(approval_item.document_pk, ))
                    # print(next_link)
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

    elif request.GET.get('from', None) == 'utilityapproval':
        approvers = UtilityApprovalItemApprover.objects.filter(user=request.user, status='P').values_list('utility_approval_item', flat=True)
        utility_account_id = int(request.GET.get('utilityaccount', None))
        approval_items = UtilityApprovalItem.objects.filter(id__in=approvers,utility_account_id=utility_account_id,status="IP").order_by('-id')
        found = False
        utility_next_link = reverse('utility_approval_list', args=(utility_account_id, ))
        next_link =""

        for approval_item in approval_items:
            if approval_item.document_pk == pk:
                found = True
            elif found:
                found = False
                document_type = get_object_or_404(DocumentTypeMaintenance, pk=approval_item.document_type.pk)
                if document_type.document_type_code == "301":
                    document = get_object_or_404(PaymentRequest, pk=approval_item.document_pk)
                    utility_next_link = reverse('py_detail', args=(approval_item.document_pk, ))

        utility_next_link = utility_next_link + '?from=utilityapproval&utilityaccount='+request.GET.get('utilityaccount', None)

    else:
        next_link = reverse('approval_list')
        utility_next_link= reverse('account_selection_list')

    py = get_object_or_404(PaymentRequest, pk=pk)
    form = DetailPaymentForm(instance=py)
    form_reject = RejectForm()
    utility_form_reject = UtilityRejectForm()
    
    return render(request, 'payment/detail.html', {'py': py, 'form': form, 'form_reject': form_reject, 'next_link': next_link,'utility_form_reject':utility_form_reject,'utility_next_link':utility_next_link})

@login_required
def pylist(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'payment/list.html', {'trans_type': transaction_type})

# @login_required
# def pylist_pettycash(request):
#     return render(request, 'pylist_pettycash.html')

# @login_required
# def pylist_cashback(request):
#     return render(request, 'pylist_cashback.html')

# @login_required
# def pylist_salescommission(request):
#     return render(request, 'pylist_salecommisions.html')

@login_required
def py_update(request, pk): 
    py = get_object_or_404(PaymentRequest, pk=pk)
    if request.method == 'POST':
        form = UpdatePaymentForm(request.POST, instance=py)
        if form.is_valid():
            py = form.save()
            py.revision = py.revision + 1
            py.save()
            return redirect('py_detail', pk=py.pk)
        else:
            print(form.errors)
    else:
        form = UpdatePaymentForm(instance=py)
        form_item = NewPYItemForm()
        form_attachment = NewPYAttachmentForm()
    return render(request, 'payment/update.html', {'py': py, 'form': form, 'form_item':form_item , 'form_attachment':form_attachment})

@login_required
def py_item_create(request, pk):    
    form = NewPYItemForm(request.POST)
    if form.is_valid():
        py_item = form.save(commit=False)
        tax = form.cleaned_data['tax']
        py = get_object_or_404(PaymentRequest, pk=pk)
        payment_items = PaymentRequestDetail.objects.filter(py=py)
        py_item.py = py
        py_item.tax= tax
        line_total = 0
        taxamount = py_item.price * tax.rate / 100
        py_item.line_taxamount = taxamount
        line_total = py_item.price + taxamount
        py_item.line_total = line_total
        py_item.linenum = payment_items.count() + 1
        py_item.save()
        
        sub_total = 0
        price = 0
        total_tax_amount = 0
        payment_items = PaymentRequestDetail.objects.filter(py=py)
        for payment_item in payment_items:
            sub_total += payment_item.price
            price += payment_item.line_total
            total_tax_amount += payment_item.line_taxamount

        discount_amount = py.discount_amount
        total_amount_afterdiscount = (sub_total - discount_amount)
        after_add_taxamount = total_amount_afterdiscount + total_tax_amount
        discount_rate = (discount_amount / sub_total) * 100

        py.sub_total = sub_total
        py.tax_amount = total_tax_amount
        py.total_amount = price
        py.save()
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success', 'sub_total': sub_total, 'tax_amount':total_tax_amount})

@login_required
def py_item_delete(request, pk):
    py_item = get_object_or_404(PaymentRequestDetail, pk=pk)
    py = get_object_or_404(PaymentRequest, pk=py_item.py.pk)
    py_item.delete()

    sub_total = 0
    price = 0
    total_tax_amount = 0
    payment_items = PaymentRequestDetail.objects.filter(py=py)
    if(payment_items.count() !=0):
        for payment_item in payment_items:
            sub_total += payment_item.price
            price += payment_item.line_total
            total_tax_amount += payment_item.line_taxamount

        # total_amount_afterdiscount = (sub_total - discount_amount)
        # after_add_taxamount = total_amount_afterdiscount + total_tax_amount
        # discount_rate = (discount_amount / sub_total) * 100 
        py.sub_total = sub_total
        py.tax_amount = total_tax_amount
        py.total_amount = price
        py.save()
        
    else:
        sub_total = 0.00
        total_tax_amount = 0.00
        price = 0.00
        py.sub_total = sub_total
        py.tax_amount = total_tax_amount
        py.total_amount = price
        py.save()

    return JsonResponse({'message': 'Success', 'sub_total': sub_total, 'tax_amount':total_tax_amount})

@login_required
def py_attachment_create(request, pk):    
    form = NewPYAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        py_attachment = form.save(commit=False)
        py = get_object_or_404(PaymentRequest, pk=pk)
        py_attachment.py = py
        py_attachment.save()
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success'}) 

@login_required
def py_attachment_delete(request, pk):
    py_attachment = get_object_or_404(PaymentAttachment, pk=pk)
    py = get_object_or_404(PaymentRequest, pk=py_attachment.py.pk)
    py_attachment.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def py_print(request, pk): 
    py = get_object_or_404(PaymentRequest, pk=pk)
    py_item = PaymentRequestDetail.objects.filter(py=py).order_by("linenum")
    if py.transaction_type.is_utility:
        approval_item = get_object_or_404(UtilityApprovalItem, pk=py.utility_account_approval.pk)
        approver = UtilityApprovalItemApprover.objects.filter(utility_approval_item=approval_item).order_by('-stage')[0]
    else:
        approval_item = get_object_or_404(ApprovalItem, pk=py.approval.pk)
        approver = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('-stage')[0]

    requester = get_object_or_404(User, pk=py.submit_by.pk)
    approver_employee = get_object_or_404(EmployeeMaintenance, user=approver.user)

    company_address = CompanyAddressDetail.objects.filter(company=py.company,default=True)
    if company_address.count() > 0:
        company_address = company_address[0]
    else:
        company_address = CompanyAddressDetail.objects.filter(company=py.company)
        if company_address.count() > 0:
            company_address = company_address[0]

    company_contact = CompanyContactDetail.objects.filter(company=py.company,default=True)
    if company_contact.count() > 0:
        company_contact = company_contact[0]
    else:
        company_contact = CompanyContactDetail.objects.filter(company=py.company)
        if company_contact.count() > 0:
            company_contact = company_contact[0]

    # return render(request, 'PR/print.html', {'py': py, 'py_item':py_item})
    params = {
        'py': py, 
        'py_item': py_item, 
        'request': request, 
        'approval_item': approval_item, 
        'requester': requester, 
        'approver_employee': approver_employee, 
        'company_address': company_address,
        'company_contact': company_contact,
    }
    
    pdf = Render.render('PR/print.html', params)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "PaymentRequest_%s.pdf" %(py.document_number)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return response("errors")