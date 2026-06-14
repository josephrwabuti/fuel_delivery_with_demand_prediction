/* ================================================
   FUELFLOW – Authentication JavaScript
   ================================================ */

const wrapper = document.getElementById('authWrapper');

/* ---- PANEL SWITCHING ---- */
function activateSignUp() {
  wrapper.classList.add('right-panel-active');
}
function activateSignIn() {
  wrapper.classList.remove('right-panel-active');
}

/* ---- PASSWORD VISIBILITY TOGGLE ---- */
function togglePw(inputId, btn) {
  const input = document.getElementById(inputId);
  const icon  = btn.querySelector('i');
  if (input.type === 'password') {
    input.type = 'text';
    icon.classList.replace('fa-eye-slash', 'fa-eye');
  } else {
    input.type = 'password';
    icon.classList.replace('fa-eye', 'fa-eye-slash');
  }
}

/* ---- PASSWORD STRENGTH ---- */
function checkStrength(pw) {
  let score = 0;
  if (pw.length >= 8)              score++;
  if (/[A-Z]/.test(pw))            score++;
  if (/[0-9]/.test(pw))            score++;
  if (/[^A-Za-z0-9]/.test(pw))     score++;
  return score; // 0-4
}

const suPwInput = document.getElementById('suPassword');
if (suPwInput) {
  // Build strength bar dynamically
  const group = suPwInput.closest('.input-group-ff');
  const strengthEl = document.createElement('div');
  strengthEl.className = 'pw-strength';
  strengthEl.innerHTML = '<div class="ps-bar" id="pb1"></div><div class="ps-bar" id="pb2"></div><div class="ps-bar" id="pb3"></div><div class="ps-bar" id="pb4"></div>';
  group.insertAdjacentElement('afterend', strengthEl);

  suPwInput.addEventListener('input', function () {
    const score  = checkStrength(this.value);
    const bars   = ['pb1','pb2','pb3','pb4'].map(id => document.getElementById(id));
    const levels = ['weak','fair','good','strong'];
    strengthEl.classList.toggle('visible', this.value.length > 0);
    bars.forEach((bar, i) => {
      bar.className = 'ps-bar';
      if (i < score) bar.classList.add(levels[score - 1]);
    });
  });
}

/* ---- TOAST ---- */
function showToast(msg, icon = 'fa-check-circle', color = '#4cd164') {
  const toast = document.getElementById('toastFF');
  const msgEl = document.getElementById('toastMsg');
  const iconEl = toast.querySelector('i');
  msgEl.textContent = msg;
  iconEl.className = `fas ${icon} me-2`;
  iconEl.style.color = color;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

/* ---- FORM VALIDATION ---- */
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function shakeInput(input) {
  input.style.borderColor = '#ef4444';
  input.style.animation   = 'shake 0.4s ease';
  setTimeout(() => {
    input.style.borderColor = '';
    input.style.animation   = '';
  }, 500);
}

// Inject shake keyframe
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
@keyframes shake {
  0%,100% { transform: translateX(0); }
  20%      { transform: translateX(-8px); }
  40%      { transform: translateX(8px); }
  60%      { transform: translateX(-5px); }
  80%      { transform: translateX(5px); }
}
@keyframes btnSuccess {
  0%   { transform: scale(1); }
  40%  { transform: scale(0.96); }
  70%  { transform: scale(1.03); }
  100% { transform: scale(1); }
}
`;
document.head.appendChild(shakeStyle);

/* ---- SIGN IN HANDLER ---- */
function handleSignIn(btn) {
  const form    = btn.closest('form');
  const emailEl = form.querySelector('input[type="email"]');
  const pwEl    = form.querySelector('input[type="password"]');
  let   valid   = true;

  if (!validateEmail(emailEl.value.trim())) {
    shakeInput(emailEl); valid = false;
  }
  if (pwEl.value.length < 6) {
    shakeInput(pwEl); valid = false;
  }
  if (!valid) {
    showToast('Please check your credentials.', 'fa-exclamation-circle', '#ef4444');
    return;
  }

  // Loading state
  const original = btn.innerHTML;
  btn.classList.add('loading');
  btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>SIGNING IN...';

  setTimeout(() => {
    btn.classList.remove('loading');
    btn.innerHTML = '<i class="fas fa-check me-2"></i>WELCOME BACK!';
    btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
    btn.style.animation  = 'btnSuccess 0.4s ease';
    showToast('Signed in successfully! Redirecting…');
    setTimeout(() => {
      btn.innerHTML        = original;
      btn.style.background = '';
      btn.style.animation  = '';
      // In a real Django app: window.location.href = '/dashboard/';
    }, 2500);
  }, 1400);
}

/* ---- SIGN UP HANDLER ---- */
function handleSignUp(btn) {
  const form    = btn.closest('form');
  const nameEl  = form.querySelector('input[type="text"]');
  const emailEl = form.querySelector('input[type="email"]');
  const pwEl    = form.querySelector('input[type="password"]');
  let   valid   = true;

  if (nameEl.value.trim().length < 2) {
    shakeInput(nameEl); valid = false;
  }
  if (!validateEmail(emailEl.value.trim())) {
    shakeInput(emailEl); valid = false;
  }
  if (pwEl.value.length < 6) {
    shakeInput(pwEl); valid = false;
  }
  if (!valid) {
    showToast('Please fill in all fields correctly.', 'fa-exclamation-circle', '#ef4444');
    return;
  }

  const original = btn.innerHTML;
  btn.classList.add('loading');
  btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>CREATING ACCOUNT...';

  setTimeout(() => {
    btn.classList.remove('loading');
    btn.innerHTML = '<i class="fas fa-check me-2"></i>ACCOUNT CREATED!';
    btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
    btn.style.animation  = 'btnSuccess 0.4s ease';
    showToast('Account created! Welcome to FuelFlow 🎉');
    setTimeout(() => {
      // Switch back to sign-in panel after successful signup
      activateSignIn();
      btn.innerHTML        = original;
      btn.style.background = '';
      btn.style.animation  = '';
      // In real Django: window.location.href = '/login/';
    }, 2500);
  }, 1600);
}

/* ---- KEYBOARD ACCESSIBILITY ---- */
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') activateSignIn();
});

/* ---- RIPPLE EFFECT ON BUTTONS ---- */
document.querySelectorAll('.btn-submit, .btn-overlay').forEach(btn => {
  btn.addEventListener('click', function (e) {
    const rect   = btn.getBoundingClientRect();
    const ripple = document.createElement('span');
    const size   = Math.max(rect.width, rect.height);
    ripple.style.cssText = `
      position: absolute;
      width: ${size}px; height: ${size}px;
      left: ${e.clientX - rect.left - size/2}px;
      top:  ${e.clientY - rect.top  - size/2}px;
      background: rgba(255,255,255,0.25);
      border-radius: 50%;
      transform: scale(0);
      animation: rippleAnim 0.55s linear;
      pointer-events: none;
    `;
    btn.style.position = 'relative';
    btn.style.overflow = 'hidden';
    btn.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove());
  });
});

const rippleCSS = document.createElement('style');
rippleCSS.textContent = `
@keyframes rippleAnim {
  to { transform: scale(4); opacity: 0; }
}
`;
document.head.appendChild(rippleCSS);

/* ---- INPUT FLOAT LABEL EFFECT ---- */
document.querySelectorAll('.ff-input').forEach(input => {
  input.addEventListener('focus', function () {
    const icon = this.parentElement.querySelector('.input-icon');
    if (icon) icon.style.color = '#4361ee';
  });
  input.addEventListener('blur', function () {
    const icon = this.parentElement.querySelector('.input-icon');
    if (icon) icon.style.color = '';
  });
});
