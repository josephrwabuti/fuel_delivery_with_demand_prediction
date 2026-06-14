/* ================================================
   FUELFLOW – Driver Dashboard JavaScript
   Handles: sidebar, online toggle, toast,
            bar animations, modal, stepper sync
   ================================================ */

/* ---- SIDEBAR ---- */
function toggleSidebar() {
  document.getElementById('sidebar')?.classList.toggle('open');
  document.getElementById('sidebarOverlay')?.classList.toggle('active');
}
function closeSidebar() {
  document.getElementById('sidebar')?.classList.remove('open');
  document.getElementById('sidebarOverlay')?.classList.remove('active');
}

/* ---- ONLINE / OFFLINE TOGGLE ---- */
let isOnline = true;

function toggleOnlineStatus() {
  isOnline = !isOnline;

  /* Topbar toggle */
  const toggle = document.getElementById('onlineToggle');
  const dot    = document.getElementById('otDot');
  const label  = document.getElementById('otLabel');

  if (toggle && dot && label) {
    if (isOnline) {
      toggle.classList.remove('offline');
      dot.style.background   = 'var(--success)';
      dot.style.boxShadow    = '0 0 6px rgba(34,197,94,0.6)';
      label.textContent      = 'Online';
    } else {
      toggle.classList.add('offline');
      dot.style.background   = 'var(--text-muted)';
      dot.style.boxShadow    = 'none';
      label.textContent      = 'Offline';
    }
  }

  /* Sidebar dot */
  const sbDot   = document.getElementById('sidebarStatusDot');
  const sbLabel = document.getElementById('sidebarStatusLabel');
  if (sbDot && sbLabel) {
    sbDot.className = 'status-dot ' + (isOnline ? 'online' : 'offline');
    sbLabel.style.color = isOnline ? 'var(--success)' : 'var(--text-muted)';
    sbLabel.textContent = isOnline ? 'Online' : 'Offline';
  }

  /* Availability checkbox on profile page */
  const availToggle = document.getElementById('availToggle');
  if (availToggle) availToggle.checked = isOnline;

  showDashToast(
    isOnline ? 'You are now Online — ready for orders' : 'You are now Offline — no new orders',
    isOnline ? 'fa-circle-check' : 'fa-circle-xmark',
    isOnline ? 'var(--success)' : 'var(--text-muted)'
  );
}

/* ---- TOAST ---- */
function showDashToast(msg, iconClass = 'fa-check-circle', color = 'var(--driver)') {
  const toast = document.getElementById('dashToast');
  const msgEl = document.getElementById('dashToastMsg');
  const iconEl = toast?.querySelector('i');
  if (!toast || !msgEl) return;
  msgEl.textContent = msg;
  if (iconEl) { iconEl.className = `fas ${iconClass}`; iconEl.style.color = color; }
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}

/* ---- BAR CHART ANIMATION ---- */
function animateBars() {
  document.querySelectorAll('.eb-fill[data-w]').forEach(bar => {
    bar.style.width = '0%';
    bar.style.transition = 'none';
    setTimeout(() => {
      bar.style.transition = 'width 1.1s ease';
      bar.style.width = bar.dataset.w + '%';
    }, 300);
  });
}

/* ---- MODAL HELPERS ---- */
function openModal(id)  { document.getElementById(id)?.classList.add('active'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('active'); }

document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) e.target.classList.remove('active');
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
});

/* ---- ON DOM READY ---- */
document.addEventListener('DOMContentLoaded', function () {
  /* Close sidebar on nav click (mobile) */
  document.querySelectorAll('.nav-item').forEach(link => {
    link.addEventListener('click', () => { if (window.innerWidth < 992) closeSidebar(); });
  });

  /* Animate bars */
  animateBars();

  /* Smooth page fade in */
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.3s ease';
  setTimeout(() => { document.body.style.opacity = '1'; }, 40);

  /* Intersection observer for bars (re-animate when scrolled into view) */
  const barContainer = document.querySelector('.earnings-bar');
  if (barContainer) {
    new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) animateBars(); });
    }, { threshold: 0.3 }).observe(barContainer);
  }
});
