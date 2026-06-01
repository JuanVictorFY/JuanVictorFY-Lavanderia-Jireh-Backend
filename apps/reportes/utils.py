from datetime import date, timedelta


def rango_semana_actual():
    hoy   = date.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    return lunes, hoy


def rango_mes_actual():
    hoy   = date.today()
    inicio = hoy.replace(day=1)
    return inicio, hoy


def rango_anio_actual():
    hoy    = date.today()
    inicio = hoy.replace(month=1, day=1)
    return inicio, hoy


def porcentaje_cambio(valor_actual: float, valor_anterior: float) -> float:
    if valor_anterior == 0:
        return 100.0 if valor_actual > 0 else 0.0
    return round(((valor_actual - valor_anterior) / valor_anterior) * 100, 2)
