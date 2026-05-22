"""
Script de carga masiva - MotoPartes
Ubicacion: raiz del proyecto (donde esta manage.py)
Ejecucion: python cargar_datos.py
"""

import os

import django
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from acceso.models import (
    CategoriaProducto,
    Empleado,
    Producto,
    Rol,
    Sede,
    Usuarios,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "motopartesetings.settings")
django.setup()


print("Iniciando carga masiva de datos...")
print("=" * 50)

# 1. ROLES
print("\nCreando roles...")
roles_data = [
    {"idRol": 1, "descripcionRol": "Administrador"},
    {"idRol": 2, "descripcionRol": "Cliente"},
    {"idRol": 3, "descripcionRol": "Empleado"},
]
for r in roles_data:
    rol, creado = Rol.objects.get_or_create(
        idRol=r["idRol"], defaults={"descripcionRol": r["descripcionRol"]}
    )
    print(f"  {'Creado' if creado else 'Ya existe'}: {rol.descripcionRol}")

# 2. CATEGORIAS
print("\nCreando categorias...")
categorias_data = [
    {
        "nombreCategoria": "Motor",
        "descripcion": "Partes del motor y componentes internos",
    },
    {
        "nombreCategoria": "Frenos",
        "descripcion": "Pastillas, discos, cables y sistemas de freno",
    },
    {
        "nombreCategoria": "Suspension",
        "descripcion": "Amortiguadores, resortes y horquillas",
    },
    {
        "nombreCategoria": "Electrico",
        "descripcion": "Baterias, luces, reguladores y cableado",
    },
    {
        "nombreCategoria": "Transmision",
        "descripcion": "Cadenas, pinones, coronas y embrague",
    },
    {
        "nombreCategoria": "Carroceria",
        "descripcion": "Plasticos, tapas y partes externas",
    },
    {
        "nombreCategoria": "Escape",
        "descripcion": "Silenciadores, tubos de escape y colectores",
    },
    {
        "nombreCategoria": "Filtros",
        "descripcion": "Filtros de aire, aceite y combustible",
    },
    {
        "nombreCategoria": "Lubricantes",
        "descripcion": "Aceites, grasas y liquidos especiales",
    },
    {
        "nombreCategoria": "Accesorios",
        "descripcion": "Espejos, manubrios, palancas y extras",
    },
]
for cat in categorias_data:
    obj, creado = CategoriaProducto.objects.get_or_create(
        nombreCategoria=cat["nombreCategoria"],
        defaults={"descripcion": cat["descripcion"]},
    )
    print(f"  {'Creada' if creado else 'Ya existe'}: {obj.nombreCategoria}")

# 3. SEDES
print("\nCreando sedes...")
sedes_data = [
    {
        "nombre": "Sede Principal Centro",
        "direccion": "Cra 7 #12-34",
        "ciudad": "Bogota",
        "telefono": "601-2345678",
    },
    {
        "nombre": "Sede Norte",
        "direccion": "Calle 100 #15-20",
        "ciudad": "Bogota",
        "telefono": "601-3456789",
    },
    {
        "nombre": "Sede Sur",
        "direccion": "Av. 68 #38-10",
        "ciudad": "Bogota",
        "telefono": "601-4567890",
    },
    {
        "nombre": "Sede Medellin El Poblado",
        "direccion": "Cra 43A #7-50",
        "ciudad": "Medellin",
        "telefono": "604-5678901",
    },
    {
        "nombre": "Sede Cali Centro",
        "direccion": "Calle 15 #5-30",
        "ciudad": "Cali",
        "telefono": "602-6789012",
    },
    {
        "nombre": "Sede Barranquilla",
        "direccion": "Cra 53 #72-100",
        "ciudad": "Barranquilla",
        "telefono": "605-7890123",
    },
    {
        "nombre": "Sede Bucaramanga",
        "direccion": "Calle 35 #20-15",
        "ciudad": "Bucaramanga",
        "telefono": "607-8901234",
    },
    {
        "nombre": "Sede Pereira",
        "direccion": "Av. Circunvalar #5-20",
        "ciudad": "Pereira",
        "telefono": "606-9012345",
    },
]
for sede in sedes_data:
    obj, creado = Sede.objects.get_or_create(
        nombre=sede["nombre"],
        defaults={
            "direccion": sede["direccion"],
            "ciudad": sede["ciudad"],
            "telefono": sede["telefono"],
            "activa": True,
        },
    )
    print(f"  {'Creada' if creado else 'Ya existe'}: {obj.nombre} - {obj.ciudad}")

# 4. CLIENTES
print("\nCreando clientes...")
rol_cliente = Rol.objects.get(idRol=2)
clientes_data = [
    {
        "nombre": "Carlos",
        "apellidos": "Rodriguez",
        "doc": 1001234567,
        "correo": "carlos.rodriguez@gmail.com",
        "telefono": 3101234567,
        "direccion": "Calle 45 #12-30, Bogota",
    },
    {
        "nombre": "Maria",
        "apellidos": "Gonzalez",
        "doc": 1002345678,
        "correo": "maria.gonzalez@gmail.com",
        "telefono": 3112345678,
        "direccion": "Cra 80 #35-15, Medellin",
    },
    {
        "nombre": "Andres",
        "apellidos": "Martinez",
        "doc": 1003456789,
        "correo": "andres.martinez@gmail.com",
        "telefono": 3123456789,
        "direccion": "Av. 6N #23-10, Cali",
    },
    {
        "nombre": "Luisa",
        "apellidos": "Hernandez",
        "doc": 1004567890,
        "correo": "luisa.hernandez@gmail.com",
        "telefono": 3134567890,
        "direccion": "Calle 72 #50-30, Barranquilla",
    },
    {
        "nombre": "Juan",
        "apellidos": "Lopez",
        "doc": 1005678901,
        "correo": "juan.lopez@gmail.com",
        "telefono": 3145678901,
        "direccion": "Cra 27 #45-20, Bucaramanga",
    },
    {
        "nombre": "Valentina",
        "apellidos": "Perez",
        "doc": 1006789012,
        "correo": "valentina.perez@gmail.com",
        "telefono": 3156789012,
        "direccion": "Av. 30 de Agosto #5-10, Pereira",
    },
    {
        "nombre": "Diego",
        "apellidos": "Sanchez",
        "doc": 1007890123,
        "correo": "diego.sanchez@gmail.com",
        "telefono": 3167890123,
        "direccion": "Calle 19 #8-40, Manizales",
    },
    {
        "nombre": "Camila",
        "apellidos": "Ramirez",
        "doc": 1008901234,
        "correo": "camila.ramirez@gmail.com",
        "telefono": 3178901234,
        "direccion": "Cra 5 #12-50, Cartagena",
    },
    {
        "nombre": "Sebastian",
        "apellidos": "Torres",
        "doc": 1009012345,
        "correo": "sebastian.torres@gmail.com",
        "telefono": 3189012345,
        "direccion": "Calle 10 #3-20, Ibague",
    },
    {
        "nombre": "Isabella",
        "apellidos": "Flores",
        "doc": 1000123456,
        "correo": "isabella.flores@gmail.com",
        "telefono": 3190123456,
        "direccion": "Cra 15 #20-10, Cucuta",
    },
]
for c in clientes_data:
    if not Usuarios.objects.filter(numDocUsuario=c["doc"]).exists():
        Usuarios.objects.create(
            tipoDocUsuario="CC",
            numDocUsuario=c["doc"],
            nombreUsuario=c["nombre"],
            apellidosUsuario=c["apellidos"],
            correoUsuario=c["correo"],
            telefonoUsuario=c["telefono"],
            direccionUsuario=c["direccion"],
            claveUsuario=make_password("Moto1234"),
            estadoUsuario="A",
            idRol=rol_cliente,
        )
    username = c["correo"].split("@")[0]
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            email=c["correo"],
            password="Moto1234",
            first_name=c["nombre"],
            last_name=c["apellidos"],
        )
        print(f"  Creado: {c['nombre']} {c['apellidos']} - usuario: {username}")
    else:
        print(f"  Ya existe: {c['nombre']} {c['apellidos']}")

# 5. EMPLEADOS
print("\nCreando empleados...")
empleados_data = [
    {
        "nombre": "Roberto",
        "apellido": "Vargas",
        "username": "rvargas",
        "email": "rvargas@motopartes.com",
        "cedula": "80123456",
        "cargo": "empleado",
        "telefono": "3201234567",
        "direccion": "Calle 50 #30-10, Bogota",
        "fnac": "1990-05-15",
        "salario": 2500000,
    },
    {
        "nombre": "Patricia",
        "apellido": "Morales",
        "username": "pmorales",
        "email": "pmorales@motopartes.com",
        "cedula": "52234567",
        "cargo": "empleado",
        "telefono": "3212345678",
        "direccion": "Cra 40 #25-20, Medellin",
        "fnac": "1988-09-20",
        "salario": 2500000,
    },
    {
        "nombre": "Fernando",
        "apellido": "Castro",
        "username": "fcastro",
        "email": "fcastro@motopartes.com",
        "cedula": "71345678",
        "cargo": "empleado",
        "telefono": "3223456789",
        "direccion": "Av. 3N #40-30, Cali",
        "fnac": "1992-03-10",
        "salario": 2500000,
    },
    {
        "nombre": "Sandra",
        "apellido": "Jimenez",
        "username": "sjimenez",
        "email": "sjimenez@motopartes.com",
        "cedula": "45456789",
        "cargo": "empleado",
        "telefono": "3234567890",
        "direccion": "Calle 80 #55-40, Bogota",
        "fnac": "1995-07-25",
        "salario": 2500000,
    },
    {
        "nombre": "Miguel",
        "apellido": "Ortega",
        "username": "mortega",
        "email": "mortega@motopartes.com",
        "cedula": "93567890",
        "cargo": "admin",
        "telefono": "3245678901",
        "direccion": "Cra 60 #10-50, Bogota",
        "fnac": "1985-11-30",
        "salario": 4000000,
    },
]
for e in empleados_data:
    if not User.objects.filter(username=e["username"]).exists():
        user = User.objects.create_user(
            username=e["username"],
            email=e["email"],
            password="Empleado1234",
            first_name=e["nombre"],
            last_name=e["apellido"],
            is_staff=(e["cargo"] == "admin"),
        )
        Empleado.objects.create(
            usuario=user,
            cedula=e["cedula"],
            cargo=e["cargo"],
            telefono=e["telefono"],
            direccion=e["direccion"],
            fecha_nacimiento=e["fnac"],
            salario=e["salario"],
        )
        print(
            f"  Creado: {e['nombre']} "
            f"{e['apellido']} "
            f"({e['cargo']}) - "
            f"usuario: {e['username']}"
        )
    else:
        print(f"  Ya existe: {e['username']}")

# 6. PRODUCTOS
print("\nCreando productos...")

productos_data = [
    # MOTOR
    {
        "nombre": "Piston FZ 150cc",
        "precio": 85000,
        "stock": 50,
        "cat": "Motor",
        "estado": "Disponible",
        "desc": "Piston original para moto FZ 150cc, alta durabilidad",
    },
    {
        "nombre": "Ciguenal XR 200",
        "precio": 320000,
        "stock": 20,
        "cat": "Motor",
        "estado": "Disponible",
        "desc": "Ciguenal balanceado para Honda XR 200",
    },
    {
        "nombre": "Culata GN 125",
        "precio": 180000,
        "stock": 15,
        "cat": "Motor",
        "estado": "Disponible",
        "desc": "Culata completa para Suzuki GN 125",
    },
    {
        "nombre": "Eje de levas CB 190",
        "precio": 95000,
        "stock": 30,
        "cat": "Motor",
        "estado": "Disponible",
        "desc": "Eje de levas de precision para Honda CB 190",
    },
    {
        "nombre": "Empaque de motor AKT",
        "precio": 35000,
        "stock": 80,
        "cat": "Motor",
        "estado": "Disponible",
        "desc": "Kit de empaques completo para motores AKT",
    },
    {
        "nombre": "Carburador VM22",
        "precio": 185000,
        "stock": 0,
        "cat": "Motor",
        "estado": "Agotado",
        "desc": "Carburador Mikuni VM22 para motos 125cc",
    },
    # FRENOS
    {
        "nombre": "Pastillas de freno Brembo",
        "precio": 65000,
        "stock": 60,
        "cat": "Frenos",
        "estado": "Disponible",
        "desc": "Pastillas de freno de alta performance Brembo",
    },
    {
        "nombre": "Disco de freno delantero",
        "precio": 120000,
        "stock": 25,
        "cat": "Frenos",
        "estado": "Disponible",
        "desc": "Disco de freno ventilado para motos 150-200cc",
    },
    {
        "nombre": "Cable de freno trasero",
        "precio": 18000,
        "stock": 100,
        "cat": "Frenos",
        "estado": "Disponible",
        "desc": "Cable de freno trasero universal reforzado",
    },
    {
        "nombre": "Liquido de frenos DOT4",
        "precio": 22000,
        "stock": 90,
        "cat": "Frenos",
        "estado": "Disponible",
        "desc": "Liquido de frenos DOT4 500ml",
    },
    {
        "nombre": "Manigueta de freno",
        "precio": 28000,
        "stock": 45,
        "cat": "Frenos",
        "estado": "Disponible",
        "desc": "Manigueta de freno ajustable universal",
    },
    # SUSPENSION
    {
        "nombre": "Amortiguador trasero YSS",
        "precio": 280000,
        "stock": 18,
        "cat": "Suspension",
        "estado": "Disponible",
        "desc": "Amortiguador trasero YSS ajustable",
    },
    {
        "nombre": "Horquilla delantera 150cc",
        "precio": 450000,
        "stock": 8,
        "cat": "Suspension",
        "estado": "Disponible",
        "desc": "Kit horquilla delantera para motos 150cc",
    },
    {
        "nombre": "Resorte de suspension",
        "precio": 55000,
        "stock": 35,
        "cat": "Suspension",
        "estado": "Disponible",
        "desc": "Resorte de suspension trasera reforzado",
    },
    {
        "nombre": "Buje delantero AKT 125",
        "precio": 75000,
        "stock": 22,
        "cat": "Suspension",
        "estado": "Disponible",
        "desc": "Buje delantero original AKT 125",
    },
    # ELECTRICO
    {
        "nombre": "Bateria 12V 7Ah Yuasa",
        "precio": 145000,
        "stock": 30,
        "cat": "Electrico",
        "estado": "Disponible",
        "desc": "Bateria sellada Yuasa 12V 7Ah",
    },
    {
        "nombre": "Regulador de voltaje",
        "precio": 48000,
        "stock": 40,
        "cat": "Electrico",
        "estado": "Disponible",
        "desc": "Regulador rectificador de voltaje universal",
    },
    {
        "nombre": "Bobina de encendido",
        "precio": 62000,
        "stock": 25,
        "cat": "Electrico",
        "estado": "Disponible",
        "desc": "Bobina de encendido de alta energia",
    },
    {
        "nombre": "Faro LED universal",
        "precio": 85000,
        "stock": 20,
        "cat": "Electrico",
        "estado": "Disponible",
        "desc": "Faro LED 12V 35W universal blanco",
    },
    {
        "nombre": "CDI digital Honda",
        "precio": 95000,
        "stock": 15,
        "cat": "Electrico",
        "estado": "Disponible",
        "desc": "CDI digital de alto rendimiento para Honda",
    },
    {
        "nombre": "Bujia NGK CR7HSA",
        "precio": 12000,
        "stock": 150,
        "cat": "Electrico",
        "estado": "Disponible",
        "desc": "Bujia NGK CR7HSA para motos 125-150cc",
    },
    # TRANSMISION
    {
        "nombre": "Cadena 428H 130 eslabones",
        "precio": 48000,
        "stock": 55,
        "cat": "Transmision",
        "estado": "Disponible",
        "desc": "Cadena reforzada 428H para motos sport",
    },
    {
        "nombre": "Corona 37 dientes",
        "precio": 38000,
        "stock": 40,
        "cat": "Transmision",
        "estado": "Disponible",
        "desc": "Corona trasera 37 dientes acero",
    },
    {
        "nombre": "Pinon 14 dientes",
        "precio": 22000,
        "stock": 60,
        "cat": "Transmision",
        "estado": "Disponible",
        "desc": "Pinon delantero 14 dientes",
    },
    {
        "nombre": "Kit transmision completo",
        "precio": 98000,
        "stock": 30,
        "cat": "Transmision",
        "estado": "Disponible",
        "desc": "Kit cadena + corona + pinon para 125cc",
    },
    {
        "nombre": "Disco de embrague GN 125",
        "precio": 45000,
        "stock": 28,
        "cat": "Transmision",
        "estado": "Disponible",
        "desc": "Disco de embrague original para GN 125",
    },
    # CARROCERIA
    {
        "nombre": "Carenaje lateral FZ 150",
        "precio": 75000,
        "stock": 12,
        "cat": "Carroceria",
        "estado": "Disponible",
        "desc": "Carenaje lateral derecho FZ 150 negro",
    },
    {
        "nombre": "Guardabarro trasero",
        "precio": 45000,
        "stock": 20,
        "cat": "Carroceria",
        "estado": "Disponible",
        "desc": "Guardabarro trasero universal negro",
    },
    {
        "nombre": "Tanque de combustible CB",
        "precio": 350000,
        "stock": 5,
        "cat": "Carroceria",
        "estado": "Disponible",
        "desc": "Tanque de combustible para Honda CB series",
    },
    {
        "nombre": "Espejos retrovisores par",
        "precio": 32000,
        "stock": 50,
        "cat": "Carroceria",
        "estado": "Disponible",
        "desc": "Par de espejos retrovisores cromados universales",
    },
    {
        "nombre": "Llanta delantera 90/90-18",
        "precio": 145000,
        "stock": 0,
        "cat": "Carroceria",
        "estado": "Agotado",
        "desc": "Llanta delantera 90/90-18 Pirelli",
    },
    # FILTROS
    {
        "nombre": "Filtro de aire KN",
        "precio": 85000,
        "stock": 35,
        "cat": "Filtros",
        "estado": "Disponible",
        "desc": "Filtro de aire de alto flujo KN lavable",
    },
    {
        "nombre": "Filtro de aceite HF111",
        "precio": 18000,
        "stock": 80,
        "cat": "Filtros",
        "estado": "Disponible",
        "desc": "Filtro de aceite Hiflofiltro HF111",
    },
    {
        "nombre": "Filtro de combustible",
        "precio": 12000,
        "stock": 90,
        "cat": "Filtros",
        "estado": "Disponible",
        "desc": "Filtro de combustible inline universal",
    },
    # LUBRICANTES
    {
        "nombre": "Aceite Motul 10W40 1L",
        "precio": 38000,
        "stock": 100,
        "cat": "Lubricantes",
        "estado": "Disponible",
        "desc": "Aceite de motor 4T Motul 10W40 semi-sintetico",
    },
    {
        "nombre": "Grasa para cadena",
        "precio": 22000,
        "stock": 70,
        "cat": "Lubricantes",
        "estado": "Disponible",
        "desc": "Grasa spray para cadena resistente al agua",
    },
    {
        "nombre": "Aceite horquilla 10W",
        "precio": 28000,
        "stock": 45,
        "cat": "Lubricantes",
        "estado": "Disponible",
        "desc": "Aceite para horquilla delantera 10W 500ml",
    },
    # ACCESORIOS
    {
        "nombre": "Manubrio deportivo CNC",
        "precio": 55000,
        "stock": 25,
        "cat": "Accesorios",
        "estado": "Disponible",
        "desc": "Manubrio deportivo aluminio CNC",
    },
    {
        "nombre": "Palanca de cambios",
        "precio": 35000,
        "stock": 40,
        "cat": "Accesorios",
        "estado": "Disponible",
        "desc": "Palanca de cambios ajustable universal",
    },
    {
        "nombre": "Reposapiés deportivos",
        "precio": 68000,
        "stock": 18,
        "cat": "Accesorios",
        "estado": "Disponible",
        "desc": "Kit reposapiés CNC aluminio antideslizante",
    },
    {
        "nombre": "Tapizado de asiento",
        "precio": 45000,
        "stock": 30,
        "cat": "Accesorios",
        "estado": "Disponible",
        "desc": "Tapizado impermeable universal negro",
    },
    {
        "nombre": "Protector de motor",
        "precio": 92000,
        "stock": 15,
        "cat": "Accesorios",
        "estado": "Disponible",
        "desc": "Protector de carter en aluminio reforzado",
    },
]

creados = 0
for p in productos_data:
    try:
        cat = CategoriaProducto.objects.get(nombreCategoria=p["cat"])
    except CategoriaProducto.DoesNotExist:
        print(f"  SKIP (sin categoria): {p['nombre']}")
        continue
    if not Producto.objects.filter(nombreProducto=p["nombre"]).exists():
        Producto.objects.create(
            nombreProducto=p["nombre"],
            precioProducto=p["precio"],
            stock=p["stock"],
            estadoProducto=p["estado"],
            descripcion=p["desc"],
            idCategoria_Producto=cat,
        )
        creados += 1
        print(f"  Creado: {p['nombre']} - ${p['precio']:,}")
    else:
        print(f"  Ya existe: {p['nombre']}")
print(f"  Total creados: {creados}")

# RESUMEN
print("\n" + "=" * 50)
print("CARGA COMPLETADA")
print("=" * 50)
print(f"  Roles:      {Rol.objects.count()}")
print(f"  Categorias: {CategoriaProducto.objects.count()}")
print(f"  Sedes:      {Sede.objects.count()}")
print(f"  Clientes:   {Usuarios.objects.count()}")
print(f"  Empleados:  {Empleado.objects.count()}")
print(f"  Productos:  {Producto.objects.count()}")
print("")
print("Contrasenas de prueba:")
print("  Clientes:   Moto1234")
print("  Empleados:  Empleado1234")
print("=" * 50)
