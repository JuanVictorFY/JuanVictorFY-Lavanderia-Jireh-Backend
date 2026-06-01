from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate
from apps.pedidos.models import Pedido
from apps.pagos.models import Pago
from apps.clientes.models import Cliente


class ReporteService:

    @staticmethod
    def resumen_por_rango(fecha_inicio: date, fecha_fin: date) -> dict:
        pedidos = Pedido.objects.filter(
            fecha_ingreso__date__range=(fecha_inicio, fecha_fin)
        )
        pagos = Pago.objects.filter(
            fecha_pago__date__range=(fecha_inicio, fecha_fin),
            estado_pago=Pago.PAGADO,
        )
        return {
            "fecha_inicio":        str(fecha_inicio),
            "fecha_fin":           str(fecha_fin),
            "total_pedidos":       pedidos.count(),
            "pedidos_entregados":  pedidos.filter(estado=Pedido.ENTREGADO).count(),
            "pedidos_cancelados":  pedidos.filter(estado=Pedido.CANCELADO).count(),
            "ingresos_totales":    float(pagos.aggregate(t=Sum("monto"))["t"] or 0),
            "ticket_promedio":     float(pagos.aggregate(a=Avg("monto"))["a"] or 0),
            "total_pagos":         pagos.count(),
        }

    @staticmethod
    def clientes_frecuentes(limite: int = 10) -> list:
        return list(
            Pedido.objects
            .values("id_cliente__nombres", "id_cliente__apellidos", "id_cliente__telefono")
            .annotate(total_pedidos=Count("id"))
            .order_by("-total_pedidos")[:limite]
        )

    @staticmethod
    def ingresos_por_dia(dias: int = 30) -> list:
        fecha_inicio = date.today() - timedelta(days=dias - 1)
        qs = (
            Pago.objects
            .filter(fecha_pago__date__gte=fecha_inicio, estado_pago=Pago.PAGADO)
            .annotate(dia=TruncDate("fecha_pago"))
            .values("dia")
            .annotate(total=Sum("monto"))
            .order_by("dia")
        )
        mapa = {r["dia"]: float(r["total"]) for r in qs}
        resultado = []
        for i in range(dias):
            d = fecha_inicio + timedelta(days=i)
            resultado.append({"fecha": str(d), "total": mapa.get(d, 0.0)})
        return resultado
