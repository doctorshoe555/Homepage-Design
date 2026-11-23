# Review: lappmuller.lappgroup.com/en/

Stand der Analyse: 23.11.2026. Geprüft wurden Startseite, „About us – LAPP Muller“, „Contact us“, die Navigationsstruktur sowie öffentlich verlinkte Broschüren und Datenblätter. Einige Unterseiten (Defense, Electrification, Customised solutions) waren beim Abruf nicht erreichbar bzw. rate-limitiert; ihre Inhalte wurden aus Navigation, Suchindex und PDFs rekonstruiert.

## Kurzfazit

LAPP Muller hat ein starkes, seltenes Angebot – kundenspezifische Spezialkabel für Verteidigung, Kerntechnik, Subsea und Elektrifizierung, auch in Kleinstmengen – aber der Auftritt verkauft es nicht. Die Seite ist ein Ableger des Konzern-CMS: generische Konzernnavigation, Slider ohne Botschaft, Prozess und Zertifikate nur als Bild, keine klare Anfrage-Strecke. Für einen Engineering-getriebenen B2B-Kauf fehlen die drei Dinge, die Einkäufer und Ingenieure suchen: **Nachweis von Kompetenz** (Referenzen, Normen, Grenzwerte), **ein klarer nächster Schritt** (Anfrage mit technischen Parametern) und **Vertrauen** (wer, wo, seit wann, Ansprechpartner).

## Befunde

### 1. Positionierung und Botschaft
- H1 „Welcome to LAPP Muller“ ist eine Leerformel. Die eigentliche Differenzierung („jede Länge, jeder Querschnitt, auch Kurzlängen; extreme Umgebungen; schnell“) steht erst auf der About-Seite.
- Der Hero-Slider hat vier Bilder ohne lesbare Captions. Auto-Slider haben nachweislich niedrige Interaktionsraten und verschieben die Kernbotschaft.
- Fakten, die Vertrauen schaffen, fehlen auf der Startseite: Technologiezentrum der LAPP Gruppe seit 2003, Standort Grimaud (Var), Referenzen wie EPR-Kraftwerke, EDF, ORANO La Hague, CERN, Archiv von rund 60.000 Spezialkabel-Konstruktionen.

### 2. Informationsarchitektur
- 11 Anwendungsbereiche plus verschachtelte Untermenüs, teils überlappend (Customised solutions ↔ Special cables; Electrification als Branche und als Anwendung).
- Uneinheitliche URL-Muster: `/applications/robotics.html`, `/applications-and-solutions/...`, `/electrification-1.html`, `/contacts/` vs. `/contact-us/`.
- Übersetzungsreste in URLs und Menüs: `translate-to-english-...`, „Postes à pourvoir“, „equipe-commerciale“ auf der englischen Seite.
- Case Studies sind unter „Defense“ versteckt statt als eigener Beweisbereich sichtbar.

### 3. Conversion
- Die E-Mail-CTA verlinkt auf `#` – führt ins Leere.
- Kein Anfrageformular mit technischen Parametern, obwohl ein „Needs Analysis Sheet (FIB)“ existiert – als PDF-Download versteckt.
- Telefonnummer ohne Ländervorwahl (`0494566500`), Tel-Link mit Leerzeichen. Für internationale Kunden nicht wählbar.
- Öffnungszeiten widersprüchlich: Startseite 08:00–17:00, Kontaktseite Mo–Do 08:30–17:00, Fr bis 15:30.
- Kein Hinweis auf Reaktionszeit, Ansprechpartner oder NDA-Fähigkeit – bei Defence- und Nuklearprojekten ein Kaufkriterium.

### 4. Inhalt und Sprache
- Tippfehler („Pease call us“), inkonsistente Schreibweisen („Terms of trade“/„Terms of Trade“, „Oil&Gas“, „Defense“/„Defence“).
- Der Kollaborationsprozess (6 Schritte) existiert nur als Grafik.
- Zertifizierungen nur als Bild, keine konkreten Normen im Text. Meta-Keywords erwähnen UL und DNV, sichtbar ist davon nichts.
- Footer-Disclaimer „Lapp Insulator is not affiliated with the Lapp Group“ erscheint doppelt und irritiert eher, als dass er aufklärt.

### 5. Technik, SEO, Barrierefreiheit
- Sichtbarer CMS-Platzhalter „You're logged in as Max Mustermann“ – wirkt unprofessionell.
- Doppelte Alt-Texte („DéfenseDéfenseDefence“, „electificity-icon…“), Prozessschritte nicht screenreader-tauglich.
- Splash/Overlay „Sie verlassen die deutsche Website“ beim Erstbesuch – unnötige Hürde.
- `fr`-Schalter führt auf die Root-URL statt auf die französische Entsprechung der aktuellen Seite; keine erkennbaren `hreflang`-Paare.
- Keine strukturierten Daten (Organization, LocalBusiness), keine Adresse auf der Startseite (lokales SEO, Vertrauen).

## Zielbild des Relaunch-Konzepts

| Ziel | Umsetzung im Repository |
|---|---|
| Klare Positionierung in einem Satz | Hero: „Cables built for one job, in any length.“ + drei harte Fakten |
| Wenige, eindeutige Einstiege | 8 Branchen statt 11+ Anwendungen; Spezialanwendungen gebündelt |
| Beweise sichtbar machen | Eigener Bereich Case Studies, Referenzen pro Branche, Spezifikationstabellen |
| Ein klarer nächster Schritt | „Start a project“: Online-Bedarfsanalyse (ersetzt das FIB-PDF) auf jeder Seite |
| Prozess als Text | 6 Schritte als echte, zugängliche Liste |
| Saubere Struktur | Sprechende, einheitliche URLs (`/industries/nuclear.html`), Sitemap, robots.txt |
| Vertrauen | Adresse, Ländervorwahl, einheitliche Servicezeiten, Ansprechpartner-Logik, JSON-LD |
| Barrierefreiheit | Semantisches HTML, Fokus-Stile, Skip-Link, reduzierte Bewegung, Kontrast AA |
| Wartbarkeit | Inhalte zentral in `build.py`, Seiten werden generiert – keine Copy-Paste-Pflege |

## Neue Sitemap

```
/                       Startseite
/industries/            Branchenübersicht
  defence, electrification, nuclear, marine-subsea,
  oil-gas, robotics-automation, medical, harsh-environments
/capabilities.html      Engineering, Konfektion, Prüfung & Zertifizierung, Prozess
/case-studies/          Übersicht + 2 Fallstudien
/about.html             Unternehmen, LAPP Gruppe, Nachhaltigkeit, Compliance
/careers.html           Karriere
/downloads.html         Kataloge, Datenblätter, AGB
/contact.html           Kontakt
/start-a-project.html   Projektanfrage (Bedarfsanalyse)
/legal.html             Impressum & Datenschutz (Platzhalter)
```

## Vor Go-live zu klären

- Alle als Entwurf markierten Texte (insb. Fallstudien und Prozessschritte) mit Produktmanagement abstimmen; die Originale liegen bisher nur als Bild vor.
- Konkrete Zertifikate (z. B. ISO 9001, DNV, UL) und Normen bestätigen, bevor sie genannt werden.
- Formular-Backend anbinden (CRM/Mail), DSGVO-Einwilligung juristisch prüfen.
- Eigene Fotos aus Fertigung und Prüffeld ergänzen; das Konzept arbeitet bewusst mit technischen Zeichnungen statt Stockfotos.
- Webfont selbst hosten (z. B. Barlow, OFL) statt Systemschriften; keine Google-Fonts-Einbindung (DSGVO).
- Französische Version mit `hreflang`-Paaren aufsetzen; der Generator ist dafür vorbereitet.
