from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NewPOForm, DetailPOForm, UpdatePOForm, NewPOAttachmentForm, NewPOComparison2AttachmentForm, NewPOComparison3AttachmentForm, NewPODetailForm
from .models import PurchaseOrder, PurchaseOrderDetail, PurchaseOrderAttachment, PurchaseOrderComparison2Attachment, PurchaseOrderComparison3Attachment, VendorMasterData, VendorAddressDetail
from rest_framework import viewsets
from .serializers import POSerializer, PODetailSerializer, POAttachmentSerializer, POComparison2AttachmentSerializer, POComparison3AttachmentSerializer
from django.contrib.auth.models import User
from administration.models import CompanyMaintenance, CompanyAddressDetail, CurrencyMaintenance, DocumentTypeMaintenance
from administration.models import StatusMaintenance, TransactiontypeMaintenance, WorkflowApprovalRule, ProjectMaintenance
from approval.models import ApprovalItem
from django.http import JsonResponse

class POAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderAttachment.objects.all()
    serializer_class = POAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder,pk=self.request.query_params.get('pk', None))
        return PurchaseOrderAttachment.objects.filter(po=po)

class POComparison2AttachmentViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderComparison2Attachment.objects.all()
    serializer_class = POComparison2AttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder,pk=self.request.query_params.get('pk', None))
        return PurchaseOrderComparison2Attachment.objects.filter(po=po)

class POComparison3AttachmentViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderComparison3Attachment.objects.all()
    serializer_class = POComparison3AttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder,pk=self.request.query_params.get('pk', None))
        return PurchaseOrderComparison3Attachment.objects.filter(po=po)

class PODetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderDetail.objects.all()
    serializer_class = PODetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        po = get_object_or_404(PurchaseOrder,pk=self.request.query_params.get('pk', None))
        return PurchaseOrderDetail.objects.filter(po=po)

class MyPOViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')
    serializer_class = POSerializer
    
    def get_queryset(self):
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return PurchaseOrder.objects.filter(submit_by=self.request.user.id, transaction_type=transaction_type)

class TeamPOViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')    
    serializer_class = POSerializer

    def get_queryset(self):
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return PurchaseOrder.objects.filter(submit_by__in=users, transaction_type=transaction_type)

@login_required
def po_delete(request):
    po =  get_object_or_404(PurchaseOrder, pk=request.POST['hiddenValue'])
    po.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def po_list(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    return render(request, 'po/list.html', {'trans_type': transaction_type})

@login_required
def po_detail(request, pk):
    po =  get_object_or_404(PurchaseOrder, pk=pk)
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
    form.fields['payment_schedule'].initial = po.payment_schedule
    form.fields['vendor_address'].initial = po.vendor_address
    return render(request, 'po/detail.html', {'po': po, 'form': form})

@login_required
def po_init(request, pk):
    transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=pk)
    po = PurchaseOrder.objects.create(submit_by=request.user, transaction_type=transaction_type)
    return redirect(po_create, po.pk)

@login_required
def po_create(request, pk):
    po =  get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = NewPOForm(request.POST, instance=po)
        po_type = DocumentTypeMaintenance.objects.filter(document_type_name="Purchase Order")[0]
        document_number = po_type.running_number + 1
        po_type.running_number = document_number 
        po_type.save()

        transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=request.POST['transaction_type'])

        po.document_number = '{0}-{1:05d}'.format(po_type.document_type_code,document_number)
        po.company = get_object_or_404(CompanyMaintenance, pk=request.POST['company'])
        po.currency = get_object_or_404(CurrencyMaintenance, pk=request.POST['currency'])
        po.vendor = get_object_or_404(VendorMasterData, pk=request.POST['vendor'])
        po.delivery_receiver = get_object_or_404(CompanyMaintenance, pk=request.POST['delivery_receiver'])     
        po.project = get_object_or_404(ProjectMaintenance, pk=request.POST['project'])
        po.status = get_object_or_404(StatusMaintenance, document_type=po_type, status_code="100")
        po.transaction_type = transaction_type
        po.reference = request.POST['reference']
        po.subject = request.POST['subject']
        po.discount = request.POST['discount']
        po.discount_amount = request.POST['discount_amount']
        po.sub_total = request.POST['sub_total']
        po.tax_amount = request.POST['tax_amount']
        po.total_amount = request.POST['total_amount']
        po.payment_term = request.POST['payment_term']
        po.payment_schedule = request.POST['payment_schedule']
        po.vendor_address = request.POST['vendor_address']
        po.delivery_address = request.POST['delivery_address']
        po.delivery_instruction = request.POST['delivery_instruction']
        po.remarks = request.POST['remarks']
        po.comparison_vendor_2 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_2'])
        po.comparison_vendor_2_amount = request.POST['comparison_vendor_2_amount']
        po.comparison_vendor_3 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_3'])
        po.comparison_vendor_3_amount = request.POST['comparison_vendor_3_amount']
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
def po_send_approval(request,pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    approval_level = WorkflowApprovalRule.objects.filter(document_amount_range2__gte=po.total_amount, document_amount_range__lte= po.total_amount)[0]
    approval_item = get_object_or_404(ApprovalItem, pk=po.approval.pk)       
    approval_item.approval_level = approval_level
    approval_item.save()

    return redirect('approval_detail', pk=approval_item.pk)

@login_required
def po_update(request, pk):
    po =  get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = UpdatePOForm(request.POST, instance=po)
        po.document_number = request.POST['document_number']
        po.company = get_object_or_404(CompanyMaintenance, pk=request.POST['company'])
        po.currency = get_object_or_404(CurrencyMaintenance, pk=request.POST['currency'])
        po.vendor = get_object_or_404(VendorMasterData, pk=request.POST['vendor'])
        po.delivery_receiver = get_object_or_404(CompanyMaintenance, pk=request.POST['delivery_receiver'])     
        po.project = get_object_or_404(ProjectMaintenance, pk=request.POST['project'])
        po.transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=request.POST['transaction_type'])
        po.reference = request.POST['reference']
        po.subject = request.POST['subject']
        po.discount = request.POST['discount']
        po.discount_amount = request.POST['discount_amount']
        po.sub_total = request.POST['sub_total']
        po.tax_amount = request.POST['tax_amount']
        po.total_amount = request.POST['total_amount']
        po.payment_term = request.POST['payment_term']
        po.payment_schedule = request.POST['payment_schedule']
        po.vendor_address = request.POST['vendor_address']
        po.delivery_address = request.POST['delivery_address']
        po.delivery_instruction = request.POST['delivery_instruction']
        po.remarks = request.POST['remarks']
        po.comparison_vendor_2 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_2'])
        po.comparison_vendor_2_amount = request.POST['comparison_vendor_2_amount']
        po.comparison_vendor_3 = get_object_or_404(VendorMasterData, pk=request.POST['comparison_vendor_3'])
        po.comparison_vendor_3_amount = request.POST['comparison_vendor_3_amount']
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
    address = CompanyAddressDetail.objects.filter(company=delivery)[0]
    return render(request, 'po/delivery_address_field.html', {'address': address})

@login_required
def load_vendor_address(request):
    vendor = get_object_or_404(VendorMasterData, pk=request.GET.get('vendor'))
    address = VendorAddressDetail.objects.filter(vendor=vendor)[0]
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
    poattachment =  get_object_or_404(PurchaseOrderAttachment, pk=request.POST['hiddenValuePOA'])
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
    pocov2attachment =  get_object_or_404(PurchaseOrderComparison2Attachment, pk=request.POST['hiddenValuePOCV2'])
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
    pocov3attachment =  get_object_or_404(PurchaseOrderComparison3Attachment, pk=request.POST['hiddenValuePOCV3'])
    po = get_object_or_404(PurchaseOrder, pk=pk)
    pocov3attachment.delete()
    return JsonResponse({'message': 'Success'})

def detail_subtotalamount(pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    po_details = PurchaseOrderDetail.objects.filter(po=po)
    sub_total = 0
    for detail in po_details:
        sub_total = sub_total + detail.amount

    return sub_total

def detail_totalamount(pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    sub_total = po.sub_total
    discount = sub_total * (po.discount / 100)
    total_amount = (sub_total - discount) + po.tax_amount
    
    return total_amount

@login_required
def po_detail_create(request, pk):    
    form = NewPODetailForm(request.POST)
    if form.is_valid():
        po_detail = form.save(commit=False)
        item = form.cleaned_data['item']
        uom = form.cleaned_data['uom']    
        po = get_object_or_404(PurchaseOrder, pk=pk)
        po_detail.po = po
        po_detail.item = item
        po_detail.uom = uom
        po_detail.amount = po_detail.quantity * po_detail.unit_price
        po_detail.save()
        
        po = get_object_or_404(PurchaseOrder, pk=pk)
        po.sub_total = detail_subtotalamount(pk=pk)
        po.save()

        po = get_object_or_404(PurchaseOrder, pk=pk)
        po.total_amount = detail_totalamount(pk=pk)
        po.save()    
    return JsonResponse({'message': 'Success', 'sub_total': po.sub_total, 'total_amount': po.total_amount})

@login_required
def po_detail_delete(request, pk):
    podetail=  get_object_or_404(PurchaseOrderDetail, pk=request.POST['hiddenValueDetail'])
    po = get_object_or_404(PurchaseOrder, pk=pk)
    podetail.delete()

    po.sub_total = detail_subtotalamount(pk=po.pk)
    po.save()

    po.total_amount = detail_totalamount(pk=po.pk)
    po.save()
    return JsonResponse({'message': 'Success', 'sub_total': po.sub_total, 'total_amount': po.total_amount})