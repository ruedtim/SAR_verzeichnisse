#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Findmittel-PDFs aus dem Online-Archiv des Stadtarchivs Zürich auflisten und herunterladen.

Aufruf
    uv run findmittel_laden.py --liste findmittel_pdf/verzeichnis.csv
        geht den Archivplan durch und schreibt alle Bestände mit angehängten PDFs (inkl. Grösse) in die CSV
    uv run findmittel_laden.py --liste findmittel_pdf/verzeichnis.csv --laden findmittel_pdf/
        lädt die in der CSV aufgeführten Findmittel-PDFs (bereits vorhandene gleich grosse Dateien werden übersprungen)

Quelle: Online-Archivkatalog https://amsquery.stadt-zuerich.ch/ (scopeArchiv Query). Das Skript folgt von der
Wurzel aus den Links «Zum Eintrag auf untergeordneter Stufe» und «Zum nächsten Eintrag im Archivplan» bis zur
Stufe «Bestand» und liest dort die angehängten Dateien («openDoc('Dateien/…')»). Unterhalb der Bestände wird
nicht gesucht. Zwischen zwei Abfragen wartet es PAUSE Sekunden; der Rundgang lässt sich fortsetzen
(Zwischenstand in <liste>.rundgang.jsonl).

Gebraucht werden nur Findmittel von Beständen, die in scope noch keine Untereinheiten haben (Spalte «noetig»).
Bestände mit Untereinheiten gelten als erschlossen; ihre PDFs stehen nur zur Kontrolle in der Liste.

Die CSV (Semikolon, UTF-8 mit BOM, für Excel) eignet sich auch für findmittel_zu_scope.py --katalog …:
dann gilt die Bestandssignatur aus dem Katalog statt der aus dem PDF gelesenen.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASIS = "https://amsquery.stadt-zuerich.ch/"
WURZEL_ID = 1  # «Stadtarchiv Zürich (Archiv)»
PAUSE = 0.3  # Sekunden zwischen zwei Abfragen
KOPF = {"User-Agent": "Mozilla/5.0 (findmittel_laden.py)"}
# Unterhalb dieser Stufen wird nicht weitergesucht
NICHT_ABSTEIGEN = {"Bestand", "Teilbestand", "Serie", "Teilserie", "Dossier", "Teildossier", "Dokument",
                   "Einzelstück", "Subdossier", "Akte", "Band"}

FELDER = ["ve_id", "signatur", "titel", "stufe", "untereinheiten", "noetig", "datei", "pfad", "url", "bytes",
          "findmittel"]


def hole(url: str, methode: str = "GET", versuche: int = 3) -> tuple[bytes, dict]:
    for n in range(versuche):
        try:
            anfrage = urllib.request.Request(url, headers=KOPF, method=methode)
            with urllib.request.urlopen(anfrage, timeout=60) as antwort:
                return (antwort.read() if methode == "GET" else b""), dict(antwort.headers)
        except (urllib.error.URLError, TimeoutError) as fehler:
            if n + 1 == versuche:
                raise
            print(f"  … {fehler} – neuer Versuch", file=sys.stderr)
            time.sleep(3 * (n + 1))
    raise RuntimeError("unerreichbar")


def feld(seite: str, name: str) -> str:
    m = re.search(rf">{name}:</td>\s*<td[^>]*>(.*?)</td>", seite, re.S)
    return html.unescape(re.sub(r"<[^>]+>|\s+", " ", m.group(1))).strip() if m else ""


def link(seite: str, schluessel: str) -> int | None:
    m = re.search(rf'id="[^"]*_ap_img{schluessel}"\s+href="detail\.aspx\?ID=(\d+)"', seite)
    return int(m.group(1)) if m else None


def lies_ve(ve_id: int) -> dict:
    roh, _ = hole(f"{BASIS}detail.aspx?ID={ve_id}")
    seite = roh.decode("utf-8", errors="replace")
    titel = html.unescape(re.sub(r"\s+", " ", (re.search(r"<title>(.*?)</title>", seite, re.S) or [None, ""])[1]))
    dateien = [{"pfad": p, "datei": html.unescape(n).strip()}
               for p, n in re.findall(r"openDoc\('(Dateien/[^']+)'\);?\"[^>]*>([^<]+)<", seite)]
    return {"ve_id": ve_id, "titel": titel.strip(), "signatur": feld(seite, "Signatur"), "stufe": feld(seite, "Stufe"),
            "kind": link(seite, "UntergeordneterEintrag"), "naechster": link(seite, "NaechsterEintrag"),
            "dateien": dateien}


def rundgang(zwischenstand: Path) -> list[dict]:
    """Archivplan bis zur Stufe Bestand durchgehen; bereits gelesene VE kommen aus dem Zwischenstand."""
    bekannt: dict[int, dict] = {}
    if zwischenstand.exists():
        for zeile in zwischenstand.read_text(encoding="utf-8").splitlines():
            try:
                ve = json.loads(zeile)
            except json.JSONDecodeError:  # beim Abbruch halb geschriebene Zeile
                continue
            bekannt[ve["ve_id"]] = ve
    ausgabe = zwischenstand.open("a", encoding="utf-8")
    besucht: list[dict] = []
    gesehen: set[int] = set()

    def besuche(ve_id: int | None, tiefe: int) -> None:
        while ve_id and ve_id not in gesehen:  # Schutz vor Schleifen in der Navigation
            gesehen.add(ve_id)
            if ve_id in bekannt:
                ve = bekannt[ve_id]
            else:
                ve = lies_ve(ve_id)
                bekannt[ve_id] = ve
                ausgabe.write(json.dumps(ve, ensure_ascii=False) + "\n")
                ausgabe.flush()
                time.sleep(PAUSE)
            besucht.append(ve)
            if len(besucht) % 50 == 0:
                print(f"  {len(besucht)} Einträge gelesen … zuletzt {ve['signatur']} ({ve['stufe']})", flush=True)
            if ve["kind"] and ve["stufe"] not in NICHT_ABSTEIGEN:
                besuche(ve["kind"], tiefe + 1)
            ve_id = ve["naechster"] if tiefe > 0 else None

    wurzel = lies_ve(WURZEL_ID)
    besucht.append(wurzel)
    besuche(wurzel["kind"], 1)
    ausgabe.close()
    return besucht


def liste(ziel: Path) -> None:
    ziel.parent.mkdir(parents=True, exist_ok=True)
    print("Gehe den Archivplan durch (kann einige Minuten dauern) …", flush=True)
    ves = rundgang(ziel.with_suffix(".rundgang.jsonl"))
    zeilen = []
    for ve in ves:
        # Ein Bestand mit Untereinheiten ist in scope schon (zumindest teilweise) erschlossen:
        # sein PDF wird nur aufgeführt, nicht gebraucht (keine Grössenabfrage, kein Download).
        erschlossen = ve["kind"] is not None
        for d in ve["dateien"]:
            if not d["pfad"].lower().endswith(".pdf"):
                continue
            url = BASIS + d["pfad"]
            ist_fm = "findmittel" in d["datei"].lower()
            groesse: int | str = ""
            if not erschlossen:
                try:
                    _, kopf = hole(url, "HEAD")
                    groesse = int(kopf.get("Content-Length", 0) or 0)
                except Exception as fehler:  # Datei fehlt o. Ä. – trotzdem aufführen
                    print(f"  HEAD {url}: {fehler}", file=sys.stderr)
                    groesse = 0
                time.sleep(PAUSE)
            zeilen.append({"ve_id": ve["ve_id"], "signatur": ve["signatur"], "titel": ve["titel"],
                           "stufe": ve["stufe"], "untereinheiten": "ja" if erschlossen else "nein",
                           "noetig": "ja" if (ist_fm and not erschlossen) else "nein",
                           "datei": d["datei"], "pfad": d["pfad"], "url": url, "bytes": groesse,
                           "findmittel": "ja" if ist_fm else "nein"})
    with ziel.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FELDER, delimiter=";")
        w.writeheader()
        w.writerows(zeilen)
    bestaende = [ve for ve in ves if ve["stufe"] == "Bestand"]
    mit_pdf = {z["ve_id"] for z in zeilen}
    noetig = [z for z in zeilen if z["noetig"] == "ja"]
    andere = [z for z in zeilen if z["untereinheiten"] == "nein" and z["findmittel"] == "nein"]
    print(f"{len(ves)} Einträge gelesen, davon {len(bestaende)} Bestände; "
          f"{sum(1 for b in bestaende if b['kind'] is None)} ohne Untereinheiten in scope")
    print(f"Bestände mit PDF: {len(mit_pdf)}; davon schon erschlossen (mit Untereinheiten): "
          f"{len({z['ve_id'] for z in zeilen if z['untereinheiten'] == 'ja'})}")
    print(f"Gebraucht: {len(noetig)} Findmittel-PDFs aus {len({z['ve_id'] for z in noetig})} Beständen, "
          f"zusammen {sum(int(z['bytes'] or 0) for z in noetig) / 1e6:.1f} MB"
          + (f" (dazu {len(andere)} weitere PDFs ohne «Findmittel» im Namen, "
             f"{sum(int(z['bytes'] or 0) for z in andere) / 1e6:.1f} MB)" if andere else ""))
    print(f"-> {ziel}")


def laden(liste_csv: Path, ordner: Path, alle: bool, erschlossene: bool) -> int:
    """Gebrauchte PDFs laden: Findmittel von Beständen ohne Untereinheiten (Optionen erweitern das)."""
    ordner.mkdir(parents=True, exist_ok=True)
    with liste_csv.open(encoding="utf-8-sig") as f:
        zeilen = [z for z in csv.DictReader(f, delimiter=";")
                  if (alle or z["findmittel"] == "ja") and (erschlossene or z["untereinheiten"] == "nein")]
    fehler = 0
    for nr, z in enumerate(zeilen, start=1):
        ziel = ordner / Path(z["pfad"]).name
        if ziel.exists() and str(ziel.stat().st_size) == z["bytes"]:
            continue
        try:
            daten, _ = hole(z["url"])
            ziel.write_bytes(daten)
        except Exception as ex:
            fehler += 1
            print(f"  FEHLER {z['url']}: {ex}", file=sys.stderr)
        if nr % 25 == 0:
            print(f"  {nr}/{len(zeilen)} …", flush=True)
        time.sleep(PAUSE)
    print(f"{len(zeilen) - fehler} von {len(zeilen)} Dateien in {ordner}")
    return 1 if fehler else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Findmittel-PDFs des Stadtarchivs Zürich auflisten und laden")
    ap.add_argument("--liste", type=Path, required=True, help="CSV mit allen Beständen und PDFs (wird erzeugt, "
                                                              "falls sie fehlt)")
    ap.add_argument("--laden", type=Path, help="Zielordner: PDFs aus der Liste herunterladen")
    ap.add_argument("--alle-pdf", action="store_true", help="auch PDFs laden, die nicht «Findmittel…» heissen")
    ap.add_argument("--auch-erschlossene", action="store_true",
                    help="auch PDFs von Beständen laden, die in scope schon Untereinheiten haben")
    args = ap.parse_args()
    if not args.liste.exists() or not args.laden:
        liste(args.liste)
    if args.laden:
        return laden(args.liste, args.laden, args.alle_pdf, args.auch_erschlossene)
    return 0


if __name__ == "__main__":
    sys.exit(main())
