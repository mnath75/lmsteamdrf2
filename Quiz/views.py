from django.shortcuts import render

# Create your views here.
from .models import Qtype,Dlevel,Language
from .serializers import QtypeSerializer,DlevelSerializer,LSerializer
from rest_framework import viewsets
import django_filters
from django_filters import rest_framework as filters
class QtypeModelViewSet(viewsets.ModelViewSet):
  queryset = Qtype.objects.all()
  serializer_class = QtypeSerializer
class DlevelModelViewSet(viewsets.ModelViewSet):
  queryset = Dlevel.objects.all()
  serializer_class = DlevelSerializer
class LanguageModelViewSet(viewsets.ModelViewSet):
  queryset = Language.objects.all()
  serializer_class = LSerializer    