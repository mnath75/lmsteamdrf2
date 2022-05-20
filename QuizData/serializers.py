from rest_framework import serializers
from.models import Question,Ques,Choice,TestLayout,Testmake,TestSection
from account.models import User
from course.models import Topic
from Quiz.models import Qtype,Dlevel,Language

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class QtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qtype
        fields = '__all__'
class DlevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dlevel
        fields = [' dl_id ','dl_title']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['lg_id','lg_title']


class QuestionSerializer(serializers.ModelSerializer):
    #qtype=StringSerializer(many=True)
    #difficulty=StringSerializer(many=True)
    #language=StringSerializer(many=True)
    #user=StringSerializer(many=True)
    #topic=StringSerializer(many=True)
    #qtype=QtypeSerializer(many=True,read_only=True)
    #difficulty=DlevelSerializer(many=True,read_only=True)
    #language=TopicSerializer(many=True,read_only=True)
    #user=UserSerializer(many=True,read_only=True)
    #topic=TopicSerializer(many=True,read_only=True)dl_title


    class Meta:
        model = Question
        fields = ['qu_id','qtype','difficulty','language','user','topic']
        

  
        
class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choice
        fields = [
          'id',
          'question',
          'language',
          'answer_text',
          'is_right'
        ]
        read_only_fields = ('question',)
        

class QuesSerializer(serializers.ModelSerializer):
    lastQid = serializers.SerializerMethodField()

    def get_lastQid(self,obj):
        return Question.objects.all().last().qu_id

   
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Ques
        fields = [
            "qd_id",'lastQid',"qid",'question_para','question_text','ques_lang','description','solution','is_active',
            "choices",
        
        ]
      
    def create(self,validate_data):
        
        
        choices=validate_data.pop('choices')
        question=Ques.objects.create(**validate_data)
        for choice in choices:
            choice.question=question
            Choice.objects.create(**choice,question=question)
        return question    

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices')
        instance.question_para = validated_data.get("question_para", instance.question_para)
        instance.question_text = validated_data.get("question_text", instance.question_text)
        instance.save()
        keep_choices = []
        for choice in choices:
            if "id" in choice.keys():
                if Choice.objects.filter(id=choice["id"]).exists():
                    c = Choice.objects.get(id=choice["id"])
                    c.answer_text = choice.get('answer_text', c.answer_text)
                    c.save()
                    keep_choices.append(c.id)
                else:
                    continue
            else:
                c = Choice.objects.create(**choice, question=instance)
                keep_choices.append(c.id)

        for choice in instance.choices:
            if choice.id not in keep_choices:
                choice.delete()

        return instance   

class TestLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestLayout
        fields = '__all__'
    
class TestmakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testmake
        fields = ['te_id','user','testName','tags','totalMarks','noOfQuestions','hour',
        'minute','testCategory','testLayout','poolQuestion','freeAvailable','testShowFrom','testEndON']      

class TestSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSection
        fields ='__all__'        
