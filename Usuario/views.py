
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,Group
from .forms import CustomUserCreationForm, CustomAdminUserChangeForm, GroupForm, GroupEditForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

# Create your views here.
def home(request):
    """
    Renderiza la página de inicio.
    """
    # Renderiza la página de inicio
    # La función 'render' toma el objeto 'request' y la plantilla 'home.html' para generar la respuesta HTTP.
    return render(request, 'home.html')


def exito(request):
    """
    Renderiza la página de éxito, que podría mostrar un mensaje 
    después de que el usuario complete una acción como el registro o el inicio de sesión.
    """
    # Renderiza la página de éxito, que podría mostrar un mensaje de éxito
    # después de que el usuario complete una acción como el registro o el inicio de sesión.
    return render(request, 'exito.html')


def cerrar_sesion(request):
    """
    Cierra la sesión del usuario actual y redirige a la página de inicio.
    """
    # Cierra la sesión del usuario actual utilizando la función 'logout'.
    # Luego redirige a la página de inicio.
    logout(request)
    return redirect ('home')


def Iniciar_Sesion(request):
    """
    Maneja el proceso de inicio de sesión. 
    Si la solicitud es GET, se muestra el formulario de inicio de sesión; 
    si es POST, se intenta autenticar al usuario.
    """
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
    """
    Maneja el registro de nuevos usuarios. 
    Si la solicitud es POST, procesa el formulario de registro.
    """
    # Maneja el registro de nuevos usuarios
    # Si la solicitud es POST, procesa el formulario de registro con los datos proporcionados.
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            # Si el formulario es válido, guarda el nuevo usuario en la base de datos.
            #print("Datos recibidos (POST):", request.POST)  # Muestra los datos del formulario recibidos en la solicitud POST.
            user=form.save()

            # Comprobar si este es el primer usuario registrado
            if User.objects.count() == 1:
                # Asignar el grupo "Administrador" si es el primer usuario
                admin_group, created = Group.objects.get_or_create(name='Administrador')
                user.groups.add(admin_group)
            else:
                # Asignar el grupo "Suscriptor" a los demás usuarios
                suscriptor_group, created = Group.objects.get_or_create(name='Suscriptor')
                user.groups.add(suscriptor_group)
                
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            #print("Datos validados y limpios:", form.cleaned_data)  # Muestra los datos validados y limpios del formulario.
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
        #print("Datos recibidos (GET):", request.GET) # Muestra los datos recibidos en la solicitud GET, aunque no deberían haber datos en GET para el registro.
    
    # Renderiza la plantilla del formulario de registro con el formulario en el contexto.
    return render(request, 'registrar.html', {'form': form})

@permission_required('auth.add_group',raise_exception=True)
def crear_rol(request):
    """
    Crea un nuevo rol (grupo) si la solicitud es POST.
    Renderiza el formulario para crear un rol si la solicitud es GET.
    """
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles_listar')
    else:
        form = GroupForm()
    return render(request, 'crear_rol.html', {'form': form})

@permission_required('auth.change_group',raise_exception=True)
def editar_rol(request, pk):
    """
    Edita un rol (grupo) existente. 
    Si la solicitud es POST, actualiza el grupo con los datos del formulario.
    """
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupEditForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('roles_listar')
    else:
        form = GroupEditForm(instance=group)
    return render(request, 'editar_rol.html', {'form': form})

@permission_required('auth.delete_group',raise_exception=True)
def eliminar_rol(request, pk):
    """
    Elimina un rol (grupo) existente. 
    Si la solicitud es POST, elimina el grupo.
    """
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('roles_listar')
    return render(request, 'eliminar_rol.html', {'group': group})

@permission_required('auth.view_group',raise_exception=True)
def roles_listar(request):
    """
    Lista todos los roles (grupos) existentes.
    """
    roles = Group.objects.all()
    return render(request, 'roles_listar.html', {'roles': roles})

@permission_required('auth.view_user',raise_exception=True)
def ver_usuarios(request):
    """
    Muestra una lista de todos los usuarios registrados.
    """
    usuarios = User.objects.all()
    return render(request, 'ver_usuarios.html', {'usuarios': usuarios})

@permission_required('auth.view_group',raise_exception=True)
def ver_roles(request):
    """
    Muestra una lista de todos los roles (grupos) existentes.
    """
    roles = Group.objects.all()
    return render(request, 'ver_roles.html', {'roles': roles})

@permission_required('auth.view_user',raise_exception=True)
def lista_usuarios(request):
    """
    Obtiene todos los usuarios registrados y los muestra en una lista.
    """
    # Obtener todos los usuarios registrados
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

# Nueva vista para editar los roles de un usuario
@permission_required('auth.change_user',raise_exception=True)
def cambiar_rol_usuario(request, pk):
    """
    Cambia el rol (grupo) de un usuario existente. 
    Si la solicitud es POST, actualiza los grupos del usuario.
    """
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomAdminUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()  # Guardar los cambios del rol
            return redirect('lista_usuarios')  # Redirigir de nuevo a la lista de usuarios
    else:
        form = CustomAdminUserChangeForm(instance=usuario)
    return render(request, 'cambiar_rol_usuario.html', {'form': form, 'usuario': usuario})

# Nueva vista para eliminar un usuario
@permission_required('auth.delete_user',raise_exception=True)
def eliminar_usuario(request, pk):
    """
    Elimina un usuario existente. 
    Si la solicitud es POST, se elimina el usuario.
    """
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()  # Eliminar el usuario
        return redirect('lista_usuarios')  # Redirigir a la lista de usuarios
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})

