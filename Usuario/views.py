
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login,logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,Group
from .forms import GroupForm, GroupEditForm

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

            # Obtener el nombre del rol del usuario
            user_groups = user.groups.all()
            user_roles = [group.name for group in user_groups]
            request.session['roles'] = user_roles  # Guardar roles en la sesión
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


# usuarios/views.py
def crear_rol(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles_listar')
    else:
        form = GroupForm()
    return render(request, 'crear_rol.html', {'form': form})

def editar_rol(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupEditForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('roles_listar')
    else:
        form = GroupEditForm(instance=group)
    return render(request, 'editar_rol.html', {'form': form})

def eliminar_rol(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('roles_listar')
    return render(request, 'eliminar_rol.html', {'group': group})

def roles_listar(request):
    roles = Group.objects.all()
    return render(request, 'roles_listar.html', {'roles': roles})

def ver_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'ver_usuarios.html', {'usuarios': usuarios})

def ver_roles(request):
    roles = Group.objects.all()
    return render(request, 'ver_roles.html', {'roles': roles})


def lista_usuarios(request):
    # Obtener todos los usuarios registrados
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})


