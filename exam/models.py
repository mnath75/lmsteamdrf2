from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.\
from Quiz.models import Qtype
from account.models import User

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
    lg_id = models.AutoField(primary_key=True, db_column='qt_id')

    lg_title = models.CharField('Title', max_length=255) 

    def __str__(self):
        return self.lg_title

class Tag(ObjectTracking):
    tag_id = models.AutoField(primary_key=True, db_column='qt_id')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [] 

class Question(ObjectTracking):

    class Meta:
        verbose_name = ("Question")
        verbose_name_plural = ("Questions")
        ordering = ['id']
    qtype = models.ForeignKey(
        Qtype, related_name='qtype', on_delete=models.DO_NOTHING)

    difficulty = models.ForeignKey(
        Dlevel, related_name='dlavel_qproto', on_delete=models.DO_NOTHING)

    language = models.ForeignKey(
        Language, related_name='language_qproto', on_delete=models.DO_NOTHING)


    title = models.CharField(max_length=255, verbose_name =("Title"))

    description = models.TextField('description', blank=True, null=True)
    solution = models.TextField('solution', blank=True, null=True)
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active Status"))

    @property
    def answers(self):
        return answer_set.all()    

    def __str__(self):
        return self.title  
         

class Answer(ObjectTracking):
    class Meta:
        verbose_name =("Answer")
        verbose_name_plural =("Answers")
        ordering = ['id']

    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    language = models.ForeignKey(
     Language, related_name='language_answer', on_delete=models.DO_NOTHING)
    answer_text = models.CharField(
    max_length=255, verbose_name=_("Answer Text"))
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text



