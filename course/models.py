from django.db import models

# Create your models here.
class CourseCategory(models.Model):
    category_id=models.AutoField(primary_key=True,db_column='category_id')
    category_title=models.CharField('Title',max_length=255)
    category_slug=models.SlugField('slug',max_length=255,null=True)
    category_short=models.TextField('short description',blank=True,null=True)
    category_createddate=models.DateTimeField('created',auto_now_add=True)
    class meta:
        verbose_name_plural='Categories'
    def __str__(self):
        return self.category_title

class Course(models.Model):
    cr_id = models.AutoField(primary_key=True, db_column='cr_id')
    cr_categ = models.ManyToManyField(CourseCategory,
                            verbose_name='Category',
                            db_column = 'cr_categ',
                            related_name='courses',
                            
                            )
    cr_title = models.CharField('Title', max_length=255)
    cr_slug = models.SlugField('Slug', max_length=255)
    cr_short = models.TextField('Short description', blank=True, null=True)
    cr_long = models.TextField('Long description', blank=True, null=True)
    cr_created_at = models.DateTimeField('Created at', auto_now_add=True)
    def __str__(self):
        return self.cr_title


class Subject(models.Model):
    sub_id = models.AutoField(primary_key=True, db_column='sub_id')
    sub_course = models.ManyToManyField(Course,
                            verbose_name='Subject',
                            db_column = 'sub_course',
                            related_name='subject')
    sub_title = models.CharField('Title', max_length=255)
    sub_slug = models.SlugField('Slug', max_length=255)
    sub_short = models.TextField('Short description', blank=True, null=True)
    sub_long = models.TextField('Long description', blank=True, null=True)
    sub_created_at = models.DateTimeField('Created at', auto_now_add=True)
    def __str__(self):
        return self.sub_title
class Topic(models.Model):
    top_id = models.AutoField(primary_key=True, db_column='top_id')
    top_subject = models.ManyToManyField(Subject,
                            verbose_name='Topic',
                            db_column = 'top_subject',
                            related_name='topics')
    top_title = models.CharField('Title', max_length=255)
    top_slug = models.SlugField('Slug', max_length=255,blank=True,null=True)
    top_short = models.TextField('Short description', blank=True, null=True)
    top_long = models.TextField('Long description', blank=True, null=True)
    top_created_at = models.DateTimeField('Created at', auto_now_add=True)
    def __str__(self):
        return self.top_title        