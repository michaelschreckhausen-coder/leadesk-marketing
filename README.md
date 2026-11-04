# leadesk-marketing

Statische Marketing-Website (leadesk.de). Reines HTML + `assets/leadesk.css` + `assets/leadesk.js`, kein Build.

**Statistik:** Vercel Web Analytics (cookielos), einsehbar im Vercel-Dashboard → Projekt `leadesk-marketing` → **Analytics**. Jede Seite bindet dafür im `<head>` `/_vercel/insights/script.js` ein — bei neuen Seiten mitkopieren.

**Deploy:** Git-verbunden mit dem Vercel-Projekt `leadesk-marketing` → jeder Push auf `main` = automatischer Production-Deploy.

**Stand:** Am 14.07.2026 aus der Live-Auslieferung rekonstruiert (der frühere CLI-Deploy-Stand war nicht mehr im Repo) + echte Impressum-/Datenschutz-Seiten ergänzt.

## Design „Signal“ (seit 04.11.2026)

Seit PR #18/#19 hat die Seite einen eigenen Look: dunkle Page-Heros mit gestauchten Versalien, Papierflächen, Cyan als einzige Signalfarbe, harte Kanten, keine Schatten, **keine Serifen, keine Emojis**.

| Datei | Wofür |
|---|---|
| `assets/signal-base.css` | gemeinsam: Schriften (self-hosted), Farben, Korn, Cursor-Ring, dunkler Header/Footer, Buttons |
| `assets/home-signal.css` / `.js` | nur `index.html` (`<body class="sig">`): Partikel-Hero, Scroll-Sequenzen, Kanal-Panels usw. |
| `assets/signal-sub.css` / `.js` | alle Unterseiten (`<body class="sig-sub">`): Skin für die bestehenden Komponenten aus `leadesk.css` |
| `assets/fonts/` | Archivo (variabel, wdth 62–125 / wght 100–900) und JetBrains Mono, OFL-Lizenz |

**Farben:** Ink `#07091A` · Papier `#ECEAE3` / `#E2DFD5` · Signal-Cyan `#16A8DC` · Cyan dunkel `#0A6FB0`.
**Schrift:** Headlines Archivo 800, `font-stretch:74–78%`, Versalien. Akzentwörter (`<span class="grad-text">` in Headlines) werden automatisch zu Archivo 200 / 62 % in Cyan. Labels und Buttons: JetBrains Mono, Versalien.

### Neue Unterseite anlegen

Zusätzlich zu den bisherigen Punkten (Header/Footer einkopieren, Meta-Tags, JSON-LD, `sitemap.xml`, verlinken):

1. `<body class="sig-sub">`
2. Im `<head>` **nach** `leadesk-redesign.css`:
   ```html
   <link rel="preload" href="assets/fonts/Archivo-normal-100_900.woff2" as="font" type="font/woff2" crossorigin>
   <link rel="stylesheet" href="assets/signal-base.css">
   <link rel="stylesheet" href="assets/signal-sub.css">
   <script>document.documentElement.classList.add('js-sub')</script>
   ```
   (im Blog mit `/assets/...`)
3. Am Ende nach `leadesk-redesign.js`: `<script src="assets/signal-sub.js"></script>`
4. `<meta name="theme-color" content="#07091A">`
5. Seite mit einem `<section class="page-hero">` beginnen. Die bestehenden Bausteine (`.card`, `.mock`, `.checklist`, `.cta-band`, `.faq`, `.plans` …) bekommen den neuen Look automatisch.
6. Keine Emojis und keine Serifenschriften verwenden. Icons in `.card .ic` bleiben leer — dort erscheint automatisch eine Nummer.

### Fallstricke

- **Klassennamen:** Der Cursor-Ring heißt `.sgc`. Kurze generische Klassen (`.cur`, `.grain` …) nicht doppelt belegen — `.cur` ist das €-Zeichen auf `preise.html`.
- **Dunkle Zonen** (`.page-hero`, `.mock`, `.plan.pop`, `.cust`) setzen die Farb-Variablen lokal um. Inline-Styles mit `var(--ink)`, `var(--muted)` passen sich dort an; feste Farben wie `#fff` nicht — `signal-sub.js` dunkelt weiße Flächen in Mocks automatisch ab.
- **Effekte testen:** Partikel, Ticker und Blobs laufen endlos. Für Screenshot-Vergleiche `reducedMotion: 'reduce'` setzen — dann ist alles statisch.
