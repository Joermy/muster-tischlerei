#!/usr/bin/env python3
import os
import re
import sys
import urllib.parse

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORIEREN = {".git", "node_modules", "scripts", ".github"}

ZIEL_STARTSEITE_BYTES = 800 * 1024
GRENZE_STARTSEITE_BYTES = 1500 * 1024

IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_ATTR = re.compile(r'alt\s*=\s*"([^"]*)"', re.IGNORECASE)
HREF_SRC = re.compile(r'\b(?:href|src)\s*=\s*"([^"]+)"', re.IGNORECASE)

def html_dateien():
    for wurzel, ordner, dateien in os.walk(WURZEL):
        ordner[:] = [o for o in ordner if o not in IGNORIEREN and not o.startswith(".")]
        for name in dateien:
            if name.endswith(".html"):
                yield os.path.join(wurzel, name)

def pruefe_alt_texte():
    fehler = []
    for pfad in html_dateien():
        with open(pfad, encoding="utf-8") as f:
            inhalt = f.read()
        for tag in IMG_TAG.findall(inhalt):
            if not ALT_ATTR.search(tag):
                fehler.append(f"{rel(pfad)}: <img> ohne alt-Attribut")
    return fehler

def ist_extern(ziel):
    return ziel.startswith(("http://", "https://", "mailto:", "tel:", "#"))

def pruefe_links():
    fehler = []
    geprueft = 0
    for pfad in html_dateien():
        with open(pfad, encoding="utf-8") as f:
            inhalt = f.read()
        ordner = os.path.dirname(pfad)
        for ziel in HREF_SRC.findall(inhalt):
            ziel = ziel.split("#")[0]
            if not ziel or ist_extern(ziel):
                continue
            ziel_pfad = urllib.parse.unquote(ziel)
            absolut = os.path.normpath(os.path.join(ordner, ziel_pfad))
            geprueft += 1
            if not os.path.exists(absolut):
                fehler.append(f"{rel(pfad)}: kaputter Link -> {ziel}")
    return fehler, geprueft

def rel(pfad):
    return os.path.relpath(pfad, WURZEL).replace("\\", "/")

def startseiten_gewicht():
    import re

    startseite = os.path.join(WURZEL, "index.html")
    dateien = ["index.html"]

    if os.path.exists(startseite):
        with open(startseite, encoding="utf-8") as f:
            inhalt = f.read()
        for treffer in re.findall(r'(?:href|src)="([^"]+\.(?:css|js))"', inhalt):
            if not treffer.startswith(("http", "//")):
                dateien.append(treffer.lstrip("/"))

    schriftordner = os.path.join(WURZEL, "assets", "fonts")
    if os.path.isdir(schriftordner):
        for name in sorted(os.listdir(schriftordner)):
            if name.endswith(".woff2"):
                dateien.append(f"assets/fonts/{name}")

    gesamt = 0
    fehlend = []
    for relpfad in dict.fromkeys(dateien):
        pfad = os.path.join(WURZEL, relpfad)
        if os.path.exists(pfad):
            gesamt += os.path.getsize(pfad)
        else:
            fehlend.append(relpfad)
    return gesamt, fehlend

def haupt():
    print("site-audit — Portfolio-Pruefung\n")

    gesamt, fehlend = startseiten_gewicht()
    print(f"Startseite (HTML+CSS+JS+Daten+Fonts+erste Bilder @400w): {gesamt / 1024:.1f} KB")
    print(f"  Ziel:  < {ZIEL_STARTSEITE_BYTES / 1024:.0f} KB")
    print(f"  Grenze: < {GRENZE_STARTSEITE_BYTES / 1024:.0f} KB")
    status = "OK (unter Ziel)" if gesamt < ZIEL_STARTSEITE_BYTES else ("OK" if gesamt < GRENZE_STARTSEITE_BYTES else "FEHLER")
    print(f"  Status: {status}")
    if fehlend:
        print("  Fehlende Dateien in der Gewichtspruefung:")
        for f in fehlend:
            print(f"    - {f}")

    print()
    alt_fehler = pruefe_alt_texte()
    print(f"Alt-Texte: {len(alt_fehler)} Problem(e)")
    for f in alt_fehler:
        print(f"  - {f}")
    if not alt_fehler:
        print("  Alle <img>-Tags haben ein alt-Attribut.")

    print()
    link_fehler, geprueft = pruefe_links()
    print(f"Interne Links: {geprueft} geprueft, {len(link_fehler)} kaputt")
    for f in link_fehler:
        print(f"  - {f}")
    if not link_fehler:
        print("  Alle internen Links loesen auf.")

    fehlgeschlagen = bool(alt_fehler) or bool(link_fehler) or gesamt >= GRENZE_STARTSEITE_BYTES
    print()
    print("Ergebnis: " + ("FEHLER" if fehlgeschlagen else "OK"))
    return 1 if fehlgeschlagen else 0

if __name__ == "__main__":
    sys.exit(haupt())
