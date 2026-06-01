from rest_framework import serializers


class ResumenDiarioSerializer(serializers.Serializer):
    fecha         = serializers.DateField()
    total_pedidos = serializers.IntegerField()
    total_pagos   = serializers.DecimalField(max_digits=12, decimal_places=2)
    pedidos_entregados = serializers.IntegerField()


class TopServicioSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    count  = serializers.IntegerField()


class EstadoPedidoResumenSerializer(serializers.Serializer):
    estado = serializers.CharField()
    count  = serializers.IntegerField()


class ResumenGeneralSerializer(serializers.Serializer):
    pedidos_hoy    = serializers.IntegerField()
    ingresos_hoy   = serializers.FloatField()
    pedidos_mes    = serializers.IntegerField()
    clientes_total = serializers.IntegerField()
