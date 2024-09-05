
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect

# Create your views here.
def home(request):
    # Renderiza la página de inicio
    # La función 'render' toma el objeto 'request' y la plantilla 'home.html' para generar la respuesta HTTP.
    return render(request, 'home.html')

    
def exito(request):
    # Renderiza la página de éxito, que podría mostrar un mensaje de éxito
    # después de que el usuario complete una acción como el registro o el inicio de sesión.
    return render(request, 'exito.html')


def cerrar_sesion(request):
    # Cierra la sesión del usuario actual utilizando la función 'logout'.
    # Luego redirige a la página de inicio.
    logout(request)
    return redirect ('home')


def Iniciar_Sesion(request):
    # Maneja el proceso de inicio de sesión.
    # Si la solicitud es GET, se muestra el formulario de inicio de sesión.
    # Si la solicitud es POST, se intenta autenticar al usuario con las credenciales proporcionadas.
    if request.method == 'GET':
        # Si la solicitud es GET, se muestra el formulario de inicio de sesión.
        # Si la solicitud es POST, se intenta autenticar al usuario con las credenciales proporcionadas.
        return render(request, 'Iniciar_Sesion.html',{
            'form': AuthenticationForm  # Crea una instancia del formulario de autenticación
        })
    else:
        # Si la solicitud es POST, intenta autenticar al usuario con el nombre de usuario y la contraseña recibidos.
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is None:
            # Si la autenticación falla, se renderiza de nuevo el formulario con un mensaje de error.
            return render(request, 'Iniciar_Sesion.html',{
                'form': AuthenticationForm, # Vuelve a crear una instancia del formulario
                'error': 'Username or password is incorrect'    # Mensaje de error que se mostrará al usuario.
            })
        else:
            # Si la autenticación es exitosa, se inicia la sesión del usuario.
            # Luego se redirige a la página de inicio.
            login(request, user)
            return redirect ('home')

     

def registrar(request):
    # Maneja el registro de nuevos usuarios
    # Si la solicitud es POST, procesa el formulario de registro con los datos proporcionados.
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            # Si el formulario es válido, guarda el nuevo usuario en la base de datos.
            print("Datos recibidos (POST):", request.POST)  # Muestra los datos del formulario recibidos en la solicitud POST.
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            print("Datos validados y limpios:", form.cleaned_data)  # Muestra los datos validados y limpios del formulario.
            user = authenticate(username=username, password=password, email=email) # Autentica al usuario
            login(request, user)    # Inicia sesión automáticamente al usuario recién registrado.

            # Redirige al usuario a la página de éxito después del registro.
            return redirect('exito')  
        else:
            # Si el formulario no es válido, se muestran los errores en la consola para depuración.
            print("Errores de formulario:", form.errors)  
        
    else:
        # Si la solicitud es GET, se renderiza un formulario vacío para el registro.
        form = CustomUserCreationForm()
        print("Datos recibidos (GET):", request.GET) # Muestra los datos recibidos en la solicitud GET, aunque no deberían haber datos en GET para el registro.
    
    # Renderiza la plantilla del formulario de registro con el formulario en el contexto.
    return render(request, 'registrar.html', {'form': form})
