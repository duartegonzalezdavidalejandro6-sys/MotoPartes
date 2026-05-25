document.addEventListener('DOMContentLoaded', function () {

  // ── Referencias ──
  const grid        = document.getElementById('productos-grid');
  const contador    = document.getElementById('count-visible');
  const noResults   = document.getElementById('no-results');
  const buscador    = document.getElementById('buscador');
  const sliderPrecio = document.getElementById('filtro-precio');
  const precioValor  = document.getElementById('precio-valor');
  const selectOrden  = document.getElementById('orden');

  // ── Estado global de filtros ──
  window._filtros = {
    busqueda:  '',
    categoria: 'todos',
    precio:    100000000,
    estado:    'todos',
    orden:     'default'
  };

  // ── Función principal ──
  function aplicarFiltros() {
    if (!grid) return;
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.prod-card'));
    var visibles = [];

    cards.forEach(function(card) {
      var nombre    = (card.getAttribute('data-nombre')    || '').toLowerCase();
      var categoria = (card.getAttribute('data-categoria') || '').toLowerCase().trim();
      var precio    = parseFloat(card.getAttribute('data-precio')) || 0;
      var estadoProd = (card.getAttribute('data-estado')  || '').toLowerCase().trim();

      var okBusqueda  = window._filtros.busqueda === '' || nombre.indexOf(window._filtros.busqueda) !== -1;
      var okCategoria = window._filtros.categoria === 'todos' || categoria === window._filtros.categoria.toLowerCase();
      var okPrecio    = precio <= window._filtros.precio;
      var okEstado    = window._filtros.estado === 'todos' || estadoProd === window._filtros.estado.toLowerCase();

      if (okBusqueda && okCategoria && okPrecio && okEstado) {
        card.style.display = '';
        visibles.push(card);
      } else {
        card.style.display = 'none';
      }
    });

    // Ordenar
    if (window._filtros.orden === 'precio-asc') {
      visibles.sort(function(a, b) {
        return parseFloat(a.getAttribute('data-precio')) - parseFloat(b.getAttribute('data-precio'));
      });
    } else if (window._filtros.orden === 'precio-desc') {
      visibles.sort(function(a, b) {
        return parseFloat(b.getAttribute('data-precio')) - parseFloat(a.getAttribute('data-precio'));
      });
    } else if (window._filtros.orden === 'nombre') {
      visibles.sort(function(a, b) {
        return (a.getAttribute('data-nombre') || '').localeCompare(b.getAttribute('data-nombre') || '');
      });
    }
    visibles.forEach(function(c) { grid.appendChild(c); });

    if (contador) contador.textContent = visibles.length;
    if (noResults) noResults.style.display = visibles.length === 0 ? 'block' : 'none';
  }

  // ── Exponer funciones globales que el HTML llama con onclick/oninput ──

  window.filtrar = function() {
    if (buscador)    window._filtros.busqueda = buscador.value.toLowerCase().trim();
    if (sliderPrecio) window._filtros.precio  = parseInt(sliderPrecio.value);
    if (selectOrden)  window._filtros.orden   = selectOrden.value;
    aplicarFiltros();
  };

  window.toggleFiltro = function(label, tipo, valor) {
    // Desactivar otros del mismo grupo
    var grupo = label.closest('.filtro-opciones');
    if (grupo) {
      grupo.querySelectorAll('.filtro-check').forEach(function(l) {
        l.classList.remove('active');
      });
    }
    label.classList.add('active');
    if (tipo === 'categoria') window._filtros.categoria = valor;
    if (tipo === 'estado')    window._filtros.estado    = valor;
    aplicarFiltros();
  };

  window.actualizarPrecio = function() {
    if (!sliderPrecio) return;
    window._filtros.precio = parseInt(sliderPrecio.value);
    if (precioValor) precioValor.textContent = '$' + window._filtros.precio.toLocaleString('es-CO');
    aplicarFiltros();
  };

  window.limpiarFiltros = function() {
    if (buscador)     buscador.value = '';
    if (sliderPrecio) sliderPrecio.value = 100000000;
    if (selectOrden)  selectOrden.value = 'default';
    if (precioValor)  precioValor.textContent = '$100.000.000';

    document.querySelectorAll('.filtro-opciones').forEach(function(grupo) {
      grupo.querySelectorAll('.filtro-check').forEach(function(l) { l.classList.remove('active'); });
      var primero = grupo.querySelector('.filtro-check');
      if (primero) primero.classList.add('active');
    });

    window._filtros = { busqueda: '', categoria: 'todos', precio: 100000000, estado: 'todos', orden: 'default' };
    aplicarFiltros();
  };

  // ── Carrito ──
  window.agregarCarrito = function(productoId, nombre, precio) {
    var csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    var token = csrfInput ? csrfInput.value : '';
    if (!token) {
      token = document.cookie.split(';').map(function(c){return c.trim();})
        .find(function(c){return c.startsWith('csrftoken=');});
      token = token ? token.split('=')[1] : '';
    }

    fetch('/carrito/agregar/' + productoId + '/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': token,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'cantidad=1'
    })
    .then(function(r) {
      if (r.redirected) { window.location.href = '/login/'; return null; }
      return r.json();
    })
    .then(function(data) {
      if (!data) return;
      mostrarToast(data.ok
        ? '✅ "' + nombre + '" agregado al carrito'
        : '❌ No se pudo agregar', !data.ok);
    })
    .catch(function() { window.location.href = '/login/'; });
  };

  window.mostrarToast = function(mensaje, esError) {
    var toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = mensaje;
    toast.style.background = esError ? '#e63946' : '#27ae60';
    toast.classList.add('show');
    setTimeout(function() { toast.classList.remove('show'); }, 3000);
  };

  // ── Ejecutar al cargar ──
  aplicarFiltros();
});
