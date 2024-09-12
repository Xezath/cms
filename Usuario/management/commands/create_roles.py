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
            'Suscriptor': ['add_categoria', 'change_categoria', 'delete_categoria'],
            'Autor': ['add_contenidos', 'change_contenidos', 'delete_contenidos'],  # Permisos CRUD para Contenido
            'Editor': ['add_contenidos', 'change_contenidos', 'delete_contenidos', 'change_categoria'],
            'Publicador': ['add_contenidos', 'change_contenidos', 'delete_contenidos', 'change_categoria'],
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

        self.stdout.write(self.style.SUCCESS('Roles y permisos asignados correctamente.'))
