from django.db import models
from django.conf import settings


class Holiday(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} ({self.date})"


class Classe(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_department = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
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
    classe = models.ForeignKey(
        Classe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects'
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


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


class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"Exam: {self.subject.name} on {self.date}"


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
        related_name='exam_results'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.exam.subject.name}: {self.score}"


class Note(models.Model):
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
        related_name='notes'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notes_given'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student} — {self.subject.name} : {self.score}/{self.max_score}"

    @property
    def percentage(self):
        if self.max_score:
            return round((self.score / self.max_score) * 100, 1)
        return 0

    @property
    def mention(self):
        pct = self.percentage
        if pct >= 90: return ('Excellent', 'success')
        if pct >= 75: return ('Bien', 'primary')
        if pct >= 60: return ('Assez bien', 'info')
        if pct >= 50: return ('Passable', 'warning')
        return ('Insuffisant', 'danger')


class Notification(models.Model):
    TYPE_ICONS = {
        'teacher':    'fas fa-chalkboard-teacher',
        'department': 'fas fa-building',
        'subject':    'fas fa-book-reader',
        'timetable':  'fas fa-table',
        'exam':       'fas fa-clipboard-list',
    }

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.CharField(max_length=255)
    notif_type = models.CharField(max_length=20, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} — {self.message[:50]}"

    @property
    def icon(self):
        return self.TYPE_ICONS.get(self.notif_type, 'fas fa-bell')
