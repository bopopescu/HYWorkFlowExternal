from django.shortcuts import get_object_or_404
from administration.models import DocumentTypeMaintenance, TransactiontypeMaintenance

def po_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="205")
    return {
        'po_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type).order_by('transaction_type_name')
    }

def grn_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="206")
    return {
        'grn_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type).order_by('transaction_type_name')
    }

def pi_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="208")
    return {
        'pi_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type).order_by('transaction_type_name')
    }

def pcn_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="209")
    return {
        'pcn_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type).order_by('transaction_type_name')
    }

def pdn_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="213")
    return {
        'pdn_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type).order_by('transaction_type_name')
    }