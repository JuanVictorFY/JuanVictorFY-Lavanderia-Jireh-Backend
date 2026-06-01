from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


AZUL_MARCA  = colors.HexColor("#1A73E8")
GRIS_CLARO  = colors.HexColor("#F5F5F5")
GRIS_BORDE  = colors.HexColor("#DADADA")


def _estilo_titulo():
    return ParagraphStyle(
        "titulo",
        fontSize=18,
        textColor=AZUL_MARCA,
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName="Helvetica-Bold",
    )


def _estilo_subtitulo():
    return ParagraphStyle(
        "subtitulo",
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=12,
    )


def _estilo_etiqueta():
    return ParagraphStyle(
        "etiqueta",
        fontSize=9,
        textColor=colors.grey,
        fontName="Helvetica",
    )


def _estilo_valor():
    return ParagraphStyle(
        "valor",
        fontSize=10,
        textColor=colors.black,
        fontName="Helvetica-Bold",
    )


def _tabla_info(datos):
    tabla = Table(datos, colWidths=[5 * cm, 10 * cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GRIS_CLARO),
        ("GRID",       (0, 0), (-1, -1), 0.5, GRIS_BORDE),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",    (0, 0), (-1, -1), 6),
    ]))
    return tabla


def generar_buffer_recibo(pedido) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles   = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Lavanderia Jireh", _estilo_titulo()))
    elementos.append(Paragraph("Recibo de Servicio", _estilo_subtitulo()))
    elementos.append(Spacer(1, 0.3 * cm))

    info_pedido = [
        ["Codigo",       pedido.codigo],
        ["Cliente",      str(pedido.id_cliente)],
        ["Empleado",     str(pedido.id_empleado)],
        ["Fecha",        pedido.fecha_ingreso.strftime("%d/%m/%Y %H:%M")],
        ["Estado",       pedido.get_estado_display()],
        ["Total",        f"S/ {pedido.total:.2f}"],
    ]
    elementos.append(_tabla_info(info_pedido))
    elementos.append(Spacer(1, 0.5 * cm))

    prendas_data = [["Prenda", "Color", "Cantidad", "Peso (kg)"]]
    for prenda in pedido.prendas.all():
        prendas_data.append([
            prenda.tipo_prenda,
            prenda.color or "—",
            str(prenda.cantidad),
            f"{prenda.peso:.2f}",
        ])

    if len(prendas_data) > 1:
        tabla_prendas = Table(prendas_data, colWidths=[7 * cm, 4 * cm, 3 * cm, 3 * cm])
        tabla_prendas.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), AZUL_MARCA),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID",       (0, 0), (-1, -1), 0.5, GRIS_BORDE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS_CLARO]),
            ("PADDING",    (0, 0), (-1, -1), 6),
        ]))
        elementos.append(Paragraph("Prendas", styles["Heading3"]))
        elementos.append(tabla_prendas)

    doc.build(elementos)
    buffer.seek(0)
    return buffer
