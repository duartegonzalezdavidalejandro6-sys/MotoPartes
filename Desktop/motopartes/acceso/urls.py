from django.urls import path
from . import views
from .views_recuperar import recuperar_solicitud, recuperar_nueva_clave

urlpatterns = [
    # ── Tienda pública ──
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("registro/", views.registro, name="registro"),
    path("productos/", views.productos, name="productos"),
    path("productos/<int:pk>/", views.detalle_producto, name="detalle_producto"),
    path('venta/<int:pk>/', views.empleado_venta_detalle, name='empleado_venta_detalle'),
    path("productos/<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<int:pk>/eliminar/", views.eliminar_producto, name="eliminar_producto"),

    # ── Recuperar contraseña ──
    path("recuperar/", recuperar_solicitud, name="recuperar_solicitud"),
    path("recuperar/nueva-clave/<uuid:token>/", recuperar_nueva_clave, name="recuperar_nueva_clave"),

    # ── Panel Admin ──
    path("panel/clientes/<int:pk>/toggle/", views.panel_cliente_toggle, name="panel_cliente_toggle"),
    path("panel/", views.panel_dashboard, name="panel_dashboard"),
    path("panel/productos/", views.panel_productos, name="panel_productos"),
    path("panel/productos/nuevo/", views.panel_producto_crear, name="panel_producto_crear"),
    path("panel/productos/<int:pk>/editar/", views.panel_producto_editar, name="panel_producto_editar"),
    path("panel/productos/<int:pk>/eliminar/", views.panel_producto_eliminar, name="panel_producto_eliminar"),
    path("panel/pedidos/", views.panel_pedidos, name="panel_pedidos"),
    path("panel/pedidos/<int:pk>/", views.panel_pedido_detalle, name="panel_pedido_detalle"),
    path("panel/clientes/", views.panel_clientes, name="panel_clientes"),
    path("panel/clientes/importar/", views.panel_clientes_importar, name="panel_clientes_importar"),
    path("panel/empleados/", views.panel_empleados, name="panel_empleados"),
    path("panel/empleados/nuevo/", views.panel_empleado_crear, name="panel_empleado_crear"),
    path("panel/empleados/<int:pk>/editar/", views.panel_empleado_editar, name="panel_empleado_editar"),
    path("panel/empleados/<int:pk>/eliminar/", views.panel_empleado_eliminar, name="panel_empleado_eliminar"),
    path("panel/categorias/", views.panel_categorias, name="panel_categorias"),
    path("panel/categorias/nueva/", views.panel_categoria_crear, name="panel_categoria_crear"),
    path("panel/categorias/<int:pk>/editar/", views.panel_categoria_editar, name="panel_categoria_editar"),
    path("panel/categorias/<int:pk>/eliminar/", views.panel_categoria_eliminar, name="panel_categoria_eliminar"),
    path("panel/reportes/", views.panel_reportes, name="panel_reportes"),
    path("panel/sedes/", views.panel_sedes, name="panel_sedes"),
    path("panel/sedes/nueva/", views.panel_sede_crear, name="panel_sede_crear"),
    path("panel/sedes/<int:pk>/editar/", views.panel_sede_editar, name="panel_sede_editar"),
    path("panel/sedes/<int:pk>/eliminar/", views.panel_sede_eliminar, name="panel_sede_eliminar"),
    path("panel/compras/", views.panel_compras, name="panel_compras"),
    path("panel/productos/importar/", views.panel_productos_importar, name="panel_productos_importar"),
    path("panel/productos/plantilla/", views.descargar_plantilla_productos, name="descargar_plantilla_productos"),

    # ── Ventas (admin) ──
    path("panel/ventas/", views.panel_ventas, name="panel_ventas"),
    path("panel/ventas/<int:pk>/", views.panel_venta_detalle, name="panel_venta_detalle"),
    path("panel/reportes/ventas/pdf/", views.reporte_ventas_pdf, name="reporte_ventas_pdf"),

    # ── Reportes PDF Admin ──
    path("panel/reportes/empleados/pdf/", views.reporte_empleados_pdf, name="reporte_empleados_pdf"),
    path("panel/reportes/productos/pdf/", views.reporte_productos_pdf, name="reporte_productos_pdf"),
    path("panel/reportes/pedidos/pdf/", views.reporte_pedidos_pdf, name="reporte_pedidos_pdf"),
    path("panel/reportes/categorias/pdf/", views.reporte_categorias_pdf, name="reporte_categorias_pdf"),
    path("panel/reportes/clientes/pdf/", views.reporte_clientes_pdf, name="reporte_clientes_pdf"),
    path("panel/reportes/sedes/pdf/", views.reporte_sedes_pdf, name="reporte_sedes_pdf"),

    # ── Panel Empleado ──
    path("empleado/login/", views.login_empleado, name="login_empleado"),
    path("empleado/panel/", views.panel_empleado, name="panel_empleado"),
    path("empleado/productos/nuevo/", views.empleado_producto_crear, name="empleado_producto_crear"),
    path("empleado/productos/<int:pk>/editar/", views.empleado_producto_editar, name="empleado_producto_editar"),
    path("empleado/productos/<int:pk>/eliminar/", views.empleado_producto_eliminar, name="empleado_producto_eliminar"),
    path("empleado/agregar-producto/", views.agregar_producto_empleado, name="agregar_producto_empleado"),
    path("empleado/pedidos/", views.empleado_pedidos, name="empleado_pedidos"),
    path("empleado/pedidos/<int:pk>/", views.empleado_pedido_detalle, name="empleado_pedido_detalle"),
    path("empleado/categorias/", views.empleado_categorias, name="empleado_categorias"),
    path("empleado/categorias/nueva/", views.empleado_categoria_crear, name="empleado_categoria_crear"),
    path("empleado/categorias/<int:pk>/editar/", views.empleado_categoria_editar, name="empleado_categoria_editar"),
    path("empleado/categorias/<int:pk>/eliminar/", views.empleado_categoria_eliminar, name="empleado_categoria_eliminar"),
    path("empleado/compras/", views.empleado_compras, name="empleado_compras"),
    path("empleado/ventas/", views.empleado_ventas, name="empleado_ventas"),
    path("empleado/facturas/", views.empleado_facturas, name="empleado_facturas"),

    # ── Reportes PDF Empleado ──
    path("empleado/reportes/productos/pdf/", views.empleado_reporte_productos_pdf, name="empleado_reporte_productos_pdf"),
    path("empleado/reportes/categorias/pdf/", views.empleado_reporte_categorias_pdf, name="empleado_reporte_categorias_pdf"),
    path("empleado/reportes/pedidos/pdf/", views.empleado_reporte_pedidos_pdf, name="empleado_reporte_pedidos_pdf"),
    path("empleado/reportes/ventas/pdf/", views.empleado_reporte_ventas_pdf, name="empleado_reporte_ventas_pdf"),

    # ── Campaña ──
    path("panel/campana/", views.panel_campana, name="panel_campana"),

    # ── Carrito ──
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:pk>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/actualizar/<int:pk>/", views.actualizar_cantidad_carrito, name="actualizar_cantidad_carrito"),
    path("carrito/eliminar/<int:pk>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),

    # ── Checkout ──
    path("checkout/", views.checkout, name="checkout"),

    # ── Facturas del usuario ──
    path("mis-facturas/", views.mis_facturas, name="mis_facturas"),
    path("mis-facturas/<int:pk>/", views.detalle_factura, name="detalle_factura"),
    path("mis-compras/", views.mis_compras, name="mis_compras"),
    path("facturas/<int:pk>/", views.ver_factura, name="ver_factura"),

    # ── Perfil ──
    path("perfil/", views.mi_perfil, name="mi_perfil"),
]