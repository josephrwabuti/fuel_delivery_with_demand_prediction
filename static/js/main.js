/* ============================================
   FUELFLOW – Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ---- NAVBAR SCROLL ---- */
  const nav = document.getElementById('mainNav');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 50);
  });

  /* ---- BACK TO TOP ---- */
  const btt = document.getElementById('backToTop');
  window.addEventListener('scroll', () => {
    btt.classList.toggle('visible', window.scrollY > 400);
  });
  btt.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---- COUNTER ANIMATION ---- */
  function animateCounter(el) {
    const target = parseInt(el.dataset.count, 10);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = Math.floor(current).toLocaleString();
    }, 16);
  }

  const counters = document.querySelectorAll('.stat-number');
  let countersStarted = false;
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !countersStarted) {
        countersStarted = true;
        counters.forEach(animateCounter);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => counterObserver.observe(c));

  /* ---- AOS-LIKE SCROLL REVEAL ---- */
  const aosEls = document.querySelectorAll('[data-aos]');
  const aosObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = entry.target.dataset.aosDelay || 0;
        setTimeout(() => {
          entry.target.classList.add('aos-animate');
        }, parseInt(delay));
        aosObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  aosEls.forEach(el => aosObserver.observe(el));

  /* ---- FUEL LEVEL ANIMATION ---- */
  const fuelFill = document.getElementById('fuelFill');
  const fuelPercent = document.getElementById('fuelPercent');
  if (fuelFill) {
    let lvl = 78;
    setInterval(() => {
      lvl = 60 + Math.round(Math.random() * 30);
      fuelFill.style.width = lvl + '%';
      if (fuelPercent) fuelPercent.textContent = lvl + '%';
    }, 4000);
  }

  /* ---- AI BAR CHART ANIMATE ---- */
  const aiBars = document.querySelectorAll('.ai-bar, .ai-bar.predicted, .ai-bar.predicted-only');
  const originalHeights = Array.from(aiBars).map(b => b.style.height);

  aiBars.forEach(bar => { bar.style.height = '0%'; });

  const barObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        aiBars.forEach((bar, i) => {
          setTimeout(() => {
            bar.style.transition = 'height 0.8s ease';
            bar.style.height = originalHeights[i];
          }, i * 80);
        });
        barObserver.disconnect();
      }
    });
  }, { threshold: 0.3 });

  const chartEl = document.querySelector('.ai-bars');
  if (chartEl) barObserver.observe(chartEl);

  /* ---- SMOOTH SCROLL FOR ANCHOR LINKS ---- */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = 80;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
        // close mobile nav if open
        const navMenu = document.getElementById('navMenu');
        if (navMenu && navMenu.classList.contains('show')) {
          navMenu.classList.remove('show');
        }
      }
    });
  });

  /* ---- NAVBAR ACTIVE LINK ON SCROLL ---- */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      if (window.scrollY >= section.offsetTop - 120) {
        current = section.getAttribute('id');
      }
    });
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) {
        link.classList.add('active');
      }
    });
  });

  /* ---- CONTACT FORM FAKE SUBMIT ---- */
  const submitBtn = document.querySelector('.contact-form-card .btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', function () {
      const inputs = document.querySelectorAll('.cf-input');
      let hasValues = false;
      inputs.forEach(i => { if (i.value.trim()) hasValues = true; });
      if (hasValues) {
        submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Message Sent!';
        submitBtn.style.background = '#27ae60';
        setTimeout(() => {
          submitBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Send Message';
          submitBtn.style.background = '';
          inputs.forEach(i => { i.value = ''; });
        }, 3000);
      }
    });
  }

  /* ---- PARTICLES ---- */
  const canvas = document.createElement('canvas');
  const particlesContainer = document.getElementById('particles');
  if (particlesContainer) {
    canvas.style.position = 'absolute';
    canvas.style.inset = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.opacity = '0.35';
    particlesContainer.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let W, H;

    function resize() {
      W = canvas.width = particlesContainer.offsetWidth;
      H = canvas.height = particlesContainer.offsetHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const dots = Array.from({ length: 60 }, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.5 + 0.5,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
    }));

    function drawParticles() {
      ctx.clearRect(0, 0, W, H);
      dots.forEach(d => {
        d.x += d.vx;
        d.y += d.vy;
        if (d.x < 0 || d.x > W) d.vx *= -1;
        if (d.y < 0 || d.y > H) d.vy *= -1;
        ctx.beginPath();
        ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(232, 93, 4, 0.6)';
        ctx.fill();
      });
      // Connect nearby dots
      dots.forEach((a, i) => {
        dots.slice(i + 1).forEach(b => {
          const dist = Math.hypot(a.x - b.x, a.y - b.y);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.strokeStyle = `rgba(232,93,4,${0.12 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        });
      });
      requestAnimationFrame(drawParticles);
    }
    drawParticles();
  }

});
