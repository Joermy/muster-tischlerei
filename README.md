# Tischlerei Hallmann — Musterwebsite

Eine Musterwebsite für einen Tischlerbetrieb. Der Betrieb ist frei erfunden: Name, Personen,
Anschrift, Telefonnummer, Preise, Register- und Kammernummern gibt es nicht.
Die Seite gehört zu keinem Kundenauftrag und bietet nichts an.

Statisches HTML, CSS und JavaScript. Kein Framework, kein Build-Schritt, keine
externe Ressource — Schriften und Bilder liegen im Ordner.

## Ansehen

```bash
python scripts/dev-server.py
```

Dann `http://localhost:8080` öffnen.

## Prüfen

```bash
python scripts/pruefen.py
```

Prüft externe Ressourcen, Pflichtbestandteile je Seite, Bilder, interne Links,
das Gewicht des ersten Aufrufs und verbliebene Platzhalter.

## Bilder

Die Fotos stammen von Unsplash und zeigen nicht diesen Betrieb. Urheber und
Lizenz stehen im Impressum der Seite.

## Suchmaschinen

Die Seite ist bewusst auf `noindex` gestellt und `robots.txt` verbietet das
Einlesen. Ein erfundener Betrieb soll nicht in Suchergebnissen auftauchen.
