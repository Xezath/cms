# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def create_superuser(sender, instance, created, **kwargs):
    if created:
        if not (User.objects.all().count() > 0):
            # Si es el primer usuario, hacerlo administrador}
            group, created = Group.objects.get_or_create(name='Administrador')
            instance.groups.add(group)
            instance.save()
        else:
            # Si no es el primer usuario, asignar rol de suscriptor
            group, created = Group.objects.get_or_create(name='Suscriptor')
            instance.groups.add(group)
            instance.save()