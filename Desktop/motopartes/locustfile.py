"""
=============================================================
  PRUEBAS DE CARGA - MOTOPARTES
  Herramienta: Locust
  App: Django con sesiones (CSRF)
  Documento de referencia: Casos de Prueba, Matriz de Resultados
  e Informe de Aceptacion - GTI-F-007 v1.0
  Casos cubiertos:
    CP-NF-007 - Carga concurrente de clientes en tienda
    CP-NF-008 - Carga en panel de administracion
    CP-NF-009 - Estres combinado multi-perfil

  COMO EJECUTAR:
  --------------
  1. Instala locust:
       pip install locust

  2. Corre la interfaz web:
       locust -f locustfile.py --host=http://localhost:8000

  3. Abre en el navegador:
       http://localhost:8089

  4. Modo automatico CP-NF-007 (50 usuarios - ClientePublico):
       locust -f locustfile.py --host=http://localhost:8000 ^
         --headless --users 50 --spawn-rate 5 --run-time 3m ^
         --html reporte_CP_NF_007.html

  5. Modo automatico CP-NF-008 (20 usuarios - AdminUsuario):
       locust -f locustfile.py --host=http://localhost:8000 ^
         --headless --users 20 --spawn-rate 2 --run-time 3m ^
         --html reporte_CP_NF_008.html

  6. Modo automatico CP-NF-009 (100 usuarios - todos los perfiles):
       locust -f locustfile.py --host=http://localhost:8000 ^
         --headless --users 100 --spawn-rate 10 --run-time 5m ^
         --html reporte_CP_NF_009.html

  RESULTADOS ESPERADOS (segun documento GTI-F-007):
  --------------------------------------------------
  CP-NF-007:
    - Tiempo de respuesta promedio < 2 s
    - Tasa de error < 1%
    - Sistema estable sin caidas

  CP-NF-008:
    - Tiempo de respuesta promedio < 3 s
    - Generacion de PDF < 30 s
    - Tasa de error < 2%

  CP-NF-009:
    - Sistema estable con 3 perfiles simultaneos
    - Sin errores HTTP 500
    - p95 < 4 s

  USUARIOS CONFIGURADOS:
  ----------------------
  - ClientePublico   -> usuario: prueba
  - AdminUsuario     -> usuario: juancamilo
  - EmpleadoUsuario  -> usuario: felipe
=============================================================
"""

import random
import re

from locust import HttpUser, between, task


# ---------------------------------------------------------
# UTILIDAD: obtener token CSRF de la respuesta
# ---------------------------------------------------------
def get_csrf_token(response_text):
    """Extrae el csrfmiddlewaretoken del HTML de un formulario Django."""
    match = re.search(r'csrfmiddlewaretoken.*?value=["\'](.+?)["\']', response_text)
    return match.group(1) if match else ""


# ---------------------------------------------------------
# CP-NF-007 - Carga concurrente de clientes en tienda
# Configuracion: 50 usuarios, spawn-rate 5/s, duracion 3 min
# Resultado esperado: p50 < 2 s, error < 1%, sin caidas
# ---------------------------------------------------------
class ClientePublico(HttpUser):
    weight = 3
    wait_time = between(2, 5)
    token = ""

    def on_start(self):
        self.login_cliente()

    def login_cliente(self):
        res = self.client.get("/login/", name="/login [GET]")
        self.token = get_csrf_token(res.text)

        with self.client.post(
            "/login/",
            data={
                "csrfmiddlewaretoken": self.token,
                "username": "prueba",
                "password": "prueba1234",
            },
            headers={"Referer": "http://localhost:8000/login/"},
            catch_response=True,
            name="/login [POST]",
            allow_redirects=True,
        ) as res:
            if res.status_code == 200 and "Cerrar" in res.text:
                res.success()
            else:
                res.failure(f"Login cliente fallo (status {res.status_code})")

    @task(5)
    def ver_tienda(self):
        self.client.get("/productos/", name="/productos [lista]")

    @task(4)
    def ver_producto_detalle(self):
        pk = random.randint(1, 30)
        self.client.get(
            f"/productos/{pk}/",
            name="/productos/:id [detalle]",
            catch_response=True,
        )

    @task(3)
    def ver_inicio(self):
        self.client.get("/", name="/ [inicio]")

    @task(2)
    def agregar_al_carrito(self):
        pk = random.randint(1, 30)
        res = self.client.get(f"/productos/{pk}/", name="/productos/:id [pre-carrito]")
        csrf = get_csrf_token(res.text)

        self.client.post(
            f"/carrito/agregar/{pk}/",
            data={
                "csrfmiddlewaretoken": csrf,
                "cantidad": random.randint(1, 3),
            },
            headers={"Referer": f"http://localhost:8000/productos/{pk}/"},
            name="/carrito/agregar/:id [POST]",
            allow_redirects=True,
        )

    @task(2)
    def ver_carrito(self):
        self.client.get("/carrito/", name="/carrito [ver]")

    @task(1)
    def ver_mis_facturas(self):
        self.client.get("/mis-facturas/", name="/mis-facturas [lista]")

    @task(1)
    def ver_perfil(self):
        self.client.get("/perfil/", name="/perfil [ver]")

    @task(1)
    def checkout(self):
        res = self.client.get("/checkout/", name="/checkout [GET]")
        csrf = get_csrf_token(res.text)

        if csrf:
            self.client.post(
                "/checkout/",
                data={"csrfmiddlewaretoken": csrf},
                headers={"Referer": "http://localhost:8000/checkout/"},
                name="/checkout [POST]",
                allow_redirects=True,
            )

    def on_stop(self):
        self.client.get("/logout/", name="/logout")


# ---------------------------------------------------------
# CP-NF-008 - Carga en panel de administracion
# Configuracion: 20 usuarios, spawn-rate 2/s, duracion 3 min
# Resultado esperado: p50 < 3 s, PDFs < 30 s, error < 2%
# ---------------------------------------------------------
class AdminUsuario(HttpUser):
    weight = 1
    wait_time = between(3, 8)
    token = ""

    def on_start(self):
        self.login_admin()

    def login_admin(self):
        res = self.client.get("/login/", name="/login [GET admin]")
        self.token = get_csrf_token(res.text)

        with self.client.post(
            "/login/",
            data={
                "csrfmiddlewaretoken": self.token,
                "username": "juancamilo",
                "password": "juan1234",
            },
            headers={"Referer": "http://localhost:8000/login/"},
            catch_response=True,
            name="/login [POST admin]",
            allow_redirects=True,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"Login admin fallo (status {res.status_code})")

    @task(4)
    def ver_dashboard(self):
        self.client.get("/panel/", name="/panel [dashboard]")

    @task(4)
    def listar_productos(self):
        self.client.get("/panel/productos/", name="/panel/productos [lista]")

    @task(3)
    def listar_pedidos(self):
        self.client.get("/panel/pedidos/", name="/panel/pedidos [lista]")

    @task(3)
    def ver_pedido_detalle(self):
        pk = random.randint(1, 20)
        self.client.get(
            f"/panel/pedidos/{pk}/",
            name="/panel/pedidos/:id [detalle]",
        )

    @task(2)
    def listar_clientes(self):
        self.client.get("/panel/clientes/", name="/panel/clientes [lista]")

    @task(2)
    def listar_empleados(self):
        self.client.get("/panel/empleados/", name="/panel/empleados [lista]")

    @task(2)
    def listar_categorias(self):
        self.client.get("/panel/categorias/", name="/panel/categorias [lista]")

    @task(2)
    def listar_sedes(self):
        self.client.get("/panel/sedes/", name="/panel/sedes [lista]")

    @task(1)
    def ver_reportes(self):
        self.client.get("/panel/reportes/", name="/panel/reportes [ver]")

    @task(1)
    def reporte_productos_pdf(self):
        with self.client.get(
            "/panel/reportes/productos/pdf/",
            name="/panel/reportes/productos/pdf [descarga]",
            catch_response=True,
            timeout=30,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"PDF productos fallo: {res.status_code}")

    @task(1)
    def reporte_pedidos_pdf(self):
        with self.client.get(
            "/panel/reportes/pedidos/pdf/",
            name="/panel/reportes/pedidos/pdf [descarga]",
            catch_response=True,
            timeout=30,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"PDF pedidos fallo: {res.status_code}")

    @task(1)
    def crear_producto(self):
        res = self.client.get(
            "/panel/productos/nuevo/",
            name="/panel/productos/nuevo [GET]",
        )
        csrf = get_csrf_token(res.text)

        if csrf:
            self.client.post(
                "/panel/productos/nuevo/",
                data={
                    "csrfmiddlewaretoken": csrf,
                    "nombre": f"Producto Test {random.randint(1000, 9999)}",
                    "precio": random.randint(10000, 500000),
                    "stock": random.randint(1, 100),
                },
                headers={"Referer": "http://localhost:8000/panel/productos/nuevo/"},
                name="/panel/productos/nuevo [POST]",
                allow_redirects=True,
            )

    def on_stop(self):
        self.client.get("/logout/", name="/logout [admin]")


# ---------------------------------------------------------
# CP-NF-009 - Estres combinado multi-perfil
# Configuracion: 100 usuarios totales (weight 3:2:1), spawn-rate 10/s, 5 min
# Resultado esperado: sin HTTP 500, p95 < 4 s
# ---------------------------------------------------------
class EmpleadoUsuario(HttpUser):
    weight = 2
    wait_time = between(2, 6)
    token = ""

    def on_start(self):
        self.login_empleado()

    def login_empleado(self):
        res = self.client.get("/empleado/login/", name="/empleado/login [GET]")
        self.token = get_csrf_token(res.text)

        with self.client.post(
            "/empleado/login/",
            data={
                "csrfmiddlewaretoken": self.token,
                "username": "felipe",
                "password": "felipe1234",
            },
            headers={"Referer": "http://localhost:8000/empleado/login/"},
            catch_response=True,
            name="/empleado/login [POST]",
            allow_redirects=True,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"Login empleado fallo: {res.status_code}")

    @task(4)
    def ver_panel_empleado(self):
        self.client.get("/empleado/panel/", name="/empleado/panel [dashboard]")

    @task(3)
    def ver_pedidos_empleado(self):
        self.client.get("/empleado/pedidos/", name="/empleado/pedidos [lista]")

    @task(2)
    def ver_pedido_detalle(self):
        pk = random.randint(1, 20)
        self.client.get(
            f"/empleado/pedidos/{pk}/",
            name="/empleado/pedidos/:id [detalle]",
        )

    @task(2)
    def ver_categorias_empleado(self):
        self.client.get("/empleado/categorias/", name="/empleado/categorias [lista]")

    @task(1)
    def ver_compras_empleado(self):
        self.client.get("/empleado/compras/", name="/empleado/compras [lista]")

    def on_stop(self):
        self.client.get("/logout/", name="/logout [empleado]")