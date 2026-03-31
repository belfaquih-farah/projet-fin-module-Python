from django.db import models
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers'
    )
    joining_date = models.DateField()
    profile_pic = models.ImageField(upload_to='teachers/', blank=True)
    qualification = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.employee_id})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects'
    )

    def __str__(self):
        return self.name


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} ({self.date})"


class Event(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField()
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} ({self.date})"


class TimeTable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetable_entries')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.subject} — {self.day} {self.start_time:%H:%M}-{self.end_time:%H:%M}"
