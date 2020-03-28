from rest_framework import serializers
from .models import Memo, MemoAttachment

class MemoSerializer(serializers.ModelSerializer):
    submit_date = serializers.DateField(format='%d/%m/%Y')
    company = serializers.StringRelatedField(many=False)
    project = serializers.StringRelatedField(many=False)

    class Meta:
        model = Memo
        fields = ['id', 'revision', 'document_number', 'subject', 'submit_date', 'company', 'project']

class MemoAttachmentSerializer(serializers.ModelSerializer):
    attachment_date = serializers.DateField(format='%d/%m/%Y')
    attachment = serializers.FileField()
    class Meta:
        model = MemoAttachment
        fields = ['id', 'memo', 'attachment', 'attachment_date']