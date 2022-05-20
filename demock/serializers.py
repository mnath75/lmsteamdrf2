

from rest_framework import serializers
from demock.models import demock





class ckSerializer(serializers.ModelSerializer):
    class Meta:
        model = demock
        fields = ['ck_text']