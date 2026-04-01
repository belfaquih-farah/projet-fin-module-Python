import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from home_auth.models import CustomUser

users = [
    {'username': 'ikram@admin.com', 'email': 'ikram@admin.com', 'password': '12345', 'first_name': 'Ikram', 'last_name': 'Admin', 'is_admin': True, 'is_staff': True, 'is_superuser': True},
    {'username': 'test@prof.com', 'email': 'test@prof.com', 'password': '12345', 'first_name': 'Test', 'last_name': 'Prof', 'is_teacher': True},
    {'username': 'test@student.com', 'email': 'test@student.com', 'password': '12345', 'first_name': 'Test', 'last_name': 'Student', 'is_student': True},
]

for u in users:
    if CustomUser.objects.filter(email=u['email']).exists():
        print(f'[SKIP] {u["email"]}')
        continue
    CustomUser.objects.create_user(**u)
    print(f'[OK] {u["email"]}')
