/* ==========================================================================
   Crypto Master — Professional Multi-Market Trader Portfolio
   JavaScript Logic & Interactivity
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggler
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      const isExpanded = navMenu.classList.contains('active');
      mobileToggle.setAttribute('aria-expanded', isExpanded);
      mobileToggle.innerHTML = isExpanded ? '✕' : '☰';
    });

    // Close menu when a link is clicked
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        mobileToggle.innerHTML = '☰';
      });
    });
  }

  // 2. Active Navigation Link on Scroll
  const sections = document.querySelectorAll('section[id]');
  
  function highlightNavOnScroll() {
    const scrollY = window.pageYOffset;
    
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      
      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        document.querySelector(`.nav-link[href*="${sectionId}"]`)?.classList.add('active');
      } else {
        document.querySelector(`.nav-link[href*="${sectionId}"]`)?.classList.remove('active');
      }
    });
  }

  window.addEventListener('scroll', highlightNavOnScroll);

  // 3. Scroll Reveal Animations (IntersectionObserver)
  const revealElements = document.querySelectorAll('.market-card, .stat-card, .pillar-card, .achievement-card');
  
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const revealOnScroll = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  revealElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(25px)';
    el.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
    revealOnScroll.observe(el);
  });

  // 4. Interactive Contact Form Submission Handler
  const contactForm = document.getElementById('contact-form');
  const formStatus = document.getElementById('form-status');

  if (contactForm && formStatus) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.innerHTML;
      
      // Loading state
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
          <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="10"></circle>
        </svg>
        Sending...
      `;

      // Simulate form submission delay
      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
        
        contactForm.reset();
        formStatus.className = 'form-status success';
        formStatus.textContent = '✓ Thank you! Your message has been sent successfully. I will get back to you shortly.';
        
        setTimeout(() => {
          formStatus.style.display = 'none';
        }, 6000);
      }, 1200);
    });
  }

  // 5. Live Market Price Simulation (Adds dynamic feel to ticker)
  const tickerItems = [
    { symbol: 'BTC/USD', priceEl: 'btc-price', changeEl: 'btc-change', basePrice: 94250.00, isCrypto: true },
    { symbol: 'ETH/USD', priceEl: 'eth-price', changeEl: 'eth-change', basePrice: 3480.50, isCrypto: true },
    { symbol: 'EUR/USD', priceEl: 'eur-price', changeEl: 'eur-change', basePrice: 1.0845, isCrypto: false },
    { symbol: 'S&P 500', priceEl: 'sp-price', changeEl: 'sp-change', basePrice: 5980.20, isCrypto: false },
    { symbol: 'GOLD', priceEl: 'gold-price', changeEl: 'gold-change', basePrice: 2745.10, isCrypto: false }
  ];

  function updateTickerSimulation() {
    const item = tickerItems[Math.floor(Math.random() * tickerItems.length)];
    const priceNode = document.getElementById(item.priceEl);
    const changeNode = document.getElementById(item.changeEl);
    
    if (!priceNode || !changeNode) return;

    // Small random fluctuation (-0.15% to +0.15%)
    const deltaPercent = (Math.random() * 0.3 - 0.15);
    const currentPrice = parseFloat(priceNode.textContent.replace(/[^0-9.]/g, ''));
    const newPrice = currentPrice * (1 + deltaPercent / 100);
    
    const formattedPrice = item.isCrypto && newPrice > 1000 
      ? '$' + newPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      : (item.symbol.includes('/') && !item.isCrypto
          ? newPrice.toFixed(4)
          : '$' + newPrice.toFixed(2));

    priceNode.textContent = formattedPrice;

    // Pulse effect
    priceNode.style.color = deltaPercent >= 0 ? 'var(--bull-green)' : 'var(--bear-red)';
    setTimeout(() => {
      priceNode.style.color = 'var(--text-secondary)';
    }, 800);
  }

  // Update ticker every 3.5 seconds
  setInterval(updateTickerSimulation, 3500);
});
