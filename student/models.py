from django.db import models
from django.conf import settings


class Parent(models.Model):
    father_name = models.CharField(max_length=100, blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=15, blank=True)
    father_email = models.EmailField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=15, blank=True)
    mother_email = models.EmailField(max_length=100, blank=True)
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.father_name} & {self.mother_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField(null=True, blank=True)
    classe = models.ForeignKey(
        'faculty.Classe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    email = models.EmailField(max_length=150, blank=True, unique=True, null=True)
    joining_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    admission_number = models.CharField(max_length=20, blank=True)
    section = models.CharField(max_length=10, blank=True)
    student_image = models.ImageField(upload_to='students/', blank=True)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
