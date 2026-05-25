from django.db import models
from core.models import TimeStampedModel


class Cliente(TimeStampedModel):
    nombres        = models.CharField(max_length=100)
    apellidos      = models.CharField(max_length=100)
    telefono       = models.CharField(max_length=20, blank=True, null=True)
    direccion      = models.CharField(max_length=255, blank=True, null=True)
    correo         = models.EmailField(max_length=150, unique=True, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cliente"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class PersonaAutorizada(TimeStampedModel):
    id_cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE,
        db_column="id_cliente", related_name="personas_autorizadas"
    )
    nombres  = models.CharField(max_length=100)
    dni      = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "persona_autorizada"

    def __str__(self):
        return f"{self.nombres} — DNI: {self.dni}"