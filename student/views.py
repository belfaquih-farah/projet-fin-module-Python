from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home_auth.decorators import admin_required
from .models import Student, Parent


@admin_required
def student_list(request):
    students = Student.objects.select_related('parent').all()
    return render(request, 'students/students.html', {'students': students})


@admin_required
def add_student(request):
    if request.method == 'POST':
        parent = Parent.objects.create(
            father_name=request.POST.get('father_name'),
            father_occupation=request.POST.get('father_occupation', ''),
            father_mobile=request.POST.get('father_mobile'),
            father_email=request.POST.get('father_email'),
            mother_name=request.POST.get('mother_name'),
            mother_occupation=request.POST.get('mother_occupation', ''),
            mother_mobile=request.POST.get('mother_mobile'),
            mother_email=request.POST.get('mother_email'),
            present_address=request.POST.get('present_address'),
            permanent_address=request.POST.get('permanent_address'),
        )
        Student.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            student_id=request.POST.get('student_id'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            student_class=request.POST.get('student_class'),
            joining_date=request.POST.get('joining_date'),
            mobile_number=request.POST.get('mobile_number'),
            admission_number=request.POST.get('admission_number'),
            section=request.POST.get('section'),
            student_image=request.FILES.get('student_image'),
            parent=parent,
        )
        messages.success(request, 'Student added successfully.')
        return redirect('student_list')
    return render(request, 'students/add-student.html')


@admin_required
def view_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student, 'parent': student.parent})


@admin_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    parent = student.parent

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name', student.first_name)
        student.last_name = request.POST.get('last_name', student.last_name)
        student.gender = request.POST.get('gender', student.gender)
        student.date_of_birth = request.POST.get('date_of_birth', student.date_of_birth)
        student.student_class = request.POST.get('student_class', student.student_class)
        student.joining_date = request.POST.get('joining_date', student.joining_date)
        student.mobile_number = request.POST.get('mobile_number', student.mobile_number)
        student.admission_number = request.POST.get('admission_number', student.admission_number)
        student.section = request.POST.get('section', student.section)
        if request.FILES.get('student_image'):
            student.student_image = request.FILES['student_image']

        parent.father_name = request.POST.get('father_name', parent.father_name)
        parent.father_occupation = request.POST.get('father_occupation', parent.father_occupation)
        parent.father_mobile = request.POST.get('father_mobile', parent.father_mobile)
        parent.father_email = request.POST.get('father_email', parent.father_email)
        parent.mother_name = request.POST.get('mother_name', parent.mother_name)
        parent.mother_occupation = request.POST.get('mother_occupation', parent.mother_occupation)
        parent.mother_mobile = request.POST.get('mother_mobile', parent.mother_mobile)
        parent.mother_email = request.POST.get('mother_email', parent.mother_email)
        parent.present_address = request.POST.get('present_address', parent.present_address)
        parent.permanent_address = request.POST.get('permanent_address', parent.permanent_address)

        student.save()
        parent.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')

    return render(request, 'students/edit-student.html', {'student': student, 'parent': parent})


@admin_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.parent.delete()  # cascades to student via OneToOneField
    messages.success(request, 'Student deleted successfully.')
    return redirect('student_list')
