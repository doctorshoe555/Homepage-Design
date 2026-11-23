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

## Design-Idee

Die technische Zeichnung als Markensprache: Jede Branche bekommt einen eigenen, berechneten Kabelquerschnitt als SVG statt Stockfotos. Spezifikationen erscheinen als Schriftfeld wie auf einer Konstruktionszeichnung, der Footer ist als Zeichnungs-Schriftfeld gebaut. LAPP-Orange ist ausschließlich für Aktionen reserviert. Auf der Startseite zeichnet sich der Querschnitt einmalig beim Laden auf; bei reduzierter Bewegung entfällt die Animation.

## Qualität

- Semantisches HTML, Skip-Link, sichtbare Fokuszustände, ARIA für Menü und Formularschritte
- Funktioniert ohne JavaScript (Progressive Enhancement)
- Responsiv von 360 px bis Desktop, getestet bei 390, 1100 und 1400 px
- SEO: individuelle Titles und Descriptions, Canonicals, hreflang, Open Graph, JSON-LD Organization, Sitemap
- Keine externen Skripte, Fonts oder Tracker

## Vor Go-live

Siehe „Vor Go-live zu klären“ in [REVIEW.md](REVIEW.md): Texte freigeben, Zertifikate bestätigen, Formular-Backend anbinden, eigene Fotos und Webfont ergänzen, französische Version anlegen.
