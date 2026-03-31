from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Holiday, Teacher, Department, Subject
from student.models import Student

User = get_user_model()


def index(request):
    return render(request, 'authentication/login.html')


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'students/student-dashboard.html', {'total_students': total_students})


@login_required
def admin_dashboard(request):
    context = {
        'teacher_count': Teacher.objects.count(),
        'student_count': Student.objects.count(),
        'department_count': Department.objects.count(),
        'subject_count': Subject.objects.count(),
    }
    return render(request, 'students/student-dashboard.html', context)


@login_required
def teacher_dashboard(request):
    teacher = None
    if hasattr(request.user, 'teacher_profile'):
        teacher = request.user.teacher_profile
    return render(request, 'students/student-dashboard.html', {'teacher': teacher})


# ── Holidays ──────────────────────────────────────────────────────────────────

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


# ── Teacher CRUD ──────────────────────────────────────────────────────────────

@login_required
def teacher_list(request):
    teachers = Teacher.objects.select_related('user', 'department').all()
    return render(request, 'faculty/teachers.html', {'teachers': teachers})


@login_required
def add_teacher(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        employee_id = request.POST.get('employee_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        department_id = request.POST.get('department')
        joining_date = request.POST.get('joining_date')
        qualification = request.POST.get('qualification')
        profile_pic = request.FILES.get('profile_pic')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'faculty/add-teacher.html', {'departments': departments})

        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_teacher=True,
        )
        department = Department.objects.filter(pk=department_id).first() if department_id else None
        Teacher.objects.create(
            user=user,
            employee_id=employee_id,
            gender=gender,
            date_of_birth=date_of_birth,
            phone=phone,
            address=address,
            department=department,
            joining_date=joining_date,
            qualification=qualification,
            profile_pic=profile_pic,
        )
        messages.success(request, 'Teacher added successfully.')
        return redirect('teacher_list')

    return render(request, 'faculty/add-teacher.html', {'departments': departments})


@login_required
def view_teacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id)
    return render(request, 'faculty/teacher-details.html', {'teacher': teacher})


@login_required
def edit_teacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id)
    departments = Department.objects.all()

    if request.method == 'POST':
        teacher.user.first_name = request.POST.get('first_name')
        teacher.user.last_name = request.POST.get('last_name')
        teacher.user.save()

        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.phone = request.POST.get('phone')
        teacher.address = request.POST.get('address')
        department_id = request.POST.get('department')
        teacher.department = Department.objects.filter(pk=department_id).first() if department_id else None
        teacher.joining_date = request.POST.get('joining_date')
        teacher.qualification = request.POST.get('qualification')
        if request.FILES.get('profile_pic'):
            teacher.profile_pic = request.FILES['profile_pic']
        teacher.save()

        messages.success(request, 'Teacher updated successfully.')
        return redirect('teacher_list')

    return render(request, 'faculty/edit-teacher.html', {
        'teacher': teacher,
        'departments': departments,
    })


@login_required
def delete_teacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id)
    teacher.user.delete()
    messages.success(request, 'Teacher deleted successfully.')
    return redirect('teacher_list')
