from django.shortcuts import render

# Create your views here.
from .models import demock
from .serializers import ckSerializer
from rest_framework import viewsets

class ckModelViewSet(viewsets.ModelViewSet):
  queryset = demock.objects.all()
  serializer_class = ckSerializer