#!/usr/bin/env python3
"""Build all Leadesk marketing site subpages with a shared nav/footer."""

import os, re
from textwrap import dedent

OUT = os.path.dirname(os.path.abspath(__file__))

# ─── SHARED NAV + FOOTER ──────────────────────────────────────────────────────

APP_URL = "https://app.leadesk.de"

def nav(active=None):
    items = [
        ('funktionen', 'Funktionen', 'features.html'),
        ('ki',         'KI',         'ki.html'),
        ('preise',     'Preise',     'pricing.html'),
    ]
    links = ''.join(
        f'<a href="{href}"{" class=\"active\"" if active == key else ""}>{label}</a>\n        '
        for key, label, href in items
    )
    return dedent(f"""\
    <nav class="nav">
      <div class="nav__inner">
        <a href="index.html" class="brand" aria-label="Leadesk"><img src="leadesk-logo.png" alt="Leadesk" /></a>
        <div class="nav__links">
          {links.strip()}
        </div>
        <div class="nav__cta">
          <a href="{APP_URL}/login" class="nav__login">Anmelden</a>
          <a href="{APP_URL}/register" class="btn btn--primary btn--sm">Kostenlos starten</a>
        </div>
      </div>
    </nav>
    """)

FOOTER = dedent(f"""\
<footer class="footer">
    <div class="footer__inner">
      <div class="footer__grid">
        <div class="footer__brand-col">
          <div class="brand brand--footer"><img src="leadesk-logo-white.png" alt="Leadesk" /></div>
          <div class="footer__tagline">Die LinkedIn-Suite für B2B-Teams. Marke, Outreach und CRM in einem Tool.</div>
          <div class="footer__trust">
            <span class="footer__trust-badge">🇩🇪 DSGVO</span>
            <span class="footer__trust-badge">🔒 ISO 27001</span>
            <span class="footer__trust-badge">⚡ 99,9% Uptime</span>
          </div>
        </div>
        <div><div class="footer__col-title">Produkt</div><ul class="footer__links"><li><a href="features.html">Funktionen</a></li><li><a href="pricing.html">Preise</a></li><li><a href="chrome-extension.html">Chrome-Extension</a></li><li><a href="integrationen.html">Integrationen</a></li><li><a href="changelog.html">Changelog</a></li></ul></div>
        <div><div class="footer__col-title">Hilfe</div><ul class="footer__links"><li><a href="support.html">Support</a></li></ul></div>
        <div><div class="footer__col-title">Unternehmen</div><ul class="footer__links"><li><a href="ueber-uns.html">Über uns</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
        <div><div class="footer__col-title">Rechtliches</div><ul class="footer__links"><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li><li><a href="agb.html">AGB</a></li><li><a href="av-vertrag.html">AV-Vertrag</a></li></ul></div>
      </div>
      <div class="footer__bottom">
        <div>© 2026 Leadesk. Alle Rechte vorbehalten.</div>
        <div class="footer__legal">
          <a href="impressum.html">Impressum</a>
          <a href="datenschutz.html">Datenschutz</a>
          <a href="agb.html">AGB</a>
        </div>
      </div>
    </div>
  </footer>""")

def page(title, description, body, active=None, scripts="", filename=""):
    slug = filename[:-5] if filename.endswith('.html') else filename
    url = f"https://www.leadesk.de/{slug}" if slug else "https://www.leadesk.de/"
    og_image = "https://www.leadesk.de/screenshot-dashboard.png"
    return dedent(f"""\
    <!DOCTYPE html>
    <html lang="de">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{title}</title>
      <meta name="description" content="{description}">
      <link rel="canonical" href="{url}">
      <link rel="icon" type="image/png" href="/Leadesk_Favicon.png">
      <!-- Open Graph -->
      <meta property="og:type" content="website">
      <meta property="og:url" content="{url}">
      <meta property="og:title" content="{title}">
      <meta property="og:description" content="{description}">
      <meta property="og:image" content="{og_image}">
      <meta property="og:locale" content="de_DE">
      <meta property="og:site_name" content="Leadesk">
      <!-- Twitter Card -->
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="{title}">
      <meta name="twitter:description" content="{description}">
      <meta name="twitter:image" content="{og_image}">
      <link rel="stylesheet" href="styles.css">
    </head>
    <body>

    {nav(active).strip()}

    {body.strip()}

    {FOOTER.strip()}
    {scripts}
      <script>
        const io = new IntersectionObserver((entries) => {{
          entries.forEach(entry => {{
            if (entry.isIntersecting) {{
              entry.target.classList.add('is-visible');
              io.unobserve(entry.target);
            }}
          }});
        }}, {{ threshold: 0.12, rootMargin: '0px 0px -30px 0px' }});
        document.querySelectorAll('.reveal').forEach(el => io.observe(el));

        document.querySelectorAll('.faq__q').forEach(btn => {{
          btn.addEventListener('click', () => btn.parentElement.classList.toggle('open'));
        }});
      </script>
    </body>
    </html>
    """)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def hero(eyebrow, title_html, sub, max_title_ch=20):
    return dedent(f"""\
    <section class="hero" style="padding-bottom: 40px;">
      <div class="container">
        <div class="hero__eyebrow reveal">{eyebrow}</div>
        <h1 class="h1-hero hero__title reveal" style="max-width: {max_title_ch}ch;">{title_html}</h1>
        <p class="sub hero__sub reveal">{sub}</p>
      </div>
    </section>
    """)

def footer_cta(title_html="Mehr Pipeline.<br>Weniger Stress.", sub="7 Tage kostenlos testen. Keine Kreditkarte, keine Verlängerungsfalle.", cta_label="Kostenlos starten"):
    return dedent(f"""\
    <section class="footer-cta">
      <div class="container footer-cta__inner">
        <h2 class="footer-cta__title reveal">{title_html}</h2>
        <p class="footer-cta__sub reveal">{sub}</p>
        <div class="reveal">
          <a href="{APP_URL}/register" class="btn btn--on-blue btn--lg">
            <svg class="btn__rocket" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/></svg>
            {cta_label}
          </a>
        </div>
      </div>
    </section>
    """)

def coming_soon_hero(eyebrow, title, sub, email_label="Informier mich, wenn's so weit ist"):
    return dedent(f"""\
    <section class="hero" style="padding: 100px 0 80px;">
      <div class="container">
        <div class="hero__eyebrow reveal" style="background: var(--warm-soft); border-color: var(--warm);">⏳ Bald verfügbar</div>
        <h1 class="h1-hero hero__title reveal" style="max-width: 18ch;">{title}</h1>
        <p class="sub hero__sub reveal">{sub}</p>
        <div class="hero__ctas reveal">
          <a href="kontakt.html" class="btn btn--primary btn--lg">{email_label}</a>
          <a href="index.html" class="link-arrow">Zurück zur Startseite</a>
        </div>
      </div>
    </section>
    """)

def simple_section(eyebrow, title, sub=None, body=""):
    sub_html = f'<p class="sub section__sub">{sub}</p>' if sub else ''
    return dedent(f"""\
    <section class="section">
      <div class="container">
        <div class="section__head reveal">
          <div class="section__eyebrow-wrap"><span class="eyebrow">{eyebrow}</span></div>
          <h2 class="h2-section">{title}</h2>
          {sub_html}
        </div>
        {body}
      </div>
    </section>
    """)

def legal_prose(heading, intro, sections):
    """sections: list of (title, html_body)"""
    blocks = []
    for title, body in sections:
        blocks.append(f"<h2>{title}</h2>\n{body}")
    blocks_html = "\n\n".join(blocks)
    return dedent(f"""\
    <section class="legal-hero">
      <div class="container">
        <div class="legal-hero__eyebrow"><span class="eyebrow">Rechtliches</span></div>
        <h1 class="legal-hero__title">{heading}</h1>
        <p class="legal-hero__sub">{intro}</p>
      </div>
    </section>

    <section class="legal-content">
      <div class="container">
        <div class="legal-prose">
          {blocks_html}
          <p class="legal-prose__meta">Stand: <mark class="todo">[Monat Jahr, z.B. April 2026]</mark></p>
        </div>
      </div>
    </section>
    """)

# ─── KI.HTML ──────────────────────────────────────────────────────────────────

ki_body = hero(
    "KI-Funktionen",
    'KI, die <span class="highlight">versteht</span>,<br>wie Vertrieb funktioniert.',
    "Acht trainierte Funktionen, ein Assistent — alle auf deine Markenstimme und Zielgruppen abgestimmt.",
    20
) + dedent("""\
<section class="section section--cream">
  <div class="container container--wide">
    <div class="ai-grid">
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg></div></div>
        <div class="ai-card__title">Post-Generator</div>
        <div class="ai-card__desc">Hook, Body und CTA in unter 30 Sekunden. Im Ton deiner Markenstimme, mit deinen Zielgruppen im Kopf.</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div></div>
        <div class="ai-card__title">Nachrichten-Assistent</div>
        <div class="ai-card__desc">Personalisierte DMs, die nicht nach Copy-Paste aussehen. Pro Lead einzigartig, in deinem Ton.</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/></svg></div></div>
        <div class="ai-card__title">Kommentar-Responder</div>
        <div class="ai-card__desc">Auf fremde Posts sichtbar werden — ohne Phrasen, ohne Generisches. Mit echter Meinung.</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div></div>
        <div class="ai-card__title">Lead-Scoring</div>
        <div class="ai-card__desc">Welche Leads lohnen sich jetzt? Datenbasiertes Scoring: Signal, Verhalten, Firmografika.</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg></div></div>
        <div class="ai-card__title">Pipeline-Insights</div>
        <div class="ai-card__desc">Wo bleibt Umsatz liegen? Wo drohen Verluste? Konkrete Empfehlungen pro Stage.</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div></div>
        <div class="ai-card__title">SSI-Empfehlungen</div>
        <div class="ai-card__desc">Konkrete Aktionen, die deinen Social Selling Index heben — nicht das übliche "poste regelmäßig".</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div></div>
        <div class="ai-card__title">Themen-Recherche</div>
        <div class="ai-card__desc">Trending-Themen in deiner Nische. Plus: welche Hooks in deinem Markt gerade funktionieren.</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div></div>
        <div class="ai-card__title">E-Mail-Sequenzen</div>
        <div class="ai-card__desc">Follow-ups per E-Mail, sobald der LinkedIn-Kanal ausgereizt ist. Multi-Channel, ein Ton.</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section__head reveal">
      <div class="section__eyebrow-wrap"><span class="eyebrow">Wie es funktioniert</span></div>
      <h2 class="h2-section">Deine Daten.<br>Deine Stimme.</h2>
      <p class="sub section__sub">Keine generische KI. Leadesk wird auf deine Marke trainiert — und bleibt privat.</p>
    </div>
    <div class="trust-grid reveal">
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8"/></svg></div>
        <div class="trust-card__title">Markenstimme</div>
        <div class="trust-card__desc">Beschreib deine Marke in natürlicher Sprache. Die KI wendet dein Profil auf jeden Text an.</div>
      </div>
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/></svg></div>
        <div class="trust-card__title">Zielgruppen</div>
        <div class="trust-card__desc">Pains, Gains, Trigger-Momente. Die KI weiß, wem sie schreibt — und warum.</div>
      </div>
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
        <div class="trust-card__title">Wissensdatenbank</div>
        <div class="trust-card__desc">Deine Case Studies, deine Blog-Artikel, deine Frameworks. Die KI referenziert — nicht erfindet.</div>
      </div>
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
        <div class="trust-card__title">Privat & DSGVO</div>
        <div class="trust-card__desc">Deine Daten trainieren kein öffentliches Modell. EU-Hosting, ISO-zertifiziert.</div>
      </div>
    </div>
  </div>
</section>
""") + footer_cta()

# ─── KUNDEN.HTML (Coming Soon weil fake Testimonials problematisch) ────────────

kunden_body = coming_soon_hero(
    "Bald verfügbar",
    "Kundenstimmen folgen in Kürze.",
    "Wir sammeln gerade echte Case Studies von unseren B2B-Teams. Wenn du zu den ersten gehören willst, die sehen was Leadesk für andere geleistet hat — trag dich ein.",
) + dedent("""\
<section class="section section--cream">
  <div class="container">
    <div class="section__head reveal">
      <div class="section__eyebrow-wrap"><span class="eyebrow">Bereits an Bord</span></div>
      <h2 class="h2-section">Teams, die Leadesk nutzen.</h2>
      <p class="sub section__sub">Case Studies, SSI-Historien und Pipeline-Ergebnisse veröffentlichen wir, sobald sie reif sind — nichts erfunden.</p>
    </div>
    <div class="logos__track-wrap">
      <div class="logos__track" style="animation: none; justify-content: center;">
        <span class="logo-placeholder"><span class="logo-placeholder__icon">A</span>Axentric</span>
        <span class="logo-placeholder logo-placeholder--alt"><span class="logo-placeholder__icon">N</span>Norvo</span>
        <span class="logo-placeholder"><span class="logo-placeholder__icon">K</span>Kronex</span>
        <span class="logo-placeholder logo-placeholder--warm"><span class="logo-placeholder__icon">B</span>Brevoria</span>
        <span class="logo-placeholder"><span class="logo-placeholder__icon">L</span>Luminax</span>
      </div>
    </div>
  </div>
</section>
""") + footer_cta(
    title_html="Selbst ein Case Study werden.",
    sub="Die ersten 50 Kunden, die eine Case Study erlauben, bekommen 6 Monate Professional-Plan kostenlos.",
    cta_label="Kostenlos starten"
)

# ─── CHROME-EXTENSION.HTML ────────────────────────────────────────────────────

chrome_body = hero(
    "Chrome-Erweiterung",
    'Ein Klick.<br>LinkedIn wird zur <span class="highlight">Datenquelle</span>.',
    "Die Leadesk-Extension importiert Profile, liest SSI-Scores und steuert Vernetzungen — direkt aus LinkedIn in deine Pipeline.",
    18
) + dedent("""\
<section class="feature-block section--blue-tint">
  <div class="container container--wide">
    <div class="feature-block__grid">
      <div class="feature-block__content">
        <div class="chapter__eyebrow-wrap reveal"><span class="eyebrow">Was sie kann</span></div>
        <h2 class="feature-block__title reveal">Profile werden zu Leads.<br>In einer Sekunde.</h2>
        <p class="feature-block__sub reveal">Besuche ein LinkedIn-Profil, klicke das Leadesk-Icon — Name, Firma, Headline, Location und SSI werden automatisch als Lead angelegt. Kein Copy-Paste, keine doppelte Pflege.</p>
        <ul class="feature-list reveal">
          <li><span class="feature-list__check">✓</span>Profile mit einem Klick als Lead importieren</li>
          <li><span class="feature-list__check">✓</span>SSI-Score automatisch gelesen und getrackt</li>
          <li><span class="feature-list__check">✓</span>Vernetzungen mit KI-Notiz direkt aus LinkedIn starten</li>
          <li><span class="feature-list__check">✓</span>Sicher, MV3-konform, ohne Session-Hacks</li>
          <li><span class="feature-list__check">✓</span>Pausiert automatisch bei LinkedIn-Grenzen</li>
        </ul>
      </div>
      <div class="feature-block__visual reveal">
        <div class="screenshot">
          <div class="screenshot__chrome"><span class="screenshot__dot"></span><span class="screenshot__dot"></span><span class="screenshot__dot"></span><span class="screenshot__url">linkedin.com/in/...</span></div>
          <div class="screenshot__body"><div class="screenshot__placeholder"><div class="screenshot__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 7h.01M11 7h.01M15 7h.01"/></svg></div><div class="screenshot__label">Chrome-Extension</div><div class="screenshot__hint">Screenshot folgt</div></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section__head reveal">
      <div class="section__eyebrow-wrap"><span class="eyebrow">Sicherheit zuerst</span></div>
      <h2 class="h2-section">MV3-konform.<br>LinkedIn-safe.</h2>
      <p class="sub section__sub">Wir nutzen keine Session-Hacks, keine Selenium-Tricks. Die Extension arbeitet innerhalb der LinkedIn-UI und respektiert alle üblichen Limits.</p>
    </div>
    <div class="trust-grid reveal">
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
        <div class="trust-card__title">Chrome MV3</div>
        <div class="trust-card__desc">Moderner Manifest V3 Service Worker. Keine Background Pages, keine persistenten Scripts.</div>
      </div>
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
        <div class="trust-card__title">Menschliche Pausen</div>
        <div class="trust-card__desc">Randomisierte Delays zwischen Aktionen. Tägliche Limits. Pausiert bei Warnungen.</div>
      </div>
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
        <div class="trust-card__title">Keine Credentials</div>
        <div class="trust-card__desc">Wir sehen dein LinkedIn-Passwort nie. Die Extension arbeitet in deinem Browser-Kontext.</div>
      </div>
      <div class="trust-card">
        <div class="trust-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg></div>
        <div class="trust-card__title">Chrome Web Store</div>
        <div class="trust-card__desc">Offiziell gelistet, Code-Reviewed, automatische Updates.</div>
      </div>
    </div>
  </div>
</section>
""") + footer_cta(
    title_html="Extension installieren.<br>In 2 Minuten einsatzbereit.",
    sub="Aus dem Chrome Web Store. Kostenlos mit jedem Leadesk-Plan.",
    cta_label="Zum Chrome Web Store"
)

# ─── INTEGRATIONEN.HTML ───────────────────────────────────────────────────────

def integration_card(letter, color, name, desc, cat):
    return f'''<div class="integration" style="padding: 20px; flex-direction: column; align-items: flex-start; gap: 14px;">
      <div class="integration__logo" style="background:{color}; width: 48px; height: 48px; font-size: 16px;">{letter}</div>
      <div>
        <div class="integration__name" style="font-size: 16px;">{name}</div>
        <div class="integration__cat" style="font-size: 12px; margin-top: 4px;">{cat}</div>
        <div style="font-size: 13px; color: var(--ink-muted); line-height: 1.5; margin-top: 8px;">{desc}</div>
      </div>
    </div>'''

integrations_list = [
    ("in", "#0A66C2", "LinkedIn",  "Kernintegration", "Profile, Nachrichten, Vernetzungen, SSI — direkt aus deinem Browser ins CRM."),
    ("M",  "#EA4335", "Gmail",     "E-Mail", "Gmail-Threads pro Lead verknüpft. Follow-ups aus Leadesk versenden."),
    ("O",  "#0078D4", "Outlook",   "E-Mail", "Microsoft 365 Anbindung für E-Mail-Workflows."),
    ("#",  "#4A154B", "Slack",     "Team-Chat", "Benachrichtigungen bei Hot Leads, Antworten, Deal-Updates — direkt in Slack."),
    ("H",  "#FF7A59", "HubSpot",   "CRM-Sync", "Bidirektionaler Lead- und Deal-Sync mit HubSpot."),
    ("P",  "#1A1A1A", "Pipedrive", "CRM-Sync", "Automatischer Sync deiner Pipedrive-Deals mit Leadesk."),
    ("Z",  "#FF4A00", "Zapier",    "Automation", "5.000+ Apps via Zapier anbinden — Trigger und Actions."),
    ("m",  "#6E4AF7", "Make",      "Automation", "Komplexe Workflows mit Make.com bauen."),
    ("n8", "#EA4B71", "n8n",       "Automation", "Self-hosted Automations für Datenschutz-bewusste Teams."),
    ("G",  "#4285F4", "Google Calendar", "Kalender", "Meetings direkt aus dem Lead anlegen — mit Kontext."),
    ("T",  "#5059C9", "MS Teams",  "Team-Chat", "Microsoft Teams-Channels für Lead-Updates."),
    ("{ }","#22C55E", "Webhooks",  "Developer", "Custom Webhooks für alle Events. REST API für deine Integrationen."),
]

integrations_body = hero(
    "Integrationen",
    'Passt zu deinem <span class="highlight">Stack</span>.',
    "Native Integrationen zu den wichtigsten Sales-, Marketing- und Automations-Tools.",
    18
) + dedent(f"""\
<section class="section section--cream">
  <div class="container container--wide">
    <div class="ai-grid" style="grid-template-columns: repeat(3, 1fr); max-width: 1080px;">
      {chr(10).join(integration_card(*x) for x in integrations_list)}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section__head reveal">
      <div class="section__eyebrow-wrap"><span class="eyebrow">Dein eigenes Tool dabei?</span></div>
      <h2 class="h2-section">Webhooks &amp; REST API.</h2>
      <p class="sub section__sub">Jedes Event in Leadesk kann per Webhook weitergereicht werden. Volle REST-API verfügbar ab dem Professional-Plan. <a href="dokumentation.html" class="link-arrow">Zur API-Dokumentation</a></p>
    </div>
  </div>
</section>
""") + footer_cta()

# ─── RESSOURCEN.HTML ──────────────────────────────────────────────────────────

ressourcen_body = hero(
    "Ressourcen",
    'Lernen, <span class="highlight">anwenden</span>,<br>wachsen.',
    "Blog-Artikel, Webinare, Templates und Dokumentation — alles um das Meiste aus Leadesk herauszuholen.",
    20
) + dedent("""\
<section class="section section--cream">
  <div class="container container--wide">
    <div class="ai-grid" style="grid-template-columns: repeat(2, 1fr); max-width: 900px;">
      <a href="blog.html" class="ai-card reveal" style="text-decoration: none; color: inherit;">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div></div>
        <div class="ai-card__title">Blog</div>
        <div class="ai-card__desc">LinkedIn-Vertrieb, SSI-Taktik, KI-Content. Neue Artikel jeden Dienstag.</div>
      </a>
      <a href="webinare.html" class="ai-card reveal" style="text-decoration: none; color: inherit;">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div></div>
        <div class="ai-card__title">Webinare</div>
        <div class="ai-card__desc">Monatlich live, danach on-demand. Deep Dives in die Produktfunktionen.</div>
      </a>
      <a href="templates.html" class="ai-card reveal" style="text-decoration: none; color: inherit;">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M3 9h18"/></svg></div></div>
        <div class="ai-card__title">Templates</div>
        <div class="ai-card__desc">Vorlagen für Outreach-Sequenzen, Content-Formate, Pipeline-Stages.</div>
      </a>
      <a href="dokumentation.html" class="ai-card reveal" style="text-decoration: none; color: inherit;">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></div></div>
        <div class="ai-card__title">Dokumentation</div>
        <div class="ai-card__desc">Feature-Guides, API-Referenz, Best Practices. Durchsuchbar.</div>
      </a>
    </div>
  </div>
</section>
""") + footer_cta()

# ─── UEBER-UNS.HTML ───────────────────────────────────────────────────────────

ueber_uns_body = hero(
    "Über uns",
    'LinkedIn-Vertrieb,<br><span class="highlight">ernstgenommen</span>.',
    "Leadesk wurde von zwei Gründern gebaut, die selbst wussten, wie nervig LinkedIn-Vertrieb ohne gutes Tool ist.",
    16
) + dedent(f"""\
<section class="section">
  <div class="container" style="max-width: 720px;">
    <div class="legal-prose">
      <h2>Warum Leadesk existiert</h2>
      <p>Die meisten LinkedIn-Tools machen eins gut — Outreach automatisieren, oder KI-Content generieren, oder Kontakte verwalten. Aber keines davon tut alles zusammen gut. Das Ergebnis: Fünf Tools nebeneinander, jede Pipeline in einer anderen Tabelle, jede Markenstimme manuell gepflegt.</p>
      <p>Wir haben Leadesk gebaut, weil wir genau diesen Schmerz selbst hatten. Als B2B-Team wollten wir CRM, Outreach, Content und KI <em>in einem Tool</em> — und zwar so, dass die Teile miteinander reden. Jetzt existiert dieses Tool.</p>

      <h2>Das Team</h2>
      <p><strong>Michael Schreck</strong> — Lead Developer. Baut die Plattform, kümmert sich um Architektur, Skalierung, Datenbank.</p>
      <p><strong>Julian Wolf</strong> — Co-Developer. Baut Features, Chrome-Extension, Integrationen, UX.</p>

      <h2>Die Firma</h2>
      <p>
        Leadesk GbR<br>
        Goldbacher Straße 100<br>
        63741 Aschaffenburg<br>
        Deutschland
      </p>
      <p>Kontakt: <a href="mailto:info@leadesk.de">info@leadesk.de</a> · <a href="tel:+4915563664275">0155 63664275</a></p>

      <h2>Prinzipien</h2>
      <ul>
        <li><strong>Eigene Daten bleiben deine.</strong> EU-Hosting, keine Weitergabe, jederzeit exportierbar.</li>
        <li><strong>Keine dunklen Patterns.</strong> Kündigung ist ein Klick. Keine Verlängerungsfalle.</li>
        <li><strong>LinkedIn-konform.</strong> Wir respektieren LinkedIn-Limits. Dein Account bleibt sicher.</li>
        <li><strong>Deutsch zuerst.</strong> Interface, Support, Compliance — alles auf Deutsch. Englisch folgt.</li>
      </ul>
    </div>
  </div>
</section>
""") + footer_cta()

# ─── KONTAKT.HTML ─────────────────────────────────────────────────────────────

kontakt_body = hero(
    "Kontakt",
    'Sag <span class="highlight">hallo</span>.',
    "Wir antworten meistens innerhalb eines Arbeitstags.",
    18
) + dedent(f"""\
<section class="section">
  <div class="container" style="max-width: 780px;">
    <div class="ai-grid" style="grid-template-columns: 1fr 1fr; gap: 24px;">
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div></div>
        <div class="ai-card__title">E-Mail</div>
        <div class="ai-card__desc"><a href="mailto:info@leadesk.de" style="color: var(--primary); text-decoration: none;">info@leadesk.de</a><br>Antwort binnen 1 Arbeitstag.</div>
      </div>
      <div class="ai-card reveal">
        <div class="ai-card__thumb"><div class="ai-card__thumb-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div></div>
        <div class="ai-card__title">Telefon</div>
        <div class="ai-card__desc"><a href="tel:+4915563664275" style="color: var(--primary); text-decoration: none;">0155 63664275</a><br>Mo–Fr 9–17 Uhr (MEZ).</div>
      </div>
    </div>

    <div style="margin-top: 48px;" class="reveal">
      <h3 style="font-size: 22px; font-weight: 600; margin-bottom: 12px; letter-spacing: -0.015em;">Presse &amp; Medien</h3>
      <p style="color: var(--ink-muted); line-height: 1.55;">Für Presse-Anfragen, Interviews und Logos: <a href="mailto:presse@leadesk.de" style="color: var(--primary);">presse@leadesk.de</a></p>
    </div>

    <div style="margin-top: 32px;" class="reveal">
      <h3 style="font-size: 22px; font-weight: 600; margin-bottom: 12px; letter-spacing: -0.015em;">Datenschutz &amp; Sicherheit</h3>
      <p style="color: var(--ink-muted); line-height: 1.55;">Fragen zu Datenverarbeitung, AV-Verträgen oder Sicherheit: <a href="mailto:datenschutz@leadesk.de" style="color: var(--primary);">datenschutz@leadesk.de</a></p>
    </div>

    <div style="margin-top: 32px;" class="reveal">
      <h3 style="font-size: 22px; font-weight: 600; margin-bottom: 12px; letter-spacing: -0.015em;">Postanschrift</h3>
      <p style="color: var(--ink-muted); line-height: 1.55;">
        Leadesk GbR<br>
        Goldbacher Straße 100<br>
        63741 Aschaffenburg<br>
        Deutschland
      </p>
    </div>
  </div>
</section>
""") + footer_cta()

# ─── COMING SOON TEMPLATES ────────────────────────────────────────────────────

def coming_soon(eyebrow, title, sub):
    return coming_soon_hero(eyebrow, title, sub) + footer_cta()

blog_body = coming_soon(
    "Blog",
    "Der Leadesk-Blog startet bald.",
    "Artikel über LinkedIn-Vertrieb, SSI-Taktik, KI-Content und B2B-Wachstum. Ab Mai 2026, jeden Dienstag ein neuer Artikel."
)

webinare_body = coming_soon(
    "Webinare",
    "Live-Webinare starten im Mai.",
    "Monatlich live: Deep Dives in Features, Best Practices von Kunden, Q&A mit dem Team. Danach dauerhaft on-demand verfügbar."
)

templates_body = coming_soon(
    "Templates",
    "Template-Bibliothek in Arbeit.",
    "Fertige Outreach-Sequenzen, Post-Formate, Pipeline-Setups — kostenlos für alle Kunden. Launch in Q3 2026."
)

karriere_body = coming_soon(
    "Karriere",
    "Wir wachsen — bald stellen wir ein.",
    "Aktuell sind wir ein Gründer-Duo und bauen mit voller Kraft die Plattform. Ab Sommer 2026 suchen wir Senior Full-Stack-Engineers, Designer und Customer Success. Schick uns gerne jetzt schon deine Bewerbung."
)

partner_body = coming_soon(
    "Partner",
    "Partnerprogramm startet in Kürze.",
    "Für Agenturen, die mehrere Kunden-Marken auf Leadesk betreuen — Whitelabel, Revenue Share, gemeinsame Go-to-Market. Infos ab Q3 2026."
)

changelog_body = coming_soon(
    "Changelog",
    "Was neu ist — in Kürze auch öffentlich.",
    "Detaillierte Release Notes aller Versionen. Bis dahin: Features und Fixes findest du direkt in der App unter Admin &rarr; Changelog &amp; Logs."
)

dokumentation_body = coming_soon(
    "Dokumentation",
    "Öffentliche Dokumentation folgt.",
    "Feature-Guides, API-Referenz, Best Practices. Bis dahin: In-App-Hilfe in der Seitenleiste deines Leadesk-Accounts."
)

support_body = coming_soon(
    "Support",
    "Support, wenn du ihn brauchst.",
    "Schick uns eine E-Mail an info@leadesk.de — wir antworten innerhalb eines Arbeitstags. Für Enterprise-Kunden: dedicated Success Manager im Business-Plan inklusive."
)

# ─── LEGAL: AGB ───────────────────────────────────────────────────────────────

agb_sections = [
    ("§ 1 Geltungsbereich", """\
<p>Diese Allgemeinen Geschäftsbedingungen (AGB) gelten für alle Verträge zwischen der Leadesk GbR (nachfolgend „Anbieter") und ihren Kunden (nachfolgend „Nutzer") über die Nutzung der Leadesk-Plattform (app.leadesk.de, inkl. Chrome-Erweiterung).</p>
<p>Abweichende Bedingungen des Nutzers werden nicht anerkannt, es sei denn, der Anbieter stimmt ihrer Geltung ausdrücklich schriftlich zu.</p>"""),

    ("§ 2 Vertragsschluss", """\
<p>Der Nutzer kann sich über die Website registrieren und einen Leadesk-Plan (Starter, Professional, Business) abschließen. Mit der Bestätigung der Plan-Auswahl und Eingabe der Zahlungsdaten kommt der Vertrag zustande.</p>
<p>Die Anbieter-Eingaben in der Plan-Auswahl stellen kein rechtlich bindendes Angebot dar, sondern eine Aufforderung zur Angebotsabgabe (invitatio ad offerendum).</p>"""),

    ("§ 3 Leistungsumfang", """\
<p>Der Anbieter stellt dem Nutzer die Leadesk-Plattform als Software-as-a-Service zur Verfügung. Der konkrete Funktionsumfang richtet sich nach dem gewählten Plan, wie auf der Preise-Seite dargestellt.</p>
<p>Der Anbieter behält sich vor, die Plattform weiterzuentwickeln, zu erweitern oder einzelne Funktionen anzupassen. Wesentliche Änderungen werden mindestens 14 Tage vorher angekündigt.</p>"""),

    ("§ 4 Vergütung und Zahlungsbedingungen", """\
<p>Die Vergütung richtet sich nach dem gewählten Plan. Alle Preise sind Nettopreise zuzüglich der gesetzlichen Mehrwertsteuer.</p>
<p>Die Abrechnung erfolgt monatlich oder jährlich im Voraus. Der Nutzer kann per Kreditkarte oder SEPA-Lastschrift zahlen. Ab dem Business-Plan ist auf Anfrage Rechnungszahlung möglich.</p>
<p>Bei Zahlungsverzug kann der Anbieter den Zugang zur Plattform nach vorheriger Mahnung einschränken oder sperren.</p>"""),

    ("§ 5 Laufzeit und Kündigung", """\
<p>Der Vertrag läuft auf unbestimmte Zeit. Monatliche Abos sind zum Monatsende kündbar, Jahresabos zum Ende der Jahreslaufzeit.</p>
<p>Die Kündigung erfolgt direkt in den Einstellungen des Leadesk-Accounts oder per E-Mail an <a href="mailto:info@leadesk.de">info@leadesk.de</a>.</p>
<p>Das Recht zur außerordentlichen Kündigung aus wichtigem Grund bleibt unberührt.</p>"""),

    ("§ 6 Pflichten des Nutzers", """\
<p>Der Nutzer verpflichtet sich, die Plattform nur im Rahmen der gesetzlichen Bestimmungen und der LinkedIn-Nutzungsbedingungen zu verwenden.</p>
<p>Insbesondere ist untersagt:</p>
<ul>
  <li>Spam-Nachrichten oder massenhafte, unpersönliche Nachrichten zu versenden</li>
  <li>Die Plattform zum Stalking, Harassment oder zur unerlaubten Datensammlung zu nutzen</li>
  <li>LinkedIn-Limits künstlich zu umgehen oder mehrere Accounts zur Umgehung von Limits einzusetzen</li>
  <li>Den Dienst an Dritte ohne schriftliche Zustimmung weiterzugeben (außer im Rahmen von Team-Lizenzen)</li>
</ul>
<p>Bei Verstößen behält sich der Anbieter vor, den Account zu sperren und das Vertragsverhältnis außerordentlich zu beenden.</p>"""),

    ("§ 7 Haftung", """\
<p>Der Anbieter haftet uneingeschränkt für Vorsatz und grobe Fahrlässigkeit. Bei einfacher Fahrlässigkeit haftet der Anbieter nur bei Verletzung wesentlicher Vertragspflichten (Kardinalpflichten) und nur bis zur Höhe des vertragstypischen, vorhersehbaren Schadens.</p>
<p>Die Haftung für LinkedIn-Account-Sperren ist ausgeschlossen, sofern die Sperre nicht auf vorsätzliches oder grob fahrlässiges Verhalten des Anbieters zurückzuführen ist. Der Anbieter weist ausdrücklich darauf hin, dass LinkedIn Accounts bei regelwidrigem Verhalten sperren kann — auch bei automatisierter Nutzung, die innerhalb der bekannten Limits bleibt.</p>
<p>Die Haftung nach dem Produkthaftungsgesetz bleibt unberührt.</p>"""),

    ("§ 8 Datenschutz und Verfügbarkeit", """\
<p>Die Verarbeitung personenbezogener Daten ist in der <a href="datenschutz.html">Datenschutzerklärung</a> geregelt. Ein Auftragsverarbeitungsvertrag (AV-Vertrag) nach Art. 28 DSGVO steht unter <a href="av-vertrag.html">av-vertrag.html</a> bereit.</p>
<p>Der Anbieter strebt eine Verfügbarkeit von 99,5 % im Jahresmittel an. Geplante Wartungsarbeiten werden vorher angekündigt.</p>"""),

    ("§ 9 Änderungen der AGB", """\
<p>Der Anbieter kann diese AGB anpassen, soweit dies aus berechtigten Gründen (z.B. Änderung der Rechtslage, neue Produktfunktionen) erforderlich ist. Die Änderungen werden dem Nutzer mindestens 6 Wochen vor Inkrafttreten per E-Mail mitgeteilt.</p>
<p>Widerspricht der Nutzer den Änderungen nicht innerhalb von 4 Wochen nach Zugang der Mitteilung, gelten diese als akzeptiert. Auf diese Wirkung wird in der Änderungsmitteilung hingewiesen.</p>"""),

    ("§ 10 Schlussbestimmungen", """\
<p>Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts. Bei Verträgen mit Unternehmern ist Gerichtsstand <mark class="todo">[Gerichtsstand, z.B. Aschaffenburg]</mark>.</p>
<p>Sollten einzelne Bestimmungen dieser AGB unwirksam sein oder werden, berührt dies die Wirksamkeit der übrigen Bestimmungen nicht.</p>"""),
]

agb_body = legal_prose(
    "Allgemeine Geschäftsbedingungen",
    "AGB für die Nutzung der Leadesk-Plattform und -Dienste.",
    agb_sections
)

# ─── LEGAL: AV-VERTRAG ────────────────────────────────────────────────────────

av_sections = [
    ("Was ist ein AV-Vertrag?", """\
<p>Wenn du Leadesk nutzt, verarbeiten wir in deinem Auftrag personenbezogene Daten — zum Beispiel Daten deiner LinkedIn-Leads, Kontakte und Empfänger deiner Nachrichten. Nach Art. 28 DSGVO musst du mit uns einen <strong>Auftragsverarbeitungsvertrag (AV-Vertrag)</strong> schließen, bevor wir diese Daten rechtmäßig verarbeiten dürfen.</p>
<p>Der AV-Vertrag regelt Art und Umfang der Datenverarbeitung, die Rechte und Pflichten beider Parteien, Sicherheitsmaßnahmen, Unterauftragsverarbeiter und die Dauer der Verarbeitung.</p>"""),

    ("Wie bekomme ich den AV-Vertrag?", """\
<p>Wir stellen dir den AV-Vertrag als PDF zum Herunterladen, Unterschreiben und Zurücksenden bereit. Sobald unterschrieben, senden wir eine gegengezeichnete Version zurück.</p>
<p><strong>Schreib uns eine E-Mail an <a href="mailto:datenschutz@leadesk.de">datenschutz@leadesk.de</a></strong> mit dem Betreff „AV-Vertrag" — wir schicken dir innerhalb eines Werktags:</p>
<ul>
  <li>Den aktuellen AV-Vertrag als PDF (deutsche &amp; englische Fassung)</li>
  <li>Unsere TOM-Liste (technische und organisatorische Maßnahmen) nach Art. 32 DSGVO</li>
  <li>Eine Liste der Unterauftragsverarbeiter (z.B. Hosting-Anbieter, E-Mail-Versand)</li>
</ul>"""),

    ("Für wen ist der AV-Vertrag relevant?", """\
<p>Grundsätzlich für <strong>alle Kunden, die mit personenbezogenen Daten Dritter arbeiten</strong> — also praktisch jeden B2B-Nutzer, der über Leadesk LinkedIn-Leads verwaltet oder Nachrichten an andere Personen sendet.</p>
<p>Einzelne Selbstnutzer, die ausschließlich ihre eigenen Daten verwalten, brauchen keinen AV-Vertrag — aber sobald du Leads, Kunden oder Kontakte verarbeitest, solltest du einen haben.</p>"""),

    ("Eckdaten des AV-Vertrags", """\
<p><strong>Auftragsverarbeiter:</strong> Leadesk GbR, Goldbacher Straße 100, 63741 Aschaffenburg, Deutschland</p>
<p><strong>Verantwortlicher:</strong> Der Kunde (du).</p>
<p><strong>Ort der Verarbeitung:</strong> EU (Frankfurt am Main, Supabase-Hosting). Keine Drittlandsübermittlungen außerhalb der EU/EWR ohne geeignete Garantien nach Art. 46 DSGVO.</p>
<p><strong>Dauer:</strong> Laufzeit des Hauptvertrags.</p>
<p><strong>Gegenstand:</strong> Bereitstellung der Leadesk-Plattform als SaaS, inkl. Speicherung, Verarbeitung und Übermittlung der durch den Kunden hochgeladenen oder erfassten Daten.</p>"""),

    ("Unterauftragsverarbeiter", """\
<p>Wir nutzen ausgewählte Dienstleister für die Bereitstellung der Plattform. Diese sind in einer Liste im AV-Vertrag benannt und werden regelmäßig aktualisiert. Wesentliche Kategorien:</p>
<ul>
  <li><strong>Hosting:</strong> Supabase / AWS Frankfurt (DSGVO-konform, ISO 27001)</li>
  <li><strong>Frontend-Hosting:</strong> Vercel (Preise-Seite, App-Auslieferung)</li>
  <li><strong>E-Mail-Versand (Transactional):</strong> <mark class="todo">[Anbieter einfügen, z.B. SendGrid/Postmark]</mark></li>
  <li><strong>KI-Dienste:</strong> <mark class="todo">[Anbieter, z.B. OpenAI/Anthropic — nur mit Standard Contractual Clauses]</mark></li>
</ul>
<p>Neue Unterauftragsverarbeiter werden mindestens 14 Tage vor Einsatz angekündigt, mit Widerspruchsrecht nach AV-Vertrag.</p>"""),
]

av_body = legal_prose(
    "AV-Vertrag (Auftragsverarbeitung)",
    "Auftragsverarbeitungsvertrag nach Art. 28 DSGVO — für alle B2B-Kunden, die Drittdaten verarbeiten.",
    av_sections
)

# ─── ALLE SEITEN SCHREIBEN ────────────────────────────────────────────────────

pages = {
    'ki.html':               ('KI-Funktionen — Leadesk',       'Die acht KI-Funktionen von Leadesk: Post-Generator, Nachrichten-Assistent, Kommentar-Responder, Lead-Scoring, Pipeline-Insights, SSI-Empfehlungen, Themen-Recherche, E-Mail-Sequenzen.', ki_body, 'ki'),
    'kunden.html':           ('Kunden — Leadesk',              'B2B-Teams, die mit Leadesk wachsen. Case Studies folgen.', kunden_body, 'kunden'),
    'chrome-extension.html': ('Chrome-Extension — Leadesk',    'Die Leadesk Chrome-Erweiterung: Profile importieren, SSI tracken, Vernetzungen direkt aus LinkedIn.', chrome_body, None),
    'integrationen.html':    ('Integrationen — Leadesk',       '12 native Integrationen: LinkedIn, Gmail, HubSpot, Slack, Pipedrive, Zapier, Make, n8n, Webhooks und mehr.', integrations_body, None),
    'ressourcen.html':       ('Ressourcen — Leadesk',          'Blog, Webinare, Templates und Dokumentation — alles um das Meiste aus Leadesk herauszuholen.', ressourcen_body, 'ressourcen'),
    'ueber-uns.html':        ('Über uns — Leadesk',            'Leadesk wird von Julian Wolf und Michael Schreck gebaut. Hier die Geschichte hinter dem Tool.', ueber_uns_body, None),
    'kontakt.html':          ('Kontakt — Leadesk',             'E-Mail, Telefon, Postanschrift. Antwort binnen 1 Arbeitstag.', kontakt_body, None),
    'blog.html':             ('Blog — Leadesk',                'Der Leadesk-Blog startet im Mai 2026.', blog_body, None),
    'webinare.html':         ('Webinare — Leadesk',            'Monatliche Live-Webinare zu LinkedIn-Vertrieb und KI-Content.', webinare_body, None),
    'templates.html':        ('Templates — Leadesk',           'Fertige Outreach-Sequenzen, Post-Formate und Pipeline-Setups.', templates_body, None),
    'karriere.html':         ('Karriere — Leadesk',            'Leadesk wächst. Ab Sommer 2026 suchen wir Verstärkung.', karriere_body, None),
    'partner.html':          ('Partner — Leadesk',             'Agentur-Partnerprogramm für Whitelabel-Kunden — startet Q3 2026.', partner_body, None),
    'changelog.html':        ('Changelog — Leadesk',           'Was neu ist in Leadesk — öffentliche Release Notes folgen.', changelog_body, None),
    'dokumentation.html':    ('Dokumentation — Leadesk',       'Feature-Guides, API-Referenz, Best Practices — öffentliche Docs folgen.', dokumentation_body, None),
    'support.html':          ('Support — Leadesk',             'Hilfe, wenn du sie brauchst. E-Mail, FAQ, dedicated Success Manager.', support_body, None),
    'agb.html':              ('AGB — Leadesk',                 'Allgemeine Geschäftsbedingungen für die Nutzung der Leadesk-Plattform.', agb_body, None),
    'av-vertrag.html':       ('AV-Vertrag — Leadesk',          'Auftragsverarbeitungsvertrag nach Art. 28 DSGVO — auf Anfrage.', av_body, None),
}

for filename, (title, desc, body, active) in pages.items():
    html = page(title, desc, body, active=active, filename=filename)
    with open(os.path.join(OUT, filename), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Wrote {filename} ({len(html):,} bytes)')

print(f'\n✓ {len(pages)} pages generated')
