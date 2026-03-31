from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import Teacher, Department, Subject, Holiday, Event, TimeTable
from home_auth.decorators import admin_required, teacher_required
from student.models import Student

User = get_user_model()


def index(request):
    return render(request, 'authentication/login.html')


@admin_required
def dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'students/student-dashboard.html', {'total_students': total_students})


@admin_required
def admin_dashboard(request):
    context = {
        'teacher_count': Teacher.objects.count(),
        'student_count': Student.objects.count(),
        'department_count': Department.objects.count(),
        'subject_count': Subject.objects.count(),
    }
    return render(request, 'faculty/admin-dashboard.html', context)


@teacher_required
def teacher_dashboard(request):
    teacher = None
    if hasattr(request.user, 'teacher_profile'):
        teacher = request.user.teacher_profile
    return render(request, 'faculty/teacher-dashboard.html', {'teacher': teacher})


# ── Teacher CRUD ──────────────────────────────────────────────────────────────

@admin_required
def teacher_list(request):
    teachers = Teacher.objects.select_related('user', 'department').all()
    return render(request, 'faculty/teachers.html', {'teachers': teachers})


@admin_required
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


@admin_required
def view_teacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id)
    return render(request, 'faculty/teacher-details.html', {'teacher': teacher})


@admin_required
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


@admin_required
def delete_teacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id)
    teacher.user.delete()
    messages.success(request, 'Teacher deleted successfully.')
    return redirect('teacher_list')


# ── Holidays ──────────────────────────────────────────────────────────────────

@admin_required
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'faculty/holiday-list.html', {'holidays': holidays})


@admin_required
def add_holiday(request):
    if request.method == 'POST':
        Holiday.objects.create(
            name=request.POST.get('name'),
            date=request.POST.get('date'),
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Holiday added successfully.')
        return redirect('holiday_list')
    return render(request, 'faculty/add-holiday.html')


@admin_required
def edit_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.name = request.POST.get('name')
        holiday.date = request.POST.get('date')
        holiday.description = request.POST.get('description', '')
        holiday.save()
        messages.success(request, 'Holiday updated.')
        return redirect('holiday_list')
    return render(request, 'faculty/edit-holiday.html', {'holiday': holiday})


@admin_required
def delete_holiday(request, pk):
    get_object_or_404(Holiday, pk=pk).delete()
    messages.success(request, 'Holiday deleted.')
    return redirect('holiday_list')


# ── Events ────────────────────────────────────────────────────────────────────

@admin_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'faculty/event-list.html', {'events': events})


@admin_required
def add_event(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST.get('title'),
            date=request.POST.get('date'),
            location=request.POST.get('location', ''),
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Event added successfully.')
        return redirect('event_list')
    return render(request, 'faculty/add-event.html')


@admin_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.date = request.POST.get('date')
        event.location = request.POST.get('location', '')
        event.description = request.POST.get('description', '')
        event.save()
        messages.success(request, 'Event updated.')
        return redirect('event_list')
    return render(request, 'faculty/edit-event.html', {'event': event})


@admin_required
def delete_event(request, pk):
    get_object_or_404(Event, pk=pk).delete()
    messages.success(request, 'Event deleted.')
    return redirect('event_list')


# ── TimeTable ─────────────────────────────────────────────────────────────────

@admin_required
def timetable_view(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    entries = TimeTable.objects.select_related('subject', 'teacher__user').all()
    timetable_rows = [(day, list(entries.filter(day=day))) for day in days]
    return render(request, 'faculty/timetable.html', {'timetable_rows': timetable_rows, 'days': days})


@admin_required
def add_timetable(request):
    subjects = Subject.objects.select_related('department').all()
    teachers = Teacher.objects.select_related('user').all()
    days = TimeTable.DAY_CHOICES
    if request.method == 'POST':
        TimeTable.objects.create(
            subject_id=request.POST.get('subject'),
            teacher_id=request.POST.get('teacher'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            room=request.POST.get('room', ''),
        )
        messages.success(request, 'Timetable entry added.')
        return redirect('timetable')
    return render(request, 'faculty/add-timetable.html', {
        'subjects': subjects,
        'teachers': teachers,
        'days': days,
    })


@admin_required
def delete_timetable(request, pk):
    get_object_or_404(TimeTable, pk=pk).delete()
    messages.success(request, 'Entry deleted.')
    return redirect('timetable')
