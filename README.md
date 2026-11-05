# leadesk-marketing

Statische Marketing-Website (leadesk.de). Reines HTML + `assets/leadesk.css` + `assets/leadesk.js`, kein Build.

**Statistik:** Vercel Web Analytics (cookielos), einsehbar im Vercel-Dashboard → Projekt `leadesk-marketing` → **Analytics**. Jede Seite bindet dafür im `<head>` `/_vercel/insights/script.js` ein — bei neuen Seiten mitkopieren.

**Deploy:** Git-verbunden mit dem Vercel-Projekt `leadesk-marketing` → jeder Push auf `main` = automatischer Production-Deploy.

**Stand:** Am 14.07.2026 aus der Live-Auslieferung rekonstruiert (der frühere CLI-Deploy-Stand war nicht mehr im Repo) + echte Impressum-/Datenschutz-Seiten ergänzt.

## Design (CI-Look, seit 05.11.2026)

Die Website folgt dem Look der App (app.leadesk.de, „2026“-Look): klare helle Flächen, Linien statt Schatten, 4px-Radien, Navy als Primärfarbe, Cyan als Akzent. Ein früherer Entwurf („Signal“, dunkel/futuristisch) war vom 04.–05.11.2026 live und wurde nach Feedback zurückgenommen — er liegt in der Git-Historie (PR #18–#21).

| Datei | Wofür |
|---|---|
| `assets/leadesk.css` | Basis-Design-System (Komponenten) |
| `assets/leadesk-redesign.css` / `.js` | Ergänzungen (Mobile-Nav, Karussell, Tabs …) |
| `assets/ci.css` | CI-Schicht: Schriften, Farben, Radien, Startseiten-Hero — lädt **nach** den beiden anderen |
| `assets/fonts/` | Inter (400–800) und Lexend Deca (400–900), aus der App übernommen, self-hosted |

**Farben:** Navy `#003060` · Text `#213343` · Text gedämpft `#516F90` · Linie `#DFE3EB` · Fläche `#EEF2F6` · Auswahl `#EEF5FB` · Cyan `#16A8DC` / `#0A6FB0`.
**Schrift:** Überschriften, Buttons, Navigation in Lexend Deca; Fließtext in Inter.
**Keine Emojis** — Icon-Plätze in `.card .ic` bleiben leer, dort erscheint automatisch eine Nummer.

### Neue Unterseite anlegen

Zusätzlich zu Header/Footer, Meta-Tags, JSON-LD, `sitemap.xml` und Verlinkung:

1. `<body class="ci">`
2. Im `<head>` **nach** `leadesk-redesign.css`:
   ```html
   <link rel="preload" href="assets/fonts/lexend-deca-latin-600.woff2" as="font" type="font/woff2" crossorigin>
   <link rel="stylesheet" href="assets/ci.css">
   ```
   (im Blog und unter `services/` mit `/assets/...`)
3. Vor `</head>` das Analytics-Snippet (siehe oben „Statistik“).
4. `<meta name="theme-color" content="#003060">`
