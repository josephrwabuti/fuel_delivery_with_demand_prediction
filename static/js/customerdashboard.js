/* ================================================
   FUELFLOW – Customer Dashboard JavaScript
   Handles: sidebar toggle, toast, modals,
            gauge animation, active nav highlight
   ================================================ */

/* ---- SIDEBAR TOGGLE (mobile) ---- */
function toggleSidebar() {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  sidebar.classList.toggle('open');
  overlay.classList.toggle('active');
}
function closeSidebar() {
  document.getElementById('sidebar')?.classList.remove('open');
  document.getElementById('sidebarOverlay')?.classList.remove('active');
}

/* Close sidebar on nav link click (mobile) */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.nav-item').forEach(link => {
    link.addEventListener('click', function () {
      if (window.innerWidth < 992) closeSidebar();
    });
  });

  /* ---- FUEL GAUGE ANIMATION ---- */
  animateGauge();

  /* ---- TOAST auto-dismiss from Django messages ---- */
  const djangoMsg = document.getElementById('djangoMessage');
  if (djangoMsg) {
    showDashToast(djangoMsg.dataset.message, djangoMsg.dataset.icon || 'fa-check-circle');
  }

  /* ---- STAT CARD counters ---- */
  document.querySelectorAll('.sc-value[data-count]').forEach(el => {
    animateCount(el, parseInt(el.dataset.count));
  });
});

/* ---- TOAST ---- */
function showDashToast(msg, iconClass = 'fa-check-circle', color = 'var(--primary)') {
  const toast = document.getElementById('dashToast');
  const msgEl = document.getElementById('dashToastMsg');
  const iconEl = toast?.querySelector('i');
  if (!toast || !msgEl) return;
  msgEl.textContent = msg;
  if (iconEl) { iconEl.className = `fas ${iconClass}`; iconEl.style.color = color; }
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}

/* ---- GAUGE ANIMATION ---- */
function animateGauge() {
  const arc = document.getElementById('gaugeArc');
  if (!arc) return;
  // Arc total length ≈ 220 (half circle, r=70)
  const total     = 220;
  const pct       = 0.78; // 78% — in Django replace with template var
  const offset    = total - (total * pct);
  arc.style.strokeDashoffset = total; // start empty
  setTimeout(() => {
    arc.style.transition = 'stroke-dashoffset 1.5s ease';
    arc.style.strokeDashoffset = offset;
  }, 400);
}

/* ---- COUNT UP ANIMATION ---- */
function animateCount(el, target) {
  const duration = 1500;
  const step     = target / (duration / 16);
  let current    = 0;
  const timer    = setInterval(() => {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = Math.floor(current).toLocaleString();
  }, 16);
}

/* ---- MODAL HELPERS ---- */
function openModal(id) {
  document.getElementById(id)?.classList.add('active');
}
function closeModal(id) {
  document.getElementById(id)?.classList.remove('active');
}
/* Close modal on overlay click */
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
  }
});
/* Close modal on Escape */
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active')
      .forEach(m => m.classList.remove('active'));
  }
});

/* ---- SMOOTH PAGE LOAD ---- */
document.addEventListener('DOMContentLoaded', function () {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.3s ease';
  setTimeout(() => { document.body.style.opacity = '1'; }, 50);
});


function openTrackModal(
orderId,
status,
created,
assigned,
loaded,
enroute,
arrived,
delivered
){

document.getElementById("trackOrderId").innerHTML="#" + orderId;

const timeline=[

{
title:"Order Placed",
icon:"fa-clipboard-check",
time:created,
done:true
},

{
title:"Driver Assigned",
icon:"fa-user",
time:assigned,
done:[
"Driver Assigned",
"Fuel Loaded",
"En Route",
"Arrived",
"Delivered"
].includes(status)
},

{
title:"Fuel Loaded",
icon:"fa-gas-pump",
time:loaded,
done:[
"Fuel Loaded",
"En Route",
"Arrived",
"Delivered"
].includes(status)
},

{
title:"En Route",
icon:"fa-truck-fast",
time:enroute,
done:[
"En Route",
"Arrived",
"Delivered"
].includes(status)
},

{
title:"Arrived",
icon:"fa-house",
time:arrived,
done:[
"Arrived",
"Delivered"
].includes(status)
},

{
title:"Delivered",
icon:"fa-circle-check",
time:delivered,
done:status=="Delivered"
}

];

let html="";

timeline.forEach(function(item,index){

html+=`

<div class="tt-item">

<div class="tt-left">

<div class="tt-dot ${item.done?'done':'pending'}">

<i class="fas ${item.icon}"></i>

</div>

${
index<timeline.length-1
?
'<div class="tt-line '+(item.done?'done':'')+'"></div>'
:
''
}

</div>

<div class="tt-content">

<div class="tt-title">

${item.title}

</div>

<div class="tt-time">

${item.time && item.time!="None" ? item.time : "Waiting..."}

</div>

</div>

</div>

`;

});

document.getElementById("trackTimeline").innerHTML=html;

document.getElementById("trackModal").classList.add("active");

}