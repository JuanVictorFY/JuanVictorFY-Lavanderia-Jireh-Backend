from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cliente


@receiver(post_save, sender=Cliente)
def log_cliente_creado(sender, instance, created, **kwargs):
    if created:
        print(f"[INFO] Nuevo cliente registrado: {instance.nombres} {instance.apellidos}")
