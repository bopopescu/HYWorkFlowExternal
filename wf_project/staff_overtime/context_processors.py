from django.shortcuts import get_object_or_404
from administration.models import DocumentTypeMaintenance, TransactiontypeMaintenance

def staff_ot_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="504")
    return {
        'staff_ot_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type).order_by('transaction_type_name')
    }