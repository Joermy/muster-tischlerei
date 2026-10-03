#!/usr/bin/env python3

import json
import pathlib

WURZEL = pathlib.Path(__file__).resolve().parent.parent

BETRIEB = "Tischlerei Hallmann"

CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
    "object-src 'none'; base-uri 'none'; form-action 'none'; "
    "upgrade-insecure-requests"
)

NAVIGATION = [
    ("leistungen", "Leistungen"),
    ("projekte", "Projekte"),
    ("ueber-uns", "Über uns"),
    ("kontakt", "Kontakt"),
]

_nachweise_pfad = WURZEL / "bilder" / "nachweise.json"
BILDER = {}
if _nachweise_pfad.exists():
    BILDER = json.loads(_nachweise_pfad.read_text(encoding="utf-8"))["bilder"]

def bild(name: str, sizes: str, *, eifrig: bool = False, alt: str = None) -> str:
    b = BILDER.get(name)
    if not b:
        return f"<!-- Bild fehlt: {name} — scripts/bilder-holen.py laufen lassen -->"
    srcset = ", ".join(f"../bilder/{name}-{w}.webp {w}w" for w in b["breiten"])
    gross = b["breiten"][-1]
    laden = (
        'fetchpriority="high" decoding="async"'
        if eifrig
        else 'loading="lazy" decoding="async"'
    )
    return (
        f'<img src="../bilder/{name}-{gross}.webp" srcset="{srcset}" '
        f'sizes="{sizes}" width="{b["breite"]}" height="{b["hoehe"]}" '
        f'alt="{alt or b["alt"]}" {laden}>'
    )

def rahmen(name: str, klasse: str, sizes: str, **kw) -> str:
    b = BILDER.get(name)
    farbe = b["farbe"] if b else "var(--flaeche-2)"
    return (
        f'<div class="bild {klasse}" style="--platzhalter:{farbe}">'
        + bild(name, sizes, **kw)
        + "</div>"
    )

def bildband(name: str, alt: str = None) -> str:
    b = BILDER.get(name)
    farbe = b["farbe"] if b else "var(--flaeche-2)"
    return (
        f'\n    <div class="heroband band" style="--platzhalter:{farbe}">\n      '
        + bild(name, "100vw", eifrig=True, alt=alt)
        + "\n    </div>\n"
    )

def kopf(slug: str, titel: str, beschreibung: str) -> str:
    nav = "\n".join(
        f'          <li><a href="../{ziel}/index.html"'
        f'{" aria-current=\"page\"" if ziel == slug else ""}>{text}</a></li>'
        for ziel, text in NAVIGATION
    )

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{titel} — {BETRIEB}</title>
  <meta name="description" content="{beschreibung}">
  <link rel="icon" href="../assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/css/basis.css">
  <link rel="stylesheet" href="../assets/css/raster.css">
  <link rel="stylesheet" href="../assets/css/komponenten.css">
  <link rel="stylesheet" href="../assets/css/bilder.css">
  <link rel="stylesheet" href="../assets/css/bewegung.css">
</head>
<body data-wurzel="../">
  <a class="sprunglink" href="#inhalt">Zum Inhalt</a>

  <header class="kopfzeile">
    <div class="breite kopfzeile__inhalt">
      <a class="marke" href="../index.html">{BETRIEB}<span>.</span></a>
      <nav class="hauptnav" aria-label="Hauptnavigation">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main id="inhalt">
"""

FUSS = f"""  </main>

  <footer class="fusszeile">
    <div class="breite">
      <div class="fusszeile__raster">
        <div>
          <h2>{BETRIEB}</h2>
          <p style="color:var(--muted)">
            Gunzelinstraße 14<br>
            31224 Peine
          </p>
        </div>
        <div>
          <h2>Kontakt</h2>
          <ul>
            <li><a href="tel:+4951715824900">05171 58 24 90</a></li>
            <li><a href="mailto:werkstatt@tischlerei-hallmann.de">werkstatt@tischlerei-hallmann.de</a></li>
          </ul>
        </div>
        <div>
          <h2>Öffnungszeiten</h2>
          <ul>
            <li>Mo – Fr  7.30 – 16.30 Uhr</li>
            <li>Sa  nach Vereinbarung</li>
          </ul>
        </div>
      </div>

      <p class="fusszeile__hinweis">
        <strong>Musterprojekt.</strong> Betrieb, Anschrift und Inhalte sind frei
        erfunden. Kein Kundenauftrag. Diese Seite dient als Arbeitsprobe.
        Die Fotos stammen von Unsplash und zeigen nicht diesen Betrieb —
        Urheber und Lizenz stehen im <a href="../impressum/index.html">Impressum</a>.
      </p>

      <div class="fusszeile__unten">
        <p>{BETRIEB} — © 2026</p>
        <ul>
          <li><a href="../impressum/index.html">Impressum</a></li>
          <li><a href="../datenschutz/index.html">Datenschutz</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script src="../daten/inhalte.js" defer></script>
  <script src="../daten/bilder.js" defer></script>
  <script src="../assets/js/bewegung.js" defer></script>
  <script src="../assets/js/komponenten.js" defer></script>
</body>
</html>
"""

def seitenkopf(auge: str, titel: str, lead: str) -> str:
    return f"""
    <section class="hero breite">
      <p class="hero__auge einblenden">{auge}</p>
      <h1 class="einblenden" style="font-size:var(--fs-h2)">{titel}</h1>
      <p class="hero__lead einblenden">{lead}</p>
    </section>
"""

SEITEN = {
    "leistungen": {
        "titel": "Leistungen",
        "beschreibung": "Möbel nach Maß, Innenausbau, Küchen, Türen, Restaurierung und Reparatur aus einer Tischlerei in Peine.",
        "inhalt": seitenkopf(
            "Was wir machen",
            "Sechs Arbeitsbereiche, ein Maßstab.",
            "Vom eingebauten Schrank bis zur klemmenden Schublade. "
            "Kleine Arbeiten nehmen wir genauso an wie große.",
        )
        + bildband("leistung-innenausbau", "Raum mit eingebauten Holzregalen")
        + """
    <section class="abschnitt breite">
      <div class="spalten spalten--2" id="leistungen-raster"></div>
      <noscript>
        <ul>
          <li>Möbel nach Maß</li><li>Innenausbau</li><li>Küchen</li>
          <li>Türen und Zargen</li><li>Restaurierung</li><li>Reparatur</li>
        </ul>
      </noscript>
    </section>

    <section class="abschnitt breite" aria-labelledby="werkstatt-leistungen">
      <p class="kopf einblenden" data-nummer="01">Aus der Werkstatt</p>
      <h2 id="werkstatt-leistungen" class="nur-vorlesen">Eindrücke aus der Werkstatt</h2>
      __STRECKE_LEISTUNGEN__
    </section>

    <section class="abschnitt breite" aria-labelledby="ablauf-titel">
      <p class="kopf einblenden" data-nummer="02">Ablauf</p>
      <h2 id="ablauf-titel" class="aussage einblenden">Vier Schritte, keine Überraschungen.</h2>

      <div class="einblenden" style="margin-top:var(--sp-7)">
        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="schritt-1">
            <span>01 — Termin vor Ort</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="schritt-1">
            <div><p>Wir sehen uns den Raum an und nehmen Maß. Das kostet nichts und dauert meist unter einer Stunde.</p></div>
          </div>
        </div>

        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="schritt-2">
            <span>02 — Zeichnung und Angebot</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="schritt-2">
            <div><p>Sie bekommen eine maßstäbliche Zeichnung und ein schriftliches Angebot mit Materialangabe. Bis zum Angebot vergehen in der Regel fünf bis sieben Werktage.</p></div>
          </div>
        </div>

        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="schritt-3">
            <span>03 — Bau in der Werkstatt</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="schritt-3">
            <div><p>Gebaut wird bei uns, nicht bei Ihnen. Das hält Staub und Lärm aus der Wohnung.</p></div>
          </div>
        </div>

        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="schritt-4">
            <span>04 — Montage</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="schritt-4">
            <div><p>Wir bauen auf, richten aus und nehmen den Verpackungsmüll wieder mit.</p></div>
          </div>
        </div>
      </div>
    </section>
""",
    },
    "projekte": {
        "titel": "Projekte",
        "beschreibung": "Ausgeführte Arbeiten der Tischlerei Hallmann: Möbel nach Maß, Einbauten und Restaurierungen.",
        "inhalt": seitenkopf(
            "Arbeiten",
            "Was zuletzt die Werkstatt verlassen hat.",
            "Jedes Stück wurde für einen bestimmten Raum gebaut. "
            "Maße, Holzart und Beschläge sind deshalb bei keinem gleich.",
        )
        + bildband("projekt-bibliothek", "Raumhohe Regalwand aus Holz neben einem Fenster")
        + """
    <section class="abschnitt breite">
      <div class="spalten spalten--2" id="projekte-raster"></div>
      <noscript>
        <ul>
          <li>Eichenschrank unter der Schräge, Peine 2025</li>
          <li>Küchentheke aus einem Stamm, Vechelde 2025</li>
          <li>Bibliothekswand raumhoch, Braunschweig 2024</li>
          <li>Altbautüren aufgearbeitet, Hildesheim 2024</li>
        </ul>
      </noscript>

      <div class="einblenden" style="margin-top:var(--sp-9)">
        __STRECKE_PROJEKTE__
      </div>

      <p class="einblenden" style="margin-top:var(--sp-7);font-size:var(--fs-meta);color:var(--muted)">
        Wir zeigen hier vier Arbeiten aus den letzten beiden Jahren. Weitere Stücke sehen Sie bei einem Termin in der Werkstatt.
      </p>
    </section>
""",
    },
    "ueber-uns": {
        "titel": "Über uns",
        "beschreibung": "Meisterbetrieb in Peine: wer in der Werkstatt steht und wie gearbeitet wird.",
        "inhalt": seitenkopf(
            "Der Betrieb",
            "Eine Werkstatt, überschaubar geblieben.",
            "Gegründet 1998 von Andreas Hallmann in einer Scheune am Ortsrand, "
            "seit 2011 in der heutigen Werkstatt an der Gunzelinstraße. Geblieben "
            "ist die Größe: sechs Leute, eine Werkstatt, keine Filialen.",
        )
        + bildband("werkstatt-arbeit", "Tischler beim Ausrichten eines Werkstücks")
        + """
    <section class="abschnitt breite">
      <div class="gespann">
        <div class="gespann__fest">
          <h2 class="aussage einblenden">Wer baut, steht auch beim Aufmaß dabei.</h2>
        </div>
        <div>
          <p class="einblenden" style="color:var(--muted)">
            Zum Aufmaß kommt der, der das Stück später baut. Das klingt selbstverständlich, ist es aber nicht: in größeren Betrieben nimmt der Verkauf das Maß und die Werkstatt erfährt davon per Zettel. Bei uns steht dieselbe Person am Küchentisch und später an der Fräse — und montiert am Ende auch.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-5);color:var(--muted)">
            Wir sind zu sechst, zwei davon in der Ausbildung. Seit 2004 bilden wir durchgehend aus; die meisten bleiben danach. Für August ist ein Platz frei — eine formlose E-Mail reicht, ein Praktikumstag davor ist uns lieber als eine Mappe.
          </p>

          <div class="freilegen" style="margin-top:var(--sp-7)">
            __BILD_HOBEL__
          </div>
          <p class="bildzeile"><b>Handarbeit</b><span>Hobel und Beitel</span></p>
        </div>
      </div>
    </section>

    <section class="abschnitt--eng breite">
      <dl class="kennzahlen einblenden">
        <div class="kennzahl">
          <dt>Im Handwerk</dt>
          <dd><span data-zaehlziel="27">27</span></dd>
        </div>
        <div class="kennzahl">
          <dt>Mitarbeiter</dt>
          <dd><span data-zaehlziel="6">6</span></dd>
        </div>
        <div class="kennzahl">
          <dt>Werkstatt</dt>
          <dd><span data-zaehlziel="420">420</span> <span>m²</span></dd>
        </div>
      </dl>
    </section>

    <section class="abschnitt breite" aria-labelledby="werkstatt-titel">
      <p class="kopf einblenden" data-nummer="01">In der Werkstatt</p>
      <h2 id="werkstatt-titel" class="nur-vorlesen">Eindrücke aus der Werkstatt</h2>
      <div class="werkstatt">
        <div class="werkstatt__hoch freilegen">
          __BILD_PORTRAET__
          <p class="bildzeile"><b>Zuschnitt</b><span>Gehrungssäge</span></p>
        </div>
        <div class="werkstatt__quer freilegen">
          __BILD_SPAENE__
          <p class="bildzeile"><b>Nach dem Schliff</b><span>Späne auf der Bohle</span></p>
        </div>
      </div>
    </section>
""",
    },
    "kontakt": {
        "titel": "Kontakt",
        "beschreibung": "Telefon, E-Mail und Anfahrt zur Tischlerei Hallmann in Peine.",
        "inhalt": seitenkopf(
            "Kontakt",
            "Rufen Sie an, das geht am schnellsten.",
            "Für ein Aufmaß brauchen wir einen Termin. Am Telefon ist in "
            "fünf Minuten geklärt, ob wir der richtige Betrieb dafür sind.",
        )
        + bildband("kontakt-spaene", "Sägespäne auf einer Bohle")
        + """
    <section class="abschnitt breite">
      <div class="gespann">
        <div>
          <dl class="kontaktliste einblenden">
            <dt>Telefon</dt>
            <dd><a href="tel:+4951715824900">05171 58 24 90</a></dd>
            <dt>E-Mail</dt>
            <dd><a href="mailto:werkstatt@tischlerei-hallmann.de">werkstatt@tischlerei-hallmann.de</a></dd>
            <dt>Werkstatt</dt>
            <dd>Gunzelinstraße 14<br>31224 Peine</dd>
            <dt>Öffnungszeiten</dt>
            <dd>Mo – Fr  7.30 – 16.30 Uhr<br>Sa  nach Vereinbarung</dd>
          </dl>
        </div>

        <div class="einblenden">
          <h2 style="font-size:var(--fs-h3);margin-bottom:var(--sp-4)">Anfahrt</h2>
          <p style="color:var(--muted)">
            Von der B 494 kommend an der Ampel am Schützenplatz in die Gunzelinstraße abbiegen, die Werkstatt liegt nach 300 Metern rechts hinter dem Holzlager. Vor dem Tor stehen vier Parkplätze, die Einfahrt bitte frei lassen.
          </p>
          <p style="margin-top:var(--sp-5);font-size:var(--fs-meta);color:var(--muted)">
            Eine eingebettete Karte fehlt hier bewusst: sie würde beim Aufruf
            Daten an einen fremden Anbieter senden, bevor jemand eingewilligt
            hat. Ein Link zur Kartenanwendung wird erst auf Klick geöffnet.
          </p>
          <p style="margin-top:var(--sp-5)">
            <a class="knopf knopf--leer" href="https://www.openstreetmap.org/search?query=Gunzelinstra%C3%9Fe%2014%2C%2031224%20Peine" rel="noopener">
              In der Karte öffnen
            </a>
          </p>
        </div>
      </div>

      <div class="einblenden" style="margin-top:var(--sp-9)">
        __STRECKE_KONTAKT__
      </div>
    </section>
""",
    },
}

def strecke(*eintraege):
    karten = []
    for name, titel, zeile in eintraege:
        karten.append(
            '<div class="freilegen">'
            + rahmen(name, "bild--3-2",
                     "(max-width: 640px) 90vw, (max-width: 1100px) 45vw, 30vw")
            + f'<p class="bildzeile"><b>{titel}</b><span>{zeile}</span></p>'
            + "</div>"
        )
    return '<div class="spalten spalten--3">' + "".join(karten) + "</div>"


MARKEN = {
    "__STRECKE_LEISTUNGEN__": lambda: strecke(
        ("werkstatt-hobel", "Handarbeit", "Hobel und Beitel"),
        ("leistung-restaurierung", "Restaurierung", "alte Oberflächen"),
        ("kontakt-spaene", "Nach dem Schliff", "Späne auf der Bohle"),
    ),
    "__STRECKE_PROJEKTE__": lambda: strecke(
        ("werkstatt-arbeit", "Abbund", "Ausrichten vor dem Verleimen"),
        ("folge-7", "Fertig", "Regal aus massivem Holz"),
        ("leistung-moebel", "Unter der Schräge", "Arbeitsplatz nach Maß"),
    ),
    "__STRECKE_KONTAKT__": lambda: strecke(
        ("folge-6", "Werkstattwand", "jedes Werkzeug an seinem Platz"),
        ("folge-1", "Aufmaß", "Zeichnung und Maßband"),
        ("leistung-reparatur", "Kleine Arbeiten", "Beitel und Späne"),
    ),
    "__BILD_HOBEL__": lambda: rahmen(
        "werkstatt-hobel", "bild--3-2", "(max-width: 860px) 90vw, 55vw"
    ),
    "__BILD_PORTRAET__": lambda: rahmen(
        "werkstatt-portraet", "bild--4-5", "(max-width: 860px) 90vw, 40vw"
    ),
    "__BILD_SPAENE__": lambda: rahmen(
        "kontakt-spaene", "bild--3-2", "(max-width: 860px) 90vw, 55vw"
    ),
}

def bauen() -> None:
    if not BILDER:
        print("WARNUNG: bilder/nachweise.json fehlt.")
        print("         Erst scripts/bilder-holen.py laufen lassen.\n")

    for slug, seite in SEITEN.items():
        inhalt = seite["inhalt"]
        for marke, bauer in MARKEN.items():
            if marke in inhalt:
                inhalt = inhalt.replace(marke, bauer())

        ziel = WURZEL / slug / "index.html"
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(
            kopf(slug, seite["titel"], seite["beschreibung"]) + inhalt + FUSS,
            encoding="utf-8",
        )
        print(f"geschrieben: {ziel.relative_to(WURZEL)}")

if __name__ == "__main__":
    bauen()
    print("\nImpressum und Datenschutz werden NICHT erzeugt — sie stehen von Hand,")
    print("damit kein Generator versehentlich eine Pflichtangabe umschreibt.")
