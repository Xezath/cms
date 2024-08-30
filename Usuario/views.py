
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.shortcuts import redirect


# Create your views here.
def home(request):
   return render(request, 'home.html')

def exito(request):
    return render(request, 'exito.html')

def registrar(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("Datos recibidos (POST):", request.POST)  # Ver datos enviados en POST
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print("Datos validados y limpios:", form.cleaned_data)  # Ver datos limpios
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('exito')  # Redirige a la página que desees
        else:
            print("Errores de formulario:", form.errors)  # Ver errores de validación   
        
    else:
        form = CustomUserCreationForm()
        print("Datos recibidos (GET):", request.GET)  # Ver datos enviados en GET
    return render(request, 'registrar.html', {'form': form})
