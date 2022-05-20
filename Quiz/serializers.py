from rest_framework import serializers
from .models import Qtype,Dlevel,Language
class QtypeSerializer(serializers.ModelSerializer):
 class Meta:
  model = Qtype
  fields = ['qt_id', 'qt_title']

class DlevelSerializer(serializers.ModelSerializer):
 class Meta:
  model = Dlevel
  fields = ['dl_id', 'dl_title']

class LSerializer(serializers.ModelSerializer):
 class Meta:
  model = Language
  fields = ['lg_id', 'lg_title']  