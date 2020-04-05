from rest_framework import serializers
from .models import DrawerDisbursement
from administration.models import DrawerMaintenance
from payment.models import PaymentRequest

class DrawerDisbursementSerializer(serializers.ModelSerializer):
    disbursed_date = serializers.DateField(format='%d/%m/%Y')
    payment = serializers.StringRelatedField(many=False)

    class Meta:
        model = DrawerDisbursement
        fields = ['id','disbursed_by', 'status','total_disbursed','payment','disbursed_date']

class DrawerSelectionSerializer(serializers.ModelSerializer):
    branch = serializers.StringRelatedField(many=False)

    class Meta:
        model = DrawerMaintenance
        fields = ['id','drawer_name','branch','open_year','open_month','limit','drawer_status']

class ApprovedPaymentRequest(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)
    approval = serializers.StringRelatedField(many=False)
    submit_by = serializers.StringRelatedField(many=False)

    class Meta:
        model = PaymentRequest
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project','submit_by', 'approval','total_amount']