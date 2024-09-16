from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import *
from django.core.mail import send_mail, EmailMessage

# Create your views here.

User = get_user_model()

def home_page(request):
    context={'page':'BIT'}
    return render(request, 'homee/index.html', context)

@login_required(login_url="/login/")
def books(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
    else:
        first_name = "Guest",  # Or some default value
        last_name = "guest"
    
    context = {
        'first_name': first_name,
        'last_name': last_name
    }
    return render(request, 'homee/BookSec.html', context)

def login_page(request):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not User.objects.filter(email = email).exists():
                messages.info(request, "Invalid email..!")
                return redirect('/login/')
            
            user = authenticate(email = email, password = password)

            if user is None:
                messages.info(request, "Invalid passward..!")
                return redirect('/login/')
            else:
                login(request, user)
                return redirect('/')

        return render(request, 'login_page.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')   

def register(request):
    # User = get_user_model()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email:
            messages.error(request, "Email is required.")
            return redirect('/register/')

        if password and confirm_password and password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register/')
        
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, "Password does not meet the requirements: " + "; ".join(e.messages))
            return redirect('/register/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('/register/')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        subject = "Welcome to BIT Library"
        message = f"Hello {first_name},\n\nWelcome to BIT Library! We're glad to have you."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]  # Make sure recipient_list is a list

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Account created successfully! A welcome email has been sent.")
        except Exception as e:
            messages.warning(request, "Account created successfully, but email failed to send.")



        messages.success(request, "Account created successfully!")
        return redirect('/login/')

    return render(request, 'register.html')

