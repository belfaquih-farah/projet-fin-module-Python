from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import calendar
from datetime import date, time as dt_time

from .models import Classe, Teacher, Department, Subject, Holiday, Event, TimeTable, Exam, ExamResult, Note, Notification
from .notifications import notify_admins
from django.contrib.auth.decorators import login_required
from home_auth.decorators import admin_required, teacher_required
from student.models import Student

User = get_user_model()


def index(request):
    return render(request, 'authentication/login.html')


@login_required
def profile_view(request):
    return render(request, 'faculty/profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        if request.user.is_admin and request.FILES.get('profile_pic'):
            request.user.profile_pic = request.FILES['profile_pic']
        request.user.save()
        messages.success(request, 'Profil mis à jour avec succès.')
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))


@login_required
def inbox_view(request):
    return render(request, 'faculty/inbox.html')


@login_required
def dashboard(request):
    student = None
    notes = []
    if hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
        notes = student.notes.select_related('subject').all()
    return render(request, 'students/student-dashboard.html', {
        'student': student,
        'notes': notes,
    })


@admin_required
def admin_dashboard(request):
    context = {
        'teacher_count': Teacher.objects.count(),
        'student_count': Student.objects.count(),
        'department_count': Department.objects.count(),
        'subject_count': Subject.objects.count(),
        'exam_count': Exam.objects.count(),
        'holiday_count': Holiday.objects.count(),
        'upcoming_exams': Exam.objects.filter(date__gte=date.today()).order_by('date')[:5],
    }
    return render(request, 'faculty/admin-dashboard.html', context)


@teacher_required
def teacher_dashboard(request):
    teacher = None
    subjects = []
    students = []
    selected_subject_id = request.GET.get('subject')

    if hasattr(request.user, 'teacher_profile'):
        teacher = request.user.teacher_profile
        subjects = Subject.objects.filter(teacher=teacher).select_related('classe', 'department')

        if selected_subject_id:
            selected_subject = subjects.filter(pk=selected_subject_id).first()
            if selected_subject and selected_subject.classe:
                students = Student.objects.filter(classe=selected_subject.classe).select_related('classe')
        else:
            classes = [s.classe for s in subjects if s.classe]
            students = Student.objects.filter(classe__in=classes).select_related('classe').distinct()

    return render(request, 'faculty/teacher-dashboard.html', {
        'teacher': teacher,
        'subjects': subjects,
        'students': students,
        'selected_subject_id': selected_subject_id,
    })


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
            password=employee_id,
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
        notify_admins(f"Nouvel enseignant créé : {first_name} {last_name} ({email})", 'teacher')
        messages.success(request, f'Teacher added. Login: email = {email} | password = {employee_id}')
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


# ── Department CRUD ───────────────────────────────────────────────────────────

@admin_required
def department_list(request):
    departments = Department.objects.prefetch_related('teachers').all()
    return render(request, 'faculty/departments.html', {'department_list': departments})


@admin_required
def add_department(request):
    teachers = Teacher.objects.select_related('user').all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        head_id = request.POST.get('head_of_department')
        head = Teacher.objects.filter(pk=head_id).first() if head_id else None
        Department.objects.create(name=name, description=description, head_of_department=head)
        notify_admins(f"Nouveau département créé : {name}", 'department')
        messages.success(request, 'Department added successfully.')
        return redirect('department_list')
    return render(request, 'faculty/add-department.html', {'teachers': teachers})


@admin_required
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


@admin_required
def delete_department(request, pk):
    get_object_or_404(Department, pk=pk).delete()
    messages.success(request, 'Department deleted successfully.')
    return redirect('department_list')


# ── Subject CRUD ──────────────────────────────────────────────────────────────

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


@admin_required
def add_subject(request):
    departments = Department.objects.all()
    teachers = Teacher.objects.select_related('user').all()
    classes = Classe.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        classe_id = request.POST.get('classe')
        department = get_object_or_404(Department, pk=department_id)
        teacher = Teacher.objects.filter(pk=teacher_id).first() if teacher_id else None
        classe = Classe.objects.filter(pk=classe_id).first() if classe_id else None
        Subject.objects.create(name=name, description=description, department=department, teacher=teacher, classe=classe)
        notify_admins(f"Nouvelle matière créée : {name} (Classe : {classe or '—'}, Prof : {teacher or '—'})", 'subject')
        messages.success(request, 'Subject added successfully.')
        return redirect('subject_list')
    return render(request, 'faculty/add-subject.html', {'departments': departments, 'teachers': teachers, 'classes': classes})


@admin_required
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    departments = Department.objects.all()
    teachers = Teacher.objects.select_related('user').all()
    classes = Classe.objects.all()
    if request.method == 'POST':
        subject.name = request.POST.get('name', subject.name)
        subject.description = request.POST.get('description', subject.description)
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        classe_id = request.POST.get('classe')
        subject.department = get_object_or_404(Department, pk=department_id)
        subject.teacher = Teacher.objects.filter(pk=teacher_id).first() if teacher_id else None
        subject.classe = Classe.objects.filter(pk=classe_id).first() if classe_id else None
        subject.save()
        messages.success(request, 'Subject updated successfully.')
        return redirect('subject_list')
    return render(request, 'faculty/edit-subject.html', {
        'subject': subject,
        'departments': departments,
        'teachers': teachers,
        'classes': classes,
    })


@admin_required
def delete_subject(request, pk):
    get_object_or_404(Subject, pk=pk).delete()
    messages.success(request, 'Subject deleted successfully.')
    return redirect('subject_list')


# ── Holidays ──────────────────────────────────────────────────────────────────

@login_required
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


# ── Calendar ──────────────────────────────────────────────────────────────────

@admin_required
def calendar_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1
    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    cal = calendar.monthcalendar(year, month)
    holidays = Holiday.objects.filter(date__year=year, date__month=month)
    events = Event.objects.filter(date__year=year, date__month=month)

    day_items = {}
    for h in holidays:
        day_items.setdefault(h.date.day, []).append({'label': h.name, 'type': 'holiday'})
    for e in events:
        day_items.setdefault(e.date.day, []).append({'label': e.title, 'type': 'event'})

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'weeks': cal,
        'day_items': day_items,
        'today': today,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'day_names': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'holidays': holidays,
        'events': events,
    }
    return render(request, 'faculty/calendar.html', context)


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

@login_required
def timetable_view(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    entries = TimeTable.objects.select_related('subject__department', 'teacher__user').all()

    # Filter by class if requested
    classe_filter = request.GET.get('classe')
    classes = Classe.objects.all()
    if classe_filter:
        entries = entries.filter(subject__classe_id=classe_filter)

    # Fixed 8:00–18:00 grid, 30-min slots
    slots = [dt_time(h, m) for h in range(8, 18) for m in (0, 30)]

    # Build cell map: each entry placed only at its start_time slot
    # occupied: {day: {slot: True}} for continuation slots (greyed out)
    cell_map = {day: {slot: [] for slot in slots} for day in days}
    occupied = {day: {} for day in days}
    for entry in entries:
        if entry.start_time in cell_map.get(entry.day, {}):
            cell_map[entry.day][entry.start_time].append(entry)
        for slot in slots:
            if entry.start_time < slot < entry.end_time:
                occupied[entry.day][slot] = entry.subject.pk

    return render(request, 'faculty/timetable.html', {
        'days': days,
        'slots': slots,
        'cell_map': cell_map,
        'occupied': occupied,
        'entries': entries,
        'classes': classes,
        'classe_filter': classe_filter,
    })


@login_required
def timetable_json(request):
    entries = TimeTable.objects.select_related('subject__classe', 'teacher__user').all()
    classe_filter = request.GET.get('classe')
    if classe_filter:
        entries = entries.filter(subject__classe_id=classe_filter)
    data = []
    for e in entries:
        data.append({
            'id': e.pk,
            'day': e.day,
            'start_time': e.start_time.strftime('%H:%M'),
            'end_time': e.end_time.strftime('%H:%M'),
            'subject': e.subject.name,
            'department': e.subject.department.name if e.subject.department else '',
            'classe': e.subject.classe.name if e.subject.classe else '',
            'teacher': f"{e.teacher.user.first_name} {e.teacher.user.last_name}",
            'room': e.room,
        })
    return JsonResponse({'timetable': data})


@admin_required
def add_timetable(request):
    subjects = Subject.objects.select_related('department').all()
    teachers = Teacher.objects.select_related('user').all()
    days = TimeTable.DAY_CHOICES
    if request.method == 'POST':
        entry = TimeTable.objects.create(
            subject_id=request.POST.get('subject'),
            teacher_id=request.POST.get('teacher'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            room=request.POST.get('room', ''),
        )
        notify_admins(
            f"Nouvel emploi du temps : {entry.subject} — {entry.day} {entry.start_time}-{entry.end_time} ({entry.teacher})",
            'timetable'
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


# ── Exam CRUD ─────────────────────────────────────────────────────────────────

@login_required
def exam_list(request):
    exams = Exam.objects.select_related('subject').order_by('date')
    return render(request, 'faculty/exams.html', {'exam_list': exams})


@admin_required
def add_exam(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        exam_date = request.POST.get('date')
        duration = request.POST.get('duration')
        room = request.POST.get('room', '')
        subject = get_object_or_404(Subject, pk=subject_id)
        Exam.objects.create(subject=subject, date=exam_date, duration=duration, room=room)
        notify_admins(f"Examen planifié : {subject.name} le {exam_date} ({duration} min, salle {room or '—'})", 'exam')
        messages.success(request, 'Exam added successfully.')
        return redirect('exam_list')
    return render(request, 'faculty/add-exam.html', {'subjects': subjects})


@admin_required
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


@admin_required
def delete_exam(request, pk):
    get_object_or_404(Exam, pk=pk).delete()
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


# ── Classe CRUD ───────────────────────────────────────────────────────────────

@login_required
def classe_detail(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    subjects = Subject.objects.filter(classe=classe).select_related('teacher__user', 'department')
    students = Student.objects.filter(classe=classe)
    return render(request, 'faculty/class-detail.html', {
        'classe': classe,
        'subjects': subjects,
        'students': students,
    })


@login_required
def mark_notifications_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))


@admin_required
def classe_list(request):
    classes = Classe.objects.all()
    return render(request, 'faculty/classes.html', {'classes': classes})


@admin_required
def add_classe(request):
    if request.method == 'POST':
        Classe.objects.create(
            name=request.POST.get('name'),
            level=request.POST.get('level', ''),
        )
        messages.success(request, 'Classe ajoutée avec succès.')
        return redirect('classe_list')
    return render(request, 'faculty/add-class.html')


@admin_required
def edit_classe(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        classe.name = request.POST.get('name', classe.name)
        classe.level = request.POST.get('level', classe.level)
        classe.save()
        messages.success(request, 'Classe modifiée avec succès.')
        return redirect('classe_list')
    return render(request, 'faculty/edit-class.html', {'classe': classe})


@admin_required
def delete_classe(request, pk):
    get_object_or_404(Classe, pk=pk).delete()
    messages.success(request, 'Classe supprimée.')
    return redirect('classe_list')


# ── Notes ─────────────────────────────────────────────────────────────────────

@login_required
def notes_list(request):
    """Admin: all notes. Teacher: only their notes."""
    if request.user.is_admin:
        notes = Note.objects.select_related('student', 'subject', 'teacher__user').all()
        subjects = Subject.objects.all()
    elif request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        teacher = request.user.teacher_profile
        notes = Note.objects.filter(teacher=teacher).select_related('student', 'subject', 'teacher__user')
        subjects = Subject.objects.filter(teacher=teacher)
    else:
        return redirect('dashboard')

    # Filter by subject
    subject_id = request.GET.get('subject')
    if subject_id:
        notes = notes.filter(subject_id=subject_id)

    return render(request, 'faculty/notes.html', {
        'notes': notes,
        'subjects': subjects,
        'selected_subject': subject_id,
    })


@teacher_required
def add_note(request):
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher:
        messages.error(request, 'Profil enseignant introuvable.')
        return redirect('teacher_dashboard')

    subjects = Subject.objects.filter(teacher=teacher).select_related('classe')
    students = []
    selected_subject = None

    subject_id = request.GET.get('subject') or request.POST.get('subject')
    if subject_id:
        selected_subject = Subject.objects.filter(pk=subject_id, teacher=teacher).first()
        if selected_subject and selected_subject.classe:
            students = Student.objects.filter(classe=selected_subject.classe)

    if request.method == 'POST' and selected_subject:
        student_id = request.POST.get('student')
        score = request.POST.get('score')
        max_score = request.POST.get('max_score', 20)
        comment = request.POST.get('comment', '')
        student = get_object_or_404(Student, pk=student_id)

        note, created = Note.objects.update_or_create(
            student=student,
            subject=selected_subject,
            defaults={'teacher': teacher, 'score': score, 'max_score': max_score, 'comment': comment}
        )
        action = 'ajoutée' if created else 'modifiée'
        messages.success(request, f'Note {action} pour {student.first_name} {student.last_name}.')
        return redirect(f"{request.path}?subject={selected_subject.pk}")

    return render(request, 'faculty/add-note.html', {
        'subjects': subjects,
        'students': students,
        'selected_subject': selected_subject,
    })


@teacher_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    teacher = getattr(request.user, 'teacher_profile', None)
    if not request.user.is_admin and note.teacher != teacher:
        messages.error(request, 'Accès refusé.')
        return redirect('notes_list')

    if request.method == 'POST':
        note.score = request.POST.get('score', note.score)
        note.max_score = request.POST.get('max_score', note.max_score)
        note.comment = request.POST.get('comment', note.comment)
        note.save()
        messages.success(request, 'Note modifiée.')
        return redirect('notes_list')

    return render(request, 'faculty/edit-note.html', {'note': note})


@teacher_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    teacher = getattr(request.user, 'teacher_profile', None)
    if not request.user.is_admin and note.teacher != teacher:
        messages.error(request, 'Accès refusé.')
        return redirect('notes_list')
    note.delete()
    messages.success(request, 'Note supprimée.')
    return redirect('notes_list')


@login_required
def student_notes(request):
    """Student sees their own notes."""
    student = getattr(request.user, 'student_profile', None)
    if not student:
        messages.warning(request, 'Aucun profil étudiant lié à ce compte.')
        return render(request, 'students/my-notes.html', {'notes': [], 'student': None})

    notes = Note.objects.filter(student=student).select_related('subject__department', 'teacher__user')
    return render(request, 'students/my-notes.html', {'notes': notes, 'student': student})
