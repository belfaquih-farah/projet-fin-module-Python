from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

TEST_USERS = [
    {
        'username': 'admin@school.com',
        'email': 'admin@school.com',
        'password': 'Admin1234!',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_admin': True,
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'username': 'teacher@school.com',
        'email': 'teacher@school.com',
        'password': 'Teacher1234!',
        'first_name': 'John',
        'last_name': 'Teacher',
        'is_teacher': True,
    },
    {
        'username': 'student@school.com',
        'email': 'student@school.com',
        'password': 'Student1234!',
        'first_name': 'Jane',
        'last_name': 'Student',
        'is_student': True,
    },
]


class Command(BaseCommand):
    help = 'Create test accounts for admin, teacher, and student roles'

    def handle(self, *args, **kwargs):
        for data in TEST_USERS:
            email = data['email']
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'  [SKIP] {email} already exists'))
                continue

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_admin=data.get('is_admin', False),
                is_teacher=data.get('is_teacher', False),
                is_student=data.get('is_student', False),
                is_staff=data.get('is_staff', False),
                is_superuser=data.get('is_superuser', False),
            )
            self.stdout.write(self.style.SUCCESS(f'  [OK]   {email} created'))

        self.stdout.write(self.style.SUCCESS('\nTest accounts ready:'))
        self.stdout.write('  admin@school.com   / Admin1234!   (admin + superuser)')
        self.stdout.write('  teacher@school.com / Teacher1234! (teacher)')
        self.stdout.write('  student@school.com / Student1234! (student)')
