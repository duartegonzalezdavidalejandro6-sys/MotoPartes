"""
views_reportes.py  —  MotoPartes
Reportes PDF con los campos EXACTOS de tus modelos.

INTEGRACIÓN (2 pasos):
  1. Coloca este archivo junto a views.py y utils_pdf.py.
  2. Al FINAL de tu views.py agrega:
        from .views_reportes import *
  3. En urls.py pega las rutas del archivo rutas_reportes.py al final de urlpatterns.
"""

from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, Spacer

from .models import (
    CategoriaProducto,
    DetallePedido,
    Empleado,
    Factura,
    Pedido,
    Producto,
    Sede,
    Usuarios,
)
from .utils_pdf import (
    C_NARANJA,
    caja_resumen,
    encabezado,
    fmt_estado,
    fmt_precio,
    pdf_response,
    tabla,
    tabla_detalle,
)


def es_admin(user):
    return user.is_staff or user.is_superuser


# ════════════════════════════════════════════════════════════════════════════
# 1. PRODUCTOS — lista completa
#    Campos reales: nombreProducto, precioProducto, stock,
#                   estadoProducto, idCategoria_Producto.nombreCategoria
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_productos_pdf(request):
    qs = Producto.objects.select_related("idCategoria_Producto").order_by(
        "nombreProducto"
    )

    def build(story, e):
        encabezado(
            story,
            "Reporte de Productos",
            f"Total de productos registrados: {qs.count()}",
        )

        cabs = ["#", "PRODUCTO", "CATEGORÍA", "PRECIO", "STOCK", "ESTADO"]
        col_w = [
            0.35 * inch,
            2.5 * inch,
            1.4 * inch,
            1.2 * inch,
            0.75 * inch,
            1.1 * inch,
        ]
        filas = []
        for i, p in enumerate(qs, 1):
            cat = (
                p.idCategoria_Producto.nombreCategoria
                if p.idCategoria_Producto
                else "—"
            )
            filas.append(
                [
                    str(i),
                    p.nombreProducto,
                    cat,
                    fmt_precio(p.precioProducto),
                    str(p.stock),
                    Paragraph(fmt_estado(p.estadoProducto), e["centro"]),
                ]
            )
        story.append(tabla(filas, cabs, col_widths=col_w))
        story.append(Spacer(1, 14))

        disponibles = qs.filter(estadoProducto="Disponible").count()
        agotados = qs.filter(estadoProducto="Agotado").count()
        stock_bajo = qs.filter(stock__gt=0, stock__lte=5).count()
        caja_resumen(
            story,
            [
                ("Total productos", str(qs.count())),
                ("Disponibles", str(disponibles)),
                ("Agotados", str(agotados)),
                ("Stock bajo (≤5)", str(stock_bajo)),
            ],
        )

    return pdf_response(f"productos_{datetime.now().strftime('%Y%m%d')}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 2. PRODUCTO — ficha individual
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_producto_pdf(request, pk):
    p = get_object_or_404(
        Producto.objects.select_related("idCategoria_Producto"), pk=pk
    )

    def build(story, e):
        cat = p.idCategoria_Producto.nombreCategoria if p.idCategoria_Producto else "—"
        encabezado(
            story,
            "Ficha de Producto",
            f"ID #{p.idProducto}",
            extras=[["Categoría:", cat, "Estado:", p.estadoProducto]],
        )

        story.append(Paragraph(p.nombreProducto, e["seccion"]))
        story.append(
            HRFlowable(width="100%", thickness=1, color=C_NARANJA, spaceAfter=8)
        )

        campos = [
            ("Nombre", p.nombreProducto),
            ("Categoría", cat),
            ("Precio", fmt_precio(p.precioProducto)),
            ("Stock actual", p.stock),
            ("Estado", p.estadoProducto),
            ("Descripción", p.descripcion or "Sin descripción"),
            ("Imagen", str(p.imagen) if p.imagen else "Sin imagen"),
        ]
        tabla_detalle(story, campos)

    return pdf_response(f"producto_{pk}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 3. CATEGORÍAS
#    Campos reales: nombreCategoria, descripcion
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_categorias_pdf(request):
    qs = CategoriaProducto.objects.all().order_by("nombreCategoria")

    def build(story, e):
        encabezado(story, "Reporte de Categorías", f"Total: {qs.count()} categorías")

        cabs = ["#", "CATEGORÍA", "N.° PRODUCTOS", "DESCRIPCIÓN"]
        col_w = [0.4 * inch, 2.2 * inch, 1.3 * inch, 3.7 * inch]
        filas = []
        for i, c in enumerate(qs, 1):
            total = Producto.objects.filter(idCategoria_Producto=c).count()
            filas.append(
                [
                    str(i),
                    c.nombreCategoria,
                    str(total),
                    c.descripcion or "—",
                ]
            )
        story.append(tabla(filas, cabs, col_widths=col_w))
        story.append(Spacer(1, 14))
        caja_resumen(story, [("Total categorías", str(qs.count()))])

    return pdf_response(f"categorias_{datetime.now().strftime('%Y%m%d')}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 4. PEDIDOS — lista completa
#    Campos reales: idPedido, fechaPedido, estadoPedido, metodoPago,
#                   totalPedido, ciudad, tipo_entrega, idUsuario
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_pedidos_pdf(request):
    qs = Pedido.objects.select_related("idUsuario", "sede").order_by("-fechaPedido")

    def build(story, e):
        encabezado(story, "Reporte de Pedidos", f"Total: {qs.count()} pedidos")

        cabs = ["#", "PEDIDO", "CLIENTE", "FECHA", "CIUDAD", "TOTAL", "ESTADO"]
        col_w = [
            0.3 * inch,
            0.7 * inch,
            1.8 * inch,
            1 * inch,
            1 * inch,
            1.2 * inch,
            1.2 * inch,
        ]
        filas = []
        gran_total = 0
        for i, p in enumerate(qs, 1):
            u = p.idUsuario
            cliente = (
                f"{u.nombreUsuario} {u.apellidosUsuario or ''}".strip() if u else "—"
            )
            fecha = p.fechaPedido.strftime("%d/%m/%Y") if p.fechaPedido else "—"
            tot = float(p.totalPedido or 0)
            gran_total += tot
            filas.append(
                [
                    str(i),
                    f"#{p.idPedido}",
                    cliente,
                    fecha,
                    p.ciudad or "—",
                    fmt_precio(tot),
                    Paragraph(fmt_estado(p.estadoPedido), e["centro"]),
                ]
            )
        story.append(tabla(filas, cabs, col_widths=col_w))
        story.append(Spacer(1, 14))

        procesados = qs.filter(estadoPedido="Procesado").count()
        entregados = qs.filter(estadoPedido="Entregado").count()
        cancelados = qs.filter(estadoPedido="Cancelado").count()
        caja_resumen(
            story,
            [
                ("Total pedidos", str(qs.count())),
                ("Total facturado", fmt_precio(gran_total)),
                ("Procesados", str(procesados)),
                ("Entregados", str(entregados)),
                ("Cancelados", str(cancelados)),
            ],
        )

    return pdf_response(f"pedidos_{datetime.now().strftime('%Y%m%d')}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 5. PEDIDO — ficha individual con detalle de productos
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_pedido_pdf(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("idUsuario", "sede"), pk=pk
    )
    detalles = DetallePedido.objects.filter(idPedido=pedido).select_related(
        "idProducto"
    )
    factura = getattr(pedido, "factura", None)

    def build(story, e):
        u = pedido.idUsuario
        cliente = f"{u.nombreUsuario} {u.apellidosUsuario or ''}".strip() if u else "—"
        fecha = (
            pedido.fechaPedido.strftime("%d/%m/%Y %H:%M") if pedido.fechaPedido else "—"
        )

        encabezado(
            story,
            f"Pedido #{pedido.idPedido}",
            f"Cliente: {cliente}",
            extras=[
                ["Fecha:", fecha, "Estado:", pedido.estadoPedido],
                [
                    "Método de pago:",
                    pedido.metodoPago or "—",
                    "Entrega:",
                    pedido.get_tipo_entrega_display(),
                ],
            ],
        )

        # ── Datos del cliente ──────────────────────────────────────────────
        story.append(Paragraph("Datos del cliente", e["seccion"]))
        campos_cli = [
            ("Nombre completo", cliente),
            ("Tipo doc.", u.tipoDocUsuario or "—"),
            ("N.° documento", u.numDocUsuario),
            ("Correo", u.correoUsuario or "—"),
            ("Teléfono", u.telefonoUsuario or "—"),
            ("Dirección", u.direccionUsuario or "—"),
        ]
        tabla_detalle(story, campos_cli)

        # ── Datos de entrega ───────────────────────────────────────────────
        story.append(Spacer(1, 8))
        story.append(Paragraph("Datos de entrega", e["seccion"]))
        if pedido.tipo_entrega == "sede" and pedido.sede:
            entrega_campos = [
                ("Tipo", "Recoger en sede"),
                ("Sede", pedido.sede.nombre),
                ("Ciudad", pedido.sede.ciudad),
                ("Dirección", pedido.sede.direccion),
            ]
        else:
            entrega_campos = [
                ("Tipo", "Domicilio"),
                ("Ciudad", pedido.ciudad_domicilio or pedido.ciudad or "—"),
                ("Dirección", pedido.direccion_domicilio or "—"),
                ("Barrio", pedido.barrio_domicilio or "—"),
                ("Teléfono", pedido.telefono_domicilio or "—"),
                ("Costo envío", fmt_precio(pedido.costo_envio)),
            ]
        tabla_detalle(story, entrega_campos)

        # ── Productos del pedido ───────────────────────────────────────────
        story.append(Spacer(1, 10))
        story.append(Paragraph("Productos del pedido", e["seccion"]))
        cabs = ["PRODUCTO", "PRECIO UNIT.", "CANTIDAD", "SUBTOTAL"]
        col_w = [3.1 * inch, 1.5 * inch, 1.1 * inch, 1.5 * inch]
        filas = []
        for d in detalles:
            pu = float(d.precioUnitario or d.idProducto.precioProducto or 0)
            qty = d.cantidad or 0
            filas.append(
                [
                    d.idProducto.nombreProducto,
                    fmt_precio(pu),
                    str(qty),
                    fmt_precio(pu * qty),
                ]
            )
        if filas:
            story.append(tabla(filas, cabs, col_widths=col_w))
        else:
            story.append(Paragraph("Sin productos registrados.", e["normal"]))

        # ── Totales ────────────────────────────────────────────────────────
        story.append(Spacer(1, 10))
        resumen = []
        if factura:
            resumen += [
                (
                    "N.° Factura",
                    factura.numeroFactura or f"FAC-{factura.idFactura:06d}",
                ),
                ("Subtotal", fmt_precio(factura.subtotal)),
                ("IVA (19 %)", fmt_precio(factura.iva)),
            ]
        if pedido.tipo_entrega == "domicilio":
            resumen.append(("Costo de envío", fmt_precio(pedido.costo_envio)))
        resumen.append(("TOTAL DEL PEDIDO", fmt_precio(pedido.totalPedido)))
        caja_resumen(story, resumen)

    return pdf_response(f"pedido_{pk}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 6. CLIENTES
#    Modelo real: Usuarios  —  nombreUsuario, apellidosUsuario,
#                              correoUsuario, telefonoUsuario,
#                              tipoDocUsuario, numDocUsuario, estadoUsuario
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_clientes_pdf(request):
    from django.db.models import Count

    qs = Usuarios.objects.annotate(num_pedidos=Count("pedido")).order_by(
        "nombreUsuario"
    )

    def build(story, e):
        encabezado(
            story,
            "Reporte de Clientes",
            f"Total: {qs.count()} clientes registrados",
        )

        cabs = [
            "#",
            "NOMBRE",
            "DOCUMENTO",
            "CORREO",
            "TELÉFONO",
            "PEDIDOS",
            "ESTADO",
        ]
        col_w = [
            0.3 * inch,
            1.8 * inch,
            1.2 * inch,
            1.9 * inch,
            1.1 * inch,
            0.7 * inch,
            0.7 * inch,
        ]
        filas = []
        for i, c in enumerate(qs, 1):
            nombre = f"{c.nombreUsuario} {c.apellidosUsuario or ''}".strip()
            doc = f"{c.tipoDocUsuario or ''} {c.numDocUsuario}".strip()
            estado = "Activo" if c.estadoUsuario == "A" else "Inactivo"
            filas.append(
                [
                    str(i),
                    nombre,
                    doc,
                    c.correoUsuario or "—",
                    str(c.telefonoUsuario or "—"),
                    str(c.num_pedidos),
                    Paragraph(fmt_estado(estado), e["centro"]),
                ]
            )
        story.append(tabla(filas, cabs, col_widths=col_w))
        story.append(Spacer(1, 14))
        activos = qs.filter(estadoUsuario="A").count()
        caja_resumen(
            story,
            [
                ("Total clientes", str(qs.count())),
                ("Activos", str(activos)),
                ("Inactivos", str(qs.count() - activos)),
            ],
        )

    return pdf_response(f"clientes_{datetime.now().strftime('%Y%m%d')}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 7. EMPLEADOS
#    Modelo real: Empleado  —  usuario (OneToOne → User),
#                              cedula, cargo, telefono,
#                              direccion, fecha_nacimiento,
#                              fecha_contratacion, salario
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_empleados_pdf(request):
    qs = Empleado.objects.select_related("usuario").order_by("usuario__first_name")

    def build(story, e):
        encabezado(story, "Reporte de Empleados", f"Total: {qs.count()} empleados")

        cabs = [
            "#",
            "NOMBRE",
            "CÉDULA",
            "CARGO",
            "TELÉFONO",
            "CONTRATACIÓN",
            "SALARIO",
        ]
        col_w = [
            0.3 * inch,
            1.9 * inch,
            1.1 * inch,
            1.1 * inch,
            1 * inch,
            1.1 * inch,
            1.2 * inch,
        ]
        filas = []
        for i, emp in enumerate(qs, 1):
            nombre = emp.usuario.get_full_name() or emp.usuario.username
            contrat = (
                emp.fecha_contratacion.strftime("%d/%m/%Y")
                if emp.fecha_contratacion
                else "—"
            )
            filas.append(
                [
                    str(i),
                    nombre,
                    emp.cedula,
                    emp.get_cargo_display(),
                    emp.telefono or "—",
                    contrat,
                    fmt_precio(emp.salario),
                ]
            )
        story.append(tabla(filas, cabs, col_widths=col_w))
        story.append(Spacer(1, 14))
        admins = qs.filter(cargo="admin").count()
        empleados_n = qs.filter(cargo="empleado").count()
        caja_resumen(
            story,
            [
                ("Total empleados", str(qs.count())),
                ("Administradores", str(admins)),
                ("Empleados", str(empleados_n)),
            ],
        )

    return pdf_response(f"empleados_{datetime.now().strftime('%Y%m%d')}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 8. SEDES
#    Modelo real: Sede  —  nombre, direccion, ciudad, telefono, activa
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_sedes_pdf(request):
    from django.db.models import Count

    qs = Sede.objects.annotate(num_pedidos=Count("pedido")).order_by("nombre")

    def build(story, e):
        encabezado(story, "Reporte de Sedes", f"Total: {qs.count()} sedes")

        cabs = [
            "#",
            "SEDE",
            "CIUDAD",
            "DIRECCIÓN",
            "TELÉFONO",
            "PEDIDOS",
            "ACTIVA",
        ]
        col_w = [
            0.3 * inch,
            1.5 * inch,
            1.1 * inch,
            2 * inch,
            1 * inch,
            0.7 * inch,
            0.7 * inch,
        ]
        filas = []
        for i, s in enumerate(qs, 1):
            filas.append(
                [
                    str(i),
                    s.nombre,
                    s.ciudad,
                    s.direccion,
                    s.telefono or "—",
                    str(s.num_pedidos),
                    Paragraph(
                        fmt_estado("ACTIVO" if s.activa else "INACTIVO"),
                        e["centro"],
                    ),
                ]
            )
        story.append(tabla(filas, cabs, col_widths=col_w))
        story.append(Spacer(1, 14))
        activas = qs.filter(activa=True).count()
        caja_resumen(
            story,
            [
                ("Total sedes", str(qs.count())),
                ("Activas", str(activas)),
                ("Inactivas", str(qs.count() - activas)),
            ],
        )

    return pdf_response(f"sedes_{datetime.now().strftime('%Y%m%d')}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 9. COMPRAS / FACTURAS — panel_compras y empleado_compras usan Pedido+Factura
#    Campos reales: Factura.numeroFactura, Factura.totalPedido,
#                   Factura.fechaFactura, Factura.metodoDePago,
#                   Factura.subtotal, Factura.iva
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_compras_pdf(request):
    qs = Factura.objects.select_related(
        "idPedido__idUsuario", "idPedido__sede"
    ).order_by("-fechaFactura")

    def build(story, e):
        encabezado(
            story,
            "Reporte de Compras / Facturas",
            f"Total: {qs.count()} facturas",
        )

        cabs = [
            "#",
            "FACTURA",
            "CLIENTE",
            "FECHA",
            "MÉTODO PAGO",
            "TOTAL",
            "IVA",
        ]
        col_w = [
            0.3 * inch,
            1.1 * inch,
            1.8 * inch,
            1 * inch,
            1.2 * inch,
            1.2 * inch,
            1 * inch,
        ]
        filas = []
        gran_total = 0
        for i, f in enumerate(qs, 1):
            u = f.idPedido.idUsuario if f.idPedido else None
            cliente = (
                f"{u.nombreUsuario} {u.apellidosUsuario or ''}".strip() if u else "—"
            )
            fecha = f.fechaFactura.strftime("%d/%m/%Y") if f.fechaFactura else "—"
            tot = float(f.totalPedido or 0)
            gran_total += tot
            filas.append(
                [
                    str(i),
                    f.numeroFactura or f"#{f.idFactura}",
                    cliente,
                    fecha,
                    f.metodoDePago or "—",
                    fmt_precio(tot),
                    fmt_precio(f.iva or 0),
                ]
            )
        story.append(tabla(filas, cabs, col_widths=col_w))
        story.append(Spacer(1, 14))
        caja_resumen(
            story,
            [
                ("Total facturas", str(qs.count())),
                ("Total facturado", fmt_precio(gran_total)),
            ],
        )

    return pdf_response(f"compras_{datetime.now().strftime('%Y%m%d')}.pdf", build)


# ════════════════════════════════════════════════════════════════════════════
# 10. VENTAS — resumen mensual de pedidos (igual a panel_reportes)
#     Usa: Pedido.fechaPedido, Pedido.totalPedido, Pedido.estadoPedido
# ════════════════════════════════════════════════════════════════════════════
@login_required
@user_passes_test(es_admin, login_url="/")
def reporte_ventas_pdf(request):
    from django.db.models import Count, Sum
    from django.db.models.functions import TruncMonth

    qs_mes = (
        Pedido.objects.annotate(mes=TruncMonth("fechaPedido"))
        .values("mes")
        .annotate(total_mes=Sum("totalPedido"), n_pedidos=Count("idPedido"))
        .order_by("-mes")
    )

    # totales generales (igual que panel_reportes)
    from django.db.models import Sum as S

    total_general = Pedido.objects.aggregate(t=S("totalPedido"))["t"] or 0
    procesados = Pedido.objects.filter(estadoPedido="Procesado").count()
    entregados = Pedido.objects.filter(estadoPedido="Entregado").count()
    cancelados = Pedido.objects.filter(estadoPedido="Cancelado").count()

    def build(story, e):
        encabezado(story, "Reporte de Ventas", "Resumen mensual de todos los pedidos")

        cabs = ["MES / AÑO", "N.° PEDIDOS", "TOTAL VENDIDO"]
        col_w = [2.5 * inch, 2 * inch, 2.5 * inch]
        filas = []
        for v in qs_mes:
            mes = v["mes"].strftime("%B %Y").capitalize() if v["mes"] else "—"
            filas.append(
                [
                    mes,
                    str(v["n_pedidos"]),
                    fmt_precio(v["total_mes"] or 0),
                ]
            )

        if filas:
            story.append(tabla(filas, cabs, col_widths=col_w))
        else:
            story.append(Paragraph("No hay pedidos registrados.", e["normal"]))

        story.append(Spacer(1, 14))
        caja_resumen(
            story,
            [
                ("Total general facturado", fmt_precio(total_general)),
                ("Pedidos procesados", str(procesados)),
                ("Pedidos entregados", str(entregados)),
                ("Pedidos cancelados", str(cancelados)),
            ],
        )

    return pdf_response(f"ventas_{datetime.now().strftime('%Y%m%d')}.pdf", build)
