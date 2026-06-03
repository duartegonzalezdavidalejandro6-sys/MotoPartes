from django.contrib.auth.models import User
from django.db import models


# ── 1. SEGURIDAD Y ROLES ──
class Rol(models.Model):
    idRol = models.AutoField(primary_key=True)
    descripcionRol = models.CharField(max_length=50)
    estadoRol = models.CharField(max_length=11, default="Activo")

    class Meta:
        db_table = "Rol"

    def __str__(self):
        return self.descripcionRol


class Permisos(models.Model):
    idPermisos = models.AutoField(primary_key=True)
    descripcionPermiso = models.CharField(max_length=100, null=True, blank=True)
    fechaAsignacion = models.DateTimeField(auto_now_add=True)
    estadoPermiso = models.CharField(max_length=30, default="Activo")
    idRol = models.ForeignKey(
        Rol, on_delete=models.SET_NULL, null=True, db_column="idRol"
    )

    class Meta:
        db_table = "Permisos"

    def __str__(self):
        return self.descripcionPermiso


# ── 2. USUARIOS ──
class Usuarios(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    tipoDocUsuario = models.CharField(max_length=10, null=True, blank=True)
    numDocUsuario = models.BigIntegerField(unique=True)
    nombreUsuario = models.CharField(max_length=50)
    apellidosUsuario = models.CharField(max_length=50, null=True, blank=True)
    direccionUsuario = models.CharField(max_length=100, null=True, blank=True)
    telefonoUsuario = models.BigIntegerField(null=True, blank=True)
    correoUsuario = models.EmailField(
        max_length=100, unique=True, null=True, blank=True
    )
    claveUsuario = models.CharField(max_length=100)
    estadoUsuario = models.CharField(max_length=1, default="A")
    idRol = models.ForeignKey(
        Rol, on_delete=models.SET_NULL, null=True, db_column="idRol"
    )

    class Meta:
        db_table = "Usuarios"

    def __str__(self):
        return f"{self.nombreUsuario} {self.apellidosUsuario}"


# ── 3. PRODUCTOS ──
class CategoriaProducto(models.Model):
    idCategoria_Producto = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "CategoriaProducto"

    def __str__(self):
        return self.nombreCategoria


class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=100)
    precioProducto = models.DecimalField(max_digits=14, decimal_places=2)
    stock = models.IntegerField(default=0)
    estadoProducto = models.CharField(max_length=50, default="Disponible")
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to="productos/", null=True, blank=True)
    idCategoria_Producto = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.SET_NULL,
        null=True,
        db_column="idCategoria_Producto",
    )

    class Meta:
        db_table = "Producto"

    def __str__(self):
        return self.nombreProducto


# ── 4. SEDES ──
class Sede(models.Model):
    idSede = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "Sede"

    def __str__(self):
        return f"{self.nombre} — {self.ciudad}"


# ── 5. VENTAS ──
class Pedido(models.Model):
    TIPO_ENTREGA_CHOICES = [
        ("sede", "Recoger en Sede"),
        ("domicilio", "Domicilio"),
    ]

    # Costos de envío por ciudad (en pesos colombianos)
    COSTOS_ENVIO = {
        "Bogotá": 5000,
        "Medellín": 8000,
        "Cali": 8000,
        "Barranquilla": 10000,
    }

    idPedido = models.AutoField(primary_key=True)
    fechaPedido = models.DateTimeField(auto_now_add=True)
    horaPedido = models.TimeField(auto_now_add=True)
    estadoPedido = models.CharField(max_length=20, default="Procesado")
    metodoPago = models.CharField(max_length=30)
    totalPedido = models.DecimalField(max_digits=14, decimal_places=2)
    codigopostal = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=30)
    idUsuario = models.ForeignKey(
        Usuarios, on_delete=models.CASCADE, db_column="idUsuario"
    )
    sede = models.ForeignKey(
        Sede,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="idSede",
    )

    # ── NUEVOS CAMPOS DE DOMICILIO ──
    tipo_entrega = models.CharField(
        max_length=10, choices=TIPO_ENTREGA_CHOICES, default="sede"
    )
    direccion_domicilio = models.CharField(max_length=200, null=True, blank=True)
    barrio_domicilio = models.CharField(max_length=100, null=True, blank=True)
    ciudad_domicilio = models.CharField(max_length=50, null=True, blank=True)
    telefono_domicilio = models.CharField(max_length=20, null=True, blank=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "Pedido"

    def __str__(self):
        return f"Pedido #{self.idPedido} - {self.estadoPedido}"


class DetallePedido(models.Model):
    idDetalle = models.AutoField(primary_key=True)
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, db_column="idPedido")
    idProducto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, db_column="idProducto"
    )
    cantidad = models.IntegerField()
    precioUnitario = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "DetallePedido"

    def __str__(self):
        return f"Detalle #{self.idDetalle}"


class Factura(models.Model):
    idFactura = models.AutoField(primary_key=True)
    tipoDocUsuario = models.CharField(max_length=10, null=True, blank=True)
    numeroDoc = models.BigIntegerField(null=True, blank=True)
    valorUnitarioProducto = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    totalPedido = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    fechaPedido = models.DateTimeField(null=True, blank=True)
    fechaFactura = models.DateTimeField(auto_now_add=True)
    metodoDePago = models.CharField(max_length=50, null=True, blank=True)
    idPedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, db_column="idPedido"
    )
    numeroFactura = models.CharField(max_length=20, null=True, blank=True)
    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    iva = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "Factura"

    def __str__(self):
        return f"Factura #{self.idFactura}"


# ── 6. EMPLEADOS ──
class Empleado(models.Model):
    CARGOS = [
        ("admin", "Administrador"),
        ("empleado", "Empleado"),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=20, choices=CARGOS, default="empleado")
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    fecha_contratacion = models.DateField(auto_now_add=True)
    salario = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_cargo_display()}"


# ── 7. CARRITO ──
class CarritoItem(models.Model):
    idCarritoItem = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    idProducto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, db_column="idProducto"
    )
    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.idProducto.precioProducto * self.cantidad

    class Meta:
        db_table = "CarritoItem"
        unique_together = ["usuario", "idProducto"]

    def __str__(self):
        return f"{self.cantidad}x {self.idProducto.nombreProducto}"

# ── 8. VENTAS PRESENCIALES ──

class Venta(models.Model):
    ESTADO_CHOICES = [
        ("completada", "Completada"),
        ("anulada", "Anulada"),
        ("pendiente", "Pendiente"),
    ]

    METODO_PAGO_CHOICES = [
        ("efectivo", "Efectivo"),
        ("tarjeta_debito", "Tarjeta Débito"),
        ("tarjeta_credito", "Tarjeta Crédito"),
        ("transferencia", "Transferencia"),
        ("nequi", "Nequi"),
        ("daviplata", "Daviplata"),
    ]

    idVenta        = models.AutoField(primary_key=True)
    fechaVenta     = models.DateTimeField(auto_now_add=True)
    estadoVenta    = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="completada")
    metodoPago     = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    subtotal       = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descuento      = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    iva            = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total          = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones  = models.TextField(null=True, blank=True)

    cliente  = models.ForeignKey(Usuarios,  on_delete=models.PROTECT, db_column="idCliente",  related_name="ventas_presenciales")
    empleado = models.ForeignKey(Empleado,  on_delete=models.PROTECT, db_column="idEmpleado", related_name="ventas_realizadas")
    sede     = models.ForeignKey(Sede,      on_delete=models.PROTECT, db_column="idSede",     related_name="ventas_sede")

    class Meta:
        db_table = "Venta"

    def __str__(self):
        return f"Venta #{self.idVenta} — {self.cliente} — {self.fechaVenta.strftime('%d/%m/%Y')}"

    def calcular_totales(self):
        from decimal import Decimal
        self.subtotal = sum(d.subtotal for d in self.detalles.all()) - self.descuento
        self.iva      = (self.subtotal * Decimal("0.19")).quantize(Decimal("0.01"))
        self.total    = self.subtotal + self.iva
        self.save()


class DetalleVenta(models.Model):
    idDetalle      = models.AutoField(primary_key=True)
    cantidad       = models.PositiveIntegerField()
    precioUnitario = models.DecimalField(max_digits=14, decimal_places=2)
    descuentoLinea = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    venta    = models.ForeignKey(Venta,    on_delete=models.CASCADE,  db_column="idVenta",    related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT,  db_column="idProducto", related_name="detalles_venta")

    class Meta:
        db_table = "DetalleVenta"

    @property
    def subtotal(self):
        return (self.precioUnitario * self.cantidad) - self.descuentoLinea

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombreProducto} — Venta #{self.venta.idVenta}"


class NotaCreditoVenta(models.Model):
    MOTIVO_CHOICES = [
        ("devolucion",  "Devolución de producto"),
        ("error_cobro", "Error en cobro"),
        ("anulacion",   "Anulación total"),
    ]

    idNota        = models.AutoField(primary_key=True)
    fechaNota     = models.DateTimeField(auto_now_add=True)
    motivo        = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    descripcion   = models.TextField(null=True, blank=True)
    montoDevuelto = models.DecimalField(max_digits=14, decimal_places=2)

    venta    = models.OneToOneField(Venta,    on_delete=models.CASCADE,  db_column="idVenta",    related_name="nota_credito")
    empleado = models.ForeignKey(Empleado,   on_delete=models.PROTECT,  db_column="idEmpleado", related_name="notas_credito")

    class Meta:
        db_table = "NotaCreditoVenta"

    def __str__(self):
        return f"Nota #{self.idNota} — Venta #{self.venta.idVenta}"


# ── 9. REPORTES UNIFICADOS (sin tabla extra en BD) ──

class ResumenVenta:
    """
    Clase utilitaria (NO es un modelo de BD).
    Unifica Pedido (virtual) y Venta (presencial) para reportes.
    Úsala en tus vistas o en el admin para mostrar estadísticas globales.
    """

    @staticmethod
    def totales_por_periodo(fecha_inicio, fecha_fin):
        from django.db.models import Sum, Count
        from decimal import Decimal

        ventas_presenciales = Venta.objects.filter(
            fechaVenta__range=(fecha_inicio, fecha_fin),
            estadoVenta="completada"
        ).aggregate(
            total=Sum("total"),
            cantidad=Count("idVenta")
        )

        ventas_virtuales = Pedido.objects.filter(
            fechaPedido__range=(fecha_inicio, fecha_fin),
            estadoPedido="Procesado"
        ).aggregate(
            total=Sum("totalPedido"),
            cantidad=Count("idPedido")
        )

        total_presencial = ventas_presenciales["total"] or Decimal("0")
        total_virtual    = ventas_virtuales["total"]    or Decimal("0")

        return {
            "presencial": {
                "total":    total_presencial,
                "cantidad": ventas_presenciales["cantidad"] or 0,
            },
            "virtual": {
                "total":    total_virtual,
                "cantidad": ventas_virtuales["cantidad"] or 0,
            },
            "gran_total": total_presencial + total_virtual,
        }

    @staticmethod
    def productos_mas_vendidos(fecha_inicio, fecha_fin, limite=10):
        from django.db.models import Sum, F

        # Presenciales
        presencial = (
            DetalleVenta.objects
            .filter(venta__fechaVenta__range=(fecha_inicio, fecha_fin),
                    venta__estadoVenta="completada")
            .values(nombre=F("producto__nombreProducto"))
            .annotate(unidades=Sum("cantidad"))
        )

        # Virtuales
        virtual = (
            DetallePedido.objects
            .filter(idPedido__fechaPedido__range=(fecha_inicio, fecha_fin),
                    idPedido__estadoPedido="Procesado")
            .values(nombre=F("idProducto__nombreProducto"))
            .annotate(unidades=Sum("cantidad"))
        )

        # Combinar y ordenar
        combinado = {}
        for item in list(presencial) + list(virtual):
            combinado[item["nombre"]] = combinado.get(item["nombre"], 0) + item["unidades"]

        return sorted(combinado.items(), key=lambda x: x[1], reverse=True)[:limite]
    
    # ── Agrega esto en acceso/models.py ──────────────────────────────────────────
import uuid
from django.utils import timezone
from datetime import timedelta
 
class PasswordResetToken(models.Model):
    """Token de un solo uso para recuperar contraseña."""
    usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE,
                                  related_name='reset_tokens')
    token     = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    usado     = models.BooleanField(default=False)
 
    def es_valido(self):
        """El token expira en 1 hora."""
        return not self.usado and (timezone.now() - self.creado_en) < timedelta(hours=1)
 
    def __str__(self):
        return f"Token de {self.usuario} — {'usado' if self.usado else 'activo'}"
 
    class Meta:
        verbose_name = "Token de recuperación"
        verbose_name_plural = "Tokens de recuperación"
 