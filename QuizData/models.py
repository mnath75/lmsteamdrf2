from django.db import models


# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.\
from Quiz.models import Qtype
from account.models import User
from course.models import Topic
from ckeditor.fields import RichTextField



class Dlevel(models.Model):
    dl_id = models.AutoField(primary_key=True, db_column='dl_id')

    dl_title = models.CharField('Title', max_length=255) 
    def __str__(self):
        return self.dl_title

class ObjectTracking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

class Language(models.Model):
    lg_id = models.AutoField(primary_key=True, db_column='lg_id')

    lg_title = models.CharField('Title', max_length=255) 

    def __str__(self):
        return self.lg_title



class Question(ObjectTracking):

    class Meta:
        verbose_name = ("Question")
        verbose_name_plural = ("Questions")
        ordering = ['qu_id']
    qu_id = models.AutoField(primary_key=True, db_column='qu_id')
    qtype = models.ForeignKey(
        Qtype, related_name='qtype_question3',  on_delete=models.SET_NULL,null=True,default=None )

    difficulty = models.ForeignKey(
        Dlevel, related_name='dlavel_question3',  on_delete=models.SET_NULL,null=True,default=None )

    language = models.ForeignKey(
        Language, related_name='language_question3', on_delete=models.SET_NULL,null=True,default=None )

    reference = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,default=None , related_name='ques_user1',db_column='user')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True,default=None ,related_name='topic_question3')
    def __str__(self):
        return str(self.qu_id)


class Ques(ObjectTracking):
   
    qd_id = models.AutoField(primary_key=True, db_column='qd_id',default=None)
    qid = models.ForeignKey(Question, related_name='ques_qdes3', on_delete=models.SET_NULL,default=None,null=True)
    question_para = RichTextField(blank=True, null=True,default=None)
    question_text = RichTextField(blank=True, null=True,default=None)
    
    ques_lang = models.ForeignKey(Language, related_name='language_qdes3', on_delete=models.SET_NULL,default=None ,null=True)
    description = models.TextField('description', blank=True, null=True,default=None)
    solution = RichTextField('solution', blank=True, null=True,default=None)
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active Status"))
    
    def __str__(self):
        return self.question_text

    @property
    def choices(self):
        return self.choice_set.all()
class Choice(models.Model):
    question = models.ForeignKey(Ques, related_name='choices', on_delete=models.SET_NULL,default=None , null=True)
    language = models.ForeignKey(Language, related_name='choice_answer3',  on_delete=models.SET_NULL,default=None,null=True)
    answer_text = models.CharField( max_length=255, verbose_name=_("Answer Text"),default=None)
    is_right = models.BooleanField(default=False)
    def __str__(self):
        return self.answer_text


class TestLayout(models.Model):
    tl_id = models.AutoField(primary_key=True, db_column='tl_id')

    tl_title = models.CharField('Title', max_length=255) 
    def __str__(self):
        return self.tl_title  
TYPE_CHOICES = (
    ("Practice", "Practice"),
    ("Examination", "Examination")
)


class Testmake(ObjectTracking):
      te_id = models.AutoField(primary_key=True, db_column='te_id')
      user = models.ForeignKey(User, models.DO_NOTHING, related_name='test_user1',db_column='user')
      testName = models.CharField( max_length=255) 
      tags=models.CharField(max_length=255)
      noOfQuestions=models.PositiveIntegerField()
      totalMarks=models.PositiveIntegerField(null=True)
      hour=models.PositiveIntegerField() 
      minute=models.PositiveIntegerField() 
      testCategory= models.CharField(choices=TYPE_CHOICES , max_length = 20,default='1') 
      testLayout=models.ForeignKey(TestLayout, models.DO_NOTHING, related_name='test_TestLayout',db_column='test_layout')
      poolQuestion=models.BooleanField(default=False)
      freeAvailable=models.BooleanField(default=False)
      testShowFrom=models.DateTimeField('%d/%m/%y %H:%M')
      testEndON=models.DateTimeField(blank=True, null=True)
      def __str__(self):
        return self.testName

class TestSection(models.Model):
    ts_id=models.AutoField(primary_key=True, db_column='te_id')
    testmake=models.ForeignKey(Testmake, models.DO_NOTHING, related_name='testSeection_testMake',db_column='testmake')
    sectionName=models.CharField( max_length=255) 
    hour=models.PositiveIntegerField(default=False)
    minute=models.PositiveIntegerField(default=False) 
    allowedSectionSwitching=models.BooleanField(default=False)
    skipSectionBeforeTimeOver=models.BooleanField(default=False)
    studentChoice=models.BooleanField(default=False)
    useSectionAsBreak=models.BooleanField(default=False)
    showPreviousSection=models.BooleanField(default=False)
    sectionInstruction=models.TextField( blank=True, null=True,default=None)
    def __str__(self):
        return self.sectionName             

