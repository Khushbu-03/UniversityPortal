from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order
# Register your models here.
admin.site.register(Topic)
#admin.site.register(Course)
#admin.site.register(Student)
admin.site.register(Order)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'price', 'hours', 'for_everyone')
    actions = ['add_50_to_hours']

    def add_50_to_hours(self, request, queryset):
        for hour in queryset.all():
            queryset.update(hours=(int(hour.hours) + 10))

def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()


upper_case_name.short_description = 'Student Full Name'


class StudentAdmin(admin.ModelAdmin):
    list_display = (upper_case_name, 'city')

admin.site.register(Course,CourseAdmin)
admin.site.register(Student,StudentAdmin)