from io import BytesIO
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


VERDE_EXITO = colors.HexColor("#2E7D32")
GRIS_CLARO  = colors.HexColor("#F5F5F5")


def generar_comprobante_pago(pago) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A5,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )
    styles   = getSampleStyleSheet()
    elementos = []

    titulo_style = styles["Title"]
    titulo_style.textColor = VERDE_EXITO
    titulo_style.alignment = TA_CENTER

    elementos.append(Paragraph("Comprobante de Pago", titulo_style))
    elementos.append(Paragraph("Lavanderia Jireh", styles["Normal"]))
    elementos.append(Spacer(1, 0.5 * cm))

    datos = [
        ["N° Pago",       f"#{pago.id}"],
        ["Pedido",        pago.id_pedido.codigo],
        ["Cliente",       str(pago.id_pedido.id_cliente)],
        ["Monto",         f"S/ {pago.monto:.2f}"],
        ["Metodo",        pago.get_metodo_pago_display()],
        ["Estado",        pago.get_estado_pago_display()],
        ["Fecha",         pago.fecha_pago.strftime("%d/%m/%Y %H:%M")],
    ]

    tabla = Table(datos, colWidths=[4 * cm, 8 * cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GRIS_CLARO),
        ("GRID",       (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING",    (0, 0), (-1, -1), 5),
        ("FONTNAME",   (0, 0), (0, -1), "Helvetica-Bold"),
    ]))
    elementos.append(tabla)

    doc.build(elementos)
    buffer.seek(0)
    return buffer
