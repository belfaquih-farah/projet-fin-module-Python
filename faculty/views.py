from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Holiday
from student.models import Student


def index(request):
    return render(request, "authentication/login.html")

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'students/student-dashboard.html', {'total_students': total_students})

@login_required
def teacher_dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'students/student-dashboard.html', {'total_students': total_students})

@login_required
def admin_dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'students/student-dashboard.html', {'total_students': total_students})

@login_required
def holiday_list(request):
    holidays = Holiday.objects.all().order_by('date')
    return render(request, 'holidays/holidays.html', {'holiday_list': holidays})

@login_required
def add_holiday(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        description = request.POST.get('description', '')
        Holiday.objects.create(name=name, date=date, description=description)
        messages.success(request, 'Holiday added successfully.')
        return redirect('holiday_list')
    return render(request, 'holidays/add-holiday.html')

@login_required
def edit_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.name = request.POST.get('name', holiday.name)
        holiday.date = request.POST.get('date', holiday.date)
        holiday.description = request.POST.get('description', holiday.description)
        holiday.save()
        messages.success(request, 'Holiday updated successfully.')
        return redirect('holiday_list')
    return render(request, 'holidays/edit-holiday.html', {'holiday': holiday})

@login_required
def delete_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    holiday.delete()
    messages.success(request, 'Holiday deleted successfully.')
    return redirect('holiday_list')
