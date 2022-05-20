from django.db import models

# Create your models here.
class Image(models.Model):
   
    image_text = models.ImageField(upload_to = "images/",default="null")
    
    

    
   
  