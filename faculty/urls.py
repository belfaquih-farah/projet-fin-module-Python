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
]
