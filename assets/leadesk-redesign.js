/* =========================================================================
   Leadesk — Redesign-Entwurf: zusätzliche Interaktionen.
   ADDITIVE Datei — ergänzt assets/leadesk.js, ersetzt nichts.
   Muss NACH leadesk.js eingebunden werden. Gleiches IIFE-Pattern, gleiche
   prefers-reduced-motion-Abfrage wie im bestehenden Code.
   ========================================================================= */
(function(){
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1) Mobile-Navigation: Vollbild-Overlay ---------- */
  var burger = document.getElementById('navBurger');
  var overlay = document.getElementById('navOverlay');
  if(burger && overlay){
    function closeOverlay(){
      overlay.classList.remove('open');
      burger.setAttribute('aria-expanded','false');
      document.body.classList.remove('nav-locked');
    }
    burger.addEventListener('click', function(){
      var isOpen = overlay.classList.toggle('open');
      burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      document.body.classList.toggle('nav-locked', isOpen);
    });
    overlay.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', closeOverlay); });
    overlay.querySelectorAll('.nav-ov-trigger').forEach(function(t){
      t.addEventListener('click', function(){ t.closest('.nav-ov-group').classList.toggle('open'); });
    });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeOverlay(); });
  }

  /* ---------- 2) Wort-für-Wort Scroll-Reveal ---------- */
  var wordBlocks = document.querySelectorAll('.word-reveal');
  if(wordBlocks.length){
    wordBlocks.forEach(function(block){
      if(block.dataset.split) return;
      var html = block.innerHTML.trim();
      var wrapped = html.split(/\s+/).map(function(token){
        var isGrad = /^<grad>|<\/grad>$/.test(token);
        var clean = token.replace(/<\/?grad>/g,'');
        return '<span class="w' + (isGrad ? ' grad' : '') + '">' + clean + '</span>';
      }).join(' ');
      block.innerHTML = wrapped;
      block.dataset.split = '1';
    });

    if(rm){
      wordBlocks.forEach(function(block){ block.querySelectorAll('.w').forEach(function(w){ w.style.opacity = 1; }); });
    } else {
      var ticking = false;
      function updateWordReveal(){
        wordBlocks.forEach(function(block){
          var rect = block.getBoundingClientRect();
          var vh = window.innerHeight;
          var start = vh * 0.92, end = vh * 0.32;
          var raw = (start - rect.top) / (start - end + rect.height * 0.4);
          var progress = Math.max(0, Math.min(1, raw));
          var words = block.querySelectorAll('.w');
          words.forEach(function(w, i){
            var wp = progress * (words.length + 6) - i;
            var op = Math.max(0.16, Math.min(1, wp));
            w.style.opacity = op.toFixed(2);
          });
        });
        ticking = false;
      }
      window.addEventListener('scroll', function(){
        if(!ticking){ ticking = true; requestAnimationFrame(updateWordReveal); }
      }, {passive:true});
      window.addEventListener('resize', updateWordReveal);
      updateWordReveal();
    }
  }

  /* ---------- 3) Karussell: aktive Karte per IntersectionObserver + Punkte ---------- */
  document.querySelectorAll('.gal[data-carousel]').forEach(function(gal){
    var cards = Array.prototype.slice.call(gal.querySelectorAll('.gcard'));
    if(!cards.length) return;
    var dotsWrap = document.querySelector('[data-dots-for="' + gal.id + '"]');
    var dots = [];
    if(dotsWrap){
      cards.forEach(function(_, i){
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', 'Karte ' + (i+1) + ' anzeigen');
        b.addEventListener('click', function(){ cards[i].scrollIntoView({behavior: rm ? 'auto' : 'smooth', inline:'center', block:'nearest'}); });
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }
    function setActive(idx){
      cards.forEach(function(c,i){ c.classList.toggle('is-active', i === idx); });
      dots.forEach(function(d,i){ d.classList.toggle('on', i === idx); });
    }
    var gio = new IntersectionObserver(function(entries){
      var best = null, bestRatio = 0;
      entries.forEach(function(e){ if(e.intersectionRatio > bestRatio){ bestRatio = e.intersectionRatio; best = e.target; } });
      if(best){ setActive(cards.indexOf(best)); }
    }, {root: gal, threshold: [0.3,0.5,0.7,0.9]});
    cards.forEach(function(c){ gio.observe(c); });
    setActive(0);
  });

  /* ---------- 4) Zielgruppen-Tabs (Segmented Control) ---------- */
  document.querySelectorAll('.persona-tabs').forEach(function(tabs){
    var seg = tabs.querySelector('.seg');
    var panels = tabs.querySelectorAll('.persona-panel');
    if(!seg || !panels.length) return;
    seg.querySelectorAll('span').forEach(function(btn){
      btn.addEventListener('click', function(){
        seg.querySelectorAll('span').forEach(function(s){ s.classList.remove('on'); });
        btn.classList.add('on');
        var target = btn.getAttribute('data-target');
        panels.forEach(function(p){ p.classList.toggle('show', p.id === target); });
      });
    });
  });

  /* ---------- 5) KI-Schalter-Demo: kippt einmalig beim Einscrollen (wie #toolstage) ---------- */
  document.querySelectorAll('.ai-demo').forEach(function(demo){
    var aio = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){
          if(rm){ demo.classList.add('on'); } else { setTimeout(function(){ demo.classList.add('on'); }, 350); }
          aio.unobserve(e.target);
        }
      });
    }, {threshold:0.5});
    aio.observe(demo);
  });
})();
