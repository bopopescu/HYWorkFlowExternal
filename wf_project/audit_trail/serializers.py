from rest_framework import serializers
from drawer_disbursement.models import DrawerDisbursement
from administration.models import DrawerMaintenance
from administration.models import DocumentTypeMaintenance,StatusMaintenance
from drawer_reimbursement.models import DrawerReimbursement

class DrawerSelectionSerializer(serializers.ModelSerializer):
    branch = serializers.StringRelatedField(many=False)

    class Meta:
        model = DrawerMaintenance
        fields = ['id','drawer_name','branch','open_year','open_month','limit','drawer_status']

class DrawerDisbursementSerializer(serializers.ModelSerializer):
    disbursed_date = serializers.DateField(format='%d/%m/%Y')
    payment = serializers.StringRelatedField(many=False)
    submit_by = serializers.SerializerMethodField()

    class Meta:
        model = DrawerDisbursement
        fields = ['id','disbursed_by','status','total_disbursed','payment','disbursed_date','submit_by']

    def get_submit_by(self, obj): 
        return obj.payment.submit_by.first_name

class DrawerReimbursedSerializer(serializers.ModelSerializer):
    reimbursed_date = serializers.DateField(format='%d/%m/%Y')
    reimbursement_request = serializers.StringRelatedField(many=False)
    submit_by = serializers.SerializerMethodField()

    class Meta:
        model = DrawerReimbursement
        fields = ['id','reimbursed_by','status','total_reimburse','reimbursement_request','reimbursed_date','submit_by']

    def get_submit_by(self, obj): 
        return obj.reimbursement_request.submit_by.first_name
