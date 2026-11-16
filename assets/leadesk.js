/* ===== Leadesk Marketing — Shared Interactions ===== */
(function(){
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var hdr = document.getElementById('hdr');
  if(hdr){ window.addEventListener('scroll', function(){ hdr.classList.toggle('scrolled', window.scrollY > 30); }, {passive:true}); }

  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
  }, {threshold:0.15, rootMargin:'0px 0px -50px 0px'});
  document.querySelectorAll('.reveal').forEach(function(el){ if(rm){el.classList.add('in');} else {io.observe(el);} });

  function countUp(el){
    var to = parseFloat(el.getAttribute('data-to')), dur=1100, t0=null;
    var dec = (to % 1 !== 0) ? 1 : 0;
    if(rm){ el.textContent = to.toFixed(dec); return; }
    function step(ts){ if(!t0)t0=ts; var p=Math.min((ts-t0)/dur,1); var eased=1-Math.pow(1-p,3);
      el.textContent = (to*eased).toFixed(dec); if(p<1) requestAnimationFrame(step); else el.textContent=to.toFixed(dec); }
    requestAnimationFrame(step);
  }
  var cio = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ countUp(e.target); cio.unobserve(e.target);} });
  }, {threshold:0.6});
  document.querySelectorAll('.count').forEach(function(el){ cio.observe(el); });

  // Tool-Konsolidierung (nur Startseite)
  var stage = document.getElementById('toolstage');
  if(stage){
    var sio = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting && !rm){ setTimeout(function(){stage.classList.add('converged');},400); sio.unobserve(e.target);} });
    }, {threshold:0.4});
    sio.observe(stage);
  }

  // Typewriter (data-typewriter Attribut, \n als Zeilenumbruch)
  function typewriter(el, text, speed){
    if(rm){ el.textContent = text; return; }
    el.classList.add('typing-cursor');
    var i=0; (function tick(){ el.textContent = text.slice(0,i); i++;
      if(i<=text.length){ setTimeout(tick, speed); } else { el.classList.remove('typing-cursor'); } })();
  }
  document.querySelectorAll('[data-typewriter]').forEach(function(el){
    var txt = el.getAttribute('data-typewriter'), sp = parseInt(el.getAttribute('data-speed')||'22',10), once=false;
    var tio = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting && !once){ once=true; typewriter(el, txt, sp); tio.unobserve(e.target);} });
    }, {threshold:0.5});
    tio.observe(el);
  });
  // Conversion-Events (Vercel Web Analytics). window.va ist auf jeder Seite als
  // Stub definiert; Fehler im Tracking duerfen die Seite nie stoeren.
  // Je Event hoechstens 2 Felder (Grenze im Vercel-Pro-Plan).
  function track(name, data){
    try{ if(typeof window.va === 'function'){ window.va('event', data ? {name:name, data:data} : {name:name}); } }catch(e){}
  }
  window.lkTrack = track;

  var REGISTER = 'https://app.leadesk.de/register';
  var PAGE = location.pathname;

  // Stelle des Links auf der Seite; Hero und CTA-Band teilen sich .hero-cta,
  // daher zaehlt das umgebende Element.
  function linkPlace(a){
    if(a.closest('#navOverlay')) return 'overlay';
    if(a.closest('header')) return 'header';
    if(a.closest('footer')) return 'footer';
    if(a.closest('.cta-band')) return 'cta-band';
    if(a.closest('.plan')) return 'pricing';
    if(a.closest('.ci-hero, .page-hero, .hero')) return 'hero';
    return 'inline';
  }

  // Herkunft am Register-Link: die App uebernimmt sie bei der Registrierung.
  // Nur aus der aktuellen Adresse und dem Referrer, ohne Cookie und ohne Speicher;
  // UTM-Werte und fremder Referrer gelten daher nur auf der Einstiegsseite.
  try{
    var here = new URLSearchParams(location.search);
    var herkunft = [['src', 'web'], ['lp', PAGE]];
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function(k){
      var v = here.get(k); if(v) herkunft.push([k, v.slice(0, 100)]);
    });
    var refHost = document.referrer ? new URL(document.referrer).hostname : '';
    if(refHost && !/(^|\.)leadesk\.de$/.test(refHost)) herkunft.push(['ref_host', refHost]);
    document.querySelectorAll('a[href^="' + REGISTER + '"]').forEach(function(a){
      try{
        var u = new URL(a.getAttribute('href'));
        herkunft.forEach(function(p){ if(!u.searchParams.has(p[0])) u.searchParams.set(p[0], p[1]); });
        u.searchParams.set('cta', linkPlace(a));
        a.setAttribute('href', u.toString());
      }catch(e){}
    });
  }catch(e){}

  document.addEventListener('click', function(e){
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if(!a) return;
    var href = a.getAttribute('href') || '';
    if(href.indexOf(REGISTER) === 0){
      var m = href.match(/[?&]plan=([a-z-]+)/);
      track('register_click', {page: PAGE, plan: m ? m[1] : 'none'});
    } else if(href.indexOf('https://app.leadesk.de/login') === 0){
      track('login_click', {page: PAGE});
    } else if(href.indexOf('https://apps.apple.com/') === 0){
      track('appstore_click', {page: PAGE});
    }
  });
})();
