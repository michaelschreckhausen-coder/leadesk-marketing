# Leadesk.de — Design „Signal“

Stand: 04.11.2026 · live seit PR #18 (Merge `bec5cee`) und #19 (Merge `34dc1da`), Folge-PR „Feinschliff“ siehe unten.

## Herkunft
Inspiriert von einem Reel von @slashdevhq („6 Website Designs every designer should know“: houseevil.xyz, breachbunny.com, kidzfrmnowhere.com, bfcm.shopify.com, obsession-engineering.com, caffe.design). Übernommen wurden Prinzipien, keine Optik: ein starkes Signature-Objekt pro Seite, mutige Typografie, Übergänge, die man spürt. Michaels Vorgabe: **nicht nach KI-Website aussehen** — deshalb keine Verläufe, Blobs, Glas-Effekte, runden Karten, Emojis und **keine Serifen** (kursive Serifen-Akzente sind ein typisches KI-/Template-Muster).

## Gestaltung
- Farben: Ink `#07091A`, Papier `#ECEAE3` / `#E2DFD5`, Signal-Cyan `#16A8DC`, Cyan dunkel `#0A6FB0`. Radien 0, keine Schatten (Ausnahme: harter cyan Versatz-Schatten an Mocks).
- Schriften, self-hosted (OFL, kein Google-Fonts-Request): Archivo variabel (wdth 62–125, wght 100–900) und JetBrains Mono.
- Headlines: Archivo 800, `font-stretch` 74–78 %, Versalien. Akzentwörter: Archivo 300, 62 %, Versalien, Cyan.
- Labels/Buttons: JetBrains Mono, Versalien. Sektions-Labels nummeriert „(01) …“.
- Mauszeiger bleibt sichtbar; ein cyan Ring folgt leicht verzögert und pulsiert (Klasse `.sgc`).

## Dateien
| Datei | Wofür |
|---|---|
| `assets/signal-base.css` | gemeinsam: Fonts, Tokens, Korn, Cursor-Ring, Header/Footer dunkel, Buttons |
| `assets/home-signal.css` / `.js` | nur Startseite (`body.sig`) |
| `assets/signal-sub.css` / `.js` | alle Unterseiten (`body.sig-sub`), Skin ohne Markup-Umbau |
| `assets/fonts/` | Archivo-normal-100_900.woff2, JetBrainsMono-normal-400.woff2 |

## Startseite (Reihenfolge)
Partikel-Hero „LEADESK“ (weicht der Maus aus, zerfällt beim Scrollen) · Velocity-Marquee · „Sechs Tools“: sechs Fenster werden in den Leadesk-Kreis gezogen, Kreis füllt den Screen · Leadly als Terminal · Kanäle als horizontale Fahrt (5 Panels) · Modul-Index mit Hover-Streckung · App mit 3D-Phone · Sicherheits-Stempel · Zielgruppen-Akkordeon · Finale mit Buchstaben, die auf Mausnähe reagieren.
Ticker im Hero und KI-Chat-Panel sind als „Beispiel-Workspace“ bzw. „Illustration“ gekennzeichnet.

## Unterseiten
Dunkler Page-Hero mit gestauchter Headline, Punkteraster das der Maus ausweicht, Umriss-Geisterwort, Meta-Zeile mit Uhr. Haarlinien-Kartenraster mit Hover-Spotlight, Terminal-Mocks, cyan CTA-Flächen. Dunkle Zonen (`.page-hero`, `.mock`, `.plan.pop`, `.cust`) invertieren die Farb-Variablen lokal, damit Inline-Styles mitziehen.

## Neue Unterseite
Siehe README.md im Repo, Abschnitt „Neue Unterseite anlegen“.

## Gelöste Fallstricke
- Klassenname `.cur` für den Cursor kollidierte mit dem €-Zeichen auf preise.html → Cursor heißt `.sgc`.
- Ursprünglich war der echte Mauszeiger ausgeblendet und auf der Startseite gar kein Zeiger sichtbar → behoben, Zeiger immer sichtbar.
- Korn-Ebene (`inset:-50%`) erzeugte Überbreite → in eigenen Container mit `overflow:hidden`.
- Emojis waren zunächst nur per JS ausgeblendet (das entfernte versehentlich auch „©“) → jetzt aus dem HTML entfernt, JS-Filter raus.

## Rückweg
Vor dem Design: Production-Deployment `9e309da` (Vercel-ID 7392016762) bzw. `git revert -m 1` auf die Merge-Commits in umgekehrter Reihenfolge.
