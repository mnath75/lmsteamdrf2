from . models import Answer, Language,Question
from rest_framework import serializers

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Answer
        fields = [
            'id',
            'answer_text', 
            'is_right', 
            'question',
            'language'
        ]
class QuestionSerializer(serializers.ModelSerializer):

    answer_set = AnswerSerializer(many=True,read_only=True)
    
    class Meta:
    
        model = Question
        fields = [
        'id',
        'title', 
        'difficulty',
        'qtype',
        'solution',
        'description',
        'language',
        'answer_set'
        ]        
        depth=1



