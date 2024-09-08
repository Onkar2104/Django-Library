from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

def home_page(request):
    context={'page':'BIT'}
    return render(request, 'homee/index.html', context)

@login_required(login_url="/login/")
def books(request):
    return render(request, 'homee/BookSec.html')

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
                return redirect('/books/')

        return render(request, 'login_page.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')   

@login_required(login_url="/login/")
def profile_view(request):
    if request.method == "POST":
        data = request.POST
        full_name = data.get('full_name')
        email = data.get('email')
        phone = data.get('phone')
        educationType = data.get('educationType')
        branch = data.get('branch')
        pursuing_year = data.get('pursuingYear')
        # books_obtained = data.get('booksObtained')

        try:
            user = User.objects.get(email=request.user.email)
            user.full_name = full_name
            user.phone = phone
            user.educationType = educationType
            user.branch = branch
            user.pursuing_year = pursuing_year
            # user.books_obtained = books_obtained

            # # Update password if provided
            # if new_password:
            #     user.set_password(new_password)
            
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        
        except User.DoesNotExist:
            messages.error(request, "User not found!")

    return render(request, 'homee/profile.html', {'user': request.user})

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

        messages.success(request, "Account created successfully!")
        return redirect('/login/')

    return render(request, 'register.html')
