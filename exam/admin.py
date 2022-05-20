from django.contrib import admin
from django.contrib import admin
from . import models
from exam.models import Language,Dlevel,Tag
# Register your models here.


admin.site.register(Language)
admin.site.register(Dlevel)
admin.site.register(Tag)

@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'answer_text', 
        'is_right', 
        'question',
        'language'
        ]
class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = [
        'answer_text', 
        'is_right',
        'question',
        'language'
        ]

@admin.register(models.Question)

class QuestionAdmin(admin.ModelAdmin):
    fields = [
     'title',
     'difficulty',
     'language',
     'qtype',
     'solution',
     'description'
    ]
    list_display = [
        'title', 
        'difficulty',
        'language',
        'qtype',
        'solution',
        'description'
       
        ]
    inlines = [
        AnswerInlineModel, 
        ]
