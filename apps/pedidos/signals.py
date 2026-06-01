from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido, EstadoPedido


@receiver(post_save, sender=Pedido)
def crear_estado_inicial(sender, instance, created, **kwargs):
    if created:
        EstadoPedido.objects.create(
            id_pedido=instance,
            estado=Pedido.PENDIENTE,
            descripcion="Pedido ingresado al sistema.",
        )
