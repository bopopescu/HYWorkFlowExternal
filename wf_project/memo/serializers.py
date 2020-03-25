from rest_framework import serializers
from .models import Memo

class MemoSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)

    class Meta:
        model = Memo
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project']