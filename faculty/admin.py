from django.contrib import admin
from .models import Holiday, Department, Teacher, Subject


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description')
    search_fields = ('name',)
    list_filter = ('date',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'gender', 'joining_date', 'qualification')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('department', 'gender')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'teacher')
    list_filter = ('department',)
    search_fields = ('name',)
