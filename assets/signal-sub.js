/* =========================================================================
   Leadesk — „Signal“ für alle Unterseiten: Interaktionen
   Ergänzt leadesk.js / leadesk-redesign.js. Kein Framework.
   Erzeugt Korn, Cursor, Signalfeld + Geisterwort im Page-Hero selbst,
   damit die 45 Seiten kein zusätzliches Markup brauchen.
   prefers-reduced-motion: alles statisch, kein eigener Cursor.
   ========================================================================= */
(function(){
  var doc = document.documentElement, body = document.body;
  if(!body.classList.contains('sig-sub')) return;
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var clamp = function(v,a,b){ return Math.max(a, Math.min(b, v)); };
  var lerp = function(a,b,t){ return a + (b-a)*t; };
  var ease = function(t){ return t<.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2; };
  var $ = function(s,c){ return (c||document).querySelector(s); };
  var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };
  var mouse = {x:-9999, y:-9999, on:false};
  window.addEventListener('mousemove', function(e){ mouse.x = e.clientX; mouse.y = e.clientY; mouse.on = true; if(cur) cur.classList.add('live'); }, {passive:true});
  document.addEventListener('mouseleave', function(){ mouse.on = false; });

  /* ---------- Emojis aus dem sichtbaren Text entfernen (passen nicht zum Look) ---------- */
  try{
    var emo = /[\u{1F1E6}-\u{1F1FF}]|\p{Extended_Pictographic}|\uFE0F|\u200D/gu;
    var tw = document.createTreeWalker(body, NodeFilter.SHOW_TEXT, {acceptNode:function(n){
      var p = n.parentNode; if(!p || /^(SCRIPT|STYLE|TEXTAREA)$/.test(p.nodeName)) return NodeFilter.FILTER_REJECT;
      emo.lastIndex = 0; return emo.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; }});
    var hits = []; while(tw.nextNode()) hits.push(tw.currentNode);
    hits.forEach(function(n){ n.nodeValue = n.nodeValue.replace(emo,'').replace(/^\s+(?=\S)/, function(m){ return n.previousSibling ? m : ''; }); });
  }catch(e){}

  /* ---------- Korn + Cursor einfügen ---------- */
  var grain = document.createElement('div'); grain.className = 'grain'; grain.setAttribute('aria-hidden','true'); body.appendChild(grain);
  var cur = null, ring, dot, label, rx = 0, ry = 0;
  if(fine && !rm){
    cur = document.createElement('div'); cur.className = 'cur'; cur.setAttribute('aria-hidden','true');
    cur.innerHTML = '<span class="cur-dot"></span><span class="cur-ring"><em></em></span>';
    body.appendChild(cur); ring = $('.cur-ring', cur); dot = $('.cur-dot', cur); label = $('em', ring);
    doc.classList.add('has-cur');
    document.addEventListener('mouseover', function(e){
      var a = e.target.closest('a,button,summary,.seg span,[data-cur]');
      cur.classList.toggle('hover', !!a);
      var t = '';
      if(a){ t = a.getAttribute('data-cur') || (a.classList.contains('btn-primary') ? 'Los' : (a.tagName === 'SUMMARY' ? 'Auf' : '')); }
      label.textContent = t;
    });
  }

  /* ---------- Page-Hero: Meta-Zeile, Geisterwort, Signalfeld ---------- */
  var hero = $('.page-hero');
  var ghost = null, canvas = null, ctx, cw = 0, ch = 0, dots = [], heroVis = true, dpr = Math.min(window.devicePixelRatio||1, 2);
  if(hero){
    var eb = $('.eyebrow', hero), h1 = $('h1', hero);
    var word = (eb ? eb.textContent : (h1 ? h1.textContent : 'Leadesk')).split(/[·&|—,]/)[0].replace(/\s+/g,' ').trim();
    if(word.length > 16) word = word.split(' ')[0];
    var meta = document.createElement('div'); meta.className = 'ph-meta'; meta.setAttribute('aria-hidden','true');
    meta.innerHTML = '<span>(Leadesk)</span><span>' + (document.title.split(/[–—|]/)[0].trim()) + '</span><span data-clock>Berlin --:--:--</span>';
    hero.appendChild(meta);
    var clk = $('[data-clock]', meta);
    var tick = function(){ clk.textContent = 'Berlin ' + new Date().toLocaleTimeString('de-DE',{timeZone:'Europe/Berlin'}); };
    tick(); setInterval(tick, 1000);
    ghost = document.createElement('div'); ghost.className = 'ph-ghost'; ghost.setAttribute('aria-hidden','true'); ghost.textContent = word;
    hero.appendChild(ghost);
    canvas = document.createElement('canvas'); canvas.className = 'ph-field'; canvas.setAttribute('aria-hidden','true');
    hero.insertBefore(canvas, hero.firstChild); ctx = canvas.getContext('2d');
    new IntersectionObserver(function(en){ heroVis = en[0].isIntersecting; }).observe(hero);
  }
  function buildDots(){
    if(!canvas) return;
    var r = hero.getBoundingClientRect(); cw = r.width; ch = r.height;
    canvas.width = cw*dpr; canvas.height = ch*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
    var g = cw < 700 ? 22 : 28; dots = [];
    for(var y=g/2; y<ch; y+=g){ for(var x=g/2; x<cw; x+=g){ dots.push({ox:x, oy:y, x:x, y:y}); } }
    drawDots(0, true);
  }
  function drawDots(t, still){
    ctx.clearRect(0,0,cw,ch);
    var hr = hero.getBoundingClientRect(), mx = mouse.x - hr.left, my = mouse.y - hr.top, R = 170, R2 = R*R;
    for(var i=0;i<dots.length;i++){
      var d = dots[i], wave = still ? 0 : Math.sin(t*0.0012 + d.ox*0.012 + d.oy*0.008);
      var tx = d.ox, ty = d.oy + wave*2.2, k = 0;
      if(!still && mouse.on){
        var dx = d.ox - mx, dy = d.oy - my, dd = dx*dx + dy*dy;
        if(dd < R2){ var dist = Math.sqrt(dd)||1; k = 1 - dist/R; tx += dx/dist*k*34; ty += dy/dist*k*34; }
      }
      d.x = still ? tx : lerp(d.x, tx, 0.16); d.y = still ? ty : lerp(d.y, ty, 0.16);
      var a = 0.12 + k*0.75 + (wave+1)*0.03, s = 1.3 + k*2.6;
      ctx.fillStyle = k > 0.05 ? 'rgba(22,168,220,'+a.toFixed(3)+')' : 'rgba(236,234,227,'+a.toFixed(3)+')';
      ctx.fillRect(d.x - s/2, d.y - s/2, s, s);
    }
  }

  /* ---------- Scramble für Eyebrows ---------- */
  var glyphs = '█▓▒░<>/\\[]{}=+*#%&@01ABCDEFXYZ';
  function scramble(el){
    var final = el.getAttribute('data-final') || el.textContent; el.setAttribute('data-final', final);
    var t0 = performance.now(), dur = 650;
    (function f(t){
      var p = clamp((t-t0)/dur,0,1), out = '';
      for(var i=0;i<final.length;i++){ out += (final[i]===' ' || i < p*final.length) ? final[i] : glyphs[(Math.random()*glyphs.length)|0]; }
      el.textContent = out; if(p<1) requestAnimationFrame(f);
    })(t0);
  }
  if(!rm){
    var sio = new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting){ scramble(e.target); sio.unobserve(e.target); } }); }, {threshold:.8});
    $$('.eyebrow').forEach(function(el){ if(!el.children.length) sio.observe(el); });
  }

  /* ---------- Weiße Flächen in Mocks abdunkeln (seitenspezifische Styles mit #fff) ---------- */
  $$('.mock *, .page-hero *').forEach(function(el){
    var bg = getComputedStyle(el).backgroundColor;
    if(bg === 'rgb(255, 255, 255)'){ el.style.backgroundColor = 'rgba(255,255,255,.05)'; el.style.borderColor = 'rgba(255,255,255,.16)'; }
  });

  /* ---------- Spotlight auf Karten ---------- */
  $$('.card,.mtile,.persona,.gcard,.svc-card,.dl-card,.plan').forEach(function(c){
    c.addEventListener('mousemove', function(e){ var b = c.getBoundingClientRect(); c.style.setProperty('--mx', (e.clientX-b.left)+'px'); c.style.setProperty('--my', (e.clientY-b.top)+'px'); });
  });

  /* ---------- Magnetische Primär-Buttons ---------- */
  var mags = fine && !rm ? $$('.btn-primary').filter(function(b){ return !b.closest('header') && !b.closest('.nav-overlay'); }) : [];

  /* ---------- CTA-Band: Wisch-Einblendung ---------- */
  var bands = $$('.cta-band');

  /* ---------- Loop ---------- */
  function frame(t){
    if(canvas && heroVis && !rm) drawDots(t, false);
    if(ghost && !rm){
      var sy = window.scrollY;
      ghost.style.transform = 'translate3d(' + (-sy*0.35 + (mouse.on ? (mouse.x/innerWidth - .5)*-40 : 0)).toFixed(1) + 'px,' + (sy*0.12).toFixed(1) + 'px,0)';
    }
    if(!rm){
      bands.forEach(function(s){
        var r = s.getBoundingClientRect(); if(r.bottom < 0 || r.top > innerHeight*1.1) return;
        var e = 1 - ease(clamp((innerHeight - r.top)/(innerHeight*0.7), 0, 1));
        s.style.setProperty('--wy', (e*14).toFixed(2)+'%'); s.style.setProperty('--wx', (e*10).toFixed(2)+'%'); s.style.setProperty('--wr', (e*80).toFixed(1)+'px');
      });
    }
    mags.forEach(function(m){
      var b = m.getBoundingClientRect(), dx = mouse.x - (b.left + b.width/2), dy = mouse.y - (b.top + b.height/2), d = Math.hypot(dx,dy), R = Math.max(b.width, 110);
      var k = d < R ? 1 - d/R : 0; m.style.transform = 'translate(' + (dx*k*0.3).toFixed(1) + 'px,' + (dy*k*0.4).toFixed(1) + 'px)';
    });
    if(cur){
      rx = lerp(rx, mouse.x, 0.2); ry = lerp(ry, mouse.y, 0.2);
      dot.style.transform = 'translate(' + mouse.x + 'px,' + mouse.y + 'px)';
      ring.style.transform = 'translate(' + rx.toFixed(1) + 'px,' + ry.toFixed(1) + 'px)';
    }
    requestAnimationFrame(frame);
  }
  var rsT; window.addEventListener('resize', function(){ clearTimeout(rsT); rsT = setTimeout(buildDots, 150); });
  buildDots();
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(buildDots);
  setTimeout(buildDots, 1600);
  requestAnimationFrame(frame);
})();
