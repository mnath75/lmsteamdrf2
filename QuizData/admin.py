from django.contrib import admin

from . import models
from .models import Language,Dlevel,Question,Ques,Choice,TestLayout,Testmake,TestSection
# Register your models here.
admin.site.register(Ques)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Language)
admin.site.register(Dlevel)

admin.site.register(TestLayout)
admin.site.register(Testmake)
admin.site.register(TestSection)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = [
        'answer_text', 
        'is_right', 
        'question',
        'language'
        ]
class ChoiceInlineModel(admin.TabularInline):
    model = models.Choice
    fields = [
        'answer_text', 
        'is_right',        
        'language'
        ]



class QuesAdmin(admin.ModelAdmin):
    fields = [
     'qid',
     'question_para',
     'question_text',
     'ques_lang',
     'description',
     'solution',
     'is_active'
    ]
    list_display = [
     'qid',
     'question_para',
     'question_text',
     'ques_lang',
     'description',
     'solution',
     'is_active'
       
        ]
    inlines = [ChoiceInlineModel]  
