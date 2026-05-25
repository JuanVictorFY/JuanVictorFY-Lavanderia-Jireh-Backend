from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel


class Rol(TimeStampedModel):
    nombre_rol = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "rol"
        ordering = ["nombre_rol"]

    def __str__(self):
        return self.nombre_rol


class Empleado(TimeStampedModel):
    user      = models.OneToOneField(User, on_delete=models.CASCADE, related_name="empleado")
    id_rol    = models.ForeignKey(Rol, on_delete=models.RESTRICT, db_column="id_rol")
    nombres   = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono  = models.CharField(max_length=20, blank=True, null=True)
    estado    = models.BooleanField(default=True)

    class Meta:
        db_table = "empleado"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"