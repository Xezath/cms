from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def cat(request):
    return HttpResponse("<h1>Categoria<!h1>")