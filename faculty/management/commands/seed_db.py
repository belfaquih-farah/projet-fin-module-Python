"""
Seed the database with test data.
Usage: python manage.py seed_db
       python manage.py seed_db --flush   (wipe everything first)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import date, time

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Delete all existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self._flush()
        with transaction.atomic():
            self._seed()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
        self.stdout.write('')
        self.stdout.write('  Admin   → ikram@admin.com  / admin123')
        self.stdout.write('  Teacher → teacher1@school.ma / EMP001')
        self.stdout.write('           teacher2@school.ma / EMP002')
        self.stdout.write('           teacher3@school.ma / EMP003')
        self.stdout.write('  Student → saloua@school.ma  / STU-001')
        self.stdout.write('           (see list below for all students)')

    # ------------------------------------------------------------------
    def _flush(self):
        from faculty.models import (
            Classe, Department, Teacher, Subject,
            Holiday, TimeTable, Exam, Note, Notification
        )
        from student.models import Student, Parent
        self.stdout.write('Flushing existing data...')
        Note.objects.all().delete()
        Notification.objects.all().delete()
        TimeTable.objects.all().delete()
        Exam.objects.all().delete()
        Subject.objects.all().delete()
        Teacher.objects.all().delete()
        Department.objects.all().delete()
        Classe.objects.all().delete()
        Holiday.objects.all().delete()
        Student.objects.all().delete()
        Parent.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    # ------------------------------------------------------------------
    def _seed(self):
        from faculty.models import (
            Classe, Department, Teacher, Subject,
            Holiday, TimeTable, Exam, Note
        )
        from student.models import Student, Parent

        # ── Admin ──────────────────────────────────────────────────────
        admin, _ = User.objects.get_or_create(
            email='ikram@admin.com',
            defaults=dict(
                username='ikram@admin.com',
                first_name='Ikram',
                last_name='Admin',
                is_admin=True,
                is_staff=True,
            )
        )
        if _:
            admin.set_password('admin123')
            admin.save()

        # ── Departments ────────────────────────────────────────────────
        dept_info, _ = Department.objects.get_or_create(
            name='Informatique',
            defaults=dict(description='Département des sciences informatiques')
        )
        dept_math, _ = Department.objects.get_or_create(
            name='Mathématiques',
            defaults=dict(description='Département de mathématiques et statistiques')
        )
        dept_phys, _ = Department.objects.get_or_create(
            name='Physique',
            defaults=dict(description='Département de physique et chimie')
        )
        dept_lang, _ = Department.objects.get_or_create(
            name='Langues',
            defaults=dict(description='Département des langues et communication')
        )

        # ── Classes ────────────────────────────────────────────────────
        l1_info, _ = Classe.objects.get_or_create(name='L1 Informatique', defaults=dict(level='Licence 1'))
        l2_info, _ = Classe.objects.get_or_create(name='L2 Informatique', defaults=dict(level='Licence 2'))
        l3_info, _ = Classe.objects.get_or_create(name='L3 Informatique', defaults=dict(level='Licence 3'))
        m1_info, _ = Classe.objects.get_or_create(name='M1 Informatique', defaults=dict(level='Master 1'))

        # ── Teachers (user + profile) ───────────────────────────────────
        def make_teacher(email, emp_id, first, last, gender, dob, phone, dept, qual):
            user, created = User.objects.get_or_create(
                email=email,
                defaults=dict(username=email, first_name=first, last_name=last, is_teacher=True)
            )
            if created:
                user.set_password(emp_id)
                user.save()
            teacher, _ = Teacher.objects.get_or_create(
                employee_id=emp_id,
                defaults=dict(
                    user=user, gender=gender, date_of_birth=dob,
                    phone=phone, department=dept, joining_date=date(2020, 9, 1),
                    qualification=qual,
                )
            )
            return teacher

        t1 = make_teacher('teacher1@school.ma', 'EMP001', 'Ahmed',   'Benali',  'Male',   date(1985, 3, 15), '0661001001', dept_info, 'Doctorat Informatique')
        t2 = make_teacher('teacher2@school.ma', 'EMP002', 'Fatima',  'Alaoui',  'Female', date(1988, 7, 22), '0661001002', dept_math, 'Doctorat Mathématiques')
        t3 = make_teacher('teacher3@school.ma', 'EMP003', 'Youssef', 'Cherkaoui','Male',  date(1982, 11, 5), '0661001003', dept_phys, 'Doctorat Physique')
        t4 = make_teacher('teacher4@school.ma', 'EMP004', 'Nadia',   'Tazi',    'Female', date(1990, 2, 18), '0661001004', dept_lang, 'Master Langues')

        # ── Subjects ───────────────────────────────────────────────────
        def make_subject(name, dept, classe, teacher, desc=''):
            s, _ = Subject.objects.get_or_create(
                name=name, classe=classe,
                defaults=dict(department=dept, teacher=teacher, description=desc)
            )
            return s

        s_algo   = make_subject('Algorithmique',        dept_info, l1_info, t1)
        s_prog   = make_subject('Programmation Python', dept_info, l1_info, t1)
        s_bd     = make_subject('Bases de Données',     dept_info, l2_info, t1)
        s_reseau = make_subject('Réseaux',              dept_info, l2_info, t1)
        s_web    = make_subject('Développement Web',    dept_info, l3_info, t1)
        s_ana    = make_subject('Analyse',              dept_math, l1_info, t2)
        s_alg    = make_subject('Algèbre',              dept_math, l1_info, t2)
        s_stat   = make_subject('Statistiques',         dept_math, l2_info, t2)
        s_meca   = make_subject('Mécanique',            dept_phys, l1_info, t3)
        s_ang    = make_subject('Anglais Technique',    dept_lang, l1_info, t4)

        # ── Holidays ───────────────────────────────────────────────────
        holidays = [
            ('Aide Al-Fitr',       date(2025, 3, 30), 'Fête de fin du Ramadan'),
            ('Aide Al-Adha',       date(2025, 6, 6),  'Fête du sacrifice'),
            ('Fête du Trône',      date(2025, 7, 30), 'Commémoration de la fête du Trône'),
            ('Fête de la Jeunesse',date(2025, 8, 21), 'Anniversaire du Roi'),
            ('Fête de Indépendance',date(2025, 11, 18),'Fête de l\'indépendance du Maroc'),
            ('Nouvel An',          date(2026, 1, 1),  'Premier janvier'),
            ('Fête du Travail',    date(2026, 5, 1),  'Journée internationale du travail'),
        ]
        for name, d, desc in holidays:
            Holiday.objects.get_or_create(name=name, date=d, defaults=dict(description=desc))

        # ── Students ───────────────────────────────────────────────────
        students_data = [
            ('Saloua',   'Benali',  'STU-001', 'Female', date(2003, 4, 10), l1_info, 'saloua@school.ma'),
            ('Karim',    'Alami',   'STU-002', 'Male',   date(2003, 6, 22), l1_info, 'karim@school.ma'),
            ('Mariam',   'Tahiri',  'STU-003', 'Female', date(2004, 1, 15), l1_info, 'mariam@school.ma'),
            ('Omar',     'Idrissi', 'STU-004', 'Male',   date(2003, 9, 3),  l1_info, 'omar@school.ma'),
            ('Zineb',    'Fassi',   'STU-005', 'Female', date(2002, 11, 28),l2_info, 'zineb@school.ma'),
            ('Amine',    'Benhaddou','STU-006','Male',   date(2002, 5, 17), l2_info, 'amine@school.ma'),
            ('Hajar',    'Chraibi', 'STU-007', 'Female', date(2002, 8, 9),  l2_info, 'hajar@school.ma'),
            ('Yassine',  'Mansouri','STU-008', 'Male',   date(2001, 3, 25), l3_info, 'yassine@school.ma'),
            ('Rania',    'Moussaoui','STU-009','Female', date(2001, 7, 12), l3_info, 'rania@school.ma'),
            ('Hamza',    'Berrada', 'STU-010', 'Male',   date(2001, 12, 5), l3_info, 'hamza@school.ma'),
        ]

        created_students = []
        for first, last, sid, gender, dob, classe, email in students_data:
            student, s_created = Student.objects.get_or_create(
                student_id=sid,
                defaults=dict(
                    first_name=first, last_name=last, gender=gender,
                    date_of_birth=dob, classe=classe, email=email,
                    joining_date=date(2024, 9, 1), section='A',
                )
            )
            if s_created and email:
                user, u_created = User.objects.get_or_create(
                    email=email,
                    defaults=dict(
                        username=email, first_name=first, last_name=last,
                        is_student=True,
                    )
                )
                if u_created:
                    user.set_password(sid)
                    user.save()
                student.user = user
                student.save()
            created_students.append(student)

        # ── Timetable ──────────────────────────────────────────────────
        timetable_entries = [
            (s_algo,   t1, 'Monday',    time(8, 0),  time(10, 0), 'A101'),
            (s_prog,   t1, 'Monday',    time(10, 0), time(12, 0), 'A101'),
            (s_ana,    t2, 'Monday',    time(14, 0), time(16, 0), 'B201'),
            (s_alg,    t2, 'Tuesday',   time(8, 0),  time(10, 0), 'B201'),
            (s_meca,   t3, 'Tuesday',   time(10, 0), time(12, 0), 'C301'),
            (s_ang,    t4, 'Tuesday',   time(14, 0), time(16, 0), 'D101'),
            (s_algo,   t1, 'Wednesday', time(8, 0),  time(10, 0), 'A101'),
            (s_ana,    t2, 'Wednesday', time(10, 0), time(12, 0), 'B201'),
            (s_bd,     t1, 'Thursday',  time(8, 0),  time(10, 0), 'A102'),
            (s_reseau, t1, 'Thursday',  time(10, 0), time(12, 0), 'A102'),
            (s_stat,   t2, 'Thursday',  time(14, 0), time(16, 0), 'B202'),
            (s_prog,   t1, 'Friday',    time(8, 0),  time(10, 0), 'A101'),
            (s_ang,    t4, 'Friday',    time(10, 0), time(12, 0), 'D101'),
        ]
        for subj, teacher, day, start, end, room in timetable_entries:
            TimeTable.objects.get_or_create(
                subject=subj, day=day, start_time=start,
                defaults=dict(teacher=teacher, end_time=end, room=room)
            )

        # ── Exams ──────────────────────────────────────────────────────
        exams_data = [
            (s_algo,   date(2025, 6, 5),  120, 'A101'),
            (s_prog,   date(2025, 6, 7),  90,  'A101'),
            (s_ana,    date(2025, 6, 9),  120, 'B201'),
            (s_alg,    date(2025, 6, 11), 120, 'B201'),
            (s_meca,   date(2025, 6, 13), 90,  'C301'),
            (s_bd,     date(2025, 6, 15), 120, 'A102'),
            (s_reseau, date(2025, 6, 17), 90,  'A102'),
        ]
        exams = []
        for subj, d, dur, room in exams_data:
            exam, _ = Exam.objects.get_or_create(
                subject=subj, date=d,
                defaults=dict(duration=dur, room=room)
            )
            exams.append(exam)

        # ── Notes ──────────────────────────────────────────────────────
        l1_students = [s for s in created_students if s.classe == l1_info]
        l2_students = [s for s in created_students if s.classe == l2_info]

        l1_subjects = [s_algo, s_prog, s_ana, s_alg, s_meca, s_ang]
        scores_l1 = [
            [16, 14, 15, 12, 17, 13],  # Saloua
            [12, 11, 10, 9,  14, 15],  # Karim
            [18, 17, 16, 15, 12, 14],  # Mariam
            [10, 13, 11, 14, 9,  12],  # Omar
        ]
        for student, scores in zip(l1_students, scores_l1):
            for subj, score in zip(l1_subjects, scores):
                Note.objects.get_or_create(
                    student=student, subject=subj,
                    defaults=dict(teacher=subj.teacher, score=score, max_score=20)
                )

        l2_subjects = [s_bd, s_reseau, s_stat]
        scores_l2 = [
            [15, 13, 16],  # Zineb
            [11, 14, 10],  # Amine
            [17, 12, 15],  # Hajar
        ]
        for student, scores in zip(l2_students, scores_l2):
            for subj, score in zip(l2_subjects, scores):
                Note.objects.get_or_create(
                    student=student, subject=subj,
                    defaults=dict(teacher=subj.teacher, score=score, max_score=20)
                )

        self.stdout.write(f'  Created: {Department.objects.count()} departments, '
                          f'{Classe.objects.count()} classes, '
                          f'{Teacher.objects.count()} teachers, '
                          f'{Subject.objects.count()} subjects, '
                          f'{Student.objects.count()} students, '
                          f'{Note.objects.count()} grades')
