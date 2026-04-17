# Leadesk Marketing Website

Entwurf der Marketing-Website für Leadesk — eigenständig gehostet, getrennt von der Haupt-App (`app.leadesk.de`).

## Seiten

| Datei | Inhalt |
|-------|--------|
| `index.html` | Startseite mit 17 Sektionen (Hero, Personas, Problem, 4 Solution-Kapitel, KI-Grid, Testimonials, Timeline, Integrations, Wettbewerber, Security, FAQ, Footer-CTA) |
| `features.html` | Funktionen-Seite mit 7 Feature-Blöcken (Branding, Sales, Communication, Content, Reporting, KI-Assistent, Chrome-Extension) + Admin-Grid + Integrations |
| `pricing.html` | Preise mit Monatlich/Jährlich-Toggle, 3 Plänen, vollständiger Feature-Vergleichstabelle, Persona-Zuordnung und FAQ |
| `styles.css` | Komplettes Stylesheet (awork-inspiriert, Leadesk-Farbpalette, 16:9-Screenshot-Platzhalter) |
| `leadesk-logo.png` | Offizielles Leadesk-Logo (für helle Hintergründe in der Navigation) |
| `leadesk-logo-white.png` | Weiße Variante des Logos (für dunkle Footer und den blauen Footer-CTA) |
| `vercel.json` | Clean URLs, keine Trailing Slashes |

## Design-Richtung

- **Vorbild:** awork.com — warm, verspielt, blau als dominante Farbe statt nur Akzent
- **Schrift:** Geist (Google Fonts) + Caveat für handschriftliche Akzente
- **Farbpalette aus dem Logo extrahiert:**
  - **Primary Navy:** `rgb(0, 48, 96)` — das tiefe Marineblau aus der Kapsel-Außenkante
  - **Accent Sky Blue:** `rgb(48, 160, 208)` — das helle Blau aus der Kapsel-Mitte
  - Der Navy→Sky-Gradient spiegelt den Logo-Gradient in Footer-CTA, Hero-Glow, Badges, Avataren
- **Sektions-Rhythmus:** Weiß ↔ Cream ↔ Blue-Tint abwechselnd, mit flächig blauem Footer-CTA

## Screenshot-Platzhalter

Alle Produkt-Screenshots sind als **16:9-Breitbild-Container** mit Browser-Chrome angelegt. Jeder hat:
- Eine angedeutete URL in der Chrome-Bar (z.B. `app.leadesk.de/sales/pipeline`)
- Ein zentrales Icon + Label mit dem geplanten Screenshot-Namen
- Den Hinweis „Screenshot folgt" in handschriftlicher Optik

**Später einfach ersetzen:** Jeden `<div class="screenshot__body">`-Block durch ein `<img src="...">` austauschen — die Chrome-Bar bleibt darüber bestehen.

## Inhalte

- **Kunden-Logos:** Fake-Platzhalter (Axentric, Norvo, Kronex, Brevoria, Luminax, Velfort, Steinberg, Hypercode, Rayon, Parasol, Muuuh!, Thjnk)
- **Testimonials:** Erfunden, plausibel formuliert (Janis Berger, Louisa Frühling, Nicole Hörmann, Sebastian Smieja, Vincent Hartig, Sofia Bavas, Ben Ellermann, Ayleen Merz, Horst Wagner)
- **Preise:** Starter 23€/29€, Professional 63€/79€, Business 159€/199€ (jährlich/monatlich)

## Lokale Vorschau

Einfach `index.html` im Browser öffnen — alle Seiten sind statisch und brauchen keinen Build-Schritt.

```bash
# Optional: mit einem lokalen Server
cd leadesk-site
python3 -m http.server 8000
# dann http://localhost:8000 öffnen
```

## Deployment (später)

Als **eigenes Vercel-Projekt** (NICHT das bestehende `prj_KqhdpHmTzD8KoTpIbtPv0htTsnyC` für app.leadesk.de überschreiben!):

1. Neues GitHub-Repo anlegen (z.B. `leadesk-marketing`)
2. Dateien committen
3. In Vercel neues Projekt aus dem Repo erstellen
4. Domain `leadesk.de` (Root-Domain) darauf zeigen lassen
5. Haupt-App bleibt auf Subdomain `app.leadesk.de`

## Nächste Schritte

- [ ] Entwurf reviewen, Feedback geben
- [ ] Echte Screenshots liefern (16:9 Desktop)
- [ ] Rechtliches ausfüllen (Impressum, Datenschutz, AGB)
- [ ] Deployment als neues Vercel-Projekt

---

*Erstellt als statisches HTML/CSS-Setup — kein Build, keine Dependencies, direkt deploybar.*
