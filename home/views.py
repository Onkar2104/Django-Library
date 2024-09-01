from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home_page(request):
    context={'page':'BIT'}
    return render(request, 'homee/index.html', context)