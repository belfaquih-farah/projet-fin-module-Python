from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, PasswordResetRequest

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role') # student, teacher ou admin

        # Créer l'utilisateur
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )   
        
        # Assigner le rôle
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('index')
        
    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            # Redirection selon le rôle
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            # Create a password reset request
            reset_request = PasswordResetRequest.objects.create(
                user=user,
                email=email
            )
            # Print reset link to console (no email server)
            reset_link = f"http://localhost:8000/authentication/reset-password/{reset_request.token}/"
            print(f"\n{'='*60}")
            print(f"Password Reset Link for {email}:")
            print(f"{reset_link}")
            print(f"{'='*60}\n")
            
            messages.success(request, 'If this email exists, a reset link has been generated. Check console or email.')
            return redirect('login')
        except CustomUser.DoesNotExist:
            # For security, don't reveal if email exists
            messages.success(request, 'If this email exists, a reset link has been generated. Check console or email.')
            return redirect('login')
    
    return render(request, 'authentication/forgot-password.html')

def reset_password_view(request, token):
    try:
        reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('login')
    
    if not reset_request.is_valid():
        messages.error(request, 'This reset link has expired.')
        return redirect('login')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/reset_password.html')
        
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'authentication/reset_password.html')
        
        # Set new password
        user = reset_request.user
        user.set_password(new_password)
        user.save()
        
        # Delete the reset request after use
        reset_request.delete()
        
        messages.success(request, 'Password has been reset successfully. Please login with your new password.')
        return redirect('login')
    
    return render(request, 'authentication/reset_password.html')