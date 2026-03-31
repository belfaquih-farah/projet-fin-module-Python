from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Holidays
    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.add_holiday, name='add_holiday'),
    path('holidays/edit/<int:pk>/', views.edit_holiday, name='edit_holiday'),
    path('holidays/delete/<int:pk>/', views.delete_holiday, name='delete_holiday'),

    # Teacher CRUD
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/<str:employee_id>/', views.view_teacher, name='view_teacher'),
    path('teachers/<str:employee_id>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teachers/<str:employee_id>/delete/', views.delete_teacher, name='delete_teacher'),

    # Department CRUD
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/<int:pk>/edit/', views.edit_department, name='edit_department'),
    path('departments/<int:pk>/delete/', views.delete_department, name='delete_department'),

    # Subject CRUD
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/<int:pk>/edit/', views.edit_subject, name='edit_subject'),
    path('subjects/<int:pk>/delete/', views.delete_subject, name='delete_subject'),

    # Exam CRUD
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/<int:pk>/edit/', views.edit_exam, name='edit_exam'),
    path('exams/<int:pk>/delete/', views.delete_exam, name='delete_exam'),
    path('exams/<int:pk>/results/', views.exam_results, name='exam_results'),
]
