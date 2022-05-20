

from rest_framework import serializers
from imagedemo.models import Image





class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_text']