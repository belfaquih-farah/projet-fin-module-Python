from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Holiday, Teacher, Department, Subject, Exam, ExamResult
from student.models import Student

User = get_user_model()


def index(request):
    return render(request, 'authentication/login.html')


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'students/student-dashboard.html', {'total_students': total_students})


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


# ── Department CRUD ────────────────────────────────────────────────────────────

@login_required
def department_list(request):
    departments = Department.objects.prefetch_related('teachers').all()
    return render(request, 'faculty/departments.html', {'department_list': departments})


@login_required
def add_department(request):
    teachers = Teacher.objects.select_related('user').all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        head_id = request.POST.get('head_of_department')
        head = Teacher.objects.filter(pk=head_id).first() if head_id else None
        Department.objects.create(name=name, description=description, head_of_department=head)
        messages.success(request, 'Department added successfully.')
        return redirect('department_list')
    return render(request, 'faculty/add-department.html', {'teachers': teachers})


@login_required
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teachers = Teacher.objects.select_related('user').all()
    if request.method == 'POST':
        department.name = request.POST.get('name', department.name)
        department.description = request.POST.get('description', department.description)
        head_id = request.POST.get('head_of_department')
        department.head_of_department = Teacher.objects.filter(pk=head_id).first() if head_id else None
        department.save()
        messages.success(request, 'Department updated successfully.')
        return redirect('department_list')
    return render(request, 'faculty/edit-department.html', {'department': department, 'teachers': teachers})


@login_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, 'Department deleted successfully.')
    return redirect('department_list')


# ── Subject CRUD ───────────────────────────────────────────────────────────────

@login_required
def subject_list(request):
    department_id = request.GET.get('department')
    subjects = Subject.objects.select_related('department', 'teacher__user').all()
    if department_id:
        subjects = subjects.filter(department_id=department_id)
    departments = Department.objects.all()
    return render(request, 'faculty/subjects.html', {
        'subject_list': subjects,
        'departments': departments,
        'selected_department': department_id,
    })


@login_required
def add_subject(request):
    departments = Department.objects.all()
    teachers = Teacher.objects.select_related('user').all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        department = get_object_or_404(Department, pk=department_id)
        teacher = Teacher.objects.filter(pk=teacher_id).first() if teacher_id else None
        Subject.objects.create(name=name, description=description, department=department, teacher=teacher)
        messages.success(request, 'Subject added successfully.')
        return redirect('subject_list')
    return render(request, 'faculty/add-subject.html', {'departments': departments, 'teachers': teachers})


@login_required
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    departments = Department.objects.all()
    teachers = Teacher.objects.select_related('user').all()
    if request.method == 'POST':
        subject.name = request.POST.get('name', subject.name)
        subject.description = request.POST.get('description', subject.description)
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        subject.department = get_object_or_404(Department, pk=department_id)
        subject.teacher = Teacher.objects.filter(pk=teacher_id).first() if teacher_id else None
        subject.save()
        messages.success(request, 'Subject updated successfully.')
        return redirect('subject_list')
    return render(request, 'faculty/edit-subject.html', {
        'subject': subject,
        'departments': departments,
        'teachers': teachers,
    })


@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, 'Subject deleted successfully.')
    return redirect('subject_list')


# ── Exam CRUD ──────────────────────────────────────────────────────────────────

@login_required
def exam_list(request):
    exams = Exam.objects.select_related('subject').order_by('date')
    return render(request, 'faculty/exams.html', {'exam_list': exams})


@login_required
def add_exam(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        duration = request.POST.get('duration')
        room = request.POST.get('room', '')
        subject = get_object_or_404(Subject, pk=subject_id)
        Exam.objects.create(subject=subject, date=date, duration=duration, room=room)
        messages.success(request, 'Exam added successfully.')
        return redirect('exam_list')
    return render(request, 'faculty/add-exam.html', {'subjects': subjects})


@login_required
def edit_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        exam.subject = get_object_or_404(Subject, pk=request.POST.get('subject'))
        exam.date = request.POST.get('date', exam.date)
        exam.duration = request.POST.get('duration', exam.duration)
        exam.room = request.POST.get('room', exam.room)
        exam.save()
        messages.success(request, 'Exam updated successfully.')
        return redirect('exam_list')
    return render(request, 'faculty/edit-exam.html', {'exam': exam, 'subjects': subjects})


@login_required
def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.delete()
    messages.success(request, 'Exam deleted successfully.')
    return redirect('exam_list')


@login_required
def exam_results(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    results = ExamResult.objects.filter(exam=exam).select_related('student')
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student')
        score = request.POST.get('score')
        student = get_object_or_404(Student, pk=student_id)
        ExamResult.objects.update_or_create(exam=exam, student=student, defaults={'score': score})
        messages.success(request, 'Result saved.')
        return redirect('exam_results', pk=pk)
    return render(request, 'faculty/exam-results.html', {
        'exam': exam,
        'results': results,
        'students': students,
    })


# ── Dashboard ──────────────────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    from datetime import date
    context = {
        'student_count': Student.objects.count(),
        'teacher_count': Teacher.objects.count(),
        'department_count': Department.objects.count(),
        'subject_count': Subject.objects.count(),
        'upcoming_exams': Exam.objects.filter(date__gte=date.today()).order_by('date')[:5],
    }
    return render(request, 'faculty/admin-dashboard.html', context)
