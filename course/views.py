
# Create your views here.
from django.shortcuts import render
from .serializers import CategorySerializer,CourseSerializer,SubjectSerializer,TopicSerializer
from rest_framework import viewsets
from .models import CourseCategory,Course,Subject,Topic
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import status,permissions
from knox.auth import TokenAuthentication

class CategoryModelViewSet(viewsets.ModelViewSet):
  queryset = CourseCategory.objects.all()
  serializer_class = CategorySerializer



class CourseModelViewSet(viewsets.ModelViewSet):
  #authentication_classes = (TokenAuthentication,)
  #permission_classes = [permissions.IsAuthenticated, ]
  queryset = Course.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_fields = ['cr_categ']
  serializer_class = CourseSerializer  

  

class SubjectModelViewSet(viewsets.ModelViewSet):
  queryset = Subject.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_fields = ['sub_course']
  serializer_class = SubjectSerializer 

class TopicModelViewSet(viewsets.ModelViewSet):
  queryset = Topic.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_fields = ['top_subject']
  serializer_class = TopicSerializer
 