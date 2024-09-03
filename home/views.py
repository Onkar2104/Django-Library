from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
# Create your views here.

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
                return redirect('/home_page/')

        return render(request, 'homee/login_page.html')

def logout_page(request):
    logout(request)
    return redirect('homee/login_page/')   

def register(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        
    
        user = User.objects.filter(email = email)
        try:
            validate_password(password)
        except ValidationError as e:
            messages.info(request, "Use some strong password..!")
            return redirect('/register/')

        if user.exists():
            messages.info(request, "Already used Email..!")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully..!")

        return redirect('/login_page/')

    return render(request, 'homee/register.html/')