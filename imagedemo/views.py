from django.shortcuts import render

# Create your views here.
from .models import Image
from .serializers import ImageSerializer
from rest_framework import viewsets

class ImageModelViewSet(viewsets.ModelViewSet):
  queryset = Image.objects.all()
  serializer_class = ImageSerializer
 