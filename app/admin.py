from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Batch)
admin.site.register(Faculty)
admin.site.register(FacultyNotifications)
admin.site.register(Student)
admin.site.register(StudentNotifications)
admin.site.register(User, UserAdmin)
