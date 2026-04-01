from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from home_auth.decorators import admin_required
from .models import Student, Parent
from .forms import StudentForm, ParentForm
from faculty.models import Classe
import uuid

User = get_user_model()


@login_required
def student_list(request):
    students = Student.objects.select_related('parent', 'classe').all()
    return render(request, 'students/students.html', {'student_list': students})


@admin_required
def add_student(request):
    classes = Classe.objects.all()
    if request.method == 'POST':
        # Parent (optionnel)
        parent_fields = ['father_name', 'father_mobile', 'father_email',
                         'mother_name', 'mother_mobile', 'mother_email', 'present_address']
        has_parent_data = any(request.POST.get(f, '').strip() for f in parent_fields)
        parent = None
        if has_parent_data:
            parent = Parent.objects.create(
                father_name=request.POST.get('father_name', ''),
                father_occupation=request.POST.get('father_occupation', ''),
                father_mobile=request.POST.get('father_mobile', ''),
                father_email=request.POST.get('father_email', ''),
                mother_name=request.POST.get('mother_name', ''),
                mother_occupation=request.POST.get('mother_occupation', ''),
                mother_mobile=request.POST.get('mother_mobile', ''),
                mother_email=request.POST.get('mother_email', ''),
                present_address=request.POST.get('present_address', ''),
                permanent_address=request.POST.get('permanent_address', ''),
            )

        # Auto-générer student_id si vide
        student_id = request.POST.get('student_id', '').strip()
        if not student_id:
            student_id = 'STU-' + uuid.uuid4().hex[:6].upper()

        classe_id = request.POST.get('classe')
        classe = Classe.objects.filter(pk=classe_id).first() if classe_id else None
        email = request.POST.get('email', '').strip() or None
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Vérifier si l'email existe déjà
        if email and User.objects.filter(email=email).exists():
            messages.error(request, f"Un compte avec l'email {email} existe déjà.")
            return render(request, 'students/add-student.html', {'classes': classes})

        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth') or None,
            email=email,
            classe=classe,
            joining_date=request.POST.get('joining_date') or None,
            mobile_number=request.POST.get('mobile_number', ''),
            admission_number=request.POST.get('admission_number', ''),
            section=request.POST.get('section', ''),
            student_image=request.FILES.get('student_image'),
            parent=parent,
        )

        # Créer automatiquement le compte utilisateur si email fourni
        if email:
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=student_id,
                is_student=True,
            )
            student.user = user
            student.save()
            messages.success(
                request,
                f'Étudiant créé. Compte : email = {email} | mot de passe = {student_id}'
            )
        else:
            messages.success(request, f'Étudiant créé (ID: {student_id}). Aucun email → pas de compte login.')

        return redirect('student_list')
    return render(request, 'students/add-student.html', {'classes': classes})


@login_required
def view_student(request, student_id):
    student = get_object_or_404(Student.objects.select_related('parent', 'classe'), student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student, 'parent': student.parent})


@admin_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    parent = student.parent
    classes = Classe.objects.all()

    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        parent_form = ParentForm(request.POST, instance=parent) if parent else None

        if student_form.is_valid() and (parent_form is None or parent_form.is_valid()):
            student_form.save()
            if parent_form:
                parent_form.save()

            new_email = request.POST.get('email', '').strip() or None

            if student.user:
                # Sync name on existing account
                student.user.first_name = student.first_name
                student.user.last_name = student.last_name
                if new_email and new_email != student.user.email:
                    if User.objects.filter(email=new_email).exclude(pk=student.user.pk).exists():
                        messages.error(request, f"L'email {new_email} est déjà utilisé.")
                        return redirect('edit_student', student_id=student_id)
                    student.user.email = new_email
                    student.user.username = new_email
                student.user.save()
            elif new_email:
                # No account yet — create one
                if User.objects.filter(email=new_email).exists():
                    messages.error(request, f"L'email {new_email} est déjà utilisé.")
                    return redirect('edit_student', student_id=student_id)
                user = User.objects.create_user(
                    username=new_email,
                    email=new_email,
                    first_name=student.first_name,
                    last_name=student.last_name,
                    password=student.student_id,
                    is_student=True,
                )
                student.user = user
                student.save()
                messages.success(request, f'Compte créé : email = {new_email} | mot de passe = {student.student_id}')

            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        student_form = StudentForm(instance=student)
        parent_form = ParentForm(instance=parent) if parent else None

    return render(request, 'students/edit-student.html', {
        'student_form': student_form,
        'parent_form': parent_form,
        'student': student,
        'parent': parent,
        'classes': classes,
    })


@admin_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if student.user:
        student.user.delete()
    if student.parent:
        student.parent.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('student_list')
