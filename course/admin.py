from django.contrib import admin

from .models import CourseCategory,Course,Subject,Topic

# Register your models here.

admin.site.register(CourseCategory)

admin.site.register(Course)

admin.site.register(Subject)

admin.site.register(Topic)