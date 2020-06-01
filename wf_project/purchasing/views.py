from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import datetime
from rest_framework import viewsets
from administration.models import CompanyMaintenance, CompanyAddressDetail, CurrencyMaintenance, DocumentTypeMaintenance
from administration.models import StatusMaintenance, TransactiontypeMaintenance, WorkflowApprovalRule, ProjectMaintenance
from administration.models import PaymentTermMaintenance, EmployeeMaintenance
from administration.models import EmployeeDepartmentMaintenance,EmployeeCompanyMaintenance,EmployeeBranchMaintenance,EmployeeProjectMaintenance
from administration.models import CompanyAddressDetail, CompanyContactDetail
from approval.models import ApprovalItem, ApprovalItemApprover
from approval.forms import RejectForm
from memo.models import Memo
from payment.models import PaymentRequest
from human_resource.models import StaffRecruitmentRequest
from staff_overtime.models import StaffOT
from drawer_reimbursement.models import ReimbursementRequest
from PDFreport.render import Render
from stock.models import StockReturn, StockReturnDetail
from .forms import NewPOForm, DetailPOForm, UpdatePOForm, NewPOAttachmentForm, NewPOComparison2AttachmentForm
from .forms import NewPOComparison3AttachmentForm, NewPODetailForm, NewGRNForm, DetailGRNForm
from .forms import NewINVForm, DetailINVForm
from .models import PurchaseOrder, PurchaseOrderDetail, PurchaseOrderAttachment, PurchaseOrderComparison2Attachment
from .models import PurchaseOrderComparison3Attachment, VendorMasterData, VendorAddressDetail
from .models import GoodsReceiptNote, PurchaseInvoice, PurchaseCreditNote, PurchaseDebitNote
from .serializers import POSerializer, PODetailSerializer, POAttachmentSerializer, POComparison2AttachmentSerializer, POComparison3AttachmentSerializer
from payment.models import PaymentRequest, PaymentRequestDetail
from django.db.models import Q

class POAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderAttachment.objects.all()
    serializer_class = POAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder, pk=self.request.query_params.get('pk', None))
        return PurchaseOrderAttachment.objects.filter(po=po).order_by('-id')

class POComparison2AttachmentViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderComparison2Attachment.objects.all()
    serializer_class = POComparison2AttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder, pk=self.request.query_params.get('pk', None))
        return PurchaseOrderComparison2Attachment.objects.filter(po=po).order_by('-id')

class POComparison3AttachmentViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderComparison3Attachment.objects.all()
    serializer_class = POComparison3AttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder, pk=self.request.query_params.get('pk', None))
        return PurchaseOrderComparison3Attachment.objects.filter(po=po).order_by('-id')

class PODetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderDetail.objects.all()
    serializer_class = PODetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder, pk=self.request.query_params.get('pk', None))
        return PurchaseOrderDetail.objects.filter(po=po)

class MyPOViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')
    serializer_class = POSerializer
    
    def get_queryset(self):
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return PurchaseOrder.objects.filter(submit_by=self.request.user.id, transaction_type=transaction_type).order_by('-id')

class TeamPOViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')    
    serializer_class = POSerializer

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

        employees_as_user = EmployeeMaintenance.objects.filter(id__in=employee_id_list).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=employees_as_user).exclude(id=self.request.user.id).values_list('id', flat=True)   
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return PurchaseOrder.objects.filter(submit_by__in=users, transaction_type=transaction_type).exclude(document_number__isnull=True).order_by('-id')

class AwaitGRNViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')
    serializer_class = POSerializer

    def get_queryset(self):
        po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
        transaction_type = TransactiontypeMaintenance.objects.filter(document_type=po_type, transaction_type_name="Purchase Order")[0]
        po_with_grn = GoodsReceiptNote.objects.filter(receive_by=self.request.user.id).values_list('po_id', flat=True)
        approved_pos = ApprovalItem.objects.filter(document_type=po_type, status="A").values_list('document_pk', flat=True)
        return PurchaseOrder.objects.filter(submit_by=self.request.user.id, id__in=approved_pos, transaction_type=transaction_type).exclude(id__in=po_with_grn).order_by('-id')

class ReceivedGRNViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')
    serializer_class = POSerializer

    def get_queryset(self):
        po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
        transaction_type = TransactiontypeMaintenance.objects.filter(document_type=po_type, transaction_type_name="Purchase Order")[0]
        po_with_grn = GoodsReceiptNote.objects.filter(receive_by=self.request.user.id).values_list('po_id', flat=True)
        return PurchaseOrder.objects.filter(submit_by=self.request.user.id, id__in=po_with_grn, transaction_type=transaction_type).order_by('-id')

class AwaitPIViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')
    serializer_class = POSerializer

    def get_queryset(self):
        po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
        transaction_type = TransactiontypeMaintenance.objects.filter(document_type=po_type, transaction_type_name="Purchase Order")[0]
        po_with_grn = GoodsReceiptNote.objects.filter(receive_by=self.request.user.id).values_list('po_id', flat=True)
        po_with_inv = PurchaseInvoice.objects.filter(receive_by=self.request.user.id).values_list('po_id', flat=True)
        return PurchaseOrder.objects.filter(submit_by=self.request.user.id, id__in=po_with_grn, transaction_type=transaction_type).exclude(id__in=po_with_inv).order_by('-id')

class ReceivedPIViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')
    serializer_class = POSerializer

    def get_queryset(self):
        po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
        transaction_type = TransactiontypeMaintenance.objects.filter(document_type=po_type, transaction_type_name="Purchase Order")[0]
        approved_pos = ApprovalItem.objects.filter(document_type=po_type, status="A").values_list('document_pk', flat=True)
        po_with_inv = PurchaseInvoice.objects.filter(receive_by=self.request.user.id).values_list('po_id', flat=True)
        return PurchaseOrder.objects.filter(submit_by=self.request.user.id, id__in=po_with_inv, transaction_type=transaction_type).order_by('-id')

@login_required
def po_delete(request):
    po = get_object_or_404(PurchaseOrder, pk=request.POST['hiddenValue'])
    po.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def po_list(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'po/list.html', {'trans_type': transaction_type})

@login_required
def po_detail(request, pk):
    if request.GET.get('from', None) == 'approval':
        approvers = ApprovalItemApprover.objects.filter(user=request.user, status='P').values_list('approval_item', flat=True)
        approval_items = ApprovalItem.objects.filter(id__in=approvers,status="IP").order_by('-id')
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

    po = get_object_or_404(PurchaseOrder, pk=pk)
    document_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
    approval_item = get_object_or_404(ApprovalItem, document_pk=pk, document_type=document_type)
    form = DetailPOForm(instance=po)
    form.fields['vendor'].initial = po.vendor
    form.fields['company'].initial = po.company
    form.fields['currency'].initial = po.currency
    form.fields['project'].initial = po.project
    form.fields['transaction_type'].initial = po.transaction_type
    form.fields['delivery_receiver'].initial = po.delivery_receiver
    form.fields['comparison_vendor_2'].initial = po.comparison_vendor_2
    form.fields['comparison_vendor_3'].initial = po.comparison_vendor_3
    form.fields['subject'].initial = po.subject
    form.fields['payment_term'].initial = po.payment_term
    form.fields['payment_schedule'].initial = po.payment_schedule
    form.fields['vendor_address'].initial = po.vendor_address
    form_reject = RejectForm()
    return render(request, 'po/detail.html', {'po': po, 'form': form, 'approval_item': approval_item, 'form_reject': form_reject, 'next_link': next_link})

@login_required
def po_init(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    po = PurchaseOrder.objects.create(submit_by=request.user, transaction_type=transaction_type)
    return redirect(po_create, po.pk)

@login_required
def po_create(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = NewPOForm(request.POST, instance=po)
        discount = 0
        discount_amount = 0
        sub_total = 0
        tax_amount = 0
        total_amount = 0
        comparison_vendor_2_amount = 0
        comparison_vendor_3_amount = 0
        if form.is_valid():
            discount = form.cleaned_data['discount']
            discount_amount = form.cleaned_data['discount_amount']
            sub_total = form.cleaned_data['sub_total']
            tax_amount = form.cleaned_data['tax_amount']
            total_amount = form.cleaned_data['total_amount']
            comparison_vendor_2_amount = form.cleaned_data['comparison_vendor_2_amount']
            comparison_vendor_3_amount = form.cleaned_data['comparison_vendor_3_amount']
        else:
            print(form.errors)

        po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
        document_number = po_type.running_number + 1
        po_type.running_number = document_number
        po_type.save()

        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=request.POST['transaction_type'])

        po.document_number = '{0}-{1:05d}'.format(po_type.document_type_code, document_number)
        po.company = get_object_or_404(CompanyMaintenance, pk=request.POST['company'])
        po.currency = get_object_or_404(CurrencyMaintenance, pk=request.POST['currency'])
        po.vendor = get_object_or_404(VendorMasterData, pk=request.POST['vendor'])
        po.delivery_receiver = get_object_or_404(CompanyMaintenance, pk=request.POST['delivery_receiver'])     
        po.project = get_object_or_404(ProjectMaintenance, pk=request.POST['project'])
        po.status = get_object_or_404(StatusMaintenance, document_type=po_type, status_code="100")
        po.transaction_type = transaction_type
        po.reference = request.POST['reference']
        po.subject = request.POST['subject']
        po.discount = discount
        po.discount_amount = discount_amount
        po.sub_total = sub_total
        po.tax_amount = tax_amount
        po.total_amount = total_amount
        po.payment_term = get_object_or_404(PaymentTermMaintenance, pk=request.POST['payment_term'])
        po.payment_schedule = request.POST['payment_schedule']
        po.vendor_address = request.POST['vendor_address']
        po.delivery_address = request.POST['delivery_address']
        po.delivery_instruction = request.POST['delivery_instruction']
        po.remarks = request.POST['remarks']

        if request.POST['comparison_vendor_2'] != '':
            po.comparison_vendor_2 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_2'])
        
        po.comparison_vendor_2_amount = comparison_vendor_2_amount
        
        if request.POST['comparison_vendor_3'] != '':
            po.comparison_vendor_3 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_3'])
        
        po.comparison_vendor_3_amount = comparison_vendor_3_amount
        po.submit_by = request.user
        po.save()
        
        approval_item = ApprovalItem()        
        approval_item.document_number = po.document_number
        approval_item.document_pk = po.pk
        approval_item.document_type = po_type
        approval_item.transaction_type = transaction_type
        approval_item.notification = ""
        approval_item.status = "D"
        approval_item.save()

        po.approval = approval_item
        po.save()

        return redirect(po_update, po.pk)
    else:
        form = NewPOForm(instance=po)
        form.fields['currency'].initial = get_object_or_404(CurrencyMaintenance, alphabet="MYR")
        form.fields['transaction_type'].initial = po.transaction_type
    form_attachment = NewPOAttachmentForm()
    form_cov2_attachment = NewPOComparison2AttachmentForm()
    form_cov3_attachment = NewPOComparison3AttachmentForm()
    form_detail = NewPODetailForm()
    return render(request, 'po/create.html', {'po': po, 'form': form, 'form_attachment': form_attachment, 'form_cov2_attachment': form_cov2_attachment, 'form_cov3_attachment': form_cov3_attachment, 'form_detail': form_detail})

@login_required
def po_send_approval(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    approval_level = WorkflowApprovalRule.objects.filter(document_amount_range2__gte=po.total_amount, document_amount_range__lte= po.total_amount)[0]
    approval_item = get_object_or_404(ApprovalItem, pk=po.approval.pk)
    approval_item.approval_level = approval_level

    if approval_level.ceo_approve == True:
        approval_item.notification = "CEO will added by default"

    approval_item.save()

    return redirect('approval_detail', pk=approval_item.pk)

@login_required
def po_update(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = UpdatePOForm(request.POST, instance=po)
        discount = 0
        discount_amount = 0
        sub_total = 0
        tax_amount = 0
        total_amount = 0
        comparison_vendor_2_amount = 0
        comparison_vendor_3_amount = 0
        if form.is_valid():
            discount = form.cleaned_data['discount']
            discount_amount = form.cleaned_data['discount_amount']
            sub_total = form.cleaned_data['sub_total']
            tax_amount = form.cleaned_data['tax_amount']
            total_amount = form.cleaned_data['total_amount']
            comparison_vendor_2_amount = form.cleaned_data['comparison_vendor_2_amount']
            comparison_vendor_3_amount = form.cleaned_data['comparison_vendor_3_amount']
        else:
            print(form.errors)

        po_type = DocumentTypeMaintenance.objects.filter(document_type_code="205")[0]
        po.document_number = request.POST['document_number']
        po.company = get_object_or_404(CompanyMaintenance, pk=request.POST['company'])
        po.currency = get_object_or_404(CurrencyMaintenance, pk=request.POST['currency'])
        po.status = get_object_or_404(StatusMaintenance, document_type=po_type, status_code="100")
        po.vendor = get_object_or_404(VendorMasterData, pk=request.POST['vendor'])
        po.delivery_receiver = get_object_or_404(CompanyMaintenance, pk=request.POST['delivery_receiver'])     
        po.project = get_object_or_404(ProjectMaintenance, pk=request.POST['project'])
        po.transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=request.POST['transaction_type'])
        po.reference = request.POST['reference']
        po.subject = request.POST['subject']
        po.discount = discount
        po.discount_amount = discount_amount
        po.sub_total = sub_total
        po.tax_amount = tax_amount
        po.total_amount = total_amount
        po.payment_term = get_object_or_404(PaymentTermMaintenance, pk=request.POST['payment_term'])
        po.payment_schedule = request.POST['payment_schedule']
        po.vendor_address = request.POST['vendor_address']
        po.delivery_address = request.POST['delivery_address']
        po.delivery_instruction = request.POST['delivery_instruction']
        po.remarks = request.POST['remarks']

        if request.POST['comparison_vendor_2'] != '':
            po.comparison_vendor_2 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_2'])
        
        po.comparison_vendor_2_amount = comparison_vendor_2_amount
        
        if request.POST['comparison_vendor_3'] != '':
            po.comparison_vendor_3 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_3'])
            
        po.comparison_vendor_3_amount = comparison_vendor_3_amount
        po.revision = po.revision + 1
        po.submit_by = request.user
        po.save()
        return redirect(po_detail, pk=po.pk)
    else:
        form = UpdatePOForm(instance=po)
        form.fields['vendor'].initial = po.vendor
        form.fields['company'].initial = po.company
        form.fields['currency'].initial = po.currency
        form.fields['project'].initial = po.project
        form.fields['transaction_type'].initial = po.transaction_type
        form.fields['delivery_receiver'].initial = po.delivery_receiver
        form.fields['comparison_vendor_2'].initial = po.comparison_vendor_2
        form.fields['comparison_vendor_3'].initial = po.comparison_vendor_3
        form.fields['subject'].initial = po.subject
        form.fields['payment_term'].initial = po.payment_term
        form.fields['payment_schedule'].initial = po.payment_schedule
        form.fields['vendor_address'].initial = po.vendor_address
    form_attachment = NewPOAttachmentForm()
    form_cov2_attachment = NewPOComparison2AttachmentForm()
    form_cov3_attachment = NewPOComparison3AttachmentForm()
    form_detail = NewPODetailForm
    return render(request, 'po/update.html', {'po': po, 'form': form, 'form_attachment': form_attachment, 'form_cov2_attachment': form_cov2_attachment, 'form_cov3_attachment': form_cov3_attachment, 'form_detail': form_detail})

@login_required
def load_delivery_address(request):
    delivery = get_object_or_404(CompanyMaintenance, pk=request.GET.get('delivery_receiver'))
    # address = CompanyAddressDetail.objects.filter(company=delivery)[0]
    address = CompanyAddressDetail.objects.filter(company=delivery,default=True)
    if address.count() > 0:
        address = address[0]
    else:
        address = CompanyAddressDetail.objects.filter(company=delivery)
        if address.count() > 0:
            address = address[0]
    return render(request, 'po/delivery_address_field.html', {'address': address})

@login_required
def load_vendor_address(request):
    vendor = get_object_or_404(VendorMasterData, pk=request.GET.get('vendor'))
    # address = VendorAddressDetail.objects.filter(vendor=vendor)[0]
    address = VendorAddressDetail.objects.filter(vendor=vendor,default=True)
    if address.count() > 0:
        address = address[0]
    else:
        address = VendorAddressDetail.objects.filter(vendor=vendor)
        if address.count() > 0:
            address = address[0]
    return render(request, 'po/vendor_address_field.html', {'address': address})

@login_required
def po_attachment_create(request, pk):
    form = NewPOAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        po_attachment = form.save(commit=False)
        po = get_object_or_404(PurchaseOrder, pk=pk)
        po_attachment.po = po
        po_attachment.attachment_date = request.POST['attachment_date']
        po_attachment.save()
        
    return JsonResponse({'message': 'Success'})

@login_required
def po_attachment_delete(request, pk):
    poattachment = get_object_or_404(PurchaseOrderAttachment, pk=request.POST['hiddenValuePOA'])
    po = get_object_or_404(PurchaseOrder, pk=pk)
    poattachment.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def po_cov2_attachment_create(request, pk):
    form = NewPOComparison2AttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        po_cov2_attachment = form.save(commit=False)
        po = get_object_or_404(PurchaseOrder, pk=pk)
        po_cov2_attachment.po = po
        po_cov2_attachment.attachment_date = request.POST['attachment_date']
        po_cov2_attachment.save()
    return JsonResponse({'message': 'Success'})

@login_required
def po_cov2_attachment_delete(request, pk):
    pocov2attachment = get_object_or_404(PurchaseOrderComparison2Attachment, pk=request.POST['hiddenValuePOCV2'])
    po = get_object_or_404(PurchaseOrder, pk=pk)
    pocov2attachment.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def po_cov3_attachment_create(request, pk):    
    form = NewPOComparison3AttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        po_cov3_attachment = form.save(commit=False)
        po = get_object_or_404(PurchaseOrder, pk=pk)
        po_cov3_attachment.po = po
        po_cov3_attachment.attachment_date = request.POST['attachment_date']
        po_cov3_attachment.save()
    return JsonResponse({'message': 'Success'})

@login_required
def po_cov3_attachment_delete(request, pk):
    pocov3attachment = get_object_or_404(PurchaseOrderComparison3Attachment, pk=request.POST['hiddenValuePOCV3'])
    po = get_object_or_404(PurchaseOrder, pk=pk)
    pocov3attachment.delete()
    return JsonResponse({'message': 'Success'})

def detail_taxamount(pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    po_details = PurchaseOrderDetail.objects.filter(po=po)
    tax_total = 0
    for detail in po_details:
        tax_total = tax_total + detail.line_taxamount

    return tax_total

def detail_subtotalamount(pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    po_details = PurchaseOrderDetail.objects.filter(po=po)
    sub_total = 0
    for detail in po_details:
        sub_total = sub_total + detail.amount

    return sub_total

def detail_totalamount(pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    #sub_total = po.sub_total
    #discount = sub_total * (po.discount / 100)
    #total_amount = (sub_total - discount) + po.tax_amount
    po_details = PurchaseOrderDetail.objects.filter(po=po)
    total_amount = 0
    for detail in po_details:
        total_amount = total_amount + detail.line_total

    return total_amount

@login_required
def po_detail_create(request, pk):
    form = NewPODetailForm(request.POST)
    if form.is_valid():
        po_detail = form.save(commit=False)
        item = form.cleaned_data['item']
        uom = form.cleaned_data['uom']
        tax = form.cleaned_data['tax']
        po = get_object_or_404(PurchaseOrder, pk=pk)
        po_detail.po = po
        po_detail.item = item
        po_detail.uom = uom
        po_detail.amount = po_detail.quantity * po_detail.unit_price
        po_detail.tax = tax
        po_detail.save()

        if form.cleaned_data['tax_exclude']:
            po_detail.line_taxamount = po_detail.amount * (tax.rate/100)
            po_detail.line_total = po_detail.amount + po_detail.line_taxamount
        else:
            po_detail.line_taxamount = po_detail.amount - (po_detail.amount / (1 + (tax.rate/100)))
            po_detail.line_total = po_detail.amount
            
        po_detail.save()

        po.sub_total = detail_subtotalamount(pk=pk)
        po.tax_amount = detail_taxamount(pk=pk)
        po.save()
        
        po.total_amount = detail_totalamount(pk=pk)
        po.save()

    return JsonResponse({'message': 'Success', 'sub_total': po.sub_total, 'total_amount': po.total_amount, 'tax_amount': po.tax_amount})

@login_required
def po_detail_delete(request, pk):
    podetail = get_object_or_404(PurchaseOrderDetail, pk=request.POST['hiddenValueDetail'])
    po = get_object_or_404(PurchaseOrder, pk=pk)
    podetail.delete()

    po.sub_total = detail_subtotalamount(pk=po.pk)
    po.tax_amount = detail_taxamount(pk=po.pk)
    po.save()

    po.total_amount = detail_totalamount(pk=po.pk)
    po.save()

    return JsonResponse({'message': 'Success', 'sub_total': po.sub_total, 'total_amount': po.total_amount, 'tax_amount': po.tax_amount})

@login_required
def grn_list(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'grn/list.html', {'trans_type': transaction_type})

@login_required
def grn_init(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    # grn = GoodsReceiptNote.objects.create(receive_by=request.user, po=po)
    return redirect(grn_create, po.pk)

@login_required
def grn_create(request, pk):
    # grn = get_object_or_404(GoodsReceiptNote, pk=pk)
    po = get_object_or_404(PurchaseOrder, pk=pk)
    po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Good Receipt Note")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=po_type, transaction_type_name="Good Receipt Note")[0]
    
    if request.method == 'POST':
        form = NewGRNForm(request.POST)
        grn = GoodsReceiptNote.objects.create(receive_by=request.user, po=po)
        grn_type = DocumentTypeMaintenance.objects.filter(document_type_name="Good Receipt Note")[0]
        document_number = grn_type.running_number + 1
        grn_type.running_number = document_number
        grn_type.save()

        grn.document_number = '{0}-{1:05d}'.format(grn_type.document_type_code, document_number)
        grn.po = po
        grn.receive_by = request.user
        grn.save()

        return redirect(grn_detail, grn.pk)
    else:
        formGrn = NewGRNForm()
    
    form = DetailPOForm(instance=po)
    form.fields['vendor'].initial = po.vendor
    form.fields['company'].initial = po.company
    form.fields['currency'].initial = po.currency
    form.fields['project'].initial = po.project
    form.fields['transaction_type'].initial = po.transaction_type
    form.fields['delivery_receiver'].initial = po.delivery_receiver
    form.fields['comparison_vendor_2'].initial = po.comparison_vendor_2
    form.fields['comparison_vendor_3'].initial = po.comparison_vendor_3
    form.fields['subject'].initial = po.subject
    form.fields['payment_term'].initial = po.payment_term
    form.fields['payment_schedule'].initial = po.payment_schedule
    form.fields['vendor_address'].initial = po.vendor_address

    return render(request, 'grn/create.html', {'po': po, 'transaction_type': transaction_type, 'form': form, 'formGrn': formGrn})

@login_required
def grn_detail(request, pk):
    grn = get_object_or_404(GoodsReceiptNote, pk=pk)
    po = get_object_or_404(PurchaseOrder, pk=grn.po.id)
    po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Good Receipt Note")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=po_type, transaction_type_name="Good Receipt Note")[0]
    
    formGrn = DetailGRNForm(instance=grn)
    formGrn.fields['document_number'].initial = grn.document_number
    formGrn.fields['receive_by'].initial = grn.receive_by
    formGrn.fields['receive_date'].initial = grn.receive_date

    form = DetailPOForm(instance=po)
    form.fields['vendor'].initial = po.vendor
    form.fields['company'].initial = po.company
    form.fields['currency'].initial = po.currency
    form.fields['project'].initial = po.project
    form.fields['transaction_type'].initial = po.transaction_type
    form.fields['delivery_receiver'].initial = po.delivery_receiver
    form.fields['comparison_vendor_2'].initial = po.comparison_vendor_2
    form.fields['comparison_vendor_3'].initial = po.comparison_vendor_3
    form.fields['subject'].initial = po.subject
    form.fields['payment_term'].initial = po.payment_term
    form.fields['payment_schedule'].initial = po.payment_schedule
    form.fields['vendor_address'].initial = po.vendor_address

    return render(request, 'grn/detail.html', {'grn': grn, 'po': po, 'transaction_type': transaction_type, 'form': form, 'formGrn': formGrn})

@login_required
def pi_list(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'pi/list.html', {'trans_type': transaction_type})

@login_required
def pi_init(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    # pi = PurchaseInvoice.objects.create(receive_by=request.user, po=po)
    return redirect(pi_create, po.pk)

@login_required
def pi_create(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    # pi = get_object_or_404(PurchaseInvoice, pk=pk)
    po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Invoice")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=po_type, transaction_type_name="Purchase Invoice")[0]
    
    if request.method == 'POST':
        pi_type = DocumentTypeMaintenance.objects.filter(document_type_code="208")[0]
        document_number = pi_type.running_number + 1
        pi_type.running_number = document_number
        pi_type.save()

        pi = PurchaseInvoice.objects.create(receive_by=request.user, po=po)
        form = NewINVForm(request.POST, instance=pi)
        pi.po = po
        pi.receive_by = request.user
        pi.invoice_number = '{0}-{1:05d}'.format(pi_type.document_type_code, document_number)
        pi.save()

        return redirect(pi_detail, pi.pk)
    else:
        formPi = NewINVForm()
    
    form = DetailPOForm(instance=po)
    form.fields['vendor'].initial = po.vendor
    form.fields['company'].initial = po.company
    form.fields['currency'].initial = po.currency
    form.fields['project'].initial = po.project
    form.fields['transaction_type'].initial = po.transaction_type
    form.fields['delivery_receiver'].initial = po.delivery_receiver
    form.fields['comparison_vendor_2'].initial = po.comparison_vendor_2
    form.fields['comparison_vendor_3'].initial = po.comparison_vendor_3
    form.fields['subject'].initial = po.subject
    form.fields['payment_term'].initial = po.payment_term
    form.fields['payment_schedule'].initial = po.payment_schedule
    form.fields['vendor_address'].initial = po.vendor_address

    return render(request, 'pi/create.html', { 'po': po, 'transaction_type': transaction_type, 'form': form, 'formPi': formPi})

@login_required
def pi_send_to_pr(request, pk):
    pi = get_object_or_404(PurchaseInvoice, pk=pk)
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code ="301")
    pi_type = get_object_or_404(DocumentTypeMaintenance, document_type_code ="208")
    transaction_type = get_object_or_404(TransactiontypeMaintenance, transaction_type_name="Payment for Invoice",document_type=document_type)
    
    pr_vendor = pi.po.vendor
    pr_currency = pi.po.currency
    pr_company = pi.po.company
    pr_project = pi.po.project
    pr_subject = pi.po.subject
    pr_reference = pi.po.reference
    pr_remarks = pi.po.remarks
    pr_subtotal = pi.po.sub_total
    pr_discount = pi.po.discount
    pr_discount_amount = pi.po.discount_amount
    pr_tax_amount = pi.po.tax_amount
    pr_total_amount = pi.po.total_amount
    
    py = PaymentRequest.objects.create(submit_by=request.user, transaction_type=transaction_type,
                                        document_pk=pk, document_type=pi_type, vendor=pr_vendor, currency=pr_currency,
                                        company=pr_company, project=pr_project, subject=pr_subject, reference=pr_reference,
                                        remarks=pr_remarks, sub_total=pr_subtotal, discount_rate=pr_discount, discount_amount=pr_discount_amount,
                                        tax_amount=pr_tax_amount, total_amount=pr_total_amount)

    po_items = PurchaseOrderDetail.objects.filter(po=pi.po)
    i = 0
    for po_item in po_items:
        i = i + 1
        linenum = i
        pr_item = PaymentRequestDetail.objects.create(linenum=i, item_description=po_item.item.item_description,
                                                      line_total= po_item.line_total, price = po_item.amount, tax=po_item.tax,
                                                      line_taxamount= po_item.line_taxamount, py=py)


    return redirect('py_create_edit', py.pk)
    

@login_required
def pi_detail(request, pk):
    pi = get_object_or_404(PurchaseInvoice, pk=pk)
    po = get_object_or_404(PurchaseOrder, pk=pi.po.id)    
    pi_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Invoice")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=pi_type, transaction_type_name="Purchase Invoice")[0]
    
    formPi = DetailINVForm(instance=pi)
    formPi.fields['invoice_number'].initial = pi.invoice_number
    formPi.fields['receive_by'].initial = pi.receive_by
    formPi.fields['invoice_date'].initial = pi.invoice_date

    form = DetailPOForm(instance=po)
    form.fields['vendor'].initial = po.vendor
    form.fields['company'].initial = po.company
    form.fields['currency'].initial = po.currency
    form.fields['project'].initial = po.project
    form.fields['transaction_type'].initial = po.transaction_type
    form.fields['delivery_receiver'].initial = po.delivery_receiver
    form.fields['comparison_vendor_2'].initial = po.comparison_vendor_2
    form.fields['comparison_vendor_3'].initial = po.comparison_vendor_3
    form.fields['subject'].initial = po.subject
    form.fields['payment_term'].initial = po.payment_term
    form.fields['payment_schedule'].initial = po.payment_schedule
    form.fields['vendor_address'].initial = po.vendor_address

    return render(request, 'pi/detail.html', {'pi': pi, 'po': po, 'transaction_type': transaction_type, 'form': form, 'formPi': formPi})

@login_required
def pcn_list(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'pcn/list.html', {'trans_type': transaction_type})

@login_required
def pcn_detail(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'pcn/list.html', {'trans_type': transaction_type})

@login_required
def pdn_list(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'pdn/list.html', {'trans_type': transaction_type})

@login_required
def pdn_detail(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'pdn/list.html', {'trans_type': transaction_type})

@login_required
def po_print(request, pk): 
    po = get_object_or_404(PurchaseOrder, pk=pk)
    approval_item = get_object_or_404(ApprovalItem, pk=po.approval.pk)
    requester = get_object_or_404(User, pk=po.submit_by.pk)
    approver = ApprovalItemApprover.objects.filter(approval_item=approval_item).order_by('-stage')[0]
    approver_employee = get_object_or_404(EmployeeMaintenance, user=approver.user)
    po_details = PurchaseOrderDetail.objects.filter(po=po).order_by("id")

    company_address = CompanyAddressDetail.objects.filter(company=po.company,default=True)
    if company_address.count() > 0:
        company_address = company_address[0]
    else:
        company_address = CompanyAddressDetail.objects.filter(company=po.company)
        if company_address.count() > 0:
            company_address = company_address[0]

    company_contact = CompanyContactDetail.objects.filter(company=po.company,default=True)
    if company_contact.count() > 0:
        company_contact = company_contact[0]
    else:
        company_contact = CompanyContactDetail.objects.filter(company=po.company)
        if company_contact.count() > 0:
            company_contact = company_contact[0]

    params = {
        'po': po,
        'approval_item': approval_item,
        'requester': requester,
        'approver_employee': approver_employee,
        'po_details': po_details,
        'company_address': company_address,
        'company_contact': company_contact,
    }
    
    pdf = Render.render('report/PO/print.html', params)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "PO_%s.pdf" %(po.document_number)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return response("errors")

@login_required
def grn_print(request, pk): 
    grn = get_object_or_404(GoodsReceiptNote, pk=pk)
    po = get_object_or_404(PurchaseOrder, pk=grn.po.pk)
    po_details = PurchaseOrderDetail.objects.filter(po=po)
    company_address = CompanyAddressDetail.objects.filter(company=po.company,default=True)
    if company_address.count() > 0:
        company_address = company_address[0]
    else:
        company_address = CompanyAddressDetail.objects.filter(company=po.company)
        if company_address.count() > 0:
            company_address = company_address[0]

    company_contact = CompanyContactDetail.objects.filter(company=po.company,default=True)
    if company_contact.count() > 0:
        company_contact = company_contact[0]
    else:
        company_contact = CompanyContactDetail.objects.filter(company=po.company)
        if company_contact.count() > 0:
            company_contact = company_contact[0]

    params = {
        'po': po,
        'grn': grn,
        'po_details': po_details,
        'company_address': company_address,
        'company_contact': company_contact,
    }
    
    pdf = Render.render('report/GRN/print.html', params)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "GRN_%s.pdf" %(grn.document_number)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return response("errors")

@login_required
def pi_print(request, pk): 
    pi = get_object_or_404(PurchaseInvoice, pk=pk)
    po = get_object_or_404(PurchaseOrder, pk=pi.po.pk)
    po_details = PurchaseOrderDetail.objects.filter(po=po)
    company_address = CompanyAddressDetail.objects.filter(company=po.company,default=True)
    if company_address.count() > 0:
        company_address = company_address[0]
    else:
        company_address = CompanyAddressDetail.objects.filter(company=po.company)
        if company_address.count() > 0:
            company_address = company_address[0]

    company_contact = CompanyContactDetail.objects.filter(company=po.company,default=True)
    if company_contact.count() > 0:
        company_contact = company_contact[0]
    else:
        company_contact = CompanyContactDetail.objects.filter(company=po.company)
        if company_contact.count() > 0:
            company_contact = company_contact[0]
        
    params = {
        'po': po,
        'pi': pi,
        'po_details': po_details,
        'company_address': company_address,
        'company_contact': company_contact,
    }
    
    pdf = Render.render('report/PI/print.html', params)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "PI_%s.pdf" %(pi.invoice_number)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return response("errors")

@login_required
def grn_send_to_stock(request, pk):
    grn = get_object_or_404(GoodsReceiptNote, pk=pk)
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="214")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=document_type)[0]
    grn_type = get_object_or_404(DocumentTypeMaintenance,document_type_code ="206")
    
    
    stock_company = grn.po.company
    stock_project = grn.po.project
    stock_reference = grn.document_number
    stock_vendor = grn.po.vendor
    
    stock_return = StockReturn.objects.create(submit_by=request.user,transaction_type=transaction_type,company=stock_company,
                                        document_pk=pk,document_type=grn_type,vendor=stock_vendor,project=stock_project,reference=stock_reference)

    po_items = PurchaseOrderDetail.objects.filter(po=grn.po)
    i = 0
    for po_item in po_items:
        i = i + 1
        linenum = i
        stock_item = StockReturnDetail.objects.create(item=po_item.item,stock_return=stock_return,
                                                        additional_description=po_item.additional_description,
                                                        quantity=po_item.quantity,uom=po_item.uom,
                                                        remarks=po_item.remarks)

    return redirect('stock_return_create', stock_return.pk)
    
