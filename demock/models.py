from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class demock(models.Model):
   
    ck_text = RichTextField(blank=True, null=True,default=None)