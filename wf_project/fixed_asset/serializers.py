from rest_framework import serializers
from .models import AssetMaster

class AssetMasterSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(many=False)

    class Meta:
        model = AssetMaster
        fields = ['id', 'company', 'description']