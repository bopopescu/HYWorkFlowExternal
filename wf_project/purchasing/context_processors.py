from django.shortcuts import get_object_or_404
from administration.models import DocumentTypeMaintenance, TransactiontypeMaintenance

def po_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="205")
    return {
        'po_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type)
    }