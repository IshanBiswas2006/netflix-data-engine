/**
 * Netflix Movies and TV Shows Analysis — Frontend Interactions
 * Faithfully redesigned with micro-interactions, accordion animations,
 * search filtering, and header scroll effects matching reference site.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Frosted Header Scroll Effect
  const header = document.querySelector('#site-header');
  if (header) {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // 2. Mobile Navigation Toggle
  const toggleBtn = document.querySelector('#mobile-nav-toggle');
  const navLinks = document.querySelector('#main-navigation');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const expanded = navLinks.classList.contains('open');
      toggleBtn.setAttribute('aria-expanded', expanded);
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (!toggleBtn.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        toggleBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 3. SQL Query Accordion Expand / Collapse
  const queryBoxes = document.querySelectorAll('.query-box');
  queryBoxes.forEach((box, index) => {
    const header = box.querySelector('.query-header');
    const content = box.querySelector('.query-content');
    if (header && content) {
      // Keep first 2 open by default, close the rest for clean visual hierarchy
      if (index >= 2) {
        content.style.display = 'none';
        box.classList.remove('active');
        header.setAttribute('aria-expanded', 'false');
      } else {
        box.classList.add('active');
        header.setAttribute('aria-expanded', 'true');
      }

      header.addEventListener('click', () => {
        const isClosed = content.style.display === 'none';
        content.style.display = isClosed ? 'block' : 'none';
        box.classList.toggle('active', isClosed);
        header.setAttribute('aria-expanded', isClosed ? 'true' : 'false');
      });

      // Keyboard accessibility (Enter / Space)
      header.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          header.click();
        }
      });
    }
  });

  // 4. Client-Side Table Search / Filter
  const searchInputs = document.querySelectorAll('.table-search-input, #table-search-input');
  searchInputs.forEach(searchInput => {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      const tables = document.querySelectorAll('.data-table');
      tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(query) ? '' : 'none';
        });
      });
    });
  });

  // 5. Card Hover Focus Micro-Interactions
  const cards = document.querySelectorAll('.showcase-card, .stat-card, .chart-card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.willChange = 'transform, border-color, box-shadow';
    });
    card.addEventListener('mouseleave', () => {
      card.style.willChange = 'auto';
    });
  });

  // 6. Reference Portfolio Custom Cursor
  const cursor = document.querySelector('#custom-cursor');
  const isFinePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  if (cursor && isFinePointer) {
    // Hide OS cursor immediately on fine pointer desktop
    document.documentElement.classList.add('has-custom-cursor');
    document.body.classList.add('has-custom-cursor');

    let mouseX = -100;
    let mouseY = -100;
    let cursorX = -100;
    let cursorY = -100;
    let isVisible = false;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!isVisible) {
        isVisible = true;
        cursorX = mouseX;
        cursorY = mouseY;
        cursor.classList.add('visible');
      }
    }, { passive: true });

    document.addEventListener('mouseleave', () => {
      cursor.classList.remove('visible');
      isVisible = false;
    });

    document.addEventListener('mouseenter', () => {
      cursor.classList.add('visible');
      isVisible = true;
    });

    window.addEventListener('mousedown', () => {
      cursor.classList.add('pressed');
    });

    window.addEventListener('mouseup', () => {
      cursor.classList.remove('pressed');
    });

    const interactiveSelector = 'a, button, [role="button"], .btn-primary, .btn-secondary, .query-header, .stat-card, .showcase-card, .chart-card, .tab-btn';
    const textInputSelector = 'input, textarea, select, [contenteditable="true"]';

    document.addEventListener('mouseover', (e) => {
      if (e.target.closest && e.target.closest(textInputSelector)) {
        cursor.classList.add('text-mode');
        cursor.classList.remove('hover');
        return;
      }
      if (e.target.closest && e.target.closest(interactiveSelector)) {
        cursor.classList.add('hover');
      }
    });

    document.addEventListener('mouseout', (e) => {
      if (e.target.closest && e.target.closest(textInputSelector)) {
        cursor.classList.remove('text-mode');
      }
      if (e.target.closest && e.target.closest(interactiveSelector)) {
        const nextElem = e.relatedTarget;
        if (!nextElem || !nextElem.closest || !nextElem.closest(interactiveSelector)) {
          cursor.classList.remove('hover');
        }
      }
    });

    // Smooth Lerp Animation Loop (60/120fps)
    const lerpFactor = 0.22;
    function renderCursor() {
      if (isVisible) {
        cursorX += (mouseX - cursorX) * lerpFactor;
        cursorY += (mouseY - cursorY) * lerpFactor;
        cursor.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0) translate(-50%, -50%)`;
      }
      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);
  }
});



