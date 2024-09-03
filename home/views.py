from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home_page(request):
    context={'page':'BIT'}
    return render(request, 'homee/index.html', context)

def login_page(request):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not User.objects.filter(email = email).exists():
                messages.info(request, "Invalid email..!")
                return redirect('homee/login_page/')
            
            user = authenticate(email = email, password = password)

            if user is None:
                messages.info(request, "Invalid passward..!")
                return redirect('homee/login_page/')
            else:
                login(request, user)
                return redirect('/home_page/')

        return render(request, 'homee/login_page.html')

def logout_page(request):
    logout(request)
    return redirect('homee/login_page/')   