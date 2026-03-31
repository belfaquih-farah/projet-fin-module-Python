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
    return render(request, 'students/student-details.html', {'student': student})


@admin_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        if request.FILES.get('student_image'):
            student.student_image = request.FILES['student_image']
        student.save()

        p = student.parent
        p.father_name = request.POST.get('father_name')
        p.father_occupation = request.POST.get('father_occupation', '')
        p.father_mobile = request.POST.get('father_mobile')
        p.father_email = request.POST.get('father_email')
        p.mother_name = request.POST.get('mother_name')
        p.mother_occupation = request.POST.get('mother_occupation', '')
        p.mother_mobile = request.POST.get('mother_mobile')
        p.mother_email = request.POST.get('mother_email')
        p.present_address = request.POST.get('present_address')
        p.permanent_address = request.POST.get('permanent_address')
        p.save()

        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')
    return render(request, 'students/edit-student.html', {'student': student})


@admin_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.parent.delete()  # CASCADE deletes student too
    messages.success(request, 'Student deleted successfully.')
    return redirect('student_list')
