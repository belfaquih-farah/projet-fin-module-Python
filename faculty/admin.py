from django.contrib import admin
from .models import Holiday, Department, Teacher, Subject, Exam, ExamResult

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'duration', 'room')
    list_filter = ('subject', 'date')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score')
    list_filter = ('exam__subject',)
    search_fields = ('student__first_name', 'student__last_name')

admin.site.register(Holiday)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Subject)
