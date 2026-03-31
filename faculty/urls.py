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
]
