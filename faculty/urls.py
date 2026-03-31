from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.add_holiday, name='add_holiday'),
    path('holidays/edit/<int:pk>/', views.edit_holiday, name='edit_holiday'),
    path('holidays/delete/<int:pk>/', views.delete_holiday, name='delete_holiday'),
]