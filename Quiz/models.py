from django.db import models

# Create your models here.


# Create your models here.
class Qtype(models.Model):
    qt_id = models.AutoField(primary_key=True, db_column='qt_id')

    qt_title = models.CharField('Title', max_length=255)  
    def __str__(self):
        return self.qt_title

class Dlevel(models.Model):
    dl_id = models.AutoField(primary_key=True, db_column='dl_id')

    dl_title = models.CharField('Title', max_length=255) 
    def __str__(self):
        return self.dl_title
        
class Language(models.Model):
    lg_id = models.AutoField(primary_key=True, db_column='lg_id')

    lg_title = models.CharField('Title', max_length=255) 

    def __str__(self):
        return self.lg_id        