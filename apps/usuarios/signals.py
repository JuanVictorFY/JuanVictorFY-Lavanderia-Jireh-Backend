from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Empleado


@receiver(post_save, sender=Empleado)
def log_cambio_estado_empleado(sender, instance, created, **kwargs):
    if not created:
        estado_str = "activado" if instance.estado else "desactivado"
        print(f"[INFO] Empleado {instance.nombres} {instance.apellidos} fue {estado_str}.")
