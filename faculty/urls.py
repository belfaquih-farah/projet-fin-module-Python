from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Teacher CRUD
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/<str:employee_id>/', views.view_teacher, name='view_teacher'),
    path('teachers/<str:employee_id>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teachers/<str:employee_id>/delete/', views.delete_teacher, name='delete_teacher'),

    # Holidays
    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.add_holiday, name='add_holiday'),
    path('holidays/<int:pk>/edit/', views.edit_holiday, name='edit_holiday'),
    path('holidays/<int:pk>/delete/', views.delete_holiday, name='delete_holiday'),

    # Calendar (Holidays + Events)
    path('calendar/', views.calendar_view, name='calendar'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),

    # TimeTable
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.add_timetable, name='add_timetable'),
    path('timetable/<int:pk>/delete/', views.delete_timetable, name='delete_timetable'),
]
