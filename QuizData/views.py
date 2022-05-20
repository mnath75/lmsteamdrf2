from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from course.models import Topic
from .models import Language, Question,Ques,Testmake,TestLayout,TestSection
#from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status
from datetime import datetime
from .serializers import QuestionSerializer,QuesSerializer,DlevelSerializer,LanguageSerializer,TestmakeSerializer,TestLayoutSerializer,TestSectionSerializer
from rest_framework import viewsets
from django_filters import rest_framework as filters

class questionModelViewSet(viewsets.ModelViewSet):
  queryset = Question.objects.all()
  serializer_class = QuestionSerializer

class quesModelViewSet(viewsets.ModelViewSet):
  queryset = Ques.objects.all()
  serializer_class = QuesSerializer

class testMakeModelViewSet(viewsets.ModelViewSet):
  queryset = Testmake.objects.all()
  serializer_class = TestmakeSerializer  

class testLayoutModelViewSet(viewsets.ModelViewSet):
  queryset = TestLayout.objects.all()
  serializer_class = TestLayoutSerializer    


class TestSectionModelViewSet(viewsets.ModelViewSet):
    queryset=TestSection.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['testmake']
    serializer_class = TestSectionSerializer