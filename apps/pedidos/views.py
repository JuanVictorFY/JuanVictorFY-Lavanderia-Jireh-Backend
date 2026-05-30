import io
import html as _html

from django.http import HttpResponse
from django.utils import timezone

from reportlab.graphics.shapes import Circle, Drawing, Rect
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable, Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.permissions import EsEmpleadoActivo, EsAdministradorORecepcionista
from core.exceptions import RecursoNoEncontradoError
from .models import Pedido
from .serializers import PedidoSerializer, CrearPedidoSerializer, EstadoPedidoSerializer
from .services import PedidoService

# ── Paleta ────────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A5

TEAL       = colors.HexColor("#0891B2")
TEAL_DARK  = colors.HexColor("#0E7490")
TEAL_BG    = colors.HexColor("#E0F7FA")
TEAL_LIGHT = colors.HexColor("#BAE6FD")
VERDE      = colors.HexColor("#059669")
GRIS       = colors.HexColor("#64748B")
GRIS_BG    = colors.HexColor("#F8FAFC")
GRIS_BORDE = colors.HexColor("#E2E8F0")
NEGRO      = colors.HexColor("#0F172A")
BLANCO     = colors.white

ESTADO_MAP = {
    "pendiente":  "Pendiente",
    "en_proceso": "En Proceso",
    "listo":      "Listo para entrega",
    "entregado":  "Entregado",
    "cancelado":  "Cancelado",
}
ESTADO_COLOR = {
    "pendiente":  colors.HexColor("#D97706"),
    "en_proceso": TEAL,
    "listo":      VERDE,
    "entregado":  VERDE,
    "cancelado":  colors.HexColor("#DC2626"),
}
SVC_COLOR_MAP = {
    "lavado":    colors.HexColor("#0891B2"),
    "secado":    colors.HexColor("#F59E0B"),
    "planchado": colors.HexColor("#8B5CF6"),
    "doblado":   colors.HexColor("#059669"),
}

_STYLES = getSampleStyleSheet()
_TS     = TableStyle


# ── Helpers de texto ──────────────────────────────────────────────────────────
def _fmt_date(dt):
    if not dt:
        return "—"
    return timezone.localtime(dt).strftime("%d/%m/%Y %H:%M")


def _P(text, fs=9, fn="Helvetica", color=None, align=TA_LEFT, bold=False):
    font = (fn + "-Bold") if bold else fn
    return Paragraph(text, ParagraphStyle(
        "_p", parent=_STYLES["Normal"],
        fontSize=fs, fontName=font,
        textColor=color or NEGRO, alignment=align,
        leading=fs * 1.45,
    ))


def _lbl(text):
    return _P(_html.escape(text), fs=7, bold=True, color=GRIS)


def _val(text, color=None, fs=8.5, align=TA_LEFT):
    return _P(_html.escape(str(text)), fs=fs, color=color or NEGRO, align=align)


# ── Logo circular ─────────────────────────────────────────────────────────────
def _logo(size: int = 48) -> Drawing:
    """Círculo teal con cuerpo de lavadora, burbujas y hoja."""
    d = Drawing(size, size)
    s = size / 48

    # Fondo circular
    d.add(Circle(24 * s, 24 * s, 24 * s, fillColor=TEAL, strokeColor=None))
    # Cuerpo lavadora (blanco)
    d.add(Rect(6 * s, 3 * s, 36 * s, 30 * s, rx=3 * s, ry=3 * s,
               fillColor=BLANCO, strokeColor=None))
    # Panel de control (teal claro, arriba)
    d.add(Rect(6 * s, 29 * s, 36 * s, 4 * s, rx=0, ry=0,
               fillColor=TEAL_LIGHT, strokeColor=None))
    # Tambor exterior
    d.add(Circle(24 * s, 17 * s, 11 * s,
                 fillColor=TEAL_BG, strokeColor=TEAL, strokeWidth=2 * s))
    # Tambor interior (ojo)
    d.add(Circle(24 * s, 17 * s, 4 * s, fillColor=TEAL, strokeColor=None))
    # Burbujas (blancas, esquina superior izquierda del logo)
    d.add(Circle(9 * s, 40 * s, 3 * s, fillColor=BLANCO, strokeColor=None))
    d.add(Circle(15 * s, 44 * s, 2 * s, fillColor=BLANCO, strokeColor=None))
    # Hoja (verde, esquina superior derecha)
    d.add(Circle(39 * s, 41 * s, 4 * s, fillColor=VERDE, strokeColor=None))
    d.add(Circle(43 * s, 37 * s, 3 * s, fillColor=VERDE, strokeColor=None))

    return d


# ── Indicador de servicio (punto de color) ────────────────────────────────────
def _svc_dot(nombre: str) -> Drawing:
    n = nombre.lower()
    col = next((c for k, c in SVC_COLOR_MAP.items() if k in n), TEAL)
    d = Drawing(9, 9)
    d.add(Circle(4.5, 4.5, 4.5, fillColor=col, strokeColor=None))
    return d


# ── QR code ───────────────────────────────────────────────────────────────────
def _qr_image(data: str, size_pt: float):
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1, box_size=10, border=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img_pil = qr.make_image(fill_color="#0F172A", back_color="white")
        buf = io.BytesIO()
        img_pil.save(buf, format="PNG")
        buf.seek(0)
        return Image(buf, width=size_pt, height=size_pt)
    except ImportError:
        d = Drawing(size_pt, size_pt)
        d.add(Rect(0, 0, size_pt, size_pt,
                   fillColor=GRIS_BG, strokeColor=GRIS_BORDE, strokeWidth=1))
        return d


# ── Fondo de página ───────────────────────────────────────────────────────────
def _draw_bg(canvas, doc):
    """Fondo blanco + fila de diamantes teal en el borde superior."""
    canvas.saveState()
    canvas.setFillColor(BLANCO)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    dot_cols = [TEAL, colors.HexColor("#22D3EE"), TEAL_LIGHT]
    x  = 4 * mm
    y  = PAGE_H - 5 * mm
    sz = 2.5
    i  = 0
    while x < PAGE_W - 4 * mm:
        canvas.setFillColor(dot_cols[i % 3])
        canvas.saveState()
        canvas.translate(x + sz, y + sz)
        canvas.rotate(45)
        canvas.rect(-sz, -sz, sz * 2, sz * 2, fill=1, stroke=0)
        canvas.restoreState()
        x += sz * 3.8
        i += 1

    canvas.restoreState()


# ── ViewSet ───────────────────────────────────────────────────────────────────
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related(
        "id_cliente", "id_empleado"
    ).prefetch_related("prendas", "estados").all()
    permission_classes = [EsEmpleadoActivo]

    def get_permissions(self):
        # Operario solo puede ver pedidos y cambiar estado
        if self.action in ("create", "update", "partial_update", "destroy",
                           "calcular_total", "ticket_pdf"):
            return [EsAdministradorORecepcionista()]
        return [EsEmpleadoActivo()]

    def get_serializer_class(self):
        if self.action == "create":
            return CrearPedidoSerializer
        return PedidoSerializer

    def create(self, request, *args, **kwargs):
        serializer = CrearPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pedido = serializer.save()
        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        nuevo_estado = request.data.get("estado")
        descripcion  = request.data.get("descripcion", "")
        estado_obj   = PedidoService.cambiar_estado(pk, nuevo_estado, descripcion)
        return Response(EstadoPedidoSerializer(estado_obj).data)

    @action(detail=True, methods=["post"], url_path="calcular-total")
    def calcular_total(self, request, pk=None):
        pedido = PedidoService.obtener_pedido_por_id(pk)
        total  = PedidoService.calcular_total(pedido)
        return Response({"total": str(total)})

    @action(detail=True, methods=["get"], url_path="ticket")
    def ticket_pdf(self, request, pk=None):
        PedidoService.obtener_pedido_por_id(pk)
        pedido = Pedido.objects.select_related(
            "id_cliente", "id_empleado"
        ).prefetch_related("prendas__detalles__id_servicio").get(pk=pk)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A5,
            leftMargin=10 * mm, rightMargin=10 * mm,
            topMargin=10 * mm, bottomMargin=8 * mm,
        )

        c = pedido.id_cliente
        nombre_c     = f"{c.nombres} {c.apellidos}"
        telefono_c   = c.telefono or "—"
        direccion_c  = c.direccion or "—"
        estado_label = ESTADO_MAP.get(pedido.estado, pedido.estado)
        estado_color = ESTADO_COLOR.get(pedido.estado, GRIS)

        # ── 1. Encabezado: logo + nombre empresa ─────────────────────────────
        nombre_tbl = Table([
            [_P("Lavanderia Jireh", fs=16, bold=True, color=TEAL_DARK)],
            [_P("Servicio Profesional de Lavandería", fs=8.5, color=GRIS)],
        ], colWidths=["*"])
        nombre_tbl.setStyle(_TS([
            ("TOPPADDING",    (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ]))

        empresa = Table([[_logo(size=50), nombre_tbl]], colWidths=[58, "*"])
        empresa.setStyle(_TS([
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        # ── 2. Banner "RECIBO ELECTRÓNICO" ───────────────────────────────────
        banner = Table([
            [_P("RECIBO ELECTRÓNICO", fs=12, bold=True,
                color=BLANCO, align=TA_CENTER)]
        ], colWidths=["*"])
        banner.setStyle(_TS([
            ("BACKGROUND",    (0, 0), (-1, -1), TEAL),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))

        # ── 3. Info cliente (izq) + QR (der) ─────────────────────────────────
        qr_data = (
            f"Pedido: {pedido.codigo} | "
            f"Cliente: {nombre_c} | "
            f"Total: S/ {pedido.total:.2f}"
        )
        qr = _qr_image(qr_data, 70)

        info_rows = [
            [_lbl("DATOS DEL CLIENTE")],
            [_P(f"<b>{_html.escape(nombre_c)}</b>", fs=9.5)],
            [_val(f"Tel: {telefono_c}", fs=8)],
            [_val(f"Dir: {direccion_c}", fs=8)],
            [Spacer(1, 5)],
            [_lbl("PEDIDO")],
            [_P(f"<b>{_html.escape(pedido.codigo)}</b>", fs=12, color=TEAL_DARK)],
            [_val(f"Ingreso: {_fmt_date(pedido.fecha_ingreso)}", fs=7.5)],
            [_val(f"Entrega: {_fmt_date(pedido.fecha_entrega)}", fs=7.5)],
            [_P(f"<b>{_html.escape(estado_label)}</b>", fs=9, color=estado_color)],
        ]
        info_c = Table(info_rows, colWidths=["*"])
        info_c.setStyle(_TS([
            ("TOPPADDING",    (0, 0), (-1, -1), 1.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ]))

        bloque_info = Table([[info_c, qr]], colWidths=["*", 76])
        bloque_info.setStyle(_TS([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("BOX",           (0, 0), (-1, -1), 0.8, GRIS_BORDE),
            ("BACKGROUND",    (0, 0), (-1, -1), GRIS_BG),
            ("LINEAFTER",     (0, 0), (0, 0), 0.5, GRIS_BORDE),
            ("LEFTPADDING",   (0, 0), (0, 0), 9),
            ("RIGHTPADDING",  (0, 0), (0, 0), 6),
            ("LEFTPADDING",   (1, 0), (1, 0), 5),
            ("RIGHTPADDING",  (1, 0), (1, 0), 5),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))

        # ── 4. Tabla de servicios ─────────────────────────────────────────────
        svc_data = [[
            _P("", fs=1),
            _P("SERVICIO / PRENDA", fs=7.5, bold=True, color=BLANCO),
            _P("CANT.", fs=7.5, bold=True, color=BLANCO, align=TA_CENTER),
            _P("PESO", fs=7.5, bold=True, color=BLANCO, align=TA_CENTER),
            _P("PRECIO", fs=7.5, bold=True, color=BLANCO, align=TA_RIGHT),
        ]]

        for prenda in pedido.prendas.all():
            svc_list = [d.id_servicio.nombre_servicio for d in prenda.detalles.all()]
            svc_txt  = " / ".join(svc_list) or "—"
            subtotal = sum(d.subtotal for d in prenda.detalles.all())

            desc = Paragraph(
                f'<b>{_html.escape(prenda.tipo_prenda)}</b>'
                f'<br/><font size="7" color="#64748B">{_html.escape(svc_txt)}</font>',
                ParagraphStyle("d", parent=_STYLES["Normal"],
                               fontSize=8.5, fontName="Helvetica",
                               textColor=NEGRO, leading=12),
            )
            svc_data.append([
                _svc_dot(svc_txt),
                desc,
                _P(str(prenda.cantidad), fs=8.5, align=TA_CENTER),
                _P(f"{prenda.peso} kg", fs=8.5, align=TA_CENTER),
                _P(f"S/ {subtotal:.2f}", fs=8.5, bold=True, align=TA_RIGHT),
            ])

        if len(svc_data) == 1:
            svc_data.append([
                _P(""),
                _P("Sin prendas registradas", fs=8, color=GRIS),
                _P(""), _P(""), _P(""),
            ])

        svc_tbl = Table(svc_data, colWidths=[14, "*", 36, 40, 50])
        svc_tbl.setStyle(_TS([
            ("BACKGROUND",     (0, 0), (-1, 0), TEAL_DARK),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_BG]),
            ("BOX",            (0, 0), (-1, -1), 0.8, GRIS_BORDE),
            ("LINEBELOW",      (0, 1), (-1, -2), 0.3, GRIS_BORDE),
            ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",     (0, 0), (-1, 0), 5),
            ("BOTTOMPADDING",  (0, 0), (-1, 0), 5),
            ("TOPPADDING",     (0, 1), (-1, -1), 6),
            ("BOTTOMPADDING",  (0, 1), (-1, -1), 6),
            ("LEFTPADDING",    (0, 0), (-1, -1), 5),
            ("RIGHTPADDING",   (0, 0), (-1, -1), 5),
        ]))

        # ── 5. Observaciones (si las hay) ─────────────────────────────────────
        obs_elements: list = []
        if pedido.observaciones and pedido.observaciones.strip():
            obs_tbl = Table([
                [_lbl("OBSERVACIONES")],
                [_P(_html.escape(pedido.observaciones.strip()), fs=8)],
            ], colWidths=["*"])
            obs_tbl.setStyle(_TS([
                ("BOX",           (0, 0), (-1, -1), 0.8, GRIS_BORDE),
                ("BACKGROUND",    (0, 0), (0, 0), GRIS_BG),
                ("TOPPADDING",    (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING",   (0, 0), (-1, -1), 8),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ]))
            obs_elements = [Spacer(1, 6), obs_tbl]

        # ── 6. Resumen de pago (con IGV desglosado) ───────────────────────────
        total_val    = float(pedido.total)
        subtotal_val = total_val / 1.18
        igv_val      = total_val - subtotal_val

        resumen = Table([
            [_P("RESUMEN DE PAGO", fs=9, bold=True,
                color=BLANCO, align=TA_CENTER), ""],
            [_P("Subtotal:", fs=8.5, color=GRIS),
             _P(f"S/ {subtotal_val:.2f}", fs=8.5, align=TA_RIGHT)],
            [_P("Descuento:", fs=8.5, color=GRIS),
             _P("S/ 0.00", fs=8.5, color=GRIS, align=TA_RIGHT)],
            [_P("IGV (18%):", fs=8.5, color=GRIS),
             _P(f"S/ {igv_val:.2f}", fs=8.5, align=TA_RIGHT)],
            [_P("TOTAL A PAGAR:", fs=11, bold=True),
             _P(f"S/ {total_val:.2f}", fs=14, bold=True,
                color=TEAL_DARK, align=TA_RIGHT)],
        ], colWidths=["55%", "45%"])
        resumen.setStyle(_TS([
            ("SPAN",          (0, 0), (1, 0)),
            ("BACKGROUND",    (0, 0), (1, 0), TEAL),
            ("BACKGROUND",    (0, 1), (1, 3), GRIS_BG),
            ("BACKGROUND",    (0, 4), (1, 4), TEAL_BG),
            ("LINEABOVE",     (0, 4), (1, 4), 1.5, TEAL),
            ("LINEBELOW",     (0, 1), (1, 3), 0.3, GRIS_BORDE),
            ("BOX",           (0, 0), (-1, -1), 0.8, GRIS_BORDE),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 9),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 9),
        ]))

        resumen_wrapper = Table([["", resumen]], colWidths=["30%", "70%"])
        resumen_wrapper.setStyle(_TS([
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        # ── 7. Footer ─────────────────────────────────────────────────────────
        footer_style = ParagraphStyle(
            "fs", parent=_STYLES["Normal"],
            fontSize=7.5, fontName="Helvetica",
            textColor=GRIS, alignment=TA_CENTER, leading=12,
        )

        story = [
            Spacer(1, 7),
            empresa,
            Spacer(1, 8),
            banner,
            Spacer(1, 9),
            bloque_info,
            Spacer(1, 9),
            svc_tbl,
            *obs_elements,
            Spacer(1, 9),
            resumen_wrapper,
            Spacer(1, 10),
            HRFlowable(width="100%", thickness=0.5, color=GRIS_BORDE, spaceAfter=5),
            Paragraph("Gracias por confiar en Lavanderia Jireh", footer_style),
            Paragraph("Tu ropa, en las mejores manos · lavanderiajireh.com", footer_style),
        ]

        doc.build(story, onFirstPage=_draw_bg, onLaterPages=_draw_bg)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="recibo-{pedido.codigo}.pdf"'
        )
        return response


# ── Vista pública ─────────────────────────────────────────────────────────────
class ConsultaPedidoPublicaView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, codigo=None):
        try:
            data = PedidoService.obtener_pedido_por_codigo(codigo)
        except RecursoNoEncontradoError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(data)
