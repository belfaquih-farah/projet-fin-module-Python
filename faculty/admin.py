from django.contrib import admin
from .models import Classe, Department, Teacher, Subject, Holiday, Event, TimeTable, Exam, ExamResult


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name', 'level')


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description')
    search_fields = ('name',)
    list_filter = ('date',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department', 'description')
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'gender', 'joining_date', 'qualification')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('department', 'gender')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'classe', 'teacher')
    list_filter = ('department', 'classe')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date',)


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'day', 'start_time', 'end_time', 'room')
    list_filter = ('day', 'subject__department')
    search_fields = ('subject__name', 'teacher__user__first_name', 'teacher__user__last_name', 'room')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'duration', 'room')
    list_filter = ('subject', 'date')


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score')
    list_filter = ('exam__subject',)
    search_fields = ('student__first_name', 'student__last_name')
