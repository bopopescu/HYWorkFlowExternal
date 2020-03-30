from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewPaymentForm,UpdatePaymentForm,DetailPaymentForm,NewPYItemForm,NewPYAttachmentForm
from django.contrib.auth.decorators import login_required
from .models import PaymentRequest,PaymentRequestDetail,PaymentAttachment
from rest_framework import viewsets
from .serializers import PYSerializer,PYItemSerializer,PYAttachmentSerializer
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance
from administration.models import WorkflowApprovalRule
from approval.models import ApprovalItem
from django.contrib.auth.models import User

class PYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all() #.order_by('rank')
    serializer_class = PYSerializer

class MyPYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all().order_by('-id')
    serializer_class = PYSerializer
    
    def get_queryset(self):
        return PaymentRequest.objects.filter(submit_by=self.request.user.id)

class TeamPYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all().order_by('-id')    
    serializer_class = PYSerializer

    def get_queryset(self):
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return PaymentRequest.objects.filter(submit_by__in=users)

class PYItemViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequestDetail.objects.all()
    serializer_class = PYItemSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        py = get_object_or_404(PaymentRequest,pk=self.request.query_params.get('pk', None))
        return PaymentRequestDetail.objects.filter(py=py)

class PYAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PaymentAttachment.objects.all()
    serializer_class = PYAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        py = get_object_or_404(PaymentRequest,pk=self.request.query_params.get('pk', None))
        return PaymentAttachment.objects.filter(py=py)

@login_required
def py_create(request):    
    if request.method == 'POST':
        form = NewPaymentForm(request.POST)
        if form.is_valid():
            vendor = form.cleaned_data['vendor']
            currency = form.cleaned_data['currency']
            company = form.cleaned_data['company']
            transaction_type = form.cleaned_data['transaction_type']
            project = form.cleaned_data['project']
            employee = form.cleaned_data['employee']
            payment_mode = form.cleaned_data['payment_mode']
            py = form.save(commit=False)
            py.currency = currency
            py.vendor = vendor
            py.employee = employee
            py.company = company
            py.transaction_type = transaction_type
            py.project = project
            py.payment_mode = payment_mode
            py.submit_by = request.user
            py.save()

            document_type = get_object_or_404(DocumentTypeMaintenance,document_type_name="Payment Request")
            transaction_type = get_object_or_404(TransactiontypeMaintenance,pk = transaction_type.pk, document_type=document_type)
            approval_level = get_object_or_404(WorkflowApprovalRule,approval_level=2)

            approval_item = ApprovalItem()        
            approval_item.document_number = py.document_number
            approval_item.document_pk = py.pk
            approval_item.document_type = document_type
            approval_item.transaction_type = transaction_type
            approval_item.approval_level = approval_level
            approval_item.notification = ""
            approval_item.status = "D"
            approval_item.save()

            py.approval = approval_item
            py.save()

            return redirect(pylist)
        else:
            py = PaymentRequest
            form = NewPaymentForm()
    else:
        py = PaymentRequest
        form = NewPaymentForm()
    return render(request, 'pycreate.html', {'py': py, 'form': form})

@login_required
def py_delete(request, pk):
    py =  get_object_or_404(PaymentRequest, pk=pk)
    py.delete()
    return redirect(pylist)

@login_required
def py_detail(request, pk):
    py =  get_object_or_404(PaymentRequest, pk=pk)
    form = DetailPaymentForm(instance=py)
    return render(request, 'pydetail.html', {'py': py, 'form': form})

@login_required
def pylist(request):
    return render(request, 'pylist.html')

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
        form_attachment = NewPYAttachmentForm
    return render(request, 'pyupdate.html', {'py': py, 'form': form,'form_item':form_item ,'form_attachment':form_attachment})

@login_required
def py_item_create(request, pk):    
    form = NewPYItemForm(request.POST)
    if form.is_valid():
        py_item = form.save(commit=False)
        tax = form.cleaned_data['tax']
        py = get_object_or_404(PaymentRequest, pk=pk)
        py_item.py = py
        py_item.tax= tax
        line_total = 0
        taxamount = py_item.price * tax.rate / 100
        py_item.line_taxamount = taxamount
        line_total = py_item.price + taxamount
        py_item.line_total = line_total
        # py_item.line_num = py_item.line_num + 1
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
        py.discount_rate = discount_rate
        py.sub_total = sub_total
        py.tax_amount = total_tax_amount
        py.total_amount = after_add_taxamount
        py.save()
    else:
        print(form.errors)
    return redirect(py_update, pk=pk) 

@login_required
def py_item_delete(request, pk):
    py_item =  get_object_or_404(PaymentRequestDetail, pk=pk)
    py = get_object_or_404(PaymentRequest, pk=py_item.py.pk)
    py_item.delete()
    return redirect(py_update, pk=py.pk)

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
    return redirect(py_update, pk=pk) 

@login_required
def py_attachment_delete(request, pk):
    py_attachment =  get_object_or_404(PaymentAttachment, pk=pk)
    py = get_object_or_404(PaymentRequest, pk=py_attachment.py.pk)
    py_attachment.delete()
    return redirect(py_update, pk=py.pk)