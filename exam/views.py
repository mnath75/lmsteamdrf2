from django.shortcuts import render
from .models import  Question,Answer
from .serializers import QuestionSerializer,AnswerSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
# Create your views here.
from rest_framework.response import Response
from django_filters import rest_framework as filters

class ViewsetQuestion(viewsets.ModelViewSet):
  queryset =Question.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_fields = ['qtype']
  serializer_class = QuestionSerializer 

class ViewsetAnswer(viewsets.ModelViewSet):
  queryset =Answer.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_fields = ['qtype']
  serializer_class = AnswerSerializer 



   