from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    CategoriaProducto,
    DetallePedido,
    Factura,
    Pedido,
    Permisos,
    Producto,
    Rol,
    Usuarios,
)


# Resource para carga masiva de Usuarios/Clientes
class UsuariosResource(resources.ModelResource):
    class Meta:
        model = Usuarios
        fields = (
            "tipoDocUsuario",
            "numDocUsuario",
            "nombreUsuario",
            "apellidosUsuario",
            "direccionUsuario",
            "telefonoUsuario",
            "correoUsuario",
            "claveUsuario",
            "estadoUsuario",
            "idRol",
        )


@admin.register(Usuarios)
class UsuariosAdmin(ImportExportModelAdmin):
    resource_class = UsuariosResource


admin.site.register(Rol)
admin.site.register(Permisos)
admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Factura)
