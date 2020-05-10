from django.shortcuts import render,redirect, get_object_or_404
from .forms import NewStockTransferForm, UpdateStockTransferForm, DetailStockTransferForm, NewStockTransferDetailForm, NewStockTransferAttachmentForm
from .forms import NewStockAdjustmentForm, UpdateStockAdjustmentForm, DetailStockAdjustmentForm, NewStockAdjustmentDetailForm, NewStockAdjustmentAttachmentForm
from .forms import NewStockIssuingForm, UpdateStockIssuingForm, DetailStockIssuingForm, NewStockIssuingDetailForm, NewStockIssuingAttachmentForm
from .forms import NewStockReturnForm, UpdateStockReturnForm, DetailStockReturnForm, NewStockReturnDetailForm, NewStockReturnAttachmentForm
from .forms import StockBalanceReport,StockBalanceReportLocation
from django.contrib.auth.decorators import login_required
from .models import StockTransfer,StockTransferDetail,StockTransferAttachment
from .models import StockAdjustment,StockAdjustmentDetail,StockAdjustmentAttachment
from .models import StockIssuing,StockIssuingDetail,StockIssuingAttachment
from .models import StockReturn,StockReturnDetail,StockReturnAttachment
from .models import ItemMovement
from Inventory.models import Item
from rest_framework import viewsets
from .serializers import StockTransferSerializer, StockTransferDetailSerializer, StockTransferAttachmentSerializer
from .serializers import StockAdjustmentSerializer, StockAdjustmentDetailSerializer, StockAdjustmentAttachmentSerializer
from .serializers import StockIssuingSerializer, StockIssuingDetailSerializer, StockIssuingAttachmentSerializer
from .serializers import StockReturnSerializer, StockReturnDetailSerializer, StockReturnAttachmentSerializer
from administration.models import DocumentTypeMaintenance
from administration.models import TransactiontypeMaintenance,CompanyMaintenance,CompanyAddressDetail
from administration.models import WorkflowApprovalRule,StatusMaintenance,LocationMaintenance
from django.contrib.auth.models import User
import datetime
from django.http import JsonResponse
from PDFreport.render import Render
from django.http import HttpResponse
from django.db.models.aggregates import Sum

# Stock Transfer ViewSet
class MyStockTransferViewSet(viewsets.ModelViewSet):
    serializer_class = StockTransferSerializer
    
    def get_queryset(self):
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return StockTransfer.objects.filter(submit_by=self.request.user.id).order_by('-id')  

class TeamStockTransferViewSet(viewsets.ModelViewSet):   
    serializer_class = StockTransferSerializer

    def get_queryset(self):
        # document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="301")
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return StockTransfer.objects.filter(submit_by__in=users).order_by('-id')  

class StockTransferDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StockTransferDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_transfer = get_object_or_404(StockTransfer, pk=self.request.query_params.get('pk', None))
        return StockTransferDetail.objects.filter(stock_transfer=stock_transfer)

class StockTransferAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = StockTransferAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_transfer = get_object_or_404(StockTransfer, pk=self.request.query_params.get('pk', None))
        return StockTransferAttachment.objects.filter(stock_transfer=stock_transfer)

# Stock Adjustment ViewSet
class MyStockAdjustmentViewSet(viewsets.ModelViewSet):
    serializer_class = StockAdjustmentSerializer
    
    def get_queryset(self):
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return StockAdjustment.objects.filter(submit_by=self.request.user.id).order_by('-id')  

class TeamStockAdjustmentViewSet(viewsets.ModelViewSet):   
    serializer_class = StockAdjustmentSerializer

    def get_queryset(self):
        # document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="301")
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return StockAdjustment.objects.filter(submit_by__in=users).order_by('-id')  

class StockAdjustmentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StockAdjustmentDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_adjustment = get_object_or_404(StockAdjustment, pk=self.request.query_params.get('pk', None))
        return StockAdjustmentDetail.objects.filter(stock_adjustment=stock_adjustment)

class StockAdjustmentAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = StockAdjustmentAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_adjustment = get_object_or_404(StockAdjustment, pk=self.request.query_params.get('pk', None))
        return StockAdjustmentAttachment.objects.filter(stock_adjustment=stock_adjustment)

# Stock Issuing ViewSet
class MyStockIssuingViewSet(viewsets.ModelViewSet):
    serializer_class = StockIssuingSerializer
    
    def get_queryset(self):
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return StockIssuing.objects.filter(submit_by=self.request.user.id).order_by('-id')  

class TeamStockIssuingViewSet(viewsets.ModelViewSet):   
    serializer_class = StockIssuingSerializer

    def get_queryset(self):
        # document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="301")
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return StockIssuing.objects.filter(submit_by__in=users).order_by('-id')  

class StockIssuingDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StockIssuingDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_issuing = get_object_or_404(StockIssuing, pk=self.request.query_params.get('pk', None))
        return StockIssuingDetail.objects.filter(stock_issuing=stock_issuing)

class StockIssuingAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = StockIssuingAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_issuing = get_object_or_404(StockIssuing, pk=self.request.query_params.get('pk', None))
        return StockIssuingAttachment.objects.filter(stock_issuing=stock_issuing)

# Stock Return ViewSet
class MyStockReturnViewSet(viewsets.ModelViewSet):
    serializer_class = StockReturnSerializer
    
    def get_queryset(self):
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        return StockReturn.objects.filter(submit_by=self.request.user.id).order_by('-id')  

class TeamStockReturnViewSet(viewsets.ModelViewSet):   
    serializer_class = StockReturnSerializer

    def get_queryset(self):
        # document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="301")
        # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=self.request.query_params.get('trans_type', None))
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return StockReturn.objects.filter(submit_by__in=users).order_by('-id')  

class StockReturnDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StockReturnDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_return = get_object_or_404(StockReturn, pk=self.request.query_params.get('pk', None))
        return StockReturnDetail.objects.filter(stock_return=stock_return)

class StockReturnAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = StockReturnAttachmentSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        stock_return = get_object_or_404(StockReturn, pk=self.request.query_params.get('pk', None))
        return StockReturnAttachment.objects.filter(stock_return=stock_return)

#Stock Transfer
@login_required
def stock_transfer_init(request):    
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=document_type)[0]

    stock_transfer = StockTransfer.objects.create(submit_by=request.user, transaction_type=transaction_type)
    return redirect(stock_transfer_create, stock_transfer.pk)

@login_required
def stock_transfer_create(request, pk):    
    stock_transfer = get_object_or_404(StockTransfer, pk=pk)
    if request.method == 'POST':
        form = NewStockTransferForm(request.POST, instance=stock_transfer)
        if form.is_valid():

            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]
            document_number = document_type.running_number + 1
            document_type.running_number = document_number 
            document_type.save()

            company = form.cleaned_data['company']
            transaction_type = form.cleaned_data['transaction_type']
            project = form.cleaned_data['project']
            from_location = form.cleaned_data['from_location']
            to_location = form.cleaned_data['to_location']

            status = get_object_or_404(StatusMaintenance, document_type=document_type, status_code="100")

            stock_transfer.document_number = '{0}-{1:05d}'.format(document_type.document_type_code, document_number)
            stock_transfer.company = company
            stock_transfer.project = project
            stock_transfer.from_location = from_location
            stock_transfer.to_location = to_location
            stock_transfer.status = status
            stock_transfer.submit_by = request.user
            stock_transfer.transaction_type = transaction_type
            stock_transfer.save()

            # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=transaction_type.pk , document_type=staff_ot_type)

            return redirect(stock_transfer_update, pk=stock_transfer.pk)
        else:
            print(form.errors)
            form = NewStockTransferForm(instance=stock_transfer)
            form_detail = NewStockTransferDetailForm()
            form_attachment = NewStockTransferAttachmentForm()
    else:
        form = NewStockTransferForm(instance=stock_transfer)
        form_detail = NewStockTransferDetailForm()
        form_attachment = NewStockTransferAttachmentForm()
    return render(request, 'stock/stock_transfer/create.html', {'stock_transfer': stock_transfer, 'form': form, 'form_detail': form_detail,'form_attachment':form_attachment})

@login_required
def stock_transfer_submit(request, pk):
    stock_transfer = get_object_or_404(StockTransfer, pk=pk)
    stock_transfer_details = StockTransferDetail.objects.filter(stock_transfer=stock_transfer)
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="211")[0]
    status = StatusMaintenance.objects.filter(document_type=document_type,status_code='400')[0]

    for stock_transfer_detail in stock_transfer_details:
        item_movement_stock_in = ItemMovement()     
        item_movement_stock_out = ItemMovement()
        # from location
        item_movement_stock_out.location = stock_transfer.from_location
        item_movement_stock_out.document_type = document_type
        item_movement_stock_out.document_pk = stock_transfer.id
        item_movement_stock_out.item = stock_transfer_detail.item
        item_movement_stock_out.stock_out = stock_transfer_detail.quantity
        item_movement_stock_out.stock_in = 0.0
        item_movement_stock_out.save()

        # to location
        item_movement_stock_in.location = stock_transfer.to_location
        item_movement_stock_in.document_type = document_type
        item_movement_stock_in.document_pk = stock_transfer.id
        item_movement_stock_in.item = stock_transfer_detail.item
        item_movement_stock_in.stock_out = 0.0
        item_movement_stock_in.stock_in = stock_transfer_detail.quantity
        item_movement_stock_in.save()

    stock_transfer.status = status
    stock_transfer.save()
    

    return redirect(stock_transfer_list)

@login_required
def stock_transfer_detail(request, pk):
    stock_transfer = get_object_or_404(StockTransfer, pk=pk)
    form = DetailStockTransferForm(instance=stock_transfer)
    return render(request, 'stock/stock_transfer/detail.html', {'stock_transfer': stock_transfer, 'form': form})

@login_required
def stock_transfer_list(request):
    return render(request, 'stock/stock_transfer/list.html')

@login_required
def stock_transfer_update(request, pk):
    stock_transfer = get_object_or_404(StockTransfer, pk=pk)
    if request.method == 'POST':
        form = UpdateStockTransferForm(request.POST, instance=stock_transfer)
        status = stock_transfer.status
        stock_transfer = form.save()
        stock_transfer.revision = stock_transfer.revision + 1
        stock_transfer.status = status
        stock_transfer.save()
        return redirect('stock_transfer_detail', pk=stock_transfer.pk)
    else:
        form = UpdateStockTransferForm(instance=stock_transfer)
        form_attachment = NewStockTransferAttachmentForm()
        form_detail = NewStockTransferDetailForm()
    return render(request, 'stock/stock_transfer/update.html', {'stock_transfer': stock_transfer, 'form': form, 'form_detail':form_detail,'form_attachment':form_attachment})

@login_required
def stock_transfer_delete(request):
    stock_transfer =  get_object_or_404(StockTransfer, pk=request.POST['hiddenValue'])
    stock_transfer.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_transfer_detail_create(request, pk):    
    form = NewStockTransferDetailForm(request.POST)
    if form.is_valid():
        stock_transfer_detail = form.save(commit=False)
        stock_transfer = get_object_or_404(StockTransfer, pk=pk)

        
        item = form.cleaned_data['item']
        item_uom = item.item_uom

        stock_transfer_detail.stock_transfer = stock_transfer
        stock_transfer_detail.uom = item_uom
        stock_transfer_detail.item = item
        stock_transfer_detail.save()
        
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success'}) 

@login_required
def stock_transfer_detail_delete(request):
    stock_transfer_detail =  get_object_or_404(StockTransferDetail, pk=request.POST['hiddenValue'])
    stock_transfer_detail.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_transfer_attachment_create(request, pk):    
    form = NewStockTransferAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        stock_transfer_attachment = form.save(commit=False)
        stock_transfer = get_object_or_404(StockTransfer, pk=pk)
        stock_transfer_attachment.stock_transfer = stock_transfer
        stock_transfer_attachment.attachment_date = request.POST['attachment_date']
        stock_transfer_attachment.save()
        
    return JsonResponse({'message': 'Success'})

@login_required
def stock_transfer_attachment_delete(request, pk):
    stock_transfer_attachment = get_object_or_404(StockTransferAttachment, pk=request.POST['hiddenValue2'])
    stock_transfer_attachment.delete()
    return JsonResponse({'message': 'Success'})

#Stock Adjustment
@login_required
def stock_adjustment_init(request):    
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=document_type)[0]

    stock_adjustment = StockAdjustment.objects.create(submit_by=request.user, transaction_type=transaction_type)
    return redirect(stock_adjustment_create, stock_adjustment.pk)

@login_required
def stock_adjustment_create(request, pk):    
    stock_adjustment = get_object_or_404(StockAdjustment, pk=pk)
    if request.method == 'POST':
        form = NewStockAdjustmentForm(request.POST, instance=stock_adjustment)
        if form.is_valid():

            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]
            document_number = document_type.running_number + 1
            document_type.running_number = document_number 
            document_type.save()

            company = form.cleaned_data['company']
            transaction_type = form.cleaned_data['transaction_type']
            project = form.cleaned_data['project']
            location = form.cleaned_data['location']
            department = form.cleaned_data['department']

            status = get_object_or_404(StatusMaintenance, document_type=document_type, status_code="100")

            stock_adjustment.document_number = '{0}-{1:05d}'.format(document_type.document_type_code, document_number)
            stock_adjustment.company = company
            stock_adjustment.project = project
            stock_adjustment.location = location
            stock_adjustment.department = department
            stock_adjustment.status = status
            stock_adjustment.submit_by = request.user
            stock_adjustment.transaction_type = transaction_type
            stock_adjustment.save()

            # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=transaction_type.pk , document_type=staff_ot_type)

            return redirect(stock_adjustment_update, pk=stock_adjustment.pk)
        else:
            print(form.errors)
            form = NewStockAdjustmentForm(instance=stock_adjustment)
            form_detail = NewStockAdjustmentDetailForm()
            form_attachment = NewStockAdjustmentAttachmentForm()
    else:
        form = NewStockAdjustmentForm(instance=stock_adjustment)
        form_detail = NewStockAdjustmentDetailForm()
        form_attachment = NewStockAdjustmentAttachmentForm()
    return render(request, 'stock/stock_adjustment/create.html', {'stock_adjustment': stock_adjustment, 'form': form, 'form_detail': form_detail,'form_attachment':form_attachment})

@login_required
def stock_adjustment_submit(request, pk):
    stock_adjustment = get_object_or_404(StockAdjustment, pk=pk)
    stock_adjustment_details = StockAdjustmentDetail.objects.filter(stock_adjustment=stock_adjustment)
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="210")[0]
    status = StatusMaintenance.objects.filter(document_type=document_type,status_code='400')[0]

    for stock_adjustment_detail in stock_adjustment_details:
        item_movement= ItemMovement()     
        item_movement.location = stock_adjustment.location
        item_movement.document_type = document_type
        item_movement.document_pk = stock_adjustment.id
        item_movement.item = stock_adjustment_detail.item
        if stock_adjustment_detail.quantity < 0:
            item_movement.stock_out = abs(stock_adjustment_detail.quantity)
            item_movement.stock_in = 0.0
        else:
            item_movement.stock_out = 0.0
            item_movement.stock_in = stock_adjustment_detail.quantity
        item_movement.save()

    stock_adjustment.status = status
    stock_adjustment.save()
    return redirect(stock_adjustment_list)

@login_required
def stock_adjustment_detail(request, pk):
    stock_adjustment = get_object_or_404(StockAdjustment, pk=pk)
    form = DetailStockAdjustmentForm(instance=stock_adjustment)
    return render(request, 'stock/stock_adjustment/detail.html', {'stock_adjustment': stock_adjustment, 'form': form})

@login_required
def stock_adjustment_list(request):
    return render(request, 'stock/stock_adjustment/list.html')

@login_required
def stock_adjustment_update(request, pk):
    stock_adjustment = get_object_or_404(StockAdjustment, pk=pk)
    if request.method == 'POST':
        form = UpdateStockAdjustmentForm(request.POST, instance=stock_adjustment)
        status = stock_adjustment.status
        stock_adjustment = form.save()
        stock_adjustment.revision = stock_adjustment.revision + 1
        stock_adjustment.status = status
        stock_adjustment.save()
        return redirect('stock_adjustment_detail', pk=stock_adjustment.pk)
    else:
        form = UpdateStockAdjustmentForm(instance=stock_adjustment)
        form_attachment = NewStockAdjustmentAttachmentForm()
        form_detail = NewStockAdjustmentDetailForm()
    return render(request, 'stock/stock_adjustment/update.html', {'stock_adjustment': stock_adjustment, 'form': form, 'form_detail':form_detail,'form_attachment':form_attachment})

@login_required
def stock_adjustment_delete(request):
    stock_adjustment =  get_object_or_404(StockAdjustment, pk=request.POST['hiddenValue'])
    stock_adjustment.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_adjustment_detail_create(request, pk):    
    form = NewStockAdjustmentDetailForm(request.POST)
    if form.is_valid():
        stock_adjustment_detail = form.save(commit=False)
        stock_adjustment = get_object_or_404(StockAdjustment, pk=pk)

        item = form.cleaned_data['item']
        item_uom = item.item_uom

        stock_adjustment_detail.stock_adjustment = stock_adjustment
        stock_adjustment_detail.uom = item_uom
        stock_adjustment_detail.item = item
        stock_adjustment_detail.save()
        
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success'}) 

@login_required
def stock_adjustment_detail_delete(request):
    stock_adjustment_detail =  get_object_or_404(StockAdjustmentDetail, pk=request.POST['hiddenValue'])
    stock_adjustment_detail.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_adjustment_attachment_create(request, pk):    
    form = NewStockAdjustmentAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        stock_adjustment_attachment = form.save(commit=False)
        stock_adjustment = get_object_or_404(StockAdjustment, pk=pk)
        stock_adjustment_attachment.stock_adjustment = stock_adjustment
        stock_adjustment_attachment.attachment_date = request.POST['attachment_date']
        stock_adjustment_attachment.save()
        
    return JsonResponse({'message': 'Success'})

@login_required
def stock_adjustment_attachment_delete(request, pk):
    stock_adjustment_attachment = get_object_or_404(StockAdjustmentAttachment, pk=request.POST['hiddenValue2'])
    stock_adjustment_attachment.delete()
    return JsonResponse({'message': 'Success'})

#Stock Issuing
@login_required
def stock_issuing_init(request):    
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=document_type)[0]

    stock_issuing = StockIssuing.objects.create(submit_by=request.user, transaction_type=transaction_type)
    return redirect(stock_issuing_create, stock_issuing.pk)

@login_required
def stock_issuing_create(request, pk):    
    stock_issuing = get_object_or_404(StockIssuing, pk=pk)
    if request.method == 'POST':
        form = NewStockIssuingForm(request.POST, instance=stock_issuing)
        if form.is_valid():

            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]
            document_number = document_type.running_number + 1
            document_type.running_number = document_number 
            document_type.save()

            company = form.cleaned_data['company']
            transaction_type = form.cleaned_data['transaction_type']
            project = form.cleaned_data['project']
            location = form.cleaned_data['location']
            department = form.cleaned_data['department']
            delivery_to = form.cleaned_data['delivery_to']

            status = get_object_or_404(StatusMaintenance, document_type=document_type, status_code="100")

            stock_issuing.document_number = '{0}-{1:05d}'.format(document_type.document_type_code, document_number)
            stock_issuing.company = company
            stock_issuing.project = project
            stock_issuing.location = location
            stock_issuing.department = department
            stock_issuing.status = status
            stock_issuing.submit_by = request.user
            stock_issuing.transaction_type = transaction_type
            stock_issuing.save()

            # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=transaction_type.pk , document_type=staff_ot_type)

            return redirect(stock_issuing_update, pk=stock_issuing.pk)
        else:
            print(form.errors)
            form = NewStockIssuingForm(instance=stock_issuing)
            form_detail = NewStockIssuingDetailForm()
            form_attachment = NewStockIssuingAttachmentForm()
    else:
        form = NewStockIssuingForm(instance=stock_issuing)
        form_detail = NewStockIssuingDetailForm()
        form_attachment = NewStockIssuingAttachmentForm()
    return render(request, 'stock/stock_issuing/create.html', {'stock_issuing': stock_issuing, 'form': form, 'form_detail': form_detail,'form_attachment':form_attachment})

@login_required
def stock_issuing_submit(request, pk):
    stock_issuing = get_object_or_404(StockIssuing, pk=pk)
    stock_issuing_details = StockIssuingDetail.objects.filter(stock_issuing=stock_issuing)
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="212")[0]
    status = StatusMaintenance.objects.filter(document_type=document_type,status_code='400')[0]

    for stock_issuing_detail in stock_issuing_details:
        item_movement= ItemMovement()     
        item_movement.location = stock_issuing.location
        item_movement.document_type = document_type
        item_movement.document_pk = stock_issuing.id
        item_movement.item = stock_issuing_detail.item
        item_movement.stock_out = stock_issuing_detail.quantity
        item_movement.stock_in = 0.0
        
        item_movement.save()

    stock_issuing.status = status
    stock_issuing.save()

    return redirect(stock_issuing_list)

@login_required
def stock_issuing_detail(request, pk):
    stock_issuing = get_object_or_404(StockIssuing, pk=pk)
    form = DetailStockIssuingForm(instance=stock_issuing)
    return render(request, 'stock/stock_issuing/detail.html', {'stock_issuing': stock_issuing, 'form': form})

@login_required
def stock_issuing_list(request):
    return render(request, 'stock/stock_issuing/list.html')

@login_required
def stock_issuing_update(request, pk):
    stock_issuing = get_object_or_404(StockIssuing, pk=pk)
    if request.method == 'POST':
        form = UpdateStockIssuingForm(request.POST, instance=stock_issuing)
        status = stock_issuing.status
        stock_issuing = form.save()
        stock_issuing.revision = stock_issuing.revision + 1
        stock_issuing.status = status
        stock_issuing.save()

        return redirect('stock_issuing_detail', pk=stock_issuing.pk)
    else:
        form = UpdateStockIssuingForm(instance=stock_issuing)
        form_detail = NewStockIssuingDetailForm()
        form_attachment = NewStockIssuingAttachmentForm()
    return render(request, 'stock/stock_issuing/update.html', {'stock_issuing': stock_issuing, 'form': form, 'form_detail':form_detail,'form_attachment':form_attachment})

@login_required
def stock_issuing_delete(request):
    stock_issuing =  get_object_or_404(StockIssuing, pk=request.POST['hiddenValue'])
    stock_issuing.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_issuing_detail_create(request, pk):    
    form = NewStockIssuingDetailForm(request.POST)
    if form.is_valid():
        stock_issuing_detail = form.save(commit=False)
        stock_issuing = get_object_or_404(StockIssuing, pk=pk)

        item = form.cleaned_data['item']
        item_uom = item.item_uom

        stock_issuing_detail.stock_issuing = stock_issuing
        stock_issuing_detail.uom = item_uom
        stock_issuing_detail.item = item
        stock_issuing_detail.save()
        
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success'}) 

@login_required
def stock_issuing_detail_delete(request):
    stock_issuing_detail =  get_object_or_404(StockIssuingDetail, pk=request.POST['hiddenValue'])
    stock_issuing_detail.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_issuing_attachment_create(request, pk):    
    form = NewStockIssuingAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        stock_issuing_attachment = form.save(commit=False)
        stock_issuing = get_object_or_404(StockIssuing, pk=pk)
        stock_issuing_attachment.stock_issuing = stock_issuing
        stock_issuing_attachment.attachment_date = request.POST['attachment_date']
        stock_issuing_attachment.save()
        
    return JsonResponse({'message': 'Success'})

@login_required
def stock_issuing_attachment_delete(request, pk):
    stock_issuing_attachment = get_object_or_404(StockIssuingAttachment, pk=request.POST['hiddenValue2'])
    stock_issuing_attachment.delete()
    return JsonResponse({'message': 'Success'})


@login_required
def load_delivery_address(request):
    delivery = get_object_or_404(CompanyMaintenance, pk=request.GET.get('delivery_receiver'))
    address = CompanyAddressDetail.objects.filter(company=delivery)[0]
    return render(request, 'stock/stock_issuing/delivery_address_field.html', {'address': address})

#Stock Return
@login_required
def stock_return_init(request):    
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="214")[0]
    transaction_type = TransactiontypeMaintenance.objects.filter(document_type=document_type)[0]

    stock_return = StockReturn.objects.create(submit_by=request.user, transaction_type=transaction_type)
    return redirect(stock_return_create, stock_return.pk)

@login_required
def stock_return_create(request, pk):    
    stock_return = get_object_or_404(StockReturn, pk=pk)
    if request.method == 'POST':
        form = NewStockReturnForm(request.POST, instance=stock_return)
        if form.is_valid():

            document_type = DocumentTypeMaintenance.objects.filter(document_type_code="214")[0]
            document_number = document_type.running_number + 1
            document_type.running_number = document_number 
            document_type.save()

            company = form.cleaned_data['company']
            transaction_type = form.cleaned_data['transaction_type']
            vendor = form.cleaned_data['vendor']
            project = form.cleaned_data['project']
            location = form.cleaned_data['location']
            department = form.cleaned_data['department']

            status = get_object_or_404(StatusMaintenance, document_type=document_type, status_code="100")

            stock_return.document_number = '{0}-{1:05d}'.format(document_type.document_type_code, document_number)
            stock_return.company = company
            stock_return.project = project
            stock_return.location = location
            stock_return.department = department
            stock_return.status = status
            stock_return.submit_by = request.user
            stock_return.transaction_type = transaction_type
            stock_return.save()

            # transaction_type = get_object_or_404(TransactiontypeMaintenance, pk=transaction_type.pk , document_type=staff_ot_type)

            return redirect(stock_return_update, pk=stock_return.pk)
        else:
            print(form.errors)
            form = NewStockReturnForm(instance=stock_return)
            form_detail = NewStockReturnDetailForm()
            form_attachment = NewStockAdjustmentAttachmentForm()
    else:
        form = NewStockReturnForm(instance=stock_return)
        form_detail = NewStockReturnDetailForm()
        form_attachment = NewStockReturnAttachmentForm()
    return render(request, 'stock/stock_return/create.html', {'stock_return': stock_return, 'form': form, 'form_detail': form_detail,'form_attachment':form_attachment})

@login_required
def stock_return_submit(request, pk):
    stock_return = get_object_or_404(StockReturn, pk=pk)
    stock_return_details = StockReturnDetail.objects.filter(stock_return=stock_return)
    document_type = DocumentTypeMaintenance.objects.filter(document_type_code="214")[0]
    status = StatusMaintenance.objects.filter(document_type=document_type,status_code='400')[0]

    for stock_return_detail in stock_return_details:
        item_movement= ItemMovement()     
        item_movement.location = stock_return.location
        item_movement.document_type = document_type
        item_movement.document_pk = stock_return.id
        item_movement.item = stock_return_detail.item
        item_movement.stock_out = stock_return_detail.quantity
        item_movement.stock_in = 0.0
        item_movement.save()

    stock_return.status = status
    stock_return.save()
    return redirect(stock_return_list)

@login_required
def stock_return_detail(request, pk):
    stock_return = get_object_or_404(StockReturn, pk=pk)
    form = DetailStockReturnForm(instance=stock_return)
    return render(request, 'stock/stock_return/detail.html', {'stock_return': stock_return, 'form': form})

@login_required
def stock_return_list(request):
    return render(request, 'stock/stock_return/list.html')

@login_required
def stock_return_update(request, pk):
    stock_return = get_object_or_404(StockReturn, pk=pk)
    if request.method == 'POST':
        form = UpdateStockReturnForm(request.POST, instance=stock_return)
        status = stock_return.status
        stock_return = form.save()
        stock_return.revision = stock_return.revision + 1
        stock_return.status = status
        stock_return.save()
        return redirect('stock_return_detail', pk=stock_return.pk)
    else:
        form = UpdateStockReturnForm(instance=stock_return)
        form_attachment = NewStockReturnAttachmentForm()
        form_detail = NewStockReturnDetailForm()
    return render(request, 'stock/stock_return/update.html', {'stock_return': stock_return, 'form': form, 'form_detail':form_detail,'form_attachment':form_attachment})

@login_required
def stock_return_delete(request):
    stock_return =  get_object_or_404(StockReturn, pk=request.POST['hiddenValue'])
    stock_return.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_return_detail_create(request, pk):    
    form = NewStockReturnDetailForm(request.POST)
    if form.is_valid():
        stock_return_detail = form.save(commit=False)
        stock_return = get_object_or_404(StockReturn, pk=pk)

        item = form.cleaned_data['item']
        item_uom = item.item_uom

        stock_return_detail.stock_return = stock_return
        stock_return_detail.uom = item_uom
        stock_return_detail.item = item
        stock_return_detail.save()
        
    else:
        print(form.errors)
    return JsonResponse({'message': 'Success'}) 

@login_required
def stock_return_detail_delete(request):
    stock_return_detail =  get_object_or_404(StockReturnDetail, pk=request.POST['hiddenValue'])
    stock_return_detail.delete()
    return JsonResponse({'message': 'Success'})

@login_required
def stock_return_attachment_create(request, pk):    
    form = NewStockReturnAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        stock_return_attachment = form.save(commit=False)
        stock_return = get_object_or_404(StockReturn, pk=pk)
        stock_return_attachment.stock_return = stock_return
        stock_return_attachment.attachment_date = request.POST['attachment_date']
        stock_return_attachment.save()
        
    return JsonResponse({'message': 'Success'})

@login_required
def stock_return_attachment_delete(request, pk):
    stock_return_attachment = get_object_or_404(StockReturnAttachment, pk=request.POST['hiddenValue2'])
    stock_return_attachment.delete()
    return JsonResponse({'message': 'Success'})


@login_required
def stock_balance(request):
    if request.method == 'POST':
        hiddenvalue = request.POST['hiddenValue']
        print(hiddenvalue)
        if hiddenvalue == "item":
            form = StockBalanceReport(request.POST)
        else:
            form = StockBalanceReportLocation(request.POST)
        if hiddenvalue == "item":
            if form.is_valid():
                item = form.cleaned_data['item']
                location = form.cleaned_data['location']
                if item != None:
                    item_select = Item.objects.filter(pk=item.pk)
                    
                if location != None:
                    location_select = LocationMaintenance.objects.filter(pk=location.pk)
                else:
                    location_select = LocationMaintenance.objects.filter(is_active=True)
                date = request.POST['date']
                location_current_balance_list = []
                for itm in item_select:
                    for loc in location_select:
                        location_current_balance_list.append(count_stock_balance(itm.id,loc.id,date))


                params = {
                    'items': item_select,
                    'locations': location_select,
                    'location_current_balance':location_current_balance_list,
                    'date':date,
                }

                pdf = Render.render('stock/print.html',params)
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "StockBalanceReportAt%s.pdf" % (date) 
                    content = "attachment; filename=%s" %(filename)
                    response['Content-Disposition'] = content
                    return response
                else:
                    return response("errors")
        else:
            if form.is_valid():
                location = form.cleaned_data['location']
                date = request.POST['date']
                if location != None:
                    location_select = LocationMaintenance.objects.filter(pk=location.pk)
                else:
                    location_select = LocationMaintenance.objects.filter(is_active=True)
                    
                location_current_balance_list = []
                location_item = []
                for loc in location_select:
                    item_movements = ItemMovement.objects.filter(location=loc,submit_date__lte=date).values("item_id","location_id").annotate(total_stock_out=Sum("stock_out"),total_stock_in=Sum("stock_in"))
                    # print(item_movements.count())
                    for item_movement in item_movements:
                        total_stock_in = item_movement['total_stock_in']
                        total_stock_out = item_movement['total_stock_out']
                        item = Item.objects.get(pk=item_movement['item_id'])
                        location_current_balance = total_stock_in - total_stock_out
                        # print(item)
                        # print(location_current_balance)
                        location_current_balance_list.append(location_current_balance)
                        location_item.append(item)


                params = {
                    'locations': location_select,
                    'items':location_item,
                    'location_current_balance':location_current_balance_list,
                    'date':date,
                }

                pdf = Render.render('LocationStock/print.html',params)
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "StockBalanceReportByLocationAt%s.pdf" % (date) 
                    content = "attachment; filename=%s" %(filename)
                    response['Content-Disposition'] = content
                    return response
                else:
                    return response("errors")

            # return render(request, 'stock/print.html', {'items': item_select,'locations': location_select})
    else:
        form = StockBalanceReport()
        form2 = StockBalanceReportLocation()
    return render(request, 'stock/stock_balance_inquiry/selection.html', {'form': form,'form2':form2})


def count_stock_balance(itempk,locationpk,date):
    item = Item.objects.get(pk=itempk)
    location = LocationMaintenance.objects.get(pk=locationpk)
    item_movements = ItemMovement.objects.filter(item=item,location=location,submit_date__lte=date)

    if item_movements.count == 0:
        return 0
    else:
        total_balance = 0
        total_stock_out = 0
        total_stock_in = 0
        for item_movement in item_movements:
            total_stock_in = total_stock_in + item_movement.stock_in
            total_stock_out = total_stock_out + item_movement.stock_out
        
        total_balance = total_stock_in - total_stock_out
        return total_balance

@login_required
def stock_balance_location(request):
    if request.method == 'POST':
        form = StockBalanceReportLocation(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            date = request.POST['date']
            if location != None:
                location_select = LocationMaintenance.objects.filter(pk=location.pk)
            else:
                location_select = LocationMaintenance.objects.filter(is_active=True)
                
            location_current_balance_list = []
            location_item = []
            for loc in location_select:
                item_movements = ItemMovement.objects.filter(location=loc,submit_date__lte=date).values("item_id","location_id").annotate(total_stock_out=Sum("stock_out"),total_stock_in=Sum("stock_in"))
                # print(item_movements.count())
                for item_movement in item_movements:
                    total_stock_in = item_movement['total_stock_in']
                    total_stock_out = item_movement['total_stock_out']
                    item = Item.objects.get(pk=item_movement['item_id'])
                    location_current_balance = total_stock_in - total_stock_out
                    # print(item)
                    # print(location_current_balance)
                    location_current_balance_list.append(location_current_balance)
                    location_item.append(item)


            params = {
                'locations': location_select,
                'items':location_item,
                'location_current_balance':location_current_balance_list,
            }

            pdf = Render.render('LocationStock/print.html',params)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "StockBalanceReportByLocation.pdf" 
                content = "attachment; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response
            else:
                return response("errors")

            # return render(request, 'stock/print.html', {'items': item_select,'locations': location_select})
    else:
        form = StockBalanceReportLocation()
    return render(request, 'stock/stock_balance_inquiry/locationselection.html', {'form': form})

