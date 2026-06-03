// ── MODAL LOGIN ──
function openModal() {
  document.getElementById('loginModal').classList.add('open');
}

function closeModal() {
  document.getElementById('loginModal').classList.remove('open');
}

// Cerrar modal al hacer click fuera
document.getElementById('loginModal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

// Cerrar con Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeModal();
});

// ── NAVEGACIÓN ACTIVA ──
const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('section[id], footer[id]');

// Click en nav
navItems.forEach(item => {
  item.addEventListener('click', function () {
    navItems.forEach(i => i.classList.remove('active'));
    this.classList.add('active');
    const target = this.getAttribute('href');
    if (target && target.startsWith('#')) {
      const el = document.querySelector(target);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Scroll activo en nav
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navItems.forEach(item => {
        item.classList.toggle('active', item.getAttribute('href') === '#' + id);
      });
    }
  });
}, { threshold: 0.3 });

sections.forEach(section => observer.observe(section));

// ── ABRIR MODAL SI HAY ERROR DE LOGIN ──
document.addEventListener('DOMContentLoaded', function () {
  const hasError = document.querySelector('.form-error');
  if (hasError) openModal();
});
