from datetime import datetime
from decimal import Decimal


def calcular_total_pedido(prendas):
    total = Decimal("0.00")
    for prenda in prendas:
        for detalle in prenda.detalles.all():
            total += detalle.subtotal
    return total


def formatear_fecha_peru(dt: datetime) -> str:
    if not dt:
        return ""
    return dt.strftime("%d/%m/%Y %H:%M")


def generar_codigo_recibo(pedido_id: int) -> str:
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"REC-{timestamp}-{pedido_id:04d}"


def calcular_igv(monto: Decimal, porcentaje: float = 18.0) -> Decimal:
    return (monto * Decimal(str(porcentaje / 100))).quantize(Decimal("0.01"))
