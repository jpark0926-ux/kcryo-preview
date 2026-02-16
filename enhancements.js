/**
 * KoreaCryo v2 - Interactive Enhancements
 * Adds scroll-based animations and interactivity
 */

(function() {
  'use strict';

  // ========================================
  // Temperature Journey Scroll Animation
  // ========================================
  function initTempJourney() {
    const steps = document.querySelectorAll('.temp-journey-step');
    const gradient = document.getElementById('temp-journey-gradient');
    if (!steps.length || !gradient) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const step = entry.target;
          const index = Array.from(steps).indexOf(step);
          
          // Activate current step
          step.classList.add('active');
          
          // Update gradient bar based on progress
          const progress = ((index + 1) / steps.length) * 100;
          gradient.style.width = progress + '%';
          
          // Deactivate previous steps slightly for visual hierarchy
          steps.forEach((s, i) => {
            if (i < index) {
              s.style.opacity = '0.6';
            }
          });
        }
      });
    }, {
      threshold: 0.5,
      rootMargin: '-20% 0px -20% 0px'
    });

    steps.forEach(step => observer.observe(step));
  }

  // ========================================
  // Timeline Reveal Animation
  // ========================================
  function initTimeline() {
    const items = document.querySelectorAll('.timeline-item');
    if (!items.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.3,
      rootMargin: '0px 0px -50px 0px'
    });

    items.forEach(item => observer.observe(item));
  }

  // ========================================
  // Stats Counter Animation
  // ========================================
  function initStatsCounter() {
    const stats = document.querySelectorAll('.stat-number');
    if (!stats.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const finalValue = el.textContent;
          
          // Extract number and suffix
          const match = finalValue.match(/([\d,]+)(.*)/);
          if (match) {
            const num = parseInt(match[1].replace(/,/g, ''));
            const suffix = match[2];
            
            animateCounter(el, 0, num, 1500, suffix);
          }
          
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    stats.forEach(stat => observer.observe(stat));
  }

  function animateCounter(el, start, end, duration, suffix) {
    const startTime = performance.now();
    
    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(start + (end - start) * easeOut);
      
      el.textContent = current.toLocaleString() + suffix;
      
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }
    
    requestAnimationFrame(update);
  }

  // ========================================
  // Smooth Scroll for Anchor Links
  // ========================================
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }

  // ========================================
  // Mobile Swipe for Product Cards
  // ========================================
  function initProductSwipe() {
    if (window.matchMedia('(min-width: 769px)').matches) return;
    
    const productGrid = document.querySelector('#products .grid');
    if (!productGrid) return;

    let startX = 0;
    let scrollLeft = 0;
    let isDragging = false;

    productGrid.style.cursor = 'grab';
    productGrid.style.overflowX = 'auto';
    productGrid.style.scrollSnapType = 'x mandatory';
    productGrid.style.scrollbarWidth = 'none';
    productGrid.style.msOverflowStyle = 'none';

    productGrid.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.pageX - productGrid.offsetLeft;
      scrollLeft = productGrid.scrollLeft;
      productGrid.style.cursor = 'grabbing';
    });

    productGrid.addEventListener('mouseleave', () => {
      isDragging = false;
      productGrid.style.cursor = 'grab';
    });

    productGrid.addEventListener('mouseup', () => {
      isDragging = false;
      productGrid.style.cursor = 'grab';
    });

    productGrid.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      e.preventDefault();
      const x = e.pageX - productGrid.offsetLeft;
      const walk = (x - startX) * 2;
      productGrid.scrollLeft = scrollLeft - walk;
    });

    // Touch events
    productGrid.addEventListener('touchstart', (e) => {
      startX = e.touches[0].pageX - productGrid.offsetLeft;
      scrollLeft = productGrid.scrollLeft;
    }, { passive: true });

    productGrid.addEventListener('touchmove', (e) => {
      const x = e.touches[0].pageX - productGrid.offsetLeft;
      const walk = (x - startX) * 2;
      productGrid.scrollLeft = scrollLeft - walk;
    }, { passive: true });
  }

  // ========================================
  // Parallax Effect for Hero
  // ========================================
  function initHeroParallax() {
    const hero = document.querySelector('#hero');
    const heroContent = hero?.querySelector('.hero-parallax, .relative.z-10');
    if (!hero || !heroContent) return;

    let ticking = false;
    
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const scrolled = window.scrollY;
          const rate = scrolled * 0.3;
          heroContent.style.transform = `translateY(${rate}px)`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // ========================================
  // Back to Top Button
  // ========================================
  function initBackToTop() {
    const btn = document.createElement('button');
    btn.id = 'back-to-top';
    btn.innerHTML = '↑';
    btn.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(0, 212, 255, 0.1);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(0, 212, 255, 0.3);
      color: #00d4ff;
      font-size: 20px;
      cursor: pointer;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s;
      z-index: 9000;
    `;
    
    btn.addEventListener('mouseenter', () => {
      btn.style.background = 'rgba(0, 212, 255, 0.2)';
      btn.style.transform = 'translateY(0) scale(1.1)';
    });
    
    btn.addEventListener('mouseleave', () => {
      btn.style.background = 'rgba(0, 212, 255, 0.1)';
      btn.style.transform = 'translateY(0) scale(1)';
    });
    
    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    document.body.appendChild(btn);

    // Show/hide based on scroll
    window.addEventListener('scroll', () => {
      if (window.scrollY > 500) {
        btn.style.opacity = '1';
        btn.style.transform = 'translateY(0)';
      } else {
        btn.style.opacity = '0';
        btn.style.transform = 'translateY(20px)';
      }
    }, { passive: true });
  }

  // ========================================
  // Image Lazy Loading
  // ========================================
  function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    if (!images.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    }, { rootMargin: '50px' });

    images.forEach(img => observer.observe(img));
  }

  // ========================================
  // Temperature Converter Widget
  // ========================================
  function initTempConverter() {
    const container = document.querySelector('.temp-converter');
    if (!container) return;

    const celsius = container.querySelector('.temp-c');
    const fahrenheit = container.querySelector('.temp-f');
    const kelvin = container.querySelector('.temp-k');
    const slider = container.querySelector('.temp-slider');

    if (!celsius || !fahrenheit || !kelvin || !slider) return;

    function updateFromCelsius(c) {
      const f = (c * 9/5) + 32;
      const k = c + 273.15;
      
      celsius.value = Math.round(c);
      fahrenheit.value = Math.round(f);
      kelvin.value = Math.round(k);
      
      // Update slider position
      const min = -273;
      const max = 100;
      const percent = ((c - min) / (max - min)) * 100;
      slider.value = c;
      
      // Update visual indicator
      container.style.setProperty('--temp-percent', percent + '%');
      
      // Color shift based on temperature
      let hue;
      if (c < -100) hue = 240; // deep blue
      else if (c < 0) hue = 200 + (c / -100) * 40; // blue to cyan
      else if (c < 100) hue = 180 - (c / 100) * 60; // cyan to green
      else hue = 120; // green
      
      container.style.setProperty('--temp-hue', hue);
    }

    slider.addEventListener('input', (e) => updateFromCelsius(parseFloat(e.target.value)));
    celsius.addEventListener('input', (e) => updateFromCelsius(parseFloat(e.target.value) || 0));
    fahrenheit.addEventListener('input', (e) => updateFromCelsius((parseFloat(e.target.value) - 32) * 5/9 || 0));
    kelvin.addEventListener('input', (e) => updateFromCelsius(parseFloat(e.target.value) - 273.15 || 0));

    // Initialize at -196°C (liquid nitrogen)
    updateFromCelsius(-196);
  }

  // ========================================
  // Ice Crystal Particle Effect
  // ========================================
  function initIceParticles() {
    const canvas = document.getElementById('ice-particles');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let particles = [];
    let lastScrollY = 0;
    let scrollVelocity = 0;

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    class Particle {
      constructor() {
        this.reset();
      }

      reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height - canvas.height;
        this.size = Math.random() * 3 + 1;
        this.speedY = Math.random() * 2 + 1;
        this.speedX = (Math.random() - 0.5) * 0.5;
        this.opacity = Math.random() * 0.5 + 0.2;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotationSpeed = (Math.random() - 0.5) * 0.02;
      }

      update() {
        // Scroll velocity affects particle speed
        this.y += this.speedY + Math.abs(scrollVelocity) * 0.1;
        this.x += this.speedX + scrollVelocity * 0.05;
        this.rotation += this.rotationSpeed;

        if (this.y > canvas.height) {
          this.y = -10;
          this.x = Math.random() * canvas.width;
        }
        if (this.x > canvas.width) this.x = 0;
        if (this.x < 0) this.x = canvas.width;
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = '#ffffff';
        
        // Draw snowflake-like crystal
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
          ctx.lineTo(Math.cos(i * Math.PI / 3) * this.size, Math.sin(i * Math.PI / 3) * this.size);
          ctx.lineTo(Math.cos(i * Math.PI / 3 + Math.PI / 6) * this.size * 0.5, Math.sin(i * Math.PI / 3 + Math.PI / 6) * this.size * 0.5);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      }
    }

    // Create particles based on scroll velocity
    function updateParticleCount() {
      const targetCount = Math.min(50, Math.abs(scrollVelocity) * 5);
      while (particles.length < targetCount) {
        particles.push(new Particle());
      }
      while (particles.length > targetCount && particles.length > 10) {
        particles.pop();
      }
    }

    // Track scroll velocity
    window.addEventListener('scroll', () => {
      scrollVelocity = window.scrollY - lastScrollY;
      lastScrollY = window.scrollY;
      updateParticleCount();
    }, { passive: true });

    // Animation loop
    let animationId;
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.update();
        p.draw();
      });
      animationId = requestAnimationFrame(animate);
    }
    animate();

    // Pause when tab is hidden
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        cancelAnimationFrame(animationId);
      } else {
        animate();
      }
    });
  }

  // ========================================
  // Quiz Gamification
  // ========================================
  function initQuizGamification() {
    const quiz = document.querySelector('.cryo-quiz');
    if (!quiz) return;

    let score = 0;
    let streak = 0;
    let maxStreak = parseInt(localStorage.getItem('kcryo_quiz_max_streak') || '0');
    let totalAnswered = parseInt(localStorage.getItem('kcryo_quiz_total') || '0');
    let totalCorrect = parseInt(localStorage.getItem('kcryo_quiz_correct') || '0');

    // Add score display
    const scoreBoard = document.createElement('div');
    scoreBoard.className = 'quiz-score-board';
    scoreBoard.innerHTML = `
      <div class="quiz-stat">
        <span class="quiz-stat-value" id="quiz-score">0</span>
        <span class="quiz-stat-label">점수</span>
      </div>
      <div class="quiz-stat">
        <span class="quiz-stat-value" id="quiz-streak">0</span>
        <span class="quiz-stat-label">연속정답</span>
      </div>
      <div class="quiz-stat">
        <span class="quiz-stat-value" id="quiz-accuracy">0%</span>
        <span class="quiz-stat-label">정답률</span>
      </div>
    `;
    quiz.insertBefore(scoreBoard, quiz.firstChild);

    // Add badge container
    const badgeContainer = document.createElement('div');
    badgeContainer.className = 'quiz-badges';
    badgeContainer.innerHTML = `
      <h4>🏆 획득 배지</h4>
      <div class="badge-list"></div>
    `;
    quiz.appendChild(badgeContainer);

    const badges = [
      { id: 'first_correct', name: '첫 정답', icon: '🎯', condition: () => totalCorrect >= 1 },
      { id: 'streak_3', name: '연속 3정답', icon: '🔥', condition: () => maxStreak >= 3 },
      { id: 'streak_5', name: '연속 5정답', icon: '⚡', condition: () => maxStreak >= 5 },
      { id: 'master', name: '극저온 마스터', icon: '🧊', condition: () => totalCorrect >= 10 },
      { id: 'perfect', name: '퍼펙트 스코어', icon: '💎', condition: () => totalAnswered > 0 && totalCorrect === totalAnswered && totalAnswered >= 5 }
    ];

    function updateBadges() {
      const list = badgeContainer.querySelector('.badge-list');
      list.innerHTML = badges.map(badge => {
        const earned = badge.condition();
        return `
          <div class="quiz-badge ${earned ? 'earned' : 'locked'}">
            <span class="badge-icon">${badge.icon}</span>
            <span class="badge-name">${badge.name}</span>
          </div>
        `;
      }).join('');
    }

    function updateStats() {
      document.getElementById('quiz-score').textContent = score;
      document.getElementById('quiz-streak').textContent = streak;
      const accuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;
      document.getElementById('quiz-accuracy').textContent = accuracy + '%';
      updateBadges();
    }

    // Override quiz option clicks
    quiz.querySelectorAll('.quiz-option').forEach(option => {
      option.addEventListener('click', function() {
        const isCorrect = this.dataset.correct === 'true';
        totalAnswered++;
        
        if (isCorrect) {
          score += 100 + (streak * 10);
          streak++;
          totalCorrect++;
          if (streak > maxStreak) {
            maxStreak = streak;
            localStorage.setItem('kcryo_quiz_max_streak', maxStreak);
          }
          this.classList.add('correct-reveal');
          
          // Ice crack sound effect (visual feedback)
          createIceCrackEffect(this);
        } else {
          streak = 0;
          this.classList.add('wrong-reveal');
        }
        
        localStorage.setItem('kcryo_quiz_total', totalAnswered);
        localStorage.setItem('kcryo_quiz_correct', totalCorrect);
        updateStats();
      });
    });

    function createIceCrackEffect(element) {
      const rect = element.getBoundingClientRect();
      for (let i = 0; i < 8; i++) {
        const shard = document.createElement('span');
        shard.className = 'ice-shard';
        shard.style.cssText = `
          position: fixed;
          left: ${rect.left + rect.width/2}px;
          top: ${rect.top + rect.height/2}px;
          width: 8px;
          height: 8px;
          background: linear-gradient(135deg, #00d4ff, #ffffff);
          border-radius: 50%;
          pointer-events: none;
          z-index: 10000;
          animation: iceShardFly 0.6s ease-out forwards;
          --fly-x: ${(Math.random() - 0.5) * 100}px;
          --fly-y: ${(Math.random() - 0.5) * 100}px;
        `;
        document.body.appendChild(shard);
        setTimeout(() => shard.remove(), 600);
      }
    }

    // Add CSS animation
    if (!document.getElementById('ice-shard-style')) {
      const style = document.createElement('style');
      style.id = 'ice-shard-style';
      style.textContent = `
        @keyframes iceShardFly {
          0% { transform: translate(0, 0) scale(1); opacity: 1; }
          100% { transform: translate(var(--fly-x), var(--fly-y)) scale(0); opacity: 0; }
        }
      `;
      document.head.appendChild(style);
    }

    updateStats();
  }

  // ========================================
  // 1. 3D Tilt Cards (Product Cards)
  // ========================================
  function init3DTiltCards() {
    const cards = document.querySelectorAll('.product-card, .spec-card');
    if (!cards.length) return;

    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        card.style.transition = 'transform 0.1s ease-out';

        // Dynamic shine effect
        const shine = card.querySelector('.card-shine') || createShine(card);
        const percentX = (x / rect.width) * 100;
        const percentY = (y / rect.height) * 100;
        shine.style.background = `radial-gradient(circle at ${percentX}% ${percentY}%, rgba(255,255,255,0.2) 0%, transparent 50%)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        card.style.transition = 'transform 0.5s ease-out';
        const shine = card.querySelector('.card-shine');
        if (shine) shine.style.background = 'transparent';
      });
    });

    function createShine(card) {
      const shine = document.createElement('div');
      shine.className = 'card-shine';
      shine.style.cssText = `
        position: absolute;
        inset: 0;
        pointer-events: none;
        border-radius: inherit;
        z-index: 2;
      `;
      card.appendChild(shine);
      return shine;
    }
  }

  // ========================================
  // 4. Secret Easter Egg (Multiple ways to activate)
  // ========================================
  function initEasterEgg() {
    // Method 1: Konami Code (↑↑↓↓←→←→BA)
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    let konamiIndex = 0;

    document.addEventListener('keydown', (e) => {
      // ? key for easy activation
      if (e.key === '?' || e.key === '/') {
        activateAuroraMode();
        return;
      }

      if (e.key === konamiCode[konamiIndex]) {
        konamiIndex++;
        if (konamiIndex === konamiCode.length) {
          activateAuroraMode();
          konamiIndex = 0;
        }
      } else {
        konamiIndex = 0;
      }
    });

    // Method 2: Triple-click on hero
    const hero = document.querySelector('#hero');
    if (hero) {
      hero.addEventListener('click', (e) => {
        if (e.detail === 3) { // Triple click
          activateAuroraMode();
        }
      });
    }

    // Method 3: Click logo 3 times
    const logo = document.querySelector('.logo, header img, nav img');
    if (logo) {
      let logoClicks = 0;
      logo.addEventListener('click', () => {
        logoClicks++;
        if (logoClicks >= 3) {
          activateAuroraMode();
          logoClicks = 0;
        }
        setTimeout(() => logoClicks = 0, 1000);
      });
    }

    function activateAuroraMode() {
      // Check if already frozen - then unfreeze
      if (document.body.classList.contains('aurora-mode')) {
        deactivateFreezeMode();
        return;
      }

      document.body.classList.add('aurora-mode');

      // Show dramatic freeze notification
      const notification = document.createElement('div');
      notification.id = 'freeze-notification';
      notification.innerHTML = '🧊 동결 모드 ON';
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%) scale(0);
        background: linear-gradient(135deg, rgba(220,240,255,1), rgba(180,220,255,1));
        color: #003366;
        padding: 16px 32px;
        border-radius: 12px;
        font-weight: 900;
        font-size: 1rem;
        z-index: 10001;
        border: 2px solid rgba(255,255,255,0.9);
        box-shadow: 0 0 30px rgba(200,230,255,0.8), inset 0 0 10px rgba(255,255,255,0.5);
        animation: freeze-notification 2s ease-out forwards;
        text-shadow: 0 1px 2px rgba(255,255,255,0.8);
      `;
      document.body.appendChild(notification);
      setTimeout(() => notification.remove(), 2500);

      // Create heavy frost overlay
      const frostOverlay = document.createElement('div');
      frostOverlay.id = 'frost-overlay';
      frostOverlay.style.cssText = `
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 9998;
        background: 
          radial-gradient(ellipse at 0% 0%, rgba(255,255,255,0.4) 0%, transparent 40%),
          radial-gradient(ellipse at 100% 0%, rgba(255,255,255,0.3) 0%, transparent 35%),
          radial-gradient(ellipse at 0% 100%, rgba(255,255,255,0.3) 0%, transparent 35%),
          radial-gradient(ellipse at 100% 100%, rgba(255,255,255,0.4) 0%, transparent 40%);
        opacity: 0;
        animation: frost-overlay-appear 1.5s ease-out forwards;
      `;
      document.body.appendChild(frostOverlay);

      // Add ice texture overlay
      const iceTexture = document.createElement('div');
      iceTexture.id = 'ice-texture';
      iceTexture.style.cssText = `
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 9996;
        background-image: 
          repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px),
          repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
        opacity: 0;
        animation: ice-texture-appear 1s ease-out 0.5s forwards;
      `;
      document.body.appendChild(iceTexture);

      // Add heavy ice border
      const iceBorder = document.createElement('div');
      iceBorder.id = 'ice-border';
      iceBorder.style.cssText = `
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 9999;
        border: 30px solid transparent;
        border-image: 
          linear-gradient(135deg, 
            rgba(255,255,255,0.9) 0%,
            rgba(200,230,255,0.8) 25%,
            rgba(255,255,255,0.9) 50%,
            rgba(180,220,255,0.8) 75%,
            rgba(255,255,255,0.9) 100%
          ) 1;
        box-shadow: 
          inset 0 0 50px rgba(200,240,255,0.3),
          0 0 30px rgba(200,240,255,0.2);
        opacity: 0;
        animation: ice-border-heavy 1s ease-out forwards;
      `;
      document.body.appendChild(iceBorder);

      // Add corner ice crystals
      const corners = ['top-left', 'top-right', 'bottom-left', 'bottom-right'];
      corners.forEach((corner, i) => {
        const cornerIce = document.createElement('div');
        cornerIce.className = `corner-ice ${corner}`;
        const [v, h] = corner.split('-');
        cornerIce.style.cssText = `
          position: fixed;
          ${v}: 0;
          ${h}: 0;
          width: 150px;
          height: 150px;
          pointer-events: none;
          z-index: 9997;
          background: radial-gradient(circle at ${h === 'left' ? '0%' : '100%'} ${v === 'top' ? '0%' : '100%'}, 
            rgba(255,255,255,0.9) 0%, 
            rgba(220,240,255,0.6) 30%,
            rgba(200,230,255,0.3) 60%,
            transparent 70%);
          opacity: 0;
          animation: corner-ice-appear 0.8s ease-out ${i * 0.15}s forwards;
        `;
        document.body.appendChild(cornerIce);
      });

      // Add frost particles
      const frostCanvas = document.createElement('canvas');
      frostCanvas.id = 'frost-canvas';
      frostCanvas.style.cssText = `
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 9995;
        opacity: 0;
        animation: frost-canvas-appear 1s ease-out 0.3s forwards;
      `;
      document.body.appendChild(frostCanvas);

      // Initialize frost animation
      initFrostAnimation(frostCanvas);

      // Add heavy freeze CSS
      const freezeStyle = document.createElement('style');
      freezeStyle.id = 'freeze-mode-style';
      freezeStyle.textContent = `
        @keyframes freeze-notification {
          0% { opacity: 0; transform: translateX(-50%) scale(0.5); }
          50% { transform: translateX(-50%) scale(1.05); }
          100% { opacity: 1; transform: translateX(-50%) scale(1); }
        }

        @keyframes frost-overlay-appear {
          to { opacity: 1; }
        }

        @keyframes ice-texture-appear {
          to { opacity: 1; }
        }

        @keyframes ice-border-heavy {
          0% { opacity: 0; transform: scale(1.1); }
          100% { opacity: 0.85; transform: scale(1); }
        }

        @keyframes corner-ice-appear {
          0% { opacity: 0; transform: scale(0.5); }
          100% { opacity: 1; transform: scale(1); }
        }

        @keyframes frost-canvas-appear {
          to { opacity: 0.6; }
        }

        /* Heavy freeze effects */
        body.aurora-mode {
          filter: saturate(0.3) brightness(1.1);
        }

        body.aurora-mode #hero {
          filter: contrast(1.2) brightness(0.95);
        }

        body.aurora-mode section {
          filter: contrast(1.1);
        }

        body.aurora-mode h1, 
        body.aurora-mode h2,
        body.aurora-mode h3 {
          color: #e8f4f8 !important;
          text-shadow: 
            0 0 10px rgba(255,255,255,0.8),
            0 0 20px rgba(200,240,255,0.6),
            0 0 30px rgba(180,220,255,0.4),
            2px 2px 4px rgba(0,50,100,0.3) !important;
        }

        body.aurora-mode p,
        body.aurora-mode span:not(.temp-c):not(.temp-f):not(.temp-k) {
          color: #c8e0e8 !important;
        }

        body.aurora-mode .product-card,
        body.aurora-mode .spec-card {
          background: rgba(255,255,255,0.05) !important;
          border: 2px solid rgba(255,255,255,0.3) !important;
          box-shadow: 
            0 0 20px rgba(200,240,255,0.15),
            inset 0 0 20px rgba(255,255,255,0.05) !important;
        }

        body.aurora-mode button {
          background: linear-gradient(135deg, rgba(240,248,255,0.95), rgba(200,230,255,0.9)) !important;
          color: #003366 !important;
          border: 2px solid rgba(255,255,255,0.9) !important;
          box-shadow: 0 0 15px rgba(200,240,255,0.4) !important;
        }

        /* Exit button */
        #freeze-exit-btn {
          position: fixed;
          bottom: 20px;
          right: 20px;
          z-index: 10002;
          background: rgba(255,255,255,0.9);
          color: #003366;
          border: 2px solid rgba(200,240,255,0.8);
          padding: 10px 20px;
          border-radius: 20px;
          cursor: pointer;
          font-weight: bold;
          box-shadow: 0 0 20px rgba(200,240,255,0.5);
          animation: fade-in 0.5s ease-out;
        }
        #freeze-exit-btn:hover {
          background: rgba(255,255,255,1);
          transform: scale(1.05);
        }
      `;
      document.head.appendChild(freezeStyle);

      // Add exit button
      const exitBtn = document.createElement('button');
      exitBtn.id = 'freeze-exit-btn';
      exitBtn.textContent = '❄️ 동결 해제';
      exitBtn.onclick = deactivateFreezeMode;
      document.body.appendChild(exitBtn);

      console.log('🧊 Freeze Mode Activated!');
    }

    function deactivateFreezeMode() {
      document.body.classList.remove('aurora-mode');

      // Show unfreeze notification
      const notification = document.createElement('div');
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, rgba(255,200,150,1), rgba(255,150,100,1));
        color: #331100;
        padding: 16px 32px;
        border-radius: 12px;
        font-weight: 900;
        font-size: 1rem;
        z-index: 10001;
        border: 2px solid rgba(255,255,255,0.9);
        box-shadow: 0 0 30px rgba(255,200,150,0.6);
        animation: fade-in 0.5s ease-out;
      `;
      notification.textContent = '🔥 동결 해제 완료';
      document.body.appendChild(notification);
      setTimeout(() => notification.remove(), 2000);

      // Remove all freeze elements
      ['#frost-overlay', '#ice-texture', '#ice-border', '#frost-canvas', '#freeze-exit-btn', '#freeze-mode-style', '.corner-ice'].forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => el.remove());
      });

      console.log('🔥 Freeze Mode Deactivated!');
    }

    function initFrostAnimation(canvas) {
      const ctx = canvas.getContext('2d');
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      const crystals = [];
      const numCrystals = 50;

      class IceCrystal {
        constructor() {
          this.reset();
        }

        reset() {
          this.x = Math.random() * canvas.width;
          this.y = Math.random() * canvas.height;
          this.size = Math.random() * 20 + 10;
          this.rotation = Math.random() * Math.PI * 2;
          this.rotationSpeed = (Math.random() - 0.5) * 0.01;
          this.opacity = Math.random() * 0.3 + 0.1;
          this.growth = 0;
          this.maxGrowth = 1;
        }

        update() {
          this.rotation += this.rotationSpeed;
          if (this.growth < this.maxGrowth) {
            this.growth += 0.02;
          }
        }

        draw() {
          ctx.save();
          ctx.translate(this.x, this.y);
          ctx.rotate(this.rotation);
          ctx.globalAlpha = this.opacity * this.growth;
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
          ctx.fillStyle = 'rgba(200, 240, 255, 0.3)';
          ctx.lineWidth = 1;

          // Draw hexagonal ice crystal
          ctx.beginPath();
          for (let i = 0; i < 6; i++) {
            const angle = (i * Math.PI) / 3;
            const x = Math.cos(angle) * this.size * this.growth;
            const y = Math.sin(angle) * this.size * this.growth;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.closePath();
          ctx.fill();
          ctx.stroke();

          // Inner details
          ctx.beginPath();
          for (let i = 0; i < 6; i++) {
            const angle = (i * Math.PI) / 3;
            const x = Math.cos(angle) * this.size * 0.5 * this.growth;
            const y = Math.sin(angle) * this.size * 0.5 * this.growth;
            ctx.moveTo(0, 0);
            ctx.lineTo(x, y);
          }
          ctx.stroke();

          ctx.restore();
        }
      }

      for (let i = 0; i < numCrystals; i++) {
        crystals.push(new IceCrystal());
      }

      let animationId;
      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        crystals.forEach(c => {
          c.update();
          c.draw();
        });
        animationId = requestAnimationFrame(animate);
      }
      animate();

      window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
      }, { passive: true });
    }
  }

  // ========================================
  // 5. Scroll Ripple Effect
  // ========================================
  function initScrollRipple() {
    const journeySection = document.querySelector('#temp-journey, .temp-journey-section');
    if (!journeySection) return;

    let rippleCanvas = document.createElement('canvas');
    rippleCanvas.id = 'ripple-canvas';
    rippleCanvas.style.cssText = `
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 0;
    `;
    journeySection.style.position = 'relative';
    journeySection.insertBefore(rippleCanvas, journeySection.firstChild);

    const ctx = rippleCanvas.getContext('2d');
    let ripples = [];

    function resize() {
      rippleCanvas.width = journeySection.offsetWidth;
      rippleCanvas.height = journeySection.offsetHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    class Ripple {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 0;
        this.maxRadius = Math.max(rippleCanvas.width, rippleCanvas.height) * 0.5;
        this.opacity = 0.3;
        this.speed = 3;
      }

      update() {
        this.radius += this.speed;
        this.opacity = 0.3 * (1 - this.radius / this.maxRadius);
        return this.opacity > 0;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(0, 212, 255, ${this.opacity})`;
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    }

    // Create ripple when scrolling through journey section
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          createRipple();
        }
      });
    }, { threshold: 0.5 });

    observer.observe(journeySection);

    function createRipple() {
      const x = rippleCanvas.width / 2;
      const y = rippleCanvas.height / 2;
      ripples.push(new Ripple(x, y));
    }

    // Also create ripple on step activation
    document.querySelectorAll('.temp-journey-step').forEach(step => {
      const stepObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && entry.target.classList.contains('active')) {
            createRipple();
          }
        });
      }, { threshold: 0.5 });
      stepObserver.observe(step);
    });

    function animate() {
      ctx.clearRect(0, 0, rippleCanvas.width, rippleCanvas.height);
      ripples = ripples.filter(r => r.update());
      ripples.forEach(r => r.draw());
      requestAnimationFrame(animate);
    }
    animate();
  }

  // ========================================
  // 7. Typing Hero Title (Looping)
  // ========================================
  function initTypingHero() {
    const heroTitle = document.querySelector('#hero h1, .hero-title');
    if (!heroTitle) return;

    // Multiple texts to cycle through
    const texts = [
      '극한의 온도',
      '무한한 가능성',
      '초저온 기술의',
      '선구자 KC'
    ];

    let currentIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingSpeed = 100;
    const deleteSpeed = 50;
    const pauseTime = 2000;

    heroTitle.textContent = '';
    heroTitle.style.borderRight = '3px solid #00d4ff';
    heroTitle.style.paddingRight = '8px';

    // Add cursor blink animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes cursor-blink {
        0%, 100% { border-color: #00d4ff; }
        50% { border-color: transparent; }
      }
      .typing-cursor {
        animation: cursor-blink 1s infinite;
      }
    `;
    document.head.appendChild(style);

    heroTitle.classList.add('typing-cursor');

    function typeLoop() {
      const currentText = texts[currentIndex];

      if (isDeleting) {
        // Deleting
        heroTitle.textContent = currentText.substring(0, charIndex - 1);
        charIndex--;

        if (charIndex === 0) {
          isDeleting = false;
          currentIndex = (currentIndex + 1) % texts.length;
          setTimeout(typeLoop, 300);
        } else {
          setTimeout(typeLoop, deleteSpeed);
        }
      } else {
        // Typing
        heroTitle.textContent = currentText.substring(0, charIndex + 1);
        charIndex++;

        if (charIndex === currentText.length) {
          isDeleting = true;
          setTimeout(typeLoop, pauseTime);
        } else {
          setTimeout(typeLoop, typingSpeed);
        }
      }
    }

    // Start typing loop after delay
    setTimeout(typeLoop, 800);
  }

  // ========================================
  // 8. Scroll Snap Sections
  // ========================================
  function initScrollSnap() {
    // Only enable on desktop
    if (window.matchMedia('(pointer: coarse)').matches) return;

    const sections = document.querySelectorAll('section[id]');
    if (sections.length < 2) return;

    let isSnapping = false;
    let snapTimeout;

    const observerOptions = {
      root: null,
      rootMargin: '-40% 0px -40% 0px',
      threshold: 0
    };

    const sectionObserver = new IntersectionObserver((entries) => {
      if (isSnapping) return;

      entries.forEach(entry => {
        if (entry.isIntersecting) {
          clearTimeout(snapTimeout);
          snapTimeout = setTimeout(() => {
            snapToSection(entry.target);
          }, 100);
        }
      });
    }, observerOptions);

    sections.forEach(section => sectionObserver.observe(section));

    function snapToSection(section) {
      const sectionTop = section.offsetTop;
      const currentScroll = window.scrollY;
      const distance = Math.abs(sectionTop - currentScroll);

      if (distance > 50 && distance < window.innerHeight * 0.8) {
        isSnapping = true;
        window.scrollTo({
          top: sectionTop,
          behavior: 'smooth'
        });

        setTimeout(() => {
          isSnapping = false;
        }, 800);
      }
    }

    // Disable snap during manual scroll momentum
    let lastScrollTime = 0;
    window.addEventListener('scroll', () => {
      lastScrollTime = Date.now();
    }, { passive: true });
  }

  // ========================================
  // Initialize All
  // ========================================
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', runInit);
    } else {
      runInit();
    }
  }

  function runInit() {
    initTempJourney();
    initTimeline();
    initStatsCounter();
    initSmoothScroll();
    initProductSwipe();
    initHeroParallax();
    initBackToTop();
    initLazyLoading();
    initTempConverter();
    initIceParticles();
    initQuizGamification();
    init3DTiltCards();
    initEasterEgg();
    initScrollRipple();
    initTypingHero();
    initScrollSnap();

    console.log('🧊 KoreaCryo enhancements loaded');
  }

  init();
})();
