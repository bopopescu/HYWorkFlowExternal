from rest_framework import serializers
from .models import DrawerDisbursement
from django.utils.formats import number_format
from administration.models import DrawerMaintenance
from payment.models import PaymentRequest

class DrawerDisbursementSerializer(serializers.ModelSerializer):
    disbursed_date = serializers.DateField(format='%d/%m/%Y')
    payment = serializers.StringRelatedField(many=False)
    payment_id = serializers.SerializerMethodField()
    total_disbursed = serializers.SerializerMethodField()

    class Meta:
        model = DrawerDisbursement
        fields = ['id','disbursed_by', 'status','total_disbursed','payment','disbursed_date','payment_id']

    def get_payment_id(self, obj):  
        return obj.payment.id

    def get_total_disbursed(self,obj):
        return number_format(obj.total_disbursed)

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
    submit_by = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = PaymentRequest
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project','submit_by', 'approval','total_amount']

    def get_total_amount(self,obj):
        return number_format(obj.total_amount)
    
    def get_submit_by(self,obj):
        return obj.submit_by.first_name + " " + obj.submit_by.last_name