# Homepage-Design: LAPP Muller Relaunch-Konzept

Komplett neu aufgebauter Webauftritt für [lappmuller.lappgroup.com/en](https://lappmuller.lappgroup.com/en/) als statische, mehrseitige Website. Die Analyse des bestehenden Auftritts steht in **[REVIEW.md](REVIEW.md)**.

> Design-Konzept zur Abstimmung, nicht die offizielle Website. Jede Seite trägt einen entsprechenden Hinweis.

## Ansehen

- **Lokal:** `docs/index.html` im Browser öffnen, ohne Server und ohne Build-Schritt.
- **Online über GitHub Pages:** Settings → Pages → Source „Deploy from a branch“, Branch `main`, Ordner `/docs`.

## Struktur

```
build.py              Generator: alle Inhalte und Templates (nur Python-Standardbibliothek)
src/assets/css/       Design-System (Tokens, Komponenten, Responsive)
src/assets/js/        Menü, Mega-Menü, Formular-Validierung, mehrstufige Projektanfrage
docs/                 Generierte Website (21 Seiten, Sitemap, robots.txt)
REVIEW.md             Analyse des Ist-Zustands, Zielbild, offene Punkte
```

Inhalte ändern: Texte in `build.py` anpassen (Abschnitte `CO`, `INDUSTRIES`, `CASES`, `PROCESS`, `DOWNLOADS`), dann

```bash
python3 build.py
```

## Seiten

| Bereich | Seiten |
|---|---|
| Startseite | Positionierung, Branchen, Referenzen, Prozess, Cases, CTA |
| Branchen | Übersicht und 8 Detailseiten mit Anwendungen, Nutzen, Spezifikationstabelle, Prozess |
| Kompetenzen | Engineering, Konfektion, Prüfung und Zertifizierung, Prozess |
| Case Studies | Übersicht und 2 Fallstudien |
| Unternehmen | About (inkl. LAPP Gruppe, Nachhaltigkeit, Compliance), Karriere |
| Service | Downloads, Kontakt (mit Formular), Projektanfrage in 3 Schritten |
| Sonstiges | Impressum/Datenschutz (Platzhalter), 404 |

## Design: am LAPP.com-Auftritt ausgerichtet

Layout und Look & Feel folgen www.lapp.com, damit LAPP Muller klar als Teil der LAPP Gruppe erkennbar ist:

- **Header wie LAPP.com:** graue Service-Leiste (Download Center, Telefon, LAPP Group, Sprache), darunter weißer Header mit Logo links, Hauptnavigation *Industries / Solutions / Service / Company* mit Mega-Menüs über die volle Breite, rechts Kontakt und orangem CTA
- **Bühne mit Textbox:** Slider mit weißer Textbox und orangem Akzent, manuell bedienbar (kein Autoplay)
- **Startseite nach LAPP-Muster:** Tabs mit Karten-Raster („Discover“), „Our range of services for you“, „More than just a cable manufacturer“, „Top links“, Block „Do you have any questions?“
- **Heller Footer** mit vier Spalten, Social Links und Legal-Leiste (Imprint, Terms, Privacy notice, Cookie settings)
- **Farben:** LAPP-CI-Orange (HKS 7, RGB 231/120/23) für Akzente, ein etwas dunkleres Orange für Buttons, damit weiße Schrift WCAG AA erfüllt; Schwarz, Grautöne
- **Schrift:** CI-Schrift CorpoS ist hinterlegt, sobald sie lizenziert eingebunden wird; bis dahin Fallback auf Helvetica/Arial
- **Bildsprache:** Statt Fotos berechnete Kabelquerschnitte als SVG, bis eigene Produkt- und Fertigungsfotos vorliegen

## Qualität

- Semantisches HTML, Skip-Link, sichtbare Fokuszustände, ARIA für Menü und Formularschritte
- Funktioniert ohne JavaScript (Progressive Enhancement)
- Responsiv von 360 px bis Desktop, getestet bei 390, 1100 und 1400 px
- SEO: individuelle Titles und Descriptions, Canonicals, hreflang, Open Graph, JSON-LD Organization, Sitemap
- Keine externen Skripte, Fonts oder Tracker

## Vor Go-live

Siehe „Vor Go-live zu klären“ in [REVIEW.md](REVIEW.md): Texte freigeben, Zertifikate bestätigen, Formular-Backend anbinden, eigene Fotos und Webfont ergänzen, französische Version anlegen.
