/* =========================================================================
   Leadesk — Startseite „Signal“: Interaktionen
   Ein IIFE, kein Framework. Ein einziger rAF-Loop für alles Scroll-Getriebene.
   prefers-reduced-motion: keine Partikelbewegung, kein Pinning, kein Cursor.
   ========================================================================= */
(function(){
  var doc = document.documentElement;
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var mobile = function(){ return window.innerWidth <= 700; };
  var clamp = function(v,a,b){ return Math.max(a, Math.min(b, v)); };
  var lerp = function(a,b,t){ return a + (b-a)*t; };
  var ease = function(t){ return t<.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2; };
  var $ = function(s,c){ return (c||document).querySelector(s); };
  var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };
  var mouse = {x: innerWidth/2, y: innerHeight/2, on:false};
  window.addEventListener('mousemove', function(e){ mouse.x = e.clientX; mouse.y = e.clientY; mouse.on = true; }, {passive:true});
  document.addEventListener('mouseleave', function(){ mouse.on = false; });

  /* ---------- Text in Zeichen zerlegen (barrierearm: aria-label + aria-hidden) ---------- */
  function splitChars(el, cls, startIdx){
    var i = startIdx || 0, txt = el.textContent, out = '';
    txt.split(/(\s+)/).forEach(function(w){
      if(!w) return;
      if(/^\s+$/.test(w)){ out += ' '; return; }
      out += '<span style="display:inline-block;white-space:nowrap">';
      for(var k=0;k<w.length;k++){ out += '<span class="'+cls+'" style="--i:'+(i++)+'">'+w[k]+'</span>'; }
      out += '</span>';
    });
    el.innerHTML = out;
    return i;
  }
  var h1 = $('#megaH1');
  if(h1){
    h1.setAttribute('aria-label', h1.textContent.replace(/\s+/g,' ').trim());
    var n = splitChars($('.r1', h1), 'ch', 0);
    splitChars($('.r2 em', h1), 'ch', n + 2);
    $$('.row', h1).forEach(function(r){ r.setAttribute('aria-hidden','true'); });
  }
  var fin = $('[data-prox]');
  if(fin){
    fin.setAttribute('aria-label', fin.textContent.replace(/\s+/g,' ').trim());
    $$('.fl', fin).forEach(function(f){ splitChars(f, 'c'); f.setAttribute('aria-hidden','true'); });
  }

  /* ---------- Scramble für Mono-Labels ---------- */
  var glyphs = '█▓▒░<>/\\[]{}=+*#%&@01ABCDEFXYZ';
  function scramble(el){
    var final = el.getAttribute('data-final') || el.textContent;
    el.setAttribute('data-final', final);
    if(rm){ el.textContent = final; return; }
    var t0 = performance.now(), dur = 700;
    (function f(t){
      var p = clamp((t-t0)/dur,0,1), out = '';
      for(var i=0;i<final.length;i++){
        if(final[i]===' ' || i < p*final.length){ out += final[i]; }
        else { out += glyphs[(Math.random()*glyphs.length)|0]; }
      }
      el.textContent = out;
      if(p<1) requestAnimationFrame(f);
    })(t0);
  }
  var sio = new IntersectionObserver(function(en){
    en.forEach(function(e){ if(e.isIntersecting){ scramble(e.target); sio.unobserve(e.target); } });
  }, {threshold:.6});
  $$('[data-scramble]').forEach(function(el){ sio.observe(el); });

  /* ---------- Uhr ---------- */
  var clock = $('[data-clock]');
  function tickClock(){ if(clock) clock.textContent = 'Berlin ' + new Date().toLocaleTimeString('de-DE',{timeZone:'Europe/Berlin'}); }
  tickClock(); setInterval(tickClock, 1000);

  /* ---------- Hero-Ticker (Beispiel-Ereignisse) ---------- */
  var tk = $('[data-ticker]'), tkn = $('.tk-count b');
  var pool = ['Kontaktanfrage angenommen — Geschäftsführerin, Agentur','Leadly hat 3 Antwortentwürfe vorbereitet','Reel veröffentlicht — Reichweite wird gemessen',
    'Deal verschoben: Angebot → Verhandlung','Post eingeplant — Donnerstag, 09:00','Antwort erhalten — Head of Sales, Maschinenbau','Marke in KI-Antwort genannt','Profilbesuch — Marketing Lead, SaaS'];
  if(tk && !rm){
    var pi = 0;
    setInterval(function(){
      if(document.hidden) return;
      tk.textContent = pool[++pi % pool.length]; scramble(tk);
      var v = parseInt(tkn.getAttribute('data-n'),10) + 1 + ((Math.random()*3)|0);
      tkn.setAttribute('data-n', v); tkn.textContent = v.toLocaleString('de-DE');
    }, 2800);
  }

  /* =========================================================================
     PARTIKEL-FELD: „LEADESK“ aus Punkten, weicht der Maus aus, zerfällt beim Scrollen
     ========================================================================= */
  var canvas = $('.s-hero .field'), ctx = canvas && canvas.getContext('2d');
  var P = [], cw = 0, ch = 0, dpr = Math.min(window.devicePixelRatio||1, 2), heroVisible = true;
  function buildField(){
    if(!canvas) return;
    var r = canvas.getBoundingClientRect();
    cw = r.width; ch = r.height;
    canvas.width = cw*dpr; canvas.height = ch*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
    var off = document.createElement('canvas'), oc = off.getContext('2d');
    off.width = cw; off.height = ch;
    var meta = $('.hero-meta'), hb = canvas.parentNode.getBoundingClientRect();
    var top = meta ? meta.getBoundingClientRect().bottom - hb.top : ch*0.15, bot = h1 ? h1.getBoundingClientRect().top - hb.top : ch*0.6;
    var room = Math.max(60, bot - top);
    var word = 'LEADESK', fs = Math.min(cw*0.2, room*0.82);
    oc.font = '900 ' + fs + 'px Archivo, sans-serif';
    try{ oc.fontStretch = 'condensed'; }catch(e){}
    var w = oc.measureText(word).width;
    if(w > cw*0.94){ fs *= (cw*0.94)/w; oc.font = '900 ' + fs + 'px Archivo, sans-serif'; w = oc.measureText(word).width; }
    oc.fillStyle = '#fff'; oc.textBaseline = 'middle';
    var cy = top + room/2;
    oc.fillText(word, (cw-w)/2, cy);
    var data = oc.getImageData(0,0,cw,ch).data, step = mobile() ? 4 : 5, old = P;
    P = [];
    for(var y=0;y<ch;y+=step){ for(var x=0;x<cw;x+=step){
      if(data[((y|0)*cw + (x|0))*4+3] > 140){
        var o = old[P.length];
        P.push({tx:x, ty:y, x: o ? o.x : Math.random()*cw, y: o ? o.y : Math.random()*ch, vx:0, vy:0,
          s: Math.random()<.12 ? 2.2 : 1.4, c: Math.random()<.14 ? 1 : 0, ph: Math.random()*6.28, rx:(Math.random()-.5), ry:(Math.random()-.5)});
      }
    }}
    // Streupunkte im Raum
    for(var k=0;k<(mobile()?120:320);k++){ P.push({tx:Math.random()*cw, ty:Math.random()*ch, x:Math.random()*cw, y:Math.random()*ch, vx:0, vy:0, s:1, c:2, ph:Math.random()*6.28, rx:0, ry:0, free:1}); }
    if(rm){ drawField(0, 0, true); }
  }
  function drawField(t, disperse, snap){
    ctx.clearRect(0,0,cw,ch);
    // feines Raster
    ctx.strokeStyle = 'rgba(236,234,227,0.045)'; ctx.lineWidth = 1;
    var g = 80; ctx.beginPath();
    for(var x=g;x<cw;x+=g){ ctx.moveTo(x+.5,0); ctx.lineTo(x+.5,ch); }
    for(var y=g;y<ch;y+=g){ ctx.moveTo(0,y+.5); ctx.lineTo(cw,y+.5); }
    ctx.stroke();
    var hr = canvas.getBoundingClientRect(), mx = mouse.x - hr.left, my = mouse.y - hr.top, R = mobile()?70:130, R2 = R*R;
    for(var i=0;i<P.length;i++){
      var p = P[i];
      var tx = p.tx + Math.sin(t*0.0011 + p.ph)*1.2, ty = p.ty + Math.cos(t*0.0013 + p.ph)*1.2;
      if(p.free){ tx = p.tx + Math.sin(t*0.0003+p.ph)*30; ty = p.ty + Math.cos(t*0.0004+p.ph)*30; }
      if(disperse > 0 && !p.free){ tx += p.rx*disperse*900; ty += p.ry*disperse*700 - disperse*200; }
      if(snap){ p.x = tx; p.y = ty; }
      else {
        var dx = p.x - mx, dy = p.y - my, d2 = dx*dx + dy*dy;
        if(mouse.on && d2 < R2){ var f = (1 - d2/R2)*7; var d = Math.sqrt(d2)||1; p.vx += dx/d*f; p.vy += dy/d*f; }
        p.vx += (tx - p.x)*0.045; p.vy += (ty - p.y)*0.045;
        p.vx *= 0.82; p.vy *= 0.82; p.x += p.vx; p.y += p.vy;
      }
      var a = p.free ? 0.35 : (1 - disperse*0.85);
      ctx.fillStyle = p.c===1 ? 'rgba(236,234,227,'+a+')' : (p.c===2 ? 'rgba(22,168,220,'+(a*0.6)+')' : 'rgba(22,168,220,'+a+')');
      ctx.fillRect(p.x, p.y, p.s, p.s);
    }
    // Scanline
    if(!snap){
      var sy = (t*0.12) % (ch+200) - 100;
      var grd = ctx.createLinearGradient(0, sy-60, 0, sy);
      grd.addColorStop(0,'rgba(22,168,220,0)'); grd.addColorStop(1,'rgba(22,168,220,0.08)');
      ctx.fillStyle = grd; ctx.fillRect(0, sy-60, cw, 60);
    }
  }
  if(canvas){
    var go = function(){ buildField(); };
    if(document.fonts && document.fonts.load){ document.fonts.load('900 100px Archivo').then(go, go); } else { go(); }
    new IntersectionObserver(function(en){ heroVisible = en[0].isIntersecting; }).observe(canvas);
  }

  /* =========================================================================
     SCROLL-GETRIEBENE SEQUENZEN
     ========================================================================= */
  var chaos = $('.s-chaos'), wins = $$('.s-chaos .win'), core = $('.s-chaos .core'), chead = $('.chaos-head'), ctabs = $('[data-tabs]');
  var winGeo = [];
  function measureChaos(){
    if(!chaos) return;
    var cx = core.offsetLeft + core.offsetWidth/2, cy = core.offsetTop + core.offsetHeight/2;
    winGeo = wins.map(function(w){
      return {dx: cx - w.offsetLeft, dy: cy - (w.offsetTop + w.offsetHeight/2), r: parseFloat(w.style.getPropertyValue('--r'))||0, d: parseFloat(w.style.getPropertyValue('--d'))||0};
    });
  }
  function updateChaos(t){
    if(!chaos || rm) return;
    var r = chaos.getBoundingClientRect(), span = r.height - innerHeight;
    if(r.bottom < 0 || r.top > innerHeight) return;
    var p = clamp(-r.top / span, 0, 1), left = 6;
    wins.forEach(function(w, i){
      var g = winGeo[i]; if(!g) return;
      var k = ease(clamp((p - 0.12 - g.d*0.035) / 0.36, 0, 1));
      var fx = Math.sin(t*0.0012 + i)*6*(1-k), fy = Math.cos(t*0.001 + i*2)*8*(1-k);
      w.style.transform = 'translate(calc(-50% + ' + (g.dx*k + fx) + 'px),' + (g.dy*k + fy) + 'px) rotate(' + (g.r*(1-k) + k*g.r*-6) + 'deg) scale(' + (1 - k*0.9) + ')';
      w.style.opacity = k > 0.88 ? (1-(k-0.88)/0.12) : 1;
      if(k >= 0.98) left--;
    });
    if(ctabs){ var c = Math.max(1,left); ctabs.textContent = c; ctabs.nextSibling.textContent = c===1 ? ' Tab offen' : ' Tabs offen'; chaos.classList.toggle('done', c===1); }
    var cs;
    if(p < 0.4) cs = 0;
    else if(p < 0.58){ var q = (p-0.4)/0.18; cs = 1 + Math.sin(q*Math.PI)*0.25; cs = q*cs; }
    else if(p < 0.7) cs = 1;
    else { var q2 = ease(clamp((p-0.7)/0.24,0,1)); var need = Math.hypot(innerWidth, innerHeight)*2.2/core.offsetWidth; cs = 1 + q2*need; }
    core.style.transform = 'scale(' + cs.toFixed(3) + ')'; core.classList.toggle('big', cs > 1.6);
    chead.style.opacity = p > 0.72 ? clamp(1-(p-0.72)/0.1, 0, 1) : 1;
  }

  var wipes = $$('.wipe');
  function updateWipes(){
    if(rm) return;
    wipes.forEach(function(s){
      var r = s.getBoundingClientRect();
      if(r.bottom < 0 || r.top > innerHeight*1.1) return;
      var q = clamp((innerHeight - r.top)/(innerHeight*0.75), 0, 1), e = 1-ease(q);
      s.style.setProperty('--wy', (e*9).toFixed(2)+'%'); s.style.setProperty('--wx', (e*7).toFixed(2)+'%'); s.style.setProperty('--wr', (e*60).toFixed(1)+'px');
    });
  }

  /* Kanäle: vertikales Scrollen → horizontale Fahrt */
  var chan = $('.s-chan'), track = $('.chan-track'), panels = $$('.panel'), chanN = $('[data-chan-n]'), chanHead = $('.chan-head'), travel = 0;
  function measureChan(){
    if(!chan || rm || mobile()){ if(track) track.style.transform = ''; if(chan) chan.style.removeProperty('--chan-h'); return; }
    travel = Math.max(0, track.scrollWidth - innerWidth);
    chan.style.setProperty('--chan-h', (travel + innerHeight*1.15) + 'px');
  }
  function updateChan(){
    if(!chan || rm || mobile()) return;
    var r = chan.getBoundingClientRect();
    if(r.bottom < 0 || r.top > innerHeight) return;
    var p = clamp(-r.top / (r.height - innerHeight), 0, 1);
    track.style.transform = 'translate3d(' + (-p*travel).toFixed(1) + 'px,0,0)';
    chanHead.style.setProperty('--cp', p.toFixed(3));
    var best = 0, bd = 1e9;
    panels.forEach(function(pn, i){
      var b = pn.getBoundingClientRect(), c = b.left + b.width/2, d = Math.abs(c - innerWidth/2);
      var k = clamp(1 - d/(innerWidth*0.7), 0, 1);
      pn.style.setProperty('--ps', (62 + 63*k).toFixed(1) + '%');
      if(d < bd){ bd = d; best = i; }
      if(k > 0.75) startTyping(pn);
    });
    if(chanN) chanN.textContent = '0' + (best+1);
  }
  function startTyping(scope){
    $$('[data-type]', scope).forEach(function(el){
      if(el.dataset.typed) return; el.dataset.typed = '1';
      var txt = el.getAttribute('data-type');
      if(rm){ el.textContent = txt; return; }
      var i = 0; (function f(){ el.textContent = txt.slice(0, i++); if(i <= txt.length) setTimeout(f, 18 + Math.random()*30); })();
    });
  }
  if(chan){
    var tio = new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting && (mobile()||rm)) startTyping(e.target); }); }, {threshold:.5});
    panels.forEach(function(p){ tio.observe(p); });
  }

  /* Phone: kippt mit Scroll, folgt der Maus */
  var stage = $('[data-tilt]'), phone = stage && $('.phone', stage), tiltHover = false;
  if(stage && !rm){
    stage.addEventListener('mousemove', function(e){
      tiltHover = true; var b = stage.getBoundingClientRect();
      var x = (e.clientX - b.left)/b.width - .5, y = (e.clientY - b.top)/b.height - .5;
      phone.style.setProperty('--ry', (x*40).toFixed(1)+'deg'); phone.style.setProperty('--rx', (-y*30).toFixed(1)+'deg');
    });
    stage.addEventListener('mouseleave', function(){ tiltHover = false; });
  }
  function updatePhone(){
    if(!stage || rm || tiltHover) return;
    var b = stage.getBoundingClientRect(); if(b.bottom < 0 || b.top > innerHeight) return;
    var q = clamp((innerHeight - b.top)/(innerHeight + b.height), 0, 1);
    phone.style.setProperty('--ry', (lerp(-38, 22, q)).toFixed(1)+'deg'); phone.style.setProperty('--rx', (lerp(18, -6, q)).toFixed(1)+'deg');
  }

  /* Velocity-Marquee */
  var tracks = $$('.vm-track').map(function(el){ return {el:el, x:0, dir: parseFloat(el.getAttribute('data-dir'))||1, w:0}; });
  function measureMarq(){ tracks.forEach(function(t){ t.w = t.el.scrollWidth/2; }); }
  var lastY = scrollY, vel = 0;
  function updateMarq(){
    var dy = scrollY - lastY; lastY = scrollY;
    vel = lerp(vel, dy, 0.12);
    if(rm) return;
    tracks.forEach(function(t){
      t.x -= (1.1 + Math.abs(vel)*0.55) * t.dir * (vel < 0 ? -1 : 1);
      if(t.x <= -t.w) t.x += t.w; if(t.x > 0) t.x -= t.w;
      t.el.style.transform = 'translate3d(' + t.x.toFixed(1) + 'px,0,0) skewX(' + clamp(-vel*0.6, -14, 14).toFixed(2) + 'deg)';
    });
  }

  /* Hero-Headline: Zeile 1 streckt sich mit der Maus */
  var r1 = h1 && $('.r1', h1), stMax = 118;
  function fitHero(){
    if(!r1) return;
    var box = h1.clientWidth || h1.parentNode.clientWidth;
    r1.style.transition = 'none'; r1.style.setProperty('--st', stMax + '%'); h1.style.setProperty('--mfs', '10vw');
    var w = r1.scrollWidth, fsz = parseFloat(getComputedStyle(h1).fontSize);
    if(w > box){ h1.style.setProperty('--mfs', (fsz * box / w * 0.98 / innerWidth * 100).toFixed(2) + 'vw'); }
    r1.style.setProperty('--st', '100%'); r1.offsetWidth; r1.style.transition = '';
  }
  function updateHeroType(){
    if(!r1 || rm || !fine) return;
    var k = mouse.on ? mouse.x / innerWidth : .5;
    r1.style.setProperty('--st', (70 + k*55).toFixed(1) + '%');
  }

  /* Finale: Buchstaben reagieren auf Nähe */
  var finChars = fin ? $$('.c', fin) : [];
  function updateFin(t){
    if(!fin || rm) return;
    var b = fin.getBoundingClientRect(); if(b.bottom < 0 || b.top > innerHeight) return;
    var mx = mouse.x, my = mouse.y, auto = !mouse.on || !fine;
    finChars.forEach(function(c, i){
      var r = c.getBoundingClientRect(), cx = r.left + r.width/2, cy = r.top + r.height/2, k;
      if(auto){ k = (Math.sin(t*0.002 - i*0.35) + 1)/2; }
      else { var d = Math.hypot(mx-cx, my-cy); k = clamp(1 - d/320, 0, 1); }
      if(c.closest('.em')){ c.style.setProperty('--ty', (-k*26).toFixed(1)+'px'); c.style.setProperty('--rt', (-k*10).toFixed(1)+'deg'); }
      else { c.style.setProperty('--w', (62 + k*63).toFixed(0)); c.style.setProperty('--g', (900 - k*700).toFixed(0)); }
    });
  }

  /* Magnetische Buttons */
  var mags = $$('.magnetic');
  function updateMag(){
    if(rm || !fine) return;
    mags.forEach(function(m){
      var b = m.getBoundingClientRect(), cx = b.left + b.width/2, cy = b.top + b.height/2, dx = mouse.x - cx, dy = mouse.y - cy, d = Math.hypot(dx,dy), R = Math.max(b.width,b.height)*0.9;
      var k = d < R ? (1 - d/R) : 0;
      m.style.transform = 'translate(' + (dx*k*0.35).toFixed(1) + 'px,' + (dy*k*0.35).toFixed(1) + 'px)';
    });
  }

  /* Cursor */
  var cur = $('.cur'), ring = cur && $('.cur-ring', cur), dot = cur && $('.cur-dot', cur), label = ring && $('em', ring), rx = 0, ry = 0;
  if(cur && fine && !rm){
    doc.classList.add('has-cur');
    document.addEventListener('mouseover', function(e){
      var a = e.target.closest('a,button,[data-cur],.acc-i');
      cur.classList.toggle('hover', !!a);
      label.textContent = a ? (a.getAttribute('data-cur') || '') : '';
    });
  }
  function updateCursor(){
    if(!cur || !fine || rm) return;
    rx = lerp(rx, mouse.x, 0.18); ry = lerp(ry, mouse.y, 0.18);
    dot.style.transform = 'translate(' + mouse.x + 'px,' + mouse.y + 'px)';
    ring.style.transform = 'translate(' + rx.toFixed(1) + 'px,' + ry.toFixed(1) + 'px)';
  }

  /* ---------- Haupt-Loop ---------- */
  var heroEl = $('.s-hero');
  function frame(t){
    if(canvas && heroVisible && !rm && P.length){
      var disperse = clamp(scrollY / (heroEl.offsetHeight*0.75), 0, 1);
      drawField(t, ease(disperse), false);
    }
    updateMarq(); updateChaos(t); updateWipes(); updateChan(); updatePhone(); updateHeroType(); updateFin(t); updateMag(); updateCursor();
    requestAnimationFrame(frame);
  }
  function measureAll(){ fitHero(); measureChaos(); measureChan(); measureMarq(); }
  var rsT; window.addEventListener('resize', function(){ clearTimeout(rsT); rsT = setTimeout(function(){ measureAll(); buildField(); }, 150); });
  if(document.fonts && document.fonts.ready){ document.fonts.ready.then(measureAll); }
  measureAll();
  requestAnimationFrame(frame);

  /* ---------- Einmal-Trigger ---------- */
  var term = $('[data-term]');
  if(term){
    var lines = $$('.tl', term);
    if(rm){ lines.forEach(function(l){ l.classList.add('on'); }); }
    else {
      var tob = new IntersectionObserver(function(en){
        if(!en[0].isIntersecting) return; tob.disconnect();
        var d = 0; lines.forEach(function(l){ setTimeout(function(){ l.classList.add('on'); }, d); d += l.classList.contains('prop') ? 520 : 300; });
      }, {threshold:.35});
      tob.observe(term);
    }
  }
  var stamps = $$('.stamp');
  if(stamps.length){
    if(rm){ stamps.forEach(function(s){ s.classList.add('on'); }); }
    else {
      var stob = new IntersectionObserver(function(en){
        if(!en[0].isIntersecting) return; stob.disconnect();
        stamps.forEach(function(s, i){ setTimeout(function(){ s.classList.add('on'); }, 160 + i*220); });
      }, {threshold:.4});
      stob.observe(stamps[0].parentNode);
    }
  }

  /* Akkordeon */
  var accs = $$('.acc-i');
  accs.forEach(function(a){
    var open = function(){ accs.forEach(function(o){ o.classList.toggle('on', o === a); }); };
    a.addEventListener('mouseenter', function(){ if(fine) open(); });
    a.addEventListener('focus', open); a.addEventListener('click', open);
  });

  /* Index-Vorschau folgt dem Cursor */
  var fl = $('.idx-float'), flt = fl && $('span', fl);
  if(fl && fine){
    $$('.idx a').forEach(function(a){
      a.addEventListener('mouseenter', function(){ flt.textContent = a.getAttribute('data-prev'); fl.classList.add('on'); });
      a.addEventListener('mouseleave', function(){ fl.classList.remove('on'); });
    });
    window.addEventListener('mousemove', function(){ fl.style.left = mouse.x + 'px'; fl.style.top = mouse.y + 'px'; }, {passive:true});
  }
})();
