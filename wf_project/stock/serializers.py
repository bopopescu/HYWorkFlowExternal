from rest_framework import serializers
from .models import StockTransfer,StockTransferDetail,StockTransferAttachment
from .models import StockAdjustment,StockAdjustmentDetail,StockAdjustmentAttachment
from .models import StockIssuing,StockIssuingDetail,StockIssuingAttachment
from .models import StockReturn,StockReturnDetail,StockReturnAttachment
from administration.models import StatusMaintenance

#stock transfer
class StockTransferSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    from_location = serializers.StringRelatedField(many=False)
    to_location = serializers.StringRelatedField(many=False)
    transaction_type = serializers.StringRelatedField(many=False)
    document_status = serializers.SerializerMethodField()
    submit_by = serializers.StringRelatedField(many=False)

    def get_document_status(self, obj):    
        if obj.document_number != None:
            if obj.status.status_code == 100:
                return "Draft"
            elif obj.status.status_code == 400:
                return "Submitted"
            else:
                return "Draft(New)"
        else:
            return "Draft(New)"

    class Meta:
        model = StockTransfer
        fields = ['id','company','from_location','to_location','project','transaction_type','revision',
        'document_number','status','submit_date','submit_by','attention','document_status','reference','remarks']


class StockTransferDetailSerializer(serializers.ModelSerializer):
    uom = serializers.StringRelatedField(many=False)
    item = serializers.StringRelatedField(many=False)

    class Meta:
        model = StockTransferDetail
        fields = ['id','stock_transfer','item','quantity','uom','additional_description','reason','remarks']

class StockTransferAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()

    class Meta:
        model = StockTransferAttachment
        fields = ['id', 'stock_transfer', 'attachment', 'attachment_date']

#stock adjustment
class StockAdjustmentSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    location = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)
    transaction_type = serializers.StringRelatedField(many=False)
    document_status = serializers.SerializerMethodField()
    submit_by = serializers.StringRelatedField(many=False)

    def get_document_status(self, obj):    
        if obj.document_number != None:
            if obj.status.status_code == 100:
                return "Draft"
            elif obj.status.status_code == 400:
                return "Submitted"
            else:
                return "Draft(New)"
        else:
            return "Draft(New)"

    class Meta:
        model = StockAdjustment
        fields = ['id','company','department','location','project','transaction_type','revision',
        'document_number','status','submit_date','submit_by','attention','reference','document_status','remarks']

class StockAdjustmentDetailSerializer(serializers.ModelSerializer):
    uom = serializers.StringRelatedField(many=False)
    item = serializers.StringRelatedField(many=False)

    class Meta:
        model = StockAdjustmentDetail
        fields = ['id','stock_adjustment','item','quantity','uom','additional_description','reason','remarks']

class StockAdjustmentAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()

    class Meta:
        model = StockAdjustmentAttachment
        fields = ['id', 'stock_adjustment', 'attachment', 'attachment_date']

#stock issuing
class StockIssuingSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)
    location = serializers.StringRelatedField(many=False)
    transaction_type = serializers.StringRelatedField(many=False)
    document_status = serializers.SerializerMethodField()
    submit_by = serializers.StringRelatedField(many=False)

    def get_document_status(self, obj):    
        if obj.document_number != None:
            if obj.status.status_code == 100:
                return "Draft"
            elif obj.status.status_code == 400:
                return "Submitted"
            else:
                return "Draft(New)"
        else:
            return "Draft(New)"

    class Meta:
        model = StockIssuing
        fields = ['id','company','department','location','project','transaction_type','revision',
        'document_number','status','submit_date','attention','submit_by','reference','remarks','document_status']

class StockIssuingDetailSerializer(serializers.ModelSerializer):
    uom = serializers.StringRelatedField(many=False)
    item = serializers.StringRelatedField(many=False)

    class Meta:
        model = StockIssuingDetail
        fields = ['id','stock_issuing','item','quantity','uom','additional_description','reason','remarks']

class StockIssuingAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()

    class Meta:
        model = StockIssuingAttachment
        fields = ['id', 'stock_issuing', 'attachment', 'attachment_date']

#stock return
class StockReturnSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    location = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)
    transaction_type = serializers.StringRelatedField(many=False)
    document_status = serializers.SerializerMethodField()
    submit_by = serializers.StringRelatedField(many=False)

    def get_document_status(self, obj):    
        if obj.document_number != None:
            if obj.status.status_code == 100:
                return "Draft"
            elif obj.status.status_code == 400:
                return "Submitted"
            else:
                return "Draft(New)"
        else:
            return "Draft(New)"

    class Meta:
        model = StockReturn
        fields = ['id','company','department','location','project','transaction_type','revision',
        'document_number','status','submit_date','submit_by','attention','reference','document_status','remarks']

class StockReturnDetailSerializer(serializers.ModelSerializer):
    uom = serializers.StringRelatedField(many=False)
    item = serializers.StringRelatedField(many=False)

    class Meta:
        model = StockReturnDetail
        fields = ['id','stock_return','item','quantity','uom','additional_description','reason','remarks']

class StockReturnAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()

    class Meta:
        model = StockReturnAttachment
        fields = ['id', 'stock_return', 'attachment', 'attachment_date']