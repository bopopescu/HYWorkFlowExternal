from django.shortcuts import get_object_or_404
from administration.models import DocumentTypeMaintenance, TransactiontypeMaintenance

def reimbursement_trans_type(request):
    document_type = get_object_or_404(DocumentTypeMaintenance, document_type_code="403")
    return {
        'reimbursement_trans_type': TransactiontypeMaintenance.objects.filter(document_type=document_type,is_active=True).order_by('transaction_type_name')
    }