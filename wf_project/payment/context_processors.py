from django.shortcuts import get_object_or_404
from administration.models import DocumentTypeMaintenance, TransactiontypeMaintenance

def py_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="301")
    return {
        'py_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type,is_active=True).order_by('transaction_type_name')
    }