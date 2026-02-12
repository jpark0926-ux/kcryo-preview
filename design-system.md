# Korea Cryo Design System v1.0

> **Purpose**: Enable any LLM (Sonnet, Kimi, etc.) to produce high-quality Korea Cryo web pages  
> **Quality target**: 80% of Opus output at 20% of the cost  
> **Rule**: Copy-paste these tokens, components, and patterns. Do NOT improvise complex effects.

---

## 1. CSS Design Tokens

Paste this `:root` block into every page's `<style>`. These are the **only** design values you should use.

```css
/* ===== RESET ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Noto Sans KR', 'Outfit', -apple-system, sans-serif;
  background: var(--bg);
  color: var(--white);
  overflow-x: hidden;
  line-height: 1.6;
}

/* ===== DESIGN TOKENS ===== */
:root {
  /* --- Brand Colors --- */
  --cryo: #00d4ff;              /* Primary cyan */
  --cryo-dark: #0099cc;         /* Darker cyan for gradients */
  --cryo-light: #80f0ff;        /* Light cyan for accents */
  --cryo-glow: rgba(0, 212, 255, 0.25);  /* Glow/shadow color */

  /* --- Background Colors --- */
  --bg: #060d1b;                /* Darkest - main background */
  --bg2: #0a1628;               /* Medium - section alternation */
  --bg3: #0f2240;               /* Lightest - card backgrounds */

  /* --- Text Colors --- */
  --white: #ffffff;
  --text: rgba(255, 255, 255, 0.85);       /* Body text */
  --text-dim: rgba(255, 255, 255, 0.50);   /* Secondary text */
  --text-cryo: rgba(0, 212, 255, 0.80);    /* Accent text */

  /* --- Gradients --- */
  --grad-cryo: linear-gradient(135deg, #00d4ff, #0099cc);
  --grad-text: linear-gradient(135deg, #00e5ff, #00BFFF, #0080ff, #00e5ff);
  --grad-bg-glow: radial-gradient(circle at 50% 50%, rgba(0, 212, 255, 0.08), transparent 70%);
  --grad-bg-section: linear-gradient(180deg, var(--bg), var(--bg2), var(--bg));

  /* --- Typography Scale (use clamp for responsive) --- */
  --font-hero: clamp(40px, 8vw, 80px);       /* Hero headline */
  --font-h1: clamp(32px, 6vw, 52px);          /* Section titles */
  --font-h2: clamp(28px, 5vw, 48px);          /* Sub-section titles */
  --font-h3: clamp(20px, 3vw, 28px);          /* Card titles */
  --font-body: clamp(15px, 1.5vw, 17px);      /* Body text */
  --font-small: 14px;                          /* Labels, captions */
  --font-xs: 12px;                             /* Tags, badges */
  --font-label: 13px;                          /* Nav, buttons */

  /* --- Font Weights --- */
  --fw-light: 300;
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fw-bold: 700;
  --fw-black: 900;

  /* --- Spacing --- */
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 40px;
  --space-xl: 60px;
  --space-2xl: 80px;
  --space-3xl: 120px;
  --section-padding: 100px 24px;  /* Standard section padding */

  /* --- Border Radius --- */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-pill: 50px;

  /* --- Shadows --- */
  --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3);
  --shadow-glow: 0 4px 20px rgba(0, 212, 255, 0.25);
  --shadow-glow-hover: 0 8px 36px rgba(0, 212, 255, 0.4);
  --shadow-deep: 0 20px 60px rgba(0, 0, 0, 0.4);

  /* --- Borders --- */
  --border-subtle: 1px solid rgba(0, 212, 255, 0.08);
  --border-card: 1px solid rgba(0, 212, 255, 0.10);
  --border-hover: 1px solid rgba(0, 212, 255, 0.30);
  --border-glow: 1px solid rgba(0, 212, 255, 0.25);

  /* --- Transitions --- */
  --ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);
  --transition-fast: all 0.3s ease;
  --transition-smooth: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);

  /* --- Layout --- */
  --max-width: 1200px;
  --max-width-narrow: 900px;
  --max-width-text: 700px;
  --nav-height: 70px;
  --nav-height-scrolled: 56px;
}
```

### Google Fonts Import

Always include these two fonts. Place in `<head>` before `<style>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
```

**Font usage rules:**
- `'Noto Sans KR'` — body text, Korean content, descriptions
- `'Outfit'` — numbers, counters, English labels, tags, badges
- Headlines can use either; `font-weight: 900` for impact

---

## 2. Animation Presets

Copy these CSS blocks. Use the matching class names in HTML.

### 2a. Scroll Reveal (fadeInUp)

```css
/* ===== SCROLL REVEAL ===== */
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s var(--ease-smooth), transform 0.8s var(--ease-smooth);
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
/* Stagger delays for grid items */
.reveal-d1 { transition-delay: 0.1s; }
.reveal-d2 { transition-delay: 0.2s; }
.reveal-d3 { transition-delay: 0.3s; }
.reveal-d4 { transition-delay: 0.4s; }
```

**Required JS** (paste before `</body>`):

```js
/* Scroll Reveal Observer */
document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
});
```

**Usage:** Add `class="reveal"` to any element. Add `reveal-d1` through `reveal-d4` for staggered grid items.

### 2b. Hover Lift Effect

```css
/* ===== HOVER LIFT ===== */
.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.hover-lift:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-glow-hover);
}
```

**Usage:** Add `class="hover-lift"` to cards.

### 2c. Button Hover Glow

```css
/* ===== BUTTON GLOW ===== */
.btn-glow {
  transition: all 0.3s ease;
  box-shadow: var(--shadow-glow);
}
.btn-glow:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow-hover);
}
```

### 2d. Gradient Text Animation

```css
/* ===== GRADIENT TEXT ===== */
.gradient-text {
  background: var(--grad-text);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-shift 4s ease infinite;
}
@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

**Usage:** Wrap key words in `<span class="gradient-text">텍스트</span>`.

### 2e. Subtle Pulse (for badges/decorative elements)

```css
/* ===== SUBTLE PULSE ===== */
.pulse {
  animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 0.7; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.03); }
}
```

### ⛔ DO NOT USE these animations:
- 3D perspective/rotateX/rotateY transforms
- Custom cursor effects
- Magnetic/tilt card effects
- Glitch text effects
- Particle systems
- Complex multi-step keyframe animations (>3 steps)

---

## 3. Component Library

### 3a. Navigation Bar

```html
<nav class="navbar" id="navbar">
  <a href="/" class="nav-logo">
    <img src="logo-kc.png" alt="Korea Cryogenics" class="nav-logo-img">
    <div class="nav-logo-text">
      <span class="nav-logo-kr">한국초저온용기</span>
      <span class="nav-logo-en">KOREA CRYOGENICS</span>
    </div>
  </a>
  <ul class="nav-menu">
    <li><a href="/" class="nav-link">홈</a></li>
    <li><a href="/products" class="nav-link active">제품</a></li>
    <li><a href="/about" class="nav-link">회사소개</a></li>
    <li><a href="#contact" class="nav-cta btn-glow">문의하기</a></li>
  </ul>
</nav>
```

```css
/* ===== NAVBAR ===== */
.navbar {
  position: fixed; top: 0; left: 0; right: 0;
  height: var(--nav-height);
  background: rgba(10, 14, 26, 0.92);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: var(--border-subtle);
  z-index: 1000;
  display: flex; align-items: center;
  padding: 0 var(--space-lg);
  transition: var(--transition-fast);
}
.navbar.scrolled {
  height: var(--nav-height-scrolled);
  background: rgba(10, 14, 26, 0.98);
  box-shadow: 0 4px 40px rgba(0, 212, 255, 0.08);
}
.nav-logo {
  display: flex; align-items: center; gap: var(--space-sm);
  text-decoration: none;
}
.nav-logo-img { height: 40px; width: auto; }
.nav-logo-kr { font-size: 15px; font-weight: var(--fw-bold); color: var(--white); }
.nav-logo-en { font-size: 10px; color: var(--text-dim); letter-spacing: 0.5px; }
.nav-menu {
  display: flex; align-items: center; gap: 36px;
  margin-left: auto; list-style: none;
}
.nav-link {
  color: rgba(255, 255, 255, 0.75); text-decoration: none;
  font-size: var(--font-label); font-weight: var(--fw-medium);
  padding: var(--space-xs) 0; transition: color 0.3s;
  position: relative;
}
.nav-link:hover, .nav-link.active { color: var(--cryo); }
.nav-link::after {
  content: ''; position: absolute; bottom: 0; left: 0;
  width: 0; height: 2px;
  background: var(--grad-cryo);
  transition: width 0.3s;
}
.nav-link:hover::after, .nav-link.active::after { width: 100%; }
.nav-cta {
  padding: 10px 24px;
  background: var(--grad-cryo); color: var(--white);
  text-decoration: none; border-radius: var(--radius-sm);
  font-size: var(--font-label); font-weight: var(--fw-semibold);
}
```

**Navbar JS** (scroll behavior):

```js
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });
```

### 3b. Hero Section

```html
<section class="hero">
  <div class="hero-bg-glow"></div>
  <div class="hero-content">
    <div class="reveal">
      <span class="hero-badge">Taylor-Wharton Official Partner</span>
    </div>
    <h1 class="reveal reveal-d1">
      극한의 온도를<br>
      <span class="gradient-text">다루는 기술</span>
    </h1>
    <p class="reveal reveal-d2">
      -253°C 액화수소부터 -196°C 액체질소까지.<br>
      Taylor-Wharton의 60년 극저온 기술력을 경험하세요.
    </p>
    <div class="hero-stats reveal reveal-d3">
      <div class="hero-stat">
        <span class="hero-stat-value gradient-text">-253°C</span>
        <span class="hero-stat-label">LIQUID HYDROGEN</span>
      </div>
      <div class="hero-stat">
        <span class="hero-stat-value gradient-text">-196°C</span>
        <span class="hero-stat-label">LIQUID NITROGEN</span>
      </div>
      <div class="hero-stat">
        <span class="hero-stat-value gradient-text">60+</span>
        <span class="hero-stat-label">YEARS EXPERIENCE</span>
      </div>
    </div>
  </div>
</section>
```

```css
/* ===== HERO ===== */
.hero {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
  background: radial-gradient(circle at 50% 50%, var(--bg2), var(--bg));
  padding: calc(var(--nav-height) + 40px) var(--space-md) var(--space-xl);
}
.hero-bg-glow {
  position: absolute; inset: 0;
  background:
    radial-gradient(circle at 20% 30%, rgba(0, 212, 255, 0.10) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(0, 153, 204, 0.06) 0%, transparent 50%);
  animation: hero-glow 8s ease-in-out infinite alternate;
}
@keyframes hero-glow {
  0% { opacity: 0.5; }
  100% { opacity: 1; }
}
.hero-content {
  position: relative; z-index: 2;
  text-align: center; max-width: 1000px;
  padding: 0 var(--space-md);
}
.hero-badge {
  display: inline-block;
  padding: 6px 20px;
  border: var(--border-glow);
  border-radius: var(--radius-pill);
  color: var(--text-cryo);
  font-size: var(--font-xs); font-weight: var(--fw-medium);
  letter-spacing: 1px;
  margin-bottom: var(--space-md);
}
.hero h1 {
  font-size: var(--font-hero);
  font-weight: var(--fw-black);
  line-height: 1.1;
  margin-bottom: var(--space-md);
}
.hero p {
  font-size: clamp(16px, 2.5vw, 22px);
  color: var(--text-dim);
  line-height: 1.7;
  max-width: 660px;
  margin: 0 auto var(--space-lg);
}
.hero-stats {
  display: flex; gap: 48px; justify-content: center; flex-wrap: wrap;
  margin-top: var(--space-lg);
}
.hero-stat { text-align: center; }
.hero-stat-value {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(32px, 5vw, 52px);
  font-weight: var(--fw-black);
  display: block;
}
.hero-stat-label {
  font-size: var(--font-xs);
  color: var(--text-dim);
  letter-spacing: 1px;
  font-family: 'Outfit', sans-serif;
}
```

### 3c. Section Header (reusable)

```html
<div class="section-header reveal">
  <span class="section-tag">SECTION TAG</span>
  <h2 class="section-title">섹션 <span class="gradient-text">제목</span></h2>
  <p class="section-desc">섹션 설명 텍스트가 여기에 들어갑니다</p>
</div>
```

```css
/* ===== SECTION HEADER ===== */
.section-header {
  text-align: center;
  margin-bottom: var(--space-xl);
}
.section-tag {
  font-size: var(--font-xs); color: var(--cryo);
  letter-spacing: 2px; text-transform: uppercase;
  font-weight: var(--fw-semibold);
  font-family: 'Outfit', sans-serif;
}
.section-title {
  font-size: var(--font-h2);
  font-weight: var(--fw-black);
  margin-top: var(--space-xs);
}
.section-desc {
  color: var(--text-dim);
  font-size: var(--font-body);
  margin-top: var(--space-xs);
  max-width: var(--max-width-text);
  margin-left: auto; margin-right: auto;
}
```

### 3d. Feature Card (for grids of 3-4 items)

```html
<div class="feature-card reveal hover-lift">
  <div class="feature-icon">🧪</div>
  <h3 class="feature-title">카드 제목</h3>
  <p class="feature-desc">카드 설명 텍스트. 2-3줄 정도가 적당합니다.</p>
</div>
```

```css
/* ===== FEATURE CARD ===== */
.feature-card {
  padding: var(--space-lg);
  background: linear-gradient(135deg, rgba(15, 34, 64, 0.4), rgba(6, 13, 27, 0.7));
  border: var(--border-card);
  border-radius: var(--radius-lg);
  transition: var(--transition-smooth);
}
.feature-card:hover {
  border-color: rgba(0, 212, 255, 0.30);
}
.feature-icon {
  font-size: 40px;
  margin-bottom: var(--space-sm);
}
.feature-title {
  font-size: var(--font-h3);
  font-weight: var(--fw-bold);
  margin-bottom: var(--space-sm);
}
.feature-desc {
  font-size: var(--font-small);
  color: var(--text);
  line-height: 1.7;
}
/* Grid container */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-md);
  max-width: var(--max-width);
  margin: 0 auto;
}
```

### 3e. Product Card (large, 2-column layout)

```html
<section class="section-alt" style="padding: var(--section-padding);">
  <div class="product-row">
    <div class="product-image reveal">
      <img src="product-image.jpg" alt="Product Name">
    </div>
    <div class="product-info reveal reveal-d1">
      <span class="product-label">카테고리 라벨</span>
      <h2 class="product-title">제품 제목</h2>
      <p class="product-desc">제품 설명 텍스트. 2-3문장으로 제품의 핵심 가치를 전달합니다.</p>
      <ul class="product-features">
        <li>핵심 특성 1</li>
        <li>핵심 특성 2</li>
        <li>핵심 특성 3</li>
      </ul>
      <a href="#contact" class="btn-primary btn-glow">상담 신청하기 →</a>
    </div>
  </div>
</section>
```

```css
/* ===== PRODUCT ROW ===== */
.product-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-xl);
  align-items: center;
  max-width: var(--max-width);
  margin: 0 auto;
}
.product-row.reverse { direction: rtl; }
.product-row.reverse > * { direction: ltr; }
.product-image {
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: rgba(255, 255, 255, 0.02);
  border: var(--border-card);
  padding: var(--space-md);
}
.product-image img {
  width: 100%; height: auto;
  transition: transform 0.6s var(--ease-smooth);
}
.product-image:hover img { transform: scale(1.03); }
.product-label {
  font-size: var(--font-xs); color: var(--cryo);
  font-weight: var(--fw-semibold);
  letter-spacing: 2px; text-transform: uppercase;
  font-family: 'Outfit', sans-serif;
}
.product-title {
  font-size: var(--font-h2);
  font-weight: var(--fw-black);
  line-height: 1.15;
  margin: var(--space-sm) 0;
}
.product-desc {
  font-size: var(--font-body);
  color: var(--text);
  line-height: 1.8;
  margin-bottom: var(--space-md);
}
.product-features {
  list-style: none;
  margin-bottom: var(--space-md);
}
.product-features li {
  font-size: 15px; color: var(--text);
  padding: 10px 0 10px 28px;
  position: relative; line-height: 1.5;
  border-bottom: 1px solid rgba(0, 212, 255, 0.05);
}
.product-features li::before {
  content: '✓'; position: absolute; left: 0;
  color: var(--cryo); font-weight: var(--fw-black);
}
```

### 3f. Stats Counter Section

```html
<section style="padding: var(--section-padding); background: var(--grad-bg-section);">
  <div class="section-header reveal">
    <h2 class="section-title">신뢰의 <span class="gradient-text">숫자</span></h2>
  </div>
  <div class="stats-grid reveal">
    <div class="stat-item">
      <div class="stat-value gradient-text">280<span class="stat-unit">년</span></div>
      <div class="stat-label">Taylor-Wharton 역사</div>
    </div>
    <div class="stat-item">
      <div class="stat-value gradient-text">50,000<span class="stat-unit">+</span></div>
      <div class="stat-label">누적 용기 판매</div>
    </div>
    <div class="stat-item">
      <div class="stat-value gradient-text">99.5<span class="stat-unit">%</span></div>
      <div class="stat-label">단열 효율</div>
    </div>
    <div class="stat-item">
      <div class="stat-value gradient-text">24<span class="stat-unit">/7</span></div>
      <div class="stat-label">IoT 모니터링</div>
    </div>
  </div>
</section>
```

```css
/* ===== STATS ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-sm);
  max-width: 1000px;
  margin: 0 auto;
}
.stat-item {
  text-align: center;
  padding: var(--space-md);
}
.stat-value {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: var(--fw-black);
  font-variant-numeric: tabular-nums;
  line-height: 1;
}
.stat-unit {
  font-size: clamp(1rem, 2vw, 1.5rem);
  font-weight: var(--fw-bold);
  /* Inherits gradient from parent .gradient-text */
}
.stat-label {
  font-size: var(--font-small);
  color: var(--text-dim);
  margin-top: var(--space-xs);
}
```

### 3g. CTA Buttons

```html
<!-- Primary CTA (filled, glowing) -->
<a href="#" class="btn-primary btn-glow">문의하기 →</a>

<!-- Secondary CTA (outlined) -->
<a href="#" class="btn-secondary">자세히 보기</a>

<!-- Button group -->
<div class="btn-group">
  <a href="tel:02-1234-5678" class="btn-primary btn-glow">📞 전화 상담</a>
  <a href="mailto:info@koreacryo.com" class="btn-secondary">✉️ 이메일 문의</a>
</div>
```

```css
/* ===== BUTTONS ===== */
.btn-primary {
  display: inline-flex; align-items: center; gap: var(--space-xs);
  padding: 14px 32px;
  background: var(--grad-cryo);
  color: var(--white);
  text-decoration: none;
  border-radius: var(--radius-md);
  font-size: 15px; font-weight: var(--fw-semibold);
  transition: var(--transition-fast);
}
.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-glow-hover);
}
.btn-secondary {
  display: inline-flex; align-items: center; gap: var(--space-xs);
  padding: 14px 32px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--white);
  text-decoration: none;
  border-radius: var(--radius-md);
  font-size: 15px; font-weight: var(--fw-semibold);
  transition: var(--transition-fast);
  background: transparent;
}
.btn-secondary:hover {
  border-color: var(--cryo);
  color: var(--cryo);
  background: rgba(0, 212, 255, 0.05);
}
.btn-group {
  display: flex; gap: var(--space-sm);
  justify-content: center; flex-wrap: wrap;
}
```

### 3h. Final CTA Section

```html
<section class="final-cta" id="contact">
  <div class="final-cta-glow"></div>
  <div class="final-cta-content">
    <h2 class="reveal">극저온 기술의<br><span class="gradient-text">파트너가 되어드립니다</span></h2>
    <p class="reveal reveal-d1">귀사의 요구사항에 맞는 최적의 극저온 솔루션을 제안해 드립니다.</p>
    <div class="btn-group reveal reveal-d2">
      <a href="tel:02-1234-5678" class="btn-primary btn-glow">📞 전화 상담</a>
      <a href="mailto:info@koreacryo.com" class="btn-secondary">✉️ 이메일 문의</a>
    </div>
  </div>
</section>
```

```css
/* ===== FINAL CTA ===== */
.final-cta {
  padding: var(--space-3xl) var(--space-md);
  background: var(--bg);
  text-align: center;
  position: relative; overflow: hidden;
}
.final-cta-glow {
  position: absolute; inset: 0;
  background: var(--grad-bg-glow);
  animation: pulse 4s ease-in-out infinite;
}
.final-cta-content {
  position: relative; z-index: 2;
  max-width: var(--max-width-text);
  margin: 0 auto;
}
.final-cta h2 {
  font-size: var(--font-h1);
  font-weight: var(--fw-black);
  line-height: 1.25;
  margin-bottom: var(--space-md);
}
.final-cta p {
  font-size: var(--font-body);
  color: var(--text);
  line-height: 1.8;
  margin-bottom: var(--space-lg);
}
```

### 3i. Section Divider / Background Alternation

```css
/* ===== SECTION BACKGROUNDS ===== */
/* Alternate sections between these two: */
.section-dark { background: var(--bg); }
.section-alt  { background: var(--bg2); }

/* Or use gradient transitions between sections: */
.section-gradient-down { background: linear-gradient(180deg, var(--bg), var(--bg2)); }
.section-gradient-up   { background: linear-gradient(180deg, var(--bg2), var(--bg)); }
```

**Pattern**: Alternate `section-dark` and `section-alt` for visual rhythm. Use `section-gradient-down`/`up` for smooth transitions.

### 3j. Footer

```html
<footer class="footer">
  <p>© 2024 한국초저온용기(주) Korea Cryogenics Co., Ltd. All rights reserved.</p>
</footer>
```

```css
/* ===== FOOTER ===== */
.footer {
  background: #040912;
  border-top: var(--border-subtle);
  padding: var(--space-lg);
  text-align: center;
  font-size: var(--font-small);
  color: var(--text-dim);
}
```

---

## 4. Page Structure Template

Every product/landing page should follow this exact order:

```
┌─────────────────────────────────────┐
│  NAVBAR (fixed, glass morphism)     │  ← Always present
├─────────────────────────────────────┤
│  HERO SECTION                       │  ← min-height: 100vh
│  - Badge/tag line                   │
│  - H1 headline (with gradient-text) │
│  - Subtitle paragraph               │
│  - Key stats (3 items)              │
├─────────────────────────────────────┤
│  BRAND/STORY SECTION (optional)     │  ← 1-3 story blocks
│  - 2-column: visual + text          │
│  - Alternate direction per block    │
├─────────────────────────────────────┤
│  MAIN PRODUCT(S)                    │  ← 2-column: image + info
│  - Product 1 (image left)           │
│  - Product 2 (image right, .reverse)│
├─────────────────────────────────────┤
│  STATS COUNTER                      │  ← 4-item grid, gradient text
├─────────────────────────────────────┤
│  SECONDARY PRODUCTS / FEATURES      │  ← 3-4 column card grid
├─────────────────────────────────────┤
│  FINAL CTA                          │  ← Center-aligned, two buttons
├─────────────────────────────────────┤
│  FOOTER                             │  ← Simple copyright
└─────────────────────────────────────┘
```

### Responsive Breakpoints

```css
/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {
  .navbar { padding: 0 var(--space-sm); }
  .nav-menu { display: none; }  /* Hide menu, add hamburger if needed */
  .product-row,
  .product-row.reverse {
    grid-template-columns: 1fr;
    gap: var(--space-md);
    direction: ltr;
  }
  .hero-stats { gap: var(--space-md); }
}

@media (max-width: 600px) {
  .hero { padding-top: calc(var(--nav-height) + 20px); }
  .hero h1 { font-size: clamp(32px, 10vw, 48px); }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .feature-grid { grid-template-columns: 1fr; }
}
```

### Section Spacing Rules

| Element | Spacing |
|---------|---------|
| Section padding | `100px 24px` (top/bottom, sides) |
| Between sections | No gap needed (backgrounds provide visual separation) |
| Section header → content | `60px` (`var(--space-xl)`) |
| Card grid gap | `24px` (`var(--space-md)`) |
| Product grid gap | `60px` (`var(--space-xl)`) |
| Hero → next section | Natural flow (hero is 100vh) |

---

## 5. Usage Guide

### How to Build a New Page

1. **Start with the HTML boilerplate** (fonts + tokens + reset)
2. **Copy the Navbar** component
3. **Copy the Hero** component, change text content
4. **Add sections** by copying component blocks in order
5. **Add `.reveal`** class to every section's children
6. **Paste the Scroll Reveal JS** before `</body>`
7. **Paste the Navbar JS** before `</body>`
8. **Apply responsive CSS** at the bottom of your `<style>`

### Color Application Rules

| Context | Color to Use |
|---------|-------------|
| Page background | `var(--bg)` |
| Alternate sections | `var(--bg2)` |
| Card backgrounds | `linear-gradient(135deg, rgba(15,34,64,0.4), rgba(6,13,27,0.7))` |
| Primary text | `var(--white)` for headings, `var(--text)` for body |
| Secondary text | `var(--text-dim)` |
| Accent color | `var(--cryo)` — labels, icons, borders |
| Key headline words | `class="gradient-text"` |
| Buttons | `var(--grad-cryo)` for primary, transparent for secondary |
| Borders | `var(--border-card)` default, `var(--border-hover)` on hover |
| Glows/shadows | `var(--shadow-glow)` / `var(--shadow-glow-hover)` |

### Typography Hierarchy

| Level | Size Token | Weight | Use For |
|-------|-----------|--------|---------|
| Display | `--font-hero` | 900 | Hero headline only |
| H1 | `--font-h1` | 900 | CTA section titles |
| H2 | `--font-h2` | 900 | Section titles |
| H3 | `--font-h3` | 700 | Card titles |
| Body | `--font-body` | 400 | Paragraphs, descriptions |
| Small | `--font-small` | 400-500 | Labels, captions |
| XS | `--font-xs` | 600 | Tags, badges, uppercase labels |

### Do's and Don'ts

✅ **DO:**
- Use `clamp()` for all heading sizes
- Use `var(--token)` instead of raw values
- Alternate section backgrounds (`--bg` / `--bg2`)
- Add `class="reveal"` to all scroll-animated elements
- Use `gradient-text` on 1-2 key words per section (not entire paragraphs)
- Use `font-family: 'Outfit'` for numbers and English labels
- Keep line-height at 1.7-1.8 for body text
- Use emoji as icons (🧪 🧬 🔬 ⚙️ ❄️ 💧) — simpler than SVG/icon fonts

❌ **DON'T:**
- Don't use raw hex colors — always use CSS variables
- Don't use `px` for heading font-size — always `clamp()`
- Don't add 3D transforms, parallax, or perspective
- Don't create custom cursor or mouse-tracking effects
- Don't add particle/snow/crystal effects
- Don't use glitch text effects
- Don't use more than 2 animation types per section
- Don't set `animation-duration` under 2s for ambient animations
- Don't use JavaScript for layout (CSS Grid/Flexbox only)

### Quick Reference: Assembling a Section

```html
<!-- Standard section pattern -->
<section class="section-alt" style="padding: var(--section-padding);">
  <div style="max-width: var(--max-width); margin: 0 auto;">
    
    <!-- Header -->
    <div class="section-header reveal">
      <span class="section-tag">ENGLISH TAG</span>
      <h2 class="section-title">한국어 <span class="gradient-text">핵심 단어</span></h2>
      <p class="section-desc">설명 텍스트</p>
    </div>
    
    <!-- Content (cards, products, etc.) -->
    <div class="feature-grid">
      <div class="feature-card reveal hover-lift">...</div>
      <div class="feature-card reveal reveal-d1 hover-lift">...</div>
      <div class="feature-card reveal reveal-d2 hover-lift">...</div>
    </div>
    
  </div>
</section>
```

---

## 6. Complete Minimal JS (paste before `</body>`)

```html
<script>
(function() {
  'use strict';

  // Scroll reveal
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // Navbar scroll
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });
})();
</script>
```

---

## 7. Full Page Template (Copy & Customize)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>페이지 제목 | 한국초저온용기</title>
<meta name="description" content="페이지 설명">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* === PASTE: Reset + Design Tokens (Section 1) === */
/* === PASTE: Animation Presets (Section 2) === */
/* === PASTE: Component CSS you need (Section 3) === */
/* === PASTE: Responsive (Section 4) === */
</style>
</head>
<body>

<!-- NAVBAR -->
<!-- PASTE: Navbar HTML (Section 3a) -->

<!-- HERO -->
<!-- PASTE: Hero HTML (Section 3b) -->

<!-- SECTIONS -->
<!-- Assemble from components as needed -->

<!-- FINAL CTA -->
<!-- PASTE: Final CTA HTML (Section 3h) -->

<!-- FOOTER -->
<!-- PASTE: Footer HTML (Section 3j) -->

<!-- JS -->
<!-- PASTE: Minimal JS (Section 6) -->

</body>
</html>
```

---

## Version History
- **v1.0** (2026-02-13): Initial design system extracted from cryo-equipment-final.html
