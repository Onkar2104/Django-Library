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
from .models import StudentProfile

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




@login_required(login_url="/login/")
def student_info(request):
    user = request.user

    student_profile, created = StudentProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        student_image = request.FILES.get('student_image')
        phone = request.POST.get('phone')
        education_type = request.POST.get('education_type')
        select_branch = request.POST.get('select_branch')
        pursuing_year = request.POST.get('pursuing_year')
        books_obtained = request.POST.get('books_obtained')

        student_profile.full_name = full_name
        if student_image:
            student_profile.student_image = student_image
        student_profile.phone = phone
        student_profile.education_type = education_type
        student_profile.select_branch = select_branch
        student_profile.pursuing_year = pursuing_year
        student_profile.books_obtained = books_obtained

        student_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('/profile/') 

    context = {
        'full_name': student_profile.full_name,
        'email': user.email,  
        'phone': student_profile.phone,
        'education_type': student_profile.education_type,
        'select_branch': student_profile.select_branch,
        'pursuing_year': student_profile.pursuing_year,
        'books_obtained': student_profile.books_obtained,
        'student_image': student_profile.student_image.url if student_profile.student_image else None,
    }
    

    return render(request, 'homee/profile.html', context)


@login_required(login_url="/login/")
def my_profile(request):

#     if request.user.is_authenticated:
#         full_name = request.student_profile.full_name
#         phone = request.student_profile.phone
#         student_image = request.student_profile.student_image
#         education_type = request.student_profile.education_type
#         select_branch = request.student_profile.select_branch
#         pursuing_year = request.student_profile.pursuing_year
#         books_obtained = request.student_profile.books_obtained

    
#     context = {
#         'full_name': full_name,
#         'phone': phone,
#         'student_image':student_image,
#         'education_type':education_type,
#         'select_branch' : select_branch,
#         'pursuing_year': pursuing_year,
#         'books_obtained': books_obtained
#     }
     return render(request, 'homee/myProfile.html')




class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "if an account exists with the email you entered. You should receive them shortly." \
    
    success_url = reverse_lazy('login_page')