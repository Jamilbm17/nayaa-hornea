document.documentElement.classList.add('js');

// Luces navideñas que parpadean
const lights = document.querySelector('.lights');
if (lights) {
  const colors = ['#ffd98a', '#ff7a6b', '#8fe3ad', '#ffc36b'];
  const n = Math.max(12, Math.min(30, Math.round(innerWidth / 52)));
  for (let i = 0; i < n; i++) {
    const s = document.createElement('span');
    s.style.setProperty('--c', colors[i % colors.length]);
    s.style.animationDelay = `${(i * 0.37) % 2.6}s`;
    s.style.marginTop = `${(i % 2) * 10}px`;
    lights.appendChild(s);
  }
}

// Aparición suave al hacer scroll
const items = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0, rootMargin: '0px 0px -6% 0px' });
  items.forEach((el) => io.observe(el));
} else {
  items.forEach((el) => el.classList.add('in'));
}

// Menú con fondo al bajar
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('solid', scrollY > 30);
addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Nieve suave (se apaga si la persona prefiere menos movimiento)
const canvas = document.getElementById('snow');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (canvas && !reduce) {
  const ctx = canvas.getContext('2d');
  let w, h, flakes;
  const resize = () => {
    w = canvas.width = innerWidth;
    h = canvas.height = innerHeight;
    flakes = Array.from({ length: Math.round(w / 26) }, () => ({
      x: Math.random() * w, y: Math.random() * h,
      r: Math.random() * 2.2 + 0.7, v: Math.random() * 0.5 + 0.25, d: Math.random() * Math.PI * 2,
    }));
  };
  resize();
  addEventListener('resize', resize);
  (function tick() {
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = 'rgba(255,255,255,.8)';
    for (const f of flakes) {
      f.y += f.v; f.d += 0.01; f.x += Math.sin(f.d) * 0.35;
      if (f.y > h + 4) { f.y = -4; f.x = Math.random() * w; }
      ctx.beginPath(); ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2); ctx.fill();
    }
    requestAnimationFrame(tick);
  })();
}
