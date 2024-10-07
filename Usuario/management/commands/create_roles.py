from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Carga datos iniciales de Usuarios, Grupos, Categorías y Contenidos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos iniciales...')

        # Obtener permisos
        permisos = Permission.objects.all()
        
        administracion, created = Group.objects.get_or_create(name='Administrador')
        for permiso in permisos:
            administracion.permissions.add(permiso)

        roles = {
            'Suscriptor': ['view_contenidos'],
            'Autor': ['add_contenidos', 'view_tablero', 'ver_propio_tablero', 'view_columna','change_contenidos', 'delete_contenidos'],  
            'Editor': ['change_contenidos', 'change_categoria'],
            'Publicador': ['can_viewInactive','delete_contenidos', 'change_subcategoria','cambiar_estado_tarjeta','can_viewBorrador','can_change_estado'],
        }

        # Crea o obtiene los grupos y asigna permisos
        for role_name, permissions in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            for perm_code in permissions:
                try:
                    # Obtener el permiso
                    perm = Permission.objects.get(codename=perm_code)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permiso no encontrado: {perm_code}'))

        # Herencia de permisos
        autor = Group.objects.get(name='Autor')
        suscriptor = Group.objects.get(name='Suscriptor')
        editor = Group.objects.get(name='Editor')
        publicador = Group.objects.get(name='Publicador')

        # Asignar permisos del Suscriptor al Autor
        autor.permissions.add(*suscriptor.permissions.all())
        
        # Asignar permisos del Autor al Editor
        editor.permissions.add(*autor.permissions.all())
        
        # Asignar permisos del Editor al Publicador
        publicador.permissions.add(*editor.permissions.all())

        self.stdout.write(self.style.SUCCESS('Roles y permisos asignados correctamente.'))
