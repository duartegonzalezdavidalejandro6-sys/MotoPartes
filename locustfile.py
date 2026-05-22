"""
=============================================================
  PRUEBAS DE CARGA - MOTOPARTES
  Herramienta: Locust
  App: Django con sesiones (CSRF)
  CÓMO EJECUTAR:
  --------------
  1. Instala locust:
       pip install locust
  2. Corre la interfaz web:
       locust -f locustfile.py --host=http://localhost:8000
  3. Abre en el navegador:
       http://localhost:8089
  4. O modo automático sin interfaz:
       locust -f locustfile.py --host=http://localhost:8000 \
         --headless --users 50 --spawn-rate 5 --run-time 3m \
         --html reporte.html
  USUARIOS SIMULADOS:
  -------------------
  - ClientePublico   → navega tienda, agrega al carrito, hace checkout
  - AdminUsuario     → usa el panel de administración
  - EmpleadoUsuario  → usa el panel de empleado
=============================================================
"""

import random
import re

from locust import HttpUser, between, events, task


# ─────────────────────────────────────────────
# UTILIDAD: obtener token CSRF de la respuesta
# ─────────────────────────────────────────────
def get_csrf_token(response_text):
    """Extrae el csrfmiddlewaretoken del HTML de un formulario Django."""
    match = re.search(r'csrfmiddlewaretoken.*?value=["\'](.+?)["\']', response_text)
    return match.group(1) if match else ""


# ─────────────────────────────────────────────
# USUARIO 1: Cliente público
# Simula un cliente que navega la tienda,
# agrega productos al carrito y hace checkout
# ─────────────────────────────────────────────
class ClientePublico(HttpUser):
    weight = 3  # El más común — 3x más que Admin
    wait_time = between(2, 5)
    token = ""

    def on_start(self):
        """Login como cliente al iniciar."""
        self.login_cliente()

    def login_cliente(self):
        # 1. Obtener página de login y extraer CSRF
        res = self.client.get("/login/", name="/login [GET]")
        self.token = get_csrf_token(res.text)

        # 2. Hacer login con credenciales de prueba
        # ⚠️ CAMBIA estas credenciales por un usuario real de tu BD
        with self.client.post(
            "/login/",
            data={
                "csrfmiddlewaretoken": self.token,
                "username": "clienteprueba",  # ← cambia esto
                "password": "1234",  # ← cambia esto
            },
            headers={"Referer": "http://localhost:8000/login/"},
            catch_response=True,
            name="/login [POST]",
            allow_redirects=True,
        ) as res:
            if res.status_code == 200 and "Cerrar" in res.text:
                res.success()
            else:
                # Si falla el login, intenta como usuario anónimo
                res.failure(f"Login cliente falló (status {res.status_code})")

    # ── Tareas de navegación pública ──

    @task(5)
    def ver_tienda(self):
        """Página principal de productos — la más visitada."""
        self.client.get("/productos/", name="/productos [lista]")

    @task(4)
    def ver_producto_detalle(self):
        """Ver detalle de un producto al azar."""
        pk = random.randint(1, 30)  # ajusta el rango según cuántos productos tengas
        self.client.get(
            f"/productos/{pk}/",
            name="/productos/:id [detalle]",
            catch_response=True,
        )

    @task(3)
    def ver_inicio(self):
        """Página de inicio."""
        self.client.get("/", name="/ [inicio]")

    @task(2)
    def agregar_al_carrito(self):
        """Agrega un producto al carrito."""
        pk = random.randint(1, 30)

        # Primero obtén el CSRF del detalle del producto
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
        """Ver el carrito de compras."""
        self.client.get("/carrito/", name="/carrito [ver]")

    @task(1)
    def ver_mis_facturas(self):
        """Ver historial de facturas del usuario."""
        self.client.get("/mis-facturas/", name="/mis-facturas [lista]")

    @task(1)
    def ver_perfil(self):
        """Ver perfil del usuario."""
        self.client.get("/perfil/", name="/perfil [ver]")

    @task(1)
    def checkout(self):
        """Simula el proceso de checkout."""
        res = self.client.get("/checkout/", name="/checkout [GET]")
        csrf = get_csrf_token(res.text)

        if csrf:
            self.client.post(
                "/checkout/",
                data={
                    "csrfmiddlewaretoken": csrf,
                    # Agrega aquí los campos reales de tu form de checkout
                },
                headers={"Referer": "http://localhost:8000/checkout/"},
                name="/checkout [POST]",
                allow_redirects=True,
            )

    def on_stop(self):
        self.client.get("/logout/", name="/logout")


# ─────────────────────────────────────────────
# USUARIO 2: Administrador
# Simula un admin usando el panel de gestión
# ─────────────────────────────────────────────
class AdminUsuario(HttpUser):
    weight = 1  # Menos frecuente
    wait_time = between(3, 8)
    token = ""

    def on_start(self):
        self.login_admin()

    def login_admin(self):
        res = self.client.get("/login/", name="/login [GET admin]")
        self.token = get_csrf_token(res.text)

        # ⚠️ CAMBIA estas credenciales por un superusuario real de tu BD
        with self.client.post(
            "/login/",
            data={
                "csrfmiddlewaretoken": self.token,
                "username": "admin",  # ← cambia esto
                "password": "admin123",  # ← cambia esto
            },
            headers={"Referer": "http://localhost:8000/login/"},
            catch_response=True,
            name="/login [POST admin]",
            allow_redirects=True,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"Login admin falló (status {res.status_code})")

    # ── Tareas del panel admin ──

    @task(4)
    def ver_dashboard(self):
        """Ver el panel principal."""
        self.client.get("/panel/", name="/panel [dashboard]")

    @task(4)
    def listar_productos(self):
        """Ver lista de productos en panel."""
        self.client.get("/panel/productos/", name="/panel/productos [lista]")

    @task(3)
    def listar_pedidos(self):
        """Ver pedidos."""
        self.client.get("/panel/pedidos/", name="/panel/pedidos [lista]")

    @task(3)
    def ver_pedido_detalle(self):
        """Ver detalle de un pedido al azar."""
        pk = random.randint(1, 20)
        self.client.get(
            f"/panel/pedidos/{pk}/",
            name="/panel/pedidos/:id [detalle]",
        )

    @task(2)
    def listar_clientes(self):
        """Ver clientes registrados."""
        self.client.get("/panel/clientes/", name="/panel/clientes [lista]")

    @task(2)
    def listar_empleados(self):
        """Ver empleados."""
        self.client.get("/panel/empleados/", name="/panel/empleados [lista]")

    @task(2)
    def listar_categorias(self):
        self.client.get("/panel/categorias/", name="/panel/categorias [lista]")

    @task(2)
    def listar_sedes(self):
        self.client.get("/panel/sedes/", name="/panel/sedes [lista]")

    @task(1)
    def ver_reportes(self):
        """Ver página de reportes — carga pesada."""
        self.client.get("/panel/reportes/", name="/panel/reportes [ver]")

    @task(1)
    def reporte_productos_pdf(self):
        """Descargar reporte PDF de productos — operación costosa."""
        with self.client.get(
            "/panel/reportes/productos/pdf/",
            name="/panel/reportes/productos/pdf [descarga]",
            catch_response=True,
            timeout=30,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"PDF productos falló: {res.status_code}")

    @task(1)
    def reporte_pedidos_pdf(self):
        """Descargar reporte PDF de pedidos."""
        with self.client.get(
            "/panel/reportes/pedidos/pdf/",
            name="/panel/reportes/pedidos/pdf [descarga]",
            catch_response=True,
            timeout=30,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"PDF pedidos falló: {res.status_code}")

    @task(1)
    def crear_producto(self):
        """Simula crear un producto nuevo."""
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
                    # Agrega los demás campos requeridos por tu modelo
                },
                headers={"Referer": "http://localhost:8000/panel/productos/nuevo/"},
                name="/panel/productos/nuevo [POST]",
                allow_redirects=True,
            )

    def on_stop(self):
        self.client.get("/logout/", name="/logout [admin]")


# ─────────────────────────────────────────────
# USUARIO 3: Empleado
# Simula un empleado usando su panel
# ─────────────────────────────────────────────
class EmpleadoUsuario(HttpUser):
    weight = 2
    wait_time = between(2, 6)
    token = ""

    def on_start(self):
        self.login_empleado()

    def login_empleado(self):
        res = self.client.get("/empleado/login/", name="/empleado/login [GET]")
        self.token = get_csrf_token(res.text)

        # ⚠️ CAMBIA estas credenciales por un empleado real de tu BD
        with self.client.post(
            "/empleado/login/",
            data={
                "csrfmiddlewaretoken": self.token,
                "username": "empleado1",  # ← cambia esto
                "password": "empleado123",  # ← cambia esto
            },
            headers={"Referer": "http://localhost:8000/empleado/login/"},
            catch_response=True,
            name="/empleado/login [POST]",
            allow_redirects=True,
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure(f"Login empleado falló: {res.status_code}")

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


# ─────────────────────────────────────────────
# EVENTOS: estadísticas al terminar
# ─────────────────────────────────────────────
@events.quitting.add_listener
def resumen_final(environment, **kwargs):
    stats = environment.stats.total
    print("\n" + "=" * 50)
    print("📊  RESUMEN DE LA PRUEBA DE CARGA")
    print("=" * 50)
    print(f"  Total requests     : {stats.num_requests}")
    print(f"  Fallos             : {stats.num_failures}")
    print(f"  Tasa de error      : {stats.fail_ratio * 100:.2f}%")
    print(f"  RPS promedio       : {stats.current_rps:.1f}")
    print(f"  Tiempo resp. medio : {stats.avg_response_time:.0f} ms")
    print(f"  Tiempo resp. p95   : {stats.get_response_time_percentile(0.95):.0f} ms")
    print(f"  Tiempo resp. máx   : {stats.max_response_time:.0f} ms")
    print("=" * 50)
