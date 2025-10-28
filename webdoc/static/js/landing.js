/* =========================================================
   landing.js — Interactions for the landing page
========================================================= */

// ===== Navbar: mobile toggle + shadow on scroll =====
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navbar = document.querySelector('.navbar');

if (hamburger && navMenu) {
  hamburger.addEventListener('click', () => {
    const active = hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
    hamburger.setAttribute('aria-expanded', active ? 'true' : 'false');
  });
}
function onScrollNavbar() {
  if (!navbar) return;
  if (window.scrollY > 100) navbar.classList.add('scrolled');
  else navbar.classList.remove('scrolled');
}
window.addEventListener('scroll', onScrollNavbar);
onScrollNavbar();

// ===== Smooth scroll for local anchors =====
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    const target = document.querySelector(id);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ===== Features demo: typing effect (บทที่ 1–5) =====
(() => {
  const root = document.querySelector('.fx-typing');
  if (!root) return;
  const out = root.querySelector('.fx-typing__text');
  let strings = [];
  try { strings = JSON.parse(root.getAttribute('data-strings') || '[]'); }
  catch { strings = []; }
  if (!strings.length) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let s = 0, i = 0, typing = true;

  function type() {
    if (reduceMotion) { out.textContent = strings[s]; return; }
    const current = strings[s];
    if (typing) {
      out.textContent = current.slice(0, i++);
      if (i <= current.length) setTimeout(type, 45);
      else { typing = false; setTimeout(type, 900); }
    } else {
      typing = true;
      i = 0;
      s = (s + 1) % strings.length;
      setTimeout(type, 300);
    }
  }
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { type(); io.disconnect(); } });
  }, { threshold: 0.4 });
  io.observe(root);
})();

// ===== Stats: count-up when visible =====
(() => {
  const nums = document.querySelectorAll('.stat-number');
  if (!nums.length) return;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function animateNum(el) {
    const text = el.getAttribute('data-text');
    if (text) { el.textContent = text; return; }

    const target = parseInt(el.getAttribute('data-count') || '0', 10);
    const suffix = el.getAttribute('data-suffix') || '+';

    if (reduceMotion) { el.textContent = target + suffix; return; }

    const duration = 1400;
    const start = performance.now();

    function tick(now) {
      const p = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 2); // easeOutQuad
      const value = Math.floor(target * eased);
      el.textContent = value.toString() + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { animateNum(e.target); io.unobserve(e.target); }
    });
  }, { threshold: 0.5 });

  nums.forEach(n => io.observe(n));
})();

// ===== Ribbon marquee: duplicate content for seamless loop =====
(() => {
  const track = document.querySelector('.ribbon-track');
  if (!track) return;

  // Duplicate once for seamless loop
  track.innerHTML = track.innerHTML + track.innerHTML;

  // Pause on keyboard focus for a11y
  track.addEventListener('focusin', () => { track.style.animationPlayState = 'paused'; });
  track.addEventListener('focusout', () => { track.style.animationPlayState = ''; });
})();

// ===== Feature panels: light parallax hover (desktop only) =====
(() => {
  const panels = document.querySelectorAll('.fx-panel');
  if (!panels.length) return;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  panels.forEach(p => {
    p.addEventListener('mousemove', (e) => {
      const r = p.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      p.style.transform = `translateY(-2px) rotateX(${y*2}deg) rotateY(${x*2}deg)`;
    });
    p.addEventListener('mouseleave', () => { p.style.transform = 'translateY(-2px)'; });
  });
})();



document.addEventListener("DOMContentLoaded", function() {
  const typingElement = document.getElementById("typing-text");
  
  // ถ้าอยากให้หมุนหลายข้อความ ใส่เพิ่มใน array นี้
  const texts = [
    "FITM - Faculty of Industrial Technology and Management",
    "จัดรูปแบบตามเท็มเพลตตามที่มหาวิทยาลัยกำหนดอัตโนมัติ"
  ];

  let textIndex = 0;  // ข้อความที่กำลังใช้
  let charIndex = 0;  // ตัวอักษรปัจจุบัน
  let isDeleting = false; // สถานะพิมพ์/ลบ
  const typingSpeed = 80;  // ms ต่ออักษร
  const deletingSpeed = 80; // ms ตอนลบ
  const pauseDelay = 500;  // หยุดก่อนลบ (ms)

  function typeEffect() {
    const currentText = texts[textIndex];
    
    if (!isDeleting && charIndex <= currentText.length) {
      typingElement.textContent = currentText.substring(0, charIndex++);
      setTimeout(typeEffect, typingSpeed);
    } 
    else if (isDeleting && charIndex >= 0) {
      typingElement.textContent = currentText.substring(0, charIndex--);
      setTimeout(typeEffect, deletingSpeed);
    } 
    else {
      // สลับโหมด
      if (!isDeleting) {
        isDeleting = true;
        setTimeout(typeEffect, pauseDelay); // รอแล้วค่อยลบ
      } else {
        isDeleting = false;
        textIndex = (textIndex + 1) % texts.length;
        setTimeout(typeEffect, typingSpeed);
      }
    }
  }

  typeEffect();
});

