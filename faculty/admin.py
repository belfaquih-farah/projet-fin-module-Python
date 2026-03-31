from django.contrib import admin
from .models import Department, Teacher, Subject, Holiday, Event, TimeTable


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


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description')
    search_fields = ('name',)
    list_filter = ('date',)


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
