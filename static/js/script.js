        document.addEventListener('DOMContentLoaded', function() {
            const burgerMenu = document.querySelector('.burger-menu');
            const nav = document.querySelector('nav');
            
            burgerMenu.addEventListener('click', function() {
                this.classList.toggle('active');
                nav.classList.toggle('active');
            });
            
            // Close menu when clicking on a link
            const navLinks = document.querySelectorAll('nav a');
            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    burgerMenu.classList.remove('active');
                    nav.classList.remove('active');
                });
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', function(event) {
                const isClickInsideNav = nav.contains(event.target);
                const isClickOnBurger = burgerMenu.contains(event.target);
                
                if (!isClickInsideNav && !isClickOnBurger && nav.classList.contains('active')) {
                    burgerMenu.classList.remove('active');
                    nav.classList.remove('active');
                }
            });
        });
// ---------------------Services--------------------------------------
    // Accordion behavior: single open at a time. Smoothly expand/collapse.
    (function(){
      const list = document.getElementById('servicesList');
      const items = Array.from(list.querySelectorAll('.service-item'));

      function closeItem(item) {
        const header = item.querySelector('.service-header');
        const desc = item.querySelector('.service-desc');
        item.classList.remove('open');
        header.setAttribute('aria-expanded', 'false');
        desc.setAttribute('aria-hidden', 'true');
        // optional: shrink max-height to 0 after transition starts for reliability
        // desc.style.maxHeight = '0px';
      }

      function openItem(item) {
        const header = item.querySelector('.service-header');
        const desc = item.querySelector('.service-desc');
        // close others
        items.forEach(i => {
          if (i !== item) closeItem(i);
        });

        // open this
        item.classList.add('open');
        header.setAttribute('aria-expanded', 'true');
        desc.setAttribute('aria-hidden', 'false');

        // For better animation with dynamic content: set explicit maxHeight to scrollHeight
        // so CSS transition animates to exact height.
        // (we set max-height in CSS to a large value for general case; here we override)
        const inner = desc.querySelector('.inner');
        if (inner) {
          const target = inner.scrollHeight + 20; // small padding
          desc.style.maxHeight = target + 'px';
        } else {
          desc.style.maxHeight = '400px';
        }
      }

      // Initialize: ensure all closed
      items.forEach(i => {
        const desc = i.querySelector('.service-desc');
        desc.style.maxHeight = '0px';
        i.classList.remove('open');
      });

      // Click and key handlers
      items.forEach(item => {
        const header = item.querySelector('.service-header');
        const desc = item.querySelector('.service-desc');

        header.addEventListener('click', () => {
          const isOpen = item.classList.contains('open');
          if (isOpen) {
            closeItem(item);
          } else {
            openItem(item);
            // scroll into view if needed (nice UX on small devices)
            setTimeout(()=>{
              const rect = item.getBoundingClientRect();
              if (rect.top < 60 || rect.bottom > (window.innerHeight - 60)) {
                item.scrollIntoView({behavior:'smooth', block:'start'});
              }
            }, 260);
          }
        });

        // keyboard accessibility
        header.addEventListener('keydown', (ev) => {
          if (ev.key === 'Enter' || ev.key === ' ') {
            ev.preventDefault();
            header.click();
          }
        });

        // After transition ends, if closed, remove explicit maxHeight so future open can compute again
        desc.addEventListener('transitionend', (e) => {
          if (!item.classList.contains('open')) {
            desc.style.maxHeight = '0px';
          } else {
            // keep it auto-sized to allow content changes (remove explicit height)
            desc.style.maxHeight = 'none';
          }
        });
      });

      // Optional: open first item by default
      // openItem(items[0]);
    })();
