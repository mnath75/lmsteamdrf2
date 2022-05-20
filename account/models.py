from __future__ import unicode_literals
from tabnanny import verbose
#from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save

from django.dispatch import receiver

from django.db.models.signals import post_save
import random
import os
from rest_framework.authtoken.models import Token
import requests
#from django.contrib.auth.models import User








class UserManager(BaseUserManager):
    parent      = models.BooleanField(default=False)
    def create_user(self, phone, password=None,name=None,is_staff=False, is_active=True, is_parent=False ,is_educator=False ,is_branch=False,is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone=phone,
            name=name
        )
       
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.parent = is_parent
        user_obj.branch = is_branch
        user_obj.educator = is_educator
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,


        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user  

class User(AbstractBaseUser):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name        = models.CharField(max_length = 20, blank = True, null = True)
   
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    parent      = models.BooleanField(default=False)
    educator    = models.BooleanField(default=False)
    branch      = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_parent(self):
        return self.parent
    @property
    def is_branch(self):
        return self.branch
    @property
    def is_educator(self):
        return self.educator

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

        
class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)

    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


##### profile model

def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )
         

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


 

class Profile(models.Model):
    user            =   models.OneToOneField(User, on_delete= models.CASCADE)
    email           =   models.EmailField( blank = True, null = True)
    image           =   models.ImageField(upload_to = upload_image_path_profile, default=None,null=True, blank = True)
    pin             =   models.IntegerField(max_length=6,default=0)
    city            =   models.CharField(max_length = 30, blank = True, null = True)
    state           =   models.CharField(max_length = 30, blank = True, null = True)
    country         =   models.CharField(max_length = 30, blank = True, null = True)
    address         =   models.CharField(max_length = 900, blank = True, null = True)
    gender          =   models.CharField(max_length = 900, blank = True, null = True)
    qualification   =   models.CharField(max_length = 900, blank = True, null = True)
    dob             =   models.DateField(max_length=8, blank = True, null = True)
    def __str__(self):
        return str(self.user.name) 


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user = instance)
post_save.connect(user_created_receiver, sender = User)

