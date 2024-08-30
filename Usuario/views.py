
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.shortcuts import redirect



# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirige a la página que desees
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
