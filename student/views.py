# student/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Student, Parent
from .forms import StudentForm, ParentForm


@login_required
def student_list(request):
    students = Student.objects.select_related('parent').all()
    return render(request, 'students/students.html', {'student_list': students})


@login_required
@transaction.atomic  # Assure que les deux objets (parent et étudiant) sont créés ou aucun
def add_student(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES)
        parent_form = ParentForm(request.POST)

        if student_form.is_valid() and parent_form.is_valid():
            parent = parent_form.save()
            student = student_form.save(commit=False)
            student.parent = parent
            student.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        student_form = StudentForm()
        parent_form = ParentForm()

    return render(request, 'students/add-student.html', {
        'student_form': student_form,
        'parent_form': parent_form
    })


@login_required
@transaction.atomic
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    parent = student.parent

    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        parent_form = ParentForm(request.POST, instance=parent)

        if student_form.is_valid() and parent_form.is_valid():
            student_form.save()
            parent_form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        student_form = StudentForm(instance=student)
        parent_form = ParentForm(instance=parent)

    return render(request, 'students/edit-student.html', {
        'student_form': student_form,
        'parent_form': parent_form,
        'student': student  # Garder l'objet student pour l'affichage
    })


@login_required
def view_student(request, student_id):
    # On utilise select_related pour optimiser la requête en récupérant le parent en même temps
    student = get_object_or_404(Student.objects.select_related('parent'), student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student})


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == 'POST':
        # La suppression de l'étudiant entraînera la suppression du parent
        # si on_delete=models.CASCADE est défini sur le champ 'parent' du modèle Student.
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')

    # Pour une requête GET, on affiche une page de confirmation.
    return render(request, 'students/delete-student-confirm.html', {'student': student})