from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def cat(request):
    return render(request, 'paginas/index.html')