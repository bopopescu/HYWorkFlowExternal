from rest_framework import serializers
from .models import Memo

class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ['revision', 'document_number', 'status','subject']