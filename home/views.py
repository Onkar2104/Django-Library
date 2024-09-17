from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import *
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

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
        first_name = "Guest", 
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

        subject = "Welcome to Bit Library! 📚"
        message = f"Hello {first_name},\n\nWelcome to BIT Library! We're glad to have you.\n\nAbout Bit Library: Bit Library is more than just a collection of books; it’s a gateway to knowledge, inspiration, and connection.\n\nOnline Access: Can’t make it to the physical library? No worries! Our online catalog is accessible 24/7.\n\nHappy reading, {first_name}! 📖\n\nWarm regards,\n\nJSPM's Bit Library."
        
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Account created successfully! A welcome email has been sent.")
        except Exception as e:
            messages.warning(request, "Account created successfully, but email failed to send.")



        messages.success(request, "Account created successfully!")
        return redirect('/login/')

    return render(request, 'register.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "if an account exists with the email you entered. You should receive them shortly." \
    
    success_url = reverse_lazy('login_page')