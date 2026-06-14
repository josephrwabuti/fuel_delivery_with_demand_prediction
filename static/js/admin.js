/* ================================================
   FUELFLOW – Admin Dashboard JavaScript
   Handles: sidebar toggle, toast, modals,
            bar animations, table search/filter
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

/* ---- MODAL HELPERS ---- */
function openModal(id)  { document.getElementById(id)?.classList.add('active'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('active'); }

document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay'))
    e.target.classList.remove('active');
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape')
    document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
});

/* ---- TOAST ---- */
function showDashToast(msg, iconClass = 'fa-check-circle', color = 'var(--admin)') {
  const toast = document.getElementById('dashToast');
  const msgEl  = document.getElementById('dashToastMsg');
  const iconEl = toast?.querySelector('i');
  if (!toast || !msgEl) return;
  msgEl.textContent = msg;
  if (iconEl) { iconEl.className = `fas ${iconClass}`; iconEl.style.color = color; }
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}

/* ---- TABLE SEARCH ---- */
function filterTable(tableId, query) {
  const q = query.toLowerCase();
  document.querySelectorAll(`#${tableId} tbody tr`).forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}

/* ---- FILTER BY COLUMN VALUE ---- */
/* colIndex: 0-based column index to match against */
function filterByCol(tableId, colIndex, value) {
  document.querySelectorAll(`#${tableId} tbody tr`).forEach(row => {
    const cell = row.cells[colIndex];
    const cellText = cell ? cell.textContent.trim() : '';
    row.style.display = (value === 'all' || cellText.includes(value)) ? '' : 'none';
  });
}

/* ---- BAR ANIMATION ---- */
function animateBars() {
  document.querySelectorAll('.rb-fill[data-w]').forEach(bar => {
    bar.style.width = '0%';
    bar.style.transition = 'none';
    setTimeout(() => {
      bar.style.transition = 'width 1.2s ease';
      bar.style.width = bar.dataset.w + '%';
    }, 250);
  });
}

/* ---- ON DOM READY ---- */
document.addEventListener('DOMContentLoaded', function () {

  /* Close sidebar nav link on mobile */
  document.querySelectorAll('.nav-item').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 992) closeSidebar();
    });
  });

  /* Animate bars on page load */
  animateBars();

  /* Re-animate bars when scrolled into view */
  document.querySelectorAll('.rb-fill[data-w]').forEach(bar => {
    new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          bar.style.transition = 'width 1.2s ease';
          bar.style.width = bar.dataset.w + '%';
        }
      });
    }, { threshold: 0.3 }).observe(bar);
  });

  /* Smooth page fade in */
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.3s ease';
  setTimeout(() => { document.body.style.opacity = '1'; }, 40);
});

/* ---- REPORT PERIOD SELECTOR ---- */
function updateReportPeriod(period) {
  /* In Django this would reload with a query param:
     window.location.href = '/admin/reports/?period=' + period;
     For now just show a toast */
  const labels = { month: 'This Month', quarter: 'This Quarter', year: 'This Year', all: 'All Time' };
  showDashToast('Report period set to: ' + labels[period], 'fa-chart-bar', 'var(--admin)');
}
