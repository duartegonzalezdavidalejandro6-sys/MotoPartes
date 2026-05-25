"""
utils_pdf.py  —  MotoPartes
Helpers de estilo para todos los reportes PDF.
Coloca este archivo en la misma carpeta que views.py.
"""

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ── Paleta MotoPartes ─────────────────────────────────────────────────────────
C_NARANJA = colors.HexColor("#FF6600")
C_OSCURO = colors.HexColor("#1A1A1A")
C_GRIS_CLARO = colors.HexColor("#F5F5F5")
C_VERDE = colors.HexColor("#28A745")
C_ROJO = colors.HexColor("#DC3545")
C_AMARILLO = colors.HexColor("#FFC107")
C_TEXTO = colors.HexColor("#333333")
C_BLANCO = colors.white


def estilos():
    return {
        "titulo": ParagraphStyle(
            "titulo",
            fontSize=20,
            fontName="Helvetica-Bold",
            textColor=C_NARANJA,
            spaceAfter=2,
        ),
        "sub": ParagraphStyle(
            "sub",
            fontSize=9,
            fontName="Helvetica",
            textColor=colors.HexColor("#888888"),
            spaceAfter=6,
        ),
        "seccion": ParagraphStyle(
            "seccion",
            fontSize=12,
            fontName="Helvetica-Bold",
            textColor=C_OSCURO,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "normal": ParagraphStyle(
            "normal",
            fontSize=8.5,
            fontName="Helvetica",
            textColor=C_TEXTO,
            spaceAfter=3,
        ),
        "bold": ParagraphStyle(
            "bold", fontSize=8.5, fontName="Helvetica-Bold", textColor=C_OSCURO
        ),
        "centro": ParagraphStyle(
            "centro",
            fontSize=8.5,
            fontName="Helvetica",
            textColor=C_TEXTO,
            alignment=TA_CENTER,
        ),
    }


def encabezado(story, titulo, subtitulo="", extras=None):
    e = estilos()
    story.append(Paragraph("MOTOPARTES", e["titulo"]))
    story.append(Paragraph(f"Panel de Control — {titulo}", e["sub"]))
    story.append(HRFlowable(width="100%", thickness=2, color=C_NARANJA, spaceAfter=6))

    fecha = datetime.now().strftime("%d/%m/%Y  %H:%M")
    meta = [["Reporte:", titulo, "Generado:", fecha]]
    if subtitulo:
        meta.append(["", subtitulo, "", ""])
    if extras:
        meta += extras

    t = Table(meta, colWidths=[1.1 * inch, 3.6 * inch, 1.1 * inch, 2 * inch])
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 0), (0, -1), C_NARANJA),
                ("TEXTCOLOR", (2, 0), (2, -1), C_NARANJA),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 10))


def tabla(datos, cabeceras, col_widths=None):
    filas = [cabeceras] + datos
    t = Table(filas, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), C_OSCURO),
                ("TEXTCOLOR", (0, 0), (-1, 0), C_NARANJA),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("LINEBELOW", (0, 0), (-1, 0), 1.5, C_NARANJA),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("TEXTCOLOR", (0, 1), (-1, -1), C_TEXTO),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_BLANCO, C_GRIS_CLARO]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDDDDD")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 1), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def tabla_detalle(story, campos):
    e = estilos()
    filas = [
        [
            Paragraph(f"<b>{k}</b>", e["normal"]),
            Paragraph(str(v) if v is not None else "—", e["normal"]),
        ]
        for k, v in campos
    ]
    t = Table(filas, colWidths=[2 * inch, 5 * inch])
    t.setStyle(
        TableStyle(
            [
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [C_BLANCO, C_GRIS_CLARO]),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#DDDDDD")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 0), (0, -1), C_NARANJA),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ]
        )
    )
    story.append(t)


def caja_resumen(story, items):
    e = estilos()
    filas = [
        [Paragraph(f"<b>{k}</b>", e["bold"]), Paragraph(str(v), e["bold"])]
        for k, v in items
    ]
    t = Table(filas, colWidths=[2.8 * inch, 2.5 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), C_OSCURO),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("TEXTCOLOR", (1, 0), (1, -1), C_NARANJA),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2D2D2D")),
            ]
        )
    )
    story.append(t)


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#AAAAAA"))
    canvas.drawString(0.5 * inch, 0.38 * inch, "MotoPartes — Panel de Control")
    canvas.drawRightString(letter[0] - 0.5 * inch, 0.38 * inch, f"Página {doc.page}")
    canvas.setStrokeColor(C_NARANJA)
    canvas.setLineWidth(0.5)
    canvas.line(0.5 * inch, 0.52 * inch, letter[0] - 0.5 * inch, 0.52 * inch)
    canvas.restoreState()


def pdf_response(nombre, build_fn):
    """Genera HttpResponse con PDF que se descarga directamente."""
    from django.http import HttpResponse

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.7 * inch,
    )
    story = []
    build_fn(story, estilos())
    doc.build(story, onFirstPage=pie, onLaterPages=pie)
    buf.seek(0)
    r = HttpResponse(buf, content_type="application/pdf")
    r["Content-Disposition"] = f'attachment; filename="{nombre}"'
    return r


# ── Helpers de formato ────────────────────────────────────────────────────────
def fmt_precio(v):
    try:
        return f"$ {float(v):,.2f}"
    except Exception:
        return "—"


def fmt_estado(val):
    s = str(val)
    su = s.upper()
    if su in ("DISPONIBLE", "ACTIVO", "ENTREGADO", "CONFIRMADO", "LISTO"):
        color = "#28A745"
    elif su in ("AGOTADO", "INACTIVO", "CANCELADO"):
        color = "#DC3545"
    elif su in ("PROCESADO", "EN PROCESO", "PENDIENTE"):
        color = "#FFC107"
    else:
        color = "#333333"
    return f'<font color="{color}"><b>{s}</b></font>'
