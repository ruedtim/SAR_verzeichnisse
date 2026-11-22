#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pdfplumber>=0.11",
#     "openpyxl>=3.1",
# ]
# ///
"""Findmittel-PDF (Stadtarchiv Zürich, Word-Export) -> Excel-Tabelle für den scope-Import.

Aufruf
    uv run findmittel_zu_scope.py D151210.pdf
    uv run findmittel_zu_scope.py D151210.pdf -o VII.200_scope_import.xlsx --bestand VII.200.
    uv run findmittel_zu_scope.py pdf_ordner/ -o excel_ordner/          # alle PDFs eines Ordners
    uv run findmittel_zu_scope.py findmittel_pdf/ -o excel/ --katalog findmittel_pdf/verzeichnis.csv
        (Liste aus findmittel_laden.py: Bestandssignatur aus dem Online-Archiv zur Kontrolle bzw. als Ersatz)
    ohne uv:  pip install pdfplumber openpyxl   und dann   python findmittel_zu_scope.py …

Gedacht für die Findmittel des Stadtarchivs im Aufbau «Signatur links, Beschreibung rechts».
Erkannt werden diese Gliederungen:
    dezimal          1. / 2.1. / 2.1.1.               (z. B. VII.200., VII.212., VII.12.)
    Vollsignatur     VI.HO.A.1. / VI.HO.B.1.:1 / …A.1.-8.  (Signatur samt Bestand in der linken Spalte,
                     auch mit Leerzeichen/Tippfehlern: «V.K. c.4.:1», «VII. 121.:1», «V.E..c.11.:6»)
    Buchstabe+Nr.    A / B 3 / B 27                    (z. B. VII.267.)
    Gliederung       I. > A. > a) > 1. / 1.a.          (z. B. VII.179.; Signaturen werden aus der
                                                        Gliederung gebildet – bitte prüfen)
    fortlaufend      1 / 2 / 3, auch mit Lücken «22, 29, 30» und als «Jahr.Laufnummer» «1941.1» (VII.308.)
Eine Spalte mit blossen Zahlen am rechten Rand wird als Schachtel-Nr. gelesen, wenn ein Spaltenkopf
«Schachtel» darüber steht oder das Vorwort sie so erklärt. Findmittel ganz ohne Signaturen (reine Listen,
nach Mappen/Schachteln gegliederte Listen) und Scans ohne Textebene meldet das Skript als «Fehler».

Was das Skript macht
    1. Liest jede Zeile mit Koordinaten und Schrift (pdfplumber). Kopf- und Fusszeilen fallen weg,
       eine Datumsspalte («… 1890-1916» rechts) und Umfangsangaben («4 Bände») werden erkannt.
    2. Erkennt Signaturen nur in der linken Spalte. Datumsreste wie «19. Juni 1947», die beim
       Umbruch dorthin rutschen, gelten als Text; ebenso fehlende oder abgetrennte Schlusspunkte.
    3. Baut die Hierarchie. Kommt eine Signatur mehrfach vor (mehrere Schachteln/Einheiten mit
       derselben Nummer), werden die weiteren Nennungen «Teile» der ersten, ebenso «…, Teil 3».
    4. Trennt Titel und Darin, flickt Zeilenumbrüche (auch verschobene Namen in Rollenbuch- und
       Fotolisten), liest den Zeitraum aus Datumsspalte oder Titel, sonst aus Inhaltsverzeichnis,
       Untereinheiten, übergeordneter Einheit oder (geschätzt) aus dem Darin.
    5. Prüft die Vollständigkeit: jedes Wort des Detailverzeichnisses muss in der Excel-Zeile seiner
       Einheit wieder vorkommen (Titel, Darin, von/bis, Anmerkung, Umfang, Schachtel). Lücken und bewusst
       nicht übernommene Zeilen (Überschriften ohne Signatur u. Ä.) stehen im Blatt «Vollständigkeit».
    6. Schreibt pro PDF eine Excel-Datei mit den Blättern «scope-Import», «Prüfliste», «Vollständigkeit»
       und «Info»; bei mehreren PDFs zusätzlich «uebersicht_scope_import.xlsx» (mit «Text erfasst»).
       Alles, was ein Mensch ansehen sollte, steht in der Spalte «Prüfhinweise».

Die Einstellungen unten (Stufen, Datumsoperatoren …) bei Bedarf an die scope-Vorlage anpassen.
Exit-Codes: 0 = alles OK, 1 = einzelne PDFs fehlgeschlagen, 2 = ungültige Eingabe.
"""
from __future__ import annotations

import argparse
import bisect
import datetime as dt
import json
import os
import re
import sys
import traceback
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# ----------------------------------------------------------------------------- Einstellungen

SIGNATUR_SPALTE_MAX = 115.0  # pt: Signaturen beginnen links davon, der Text ab ca. 125 pt
SIGNATUR_SPALTE_MAX_GLIEDERUNG = 130.0  # bei I./A./a)/1.-Gliederungen sind die Stufen eingerückt
ABSATZ_ABSTAND = 7.5  # pt Leerraum zwischen zwei Zeilen, ab dem ein neuer Absatz beginnt (Word «6 pt nach» = 7,8 pt)
SPALTEN_LUECKE = 18.0  # pt Lücke vor einer Datums-/Umfangsspalte am rechten Rand
# Schachtelnummer, auch als Bereich oder Paar: «33», «80a», «33-34», «80a & 80b» (Spalte «Schachtel-Nr.», V.G.c.7.)
SCHACHTEL_NR_RE = re.compile(r"\d{1,4}[a-z]?(?:-\d{1,4}[a-z]?)?")
SCHACHTEL_PAAR_RE = re.compile(r"\d{1,4}[a-z]?\s*(?:[-–&/,]|und)\s*\d{1,4}[a-z]?")
FUSSZEILE_AB = 780.0  # pt: alles darunter ist Fusszeile
TITEL_MAX = 160  # längere Titel werden – wenn möglich – beim ersten «: » geteilt
DARIN_MAX = 30000  # Zeichen; längeres Darin wird auf Teile verteilt (Excel-Grenze 32 767)

STUFE_TIEFE_1 = "Teilbestand"  # oberste Gliederungsebene (1., 2. … bzw. I., II. bzw. A, B …)
STUFE_GRUPPE = "Serie"  # Einheiten mit Untereinheiten oder Teilen
STUFE_EINHEIT = "Dossier"  # Einheiten ohne Untereinheiten und alle «Teile»

# Wortlaut der Datumsoperatoren wie in der StAZH-Erfassungsvorlage (Spalte «Entstehungszeitraum»)
OP_GENAU = "Genau (=)"
OP_VON_BIS = "Von/bis (>= x und <=y)"

TITEL_OHNE_ZEITRAUM = True  # «Verträge 1925–1935» -> Titel «Verträge», Zeitraum 1925–1935
TEIL_IM_TITEL = True  # übernommene Titel von Teilen bekommen «, Teil n»
# Eindeutige Signaturen für Teile, z. B. "{sig}-{teil}" ergäbe «VII.200.:6.1.-3».
# None = Signatur wie im PDF (Teile teilen sich dann die Signatur, eindeutig ist die ID).
SIGNATUR_TEIL_MUSTER: str | None = None

# ----------------------------------------------------------------------------- PDF lesen


@dataclass
class Wort:
    text: str
    x0: float
    x1: float
    font: str
    size: float


@dataclass
class Zeile:
    seite: int
    top: float
    bottom: float
    worte: list[Wort]
    datum: str = ""  # Text aus der Datumsspalte rechts («1890-1916»)
    umfang: str = ""  # «1 Schachtel», «4 Bände»
    schachtel: str = ""  # «Schachtel 301» am rechten Rand
    spalten: str = ""  # weitere Tabellenspalten («Fach 170, Mappe 334, Allg. Nr. 2111», teile_tabellenspalten)

    @property
    def x0(self) -> float:
        return self.worte[0].x0

    @property
    def x1(self) -> float:
        return self.worte[-1].x1

    @property
    def text(self) -> str:
        if not any(w.text == "-" for w in self.worte):
            return " ".join(w.text for w in self.worte)
        # ein Bindestrich, der als eigenes Wort ohne Abstand an Buchstaben hängt, gehört zum Wort («„Tages» «-»
        # «Anzeiger“» → «„Tages-Anzeiger“», «„Bauschreck» «-» am Zeilenende, VII.12.B.)
        teile = [self.worte[0].text]
        for k in range(1, len(self.worte)):
            a, b = self.worte[k - 1], self.worte[k]
            haengt = (b.text == "-" and b.x0 - a.x1 < 0.6 and a.text[-1:].isalpha()
                      and (k + 1 == len(self.worte) or (self.worte[k + 1].x0 - b.x1 < 0.6
                                                         and self.worte[k + 1].text[:1].isalpha()))) \
                or (a.text == "-" and k >= 2 and b.x0 - a.x1 < 0.6 and b.text[:1].isalpha()
                    and a.x0 - self.worte[k - 2].x1 < 0.6 and self.worte[k - 2].text[-1:].isalpha())
            teile.append(("" if haengt else " ") + b.text)
        return "".join(teile)

    def text_mit_luecken(self, luecke: float = 15.0) -> str:
        """Wie text, aber grosse horizontale Lücken (Tabulatoren, Datumsspalte) als « ¦ »."""
        teile = [self.worte[0].text]
        for a, b in zip(self.worte, self.worte[1:]):
            teile.append(" ¦ " if b.x0 - a.x1 > luecke else " ")
            teile.append(b.text)
        return "".join(teile)

    def ab(self, n: int) -> "Zeile | None":
        """Zeile ohne die ersten n Wörter (None, wenn nichts übrig bleibt)."""
        if n >= len(self.worte):
            return None
        return Zeile(self.seite, self.top, self.bottom, self.worte[n:], self.datum, self.umfang, self.schachtel,
                     self.spalten)


def lese_zeilen(pdf_pfad: Path) -> tuple[list[Zeile], dict]:
    import pdfplumber

    zeilen: list[Zeile] = []
    with pdfplumber.open(pdf_pfad) as pdf:
        meta = {k: str(v) for k, v in (pdf.metadata or {}).items() if isinstance(v, (str, int, float))}
        meta["Seiten"] = len(pdf.pages)
        for nr, seite in enumerate(pdf.pages, start=1):
            woerter = seite.extract_words(extra_attrs=["fontname", "size"], x_tolerance=1.5, y_tolerance=2)
            woerter.sort(key=lambda w: (w["top"], w["x0"]))
            gruppen: list[list[dict]] = []
            for w in woerter:
                if gruppen and abs(gruppen[-1][0]["top"] - w["top"]) <= 2.5:
                    gruppen[-1].append(w)
                else:
                    gruppen.append([w])
            for g in gruppen:
                g.sort(key=lambda w: w["x0"])
                zeilen.append(Zeile(
                    seite=nr,
                    top=round(min(w["top"] for w in g), 1),
                    bottom=round(max(w["bottom"] for w in g), 1),
                    worte=[Wort(w["text"], round(w["x0"], 1), round(w["x1"], 1), w["fontname"], round(w["size"], 1))
                           for w in g],
                ))
    return zeilen, meta


def ocr_zeilen(pdf_pfad: Path) -> list[Zeile]:
    """Texterkennung für gescannte Seiten (pdftoppm + tesseract, Deutsch); leer, wenn die Werkzeuge fehlen.
    Koordinaten in pt wie bei pdfplumber; die Schriftgrösse wird aus der Wortgrösse geschätzt."""
    import shutil
    import subprocess
    import tempfile

    if not (shutil.which("pdftoppm") and shutil.which("tesseract")):
        return []
    dpi, zeilen = 300, []
    faktor = 72 / dpi
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf_pfad), f"{tmp}/s"], check=True, capture_output=True)
        for bild in sorted(Path(tmp).glob("s-*.png"), key=lambda b: int(b.stem.rsplit("-", 1)[1])):
            seite = int(bild.stem.rsplit("-", 1)[1])
            tsv = subprocess.run(["tesseract", str(bild), "stdout", "-l", "deu", "--psm", "4", "tsv"],
                                 capture_output=True, text=True).stdout
            gruppen: dict[tuple, list] = {}
            for satz in tsv.splitlines()[1:]:
                feld_ = satz.split("\t")
                if len(feld_) < 12 or not feld_[11].strip():
                    continue
                sicher, text = float(feld_[10]), feld_[11].strip()
                if sicher < 20 or (sicher < 50 and not re.search(r"\w", text)):
                    continue  # Störzeichen
                links, oben, breite, hoehe = (int(x) for x in feld_[6:10])
                gruppen.setdefault((feld_[2], feld_[3], feld_[4]), []).append((links, oben, breite, hoehe, text))
            for woerter in gruppen.values():
                groesse = round(sorted(h for _, _, _, h, _ in woerter)[len(woerter) // 2] * faktor / 0.72, 1)
                woerter.sort()
                zeilen.append(Zeile(seite, round(min(o for _, o, _, _, _ in woerter) * faktor, 1),
                                    round(max(o + h for _, o, _, h, _ in woerter) * faktor, 1),
                                    [Wort(t, round(l * faktor, 1), round((l + b) * faktor, 1), "OCR", groesse)
                                     for l, _, b, _, t in woerter]))
    zeilen.sort(key=lambda z: (z.seite, z.top, z.x0))
    return zeilen


STRICHE = str.maketrans({"‒": "–", "−": "–", "‐": "-", "‑": "-"})  # Ziffern-, Minus- und Trennstriche vereinheitlichen


ZIFFERN_L_RE = re.compile(r"[\dl.,:;/–\-()]*\d[\dl.,:;/–\-()]*")  # «l935-l983», «20l:» (kleines L statt Eins)


def _normalisiere(zeilen: list[Zeile]) -> list[Zeile]:
    """Striche vereinheitlichen, «l» in Zahlen zu «1», und zerrissene Wörter zusammenfügen: Wörter ohne Abstand
    (< 0,5 pt) sind optisch eines – getrennt hat sie ein Schriftwechsel mitten im Wort («S» + kursiv «iehe»)
    oder die Zeichenfolge im PDF («Liegenschaftenverwaltu» + «ng», «D» + «etailverzeichnis»)."""
    for z in zeilen:
        neu: list[Wort] = []
        for w in z.worte:
            w.text = w.text.translate(STRICHE)
            if "l" in w.text and ZIFFERN_L_RE.fullmatch(w.text):  # nicht «5.6.13.l.» (Buchstabe als Stufe)
                w.text = re.sub(r"(?<=\d)l|l(?=\d)|^l(?=[-–]\d)", "1", w.text)
            # Aufzählungszeichen und freistehende Striche bleiben eigene Wörter («-Die Irre …», «A – Z»)
            if neu and -1.0 <= w.x0 - neu[-1].x1 < 0.5 and z.worte[0].font != "OCR" \
                    and neu[-1].text not in AUFZAEHLUNG and w.text not in AUFZAEHLUNG:
                a = neu[-1]
                lang = a if len(a.text) >= len(w.text) else w
                neu[-1] = Wort(a.text + w.text, a.x0, max(a.x1, w.x1), lang.font, lang.size)
            else:
                neu.append(w)
        z.worte = neu
    return zeilen


def lade_oder_lese(pdf_pfad: Path, cache_ordner: Path | None) -> tuple[list[Zeile], dict]:
    zeilen, meta = _lade_oder_lese(pdf_pfad, cache_ordner)
    return _normalisiere(zeilen), meta


def _lade_oder_lese(pdf_pfad: Path, cache_ordner: Path | None) -> tuple[list[Zeile], dict]:
    """Zeilen aus dem PDF lesen; mit --cache werden sie als JSON zwischengespeichert. Hat das PDF (fast) keine
    Textebene, wird es per Texterkennung gelesen (meta «OCR»)."""
    cache = cache_ordner / f"{pdf_pfad.stem}.zeilen.json" if cache_ordner else None
    zeilen: list[Zeile] | None = None
    if cache and cache.exists() and cache.stat().st_mtime >= pdf_pfad.stat().st_mtime:
        roh = json.loads(cache.read_text(encoding="utf-8"))
        zeilen = [Zeile(z["seite"], z["top"], z["bottom"], [Wort(*w) for w in z["worte"]]) for z in roh["zeilen"]]
        meta = roh["meta"]
        if meta.get("OCR") or sum(len(z.text) for z in zeilen) >= 300:
            return zeilen, meta
    if zeilen is None:
        zeilen, meta = lese_zeilen(pdf_pfad)
    if sum(len(z.text) for z in zeilen) < 300:  # Scan: Text nur in Kopf-/Fusszeile oder gar nicht
        erkannt = ocr_zeilen(pdf_pfad)
        if sum(len(z.text) for z in erkannt) > sum(len(z.text) for z in zeilen):
            zeilen, meta = erkannt, {**meta, "OCR": "tesseract (deu)"}
    if cache:
        cache_ordner.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({"meta": meta, "zeilen": [
            {"seite": z.seite, "top": z.top, "bottom": z.bottom,
             "worte": [[w.text, w.x0, w.x1, w.font, w.size] for w in z.worte]} for z in zeilen]},
            ensure_ascii=False), encoding="utf-8")
    return zeilen, meta


FUSSZEILE_RE = re.compile(r"\d\d\.\d\d\.\d\d(?:\d\d)?\s*/\s*Seite\s+\d+|©\s*Stadtarchiv|\bSeite\s+\d+(?:\s+von\s+\d+)?\s*$"
                          r"|^\d\d\.\d\d\.\d{2,4}\s*/\s*\d{1,3}\s*/")  # «17.10.2007/3/Dr. Nicola Behrens …»


def verbinde_versetzte_nummern(zeilen: list[Zeile]) -> list[Zeile]:
    """Nummer allein auf einer Zeile, ihr Titel wenige Punkte tiefer in gleicher Schrift: eine Zeile («3.» bei 414 /
    «Werbematerial» bei 420, V.L.121.)."""
    neu: list[Zeile] = []
    k = 0
    while k < len(zeilen):
        z = zeilen[k]
        n = zeilen[k + 1] if k + 1 < len(zeilen) else None
        if n is not None and len(z.worte) == 1 and re.fullmatch(r"\d{1,3}(?:\.\d{1,3})*\.", z.worte[0].text) \
                and n.seite == z.seite and 2.5 < n.top - z.top <= 8 and n.x0 > z.worte[0].x1 + 10 \
                and abs(n.worte[0].size - z.worte[0].size) < 0.6 and not (z.datum or z.schachtel):
            neu.append(Zeile(z.seite, z.top, max(z.bottom, n.bottom), z.worte + n.worte, n.datum, n.umfang,
                             n.schachtel, n.spalten))
            k += 2
            continue
        neu.append(z)
        k += 1
    return neu


def richte_teilsignaturen(zeilen: list[Zeile]) -> list[Zeile]:
    """Signatur eine Zeile über ihrem «Teil n» (VII.200. 8.1.1.44.): «8.1.1.44. Don Carlos …» / «Teil 2» und
    «Der Kirschgarten von Anton Tschechow 8.1.1.44.» / «Teil 3» – die Signatur gehört zur Zeile «Teil n», der Text
    davor ist ein Eintrag des vorigen Teils. Nur wenn dieselbe Signatur sonst mit «Teil n» auf einer Zeile steht."""
    sig_re = re.compile(r"\d{1,3}(?:\.\d{1,4})+\.")
    mit_teil = {z.worte[0].text for z in zeilen if len(z.worte) >= 3 and sig_re.fullmatch(z.worte[0].text)
                and TEIL_NUR_RE.match(" ".join(w.text for w in z.worte[1:]))}
    neu = list(zeilen)
    for k in range(len(neu) - 1):
        z, n = neu[k], neu[k + 1]
        m_n = TEIL_NUR_RE.match(n.text.strip()) if z.worte and n.worte and n.seite == z.seite else None
        if not m_n or int(m_n.group(1)) < 2:
            continue  # («8.1.1.45. Fotos der Aufführungen …» / «Teil 1»: Überschrift und erster Teil, richtig)
        if len(z.worte) >= 2 and z.worte[0].text in mit_teil and not TEIL_NUR_RE.match(z.ab(1).text.strip()):
            sig, rest = z.worte[0], z.worte[1:]
        elif len(z.worte) >= 2 and z.worte[-1].text in mit_teil and z.worte[-1].x0 > z.worte[-2].x1:
            sig, rest = z.worte[-1], z.worte[:-1]
        else:
            continue
        neu[k] = Zeile(z.seite, z.top, z.bottom, rest, z.datum, z.umfang, z.schachtel, z.spalten)
        neu[k + 1] = Zeile(n.seite, n.top, n.bottom, [Wort(sig.text, min(sig.x0, n.x0 - 50), min(sig.x0, n.x0 - 50)
                                                          + (sig.x1 - sig.x0), sig.font, sig.size)] + n.worte,
                           n.datum, n.umfang, n.schachtel, n.spalten)
    return neu


def ist_kopf_oder_fuss(z: Zeile) -> bool:
    klein = all(w.size <= 10.5 for w in z.worte)
    # unten nur kleine Schrift bzw. typische Fusszeilen – manche Findmittel sind bis 830 pt bedruckt (VII.374.)
    if (z.top >= FUSSZEILE_AB and (klein or FUSSZEILE_RE.search(z.text))) or (klein and z.top < 70):
        return True  # Fusszeile bzw. Kopfzeile «VII. 143. … Seite 2»
    if klein and FUSSZEILE_RE.search(z.text):
        return True
    if z.top < 80 and re.search(r"\bSeite\s+\d+(?:\s+von\s+\d+)?\s*$", z.text) and len(z.text) < 120:
        return True  # Kopfzeile in Textgrösse «V.C. c.75. Büro für Wohnbauförderung Seite 2»
    # verirrte Kleinst-Schnipsel wie eine einzelne «31» in 10 pt am rechten Rand (nicht «1675» als letzte Zeile
    # einer Anmerkung in der Textspalte, VII.494.)
    return klein and re.fullmatch(r"[\d.\s]+", z.text) is not None and z.x0 >= 400


def rechter_rand(zeilen: list[Zeile]) -> float:
    """Rechter Rand des Satzspiegels (98. Perzentil der Zeilenenden)."""
    enden = sorted(z.x1 for z in zeilen if z.x1 < 590)
    return enden[int(len(enden) * 0.98)] if enden else 556.0


# ----------------------------------------------------------------------------- Datumslogik

MONATE = {
    "jan": 1, "januar": 1, "feb": 2, "febr": 2, "februar": 2, "märz": 3, "maerz": 3, "mär": 3,
    "apr": 4, "april": 4, "mai": 5, "jun": 6, "juni": 6, "jul": 7, "juli": 7, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "nov": 11, "november": 11,
    "dez": 12, "dezember": 12, "december": 12, "may": 5,
}
MONAT_MUSTER = (r"(?:Januar|Jan\.?|Februar|Febr\.?|Feb\.?|März|Maerz|April|Apr\.?|Mai|May|Juni|Jun\.?|Juli|Jul\.?"
                r"|August|Aug\.?|September|Sept\.?|Sep\.?|Oktober|Okt\.?|November|Nov\.?|Dezember|December"
                r"|Dez\.?)")
MONAT_WORT_RE = re.compile(rf"^{MONAT_MUSTER}[.,]?$")
JAHR = r"(?:1[2-9]\d\d|20[0-2]\d)"  # bis 2029: «Nr. 2037» ist kein Jahr
PUNKT_RE = re.compile(
    # «9. – 13. Juni 1986», «27. Juli – 15. August 1986», «19. / 20. April 1959»
    rf"(?<![\d.])(?P<bt1>\d{{1,2}})(?:\.\s?|\s)(?:(?P<bm1>{MONAT_MUSTER})\s?)?[/–-]\s?(?P<bt2>\d{{1,2}})\.\s?"
    rf"(?P<bm2>{MONAT_MUSTER})\s?(?P<bj>{JAHR})(?!\d)"
    # «April – Dez. 1936», «Juni – August 1943» (Monat bis Monat eines Jahres)
    rf"|(?<![\w.])(?P<mb1>{MONAT_MUSTER})\s?[/–-]\s?(?P<mb2>{MONAT_MUSTER})\s?(?P<mj>{JAHR})(?!\d)"
    # «15.1./4.3.1824», «11.6.-27.2.1965»
    rf"|(?<![\d.])(?P<nt1>\d{{1,2}})\.\s?(?P<nm1>\d{{1,2}})\.\s?[/–-]\s?(?P<nt2>\d{{1,2}})\.\s?(?P<nm2>\d{{1,2}})\.\s?"
    rf"(?P<nj>{JAHR})(?!\d)"
    rf"|(?<![\d.])(?P<t1>\d{{1,2}})\.\s?(?P<m1>\d{{1,2}})\.\s?(?P<j1>{JAHR})(?!\d)"
    rf"|(?:(?<![\d.])(?P<t2>\d{{1,2}})\.\s?)?(?P<mon>{MONAT_MUSTER})\s?(?P<j2>{JAHR})(?!\d)"
    rf"|(?<![\d/.])(?P<jz>1[2-9]\d0|20[0-4]0)er(?:\s?Jahren?|\s?Jahre)?(?!\w)"
    # «02.1934» (Monat.Jahr)
    rf"|(?<![\d.])(?P<mm>0?[1-9]|1[0-2])\.(?P<j4>{JAHR})(?![\d.])"
    # «1938/39», «1950/71», «1987 - 88» (Endjahr zweistellig)
    rf"|(?:(?<=ca\.)|(?<![\d/.]))(?P<j3>{JAHR})(?:/\s?(?P<j3b>\d{{4}}|\d{{2}})(?!\d)|\s/\s?(?P<j3d>\d{{2}})(?!\d)"
    rf"|\s?[–-]\s?(?P<j3c>\d{{2}})(?![\d.]))?(?![\d/])"
)
VERBINDER_BEREICH_RE = re.compile(r"^\.?\s*(?:[–—-]|bis(?:\s+(?:zum|zur|am|an|in|im|Ende))?)\s*$")
VERBINDER_LISTE_RE = re.compile(r"^\s*(?:,|und|u\.|sowie|/)\s*$")
VORSATZ_RE = re.compile(r"(?:^|\s)(ab|seit|nach|bis|vor|ca\.|um|circa|zirka)(?:\s+|(?<=ca\.))(?:(ca\.)\s*)?$", re.I)
EREIGNIS_RE = re.compile(r"(?:^|\s)(vom|am)\s+$", re.I)
NICHT_JAHR_VOR_RE = re.compile(r"(?:Nr\.?|Nrn\.?|No\.?|Sign\.?|Seite|S\.|Bd\.|Heft|Tel\.?|Mappe|Fach|Schachtel|Ass\.)\s*$")
LEBENSDATEN_RE = re.compile(r"^\s*(?:geb\.|gest\.|\*|†)|^\s*\d{4}\s*[–-]\s*\d{4}\s*$")
# Lebensdaten einer Person im Titel: «(1865)», «(geb. 1865)», «(1865–1932)», auch nur das Todesjahr «(-1838)» bzw.
# das Geburtsjahr «(1765-)» («Ludwig Heinrich Friedrich von Podewils (-1838)», VII.388.)
PERSON_RE = re.compile(r"\((?:geb\.|gest\.|\*|†|[–-])?\s*(?:ca\.\s*)?\d{4}\s*(?:[–-]\s*(?:(?:ca\.\s*)?\d{4})?)?\s*\)")
# nur eindeutige Lebensdaten – sie zählen gar nicht als Datum des Titels (ein blosses «(1937)» kann das Datum der
# Unterlagen sein und bleibt Ereignisdatum)
LEBENSDATEN_KLAMMER_RE = re.compile(r"\((?:(?:geb\.|gest\.|\*|†)\s*(?:ca\.\s*)?\d{4}|[–-]\s*\d{4}|\d{4}\s*[–-])\s*\)")
UNDATIERT_RE = re.compile(r"\b(undatiert|o\.\s?J\.|o\.\s?D\.|ohne Datum|s\.\s?d\.)", re.I)


@dataclass(frozen=True)
class Datum:
    jahr: int
    monat: int | None = None
    tag: int | None = None

    def text(self) -> str:
        if self.tag and self.monat:
            return f"{self.tag:02d}.{self.monat:02d}.{self.jahr}"
        if self.monat:
            return f"{self.monat:02d}.{self.jahr}"
        return str(self.jahr)

    def schluessel(self, ende: bool = False) -> tuple:
        """Vergleichswert; beim Ende zählt ein Jahr als 31.12."""
        if ende:
            return (self.jahr, self.monat or 12, self.tag or 31)
        return (self.jahr, self.monat or 1, self.tag or 1)


@dataclass
class Zeitraum:
    von: Datum | None
    bis: Datum | None
    original: str = ""  # Ausdruck wie im PDF, z. B. «1938/39–1950/51»
    ca: bool = False
    ereignis: bool = False  # «vom 23. Febr. 1947» beschreibt ein Ereignis, nicht die Laufzeit
    start: int = 0
    ende: int = 0

    @property
    def anmerkung_noetig(self) -> bool:
        """Sagt der Originalausdruck mehr als von/bis? (Spielzeiten, Listen, ab/bis/ca., offenes Ende)"""
        o = self.original
        abgedeckt = {str(x) for d in (self.von, self.bis) if d for x in (d.jahr, d.jahr % 100, d.monat, d.tag) if x}
        return bool(self.ca or not (self.von and self.bis) or re.search(r"\d\s?/\s?\d|\((?:I{1,3}|IV)\)|\d{2}er\b", o)
                    or re.search(r",|\bund\b|\bu\.|\bab\b|\bseit\b|\bff\.?|[–-]\s*$", o)
                    or {str(int(n)) for n in re.findall(r"\d+", o)} - abgedeckt)


TAGE_IM_MONAT = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _datum(jahr: str, monat: int | str | None = None, tag: str | None = None) -> Datum | None:
    m = MONATE.get(monat.rstrip(".").lower()) if isinstance(monat, str) else monat
    t = int(tag) if tag else None
    if m is not None and not 1 <= m <= 12:
        return None
    if t is not None and m and not 1 <= t <= TAGE_IM_MONAT[m - 1] + (m == 2):
        t = None  # «31. Juni»: Tag gibt es nicht – nur der Monat zählt (Wortlaut steht in der Anmerkung)
    return Datum(int(jahr), m, t if m else None)


def _punkt(m: re.Match) -> tuple[Datum, Datum] | None:
    """Ein Datumspunkt als (Beginn, Ende); eine Spielzeit «1938/39» reicht von 1938 bis 1939."""
    try:
        if m.group("bj"):
            a = _datum(m.group("bj"), m.group("bm1") or m.group("bm2"), m.group("bt1"))
            b = _datum(m.group("bj"), m.group("bm2"), m.group("bt2"))
            return (a, b) if a and b else None
        if m.group("mj"):
            a = _datum(m.group("mj"), m.group("mb1"))
            b = _datum(m.group("mj"), m.group("mb2"))
            return (a, b) if a and b and a.schluessel() <= b.schluessel() else None
        if m.group("nj"):
            a = _datum(m.group("nj"), int(m.group("nm1")), m.group("nt1"))
            b = _datum(m.group("nj"), int(m.group("nm2")), m.group("nt2"))
            return (a, b) if a and b else None
        if m.group("j1"):
            d = _datum(m.group("j1"), int(m.group("m1")), m.group("t1"))
            return (d, d) if d else None
        if m.group("j2"):
            d = _datum(m.group("j2"), m.group("mon"), m.group("t2"))
            return (d, d) if d else None
        if m.group("jz"):  # «1960er Jahre» = 1960–1969
            return Datum(int(m.group("jz"))), Datum(int(m.group("jz")) + 9)
        if m.group("j4"):  # «02.1934»
            d = _datum(m.group("j4"), int(m.group("mm")))
            return (d, d) if d else None
        j = int(m.group("j3"))
        if m.group("j3b") or m.group("j3c") or m.group("j3d"):
            b = m.group("j3b") or m.group("j3c") or m.group("j3d")
            ende = j // 100 * 100 + int(b) if len(b) == 2 else int(b)
            if len(b) == 2 and ende < j:
                ende += 100  # «1999/00»: nur als Spielzeit über die Jahrhundertgrenze, nicht «1938/37»
                if ende > j + 2:
                    return None
            if not (j <= ende <= j + 99):  # «1938/39» (Spielzeit), «1950/71» (= 1950–1971)
                return None
            return Datum(j), Datum(ende)
        return Datum(j), Datum(j)
    except (ValueError, TypeError):
        return None


def _klammer_bereiche(text: str) -> list[tuple[int, int]]:
    bereiche, stapel = [], []
    for i, c in enumerate(text):
        if c == "(":
            stapel.append(i)
        elif c == ")" and stapel:
            bereiche.append((stapel.pop(), i))
    return bereiche


def finde_zeitraeume(text: str, klammern_ignorieren: bool = True) -> list[Zeitraum]:
    """Alle Zeitausdrücke eines Textes, zusammenhängende (1938–1947, 1995 und 1997) gruppiert."""
    klammern = _klammer_bereiche(text)
    treffer = []
    for m in PUNKT_RE.finditer(text):
        if NICHT_JAHR_VOR_RE.search(text[max(0, m.start() - 9):m.start()]):
            continue
        if re.match(r"\s*[x×]\s*\d", text[m.end():m.end() + 6]) \
                or re.search(r"\d\s*[x×]\s*$", text[max(0, m.start() - 8):m.start()]):
            continue  # Massangabe «1260 x 891» (Format der Planmappen in mm, V.G.c.42.), keine Jahreszahl
        in_klammer = next(((a, b) for a, b in klammern if a < m.start() < b), None)
        if in_klammer:
            inhalt = text[in_klammer[0] + 1:in_klammer[1]]
            if LEBENSDATEN_RE.search(inhalt):
                continue
            # Klammern mitten im Titel enthalten fast immer Lebensdaten o. Ä.
            am_ende = text[in_klammer[1] + 1:].strip(" .:,") == ""
            if klammern_ignorieren and not am_ende:
                continue
        p = _punkt(m)
        if p:
            treffer.append((m, p))
    gruppen: list[list] = []
    for m, p in treffer:
        if gruppen:
            zwischen = text[gruppen[-1][-1][0].end():m.start()]
            if VERBINDER_BEREICH_RE.match(zwischen) or VERBINDER_LISTE_RE.match(zwischen):
                gruppen[-1].append((m, p))
                continue
        gruppen.append([(m, p)])
    ergebnisse = []
    for g in gruppen:
        start, ende = g[0][0].start(), g[-1][0].end()
        davor = text[max(0, start - 12):start]
        vorsatz = VORSATZ_RE.search(davor)
        art, ca = "", False
        if vorsatz:
            start = start - len(davor) + vorsatz.start(1)
            art = vorsatz.group(1).lower()
            ca = art in ("ca.", "um", "circa", "zirka") or bool(vorsatz.group(2))
        # offenes Ende: «2005-», «2005 bis», «2005 bis heute», «1970 ff.» (V.L.5., V.L.105.)
        m_offen = re.match(r"^\s*(?:[–—-](?=\s*(?![\d\w]))|bis(?:\s+heute)?(?=\s*(?:$|[,;)\]]))|ff\.?(?=\s*(?:$|[,;)\]])))",
                           text[ende:]) if len(g) == 1 else None
        offen = m_offen is not None
        if offen:
            ende = ende + len(m_offen.group(0))
        anfaenge = [p[0] for _, p in g]
        enden = [p[1] for _, p in g]
        von = min(anfaenge, key=lambda d: d.schluessel())
        bis = max(enden, key=lambda d: d.schluessel(ende=True))
        einzeln = len(g) == 1
        if art in ("ab", "seit") and einzeln:  # «ab 1938»; «ab 1922 bis 1972» bleibt ein Bereich
            bis = None
        elif art == "bis" and einzeln:
            von = None
        if offen:
            bis = None
        ereignis = (einzeln and anfaenge[0].tag is not None and anfaenge[0] == enden[0]
                    and EREIGNIS_RE.search(text[max(0, start - 6):start]) is not None)
        # «… vor 1938», «nach 1945» beschreiben den Inhalt, nicht die Laufzeit der Unterlagen
        ereignis = ereignis or (art in ("vor", "nach") and einzeln)
        ergebnisse.append(Zeitraum(von, bis, text[start:ende].strip(), ca=ca, ereignis=ereignis,
                                   start=start, ende=ende))
    return ergebnisse


def vereinige(zeitraeume: list[Zeitraum]) -> Zeitraum | None:
    """Kleinster Beginn und grösstes Ende mehrerer Zeiträume."""
    zr = [z for z in zeitraeume if z and (z.von or z.bis)]
    if not zr:
        return None
    vons = [z.von for z in zr if z.von]
    biss = [z.bis or z.von for z in zr if z.bis or z.von]
    von = min(vons, key=lambda d: d.schluessel()) if vons else None
    bis = max(biss, key=lambda d: d.schluessel(ende=True)) if biss else None
    if all(z.bis is None for z in zr):
        bis = None  # nur «ab …»-Angaben: offenes Ende bleibt offen
    return Zeitraum(von, bis, ", ".join(dict.fromkeys(z.original for z in zr if z.original)),
                    ca=any(z.ca for z in zr))


_NR_KLAMMER = r"(?:\s*\((?!\s*\d{1,2}\.\s?(?:\d{1,2}\.|[A-ZÄÖÜ][a-zäöü]+\.?)\s?(?:1[0-9]|20)\d\d\s*\))[^)\n]*\))"
NR_LISTE_RE = re.compile(
    rf"\bNrn?\.\s*\d{{1,5}}(?![.\d]){_NR_KLAMMER}?"
    rf"(?:\s*(?:bis|und|–|-)\s*\d{{1,5}}(?![.\d]){_NR_KLAMMER}?"
    rf"|\s*[,;]\s*(?:(?!(?:1[0-9]|20)\d\d\b)\d{{1,5}}(?![.\d]){_NR_KLAMMER}?"
    # Jahreszahl nach Komma: Nummer, ausser es folgt ein Zeitraum oder der Text endet («Police-Nr. 87893, 1919 - 1945»,
    # aber «Kat.-Nr. 763, 1212, 832, 1454, Kilchberg»)
    rf"|\d{{4}}(?![.\d])(?!\s*(?:[-–/]|bis\b)\s*\d)(?!\s*[)\]]?\s*$){_NR_KLAMMER}?))*")


RAHMEN_VORLAUF = 150  # Jahre: so weit vor dem Bestandszeitraum zählt eine Jahreszahl im Darin noch als Datum
HEUTE_JAHR = dt.date.today().year


def _jubilaeum_ende(f: Zeitraum) -> Zeitraum:
    """Gefeierte Spanne «1849 – 1949» → nur das Endjahr (Wortlaut und Stelle bleiben für Titel und Anmerkung)."""
    return Zeitraum(Datum(f.bis.jahr), Datum(f.bis.jahr), f.original, ca=f.ca, ereignis=f.ereignis,
                    start=f.start, ende=f.ende)


def jahre_im_text(text: str, rahmen: tuple[int, int] | None = None) -> Zeitraum | None:
    """Grobe Schätzung aus allen Jahreszahlen eines Textes (ohne Lebensdaten und Signaturen).
    rahmen: Zeitraum des Bestands laut Online-Archiv – Jahreszahlen weit davor sind Bezüge oder Nummern («Die
    Verfassung des alten Zürich … 1336», «Plan Nr. 1283», VII.174., Bestand 1820–1964), keine Laufzeit. Spätere
    Jahre bleiben (Literatur, Nachträge), nur Jahre nach heute nicht."""
    text = re.sub(r"Sign\.[^)\n]*", " ", text)
    # (nicht «Nr. 21, 24. Mai 1924»: eine Zahl mit Punkt ist ein Tag; nach Komma ist eine Jahreszahl nur mit
    # Klammer eine Nummer: «Nr. 1453 (Schaffhausen …), 1461 (Davos …)», aber «Police-Nr. 87893, 1919 - 1945»;
    # eine Klammer mit Jahr bleibt: «Sinfonie Nr. 1 (3.4.1951)»)
    text = NR_LISTE_RE.sub(" ", text)
    # Lebensdaten «30. August 1895–4. April 1961» weglassen, lange Reihen «1906 bis Juni 2018» nicht
    funde = [f for f in finde_zeitraeume(text, klammern_ignorieren=False)
             if not (f.von and f.bis and f.bis.jahr - f.von.jahr > 50 and f.von.tag and f.bis.tag)]
    # gefeierte Spannen «1834 – 1959, 125 Jahre Stadttheater» (VII.12.B.) sind keine Laufzeit – nur ihr Endjahr zählt
    def zeile_von(f: Zeitraum) -> str:
        return text[text.rfind("\n", 0, f.start) + 1:(text.find("\n", f.ende) + 1 or len(text) + 1) - 1]
    jubilaeen = [f for f in funde if f.von and f.bis and f.bis.jahr > f.von.jahr and re.search(
        rf"\b{f.bis.jahr - f.von.jahr}\s*(?:Jahre|years|ans|anni)\b", zeile_von(f), re.I)]
    # («Festakt: 125 Jahre Stadttheater Zürich 1834 – 1959, Zürich, 8. November 1959» → 08.11.1959, nicht 1959)
    ist_jub = {id(f) for f in jubilaeen}
    genauer = {f.bis.jahr for f in funde if id(f) not in ist_jub and f.bis and f.bis.monat}
    funde = [_jubilaeum_ende(f) if id(f) in ist_jub else f for f in funde
             if not (id(f) in ist_jub and f.bis.jahr in genauer)]
    if rahmen:
        a = rahmen[0] - RAHMEN_VORLAUF
        behalten, enden = [], []
        for f in funde:
            if f.von and f.bis and f.von.jahr < a and rahmen[0] <= f.bis.jahr <= HEUTE_JAHR:
                # «Zürich 600 Jahre im Bunde 1351 – 1951», «Angaben von 1759 – 1930, Mai 1942»: das Ende liegt im
                # Bestandszeitraum – es gilt, aber nur wenn sonst kein Datum bleibt
                enden.append(Zeitraum(f.bis, None, "", f.ca, f.ereignis, f.start, f.ende))
            elif all(d is None or a <= d.jahr <= HEUTE_JAHR for d in (f.von, f.bis)):
                behalten.append(f)
        funde = behalten or enden
    zr = vereinige(funde)
    if zr and zr.bis is None and zr.von:
        zr.bis = max((f.bis or f.von for f in funde if f.bis or f.von), key=lambda d: d.schluessel(ende=True))
    if zr and zr.von is None:
        return None  # nur ein Ende («Bis 1958 enthalten die Bände …», VII.308.A.): keine brauchbare Schätzung
    return zr


def ist_reiner_zeitausdruck(text: str) -> bool:
    """«1890-1916», «13. 11. 1412», «ab 1798», «o. D.» – und nichts sonst."""
    t = text.strip(" .,;()[]")
    if not t:
        return False
    if UNDATIERT_RE.fullmatch(t) or re.fullmatch(r"o\.\s?D|undatiert|s\.\s?d", t, re.I):
        return True
    funde = finde_zeitraeume(t, klammern_ignorieren=False)
    if not funde:
        return False
    rest = t
    for f in sorted(funde, key=lambda f: -f.start):
        rest = rest[:f.start] + rest[f.ende:]
    return re.fullmatch(r"[\s,;/–\-()]*(?:ca\.|und|u\.|bis|ff\.?)?[\s,;/–\-()]*", rest) is not None


NACHRUF_RE = re.compile(r"\b(?:Nachruf|Nekrolog|Todesanzeige|In Memoriam|Leidzirkular|Abdankung)", re.I)
# Verweise und Fortsetzungsnotizen im Darin: ihre Daten gehören zu anderen Beständen bzw. Einheiten (III.Q., III.R.)
VERWEIS_ZEILE_RE = re.compile(r"\bsiehe\b|\bs\.\s?auch\b|\bvgl\.|\bFortsetzung\s+(?:im|in)\b|\beingegliedert\b"
                              r"|^Fussnote \d+:", re.I)
# zusätzlicher Hinweis «siehe auch …», «s. auch …», «vgl. …»: die Unterlagen des Eintrags sind trotzdem hier
VERWEIS_AUCH_RE = re.compile(r"\b(?:siehe|s\.)\s*auch\b|\bvgl\.", re.I)
# Vermerke über Übergabe, Zuordnung und Verzeichnung: ihre Daten sind nicht die der Unterlagen (VII.388., VII.141.,
# VII.409.; «Stand: 05.07.1994», VII.2.)
VERMERK_RE = re.compile(r"\b(?:wurden?|worden)\b.{0,200}?\b(?:übergeben|abgeliefert|zugeordnet|eingereiht|umsigniert|"
                        r"überwiesen|geschenkt|eingegliedert)\b|\bArchivsignatur\b|\bStand:\s*\d", re.I | re.S)
# Spielzeit-Überschrift einer Plakat- oder Programmliste («Spielzeit 1965/66», VII.209.)
SPIELZEIT_KOPF_RE = re.compile(r"(?:Spielzeit|Saison)\s+\d{4}\s*/\s*\d{2,4}\.?", re.I)
def _ist_jahreszeile(z: "Zeile", vorher: "Zeile | None") -> bool:
    """Reine Jahreszeile im Darin, die als Datumsspalte zählt («1988 – 1989» / «Akten …», VII.151.; auch das Jahr,
    das ein umbrochenes Datum abschliesst: «… dat. 7. Aug.» / «1916») – kein Satzende «(… aus den Jahren» / «1938 -
    1945)», kein halber Bereich «1973 –» / «1976» oder «… 1857» / «– 1860», kein «seit 1401»."""
    t = z.text.strip()
    if t.count("(") != t.count(")") or t.count("[") != t.count("]") or re.match(r"seit\b|[–\-]\s*\d|bis\b", t, re.I):
        return False
    if vorher is not None and vorher.seite in (z.seite, z.seite - 1):
        v = vorher.text.rstrip()
        if re.search(r"(?:[–\-(]|\b(?:bis|von|seit|ab|Jahren?))\s*$", v) or v.count("(") > v.count(")"):
            return False
    return ist_reiner_zeitausdruck(t) and bool(finde_zeitraeume(t, False))


def _ist_jubilaeum(text: str, datum: str) -> bool:
    """«Escher Wyss, 150 years of development ¦ 1805 - 1955»: die Spalte nennt die gefeierte Spanne, nicht die
    Entstehungszeit (VII.232.)."""
    m = re.search(r"\b(\d{2,4})\s*(?:Jahre|years|ans|anni)\b", text, re.I)
    j = re.findall(rf"(?<!\d){JAHR}(?!\d)", datum)
    return bool(m and len(j) == 2 and int(j[1]) - int(j[0]) == int(m.group(1)))


UMFANG_RE = re.compile(
    r"^(?:ca\.\s*)?\d{1,4}\s*(?:Schachteln?|Mappen?|Bände|Band|Bd\.|Ordner|Kartons?|Couverts?|Rollen?|Pakete?|"
    r"Hefte?|Mikrofilme?|Fotoalben|Alben|Album|Bündel|Faszikel|Kassetten?|Dossiers?|Plakate|Plakat|Laufmeter|lfm\.?|"
    r"Fotos|Fotografien|Negative|Dias|Pläne|Plan|Bücher|Buch|Couvert|Umschläge?|Mäppchen|Stück|Stk\.?)"
    r"(?:\s*\(.*\))?\.?$", re.I)


def _ist_spaltenwert(segment: str) -> bool:
    return ist_reiner_zeitausdruck(segment) or bool(UMFANG_RE.match(segment) or SCHACHTEL_RE.match(segment))


def teile_tabellenspalten(zeilen: list[Zeile]) -> list[Zeile]:
    """Tabellen mit Kopfzeile «… Jahr Fach Mappe Allg. Nr.» (V.G.c.105.): die Spalten nach der Position der
    Spaltenköpfe abtrennen – «Jahr» wird Zeile.datum, die übrigen Zeile.spalten («Fach 170, Mappe 334,
    Allg. Nr. 2111»), damit Fach- und Mappennummern nicht als Jahre gelten. Zeilen nur mit Spaltenwerten
    («3144» unter «1576,») gehören zur Zeile davor."""
    aus: list[Zeile] = []
    koepfe: list[tuple[str, float, float]] | None = None  # (Kopf, x0, x1), erster Kopf = Jahr/Datum
    vorige: Zeile | None = None
    for z in zeilen:
        w = z.worte
        hinten = []
        for x in reversed(w):
            if x.text.strip(".,:;/()").lower() in KOPFWORTE:
                hinten.insert(0, x)
            else:
                break
        while hinten and hinten[0].text.strip(".:").lower() not in ("jahr", "jahre", "datum"):
            hinten.pop(0)  # «Bezeichnung | Jahr Fach Mappe Allg. Nr.»
        if len(hinten) >= 3 and hinten[0].text.strip(".:").lower() in ("jahr", "jahre", "datum") \
                and any(x.text.strip(".:").lower() in ("fach", "mappe", "nr", "allg") for x in hinten[1:]):
            koepfe = []
            for x in hinten:  # «Allg.» + «Nr.» ist ein Kopf
                if koepfe and x.x0 - koepfe[-1][2] < 6:
                    koepfe[-1] = (koepfe[-1][0] + " " + x.text, koepfe[-1][1], x.x1)
                else:
                    koepfe.append((x.text, x.x0, x.x1))
            aus.append(z)
            vorige = None
            continue
        if koepfe is None or z.x1 < koepfe[0][1] or ist_kopf_oder_fuss(z):
            aus.append(z)
            continue
        grenze_jahr = (koepfe[0][2] + koepfe[1][1]) / 2
        text, werte = [], {k[0]: [] for k in koepfe}
        for x in w:
            if x.x0 < koepfe[0][1] - 5:
                text.append(x)
            elif x.x0 < grenze_jahr:
                werte[koepfe[0][0]].append(x.text)
            else:
                ziel = next((k for k in koepfe[1:] if x.x1 <= k[2] + 3), koepfe[-1])
                werte[ziel[0]].append(x.text)
        jahr = " ".join(werte[koepfe[0][0]])
        rest = ", ".join(f"{k[0]} {' '.join(werte[k[0]])}" for k in koepfe[1:]
                         if werte[k[0]] and " ".join(werte[k[0]]) not in ("–", "-"))
        if not text:
            if vorige is not None:  # Fortsetzung der Spaltenwerte
                vorige.spalten = (vorige.spalten + " " + " ".join(sum(werte.values(), []))).strip()
            continue
        neu = Zeile(z.seite, z.top, z.bottom, text, z.datum or (jahr if jahr not in ("–", "-") else ""), z.umfang,
                    z.schachtel, rest)
        aus.append(neu)
        vorige = neu
    return aus


def lerne_tabstopps(zeilen: list[Zeile]) -> tuple[list[int], list[int]]:
    """Tabulatorpositionen der rechten Spalten (Datum, Umfang, Schachtel): linke bzw. rechte Kanten von Spalten-
    einträgen, die mindestens 5-mal nach einer klaren Lücke (SPALTEN_LUECKE) stehen. trenne_spalten trennt dort
    auch bei kleinerer Lücke («Führerausweise, ¦ 1947 – 1993» mit 15,7 pt in VII.328., «Gartenschmuck Schachtel 17»
    mit 3,6 pt in V.F.c.119.)."""
    links, rechts = Counter(), Counter()
    for z in zeilen:
        w = z.worte
        for i in range(len(w) - 1, 0, -1):
            if w[i].x0 - w[i - 1].x1 >= SPALTEN_LUECKE:
                if w[i].x0 >= 280 and _ist_spaltenwert(" ".join(x.text for x in w[i:])):
                    links[round(w[i].x0)] += 1
                    rechts[round(w[-1].x1)] += 1
                break

    def haeufig(c: Counter) -> list[int]:
        return sorted(x for x in c if c[x] + c.get(x - 1, 0) + c.get(x + 1, 0) >= 5)
    return haeufig(links), haeufig(rechts)


def _an_tabstopp(worte: list[Wort], i: int, tabstopps: tuple[list[int], list[int]]) -> bool:
    """Beginnt das Segment ab Wort i an einer gelernten linken Tabulatorposition oder endet die Zeile an einer
    rechten? Die Lücke muss deutlich grösser als ein Wortabstand sein (Datum ≥ 6 pt, rechtsbündig ≥ 8 pt, weil
    auch Blocksatz am Rand endet); «Schachtel N» ist eindeutig genug für jede Lücke ≥ 2,5 pt. Ein Datum nach
    «vom», «am», «bis» … gehört zum Text («… AG vom 5. Dez. 1966»)."""
    luecke = worte[i].x0 - worte[i - 1].x1
    links, rechts = tabstopps
    segment = " ".join(w.text for w in worte[i:])
    noetig = 2.5 if SCHACHTEL_RE.match(segment) else 6.0
    # (nur bei kleiner Lücke: nach einem Sprung von 10 pt und mehr an einen Tabulator ist es die Datumsspalte, und die
    # Folgezeile setzt den Text fort – «… mit Registerband und ¦ 1957-1958» / «Unterlagen», VII.12.B. 3.3.1.40.)
    if luecke < 10 and worte[i - 1].text.lower().rstrip(",") in {"vom", "von", "am", "an", "bis", "im", "in", "ab",
                                                                 "seit", "um", "ca.", "per", "vor", "nach", "zum", "zur",
                                                                 "und", "–", "-", "/"}:
        return False
    return (luecke >= noetig and any(abs(worte[i].x0 - x) <= 1.5 for x in links)) \
        or (luecke >= 8 and any(abs(worte[-1].x1 - x) <= 1.5 for x in rechts))


def trenne_spalten(z: Zeile, zahlenspalte: tuple[float, str] | None = None,
                   tabstopps: tuple[list[int], list[int]] | None = None) -> Zeile:
    """Datums- und Umfangsspalte am rechten Ende einer Zeile abtrennen (Zeile.datum / Zeile.umfang);
    zahlenspalte: (rechte Kante, «schachtel»|«exemplare») einer Spalte mit blossen Zahlen (finde_schachtelspalte);
    tabstopps: gelernte Spaltenpositionen (lerne_tabstopps), an denen auch kleinere Lücken trennen."""
    worte = list(z.worte)
    datum, umfang, schachtel = "", "", ""
    # mehrere Kanten möglich (Zusammenfassung und Detailverzeichnis verschieden breit, VII.191.): die nächste gilt
    kante = min((zahlenspalte[0], *zahlenspalte[2:]), key=lambda k: abs(worte[-1].x1 - k)) \
        if zahlenspalte and worte else 0.0
    if zahlenspalte and zahlenspalte[1] == "schachtel" and len(worte) == 1 and worte[0].x0 >= 400 \
            and re.fullmatch(r"\d{1,4}[a-z]?", worte[0].text) and abs(worte[0].x1 - kante) <= 4:
        # Nummer allein in der Schachtelspalte über den Einträgen («III) B) URBARE» / «101» / «altes Urbar …»,
        # VII.191.): eine Schachtelangabe wie «Schachtel 101»
        w = worte[0]
        return Zeile(z.seite, z.top, z.bottom, [Wort("Schachtel", w.x0 - 50, w.x0 - 5, w.font, w.size), w],
                     z.datum, z.umfang, z.schachtel, z.spalten)
    if zahlenspalte and len(worte) >= 2 and worte[-1].x1 <= kante + 25:
        # auch Bereiche und Paare in der Schachtelspalte: «33-34», «80a & 80b» (V.G.c.7.) – breiter als die
        # rechtsbündigen Nummern, darum nur ungefähr an deren rechtem Rand
        for n in (1, 3):
            wert = " ".join(w.text for w in worte[-n:])
            # mit Komma nur aufeinanderfolgende Nummern («39,40»), nicht die Dezimalzahl «0,5» (Laufmeter)
            komma = re.fullmatch(r"(\d{1,4}),\s*(\d{1,4})", wert)
            if len(worte) > n and worte[-n].x0 - worte[-n - 1].x1 >= 10 and (
                    re.fullmatch(r"\d{1,4}[a-z]?", wert) and abs(worte[-1].x1 - kante) <= 4
                    or zahlenspalte[1] == "schachtel" and SCHACHTEL_PAAR_RE.fullmatch(wert)
                    and worte[-n].x0 >= kante - 40
                    and (not komma or int(komma.group(2)) == int(komma.group(1)) + 1 > 1)):
                if zahlenspalte[1] == "schachtel":
                    schachtel = re.sub(r"\s*(?:[-–&/,]|und)\s*", "-", wert)
                else:
                    umfang = f"{wert} Expl."
                worte = worte[:-n]
                break
    for _ in range(3):  # «… 1 Schachtel», «… 1890-1916», «… Schachtel 301» können kombiniert vorkommen
        if len(worte) < 2:
            break
        lueckenpos = None
        for i in range(len(worte) - 1, 0, -1):
            # an einer Tabulatorposition nur, wenn das Wort davor nicht selbst zum Datum gehört («1947 – ¦ 1993»)
            if worte[i].x0 - worte[i - 1].x1 >= SPALTEN_LUECKE or (
                    tabstopps and _an_tabstopp(worte, i, tabstopps)
                    and _ist_spaltenwert(" ".join(w.text for w in worte[i:]))
                    and not ist_reiner_zeitausdruck(" ".join(w.text for w in worte[i - 1:]))):
                lueckenpos = i
                break
        if lueckenpos is None or worte[lueckenpos].x0 < 280:
            break
        segment = " ".join(w.text for w in worte[lueckenpos:])
        if not datum and ist_reiner_zeitausdruck(segment):
            # Datum über die Lücke hinaus nach links ergänzen («April / ¦ Mai 1986», «9. – ¦ 13. Juni 1986»),
            # aber nur um Datumsteile – «Rat und ¦ 26. 8. 1414» bleibt im Titel
            def datumsteil(t: str) -> bool:
                return bool(MONAT_WORT_RE.match(t) or re.fullmatch(r"\d{1,2}\.", t))
            while lueckenpos > 1 and not re.match(rf"{JAHR}\b", worte[lueckenpos].text):
                t = worte[lueckenpos - 1].text
                if datumsteil(t):
                    lueckenpos -= 1
                elif t in ("/", "–", "-", "bis", "und", ",") and lueckenpos > 2 \
                        and datumsteil(worte[lueckenpos - 2].text):
                    lueckenpos -= 2
                else:
                    break
            segment = " ".join(w.text for w in worte[lueckenpos:])
            datum = segment
        elif not umfang and UMFANG_RE.match(segment):
            umfang = segment
        elif not schachtel and SCHACHTEL_RE.match(segment):
            schachtel = SCHACHTEL_RE.match(segment).group(1)
        else:
            break
        worte = worte[:lueckenpos]
    if not (datum or umfang or schachtel):
        return z
    return Zeile(z.seite, z.top, z.bottom, worte, datum or z.datum, umfang or z.umfang, schachtel or z.schachtel,
                 z.spalten)


# ----------------------------------------------------------------------------- Signaturen

DEZIMAL_RE = re.compile(r"^(\d{1,3}(?:\.(?:\d{1,4}|[a-z]))*)\.?$")  # 2.1.1. / 1.a. / 10 / 1.1.1000.
DEZIMAL_ANGEKLEBT_RE = re.compile(r"^(\d{1,3}(?:\.\d{1,4}){1,7})\.(?=[^\d\s.])(.+)$")  # «5.2.4.25.Aufführungen»
ROEMISCH_RE = re.compile(r"^(?=[IVXL])(L?X{0,3})(IX|IV|V?I{0,3})[.)]$")  # «II.», «II)»
GROSS_RE = re.compile(r"^([A-Z])[.)]?$")  # «A.», «A)», «A»
TITELANFANG = "„«\"(“”‚‘’'»["  # ein Titel darf auch mit Anführungszeichen oder Klammer beginnen
# nach «II.» kein Titel, sondern eine Überschrift des Findmittels
VERZEICHNISWORT = {"DETAILVERZEICHNIS", "VERZEICHNIS", "INHALTSVERZEICHNIS", "INHALT", "ÜBERSICHT", "EINLEITUNG",
                   "VORWORT", "ANHANG", "REGISTER", "ZUSAMMENFASSUNG", "INVENTARÜBERSICHT", "DETAILINVENTAR",
                   "BESTANDESÜBERSICHT", "BESTANDSÜBERSICHT", "GLIEDERUNG", "INHALTSÜBERSICHT"}
KLEIN_RE = re.compile(r"^([a-z])\)$")
NUMMER_RE = re.compile(r"^\d{1,4}[a-z]?$")
MENGE_RE = re.compile(
    r"(?:[A-ZÄÖÜ][a-zäöü]+(?=mappen?\b|schachteln?\b|ordner\b|bände\b|alben\b|rollen?\b|kassetten?\b|hefte?\b))?"
    r"(?:Schachteln?|Mappen?|mappen?|schachteln?|ordner|bände|alben|rollen?|kassetten?|hefte?|Bände|Band|Ordner|Kartons?|Couverts?|Kuverts?|Umschläge?|Rollen?|Filmrollen?|Filme?|"
    r"Hefte?|Notizhefte?|Sammelmappen?|Fotos?|Fotografien|Photographien|Bilder|Karikaturen?|Zeichnungen?|Plakate?|"
    r"Pläne?|Planrollen?|Stück|Stk\.?|Expl\.?|Exemplare?|Blätter|Blatt|Bl\.|Listen?|Schreiben|Briefe?|Karten|"
    r"Tonbandkassetten?|Tonbänder|Kassetten?|Disketten?|CDs?|DVDs?|Videos?|Dias?|Negative?|Alben|Album|Bündel|"
    r"Pakete?|Faszikel|Dossiers?|Broschüren?|Bücher|Buch|Zeitungen|Ausschnitte|Urkunden|Siegel|Uhr|Jahre?|Tage?|"
    r"Monate?|Wochen?|Stunden?|Minuten?|Mal|Prozent|Franken|Fr\.)(?:\W|$)")
# «Schachtel 3», «Schachtel I:», «Schachteln 3 und 4», «Schachteln 5–7»
SCHACHTEL_RE = re.compile(r"^(?:Schachtel|Schachteln)\s+(\d+[a-z]?(?:\s*(?:[–-]|\+|,|und|bis)\s*\d+[a-z]?)*|[IVXL]{1,6})"
                          r"\s*:?\s*$", re.I)
# Überschrift einer anderen Aufbewahrung («Mappe», «Grossformat»): die laufende Schachtel endet
AUFBEWAHRUNG_RE = re.compile(r"^(?:Mappen?|Kartonmappen?|Planmappen?|Grossformate?|Planschrank|Ordner)(?:\s+\S+){0,2}:?$")
TEIL_NUR_RE = re.compile(r"^\(?Teil\s+(\d+)\)?\s*\.?$")
TEIL_ZEILE_RE = re.compile(r"^(?P<titel>.{3,100}?),?\s+\(?Teil\s+(?P<nr>\d+)\)?\s*\.?$")
BESTANDSUMFANG_RE = re.compile(r"^Der Bestand\s+\S+(?:\s\S+)?\s+umfasst\b")
SCHLUSS_RE = re.compile(r"^(?:Archivierung\b|Archiviert\b|Verzeichnung\b.*abgeschlossen|Bearbeitet von\b|"
                        r"Der Bestand\s+(?:\S+\s+){0,3}?umfasst\b|Umfang des Bestandes\b|Stadtarchiv Zürich\s*$|"
                        r"STADTARCHIV ZÜRICH\s*$|Bestand\s*:\s*\d{1,4}\s+(?:Norm|Archiv)?(?:Schachteln?|Mappen?|Bände)\b|"
                        r"(?:Neu\s+|Bestand\s+)?(?:[Gg]eordnet|[Vv]erzeichnet)(?:\s+und\s+(?:verzeichnet|geordnet))?\s+(?:von|durch)\b|"
                        r"Letzte[rns]?\s+(?:Ae|Ä)?(?:nderung(?:en)?|Änderung(?:en)?|Ergänzung(?:en)?|"
                        r"Bearbeitung(?:en)?|Nachtr[aä]ge?)\b|Neuarchivierung\b|Neu gelayoutet\b|Neu erfasst am\b|"
                        r"[Nn]eu umgebrochen\b|[Nn]eu formatiert\b|S\.\s*\d+\s*[-–]\s*\d+\s+gelayoutet\b|"
                        r"[Ee]ndarchiviert/|"
                        r"[Aa]rchiviert/|Endarchivierung\b|Nachtr[aä]ge?\s+archiviert\b|"
                        r"Ergänz(?:t|ungen?)\b.{0,80}:\s*\d{1,2}\.\s?\S+\s?\d{4}|Stand\s*:|"
                        r"[0-9A-Z]{3,8}/\d{1,3}/[A-Za-z]{2,4}\s+Stand\s*:)")  # «0354B/1/rpt Stand: 05.07.1994» (VII.2.)
# «12. Juni 2007 / Dr. Robert Dünki» am Schluss: Datum und Bearbeiter
SCHLUSS_DATUM_RE = re.compile(r"^(?:Stadtarchiv Zürich,?\s*/?\s*)?\d{1,2}\.\s?(?:\d{1,2}\.|[A-ZÄÖÜ][a-zäöü]+\.?)"
                              r"(?:\s?bzw\.\s?\d{1,2}\.\s?[A-ZÄÖÜ][a-zäöü]+)?\s?\d{2,4}\s*/\s*\S"
                              # auch Kürzel vor dem Datum: «max / 28. März 2000» (VII.340.)
                              r"|^[A-Za-zÄÖÜäöü]{2,5}\s*/\s*\d{1,2}\.\s?(?:\d{1,2}\.|[A-ZÄÖÜ][a-zäöü]+\.?)\s?\d{4}\s*$")


# «Zürich, Oktober 1976 / Dr. Paul Guyer, a. Stadtarchivar» am Schluss (VII.109.): Ort, Datum und Bearbeiter
SCHLUSS_ORT_DATUM_RE = re.compile(rf"^(?:Stadtarchiv\s+)?Zürich,?\s+(?:\d{{1,2}}\.\s?)?{MONAT_MUSTER}\.?\s+\d{{4}}\s*/\s*\S")
# Bearbeitungsvermerk mit echtem Datum «29. Juli 1999 / RD», «7.2.1994/Anna Pia Maissen» (nicht «6. Privatkorrespondenz
# 1970 / A – P», V.F.c.204.)
VERMERK_DATUM_RE = re.compile(rf"^\d{{1,2}}\.\s?(?:\d{{1,2}}\.|{MONAT_MUSTER}\.?)"
                              rf"(?:\s?bzw\.\s?\d{{1,2}}\.\s?(?:\d{{1,2}}\.|{MONAT_MUSTER}\.?))?\s?\d{{2,4}}\s*/\s*\S")


# Anfang einer Notiz zum Bestand nach der letzten Einheit (Schlussblock in der Signaturspalte, baue_vorkommen):
# «Anmerkungen:», «Beilagen:», «Literatur», «Zu diesem Bestand vgl. auch: …», «Der Bestand wurde am … übergeben»,
# «Lagerung: …», «Stand: 06.07.1992», Bearbeitervermerk «Urs Scherer/ 7. Juni 1996»
SCHLUSSNOTIZ_RE = re.compile(
    r"^(?:Anmerkung(?:en)?|Bemerkung(?:en)?|Hinweis(?:e)?|Nota|Notiz|Beilagen?\s*:|Anlagen?\s*:|Literatur|Quellen\s*:"
    r"|Vgl\.|Zu diesem Bestand|Zur (?:Überlieferungs|Bestands|Archiv)geschichte|Der (?:Archiv)?[Bb]estand|Dieser Bestand"
    r"|Die Bestände|Der Nachlass|Das (?:Theater)?[Aa]rchiv\b|Dem Bestand|Lagerung|Umfang\s*:|Benützung|Total\s*:"
    r"|Zusätzlich|Des Weiteren|Weitere Akten|Weitere [A-ZÄÖÜ]\w+ (?:befinden sich|liegen|sind)\b"
    r"|Wenn keine|Die (?:Protokolle|Akten|Archivalien|Dokumente|Bücher|Pläne|Literatur"
    r"|verzeichneten)\b|Bei der Dokumentation|Der Inhalt der|Verzeichnis überarbeitet|endarchiviert)"
    r"|\b(?:übergeben|überbracht|zugeordnet|erhalten am)\b|\bStand:\s*\d"
    r"|(?:^|\s)[A-ZÄÖÜ][\w.\-]+(?:\s[A-ZÄÖÜ][\w.\-]+)*\s?/\s?\d{1,2}\.\s?(?:\d{1,2}\.|[A-ZÄÖÜ][a-zäöü]+\.?)\s?\d{2,4}\s*$")


# Überschrift eines Schlussabschnitts nach der letzten Einheit (baue_vorkommen): «Literatur», «Ausgewählte Literatur
# und Hinweise zu den Personen», «Genealogische Quellen:», «Verweise auf andere Bestände», «Bemerkungen zu diesem
# Teilbestand:», «Darstellungen und Mitgliederverzeichnisse in der Bibliothek des Stadtarchivs»
SCHLUSSKOPF_RE = re.compile(
    r"^(?:(?:[A-ZÄÖÜ][a-zäöü]+(?:e|en|er)\s+)?(?:Literatur|Quellen|Bibliogra(?:f|ph)ie)(?:verzeichnis(?:se)?)?\b"
    r"|Die Literatur\b|(?:Quellen)?[Nn]achweise?\s+(?:zu[mr]?|über)\s"
    r"|.{0,80}:\s*Biogra(?:f|ph)isch(?:es|e\s+(?:Angaben|Notizen))\s*$"
    r"|(?:Quer)?[Vv]erweise?\s+(?:auf|zu)\b|Hinweise?\s+(?:auf|zu)\s"
    r"|(?:Bemerkung|Anmerkung|Hinweis|Notiz|Nachbemerkung)(?:en|e)?(?:\s+zu[mr]?\s.*)?\s*:?$"
    r"|(?:Zur\s+)?(?:Bestands|Überlieferungs|Archiv)geschichte\b|Geschichte des (?:Bestandes|Nachlasses|Archivs)\b"
    r"|(?:Verwandte|Weitere|Ergänzende|Andere)\s+(?:Bestände|Unterlagen|Quellen)\b"
    r"|.{0,80}\bin der Bibliothek des Stadtarchivs\b|Benut?zung(?:sbestimmungen)?\s*:?$"
    r"|Geschichte (?:der|des)\b[^:]{0,80}:$|Zu diesem Bestand\s*:$|(?:Aufteilung|Verteilung)\b.{0,60}\bSchachteln\s*:$)")


# Stück ohne Nummer im Schlussblock (baue_vorkommen) bzw. neben den Schachteln (baue_behaelter)
STUECK_KOPF_RE = re.compile(r"^(?:Reproduktionen|Beilagen?|Grossformate?|Planmappen?|Pläne|Fotos|Fotografien|Photographien|"
                            r"Plakate)\b[^:]{0,40}:?\s*$")
STUECK_SATZ_RE = re.compile(r"^(?:Eine?|Zwei|Drei|Vier|Fünf|Sechs|\d{1,2})\s+(?:Archiv|Norm|grossformatige\s+)?"
                            r"(?:[Ss]chachteln?|Mappen?|Ordner|Bände|Kartons?)\s+(?:enthält|enthalten)\b")
# Zuordnungsliste «Schachtel 2: 4.1.2. – 4.1.5.» (VII.12.A.), «Schachtel 1: Nummern 1.1. bis 1.25.» (VII.255.)
ZUORDNUNG_RE = re.compile(r"(?:Schachtel|Schachteln)\s+(\d{1,4}[a-z]?)\s*:\s*(?:Nummern?|Nrn?\.|Signaturen?)?\s*"
                          r"(\d{1,3}(?:\.\d{1,4})*)\.?(?:\s*(?:[–-]|bis)\s*(\d{1,3}(?:\.\d{1,4})*)\.?)?")
# Schachtelübersicht am Schluss, die nur auf Nummern verweist: «Schachtel 1: Nummern 1.1. bis 1.25.», «1 Schachtel
# Grossformat: Nummer 3.5.» (VII.255.)
SCHACHTEL_VERWEIS_RE = re.compile(r"^(?:\d{1,2}\s+)?Schachtel\b[^:]{0,30}:?\s*Nummer(?:n)?\s+\d")
STUECK_SCHLUSS_RE = re.compile(r"^(?:Dem Bestand (?:liegt|liegen) (?:ferner |auch |ausserdem )?bei\b"
                               r"|Beim Bestand (?:befindet|befinden) sich\b"
                               r"|Der Bestand enthält (?:auch|ferner|ausserdem|zudem|zusätzlich|aus)\b"
                               r"|Zum Bestand gehör(?:t|en) (?:auch|ferner|ausserdem)\b"
                               r"|In (?:der )?Schachtel \d{1,3} (?:befindet|befinden|liegt|liegen) sich "
                               r"(?:ferner|auch|ausserdem)\b)")
STUECK_BEHAELTER_RE = re.compile(r"^(?:Grossformate?|Planmappen?|Rollen?|Beilagen?|Reproduktionen)\b[^:]{0,30}:\s*\S")


def ist_schlusskopf(z: Zeile, grund: float) -> bool:
    """Überschrift eines Schlussabschnitts (SCHLUSSKOPF_RE), grösser als die Grundschrift oder fett."""
    t = z.text.strip()
    return bool(z.worte) and len(t) <= 100 and SCHLUSSKOPF_RE.match(t) is not None and not t[:1].isdigit() \
        and (z.worte[0].size >= grund + 1.5 or all("Bold" in w.font for w in z.worte))


BESTANDSPROSA_RE = re.compile(r"\b(?:Bestand(?:es)?|Archivbestand(?:es)?|Nachlass(?:es)?|Verein(?:s|es)?|Stadtarchivs?|"
                              r"gegründet|Gründung|Auflösung|übergeben|integriert|abgeliefert|Ablieferung|Stadtrat(?:es)?|"
                              r"StRB|Schenkung|Depositum|zugeordnet|unterstellt|aufgelöst|umbenannt)\b")


def ist_prosa_bis_schluss(zeilen: list[Zeile]) -> bool:
    """Wie ist_schlussabsatz, aber ohne Signaturprüfung (Findmittel nach Schachteln): Prosa mit einem Wort zur
    Bestandsgeschichte bis zum Schlussvermerk, danach keine Schachtel bzw. Mappe mehr."""
    block = []
    for x in zeilen:
        t = x.text.strip()
        if ist_schlussvermerk(t) or SCHLUSS_DATUM_RE.match(t) or VERMERK_DATUM_RE.match(t):
            break
        if BEHAELTER_RE.match(t):
            return False
        block.append(t)
    text = " ".join(block)
    return 2 <= len(block) <= 12 and sum(len(t) for t in block) >= 90 \
        and re.search(r"[a-zäöü)“”\]]\.(?:\s|$)", text) is not None and BESTANDSPROSA_RE.search(text) is not None \
        and not any(BEHAELTER_RE.match(x.text.strip()) for x in zeilen[len(block):])


def ist_schlussabsatz(zeilen: list[Zeile], i: int, gl: "Gliederung") -> bool:
    """Prosa ab Zeile i bis zum Schlussvermerk bzw. Ende: mindestens zwei lange Zeilen mit Satzende und einem Wort zur
    Bestandsgeschichte (BESTANDSPROSA_RE), danach keine Signatur und keine Schachtel mehr."""
    block = []
    for x in zeilen[i:]:
        t = x.text.strip()
        if ist_schlussvermerk(t) or SCHLUSS_DATUM_RE.match(t) or VERMERK_DATUM_RE.match(t):
            break
        block.append(t)
    text = " ".join(block)
    # (der erste Absatz endet als Satz: die Listeneinträge «Geschlechter-Register …, o. O. u. J. … eigene Forschungen)»,
    # «Mario von Moos, Verzeichnis …, Feraltorf 1979» unter «3. Inventare» sind Inhalt, erst «Die … Sammlungen …
    # wurden im Mai 1999 dem Stadtarchiv Zürich übertragen.» ist Bestandsgeschichte, VII.327.)
    # (ein echtes Satzende in einer Zeile des Absatzes, keine Abkürzung «o. O. u. J.»: «… hergestellt und dem
    # Stadtarchiv übergeben.» / «Standort: …», VII.336.)
    erster = [zeilen[i]]
    for a, b in zip(zeilen[i:i + len(block)], zeilen[i + 1:i + len(block)]):
        if luft(a, b) > ABSATZ_ABSTAND:
            break
        erster.append(b)
    if not any(re.search(r"(?:[a-zäöüß]{2,}|\d{2,}|[)“”»\]])[.!?][)“”»\]]?$", x.text.strip()) for x in erster):
        return False
    # (auch länger, wenn es durchgehend Prosa ist: sieben Absätze zur Geschichte der Armenpflege, VII.158.)
    lang = 12 < len(block) <= 40 and len(re.findall(r"[a-zäöü)“”\]]\.(?:\s|$)", text)) >= 3 \
        and sum(len(t) for t in block) / len(block) >= 60
    if not (2 <= len(block) <= 12 or lang) or sum(len(t) for t in block) < 90 \
            or sum(len(t) for t in block) / len(block) < 45:
        return False
    if not re.search(r"[a-zäöü)“”\]]\.(?:\s|$)", text) or not BESTANDSPROSA_RE.search(text):
        return False
    return not any(lies_signatur(x, gl.kopie()) is not None or SCHACHTEL_RE.match(x.text.strip()) for x in zeilen[i + 1:])


def erstes_kind(t: "SigTreffer | None", v: "Vorkommen | None") -> bool:
    """Ist die Signatur t die erste Unternummer der Einheit v (6.1.1. nach 6.1.) oder ihr erster weiterer Teil
    («4.3.2. Bernhard-Littéraire» / «Liste der Veranstaltungen …, nach Saison geordnet:» / «4.3.2. 1985/86», VII.298.)?"""
    return t is not None and v is not None and (
        len(t.pfad) == len(v.pfad) + 1 and t.pfad[:-1] == v.pfad and t.pfad[-1] in ("1", "a", "A", "I")
        or t.pfad == v.pfad and not v.ist_teil)


def _eine_ziffer_anders(a: str, b: str) -> bool:
    """a und b unterscheiden sich in genau einer Ziffer (ersetzt, fehlend oder zusätzlich)."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    kurz, lang = (a, b) if len(a) < len(b) else (b, a)
    return any(lang[:j] + lang[j + 1:] == kurz for j in range(len(lang)))


def links_vom_darin(z: Zeile, v: "Vorkommen") -> bool:
    """Zeile steht deutlich links der Darin-Zeilen der Einheit (Signaturspalte, der Text der Einheit ist eingerückt)."""
    inhalt = [x for x in v.zeilen[1:] if x.worte]
    return len(inhalt) >= 2 and sum(1 for x in inhalt if x.x0 > z.x0 + 15) >= 0.8 * len(inhalt)


def _spaltenanfaenge(z: Zeile, luecke: float = 15.0) -> list[float]:
    """x0 der Spalten einer Zeile (neue Spalte nach einer Lücke > luecke); eine abgetrennte Datums-, Umfang- oder
    Schachtelspalte zählt als weitere Spalte."""
    xs = [z.worte[0].x0] if z.worte else []
    xs += [b.x0 for a, b in zip(z.worte, z.worte[1:]) if b.x0 - a.x1 > luecke]
    return xs + ([999.0] if (z.datum or z.umfang or z.schachtel or z.spalten) else [])


def ist_namenstabellenzeile(zeilen: list[Zeile], i: int) -> bool:
    """«D. Lasserre ⟨Tab⟩ Der 4. November 1440 ⟨Tab⟩ Dezember 1940, Heft 8» in einer Tabelle Autor | Titel | Heft
    (V.L.205.): Initiale(n) und Name, danach drei Spalten wie in den Zeilen ohne Initiale davor («Ernst Fischer ⟨Tab⟩
    Ibsen und das Dritte Reich ⟨Tab⟩ April 1940 …») – ein Autorenname, keine Buchstaben-Signatur."""
    z = zeilen[i]
    w = z.worte
    if len(w) < 3 or not re.fullmatch(r"[A-ZÄÖÜ]\.", w[0].text) or w[1].x0 - w[0].x1 > 6:
        return False
    xs = _spaltenanfaenge(z)
    if len(xs) < 3 or sum(1 for a in w if a.x0 < xs[1]) > 4:
        return False
    gleich = 0
    for x in zeilen[max(0, i - 15):i]:
        if not x.worte or abs(x.x0 - z.x0) > 2 or re.fullmatch(r"[A-ZÄÖÜ]\.", x.worte[0].text):
            continue
        xs_x = _spaltenanfaenge(x)
        if len(xs_x) >= 3 and abs(xs_x[1] - xs[1]) <= 3 and sum(1 for a in x.worte if a.x0 < xs_x[1]) <= 4:
            gleich += 1
    return gleich >= 2


def schlusszeile(z: Zeile, text: str) -> str:
    """Text einer Schlussvermerk-Zeile samt abgetrennten Spalten («V.J. b.202.17. Städtisches Waisenhaus Entlisberg ¦
    1947-1956», V.J.W.c.15.) – sonst fehlen Datum, Umfang und Schachtel im Blatt Info."""
    schachtel = f"Schachtel {z.schachtel}" if z.schachtel and z.schachtel.isdigit() else z.schachtel
    return " ".join([text] + [x for x in (z.datum, z.umfang, schachtel, z.spalten) if x and x not in text])


def ist_schlussvermerk(text: str, vor: "Zeile | None" = None, z: "Zeile | None" = None) -> bool:
    """SCHLUSS_RE – aber eine klein beginnende Zeile direkt nach einem unvollständigen Satz («Die Stammfolge (10
    Generationen) ist» / «verzeichnet von Michael Kreis …», VII.482.) ist kein Schlussvermerk; nach einem Absatz
    schon («geordnet und verzeichnet durch Dr. Claudia Caduff», «endarchiviert/verzeichnet …»)."""
    if not SCHLUSS_RE.match(text):
        return False
    if not text[:1].islower() or vor is None or not vor.worte or z is None:
        return True
    absatz = vor.seite != z.seite or z.top - vor.bottom > ABSATZ_ABSTAND
    return absatz or bool(re.search(r"[.:;!?)»“]$", vor.text.strip()))
KOPFWORTE = {"nr", "signatur", "titel", "inhalt", "datum", "jahr", "jahre", "zeit", "zeitraum", "laufzeit", "schachtel",
             "mappe", "fach", "allg", "umfang", "bemerkung", "bemerkungen", "ort", "bauherr", "objekt", "gesuch",
             "medium", "hinweise", "hinweis", "expl", "anzahl", "band", "bände", "seite", "seiten", "bezeichnung",
             "saison", "aufführung", "aufführungen", "zitat", "standort", "format", "sprache", "verfasser", "autor",
             "gegenstand", "beschreibung"}  # «Nr. ¦ Gegenstand ¦ Datum» (VII.37.), «Signatur ¦ Beschreibung ¦ Format» (X.H.)


def ist_tabellenkopf(text: str) -> bool:
    """Zeile nur aus Spaltenköpfen («Gesuch Nr.», «Nr. / Titel Datum», «Medium Inhalt Hinweise»)."""
    worte = [w.strip(".,:;/()").lower() for w in text.split() if w.strip(".,:;/()–-")]
    if text.strip() in ("Sch.", "Schachtel-Nr.", "Sch.-Nr."):
        return True  # Kopf der Schachtelspalte allein auf einer Zeile («1. Schlachthofordnung» / «Sch.», V.F.c.150.)
    return 2 <= len(worte) <= 8 and all(w in KOPFWORTE for w in worte)


TABELLENKOPF_RE = re.compile(r"^(?:Signatur|Saison|Nr\.)\b.*\b(?:Inhalt|Titel|Datum|Aufführung|Schachtel|Jahre?|Zeit)\b"
                             r"|^(?:Schachtel|Mappe)\s+Nr\.?\s+(?:\S+\s+){0,3}?(?:Inhalt|Titel|Datum|Jahre?|Zeit)\b")
GROSSWORT_RE = re.compile(r"^[A-ZÄÖÜ]{4,}$")  # «DETAILVERZEICHNIS», «ÜBERSICHT»
AUFZAEHLUNG = ("-", "–", "•", "−", "▪", "", "·", "o", "")
RANG = {"roem": 0, "gross": 1, "zahl": 2, "klein": 3}


def roemisch_wert(s: str) -> int:
    werte = {"I": 1, "V": 5, "X": 10, "L": 50}
    total = 0
    for i, c in enumerate(s):
        v = werte[c]
        total += -v if i + 1 < len(s) and werte[s[i + 1]] > v else v
    return total


def pfad_text(pfad: tuple[str, ...]) -> str:
    return ".".join(pfad) + "."


@dataclass
class SigTreffer:
    pfad: tuple[str, ...]
    anzeige: str  # Signatur wie sie im Excel steht (ohne Bestand), z. B. «2.1.1.», «B 3», «A.1.»
    roh: str  # wie im PDF
    rest: Zeile | None
    fett: bool
    typ: str = "zahl"
    hinweis: str = ""
    eltern: tuple | None = None  # (pfad, roh) der äusseren Marke bei «II) B) MITGLIEDERVERZEICHNISSE»


@dataclass
class Gliederung:
    """Zustand beim Lesen der Signaturen eines Findmittels."""
    modus: str = "dezimal"  # «dezimal» oder «gliederung» (römische Zahlen/Buchstaben/lokale Nummern)
    bestand: str = ""  # ohne Leerzeichen, z. B. «VI.HO.»
    stapel: list = field(default_factory=list)  # [(rang, komponenten)]
    letzte: dict = field(default_factory=dict)  # (typ, präfix) -> letzter Wert
    hauptnr: int = 0
    nur_pruefen: bool = False
    rang: dict = field(default_factory=lambda: dict(RANG))  # je Findmittel gelernt, siehe lerne_raenge()
    freie_nummern: bool = False  # laufende Nummern mit Lücken («22, 29, 30 …», VII.308.C.a.)
    jahr_nummern: bool = False  # Signaturen «Jahr.Laufnummer» («1941.1», VII.308.D.a.)
    buchstaben: bool = False  # dezimal mit Buchstabenabschnitten «A. KORRESPONDENZ …», Zählung je Abschnitt neu
    abschnitt: str = ""  # laufender Buchstabenabschnitt
    einrueck_x: float | None = None  # ab hier sind blosse Nummern eine Unterzählung (VII.380.)
    mengenzahlen: bool = False  # blosse Zahlen ohne Punkt sind Mengen, keine Signaturen (lerne_mengenzahlen)
    text_x0: float | None = None  # dezimal: hier beginnt der Titel hinter den Signaturen (lerne_textspalte)
    weitere_bestaende: frozenset = frozenset()  # Findmittel für mehrere Bestände (finde_bestandswechsel)
    gruppen_buchstaben: frozenset = frozenset()  # Buchstaben mit Untersignaturen «A.a.», «A.1.» im Verzeichnis
    kind_von: tuple = ()  # dezimal: Signatur der laufenden Einheit (deren Unternummern dürfen eingerückt sein)
    vorschau: str = ""  # erstes Wort der nächsten Zeile
    doppelmarken: bool = False  # Gruppen mit Doppelmarken «III) B) URBARE»: dann ist auch «A) …» eine Gruppe
    teil_groesse: float = 0.0  # Schriftgrösse der Teil-Überschriften «1. Alfred …», «2. Myrthe …» (VII.232.)
    registratur: bool = False  # Registraturplan mit dreistelligen Codes «010», «011», «013.1» (V.F.c.28.)
    reg_stapel: list = field(default_factory=list)  # [(Ebene, Code)] der laufenden Registraturplan-Position
    marken_groesse: dict = field(default_factory=dict)  # mittlere Schriftgrösse je Markentyp (lerne_markengroessen)
    punktnummern: bool = False  # Signaturen «1.», «2.» mit Punkt: blosse Zahlen ohne Punkt sind Mengen (VII.65.)
    letzter_pfad: tuple = ()  # Signatur der laufenden Einheit, auch eines Teils (für «20. 2.» nach 20.1., VII.151.)
    letzte_marke: tuple = ()  # (x0, fett) der Signaturzeile der laufenden Einheit
    haupt_titel: str = ""  # dezimal: Titel der laufenden Hauptnummer («7. Kassenbuch und Journal …»)
    listen_nr: tuple = ()  # dezimal: (Wert, x0, Seite) der letzten Zeile «N.», die keine Signatur war (Listenpunkt)
    listen_spalten: dict = field(default_factory=dict)  # dezimal: x0 -> (Wert, Seite, Einheit) des letzten Listenpunkts
    haupt_fett: bool = False  # dezimal: die laufende Hauptnummer steht fett («1. 1. Fortifikation von Zürich», VII.76.)
    zahl_groesse: float = 0.0  # Gliederung: grösste Schrift der bisherigen Nummern der obersten Zahlenebene
    klammer_x: float | None = None  # Gliederung: Spalte der fetten römischen Stufen «II)»; dort sind auch nicht fette
    #   «A)» und «1)» Stufen (V.G.c.107.)
    klammer_zahlen: bool = False  # Gliederung: fette «1)», «2)» … sind die oberste Stufe (VII.170.)
    naechste_dezimal: str = ""  # dezimal: nächste mehrstufige Nummer in der Signaturspalte nach der laufenden Zeile
    klammer_voll: bool = False  # Signaturen nur in Klammern bei den Behältern «Schachtel 1 (V.F. c.18.:1)» (V.F.c.18.)
    roem_einzeln: bool = False  # nur eine einzige, nicht fette römische Marke im Verzeichnis: keine Stufe (VII.11.)
    inhalt_zeilen: int = 0  # Zeilen der laufenden Einheit (Titelzeile mitgezählt)

    def kopie(self) -> "Gliederung":
        return Gliederung(self.modus, self.bestand, list(self.stapel), dict(self.letzte), self.hauptnr, True,
                          self.rang, self.freie_nummern, self.jahr_nummern, self.buchstaben, self.abschnitt,
                          self.einrueck_x, self.mengenzahlen, self.text_x0, self.weitere_bestaende,
                          self.gruppen_buchstaben, self.kind_von, self.vorschau, self.doppelmarken,
                          self.teil_groesse, self.registratur, list(self.reg_stapel), self.marken_groesse,
                          self.punktnummern, self.letzter_pfad, self.letzte_marke, self.haupt_titel,
                          self.listen_nr, dict(self.listen_spalten), self.haupt_fett, self.zahl_groesse,
                          self.klammer_x, self.klammer_zahlen, self.naechste_dezimal, self.klammer_voll,
                          self.roem_einzeln, self.inhalt_zeilen)

    def _praefix(self, typ: str) -> tuple[str, ...]:
        r = self.rang[typ]
        return tuple(k for rr, ks in self.stapel if rr < r for k in ks)

    def _setze(self, typ: str, komps: tuple[str, ...]) -> tuple[str, ...]:
        r = self.rang[typ]
        praefix = self._praefix(typ)
        if not self.nur_pruefen:
            while self.stapel and self.stapel[-1][0] >= r:
                self.stapel.pop()
            self.stapel.append((r, komps))
            # neue Nennung der Marke: die Zählung darunter beginnt neu («D. Rechnungswesen» der 3. Serie / «III. …»
            # nach «I.-II. … [leer]», V.G.c.50.)
            neu = praefix + komps
            for k in [k for k in self.letzte if len(k[1]) >= len(neu) and k[1][:len(neu)] == neu]:
                del self.letzte[k]
        return praefix + komps


def _folgt(gl: Gliederung, typ: str, wert: int, fett: bool) -> bool:
    """Passt eine Gliederungsmarke (Zahl/Buchstabe/römisch) in die Reihenfolge?"""
    schluessel = (typ, gl._praefix(typ))
    letzte = gl.letzte.get(schluessel, 0)
    # Lücken («g) bis i) fehlen») und Wiederholungen (mehrere «p)»-Gruppen) sind erlaubt
    ok = fett or wert == 1 or letzte <= wert <= letzte + 6 or (typ == "zahl" and gl.freie_nummern and wert >= letzte)
    if ok and not gl.nur_pruefen:
        gl.letzte[schluessel] = wert
    return ok


def _marken_typ(z: Zeile) -> str | None:
    """Grobe Einordnung der ersten Marke einer Zeile (für lerne_raenge)."""
    w = z.worte
    if w[0].x0 > SIGNATUR_SPALTE_MAX_GLIEDERUNG or len(w) < 2 \
            or not (w[1].text[:1].isupper() or w[1].text[:1] in TITELANFANG):
        return None
    t = w[0].text
    if t.endswith(")") and (ROEMISCH_RE.match(t) or GROSS_RE.match(t)) and "Bold" not in w[0].font:
        return None  # «A) Constaffel» ist ein Listenzeichen, keine Stufe (wie in lies_signatur)
    if ROEMISCH_RE.match(t):
        return "roem"
    if GROSS_RE.match(t):
        return "gross"
    if KLEIN_RE.match(t):
        return "klein"
    if DEZIMAL_RE.match(t) and not SCHACHTEL_RE.match(" ".join(x.text for x in w[1:])):
        rest = z.ab(1)
        if rest is not None and _ist_datumsfolge(rest):
            return None  # «1. Juni 1925» (umbrochenes Datum unter «A. Selbständig erschienene …», VII.109.)
        return "zahl"
    return None


def lerne_markengroessen(zeilen: list[Zeile]) -> dict:
    """Mittlere Schriftgrösse der Gliederungsmarken je Typ (mindestens drei Marken)."""
    groessen: dict[str, list[float]] = {}
    for z in zeilen:
        typ = _marken_typ(z)
        if typ is not None:
            groessen.setdefault(typ, []).append(z.worte[0].size)
    return {t: sum(g) / len(g) for t, g in groessen.items() if len(g) >= 3}


def lerne_raenge(zeilen: list[Zeile]) -> dict:
    """Rangfolge der Gliederungszeichen aus der Einrückung lernen.

    VII.179.: «IV.» > «a)» > «1.»; VII.249.: «27.» > «a)». Eine Marke unter einer anderen
    (eingerückt oder direkt nach einer Überschrift aus römischer Zahl/Grossbuchstabe) ist tiefer."""
    stimmen: Counter = Counter()
    vorher = None
    groessen: dict[str, list[float]] = {}
    for z in zeilen:
        typ = _marken_typ(z)
        if typ is None:
            continue
        groessen.setdefault(typ, []).append(z.worte[0].size)
        if vorher and vorher[0] != typ:
            if z.x0 > vorher[1] + 3 or (abs(z.x0 - vorher[1]) <= 3 and vorher[0] in ("roem", "gross")):
                stimmen[(vorher[0], typ)] += 1
        vorher = (typ, z.x0)
    kanten = {(a, b) for (a, b), n in stimmen.items() if n > stimmen.get((b, a), 0)}
    # Marken in deutlich grösserer Schrift stehen höher («G. Baupolizei» 14 pt über «I. Personelles …» 12 pt am
    # selben Rand, V.G.c.50.) – auch gegen die Reihenfolge-Stimmen
    mittel = {t: sum(g) / len(g) for t, g in groessen.items() if len(g) >= 3}
    for a in mittel:
        for b in mittel:
            if a != b and mittel[a] >= mittel[b] + 1.5:
                kanten.discard((b, a))
                kanten.add((a, b))
    reihenfolge, offen = [], set(RANG)
    while offen:
        frei = [t for t in offen if not any((a, t) in kanten for a in offen if a != t)] or list(offen)
        wahl = min(frei, key=lambda t: RANG[t])
        reihenfolge.append(wahl)
        offen.remove(wahl)
    return {t: i for i, t in enumerate(reihenfolge)}


def normalisiere_signatur(text: str) -> str:
    """«V.K. c.4.:1» -> «V.K.c.4.:1», «V.K. c 4.:3» -> «V.K.c.4.:3», «V.E..c.11.:6» -> «V.E.c.11.:6»,
    «V.C: c.52.:1.2» -> «V.C.c.52.:1.2» (Doppelpunkt statt Punkt vor dem Rest des Bestands, V.C.c.52.)."""
    text = re.sub(r"^([IVX]{1,4}\.[A-Z]{1,3}):\s+(?=[a-z]\.)", r"\1. ", text)
    teile = text.split()
    aus = teile[0] if teile else ""
    for t in teile[1:]:
        aus += ("" if aus.endswith((".", ":")) else ".") + t
    return re.sub(r"\.{2,}", ".", aus)


def _ein_zeichen_anders(a: str, b: str) -> bool:
    """Unterscheiden sich a und b um genau ein eingefügtes, fehlendes oder anderes Zeichen?"""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    kurz, lang = sorted((a, b), key=len)
    return any(lang[:i] + lang[i + 1:] == kurz for i in range(len(lang)))


def _titelanfang(text: str) -> str:
    """Die ersten drei Wörter ohne Satzzeichen, klein («Kassenbuch und Journal»)."""
    return " ".join(re.sub(r"[^\w\s]", " ", text).lower().split()[:3])


def _ist_datumsfolge(rest: Zeile) -> bool:
    """Beginnt der Rest nach einer Nummer wie ein umgebrochenes Datum («19. Juni 1947», «1. März“, Zürich»)
    – und nicht wie ein Name («2. August Hoffmeister», «11.25. Aug. A. Lemaître»)?"""
    w = rest.worte
    monat = w[0].text
    if not MONAT_WORT_RE.match(monat.strip("„“”\"«»‚‘’'")):
        return False
    if monat not in ("August", "Aug.") or len(w) == 1:
        return True  # «6. April. Taiko Kiwa …», «15. Febr. Mme …», «März“,», Monat am Zeilenende: ein Datum
    nach = w[1].text  # nur «August» ist auch ein Vorname
    return not (nach[:1].isupper() and not re.match(rf"{JAHR}", nach))


def lies_signatur(z: Zeile, gl: Gliederung) -> SigTreffer | None:
    w = z.worte
    if gl.bestand and w and len(w) <= 14 and (all("Bold" in x.font for x in w) or min(x.size for x in w) >= 13.5) \
            and not re.match(r"(?:siehe|vgl\.)\b", z.text, re.I):
        mk = re.search(r"\(\s*([IVX]{1,4}\.\s?[^()]{1,40}?)\s*\)\s*$", z.text)
        sig = normalisiere_signatur(mk.group(1)) if mk else ""
        lokal = sig[len(gl.bestand):].lstrip(":") if sig.startswith(gl.bestand) else ""
        if lokal and re.fullmatch(r"(?:(?:[A-Z]{1,3}|\d{1,4}[a-z]?|[a-z])[.:]{1,2})*(?:[A-Z]{1,3}|\d{1,4}[a-z]?|[a-z])\.?",
                                  lokal) and len(z.text[:mk.start()].split()) >= 1:
            n = len(z.text[:mk.start()].split())
            rest = Zeile(z.seite, z.top, z.bottom, w[:n], z.datum, z.umfang, z.schachtel, z.spalten)
            if not gl.nur_pruefen:
                gl.stapel = []
            return SigTreffer(tuple(k for k in re.split(r"[.:]+", lokal) if k), sig[len(gl.bestand):], mk.group(1),
                              rest, "Bold" in w[0].font, "voll")
    if gl.klammer_voll:
        return None  # «Schachtel 1 (V.F. c.18.:1)» / «1. Inspektionsrapporte …»: die Nummern sind Positionen im Inhalt
    grenze = SIGNATUR_SPALTE_MAX_GLIEDERUNG if gl.modus == "gliederung" else SIGNATUR_SPALTE_MAX
    if not w or len(w) > 1 and w[0].size <= 7.5 and w[1].size > w[0].size + 2 and re.fullmatch(r"\d{1,3}", w[0].text):
        return None  # Fussnote mit hochgestellter Nummer «¹ KVA steht für …» (V.F.c.28., VII.416.)
    if w[0].x0 > grenze and not (gl.registratur and w[0].x0 <= 175):
        # dezimal: Unternummer der laufenden Einheit, stärker eingerückt («1.5. Ausstellungen» / «1.5.1. Exposition
        # de céramique suisse 1927» bei x 131, VII.174.)
        # angeklebter Titel «5.3.Denkschrift von Dr. Walther Frey» (VII.47.)
        m_kl = re.fullmatch(r"(\d{1,3}(?:\.\d{1,3})+\.)([A-ZÄÖÜ][a-zäöüß]\S*)", w[0].text)
        nr_text = m_kl.group(1) if m_kl else w[0].text
        folge = m_kl.group(2) if m_kl else (w[1].text if len(w) > 1 else "")
        neu = tuple(nr_text.rstrip(".").split("."))
        eigen = gl.kind_von[1:] if gl.buchstaben and gl.kind_von[:1] == (gl.abschnitt,) else gl.kind_von
        erstes_kind = neu[:-1] == eigen and neu[-1] == "1"
        naechstes = len(eigen) >= 2 and neu[:-1] == eigen[:-1] and eigen[-1].isdigit() \
            and neu[-1] == str(int(eigen[-1]) + 1)
        # zurück zur nächsten Nummer einer höheren Stufe: «2.3.8.» / «2.4. Allgemeine Korrespondenz» (VII.47.)
        aufwaerts = 2 <= len(neu) < len(eigen) and neu[:-1] == eigen[:len(neu) - 1] \
            and eigen[len(neu) - 1].isdigit() and neu[-1] == str(int(eigen[len(neu) - 1]) + 1)
        # Unternummer ohne Punkt angehängt: «2.3. Verschiedene Akten …» / «2.31. Nr. 9-20», «2.32. …» … «2.38.»,
        # «3.5. Mitgliedschaften» / «3.51 Totenregister» (VII.47.): 2.31. ist 2.3.1.
        kompakt = ()
        if len(neu) >= 2 and all(k.isdigit() for k in neu) and eigen and all(k.isdigit() for k in eigen):
            if neu[:-1] == eigen[:-1] and neu[-1] == eigen[-1] + "1":
                kompakt = eigen + ("1",)
            elif len(eigen) == len(neu) + 1 and neu[:-1] == eigen[:-2] \
                    and neu[-1] == eigen[-2] + str(int(eigen[-1]) + 1) and int(eigen[-1]) < 9:
                kompakt = eigen[:-1] + (str(int(eigen[-1]) + 1),)
        in_folge = erstes_kind or naechstes or aufwaerts or bool(kompakt)
        # (Unternummern stehen oft in der Titelspalte der Einheit: «V.J. c.402.:15. Personal» / «15.1. Erzieherinnen
        # … 1946-1966» bei x 170, V.J.c.402.; «7.1. Abschriften …» bei x 184, V.J.W.c.15.; letzter Punkt fehlt auch:
        # «7.4 Korrespondenz …», «2.54 Bereinigung …»)
        # die nächste Nummer darf auch klein weitergehen («6.4. ohne Datum Bestattungsplan …», VII.47.)
        if not ((gl.modus == "dezimal" or eigen) and eigen and w[0].x0 <= grenze + (120 if in_folge else 40)
                and (len(w) > 1 or m_kl)
                and re.fullmatch(r"\d{1,3}(?:\.\d{1,3})+\." + ("?" if in_folge else ""), nr_text) and in_folge
                and (folge[:1].isupper() or folge[:1].isdigit() or folge[:1] in TITELANFANG
                     or (naechstes and len(w) > 2 and folge[:1].islower()))):
            return None  # («1.2.1. 1. Generation: Hans Heinrich Diener», «2.4.1. 150 Jahre Diener», VII.199.)
        if kompakt and not m_kl:
            z2 = Zeile(z.seite, z.top, z.bottom, [Wort(pfad_text(kompakt), w[0].x0, w[0].x1, w[0].font, w[0].size)]
                       + w[1:], z.datum, z.umfang, z.schachtel, z.spalten)
            t = lies_signatur(z2, gl)
            if t is not None:
                t.anzeige = nr_text if nr_text.endswith(".") else nr_text + "."
                t.roh = w[0].text
                t.hinweis = " ".join(filter(None, (t.hinweis, f"Im Findmittel «{w[0].text}» – als Unternummer "
                                                              f"{pfad_text(kompakt)} von {pfad_text(kompakt[:-1])} "
                                                              "gelesen, bitte prüfen.")))
            return t
    erstes = w[0].text
    fett = "Bold" in w[0].font
    zweites = w[1].text if len(w) > 1 else ""
    # «1)» als Gliederungsnummer «1.»: fett über eingerückten «a)» (VII.170.) oder in der Spalte der fetten römischen
    # Stufen (V.G.c.107.); sonst ist es ein Aufzählungszeichen
    if gl.modus == "gliederung" and len(w) > 1 and re.fullmatch(r"\d{1,2}\)", erstes) \
            and (gl.klammer_zahlen and fett and w[0].x0 <= SIGNATUR_SPALTE_MAX
                 or gl.klammer_x is not None and abs(w[0].x0 - gl.klammer_x) <= 2):
        w0 = w[0]
        z2 = Zeile(z.seite, z.top, z.bottom, [Wort(erstes[:-1] + ".", w0.x0, w0.x1, w0.font, w0.size)] + w[1:],
                   z.datum, z.umfang, z.schachtel, z.spalten)
        t = lies_signatur(z2, gl)
        if t is not None:
            t.roh = erstes
        return t
    if gl.modus == "gliederung" and gl.klammer_x is not None and not gl.doppelmarken \
            and re.fullmatch(r"\d{1,3}\.", erstes) and w[0].x0 > gl.klammer_x + 25:
        return None  # Liste in der Textspalte: «B) Gutachten …» / «1. Nachtrag zum Gutachten» (V.G.c.107.)

    # 1) Vollsignatur samt Bestand: «VI.HO.A.1.», «VI.HO.B.1.:1», «VI.HO.A.1.-8.», «VI.HO.C.32.a:1»,
    #    auch mit Leerzeichen und Tippfehlern: «V.K. c.4.:1», «VII. 121.:1», «V.K. c 4.:3», «V.E..c.11.:6»
    if gl.bestand:
        kandidat, n_worte = normalisiere_signatur(erstes), 1
        punkt_ergaenzt = False
        if (not kandidat.startswith(gl.bestand) and re.match(r"[IVX]{1,4}(?:\.|$)", erstes)) \
                or (kandidat == gl.bestand and len(w) > 1 and re.match(r"[:.]?\d", zweites)):
            verwandt = None  # gleicher Aufbau mit «:», aber abweichender Bestandsteil (Tippfehler im Findmittel)

            def aehnlich(vorn_: str, hinten_: str) -> bool:
                # gleiche ersten zwei Teile («V.F. c.10.» / «V.F. b.10.») – oder ein Zeichen anders, wenn die Nummer
                # die Folge fortsetzt: «V.H. c.45.:9.» / «V.G. c.45.:10.» / «V.G. c.45.:11.» (V.H.c.45.)
                if vorn_.split(".")[:2] == gl.bestand.split(".")[:2]:
                    return True
                m_n = re.match(r"\d+", hinten_)
                return _ein_zeichen_anders(vorn_ if vorn_.endswith(".") else vorn_ + ".", gl.bestand) and bool(m_n) \
                    and len(gl.letzter_pfad) == 1 and gl.letzter_pfad[0].isdigit() \
                    and int(m_n.group()) == int(gl.letzter_pfad[0]) + 1
            for n in (1, 2, 3):
                verbunden = normalisiere_signatur(" ".join(x.text for x in w[:n]))
                # Bestand ohne Schlusspunkt vor dem Doppelpunkt: «V.F. b.13.b:1» bei V.F.b.13.b. (wie im Kopf «Stadtarchiv
                # Zürich V.F. b.13.b»)
                ohne_punkt = gl.bestand.endswith(".") and verbunden.startswith(gl.bestand[:-1] + ":")
                if ohne_punkt:  # (auch «V.B. c.5::72.» mit doppeltem Doppelpunkt, V.B.c.5.)
                    verbunden = gl.bestand + ":" + verbunden[len(gl.bestand):].lstrip(":")
                # (nicht schon beim blossen «:» aufhören: «V.A. c.115.: 76 Motion …», V.A.c.115.)
                if len(w) >= n and verbunden.startswith(gl.bestand) and verbunden[len(gl.bestand):].strip(":."):
                    kandidat, n_worte, verwandt = verbunden, n, None
                    punkt_ergaenzt = ohne_punkt
                    break
                vorn, _, hinten = verbunden.partition(":")
                if len(w) >= n and verwandt is None and hinten and gl.bestand.count(".") >= 3 \
                        and vorn.count(".") == gl.bestand.count(".") and aehnlich(vorn, hinten) \
                        and re.fullmatch(r"\d{1,4}[a-z]?\.?", hinten):
                    verwandt = (verbunden, n)
            if verwandt and not kandidat.startswith(gl.bestand):
                kandidat, n_worte = verwandt
        lokal = kandidat[len(gl.bestand):].lstrip(":") if kandidat.startswith(gl.bestand) else ""
        hinweis, anzeige_typo = "", ""
        if not lokal and not re.search(r"\d", gl.bestand) and re.match(r"[IVX]{1,4}\.", kandidat):
            # Bestand nur aus Buchstaben («IV.B.»): ein Zeichen Abweichung ist ein Tippfehler («V.B. 439.», «IV.V.41.»)
            for n in (1, 2, 3):
                verbunden = normalisiere_signatur(" ".join(x.text for x in w[:n]))
                mv = re.match(r"((?:[A-Za-z]{1,4}\.)+)(\d.*)$", verbunden)
                if len(w) >= n and mv and _ein_zeichen_anders(mv.group(1), gl.bestand):
                    kandidat, n_worte, lokal, anzeige_typo = verbunden, n, mv.group(2).lstrip(":"), mv.group(2)
                    hinweis = (f"Signatur «{verbunden}» passt nicht zum Bestand {gl.bestand} – Tippfehler im Findmittel? "
                               "Bitte prüfen.")
                    break
        if not lokal and ":" in kandidat and gl.bestand.count(".") >= 3:
            # gleicher Aufbau, aber ein abweichender Teil vor dem «:» – vermutlich ein Tippfehler im Findmittel
            vorn, _, hinten = kandidat.partition(":")
            gleich2 = vorn.split(".")[:2] == gl.bestand.split(".")[:2]
            m_n2 = re.match(r"\d+", hinten)
            folge = bool(m_n2) and len(gl.letzter_pfad) == 1 and gl.letzter_pfad[0].isdigit() \
                and int(m_n2.group()) == int(gl.letzter_pfad[0]) + 1
            if vorn.count(".") == gl.bestand.count(".") and (gleich2 or folge and _ein_zeichen_anders(vorn, gl.bestand)) \
                    and re.fullmatch(r"\d{1,4}[a-z]?\.?", hinten):
                lokal, anzeige_typo = hinten, ":" + hinten
                if vorn not in gl.weitere_bestaende:  # sonst ein anderer Bestand desselben Findmittels (V.L.162.:1)
                    hinweis = (f"Signatur «{kandidat}» passt nicht zum Bestand {gl.bestand} – Tippfehler "
                               "im Findmittel? Bitte prüfen.")
        # (auch ein kurzes Wort als Teil: «V.G. c.42.:Reg. 1 Zeichnungsverzeichnis» (V.G.c.42.), «:Va.», «:Vb.»
        # (V.J.W.c.51.))
        if lokal and re.fullmatch(r"(?:[^:]*[.:])?[A-Z][a-z]{1,3}\.?", lokal) and len(w) > n_worte + 1 \
                and re.fullmatch(r"\d{1,3}", w[n_worte].text) and w[n_worte + 1].text[:1].isupper():
            kandidat, n_worte = kandidat + w[n_worte].text, n_worte + 1  # «Reg.» + «1»
            lokal = kandidat[len(gl.bestand):].lstrip(":")
        # (auch römisch mit vier Zeichen und Buchstaben: «:VIII. Nachtrag …», «:VIIIa. Inhalts-Verzeichnis …»,
        # V.J.W.c.51.)
        m = re.fullmatch(r"((?:(?:[IVXL]{4,6}[a-z]?|[A-Z]{1,3}|[A-Z][a-z]{1,3}|\d{1,4}[a-z]?|[a-z])[.:]{1,2})*"
                         r"(?:[IVXL]{4,6}[a-z]?|[A-Z]{1,3}|[A-Z][a-z]{1,3}|\d{1,4}[a-z]?|[a-z]))"
                         r"[.:)]?(?:[-–](\d{1,4}[a-z]?)\.?)?", lokal) if lokal else None  # auch «6-7a» (VII.4.)
        angeklebt_voll = None
        if not m and lokal and n_worte >= 2:
            # Nummer und Titel ohne Leerzeichen: «V.A. c.115.: 120Referendum Stop dem Ausbau …» (V.A.c.115.)
            m_k = re.fullmatch(r"(\d{1,4})([A-ZÄÖÜ][a-zäöüß]{2,}\S*)", lokal)
            if m_k:
                m = re.fullmatch(r"(\d{1,4})()", m_k.group(1))
                angeklebt_voll = m_k.group(2)
                kandidat = kandidat[:len(kandidat) - len(lokal)] + m_k.group(1)
        if m:
            komps = tuple(k for k in re.split(r"[.:]+", m.group(1)) if k)
            if m.group(2):
                komps = komps[:-1] + (f"{komps[-1]}-{m.group(2)}",)
            if not gl.nur_pruefen:
                gl.stapel = []
            roh = " ".join(x.text for x in w[:n_worte])
            anzeige = anzeige_typo or kandidat[len(gl.bestand):]
            lp = gl.letzter_pfad
            if len(komps) == 1 and komps[0].isdigit() and len(lp) >= 2 and not lp[0].isdigit() and lp[1].isdigit() \
                    and int(komps[0]) == int(lp[1]) + 1 and not any(re.fullmatch(r"\d", x) for x in lp[:1]):
                # Abschnitt fehlt: «VI.SB.C.102.:3 Band 3» / «VI.SB.103. Hauptbuch der Gemeindewerke» / «VI.SB.C.103.:1
                # Band 1» (VI.SB.) ist VI.SB.C.103.
                hinweis = (f"Im Findmittel «{roh}» – als «{gl.bestand}{lp[0]}.{komps[0]}.» gelesen (Abschnitt {lp[0]} "
                           "fehlt), bitte prüfen.")
                komps = (lp[0], komps[0])
                anzeige = f"{lp[0]}.{komps[1]}."
                kandidat = f"{gl.bestand}{anzeige}"
                return SigTreffer(komps, anzeige, kandidat, z.ab(n_worte), fett, "voll", hinweis)
            if angeklebt_voll:
                rest_v = z.ab(n_worte)
                rest_v = Zeile(z.seite, z.top, z.bottom, [Wort(angeklebt_voll, w[n_worte - 1].x0 + 25, w[n_worte - 1].x1,
                                                               w[n_worte - 1].font, w[n_worte - 1].size)]
                               + (rest_v.worte if rest_v else []), z.datum, z.umfang, z.schachtel, z.spalten)
                return SigTreffer(komps, anzeige, roh[:len(roh) - len(angeklebt_voll)], rest_v, fett, "voll", hinweis)
            if punkt_ergaenzt:  # «V.F. b.13.b:1»: Schreibweise ohne Punkt nach dem Bestand, kein Tippfehler
                return SigTreffer(komps, anzeige, kandidat, z.ab(n_worte), fett, "voll", hinweis)
            if not hinweis and re.sub(r"\s", "", roh) != kandidat:
                hinweis = f"Signatur im Findmittel «{roh}» – als «{kandidat}» gelesen (Tippfehler?), bitte prüfen."
            return SigTreffer(komps, anzeige, roh, z.ab(n_worte), fett, "voll", hinweis)

    # 1a) Buchstabenabschnitt in einem dezimalen Findmittel («A. KORRESPONDENZ …», VII.140.)
    if gl.modus == "dezimal" and gl.buchstaben and _ist_buchstabenabschnitt(z):
        buchstabe = abschnittsmarke(erstes)
        if not gl.nur_pruefen:
            gl.abschnitt, gl.hauptnr = buchstabe, 0
        return SigTreffer((buchstabe,), f"{buchstabe}.", erstes, z.ab(1), fett, "gross")

    # 1b) «Jahr.Laufnummer» («1941.1 Gampel Lonza AG …»), wenn das Findmittel so nummeriert (lerne_nummern)
    #     auch «1939.37 a Schulhaus Zeltweg», «1938.46 – Bäckerstrasse 40», «1943.37 2. Schweiz. Modewoche»
    if gl.jahr_nummern and re.fullmatch(rf"{JAHR}\.\d{{1,4}}[a-z]?\.?", erstes) and len(w) == 1 and z.schachtel \
            and gl.letzter_pfad and re.fullmatch(rf"{JAHR}\.\d{{1,4}}[a-z]?", gl.letzter_pfad[-1]):
        # nur Signatur und Schachtel, ohne Titel: «1953.1418 Fusio Maggiawerke …» / «1953.1419 ¦ 121» (VII.308.E.a.)
        pfad = gl._setze("zahl", (erstes.rstrip("."),))
        return SigTreffer(pfad, erstes.rstrip("."), erstes, None, fett)
    if gl.jahr_nummern and re.fullmatch(rf"{JAHR}\.\d{{1,4}}[a-z]?\.?", erstes) and z.ab(1):
        # (auch «1973.9a Küsnacht …» nach «1973.9», «1937.524a» / «1937.524b», VII.308.F.a., VII.308.E.a.)
        nummer, n_sig = erstes.rstrip("."), 1
        if re.fullmatch(r"[a-z]", zweites) and len(w) > 2:
            nummer, n_sig = nummer + zweites, 2
        rest = z.ab(n_sig)
        if rest and not _ist_datumsfolge(rest) and not re.fullmatch(JAHR, rest.worte[0].text):
            pfad = gl._setze("zahl", (nummer,))
            return SigTreffer(pfad, nummer, " ".join(x.text for x in w[:n_sig]), rest, fett)

    # 1c) «40a, 40b Verträge, Bauabrechnungs- und Rechnungsdoppel» (VII.80.): zwei Nummern zusammen verzeichnet
    paar = re.fullmatch(r"(\d{1,4})([a-z]),", erstes)
    if paar and gl.modus == "gliederung" and re.fullmatch(rf"{paar.group(1)}[a-z]", zweites) and len(w) > 2:
        if _folgt(gl, "zahl", int(paar.group(1)), fett):
            pfad = gl._setze("zahl", (paar.group(1) + paar.group(2),))
            return SigTreffer(pfad, pfad_text(pfad), f"{erstes} {zweites}", z.ab(2), fett,
                              hinweis=f"Im Findmittel zusammen verzeichnet: «{erstes} {zweites}» – Signatur aus der "
                                      "ersten Nummer gebildet, bitte prüfen.")
        return None

    # 1c') Registraturplan (V.F.c.28.): «010 Gesetzliche Grundlagen» (x 71), «011 Gesetze …» bzw. «1. Pressemitteilungen»
    #      unter «744» (x 120), «013.1 Verbot …» (x 156) – Ebene aus der Einrückung, Signatur = Code
    if gl.registratur and len(w) > 1:
        ebene = 1 if w[0].x0 <= 95 else 2 if w[0].x0 <= 140 else 3 if w[0].x0 <= 175 else 0
        if re.fullmatch(r"\d{3}(?:\.\d{1,3})*\.\d{3}(?:\.\d{1,3})*", erstes):
            return None  # «802 Dubletten» / «440.733.3 Schlussbericht …»: Verweis auf eine andere Position
        code = erstes if re.fullmatch(r"\d{3}[a-z]?(?:/\d{3})?(?:\.\d{1,2})*", erstes) else ""  # auch «730a» (V.F.c.28.)
        oben = [c for e_, c in gl.reg_stapel if e_ < ebene]
        geschwister = [c for e_, c in gl.reg_stapel if e_ == ebene]
        hinweis = ""
        if code and ebene >= 2 and oben and code[:1] != oben[-1][:1] and re.fullmatch(r"\d{3}", oben[-1]):
            # andere Hundertergruppe als die Position darüber: eine Unternummer («712 Verträge …» /
            # «109 Wärmelieferungsverträge» = 712.109, Fussnote 9), nicht «600» / «610 Vergütungen»
            code = f"{oben[-1]}.{code}"
        if not code and ebene >= 2 and oben:
            m_nr = re.fullmatch(r"(\d{1,3})(\.?)", erstes)
            m_unter = re.fullmatch(r"(\d{1,2})((?:\.\d{1,2})+)\.?", erstes)
            if m_nr and m_nr.group(2):
                code = f"{oben[-1]}.{m_nr.group(1)}"  # «744» / «1. Pressemitteilungen» = 744.1, auch «100.»
            elif m_nr and geschwister and geschwister[-1].startswith(oben[-1] + ".") \
                    and geschwister[-1].rsplit(".", 1)[-1].isdigit() \
                    and int(m_nr.group(1)) == int(geschwister[-1].rsplit(".", 1)[-1]) + 1:
                code = f"{oben[-1]}.{m_nr.group(1)}"  # «6. …» / «7 Wiedererwägung …» (Punkt fehlt)
                hinweis = f"Im Findmittel «{erstes}» ohne Punkt – als Unterposition {code} gelesen, bitte prüfen."
            elif m_unter and oben[-1].rsplit(".", 1)[-1] == m_unter.group(1):
                code = f"{oben[-1]}{m_unter.group(2)}"  # «702» / «5. Schlacken…» / «5.1 Ingenieurofferten» = 702.5.1
        if code and oben and code == oben[-1]:
            return None  # «020 Planung und Organisation» / «020 Allgemeine Akten»: Inhalt der Position selbst
        if code and ebene:
            rest = z.ab(1)
            if rest and rest.worte[-1].text in ("-", "–") and rest.worte[-1].x0 >= 480 and len(rest.worte) > 1:
                rest = Zeile(rest.seite, rest.top, rest.bottom, rest.worte[:-1], rest.datum, rest.umfang,
                             rest.schachtel, rest.spalten)
                hinweis = " ".join(filter(None, (hinweis, "Laut Findmittel keine Unterlagen («-» in der "
                                                                   "Schachtelspalte).")))
            if not gl.nur_pruefen:
                gl.reg_stapel = [(e_, c) for e_, c in gl.reg_stapel if e_ < ebene] + [(ebene, code)]
            pfad = tuple(oben) + (code,)
            return SigTreffer(pfad, code, erstes, rest, fett, "zahl", hinweis)

    # 1d) Teil-Überschrift in grosser Schrift «1. Alfred G. C. Wedekind-Güttinger» / «2. Myrthe …» (VII.232.):
    #     oberste Ebene, darunter beginnt die Buchstabenfolge neu
    if gl.modus == "gliederung" and gl.teil_groesse and re.fullmatch(r"\d{1,2}\.", erstes) and len(w) > 1 \
            and min(x.size for x in w) >= gl.teil_groesse - 0.5:
        pfad = gl._setze("teil", (erstes[:-1],))
        return SigTreffer(pfad, pfad_text(pfad), erstes, z.ab(1), fett, "teil")

    # 1e) Dezimalzahl mit Leerzeichen «6. 5. Komitee pro Tanne-Liquidation» nach «6.4.» (VII.296.): als «6.5.»,
    #     wenn es die nächste Nummer ist
    if gl.modus == "dezimal" and len(w) > 2 and re.fullmatch(r"\d{1,3}\.", erstes) \
            and re.fullmatch(r"\d{1,3}\.", zweites) and w[1].x0 - w[0].x1 < 10:
        eigen = gl.kind_von[1:] if gl.buchstaben and gl.kind_von[:1] == (gl.abschnitt,) else gl.kind_von
        komb = (erstes[:-1], zweites[:-1])
        if len(eigen) >= 2 and eigen[0] == komb[0] and eigen[1].isdigit() and int(komb[1]) == int(eigen[1]) + 1 \
                or eigen == komb[:1] and komb[1] == "1":
            z2 = Zeile(z.seite, z.top, z.bottom, [Wort(erstes + zweites, w[0].x0, w[1].x1, w[0].font, w[0].size)]
                       + w[2:], z.datum, z.umfang, z.schachtel, z.spalten)
            t = lies_signatur(z2, gl)
            if t is not None:
                t.roh = f"{erstes} {zweites}"
                t.hinweis = t.hinweis or f"Im Findmittel «{erstes} {zweites}» mit Leerzeichen – als «{erstes}{zweites}» " \
                                         "gelesen."
                return t

    # 1f) zwei aufeinanderfolgende Nummern als eine Einheit: «20./21. Telegramm und Brief …» (VII.380.),
    #     «594 / 595 Murg Spinnerei Murg AG» (VII.308.D.a.)
    paar = None
    if re.fullmatch(r"\d{1,4}\./\d{1,4}\.", erstes):
        paar = (*erstes[:-1].split("./"), 1)
    elif re.fullmatch(r"\d{1,4}/\d{1,4}", erstes) and len(w) > 1 and not re.fullmatch(r"\d{1,4}", zweites):
        paar = (*erstes.split("/"), 1)  # «3/4 II. Jahresberichte (ausführliche)» in einer Schachtelliste (V.L.73.)
    elif re.fullmatch(r"\d{1,4}", erstes) and zweites == "/" and len(w) > 3 and re.fullmatch(r"\d{1,4}", w[2].text):
        paar = (erstes, w[2].text, 3)
    unterzaehlung = gl.modus == "gliederung" and gl.einrueck_x is not None and w[0].x0 > gl.einrueck_x
    # (sonst nur als nächste Nummer der Folge: «2 I. Allgemeines …» / «3/4 II. Jahresberichte …», V.L.73.)
    bisher_nr = gl.hauptnr if gl.modus == "dezimal" else gl.letzte.get(("zahl", gl._praefix("zahl")), 0)
    folgt_paar = bool(paar) and bisher_nr > 0 and int(paar[0]) == bisher_nr + 1 and w[0].x0 <= SIGNATUR_SPALTE_MAX
    if paar and int(paar[1]) == int(paar[0]) + 1 and (gl.freie_nummern or unterzaehlung or folgt_paar):
        a, b, n_paar = paar
        punkt = "." if erstes.endswith(".") else ""
        z2 = Zeile(z.seite, z.top, z.bottom, [Wort(a + punkt, w[0].x0, w[n_paar - 1].x1, w[0].font, w[0].size)]
                   + w[n_paar:], z.datum, z.umfang, z.schachtel, z.spalten)
        t = lies_signatur(z2, gl)
        if t is not None and t.pfad and t.pfad[-1] == a and t.typ != "voll":
            if not gl.nur_pruefen:  # die nächste Nummer folgt auf die zweite («10/11» / Schlussvermerk «11. 2. 1987»)
                if gl.modus == "dezimal":
                    gl.hauptnr = max(gl.hauptnr, int(b))
                else:
                    schluessel = ("zahl", gl._praefix("zahl"))
                    if gl.letzte.get(schluessel) == int(a):
                        gl.letzte[schluessel] = int(b)
            t.pfad = t.pfad[:-1] + (f"{a}/{b}",)
            t.anzeige = pfad_text(t.pfad) if gl.modus != "dezimal" else t.anzeige[:-len(a) - 1] + f"{a}/{b}."
            t.roh = " ".join(x.text for x in w[:n_paar])
            return t
        return None

    # 2) Dezimalzahlen: «2.1.1.», «2.4.2.2», «5.2.4.25 .», «5.2.4.25.Aufführungen», «1.a.»
    rest_ab, angeklebt = 1, None
    # Nummer mit Leerzeichen «20. 2. Plakate der Tonhalle-Gesellschaft, undatiert» nach 20.1. (VII.151.)
    # (auch mehrstufig: «7. 2.3. Raffaele Ciampini, Filellenismo …» nach 7.2.2., VII.510.)
    if len(w) > 2 and re.fullmatch(r"\d{1,3}\.", erstes) and re.fullmatch(r"\d{1,3}(?:\.\d{1,3})*\.", zweites) \
            and (gl.kind_von or gl.letzter_pfad):
        eigen, kv = gl.kind_von or gl.letzter_pfad, (erstes[:-1],) + tuple(zweites[:-1].split("."))
        if (kv[:-1] == eigen and kv[-1] == "1") or (
                len(eigen) >= len(kv) and eigen[:len(kv) - 1] == kv[:-1] and eigen[len(kv) - 1].isdigit()
                and int(kv[-1]) == int(eigen[len(kv) - 1]) + 1):
            z2 = Zeile(z.seite, z.top, z.bottom, [Wort(erstes + zweites, w[0].x0, w[1].x1, w[0].font, w[0].size)]
                       + w[2:], z.datum, z.umfang, z.schachtel, z.spalten)
            t = lies_signatur(z2, gl)
            if t is not None:
                t.hinweis = (t.hinweis + " " if t.hinweis else "") + \
                    f"Im Findmittel «{erstes} {zweites}» mit Leerzeichen – als «{erstes}{zweites}» gelesen."
                return t
    # erste Stelle römisch geschrieben: «IV.4.1. Mappe 9:» zwischen «4.4.1. Mappe 8:» und «4.4.1. Mappe 10:» (VII.237.)
    # – dieselbe Nummer wie die laufende Einheit, als 4.4.1. gelesen
    m_rv = re.fullmatch(r"([IVX]{1,4})\.((?:\d{1,3}\.)+)", erstes) if gl.modus == "dezimal" and len(w) > 1 else None
    if m_rv and (gl.kind_von or gl.letzter_pfad):
        werte = {"I": 1, "V": 5, "X": 10}
        roem = m_rv.group(1)
        zahl = sum(werte[c] if k + 1 == len(roem) or werte[c] >= werte[roem[k + 1]] else -werte[c]
                   for k, c in enumerate(roem))
        kand_r = (str(zahl),) + tuple(m_rv.group(2)[:-1].split("."))
        if kand_r == (gl.kind_von or gl.letzter_pfad):
            z2 = Zeile(z.seite, z.top, z.bottom, [Wort(pfad_text(kand_r), w[0].x0, w[0].x1, w[0].font, w[0].size)]
                       + w[1:], z.datum, z.umfang, z.schachtel, z.spalten)
            t = lies_signatur(z2, gl)
            if t is not None:  # («Nr. im PDF» bleibt «IV.4.1.»; der Hinweis ohne «Tippfehler», sonst gilt die Form
                # als berichtigte Vollsignatur ohne Doppelpunkt, siehe signatur())
                t.roh = erstes
                t.hinweis = (t.hinweis + " " if t.hinweis else "") + \
                    f"Im Findmittel «{erstes}» mit römischer erster Stelle – als «{pfad_text(kand_r)}» gelesen " \
                    "(wohl verschrieben), bitte prüfen."
                return t
    # Unternummer mit Stückzahl ohne Punkt vor «:»: «28.3.25:1–2 Schema der electrischen Beleuchtung …» wie die Nachbarn
    # «28.3.7.:1–4 Stadttheater Zürich. Bühnenhaus» (VII.12.B.)
    m_dp = re.fullmatch(r"(\d{1,3}(?:\.\d{1,4})+):(\d.*)", erstes) if gl.modus == "dezimal" else None
    if m_dp:
        z2 = Zeile(z.seite, z.top, z.bottom, [Wort(f"{m_dp.group(1)}.:{m_dp.group(2)}", w[0].x0, w[0].x1, w[0].font,
                                                   w[0].size)] + w[1:], z.datum, z.umfang, z.schachtel, z.spalten)
        t = lies_signatur(z2, gl)
        if t is not None:
            t.roh = erstes
        return t
    # eingerückte, je Gruppe neu gezählte Nummern sind eine eigene Ebene unter der Nummer davor
    zahltyp = "zahl2" if gl.modus == "gliederung" and gl.einrueck_x and w[0].x0 > gl.einrueck_x else "zahl"
    m = DEZIMAL_RE.match(erstes)
    doppelpunkt_hinweis = ""
    if not m and re.fullmatch(r"\d{1,3}(?:\.\d{1,4}){1,6}\.\.", erstes):
        m = DEZIMAL_RE.match(erstes[:-1])  # «1.1.1018.. Georg(es) Boner an Alice Boner» (VII.389.)
        doppelpunkt_hinweis = f"Im Findmittel «{erstes}» mit doppeltem Punkt – als «{erstes[:-1]}» gelesen."
        # fehlender Punkt dazu: «14.316..» nach «14.3.15.» ist «14.3.16.» (VII.423.)
        eigen = gl.kind_von
        naechstes = eigen[:-1] + (str(int(eigen[-1]) + 1),) if eigen and eigen[-1].isdigit() else ()
        if naechstes and erstes[:-2].replace(".", "") == "".join(naechstes) and erstes[:-2] != ".".join(naechstes):
            m = DEZIMAL_RE.match(pfad_text(naechstes))
            doppelpunkt_hinweis = (f"Im Findmittel «{erstes}» – als «{pfad_text(naechstes)}» gelesen (nächste Nummer "
                                   f"nach {pfad_text(eigen)}), bitte prüfen.")
    if not m and re.fullmatch(r"\d{1,3}(?:\.\d{1,4})*\.\.\d{1,4}(?:\.\d{1,4})*\.?", erstes):
        # doppelter Punkt mitten in der Nummer: «10.5..2.» nach «10.5.1.» ist «10.5.2.» (V.F.c.150.)
        m = DEZIMAL_RE.match(re.sub(r"\.\.+", ".", erstes))
        doppelpunkt_hinweis = f"Im Findmittel «{erstes}» mit doppeltem Punkt – als «{re.sub(r'[.]{2,}', '.', erstes)}» gelesen."
    if m and re.fullmatch(rf"(?:0?[1-9]|[12]\d|3[01])\.(?:0?[1-9]|1[0-2])\.{JAHR}\.?", erstes):
        return None  # «18.12.1869 Schiller Der Neffe als Onkel» ist ein Datum, keine Signatur
    if m and re.fullmatch(r"(?:0?[1-9]|[12]\d|3[01])\.(?:0?[1-9]|1[0-2])\.\d{4}\.?", erstes) \
            and (re.fullmatch(r"0\d{3}", erstes.split(".")[2])
                 or re.fullmatch(rf"(?:0?[1-9]|[12]\d|3[01])\.(?:0?[1-9]|1[0-2])\.{JAHR}", zweites)):
        return None  # Tippfehler im Jahr: «01.12.0982 31.12.1982 - Dezember-Programmvorschau» (VII.411.) ist ein Datum
    if m and re.fullmatch(rf"(?:0?[1-9]|1[0-2])\.{JAHR}\.?", erstes) and not gl.jahr_nummern:
        return None  # «2.1939 Die Stellung der Stadt Zürich im Kanton» in einer datierten Liste (VII.109.): Monat.Jahr
    if m and len(w) > 2 and re.fullmatch(r"(?:0?[1-9]|[12]\d|3[01])\.", erstes) \
            and re.fullmatch(r"(?:0?[1-9]|1[0-2])\.", zweites) and re.fullmatch(rf"{JAHR}[,;.]?", w[2].text):
        return None  # «11. 2. 1987 / Hb; 7. 8. 1992 auf System übertragen» (Schlussvermerk, V.L.73.): ein Datum
    if m and len(w) == 1 and re.fullmatch(r"(?:0?[1-9]|[12]\d|3[01])\.(?:0?[1-9]|1[0-2])\.\d\d", erstes):
        return None  # «Lohn-Verteiler vom Zahltag 09.01.-» / «22.01.56»: umbrochenes Datum (VII.174.)
    titelanfang = len(w) > 1 and (w[1].text[:1].isupper() or w[1].text[:1] in TITELANFANG)
    # Unterpunkte «2a», «2b» ohne Punkt direkt unter «2. ZEITUNGSAUSSCHNITTE (1869-1957)» (VII.197.): Einheiten unter 2.
    #   («2a» nur gleich nach der Titelzeile von «2.»; nicht «3a Vertrag …» in einer Aktenplan-Tabelle unter «3. Akten»,
    #   VII.11.)
    m_ua = re.fullmatch(r"(\d{1,3})([a-z])", erstes) if gl.modus == "gliederung" and gl.punktnummern else None
    if m_ua and titelanfang and gl.letzter_pfad and gl.letzte_marke and abs(w[0].x0 - gl.letzte_marke[0]) <= 3:
        lp = gl.letzter_pfad
        if m_ua.group(2) == "a" and lp[-1] == m_ua.group(1) and gl.inhalt_zeilen <= 1:
            basis_u = lp
        elif m_ua.group(2) != "a" and lp[-1] == m_ua.group(1) + chr(ord(m_ua.group(2)) - 1):
            basis_u = lp[:-1]
        else:
            basis_u = ()
        if basis_u:
            return SigTreffer(basis_u + (erstes,), pfad_text(basis_u)[:-1] + m_ua.group(2), erstes, z.ab(1), fett, "zahl",
                              hinweis=f"Im Findmittel «{erstes}» unter {pfad_text(basis_u)} – als Unterpunkt übernommen.")
    if not m and gl.modus == "gliederung" and gl.punktnummern and re.fullmatch(r"\d{1,4}[a-z]\.", erstes) \
            and titelanfang:
        m = re.match(r"(\d{1,4}[a-z])", erstes)  # «3a. Tabellarisches Hauptbuch» nach «3. Band» (VII.15.)
    if not m and gl.modus == "dezimal" and re.fullmatch(r"\d{1,3}(?:\.\d{1,4})*\.\d{1,4}[a-z]\.?", erstes) \
            and titelanfang:
        # «1.23a. Besuch beim Barden Bernold» nach «1.23.» (VII.146.), «430.1.733.1a Allgemeine Sanitätstarife»
        # (V.F.c.29.)
        m = re.match(r"(\d{1,3}(?:\.\d{1,4})*\.\d{1,4}[a-z])", erstes)
    # Behälterbereich in einer Übersicht mit durchgezählten Einheiten: «Schachtel Nr. 1 – 14 ¦ Eidg. und kant. Beschlüsse
    # …», «Bände Nr. 15 – 25 ¦ Kontrollbücher …», «Schachteln Nr. 85, 86 ¦ Widerhandlungen …», «Band Nr. 164 ¦
    # Milchversorgung» unter «I. Grundlagen …» (VII.60.; das Detailverzeichnis liegt nicht im PDF) – eine Einheit
    # Bestand:1-14 unter der Gruppe, kein Darin der Gruppe
    # (auch allein neben einem zweizeiligen Titel: «Informationsplakate … betr.» / «Band Nr. 164» / «Milchversorgung»)
    m_bb = re.match(r"(?:Schachtel|Schachteln|Band|Bände|Mappe|Mappen)(?:\s+(?:u\.|und)\s+(?:Schachteln?|Bände|Mappen?))?"
                    r"\s+Nrn?\.\s+(\d{1,4})(?:\s*(?:[–-]|,|und)\s*(\d{1,4}))?(?:\s+(?=\S)|\s*$)", z.text) \
        if gl.modus == "gliederung" and len(w) >= 3 and w[0].x0 <= SIGNATUR_SPALTE_MAX else None
    if m_bb and gl.stapel:
        n_bb = len(z.text[:m_bb.end()].split())
        if (n_bb < len(w) and w[n_bb].x0 - w[n_bb - 1].x1 >= 6 and (w[n_bb].text[:1].isupper()
                                                                    or w[n_bb].text[:1] in TITELANFANG)) \
                or (n_bb == len(w) and gl.vorschau[:1].isupper()):
            a, b = m_bb.group(1), m_bb.group(2)
            bereich = f"{a}-{b}" if b and int(b) > int(a) else a
            pfad = gl._setze("zahl", (bereich,))
            return SigTreffer(pfad, bereich, " ".join(x.text for x in w[:n_bb]), z.ab(n_bb), fett,
                              hinweis=f"Im Findmittel «{' '.join(x.text for x in w[:n_bb])}» – als Einheit {bereich} "
                                      "übernommen (Übersicht, die einzelnen Nummern sind hier nicht verzeichnet), "
                                      "bitte prüfen." if b else "")
    m_rb = re.fullmatch(r"(\d{1,3})-(\d{1,3})\.", erstes) if gl.modus == "gliederung" and gl.punktnummern else None
    if not m and m_rb and titelanfang and int(m_rb.group(1)) < int(m_rb.group(2)) \
            and int(m_rb.group(1)) == gl.letzte.get(("zahl", gl._praefix("zahl")), 0) + 1:
        # Bereich «1-3. Sitzungsprotokolle ¦ 1840-1894 ¦ 3 Bd.» / «1. Band», «2. Band», «3. Band» (VII.15.): eine
        # Bereichseinheit über den einzelnen Nummern
        a, b = m_rb.group(1), m_rb.group(2)
        pfad = gl._setze("zahl", (f"{a}-{b}",))
        if not gl.nur_pruefen:
            gl.letzte[("zahl", gl._praefix("zahl"))] = int(a) - 1  # die erste Nummer des Bereichs folgt noch
        return SigTreffer(pfad, f"{a}-{b}.", erstes, z.ab(1), fett,
                          hinweis=f"Im Findmittel «{erstes}» – als Bereich {a}-{b} über den einzelnen Nummern "
                                  "übernommen, bitte prüfen.")
    if not m and gl.modus == "gliederung" and not gl.punktnummern \
            and re.fullmatch(r"\d{1,4}(?:[a-z]|[A-Z][a-z]?)", erstes) and titelanfang:
        # (auch «1Aa Gemeindegut, Ordentlicher Verkehr», «1B …» nach «1» (V.C.c.61.))
        # (nicht, wenn die Signaturen einen Punkt tragen: dann ist «6a Sammlungen im allgemeinen ¦ 15» eine
        # Aktenplan-Nummer in einer Tabelle, VII.11.)
        m = re.match(r"(\d{1,4}(?:[a-z]|[A-Z][a-z]?))", erstes)  # «50a Publikationen, Drucksachen …» nach «50» (VII.80.)
    if not m:
        # angeklebter Titel nach einer Buchstabenstelle: «7.2.1.c.1967/68» (Wörter ohne Abstand, VII.209.) ist 7.2.1.c.
        m2 = re.match(r"^(\d{1,3}(?:\.\d{1,4})+\.[a-z])\.(?=[^\s.])(.+)$", erstes) if gl.modus == "dezimal" else None
        m2 = m2 or DEZIMAL_ANGEKLEBT_RE.match(erstes)
        if m2:
            m, angeklebt = m2, m2.group(2)
            # (Blattangabe «28.3.7.:1–4 Stadttheater Zürich. Bühnenhaus» ist kein Titel; sie bleibt in «Nr. im PDF»,
            # VII.12.B.)
            if re.fullmatch(r":\d{1,4}(?:\s?[–-]\s?\d{1,4})?", angeklebt) and len(w) > 1:
                angeklebt = None
    # Nummer mit Bandzählung «3 : 1 – 3 Protokoll des Arbeitsausschusses … 3 Bände» (VII.80.): eine Einheit «3:1-3»
    band = ""
    if m and gl.modus != "dezimal" and len(w) > 5 and re.fullmatch(r"\d{1,4}", erstes) and w[1].text == ":" \
            and re.fullmatch(r"\d{1,2}", w[2].text) and w[3].text in ("–", "-") and re.fullmatch(r"\d{1,2}", w[4].text) \
            and int(w[2].text) < int(w[4].text):
        band = f"{w[2].text}-{w[4].text}"
    if m:
        nummer = m.group(1)
        if band:
            rest_ab = 5
        elif zweites == ".":
            rest_ab = 2
        elif gl.modus == "gliederung" and re.fullmatch(r"\d{1,4}", erstes) and re.fullmatch(r"[a-z]", zweites) \
                and len(w) > 2 and (w[2].text[:1].isupper() or w[2].text[:1] in TITELANFANG):
            nummer, rest_ab = nummer + zweites, 2  # «622 a Reckingen Rheinkraftwerk» (VII.308.D.a.)
        komps = tuple(nummer.split("."))
        hinweis = doppelpunkt_hinweis
        if gl.modus == "dezimal" and len(komps) == 2 and komps[1] == "1" and komps[0].isdigit() and gl.hauptnr \
                and int(komps[0]) == gl.hauptnr + 1 and gl.letzter_pfad == (str(gl.hauptnr),) \
                and gl.naechste_dezimal.rstrip(".") == f"{gl.hauptnr}.1.1":
            # «10. Bildarchiv» / «11.1. Stadt Zürich» / «10.1.1. Rechtes Limmatufer» (VII.374., Inhaltsverzeichnis
            # «10.1. Stadt Zürich»): Tippfehler in der Hauptnummer
            hinweis = (f"Im Findmittel «{erstes}», nach {gl.hauptnr}. und vor {gl.hauptnr}.1.1. aber {gl.hauptnr}.1. – "
                       "Signatur angepasst, bitte prüfen.")
            komps, nummer = (str(gl.hauptnr), "1"), f"{gl.hauptnr}.1"
        if gl.modus == "dezimal" and gl.buchstaben and gl.abschnitt.isdigit() and gl.hauptnr == 0 \
                and len(komps) == 2 and komps == (str(int(gl.abschnitt)), "1"):
            # «05 PRODUKTION» / «5.1. Produktion allgemein» / «1.1. Ofenleistung …»: die Abschnittsnummer ist
            # vor die erste Nummer geraten (VII.174., in der Zusammenfassung «1. Produktion allgemein»)
            hinweis = (f"Im Findmittel «{erstes}», als erste Nummer im Abschnitt {gl.abschnitt} aber «1.» – "
                       "Signatur angepasst, bitte prüfen.")
            komps, nummer = ("1",), "1"
        rest = z.ab(rest_ab)
        if angeklebt:
            rest = Zeile(z.seite, z.top, z.bottom,
                         [Wort(angeklebt, w[0].x0 + 40, w[0].x1, w[0].font, w[0].size)] + (rest.worte if rest else []),
                         z.datum, z.umfang)
        roh_doppelt = ""
        if rest and rest.worte[0].text in (erstes, nummer + "."):  # Tippfehler «1. 1. Manuskripte»
            rest = rest.ab(1)
        elif gl.modus == "dezimal" and fett and len(komps) == 1 and komps[0].isdigit() and rest and len(rest.worte) > 1 \
                and re.fullmatch(r"\d{1,3}\.", rest.worte[0].text) \
                and int(rest.worte[0].text[:-1]) == int(komps[0]) - 1 == gl.hauptnr + 1:
            # «4. 4. Vorschlag …», leeres «5.», «6. 5. Brückenbauten», «7. 6. Brücken im Sihltal» (fett, VII.76.): vor
            # der getippten Nummer steht eine automatische, die durch einen leeren Absatz verrutscht ist
            roh_doppelt = f"{erstes} {rest.worte[0].text}"
            nummer = rest.worte[0].text[:-1]
            komps = (nummer,)
            rest = rest.ab(1)
            hinweis = (f"Im Findmittel «{roh_doppelt}» mit zwei Nummern – als «{nummer}.» gelesen (fortlaufende "
                       "Zählung), bitte prüfen.")
        folgewort = rest.worte[0].text if rest else ""
        # «6.3. 1351 - 1951. Zürich 600 Jahre …» direkt nach 6.2.: die nächste Nummer mit einem Titel, der mit
        # Jahren beginnt – kein Datum «6. März 1351» (V.L.111.)
        eigen = gl.kind_von[1:] if gl.buchstaben and gl.kind_von[:1] == (gl.abschnitt,) else gl.kind_von
        naechste = gl.modus == "dezimal" and len(komps) >= 2 and len(eigen) >= len(komps) - 0 \
            and all(k.isdigit() for k in komps) and komps[:-1] == eigen[:len(komps) - 1] \
            and eigen[len(komps) - 1:len(komps)] and eigen[len(komps) - 1].isdigit() \
            and int(komps[-1]) == int(eigen[len(komps) - 1]) + 1 and rest is not None and len(rest.worte) >= 3
        # ebenso das erste Kind mit blossem Zeitraum als Titel: «2.6. Interpellationen» / «2.6.1. 1937 – 1943 ¦ 1930 –
        # 1943» (V.B.c.51.; drei Stellen, also kein Datum)
        naechste = naechste or gl.modus == "dezimal" and len(komps) >= 3 and all(k.isdigit() for k in komps) \
            and komps[:-1] == tuple(eigen) and komps[-1] == "1" and rest is not None and len(rest.worte) >= 3
        # Tabelle «Nummer ¦ Jahrgang ¦ Titel»: «1. ¦ 1982 ¦ Das Corso-Theater vor 75 Jahren», «2. ¦ 1983 ¦ …» (VII.164.) –
        # das Jahr steht in einer eigenen Spalte, die Nummer setzt die Folge fort: kein Datum «1. 1982»
        jahrspalte = gl.modus == "gliederung" and len(komps) == 1 and komps[0].isdigit() and erstes.endswith(".") \
            and rest is not None and len(rest.worte) >= 3 and re.fullmatch(JAHR, folgewort) is not None \
            and rest.worte[0].x0 - w[0].x1 >= 15 and rest.worte[1].x0 - rest.worte[0].x1 >= 15 \
            and int(komps[0]) == gl.letzte.get(("zahl", gl._praefix("zahl")), 0) + 1
        if ((rest and _ist_datumsfolge(rest)) or re.match(rf"^{JAHR}$", folgewort)) and not naechste and not jahrspalte:
            return None  # «19. Juni 1947», «8. Okt. 1980 …», «1. März“, Zürich» – umgebrochenes Datum
        if jahrspalte and not z.datum:
            z.datum = folgewort  # der Jahrgang ist die Datierung, nicht Teil des Titels
            rest = rest.ab(1)
            folgewort = rest.worte[0].text
        if gl.mengenzahlen and len(komps) == 1 and rest_ab == 1 and re.fullmatch(r"\d{1,3}", erstes):
            return None  # «1 Verzeichnis 1780» in einem Findmittel, dessen blosse Zahlen Mengen sind
        if gl.punktnummern and gl.modus != "dezimal" and len(komps) == 1 and rest_ab == 1 and not band \
                and re.fullmatch(r"\d{1,3}", erstes) \
                and (int(erstes) != gl.letzte.get((zahltyp, gl._praefix(zahltyp)), 0) + 1
                     or (gl.letzte_marke and w[0].x0 > gl.letzte_marke[0] + 12)
                     or (gl.listen_nr and gl.listen_nr[0] == int(erstes) - 1 and abs(gl.listen_nr[1] - w[0].x0) <= 3
                         and gl.listen_nr[2] in (z.seite, z.seite - 1))):
            # «1 Rapport des Polizeiinspektorates …» nach «1.»–«4.» (VII.65.): eine Stückzahl – auch in der Folge,
            # wenn sie eingerückt in der Textspalte steht («1. Caspar Wehrli» / «2 Rechnungen der
            # Zehntloskaufkommission ¦ 1834, 1846», VII.257.) oder die Zählung einer Liste ohne Punkt fortsetzt
            # («2. Numerierte Akten» / «Nr. Gegenstand Datum» / «1 Hans Waldmann …», «2 …», «3 Stadtratsprotokoll …»
            # bis «59», VII.37. – sonst werden 3–8 zu Signaturen und die echten 3.–8. zu deren Teil 2)
            gl.listen_nr = (int(erstes), w[0].x0, z.seite)
            return None
        if gl.modus == "dezimal" and gl.text_x0 and len(komps) == 1 and w[0].x0 >= gl.text_x0 - 4 \
                and not (erstes.endswith(".") and gl.vorschau.startswith(f"{komps[0]}.1.")):
            # Listennummer in der Textspalte («16 Luzern …», VII.494.; «15. Muntwyler …», VII.371.) – ausser
            # es folgt direkt ihre erste Unternummer («2. Neubauten Fabrik …» / «2.1. Bau eines Kammerofens», VII.174.)
            return None
        if rest is not None and rest.text.lstrip()[:1] in ",;":
            return None  # «2.12., 9.12.1959; 29.6., …»: Datumsliste im Text (V.B.c.34.)
        if len(komps) == 1 and rest_ab == 1 and not erstes.endswith(".") and not angeklebt and komps[0].isdigit() \
                and rest is not None and len(rest.worte) == 1 and rest.text.endswith(":"):
            letzte = gl.hauptnr if gl.modus == "dezimal" else gl.letzte.get(("zahl", gl._praefix("zahl")), 0)
            if not (letzte and int(komps[0]) == letzte + 1):
                return None  # «4 Kinder:» – Anzahl mit Doppelpunkt, keine Signatur (VII.394.)
        if len(komps) == 1 and rest_ab == 1 and not erstes.endswith(".") and not angeklebt \
                and MENGE_RE.match(rest.text if rest else "") and komps[0].isdigit():
            letzte = gl.hauptnr if gl.modus == "dezimal" else gl.letzte.get(("zahl", gl._praefix("zahl")), 0)
            # (aber die erste Nummer einer Liste, wenn die nächste Zeile sie fortsetzt: «1 Liste der im Gemeindegut
            # aufgegangenen Fonds» / «1Aa Gemeindegut, …» (V.C.c.61.))
            folge_vorschau = re.match(rf"(?:{komps[0]}[A-Za-z]|{int(komps[0]) + 1}\b)", gl.vorschau) is not None
            if not (letzte and int(komps[0]) == letzte + 1) and not (letzte == 0 and folge_vorschau):
                return None  # «1 Schachtel Grossformat», «2 Listen mit …», «1 Uhr aufgeboten» – Menge, keine Signatur
        if len(komps) == 1:
            bisher = gl.hauptnr if gl.modus == "dezimal" else gl.letzte.get(("zahl", gl._praefix("zahl")), 0)
            folgt_ziffer = bool(rest) and rest.text[:1].isdigit() and komps[0].isdigit() \
                and int(komps[0]) == bisher + 1 and (erstes.endswith(".") or (
                    # «89 2 Filmrollen „Euseri Schwyz“» nach «88» (VII.80.): Anzahl am Anfang des Titels
                    gl.modus == "gliederung" and re.fullmatch(r"\d{1,2}\.?", rest.worte[0].text) is not None
                    and len(rest.worte) > 1 and rest.worte[1].text[:1].isupper()))
            # (auch eine Ordnungszahl im Titel: «38 1. Legat von alt Nationalrat Fierz …» nach «37» (V.C.c.61.))
            # «639 div. O. Strassenbeläge», «229 o. O. Tagesrapporte»: Abkürzung klein, aber Nummer in der Folge
            klein_ok = bool(rest) and gl.modus == "gliederung" and komps[0].isdigit() and rest.text[:1].islower() \
                and re.fullmatch(r"[a-zäöü]{1,3}\.", rest.worte[0].text) \
                and (int(komps[0]) in (bisher, bisher + 1) or gl.freie_nummern and int(komps[0]) > bisher)
            # Bereich als Gruppe, beginnend mit der nächsten Nummer: «12 Administrativer Schlussbericht» / «13 – 34
            # Akten 1925 – 1940» (13,9 pt) / «13 Zur Vorgeschichte …»; «57 – 58 Zeitungsausschnitte (2 Schachteln)»
            # / «58 NZZ 7. Mai 1939 …» (VII.80.): eine Bereichseinheit über den Nummern
            if gl.modus == "gliederung" and folgewort in ("–", "-") and rest is not None and len(rest.worte) >= 3 \
                    and not erstes.endswith(".") and komps[0].isdigit() and re.fullmatch(r"\d{1,4}", rest.worte[1].text) \
                    and int(rest.worte[1].text) > int(komps[0]) \
                    and (rest.worte[2].text[:1].isupper() or rest.worte[2].text[:1] in TITELANFANG) \
                    and int(komps[0]) == bisher + 1 and (bisher > 0 or fett or w[0].size >= 13):
                a, b = komps[0], rest.worte[1].text
                pfad = gl._setze(zahltyp, (f"{a}-{b}",))
                if not gl.nur_pruefen:
                    gl.letzte[(zahltyp, gl._praefix(zahltyp))] = int(a) - 1  # die erste Nummer des Bereichs folgt noch
                return SigTreffer(pfad, f"{a}-{b}", f"{erstes} {folgewort} {b}", rest.ab(2), fett,
                                  hinweis=f"Im Findmittel «{erstes} {folgewort} {b}» – als Bereich {a}-{b} über den "
                                          "einzelnen Nummern übernommen, bitte prüfen.")
            if folgewort in ("–", "-", "bis", "und") or not rest or not (rest.text[:1].isupper() or folgt_ziffer
                                                                          or klein_ok or rest.text[:1] in TITELANFANG):
                return None  # «17. – 19. März», «7 und 8 fehlen.»
            if SCHACHTEL_RE.match(rest.text.strip()) and not angeklebt and gl.modus == "gliederung":
                return None  # «9 Schachtel 19» (VII.179.) ist eine Schachtelangabe
            # (nicht die nächste Nummer in der Signaturspalte, unter der eine Klammerbemerkung folgt: «88 Pläne» /
            # «(Am 17. August 2006 vom Planarchiv des Tiefbauamtes erhalten.)» nach «87 …», VII.80.)
            naechste_nummer = gl.modus == "gliederung" and komps[0].isdigit() and int(komps[0]) == bisher + 1 \
                and bool(gl.letzte_marke) and abs(w[0].x0 - gl.letzte_marke[0]) <= 3 and gl.vorschau[:1] == "("
            if re.match(r"(?:Expl\.?|Ex\.|Exemplare?|Stück|Stk\.?|Blatt|Bl\.)(?:\W|$)", rest.text) \
                    or UMFANG_RE.match(z.text.strip()) and not naechste_nummer:
                return None  # «2 Expl.», «3 Bände» (Anzahl am Zeilenanfang, D9985)
            wert = int(re.match(r"\d*", komps[0]).group() or 0)
            bisher_g = gl.letzte.get((zahltyp, gl._praefix(zahltyp)), 0)
            if gl.modus == "gliederung" and len(komps) == 1 and komps[0].isdigit() and wert < bisher_g \
                    and str(bisher_g + 1).startswith(komps[0]) and gl.vorschau.rstrip(".") == str(bisher_g + 2):
                # Ziffer verloren: «91 Handfertigkeitsunterricht …» / «9 Orgelfonds Enge» / «93 Schindler-Fonds …»
                # (V.C.c.61.) ist 92
                hinweis = f"Im Findmittel «{erstes}» zwischen {bisher_g} und {bisher_g + 2} – als {bisher_g + 1} gelesen, " \
                          "bitte prüfen."
                komps, nummer, wert = (str(bisher_g + 1),), str(bisher_g + 1), bisher_g + 1
            if gl.modus == "dezimal":
                # «20. Modegeschäft …» nach «12.»: neuer Zehnerabschnitt (VII.190.: 20.–23., 30., 40., 50.)
                # (nicht, wenn die Zahl eine nummerierte Liste derselben Spalte unter einer fetten Hauptnummer
                # fortsetzt: «9. Berichte …» / «10. Weisungen für Sprengkolonnen …» unter «1. 1. Fortifikation», VII.76.)
                listen_folge = not fett and gl.haupt_fett and any(
                    abs(x - w[0].x0) <= 3 and lw == wert - 1 and ls in (z.seite, z.seite - 1) and lu == gl.letzter_pfad
                    for x, (lw, ls, lu) in gl.listen_spalten.items())
                zehner = erstes.endswith(".") and wert > gl.hauptnr and wert % 10 == 0 and not listen_folge
                eigen = gl.kind_von[1:] if gl.buchstaben and gl.kind_von[:1] == (gl.abschnitt,) else gl.kind_von
                # (nur mit Punkt, in der Spalte und Schrift der Unternummer davor – nicht «6. Heidelberger
                # Stückemarkt» eingerückt unter fettem «6.4. Plakate», VII.209.)
                if not fett and wert == gl.hauptnr and len(komps) == 1 and len(eigen) == 2 \
                        and eigen[0] == komps[0] and eigen[1].isdigit() and rest is not None \
                        and rest.text[:1].isupper() and erstes.endswith(".") and gl.letzte_marke \
                        and abs(w[0].x0 - gl.letzte_marke[0]) <= 2 and not gl.letzte_marke[1] \
                        and _titelanfang(rest.text) != _titelanfang(gl.haupt_titel) \
                        and not (gl.listen_nr and gl.listen_nr[0] == wert - 1 and abs(gl.listen_nr[1] - w[0].x0) <= 3
                                 and gl.listen_nr[2] in (z.seite, z.seite - 1)):
                    # (nicht der nächste Punkt einer nummerierten Liste «1. …», «2. …», «3. Freisinnige Partei …»
                    # unter «3.1.», VII.76.)
                    # (nicht die Wiederholung der Hauptnummer in einer Schachtelliste am Schluss: «Schachtel 2:» /
                    # «7. Kassenbuch und Journal 1862 - 1994», VII.313.)
                    # «26. Tätigkeitsberichte» direkt nach «26.1. Akten» (V.B.c.54.): die Hauptnummer gibt es schon –
                    # Tippfehler für die nächste Unternummer 26.2. (eigene Einheit mit Hinweis)
                    neu_k = (komps[0], str(int(eigen[1]) + 1))
                    hinweis = (f"Im Findmittel «{erstes}» nach {pfad_text(eigen)} – als «{pfad_text(neu_k)}» gelesen "
                               "(Tippfehler?), bitte prüfen.")
                    komps, nummer = neu_k, ".".join(neu_k)
                elif listen_folge and wert == gl.hauptnr + 1:
                    # nummerierte Liste unter einer fetten Hauptnummer: «1. 1. Fortifikation von Zürich» (fett) /
                    # «1. Bericht …», «2. Tagebuch …» … «28. Schachtel …», unter «3.1. Militärisches» «1.» … «25.»
                    # (VII.76.) – «2.» bzw. «4.» setzt die Liste fort und ist nicht die nächste Hauptnummer (eine
                    # eingerückte Unterliste «1. Evakuationsvorschläge» … «4.» dazwischen zählt für sich)
                    gl.listen_nr = (wert, w[0].x0, z.seite)
                    gl.listen_spalten[round(w[0].x0)] = (wert, z.seite, gl.letzter_pfad)
                    return None
                elif not fett and wert == gl.hauptnr + 2 and len(komps) == 1 and erstes.endswith(".") and z.datum \
                        and rest is not None and rest.text[:1] in "„\"" + "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ" \
                        and gl.letzte_marke and abs(w[0].x0 - gl.letzte_marke[0]) <= 2 and not gl.letzte_marke[1] \
                        and len(gl.letzter_pfad) <= 2 and gl.letzter_pfad[:1] == (str(gl.hauptnr),) \
                        and not any(abs(x - w[0].x0) <= 3 and lw in (wert - 1, wert - 2) and ls in (z.seite, z.seite - 1)
                                    for x, (lw, ls, _lu) in gl.listen_spalten.items()):
                    # (nicht die Fortsetzung einer Liste «8. Abschriften …», «9. Betrachtungen …», «10. Dornacher
                    # Schlachtfeier ¦ 1936» unter einer Unternummer, VII.76.)
                    # eine Nummer übersprungen: «30. „Öffentliche Rechenschaft …“ ¦ 1843» / «32. Verkommniss zwischen dem
                    # Regierungsrate … ¦ 1834 – 1837» (VII.1.; 31. fehlt) – in Spalte, Schrift und mit Datumsspalte wie die
                    # Hauptnummer davor: Signatur, nicht Listenpunkt
                    pass
                elif not fett and wert == gl.hauptnr and len(komps) == 1 and gl.haupt_fett and erstes.endswith(".") \
                        and gl.letzter_pfad == (komps[0],) and rest is not None and rest.text[:1].isupper() \
                        and gl.letzte_marke and abs(w[0].x0 - gl.letzte_marke[0]) <= 2 and gl.letzte_marke[1] \
                        and gl.inhalt_zeilen <= 1 and _titelanfang(rest.text) != _titelanfang(gl.haupt_titel) \
                        and _titelanfang(rest.text).split()[:1] != _titelanfang(gl.haupt_titel).split()[:1] \
                        and not z.schachtel and not z.datum and not re.search(r"\bSchachtel\s+\d", rest.text):
                    # (nicht dieselbe Überschrift mit Jahren und Schachtel: «4. Korrespondenz 1958–1990 ¦ 1 Schachtel»
                    # fett / «4. Korrespondenz 1958–1981, 1971–1990 ¦ Schachtel 12», VII.285.; «1. Jahresberichte» /
                    # «1. Jahresberichte 1936 – 1941 ¦ Schachtel 1» …, V.F.c.204.)
                    # fette Hauptnummer, direkt darunter dieselbe Nummer normal mit eigenem Titel: «10. Quartierverein
                    # Hottingen Varia-Ordner ¦ 1 Schachtel» (fett) / «10. Varia - Sachen» (VII.212.) – das einzige Stück
                    # der Gruppe, als Teil 2 von 10. (wie die wiederholte «3.1.» derselben Datei)
                    pass
                elif not fett and wert != gl.hauptnr + 1 and not zehner \
                        and not (gl.hauptnr == 0 and (re.match(rf"{wert}\.[01]\.", gl.vorschau)
                                                      or re.match(rf"{wert}\.[01]\.", gl.naechste_dezimal or ""))):
                    # (nicht «0. Grundlagen ¦ 1990» vor «0.0. Adresslisten», V.A.c.120.: die Zählung beginnt bei 0; ebenso
                    # «4. Bilder, Zeichnungen …» / «4.1. Wappen» als erste Nummer eines Teilverzeichnisses, VII.327.)
                    gl.listen_nr = (wert, w[0].x0, z.seite)  # Listenpunkt, keine Signatur
                    gl.listen_spalten[round(w[0].x0)] = (wert, z.seite, gl.letzter_pfad)
                    return None
                if not gl.nur_pruefen:
                    gl.hauptnr = wert
                    if len(komps) == 1:
                        gl.haupt_titel = rest.text if rest else ""
                        gl.haupt_fett = fett
            elif len(komps) == 1 and gl.zahl_groesse and w[0].size < gl.zahl_groesse - 1.5 and not fett and (
                    wert <= gl.letzte.get((zahltyp, gl._praefix(zahltyp)), 0)
                    or any(abs(x - w[0].x0) <= 3 and lw in (wert - 1, wert - 2) and ls in (z.seite, z.seite - 1)
                           and lu == gl.letzter_pfad for x, (lw, ls, lu) in gl.listen_spalten.items())):
                # (eine Lücke darf sein: «41. von Steiner» beginnt klein und zählt nicht, VII.254.)
                # nummerierte Liste in kleinerer Schrift nach den Nummern der Gliederung: «4. Jahrgängerverein 1818»
                # (14 pt) / «Detailinventar der enthaltenen Porträtphotographien» / «1. L. R. Lavater» … «46.» (12 pt,
                # VII.254.) – Inhalt der laufenden Einheit, nicht Teile von 1.–4. und neue Einheiten 5.–46.
                gl.listen_spalten[round(w[0].x0)] = (wert, z.seite, gl.letzter_pfad)
                return None
            elif not _folgt(gl, zahltyp, wert, fett):
                return None
            elif len(komps) == 1 and not gl.nur_pruefen:
                gl.zahl_groesse = max(gl.zahl_groesse, w[0].size)
        anzeige = nummer + ("." if not nummer.endswith(".") else "")
        unter_voll = gl.modus != "dezimal" and len(komps) >= 2 and bool(gl.kind_von) \
            and komps[:-1] == gl.kind_von[:len(komps) - 1]
        pfad = komps if gl.modus == "dezimal" or unter_voll else gl._setze(zahltyp, komps)
        if unter_voll:
            anzeige = pfad_text(komps)
        if gl.modus == "dezimal" and gl.buchstaben and gl.abschnitt:
            if len(komps) == 2 and komps[1] == "0":
                komps = komps[:1]  # «1.0 Theaterkritiken» ist die Ebene über «1.1»
            pfad, anzeige = (gl.abschnitt,) + komps, f"{gl.abschnitt}.{anzeige}"
        if gl.modus == "dezimal" and not gl.nur_pruefen and len(komps) > 1 and komps[0].isdigit():
            gl.hauptnr = max(gl.hauptnr, int(komps[0]))
        if band:
            hinweis = (f"Im Findmittel «{' '.join(x.text for x in w[:5])}» (Nummer mit Bänden) – als «{nummer}:{band}» "
                       "übernommen, bitte prüfen.")
            return SigTreffer(pfad, f"{nummer}:{band}", " ".join(x.text for x in w[:5]), rest, fett, "zahl",
                              hinweis=hinweis)
        return SigTreffer(pfad, anzeige if gl.modus == "dezimal" else pfad_text(pfad),
                          roh_doppelt or erstes + ("." if rest_ab == 2 else ""), rest, fett,
                          "voll" if unter_voll else "zahl", hinweis=hinweis)  # (Unternummer einer Vollsignatur zählt wie diese, VII.47.)

    if gl.modus != "gliederung":
        return None
    rest = z.ab(1)
    if not rest:
        return None
    # 2c) Unterstufe «A.1 AV Orion 1964-1972» unter «A Akten chronologisch» (VII.310.): Buchstabe der laufenden Gruppe,
    #     Punkt, Nummer – eine Einheit unter dem Buchstaben
    m_an = re.fullmatch(r"([A-Z])\.(\d{1,3})\.?", erstes)
    if m_an and gl.letzter_pfad and gl.letzter_pfad[0] == m_an.group(1) and len(w) > 1 \
            and (w[1].text[:1].isupper() or w[1].text[:1] in TITELANFANG) and not rest.text[:1].isdigit():
        return SigTreffer((m_an.group(1), m_an.group(2)), erstes.rstrip("."), erstes, rest, fett, "gross")
    # 3) Buchstabe + Nummer: «B 3 Protokoll …», «B 1 fehlt»
    if re.fullmatch(r"[A-Z]{1,2}", erstes) and NUMMER_RE.match(zweites):
        rest2 = z.ab(2)
        if rest2 and rest2.worte[0].text in ("bis", "–", "-", "und", "u.", "/", ","):
            # «B 1 bis B 23» ist eine Fortsetzung («… Nrn. A 201 bis A 360,» / «B 1 bis B 23», VII.161.); «B 998 /
            # 1942, B 1134 / 1943» sind Stadtratsbeschlüsse mit Jahr (V.C.b.368.a.)
            return None
        pfad = gl._setze("gross", (erstes, zweites))
        return SigTreffer(pfad, f"{erstes} {zweites}", f"{erstes} {zweites}", rest2, fett, "gross")
    # 3b) dritte Stufe «D 1:1 Protokolle, Korrespondenz …» unter «D 1 Protokolle» (VII.267.)
    # (auch ohne Leerzeichen bzw. mit Punkt: «I.1:3 Untugendspiegel» nach «I 1:2», «P2:10 Musikdose-Laufwerk …» nach
    # «P 2:9», VII.267.)
    m_bnn1 = re.fullmatch(r"([A-Z]{1,2})\.?(\d{1,4}):(\d{1,4})", erstes)
    if m_bnn1 and len(w) > 1 and len(gl.letzter_pfad) == 3 and gl.letzter_pfad[0] == m_bnn1.group(1) \
            and (w[1].text[:1].isupper() or w[1].text[:1] in TITELANFANG or w[1].text[:1].isdigit()):
        b_, n_, m_ = m_bnn1.groups()
        pfad = gl._setze("gross", (b_, n_, m_))
        return SigTreffer(pfad, f"{b_} {n_}:{m_}", erstes, z.ab(1), fett, "gross",
                          hinweis=f"Im Findmittel «{erstes}» – als «{b_} {n_}:{m_}» gelesen, bitte prüfen.")
    m_bnn = re.fullmatch(r"(\d{1,4}):(\d{1,4})", zweites) if re.fullmatch(r"[A-Z]{1,2}", erstes) else None
    if m_bnn and len(w) > 2 and w[2].text not in ("bis", "–", "-", "und", "u.", "/", ","):
        # (wie «B 1 fehlt» auch «E 1:1 fehlt», «K 1:1 75 Jahre …», «F 1:27 4. Auflage»)
        pfad = gl._setze("gross", (erstes, m_bnn.group(1), m_bnn.group(2)))
        return SigTreffer(pfad, f"{erstes} {zweites}", f"{erstes} {zweites}", z.ab(2), fett, "gross")
    if not (rest.text[:1].isupper() or rest.text[:1] in TITELANFANG
            or gl.doppelmarken and re.fullmatch(r"[A-Z]\)", erstes) and rest.text[:1].isdigit()):
        return None  # (mit Doppelmarken auch «B) 1 grosses Fotoalbum …», VII.191.)
    # 4) römische Zahl «II.» – ausser sie ist der nächste Buchstabe einer Reihe «H.», «I.»
    mr = ROEMISCH_RE.match(erstes)
    if mr and gl.roem_einzeln and not fett:
        mr = None
    mg = GROSS_RE.match(erstes)
    letzter_buchstabe = gl.letzte.get(("gross", gl._praefix("gross")), 0)
    buchstabe_erwartet = bool(mg) and letzter_buchstabe > 0 and 0 < ord(mg.group(1)) - 64 - letzter_buchstabe <= 2
    g_gross, g_roem = gl.marken_groesse.get("gross"), gl.marken_groesse.get("roem")
    if buchstabe_erwartet and mr and g_gross and g_roem and abs(g_gross - g_roem) >= 1.5 \
            and abs(w[0].size - g_roem) < abs(w[0].size - g_gross):
        buchstabe_erwartet = False  # «H. Hochbauamt» (14 pt) / «I. Personelles …» (12 pt): römisch I. (V.G.c.50.)
    # «B. Detailverzeichnis», nicht «D. Verzeichnis der Partizipanten» – und nicht «A. Übersicht» mit eigenen
    # Untersignaturen «A.a.», «A.b.» (VII.308.A.)
    ueberschrift = ist_verzeichniswort(rest.text) and erstes[:1] not in gl.gruppen_buchstaben
    if erstes.endswith(")") and not fett:
        # «A) Constaffel» ist ein Listenzeichen – ausser das Findmittel gliedert mit Doppelmarken «III) B) URBARE»:
        # dann ist «A) Handschriften» die erste Gruppe unter «III) BUCHHALTUNG» (VII.191.) – oder «A)» steht in der
        # Spalte der fetten römischen Stufen («II) Zürcher Eisenbahnverkehrsfragen» / «A) Akten, Protokolle», V.G.c.107.)
        mr = None
        if not gl.doppelmarken and not (gl.klammer_x is not None and abs(w[0].x0 - gl.klammer_x) <= 2):
            mg = None
    if mr and not buchstabe_erwartet and not ueberschrift:
        if _folgt(gl, "roem", roemisch_wert(erstes[:-1]), fett):
            pfad = gl._setze("roem", (erstes[:-1],))
            innen = GROSS_RE.match(rest.worte[0].text)
            if innen and fett and len(rest.worte) > 1 and rest.worte[0].text[-1:] in ".)" \
                    and _folgt(gl, "gross", ord(innen.group(1)) - 64, fett):
                # Doppelmarke «II) B) MITGLIEDERVERZEICHNISSE» (VII.191.): Einheit II.B. unter II.
                pfad2 = gl._setze("gross", (innen.group(1),))
                return SigTreffer(pfad2, pfad_text(pfad2), f"{erstes} {rest.worte[0].text}", rest.ab(1), fett,
                                  "gross", eltern=(pfad, erstes))
            return SigTreffer(pfad, pfad_text(pfad), erstes, rest, fett, "roem")
        return None
    # 5) Grossbuchstabe «A.» / «A Semesternachrichten»
    if mg and not ueberschrift and letzter_buchstabe == 0 and ord(mg.group(1)) - 64 >= 4 and erstes.endswith(".") \
            and re.fullmatch(r"[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)?,", rest.worte[0].text):
        return None  # Initiale eines Autors: «Nummer 12» / «S. Vögelin, Zürich’s ehemalige Stadtthore, …» (VII.340.)
    if mg and not ueberschrift:
        if _folgt(gl, "gross", ord(mg.group(1)) - 64, fett):
            pfad = gl._setze("gross", (mg.group(1),))
            anzeige = erstes if len(pfad) == 1 else pfad_text(pfad)  # «A» wie im PDF (neben «B 3»)
            return SigTreffer(pfad, anzeige, erstes, rest, fett, "gross")
        return None
    # 5b) Kleinbuchstabe mit Punkt in der Schrift der Hauptabteilungen: «E. Kanzlei» / «f. Heizamt» / «F. Hochbau-
    #     inspektorat» (alle 14 pt; Einleitung: «Ausnahme: Hauptabteilung f. Heizamt», V.G.c.50.)
    mf = re.fullmatch(r"([a-z])\.", erstes)
    g_klein = gl.marken_groesse.get("klein")
    if mf and g_gross and abs(w[0].size - g_gross) < 0.6 and (g_roem is None or abs(w[0].size - g_roem) >= 1.5) \
            and (g_klein is None or abs(w[0].size - g_klein) >= 1.5) and not ueberschrift:
        if _folgt(gl, "gross", ord(mf.group(1)) - 96, fett):
            pfad = gl._setze("gross", (mf.group(1),))
            return SigTreffer(pfad, erstes if len(pfad) == 1 else pfad_text(pfad), erstes, rest, fett, "gross")
        return None
    # 6a) kursiver Kleinbuchstabe mit Punkt unter einer römischen Stufe: «III. Neu- und Umbauten (mit Plänen)» /
    #     «a. Gebäude der Allgemeinen Verwaltung ¦ Schachtel 8» (12 pt kursiv, V.G.c.50.)
    m_it = re.fullmatch(r"([a-z])\.", erstes)
    if m_it and "Italic" in w[0].font and not fett and not ueberschrift and w[0].x0 <= SIGNATUR_SPALTE_MAX:
        if _folgt(gl, "klein", ord(m_it.group(1)) - 96, False):
            pfad = gl._setze("klein", (m_it.group(1),))
            return SigTreffer(pfad, pfad_text(pfad), erstes, rest, fett, "klein")
        return None
    # 6) Kleinbuchstabe «a)» – auch «a» ohne Klammer direkt vor «b)» («a Rollenbuch [Hörspiel Radio]», VII.170.)
    mk = KLEIN_RE.match(erstes)
    ohne_klammer = not mk and re.fullmatch(r"[a-y]", erstes) is not None and gl.vorschau == chr(ord(erstes) + 1) + ")"
    if ohne_klammer:
        mk = re.match(r"([a-z])", erstes)
    if mk and _folgt(gl, "klein", ord(mk.group(1)) - 96, fett):
        pfad = gl._setze("klein", (mk.group(1),))
        t = SigTreffer(pfad, pfad_text(pfad), erstes, rest, fett, "klein")
        if ohne_klammer:
            t.hinweis = f"Im Findmittel «{erstes}» ohne Klammer – als «{erstes})» gelesen, bitte prüfen."
        return t
    return None


def ist_verzeichniswort(text: str) -> bool:
    """«Detailverzeichnis», «INVENTARÜBERSICHT», «Übersicht», «Register» – eine Überschrift des Findmittels."""
    return text.strip(":.,").upper() in VERZEICHNISWORT  # nicht «Inventare», «Mitgliederverzeichnisse»


def abschnittsmarke(text: str) -> str:
    """Kennung eines Abschnitts mit eigener Zählung: «A.» -> «A», «01» -> «01» («01 URKUNDEN», VII.174.)."""
    return text[0] if re.fullmatch(r"[A-Z]\.", text) else text if re.fullmatch(r"\d{2}", text) else ""


def _ist_buchstabenabschnitt(z: Zeile) -> bool:
    w = z.worte
    if len(w) < 2 or w[0].x0 > SIGNATUR_SPALTE_MAX or not abschnittsmarke(w[0].text) \
            or ist_verzeichniswort(" ".join(x.text for x in w[1:])):
        return False
    rest = z.ab(1)
    kern = re.sub(r"\s+(?:Schachteln?|Mappen?)\b.*$", "", rest.text) if rest else ""  # «01 URKUNDEN Schachtel»
    gross = kern.isupper() and len(kern) > 3
    if w[0].text.isdigit():
        return gross  # «02 NEUBAUTEN», nicht «12 Briefe an …»
    return bool(rest) and (all("Bold" in x.font for x in w) or gross)


def lerne_unterzaehlung(zeilen: list[Zeile]) -> float | None:
    """x-Grenze, ab der blosse Nummern eine Unterzählung sind (VII.380.: «1.» bei x 71, eingerückt «1.», «2.» …
    bei x 110). Nur wenn die eingerückte Zählung mindestens zweimal neu bei 1 beginnt."""
    marken = []
    for z in zeilen:
        w = z.worte
        if len(w) >= 2 and w[0].x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG and re.fullmatch(r"\d{1,3}\.?", w[0].text) \
                and (w[1].text[:1].isupper() or w[1].text[:1].isdigit() or w[1].text[:1] in TITELANFANG):
            marken.append((int(w[0].x0) // 5 * 5, int(w[0].text.rstrip("."))))
    spalten = sorted(x for x, n in Counter(x for x, _ in marken).items() if n >= 3)
    if len(spalten) < 2 or spalten[1] - spalten[0] < 12:
        return None
    gegliedert = sum(1 for z in zeilen if z.worte and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG
                     and (ROEMISCH_RE.match(z.worte[0].text) or KLEIN_RE.match(z.worte[0].text)
                          or re.fullmatch(r"[A-Z]\.", z.worte[0].text))) >= 3
    if gegliedert:
        return None  # mit I./A./a)-Gliederung gibt es schon Ebenen (VII.179.) – nur flache Nummernlisten
    innen = [v for x, v in marken if x == spalten[1]]
    return (spalten[0] + spalten[1]) / 2 + 2.5 if innen.count(1) >= 2 else None


def lerne_buchstabenabschnitte(zeilen: list[Zeile]) -> bool:
    """Dezimales Findmittel, dessen Zählung in jedem Buchstabenabschnitt neu beginnt («A. …» 1., 2. / «B. …» 1.0,
    2.0): dann gehört der Buchstabe in die Signatur («B.1.0»)."""
    def nummer(z: Zeile) -> bool:
        return z.worte[0].x0 <= SIGNATUR_SPALTE_MAX and re.fullmatch(r"\d{1,3}(?:\.\d{1,3})*\.?", z.worte[0].text) \
            and not _ist_buchstabenabschnitt(z)

    nummern_x = [z.worte[0].x0 for z in zeilen if nummer(z)]
    links = min(nummern_x) if nummern_x else 0
    erste_nummer = next((k for k, z in enumerate(zeilen) if nummer(z)), len(zeilen))
    erster_buchstabe = next((k for k, z in enumerate(zeilen) if _ist_buchstabenabschnitt(z)), len(zeilen))
    if erster_buchstabe > erste_nummer:
        return False  # die Buchstaben stehen erst im Inhalt einer Einheit
    abschnitt, gesehen = "", {}
    for z in zeilen:
        if _ist_buchstabenabschnitt(z) and z.worte[0].x0 <= links + 4:
            abschnitt = abschnittsmarke(z.worte[0].text)
        elif abschnitt and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX and re.fullmatch(r"\d{1,3}(?:\.\d{1,3})*\.?", z.worte[0].text):
            gesehen.setdefault(z.worte[0].text.rstrip("."), set()).add(abschnitt)
    return sum(1 for v in gesehen.values() if len(v) > 1) >= 2


def lerne_nummern(zeilen: list[Zeile]) -> tuple[bool, bool]:
    """Nummerierungsart des Findmittels: (laufende Nummern mit Lücken, Signaturen «Jahr.Laufnummer»)."""
    links = [z for z in zeilen if z.worte[0].x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG and len(z.worte) > 1
             and z.worte[1].text[:1].isupper()]
    nummern = [int(m.group(1)) for z in links if (m := re.fullmatch(r"(\d{1,3})\.?", z.worte[0].text))]
    # nur flache Listen: mit Gliederung durch I./A./a) sind Zahlen am Zeilenanfang oft Anzahlen («51 Zunft-Rechnungen»)
    gegliedert = sum(1 for z in links if ROEMISCH_RE.match(z.worte[0].text) or KLEIN_RE.match(z.worte[0].text)
                     or re.fullmatch(r"[A-Z]\.", z.worte[0].text)) >= 3
    steigend = (len(nummern) >= 8 and not gegliedert
                and sum(b >= a for a, b in zip(nummern, nummern[1:])) >= 0.8 * (len(nummern) - 1))
    jahr = sum(1 for z in links if re.fullmatch(rf"{JAHR}\.\d{{1,4}}\.?", z.worte[0].text)) >= 5
    return steigend, jahr


def lerne_textspalte(zeilen: list[Zeile]) -> float | None:
    """Dezimal: x-Position, an der die Titel hinter den Signaturen «1.», «2.1.» beginnen. Eine blosse Zahl ohne
    Punkt, die erst dort steht, ist eine Listennummer im Text («16 Luzern und seine Umgebung», Bandliste VII.494.)."""
    kandidaten = [z for z in zeilen if len(z.worte) > 1 and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX
                  and re.fullmatch(r"\d{1,3}(?:\.\d{1,4})*\.", z.worte[0].text) and z.worte[1].text[:1].isupper()]
    if not kandidaten:
        return None
    # nur die Signaturspalte (die linkeste mit mindestens 3 Nummern), nicht Listennummern im Text
    spalten = Counter(round(z.worte[0].x0) for z in kandidaten)
    links = min((x for x, n in spalten.items() if n >= 3), default=min(spalten))
    starts = Counter(round(z.worte[1].x0) for z in kandidaten if z.worte[0].x0 <= links + 3)
    if not starts:
        return None
    x, n = starts.most_common(1)[0]
    n += starts.get(x - 1, 0) + starts.get(x + 1, 0)
    return float(x) if n >= 3 and n >= 0.5 * sum(starts.values()) else None


def lerne_punktnummern(zeilen: list[Zeile]) -> bool:
    """Tragen die Signaturen einen Punkt und bilden eine Folge («1. Protokoll», «2. Kassenbuch», … «4.», VII.65.)?
    Dann ist eine blosse Zahl ohne Punkt, die die Folge nicht fortsetzt, eine Menge («1 Rapport des
    Polizeiinspektorates …» unter «Beilagen:»; «6 Reproduktionen in Lichtdruck» vor «1.», V.L.221.)."""
    kand = [(int(z.worte[0].text[:-1]), z.worte[0].x0) for z in zeilen
            if len(z.worte) > 1 and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG
            and re.fullmatch(r"\d{1,3}\.", z.worte[0].text)]
    # nur die Signaturspalte (die linkeste mit mindestens 3 Nummern) – nicht Tagesangaben umbrochener Zeilen
    # («… Gustav Stähli,» / «24. Juli 1935 und Zürichsee-Zeitung …», eingerückt, VII.37.), die die Folge 1., 2., 3. …
    # sonst unterbrechen
    spalten = Counter(round(x) for _, x in kand)
    links = min((x for x in spalten if sum(n for xx, n in spalten.items() if abs(xx - x) <= 3) >= 3), default=None)
    nummern = [n for n, x in kand if links is None or abs(x - links) <= 3]
    lauf = best = 0
    for a, b in zip(nummern, nummern[1:]):
        lauf = lauf + 1 if b == a + 1 else 0
        best = max(best, lauf)
    return best >= 2


def lerne_mengenzahlen(zeilen: list[Zeile]) -> bool:
    """Sind blosse Zahlen ohne Punkt am Zeilenanfang Mengenangaben statt Signaturen? Ja, wenn sie keine Folge
    bilden: «1 Stammbuch …», «1 Stammbuch do.», «4 gedruckte Broschüren», «1 Heft» (VII.191.) – meist 1, 1, 1 …"""
    nummern = [int(z.worte[0].text) for z in zeilen
               if len(z.worte) > 1 and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG
               and re.fullmatch(r"\d{1,3}", z.worte[0].text) and not SCHACHTEL_RE.match(z.ab(1).text)]
    folge = sum(1 for a, b in zip(nummern, nummern[1:]) if b == a + 1)
    bruch = sum(1 for a, b in zip(nummern, nummern[1:]) if b != a + 1 and not (b == a and a > 1))
    return bruch >= 4 and bruch > 2 * folge


SCHACHTELKOPF_RE = re.compile(r"(?:Schachtel(?:-?Nr\.?|-)?|Schachteln|Sch\.|Schachtelnr\.?|Schachtelnummern?|Box|Karton)")


EXEMPLARKOPF_RE = re.compile(r"(?:Expl\.?|Ex\.|Exemplare?|Anzahl|Stück|Stk\.?)")


def finde_schachtelspalte(zeilen: list[Zeile], alle: list[Zeile]) -> tuple[float, str] | None:
    """Spalte mit blossen Zahlen am rechten Rand («… 1925 ¦ 1»), wenn mindestens 8 Zeilen so enden: als
    Schachtel-Nr., wenn ein Spaltenkopf «Schachtel» darüber steht bzw. das Vorwort sie so erklärt; als Anzahl
    Exemplare (Umfang), wenn darüber «Expl.»/«Anzahl» steht. Sonst bleibt die Zahl im Text."""
    def unter_kopf() -> tuple[float, str] | None:
        # kleine Tabelle mit Spaltenkopf «Nr. Titel Schachtel Jahre» und nur einer Zahl in der Spalte: «1. Korrespondenz
        # privat ¦ 1» (VII.83.)
        for k in alle:
            t = [w.text for w in k.worte]
            # (auch «Akte / Dossier ¦ Schachtel-Nr.» mit nur drei Zeilen, V.J.c.68.)
            i_s = next((n for n, x in enumerate(t) if x == "Schachtel" or re.fullmatch(r"Schachtel-(?:Nr\.?)?", x)), None)
            if i_s is None or sum(x in t for x in ("Nr.", "Titel", "Jahre", "Jahr", "Inhalt", "Signatur", "Datum",
                                                   "Akte", "Dossier")) < 2:
                continue
            kw = k.worte[i_s]
            kanten = [round(w[-1].x1) for z in zeilen if len(w := z.worte) >= 3
                      and re.fullmatch(r"\d{1,3}[a-z]?", w[-1].text) and kw.x0 - 8 <= w[-1].x0 <= kw.x1 + 8
                      and w[-1].x0 - w[-2].x1 >= SPALTEN_LUECKE]
            if kanten:
                return float(Counter(kanten).most_common(1)[0][0]), "schachtel"
        return None

    enden: Counter = Counter()
    for z in zeilen:
        w = z.worte
        if len(w) >= 3 and re.fullmatch(r"\d{1,3}[a-z]?", w[-1].text) and w[-1].x0 >= 440 \
                and w[-1].x0 - w[-2].x1 >= SPALTEN_LUECKE:
            enden[round(w[-1].x1)] += 1
    if not enden:
        return unter_kopf()

    def anzahl(x: int) -> int:
        return sum(c for xx, c in enden.items() if abs(xx - x) <= 3)

    x, n = max(((x, anzahl(x)) for x in enden), key=lambda t: t[1])
    if n < 8:
        return unter_kopf()
    vorwort = any(re.search(r"\b\w+te\s+Spalte\s+(?:bezeichnet|nennt|gibt|enthält)\s+(?:die\s+)?(?:Nummer\s+der\s+)?"
                            r"Schachtel", z.text) for z in alle)

    def art(x: int) -> str | None:
        ueber = [w for z in alle for w in z.worte if w.x1 >= x - 60 and w.x0 <= x + 10]
        if any(EXEMPLARKOPF_RE.fullmatch(w.text) for w in ueber):
            return "exemplare"
        kopf = any(SCHACHTELKOPF_RE.fullmatch(w.text) for w in ueber)
        return "schachtel" if kopf or vorwort else None

    a = art(x)
    if a is None:
        return None
    # weitere Kanten derselben Art mit ebenso vielen Zeilen (Zusammenfassung bei x 546, Detail bei x 560, VII.191.)
    weitere: list[float] = []
    for xx in sorted(enden, key=lambda k: (-anzahl(k), k)):
        if anzahl(xx) >= 8 and abs(xx - x) > 3 and all(abs(xx - k) > 3 for k in weitere) and art(xx) == a:
            weitere.append(float(xx))
    return (float(x), a, *weitere)


def bestimme_modus(zeilen: list[Zeile]) -> str:
    """«dezimal», wenn das Findmittel mehrstufige Zahlen wie 2.1. verwendet, sonst «gliederung»."""
    n = sum(1 for z in zeilen if z.worte[0].x0 <= SIGNATUR_SPALTE_MAX
            and re.fullmatch(r"\d{1,3}(?:\.\d{1,3})+\.?", z.worte[0].text))
    return "dezimal" if n >= 5 else "gliederung"


def ist_aufzaehlung(z: Zeile) -> bool:
    t = z.worte[0].text
    return t in AUFZAEHLUNG and (t != "o" or len(z.worte) > 1)


def ist_aufzaehlung_mit_marke(z: Zeile) -> bool:
    """«a) …», «1) …» – eigener Eintrag, die Marke bleibt stehen."""
    return re.fullmatch(r"[a-z]\)|\d{1,2}\)", z.worte[0].text) is not None and len(z.worte) > 1


def abstand(a: Zeile, b: Zeile) -> float | None:
    """Leerraum zwischen zwei Zeilen; None bei Seitenwechsel."""
    if a.seite != b.seite:
        return None
    return b.top - a.bottom


def luft(a: Zeile | None, b: Zeile | None) -> float:
    """Wie abstand(), aber Seitenwechsel und Textanfang/-ende zählen als grosser Abstand."""
    if a is None or b is None or a.seite != b.seite:
        return float("inf")
    return b.top - a.bottom


# ----------------------------------------------------------------------------- Rohe Vorkommen


@dataclass
class Vorkommen:
    pfad: tuple[str, ...]
    anzeige: str
    roh: str
    seite: int
    zeilen: list[Zeile]
    fett: bool = False
    typ: str = "zahl"
    teil_nr: int | None = None  # aus «Teil n»-Zeilen ohne Signatur
    schachtel: str | None = None
    datum: str = ""  # aus der Datumsspalte
    umfang: list[str] = field(default_factory=list)
    hinweise: list[str] = field(default_factory=list)
    einheit: Einheit | None = None  # die daraus gebaute Einheit (für die Vollständigkeitsprüfung)
    aus_marke: bool = False  # Teil, der mit einer Schachtelangabe begann
    ist_teil: bool = False  # wiederholte Signatur, «Teil n» oder Teil aus einer Schachtelangabe
    kopf_ids: set[int] = field(default_factory=set)  # Zeilen des Titelblocks (für die Vollständigkeitsprüfung)
    titel_vorgabe: str = ""  # «Mappe 3» bzw. Bestandstitel: dann sind alle Zeilen Darin
    weitere_daten: list[str] = field(default_factory=list)  # 2./3. Zeile der Datumsspalte («1961–1985»)
    vorgabe_ids: set[int] = field(default_factory=set)  # Zeilen, aus denen titel_vorgabe gebildet ist
    x0: float = 0.0  # linke Kante der Signaturzeile (Einrückung der Gliederungsstufe)
    bestand: str = ""  # nur bei Findmitteln für mehrere Bestände: Bestand dieser Einheit (finde_bestandswechsel)
    titel_neben: bool = False  # Signatur vertikal mittig neben dem Titel; erste Titelzeile steht vor ihr im PDF
    schachtel_geerbt: bool = False  # Schachtel von einer früheren Angabe übernommen, nicht bei der Einheit selbst
    titel_bis: int = 0  # Zeilen vor einer Schachtelangabe («Schachtel 101» unter dem Titel): nur sie bilden den Titel
    signatur_fest: str = ""  # berichtigte Vollsignatur (korrigiere_doppelnummern); roh bleibt die Form im PDF


@dataclass
class Verbleib:
    """Wohin eine Zeile des Detailverzeichnisses gegangen ist – Grundlage der Vollständigkeitsprüfung."""
    zeile: Zeile
    art: str  # einheit | ohne_erstes_wort | schachtel | schluss | ueberschrift | vorlauf
    vorkommen: Vorkommen | None = None
    pfad: tuple | None = None
    wert: str = ""


def hat_inhalt(v: Vorkommen) -> bool:
    """Hat die Einheit schon Text unter ihrem Titel (neuer Absatz, Aufzählung oder eigene Tabellenzeile
    mit Datum/Umfang)? Ein mit einer Schachtelangabe begonnener Teil hat keinen Titel, nur Inhalt."""
    zs = v.zeilen
    if v.aus_marke:
        return bool(zs)
    return any(ist_aufzaehlung(b) or luft(a, b) > ABSATZ_ABSTAND or b.datum or b.umfang for a, b in zip(zs, zs[1:]))


def baue_vorkommen(zeilen: list[Zeile], gl: Gliederung, info: dict) -> list[Vorkommen]:
    vorkommen: list[Vorkommen] = []
    aktuell: Vorkommen | None = None
    gesehen: set[tuple] = set()
    im_schluss = False
    gesperrt: Vorkommen | None = None  # Einheit, deren Inhalt «Signatur: …» für alles Folgende nennt
    im_anhang = False  # nach «Anmerkungen zum Bestand …» auf den letzten Seiten: alles ins Info-Blatt
    letzte_seite = zeilen[-1].seite if zeilen else 0
    # Nummern in der Signaturspalte mit Schriftgrösse: kommt dieselbe Nummer später deutlich grösser («2. Manuskripte»
    # 13,9 pt), ist die kleinere davor Inhalt («1.2. Verschiedenes» / «2. Stammbuch der Libertas Turicensis» 12 pt,
    # VII.374.)
    dezimal_zeilen = [k for k, x in enumerate(zeilen) if x.worte and x.worte[0].x0 <= SIGNATUR_SPALTE_MAX
                      and re.fullmatch(r"\d{1,3}(?:\.\d{1,3})+\.?", x.worte[0].text)]
    alle_dezimal = {tuple(zeilen[k].worte[0].text.rstrip(".").split(".")) for k in dezimal_zeilen}
    nummer_zeilen: list[tuple[int, int, float]] = []  # (Zeile, Nummer, Schriftgrösse)
    for k_n, x_n in enumerate(zeilen):
        if len(x_n.worte) > 1 and x_n.worte[0].x0 <= SIGNATUR_SPALTE_MAX and re.fullmatch(r"\d{1,3}\.", x_n.worte[0].text) \
                and not _ist_datumsfolge(x_n.ab(1)):
            nummer_zeilen.append((k_n, int(x_n.worte[0].text[:-1]), x_n.worte[0].size))

    def spaeter_mit_punkt(i_z: int, z_: Zeile) -> bool:
        """Blosse Zahl ohne Punkt, nicht fett – und die nächste Nummernzeile ist dieselbe Nummer mit Punkt in fetter
        Schrift: «2 Handwerkskundschaften von Jakob Friedrich Fissler …» im Inhalt von 1. / fett-kursiv «2. Vorträge
        und nicht einer Publikation zuordenbare Artikel» (VII.141.) – eine Anzahl, keine Signatur."""
        if "Bold" in z_.worte[0].font:
            return False
        n_z = int(z_.worte[0].text)
        naechste = next(((k_, n_) for k_, n_, _ in nummer_zeilen if k_ > i_z and n_z <= n_ <= n_z + 3), None)
        return naechste is not None and naechste[1] == n_z and "Bold" in zeilen[naechste[0]].worte[0].font

    def spaeter_groesser(i_z: int, z_: Zeile) -> bool:
        """Ist die nächste Nummernzeile ab dieser Nummer dieselbe Nummer in deutlich grösserer Schrift?"""
        n_z = int(z_.worte[0].text[:-1])
        # (nur nahe Nummern: «75. Geburtstag von Walter Baumann» dazwischen zählt nicht, VII.374.)
        naechste = next(((n_, g_) for k_, n_, g_ in nummer_zeilen if k_ > i_z and n_z <= n_ <= n_z + 3), None)
        return naechste is not None and naechste[0] == n_z and naechste[1] >= z_.worte[0].size + 1.5
    verbleib: list[Verbleib] = info.setdefault("verbleib", [])
    # Schachtelangaben («Schachtel 3», «11.1. Schachtel 2») gelten für das, was folgt: für die nächsten
    # Einheiten im selben Hauptabschnitt. Folgt direkt Text, beginnt damit ein neuer Teil in dieser Schachtel
    # (VII.200.: «11.1. Schachtel 2» + «Cofalka, Ute: …») – ausser die Einheit hat bisher nur ihren Titel.
    box: dict = {"nr": None, "abschnitt": None, "marke": None, "datum": "", "extra": []}
    zuordnung: list[tuple] = []  # («2», von_pfad, bis_pfad|None, Verbleib) aus «Schachtel 2: 4.1.2. – 4.1.5.»
    # Schachtelspalte selten und nie zweimal hintereinander gleich («Schachtel 1» bei :1., «Schachtel 2» bei :12.):
    # sie markiert den Beginn einer Schachtel; steht sie bei jeder Einheit (auch wiederholt), gilt sie nur dort
    spalte = [z.schachtel for z in zeilen if z.schachtel]
    links = sum(1 for z in zeilen if z.worte and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG)
    # (einzelne Wiederholungen in einer langen Folge stören nicht: «Schachtel 60» bei 7.3. und 7.4., VII.174.)
    spalte_fortfuehren = bool(spalte) and len(spalte) <= 0.4 * max(1, links) \
        and sum(a == b for a, b in zip(spalte, spalte[1:])) <= len(spalte) // 20
    # Beginnen die Schachtelnummern in jedem Abschnitt neu (VII.200.: 11.1. Schachtel 1–3, 11.2. Schachtel 1–2),
    # gilt eine Schachtel nur innerhalb der Einheit bzw. Gruppe, in der sie steht; bei fortlaufender Zählung
    # (VII.179.: 1a, 1b, 1, 2, … 13) im ganzen Hauptabschnitt
    nummern = [int(m.group(1)) for z in zeilen
               if (m := re.search(r"(?:^|\s)Schachtel\s+(\d+)[a-z]?\s*$", z.text)) and len(z.worte) <= 3]
    abschnittsweise = any(b < a for a, b in zip(nummern, nummern[1:]))
    # Findmittel ohne Unternummern («Schachtel II» / 2. … 6. / «Schachtel III» / 7., VII.67.): eine Schachtelüberschrift
    # gilt bis zur nächsten, nicht nur für die eine Hauptnummer
    def gliedernd(z: Zeile) -> bool:
        if not z.worte or z.worte[0].x0 > SIGNATUR_SPALTE_MAX_GLIEDERUNG:
            return False
        t = z.worte[0].text
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3})+\.?", t):
            return True
        return z.worte[0].x0 <= SIGNATUR_SPALTE_MAX and len(z.worte) > 1 and z.worte[1].text[:1].isupper() \
            and bool(ROEMISCH_RE.match(t) or GROSS_RE.match(t))
    flach = not any(gliedernd(z) for z in zeilen)

    def merke(z: Zeile, art: str, v: Vorkommen | None = None, pfad: tuple | None = None, wert: str = "") -> Verbleib:
        vb = Verbleib(z, art, v, pfad, wert)
        verbleib.append(vb)
        return vb

    def bereich(v: Vorkommen) -> tuple:
        """Wie weit eine Schachtelangabe reicht, die bei Einheit v beginnt."""
        if flach and len(v.pfad) == 1 and v.pfad[0].isdigit():
            return ()
        if not abschnittsweise:
            return v.pfad[:1]
        return v.pfad if v.ist_teil else v.pfad[:-1]

    def box_fuer(v: Vorkommen) -> str | None:
        if box["nr"] is None:
            return None
        if box["abschnitt"] is None:
            box["abschnitt"] = bereich(v)
        elif v.pfad[:len(box["abschnitt"])] != box["abschnitt"]:  # anderer Abschnitt: nicht weiterziehen
            box["nr"] = box["abschnitt"] = None
            return None
        return box["nr"]

    def basis_fuer(marke: Zeile) -> Vorkommen:
        """Zu welcher Einheit ein Teil aus einer Schachtelangabe gehört: zur laufenden – ausser die Angabe steht
        so weit links wie deren Signatur (VII.181.: «Schachtel 2» auf der Höhe von «a)», «b)»), dann zur
        nächsten weniger eingerückten Einheit darüber."""
        if aktuell.aus_marke or not aktuell.x0 or marke.x0 > aktuell.x0 + 2:
            return aktuell
        return next((v for v in reversed(vorkommen) if not v.ist_teil and v.x0 and v.x0 < marke.x0 - 2
                     and aktuell.pfad[:len(v.pfad)] == v.pfad), aktuell)

    def extra_zuordnen(v: Vorkommen) -> None:
        for vb_ in box["extra"]:
            vb_.vorkommen = v
        box["extra"] = []

    def schachtel_als_teil() -> None:
        """Offene Marke mit Datum ohne Text danach («Schachtel 10 ¦ 1952-1958», «Schachtel 11 ¦ 1958-1961»):
        die Schachtel ist selbst ein Eintrag – ein Teil der laufenden Einheit."""
        nonlocal aktuell
        nummer, _, vb = box["marke"]
        basis = basis_fuer(vb.zeile)
        teil = Vorkommen(basis.pfad, basis.anzeige, basis.roh, vb.zeile.seite, [], typ=basis.typ,
                         schachtel=nummer, aus_marke=True, ist_teil=True, datum=box["datum"], x0=basis.x0)
        vorkommen.append(teil)
        aktuell, vb.vorkommen = teil, teil
        extra_zuordnen(teil)
        box.update(nr=nummer, abschnitt=bereich(teil), marke=None)

    def marke_setzen(z: Zeile, nummer: str, quelle: tuple | None) -> None:
        """quelle: (pfad, anzeige, roh, typ) bei «11.1. Schachtel 2», sonst None."""
        if box["marke"] and box["marke"][1] is None and box["datum"] and aktuell is not None:
            schachtel_als_teil()
        if box["marke"] and box["marke"][1] is not None:
            # zwei Marken hintereinander («10.1. Schachtel 10» / «10.2. Schachtel 8»): eine Zuordnungsliste –
            # die Schachtel gilt für die schon bekannte Einheit mit dieser Signatur
            alt_nummer, alt_quelle, alt_vb = box["marke"]
            bekannt = next((v for v in reversed(vorkommen) if v.pfad == alt_quelle[0]), None)
            if bekannt is not None and not bekannt.schachtel:
                bekannt.schachtel = alt_nummer
                alt_vb.vorkommen = bekannt
        box["marke"] = (nummer, quelle, merke(z, "schachtel", None, quelle[0] if quelle else None, nummer))
        box["datum"] = z.datum  # «Schachtel 17 ¦ 1946 – 1947»

    def vor_neuer_einheit() -> None:
        """Offene Marke mit Datum direkt vor einer neuen Signatur: der letzte Schachtel-Eintrag der laufenden
        Einheit, nicht der Beginn der neuen («Schachtel 19 ¦ 1979-1980» / «III. Mitglieder»)."""
        if box["marke"] and box["marke"][1] is None and box["datum"] and aktuell is not None:
            schachtel_als_teil()
            box.update(nr=None, abschnitt=None)

    def neue_einheit(v: Vorkommen) -> None:
        """Eine offene Schachtelmarke gilt ab dieser Einheit (sie steht vor ihr)."""
        if box["marke"]:
            nummer, _, vb = box["marke"]
            box.update(nr=nummer, abschnitt=None, marke=None)
            vb.vorkommen = v
            extra_zuordnen(v)
            if not v.schachtel:
                v.schachtel = box_fuer(v)

    def inhalt_beginnt(z: Zeile) -> None:
        """Text direkt nach einer Schachtelmarke: neuer Teil – oder die Schachtel der Einheit selbst."""
        nonlocal aktuell
        if not box["marke"]:
            return
        nummer, quelle, vb = box["marke"]
        box.update(nr=nummer, marke=None)
        basis = basis_fuer(vb.zeile) if quelle is None and aktuell is not None else aktuell
        # (nicht, wenn nach der Marke derselbe Titel wiederkommt: «V.J.W. c.12.:1. ¦ Schachtel 1» / «Akten ¦ 1893-1896» /
        # «Schachtel 2» / «Akten ¦ 1897-1900» – ein weiterer Teil, V.J.W.c.12.)
        gleicher_titel = aktuell is not None and bool(aktuell.zeilen) and bool(z.worte) \
            and _titelanfang(z.text) == _titelanfang(aktuell.zeilen[0].text) != ""
        # (Liste, deren Schachtelwechsel sonst in der rechten Spalte der Einträge stehen: «Ave Maria F. Mendelssohn ¦
        # Schachtel 41» … / «Schachtel 42» allein / «Dankeschön und auf Wiedersehen …» unter 7.4., VII.122. – die
        # Schachtel kommt zur Einheit dazu, kein neuer Teil)
        spalte_im_darin = quelle is None and aktuell is not None and not aktuell.aus_marke and basis is aktuell \
            and nummer.isdigit() and any(x.schachtel and x.schachtel.isdigit() for x in aktuell.zeilen[1:]) \
            and all(int(x.schachtel) < int(nummer) for x in aktuell.zeilen[1:] if x.schachtel and x.schachtel.isdigit())
        if spalte_im_darin:  # die Nummer gilt für den Eintrag (wie die Angaben in der rechten Spalte)
            if not z.schachtel:
                z.schachtel = nummer
            box["abschnitt"] = bereich(aktuell)
            vb.vorkommen = aktuell
            return
        if quelle is None and basis is aktuell and aktuell is not None and not aktuell.aus_marke \
                and not hat_inhalt(aktuell) and not gleicher_titel:
            alt = aktuell.schachtel
            if alt and not aktuell.schachtel_geerbt and alt.isdigit() and nummer.isdigit() \
                    and int(nummer) == int(alt) + 1:
                nummer = f"{alt}-{nummer}"  # «8) Polizist Wäckerli ¦ Schachtel 04» / «Schachtel 05» (VII.170.)
            aktuell.schachtel = nummer
            aktuell.schachtel_geerbt = False
            aktuell.titel_bis = len(aktuell.zeilen)  # was nach der Schachtelangabe folgt, ist Inhalt (VII.191.)
        else:
            pfad, anzeige, roh, typ = quelle or (basis.pfad, basis.anzeige, basis.roh, basis.typ)
            aktuell = Vorkommen(pfad, anzeige, roh, z.seite, [], typ=typ, schachtel=nummer, aus_marke=True,
                                ist_teil=True, datum=box["datum"], x0=basis.x0 if quelle is None else 0.0)
            vorkommen.append(aktuell)
        box["abschnitt"] = bereich(aktuell)
        vb.vorkommen = aktuell
        extra_zuordnen(aktuell)

    erste_x0: dict[tuple, float] = {}  # Einrückung der ersten Nennung je Signatur

    def folgt_signatur(x: Zeile | None) -> bool:
        """Wird x als Signaturzeile gelesen (wie in der Hauptschleife, ohne den Zustand zu ändern)?"""
        t = lies_signatur(x, gl.kopie()) if x is not None else None
        if t is None:
            return False
        # eingerückte Aufzählung im Inhalt («Originalhefte:» / «1. Heft: …», VII.194.)
        return not (t.pfad in erste_x0 and len(t.pfad) == 1 and x.x0 > erste_x0[t.pfad] + 25
                    and not (gl.einrueck_x and x.x0 > gl.einrueck_x))
    zwischentitel = ""  # fette Überschrift ohne Signatur vor der nächsten Einheit
    # Stücke ohne Nummer («Keine Nr. …», «VII. 138. Fotografien», «Mappe – Porträt (Grossformat)» nach der letzten
    # Einheit): Darin einer Zeile für den Bestand selbst, nicht einer fremden Einheit und ohne erfundene Signatur
    sammel: list[Vorkommen] = []

    def sammelzeile(z_s: Zeile) -> Vorkommen:
        if not sammel:
            v_s = Vorkommen(("Bestand",), "", "", z_s.seite, [], typ="bestand")
            sammel.append(v_s)
            vorkommen.append(v_s)
        return sammel[0]

    def stueck_ohne_nummer(z_s: Zeile) -> None:
        """Ab z_s gehört der Text zu einem Stück ohne Nummer: Zeile für den Bestand (mit Hinweis)."""
        nonlocal aktuell
        v_s = sammelzeile(z_s)
        v_s.hinweise.append(f"Stück ohne Nummer im Findmittel («{z_s.text.strip()[:70]}», S. {z_s.seite}) – hier beim "
                            "Bestand übernommen (keine Signatur erfunden); in scope beim Bestand ergänzen oder von Hand als "
                            "Einheit anlegen.")
        aktuell = v_s
    # Anteil kursiver Zeilen je Spalte (x0 gerundet): kursive Überschriften gibt es nur, wo Kursiv selten ist (nicht in
    # VII.333., wo alle Inhaltszeilen «Flugblatt», «Programm» … kursiv stehen)
    alle_x: Counter = Counter()
    kursiv_x: Counter = Counter()
    for x_z in zeilen:
        if x_z.worte:
            alle_x[round(x_z.x0)] += 1
            if all(("Italic" in w.font or "Kursiv" in w.font or "Oblique" in w.font) and "Bold" not in w.font
                   for w in x_z.worte):
                kursiv_x[round(x_z.x0)] += 1

    def kursiv_selten(x0: float) -> bool:
        n_a = sum(alle_x[k] for k in range(round(x0) - 2, round(x0) + 3))
        n_k = sum(kursiv_x[k] for k in range(round(x0) - 2, round(x0) + 3))
        return n_a > 0 and n_k <= max(1, 0.1 * n_a)
    zt_zeilen: list[Zeile] = []  # Zeilen der laufenden Zwischenüberschrift (für ihre Beschreibung)
    gruppe_darin: tuple | None = None  # (Beschreibungszeilen, Elternpfad, Tiefe) der laufenden Gruppe
    gruppen_nachtrag: list[tuple] = []  # (Einheit, Beschreibungszeilen): am Ende hinter ihr Darin
    stueck_modus: str | None = None  # Satz bzw. Liste eines Stücks ohne Nummer im Schlussteil (zur Bestandszeile)
    stueck_vorher: tuple = ()
    umleitung: tuple | None = None  # (Unterpunkt, Abschnitt): «–»-Einträge auf Abschnittsebene (VII.494.)
    liste_im_inhalt: tuple | None = None  # (x0, pfad) des letzten Listenpunkts einer Kurzliste im Inhalt (VII.191.)
    aufz_im_inhalt: tuple | None = None  # eingerückte Aufzählung nach «… enthält:» (x0, letzte Nummer)
    kopfblock = False  # nach einer Bereichsüberschrift «4.2.22. bis 4.2.67.»: Zeilen bis zur nächsten Signatur dazu
    kopf_darin: list[Zeile] = []  # Bereichskopf «2.8. – 9. …» mit Beschreibung: ins Darin der ersten Einheit danach
    serienkopf = False  # Titelblock einer weiteren Serie («Stadtarchiv Zürich V.G. c.50., 2. Serie» …)
    ueberspringen_bis = -1  # Folgezeilen eines mehrzeiligen Überschriftenblocks (schon als Überschrift gemerkt)
    ueberspringen: Zeile | None = None  # zweite Zeile eines Bereichs «10.1. –» / «10.48.» (schon verarbeitet)
    uebersicht_bis: int | None = None  # Übersicht mitten im Verzeichnis bis zur Wiederholung der Abschnittssignatur
    uebersicht_kopf = False  # endet die Übersicht mit der wiederholten Abschnittsüberschrift (sonst mit «4.1.»)
    # «–»-Einträge auf Abschnittsebene (VII.494.) nur, wenn das Findmittel sie grundsätzlich an den Signaturrand
    # setzt (nicht bloss ein verrutschter Strich, VII.12.B.) und Abschnitte mischt: erst «–»-Einträge, dann
    # nummerierte Unterpunkte («2.2. Reiseführer …» / «– H. Stüssi …» / «2.2.1. …»). Sonst sind es die Listen der
    # Unterpunkte («1.4.1. Statuten …» / «- Entwurf …», VII.360.)
    links_x = min((z.x0 for z in zeilen), default=0.0)
    am_rand = [ist_aufzaehlung(z) and z.x0 <= links_x + 3 for z in zeilen]
    striche = [z.x0 for z in zeilen if ist_aufzaehlung(z)]
    nummern = [(k, z.text.split(" ", 1)[0]) for k, z in enumerate(zeilen)
               if z.x0 <= links_x + 3 and re.match(r"\d{1,3}\.(?:\d{1,3}\.)*\s", z.text)]
    gemischt = sum(1 for (a, p), (b, q) in zip(nummern, nummern[1:])
                   if q.startswith(p) and len(q) > len(p) and any(am_rand[a + 1:b]))
    striche_am_rand = len(striche) >= 3 and sum(am_rand) >= 0.7 * len(striche) and gemischt >= 2
    # Inhaltsübersicht mit Seitenzahlen mitten im Verzeichnis («A. Persönliches S. 2» … «N. Verschiedenes S. 5»
    # unter «2. Myrthe Wedekind-Güttinger», VII.232.): mindestens drei solche Zeilen hintereinander, keine Einheiten
    seitenref = [z.x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG and re.match(r"(?:[A-Z]|[IVX]{1,4}|\d{1,2})[.)]\s", z.text)
                 is not None and re.search(r"\bS\.\s?\d{1,3}(?:\s?[-–]\s?\d{1,3})?$", z.text) is not None
                 for z in zeilen]
    uebersicht_ids: set[int] = set()
    k = 0
    while k < len(zeilen):
        j, n_ref = k, 0
        # Folgezeilen eines Eintrags («C. Escher Wyss, Maschinenfabrik S. 3» / «(Drucksachen)») gehören dazu
        while j < len(zeilen) and (seitenref[j] or n_ref and j + 1 < len(zeilen) and seitenref[j + 1]
                                   and not re.match(r"(?:[A-Z]|[IVX]{1,4}|\d{1,2})[.)]\s", zeilen[j].text)):
            n_ref += seitenref[j]
            j += 1
        if n_ref >= 3:
            uebersicht_ids.update(id(zeilen[x]) for x in range(k, j))
            if k and ist_verzeichniswort(zeilen[k - 1].text):  # «Übersicht» darüber
                uebersicht_ids.add(id(zeilen[k - 1]))
        k = max(j, k + 1)
    # Schachtelübersicht nach dem Verzeichnis: «Aufteilung des Bestandes in Schachteln:» / «Schachtel 1: 1. Protokoll» /
    # «2. Geschäftskontrolle» / «3. Akten, Nrn. 1a - 2 b = Mappen 1 - 10» / «Schachtel 2: 3. Akten, …» … «Schachtel 5:
    # 5. Buchhaltung» (VII.11.): keine Einheiten und keine Teile – die Schachteln gelten für die genannten Nummern
    box_uebersicht: dict[tuple, list[str]] = {}
    for k_u, z_u in enumerate(zeilen):
        if not re.fullmatch(r"(?:Aufteilung|Verteilung|Einteilung)\b.{0,40}\bSchachteln\s*:", z_u.text.strip()):
            continue
        j_u, box_nr, block = k_u + 1, None, []
        while j_u < len(zeilen):
            t_u = zeilen[j_u].text.strip()
            m_b = re.match(r"Schachtel\s+(\d{1,4}[a-z]?)\s*:\s*(\d{1,3}(?:\.\d{1,3})*)\.\s+\S", t_u)
            m_n = re.match(r"(\d{1,3}(?:\.\d{1,3})*)\.\s+\S", t_u)
            if m_b:
                box_nr = m_b.group(1)
                block.append((j_u, box_nr, tuple(m_b.group(2).split("."))))
            elif m_n and box_nr is not None and zeilen[j_u].x0 > zeilen[k_u].x0 + 20:
                block.append((j_u, box_nr, tuple(m_n.group(1).split("."))))
            else:
                break
            j_u += 1
        if len({b for _, b, _ in block}) >= 2:
            uebersicht_ids.add(id(z_u))
            for j_b, b, pfad_b in block:
                uebersicht_ids.add(id(zeilen[j_b]))
                box_uebersicht.setdefault(pfad_b, []).append(b)
    grund_groesse = Counter(round(w.size) for z in zeilen for w in z.worte).most_common(1)
    grund_groesse = grund_groesse[0][0] if grund_groesse else 12
    fussnote_seite = None  # Seite, auf der eine Fussnote begonnen hat (Folgezeilen in kleiner Schrift gehören dazu)
    fussnote_ziel: Vorkommen | None = None  # Einheit, deren Darin die laufende Fussnote aufnimmt
    gruppenkopf_bis = -1  # letzte Zeile einer mehrzeiligen Gruppenüberschrift (siehe «Bände» unten)
    for i, z in enumerate(zeilen):
        vor = zeilen[i - 1] if i else None
        nach = zeilen[i + 1] if i + 1 < len(zeilen) else None
        if i <= gruppenkopf_bis:
            merke(z, "ueberschrift")
            continue
        if id(z) in uebersicht_ids:
            merke(z, "ueberschrift")
            continue
        if i < ueberspringen_bis:  # Folgezeile eines Überschriftenblocks (schon gemerkt)
            continue
        if z is ueberspringen:
            merke(z, "einheit", aktuell)
            continue
        if uebersicht_bis is not None:
            if i < uebersicht_bis:  # Zeile der Übersicht: Darin des Abschnitts, keine Einheit
                aktuell.zeilen.append(z)
                merke(z, "einheit", aktuell)
                continue
            uebersicht_bis = None
            if uebersicht_kopf:
                merke(z, "wiederholung")  # wiederholte Abschnittsüberschrift nach der Übersicht
                continue
        # Fussnote am Seitenende: hochgestellte Nummer «⁵ Seit 1898 bestand …» in kleiner Schrift (V.F.c.28.)
        klein = max(x.size for x in z.worte) <= grund_groesse - 1.5
        if len(z.worte) > 1 and z.worte[0].size <= 7.5 and z.worte[1].size > z.worte[0].size + 2 and klein \
                and re.fullmatch(r"\d{1,3}", z.worte[0].text):
            # ins Darin der Einheit mit dem Fussnotenzeichen auf derselben Seite («… FMB ¹ -» / «¹ KVA steht für …»,
            # V.F.c.28.), sonst eines am Wort klebenden Zeichens («Arbeitnehmer²»), sonst der letzten Einheit der Seite
            fussnote_seite, nr = z.seite, z.worte[0].text
            def hat_zeichen(x: Zeile, angeklebt: bool, seite: int) -> bool:
                if x.seite != seite:
                    return False
                if not angeklebt:
                    # hochgestellt = deutlich kleiner als die übrigen Wörter der Zeile (8 pt in 11-pt-Text, V.F.c.29.;
                    # 9,1 pt hinter «1969)» in einer 13,9-pt-Überschrift, VII.416.)
                    gross = max((w.size for w in x.worte if w.text != nr), default=0)
                    return any(w.text == nr and (w.size <= 7.5 or w.size <= gross - 2) for w in x.worte[1:])
                # («Arbeitnehmer²», auch hinter Klammer oder Anführung: «(1894 – 1969)¹» als «1969)1», VII.416.)
                return any(re.fullmatch(rf"[A-Za-zÄÖÜäöüß»“\")]+{nr}[.,;:]?|\S*[)»“\"]{nr}[.,;:]?", w.text)
                           for w in x.worte)
            # auf derselben Seite, sonst auf der Seite davor (Zeichen unten auf S. 2, Text oben auf S. 3)
            fussnote_ziel = next((v for seite in (z.seite, z.seite - 1) for angeklebt in (False, True)
                                  for v in reversed(vorkommen)
                                  if any(hat_zeichen(x, angeklebt, seite) for x in v.zeilen)), None)
            if fussnote_ziel is None and aktuell is not None and any(x.seite == z.seite for x in aktuell.zeilen):
                fussnote_ziel = aktuell
                aktuell.hinweise.append(f"Fussnote {nr} ohne erkennbares Zeichen hier angefügt – bitte prüfen.")
            if fussnote_ziel is None:
                merke(z, "fussnote")
                continue
            fz = Zeile(z.seite, z.top, z.bottom, [Wort(f"Fussnote {nr}:", z.worte[0].x0, z.worte[0].x1,
                                                       z.worte[1].font, z.worte[1].size)] + z.worte[1:])
            fussnote_ziel.zeilen.append(fz)
            merke(fz, "einheit", fussnote_ziel)
            continue
        if fussnote_seite == z.seite and klein:
            if fussnote_ziel is not None:
                fussnote_ziel.zeilen.append(z)
                merke(z, "einheit", fussnote_ziel)
            else:
                merke(z, "fussnote")
            continue
        fussnote_seite = None
        gl.kind_von = aktuell.pfad if aktuell is not None and (
            gl.modus == "dezimal" or aktuell.typ == "voll" and not aktuell.ist_teil
            and all(k.isdigit() for k in aktuell.pfad)) else ()
        gl.vorschau = nach.worte[0].text if nach is not None and nach.worte else ""
        k_dez = bisect.bisect_right(dezimal_zeilen, i)
        gl.naechste_dezimal = zeilen[dezimal_zeilen[k_dez]].worte[0].text \
            if k_dez < len(dezimal_zeilen) and dezimal_zeilen[k_dez] - i <= 8 else ""
        gl.letzter_pfad = aktuell.pfad if aktuell is not None else ()
        gl.letzte_marke = (aktuell.x0, aktuell.fett) if aktuell is not None and aktuell.x0 else ()
        gl.inhalt_zeilen = len(aktuell.zeilen) if aktuell is not None else 0
        probe = lies_signatur(z, gl.kopie())
        # bekannte Nummer, aber deutlich eingerückt: Aufzählung im Inhalt («Originalhefte:» / «1. Heft: …», VII.194.)
        # (VII.200. rückt wiederholte Signaturen bis 15 pt ein – das sind echte Teile)
        eingerueckt = probe is not None and probe.pfad in erste_x0 and len(probe.pfad) == 1 \
            and z.x0 > erste_x0[probe.pfad] + 25 and not (gl.einrueck_x and z.x0 > gl.einrueck_x)
        # neue Unternummer, deutlich eingerückt, die zu einer früheren Hauptnummer zurückspringt: Aufzählung
        # im Inhalt («7. Bauordnung …» / «2. Wohnungsbauförderung» / «2.1. Massnahmen …», V.B.b.46.)
        zurueck = probe is not None and not eingerueckt and gl.modus == "dezimal" and len(probe.pfad) >= 2 \
            and probe.pfad not in gesehen and aktuell is not None and probe.pfad[0].isdigit() \
            and aktuell.pfad[0].isdigit() and int(probe.pfad[0]) < int(aktuell.pfad[0]) \
            and probe.pfad[:1] in erste_x0 and z.x0 > erste_x0[probe.pfad[:1]] + 20
        # Kurzliste mitten in einer langen Liste derselben Einrückung: «Musikanten:» / «1. Eduard , Kupferschmid,
        # No 343» / «2. Ernst, No 395» in der Fotoliste von «D) FOTOS wie folgt:» (VII.191.) – Listenpunkte im
        # Inhalt, keine Einheiten (anders «Acht Aktenstücke enthaltend:» / «1.» … «8.» gleich unter dem Titel)
        inhaltsliste = False
        if probe is not None and gl.modus == "gliederung" and aktuell is not None and probe.pfad[-1].isdigit():
            if liste_im_inhalt is not None:
                lx, lp = liste_im_inhalt
                inhaltsliste = abs(z.x0 - lx) <= 2 and probe.pfad[:-1] == lp[:-1] and lp[-1].isdigit() \
                    and int(probe.pfad[-1]) == int(lp[-1]) + 1
            elif probe.pfad[-1] == "1" and vor is not None and aktuell.zeilen and aktuell.zeilen[-1] is vor \
                    and vor.text.rstrip().endswith(":") and abs(vor.x0 - z.x0) <= 2 and not aktuell.ist_teil \
                    and sum(1 for x in aktuell.zeilen if abs(x.x0 - z.x0) <= 2) >= 10:
                inhaltsliste = True
            if inhaltsliste:
                liste_im_inhalt = (z.x0, probe.pfad)
        # Ordnungszahl im Text, tiefer eingerückt als die laufende Unternummer und mit weniger Stellen: «1.
        # Kammermusikabend, Tonhalle-Quartett …» (x 105) unter «20.1. Plakate …» (x 57, VII.151.) – Inhalt
        if probe is not None and aktuell is not None and aktuell.x0 and len(probe.pfad) < len(aktuell.pfad) \
                and z.x0 > aktuell.x0 + 30 and all(k.isdigit() for k in probe.pfad + aktuell.pfad) \
                and "Bold" not in z.worte[0].font:
            inhaltsliste = True
        # Aufzählung im Inhalt nach «Die Chronik enthält:» – «1. Verzeichnis der Autoren» … «5. Verzeichnisse der
        # Mitglieder …», gegenüber der Signatur der laufenden Einheit eingerückt (VII.99.): keine Einheiten 2.–5.
        if aufz_im_inhalt is not None and z.worte and abs(z.x0 - aufz_im_inhalt[0]) > 2 and probe is not None:
            aufz_im_inhalt = None
        if probe is not None and aktuell is not None and aktuell.x0 and len(probe.pfad) == 1 \
                and probe.pfad[0].isdigit():
            if aufz_im_inhalt is not None and int(probe.pfad[0]) == aufz_im_inhalt[1] + 1:
                inhaltsliste, aufz_im_inhalt = True, (aufz_im_inhalt[0], aufz_im_inhalt[1] + 1)
            elif probe.pfad[0] == "1" and vor is not None and vor.text.rstrip().endswith(":") \
                    and z.x0 > aktuell.x0 + 25 and abs(vor.x0 - z.x0) <= 2:
                inhaltsliste, aufz_im_inhalt = True, (z.x0, 1)
        # (auch mit abgekürztem Ende: «2.8. – 9. „Jahrbüchli“ (Merkbücher, Memoranda), 2 Bände, in Schuber» / «Eingetragen
        # sind persönliche Daten …» vor «2.8. Jahrbüchli, Band 1», VII.400. – die Beschreibung gehört zu 2.8./2.9.)
        # (nur wenn das Ende knapp über dem Anfang liegt und beide Nummern danach einzeln folgen – nicht «5.2.4.31. -
        # 85. Geburtstag von Fritz Hochwälder …», VII.200.)
        m_bk = re.match(r"[–-]\s*(\d{1,3})\.\s+\S", probe.rest.text.strip()) \
            if probe is not None and probe.rest is not None and gl.modus == "dezimal" and len(probe.pfad) >= 2 \
            and probe.pfad[-1].isdigit() else None
        bereich_kurz = m_bk is not None and int(probe.pfad[-1]) < int(m_bk.group(1)) <= int(probe.pfad[-1]) + 10 \
            and any((t_n := lies_signatur(x, gl.kopie())) is not None and t_n.pfad == probe.pfad
                    for x in zeilen[i + 1:i + 6]) \
            and any((t_n := lies_signatur(x, gl.kopie())) is not None
                    and t_n.pfad == probe.pfad[:-1] + (m_bk.group(1),) for x in zeilen[i + 1:i + 40])
        if probe is not None and probe.rest is not None and gl.modus == "dezimal" \
                and re.match(r"bis\s+\d{1,3}(?:\.\d{1,4})+\.?(?:\s|$)", probe.rest.text.strip()) or bereich_kurz:
            merke(z, "ueberschrift")
            zwischentitel, kopfblock = z.text.strip(), True
            if bereich_kurz:
                kopf_darin = [z]
            continue
        # Initiale am Zeilenanfang als Fortsetzung der Zeile davor: «"En unfehlbars Schönheitsmittel" von» /
        # «B. Grützner-Zaugg 1916» (VII.197.) – kein Buchstabe «B.» der Gliederung; ebenso nach einer
        # Personenbezeichnung: «- Schreiben des Stadtpräsidenten R. Billeter an Herrn ¦ 25. Mai 1912» / «A. Bodmer»
        # (VII.37.: sonst erfundene Einheiten 3.A., 3.E.)
        if probe is not None and vor is not None and re.fullmatch(r"[A-ZÄÖÜ]\.|[IVXL]{1,5}\.", z.worte[0].text) \
                and luft(vor, z) <= 4 and vor.text.split() \
                and (vor.text.split()[-1] in ANSCHLUSS_WOERTER or vor.text.split()[-1].lower() in ANSCHLUSS_KLEIN
                     or vor.text.rstrip()[-1:] in ",&+"
                     or PERSONENBEZEICHNUNG_AM_ENDE_RE.search(re.sub(rf"\s+{JAHR}\s*$", "", vor.text.rstrip()))):
            # (auch vor einer Datumsspalte: «… im Seitenprofil; Künstler: ¦ 1929» / «A. Engelhardt», VII.109.)
            inhaltsliste = True  # (nicht «a)» nach «… Handwerks:», VII.179.)
        if probe is not None and ist_namenstabellenzeile(zeilen, i):
            inhaltsliste = True  # Autor in einer Tabelle Autor | Titel | Heft (V.L.205.)
        # zwei Initialen vor einem Nachnamen: «B. G. Mantegazzi, Hans Waldmann, Komposition (Marsch) …» unter «Mappe 6»
        # (VII.37.) – ein Personenname, kein Buchstabe der Gliederung (sonst erfundene Einheit 6.B.)
        if probe is not None and len(z.worte) >= 3 and re.fullmatch(r"[A-ZÄÖÜ]\.", z.worte[0].text) \
                and re.fullmatch(r"[A-ZÄÖÜ]\.", z.worte[1].text) and z.worte[1].x0 - z.worte[0].x1 < 6 \
                and re.fullmatch(r"[A-ZÄÖÜ][a-zäöüßéèàç'’\-]+,?", z.worte[2].text):
            inhaltsliste = True
        # Überschrift mit Anzahl vor einer bei 1 beginnenden Liste: «9 Stadträte» / «1. Dr. Emil Landolt …»
        # (V.L.136.b.) – keine Signatur 9, sondern eine Zwischenüberschrift
        if probe is not None and aktuell is None and len(probe.pfad) == 1 and probe.pfad[0].isdigit() \
                and probe.pfad[0] != "1" and not probe.pfad[0].startswith("0") and "." not in probe.roh \
                and not gl.registratur and not gl.buchstaben and nach is not None and re.match(r"1\.\s", nach.text) \
                and len(z.worte) <= 6 and not z.datum:
            merke(z, "ueberschrift")
            zwischentitel = z.text.strip()
            continue
        if probe is not None and len(probe.pfad) == 1 and probe.typ != "voll" \
                and re.fullmatch(r"\d{1,3}\.", z.worte[0].text) and spaeter_groesser(i, z):
            inhaltsliste = True
        if probe is not None and len(probe.pfad) == 1 and probe.typ != "voll" \
                and re.fullmatch(r"\d{1,3}", z.worte[0].text) and spaeter_mit_punkt(i, z):
            inhaltsliste = True
        # «Anmerkungen zum Bestand V.C. b.368.» auf den letzten Seiten / «Laut Protokoll … ist weiteres Material …
        # ins Stadtarchiv gegeben worden:» / «1. Ernennung …» … «7. …» (V.C.b.368.): Notizen zum Bestand, keine
        # Einheiten (sonst Teile von 1.–7.)
        # allein stehendes «Anhang» als Überschrift auf den letzten Seiten (14 pt, darunter «Verweis auf andere
        # Archivbestände» / «V.J. b.301. Aufnahmeprotokoll …», V.J.c.402.): ab hier Info-Blatt, auch die Überschrift
        if not im_anhang and z.seite >= max(2, letzte_seite - 1) and re.fullmatch(r"Anhang\s*:?", z.text.strip()) \
                and (z.worte[0].size >= 13 or all("Bold" in w.font for w in z.worte)):
            im_anhang = True
        # (auch weiter vorn, wenn danach keine Signatur mehr folgt: fett «Anhang:» S. 19 von 21 mit Gebäck-Modeln,
        # Medaillen, Orden … (VII.190.); «Anhang zum Detailverzeichnis Aktienbauverein Zürich» 14 pt oben auf S. 26
        # mit einer Tabelle der Baugruppen, VII.24.)
        # (in Textgrösse «Anhang:» oben auf S. 19, danach eine eigene Zählung «1.# Gebäck-Model» … «4. Gegenstände …»
        # unter der letzten Nummer 51., VII.190.: die Folge der Signaturen geht nicht weiter)
        if not im_anhang and aktuell is not None and probe is None and z.worte and z.x0 <= SIGNATUR_SPALTE_MAX \
                and len(z.text) <= 80 and (
                    re.fullmatch(r"Anhang\s*:?", z.text.strip()) and (z.worte[0].size >= 13 or luft(vor, z) > 20
                                                                    or all("Bold" in w.font for w in z.worte))
                    or re.match(r"Anhang\s+(?:zu[mr]?|des|der)\b", z.text.strip())
                    and z.worte[0].size >= grund_groesse + 1.5):
            spaeter = [t for t in (lies_signatur(x, gl.kopie()) for x in zeilen[i + 1:]) if t is not None]
            if not spaeter or aktuell.pfad and aktuell.pfad[0].isdigit() and all(
                    not t.pfad or not t.pfad[0].isdigit() or int(t.pfad[0]) < int(aktuell.pfad[0]) for t in spaeter):
                im_anhang = True
                # (die Zeilen zählen weiter für den rechten Rand der Textspalte wie früher im Darin der letzten Einheit –
                # sonst ändert sich das Zusammenfügen der Zeilen im ganzen Verzeichnis, VII.190.)
                weg = [x for x in zeilen[i:] if x.worte and not ist_schlussvermerk(x.text.strip())]
                if any(x.datum or x.umfang for x in aktuell.zeilen + weg):
                    info.setdefault("rand_zusatz", []).extend(
                        weg + ([] if any(x.datum or x.umfang for x in aktuell.zeilen) else list(aktuell.zeilen)))
        # ebenso «Anhang: Vorhelvetische Urkunden» (fett, S. 9 von 12, VII.1.), wenn danach keine Signatur mehr folgt
        if not im_anhang and aktuell is not None and z.x0 <= SIGNATUR_SPALTE_MAX and len(z.text) <= 80 \
                and re.match(r"Anhang\s*:\s*\S", z.text.strip()) and all("Bold" in w.font for w in z.worte) \
                and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
            im_anhang = True
        # «Nicht im Detail verzeichnet (Vgl. Zusammenfassung vorn.)» auf der letzten Seite (VII.174.): was folgt, steht
        # nur als Kurzliste da (die Einheiten kommen aus der Zusammenfassung) – Info-Blatt, nicht Darin der letzten Einheit
        if not im_anhang and z.seite >= max(2, letzte_seite - 1) and z.x0 <= SIGNATUR_SPALTE_MAX \
                and re.match(r"Nicht im Detail verzeichnet\b", z.text.strip(), re.I) \
                and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
            im_anhang = True
        # «Anmerkungen zum Bestand V.L. 167.» (16 pt) auf den letzten Seiten: ab hier Info-Blatt, auch die Überschrift
        if not im_anhang and len(z.text) <= 80 and z.seite >= max(2, letzte_seite - 1) and re.match(
                r"(?:Anmerkungen|Bemerkungen)\s+zu(?:m|r)?\s+(?:diesem\s+)?(?:Teil)?[Bb]estand(?:es)?\b", z.text.strip()):
            im_anhang = True
        # Anmerkungen zu einer bestimmten Schachtel nach der letzten Einheit: «Anmerkungen zu Schachtel 29:» / «- Gut zum
        # Weinberg, …» (VII.330.) – ins Darin der Einheit mit dieser Schachtel bzw. Nummer, nicht ins Blatt Info
        m_zu = re.match(r"(?:Anmerkung|Bemerkung|Hinweis)(?:en|e)?\s+zu[mr]?\s+(?:Schachtel|Mappe|Nr\.?)\s*(\d{1,4})\s*:?$",
                        z.text.strip()) if not im_anhang and probe is None and aktuell is not None else None
        if m_zu:
            ziel_zu = next((v for v in vorkommen if not v.ist_teil and (v.schachtel == m_zu.group(1)
                                                                        or v.pfad == (m_zu.group(1),))), None)
            if ziel_zu is not None and ziel_zu is not aktuell \
                    and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
                aktuell = ziel_zu
                aktuell.hinweise.append(f"«{z.text.strip()}» steht im Findmittel nach der letzten Einheit – hier im "
                                        "Darin dieser Einheit übernommen.")
        # Überschrift eines Schlussabschnitts ohne «Anhang» davor, nach der keine Signatur und keine Schachtel mehr
        # folgt: «Literatur» (16 pt, VII.400.), «Ausgewählte Literatur und Hinweise zu den Personen» (14 pt, VII.144.),
        # «Genealogische Quellen:» (VII.390.), «Verweise auf andere Bestände» (V.L.71.), «Bemerkungen» (fett,
        # V.L.126.), «Darstellungen und Mitgliederverzeichnisse in der Bibliothek des Stadtarchivs» (VII.309.) – auch
        # in Textgrösse, wenn sie links vom Darin der letzten Einheit steht («Die Literatur bis 1968 ist verzeichnet
        # bei:», V.L.82.): ab hier Info-Blatt, auch die Überschrift (sonst Literatur und Notizen im Darin)
        # (auch fett weiter rechts: «HEINRICH WEHRLI (1834-1909): Biografisches» bei x 185, VII.257.)
        if not im_anhang and aktuell is not None and probe is None and z.worte and not m_zu \
                and (z.x0 <= SIGNATUR_SPALTE_MAX and (
                    ist_schlusskopf(z, grund_groesse)
                    or len(z.worte) <= 10 and len(z.text.strip()) <= 100 and SCHLUSSKOPF_RE.match(z.text.strip())
                    and luft(vor, z) > ABSATZ_ABSTAND and links_vom_darin(z, aktuell))
                     or z.x0 <= 300 and ist_schlusskopf(z, grund_groesse) and luft(vor, z) > 20) \
                and not any(lies_signatur(x, gl.kopie()) is not None
                            or SCHACHTEL_RE.match(x.text.strip()) and not SCHACHTEL_VERWEIS_RE.match(x.text.strip())
                            for x in zeilen[i + 1:]):
            im_anhang = True
        # Absatz zur Bestandsgeschichte nach der letzten Einheit, ohne Überschrift, nach einem Abstand in der Signatur-
        # spalte und vor dem Schlussvermerk: «1928 wurde der Verein „Schweizerische Reisevereinigung“ gegründet, …»
        # (VII.312.), «Auf Gesuch der Schweizerischen Gesellschaft … spricht der Stadtrat mit StRB 1492 …» (VII.108.),
        # «Eine Auswahl von Plänen kopierte der GeoPrintShop … in den Archivbestand integriert.» (V.G.c.118.)
        # (nur in der Spalte der Signatur der letzten Einheit, nicht ihr eingerückter Inhalt; links vom eingerückten
        # Darin auch nach kleinem Abstand: «Der Volleyballclub Spada Academica Zürich … Gegründet wurde der Verein im
        # Jahre 1959.» 17 pt unter dem letzten Wimpel, VII.403.)
        if not im_anhang and aktuell is not None and probe is None and z.worte and z.x0 <= SIGNATUR_SPALTE_MAX \
                and aktuell.x0 and z.x0 <= aktuell.x0 + 3 \
                and (luft(vor, z) > 12 or luft(vor, z) > 3 and links_vom_darin(z, aktuell)) \
                and z.text.strip()[:1].isalnum() and len(z.text) >= 50 \
                and z.seite >= letzte_seite - 1 and ist_schlussabsatz(zeilen, i, gl):
            im_anhang = True
        # Stück ohne Nummer im Schlussteil: «Dem Bestand liegen bei:» mit der Liste darunter (VII.394.), «Beim Bestand
        # befinden sich ferner 4 Ausstellungstafeln …» unter «Anmerkungen:» (VII.34.), «Drei Archivschachteln enthalten
        # Drucksachen des Heizamtes ab 1945.» (V.G.b.903.), «In Schachtel 9 befindet sich ferner ein "Schachtelregister
        # …"» (VII.308.A.) – der Satz bzw. die Liste zur Zeile für den Bestand (Regel 31), der übrige Schlussteil bleibt
        # im Blatt Info
        t_st = z.text.strip()
        if stueck_modus is None and probe is None and aktuell is not None and z.worte and z.x0 <= SIGNATUR_SPALTE_MAX \
                and (STUECK_SCHLUSS_RE.match(t_st)
                     or STUECK_SATZ_RE.match(t_st) and (im_schluss or im_anhang or i > len(zeilen) - 15)) \
                and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
            stueck_vorher = (aktuell, im_anhang, im_schluss, z.x0)
            stueck_ohne_nummer(z)
            stueck_modus = "liste" if t_st.endswith(":") else "satz"
            im_anhang = im_schluss = False
        if stueck_modus is not None:
            aktuell.zeilen.append(z)
            merke(z, "einheit", aktuell)
            nach_st = zeilen[i + 1] if i + 1 < len(zeilen) else None
            t_nach = nach_st.text.strip() if nach_st is not None else ""
            if stueck_modus == "satz" and (luft(z, nach_st) > ABSATZ_ABSTAND or ist_schlussvermerk(t_nach)
                                           or VERMERK_DATUM_RE.match(t_nach)) \
                    or stueck_modus == "liste" and (nach_st is None or luft(z, nach_st) > 30
                                                     or nach_st.x0 <= stueck_vorher[3] + 3
                                                     or ist_schlussvermerk(t_nach) or VERMERK_DATUM_RE.match(t_nach)) \
                    or nach_st is None:
                aktuell, im_anhang, im_schluss = stueck_vorher[:3]
                stueck_modus = None
            continue
        # (im Schlussblock eine fette Überschrift eines Stücks ohne Nummer: «Reproduktionen (Beilage):», VII.336.)
        if im_anhang and probe is None and aktuell is not None and aktuell.typ != "bestand" and z.worte \
                and z.x0 <= SIGNATUR_SPALTE_MAX and all("Bold" in w.font for w in z.worte) \
                and STUECK_KOPF_RE.match(z.text.strip()) \
                and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
            im_anhang = False
            stueck_ohne_nummer(z)
        if im_anhang:
            info.setdefault("schluss", []).append(schlusszeile(z, z.text.strip()))
            # (eine Zuordnungsliste im Schlussteil gilt trotzdem: «Aufteilung der Publikationen nach Schachteln:» /
            # «Schachtel 1: Nummern 1.1. bis 1.25.» …, VII.255.)
            m_zo = ZUORDNUNG_RE.fullmatch(z.text.strip())
            if m_zo:
                zuordnung.append((m_zo.group(1), tuple(m_zo.group(2).split(".")),
                                  tuple(m_zo.group(3).split(".")) if m_zo.group(3) else None,
                                  merke(z, "schachtel", None, None, m_zo.group(1))))
            else:
                merke(z, "schluss")
            continue
        # «Keine Nr. Französische Photographie 1840 – 1871, …» (X.G.) bzw. nur die Bestandssignatur in der Signaturspalte
        # «VII. 138. Fotografien» (VII.138.): ein Stück ohne Nummer
        if probe is None and aktuell is not None and aktuell.typ != "bestand" and z.worte \
                and z.x0 <= SIGNATUR_SPALTE_MAX and (
                    re.match(r"(?:Keine|Ohne|o\.)\s*Nr\.?(?:\s|$)", z.text.strip())
                    or re.match(r"Zu diesem Bestand gehör(?:t|en) (?:auch|ferner|ausserdem)\b", z.text.strip())
                    and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:])
                    or (gl.bestand and len(z.worte) >= 2 and any(
                        n < len(z.worte) and normalisiere_signatur(" ".join(x.text for x in z.worte[:n])) == gl.bestand
                        and z.worte[n].text[:1].isupper() for n in (1, 2)))):
            stueck_ohne_nummer(z)
        # Eintrag ohne Nummer in der Nummernspalte einer Liste «Bände Nr. 15 – 25 ¦ Kontrollbücher der Markenverwaltung»:
        # «Drucksache Kriegsursachen im Urteile des Auslandes, Berlin 1917.» (VII.60.) – ein Stück ohne Nummer
        if probe is None and aktuell is not None and aktuell.typ not in ("bestand",) and aktuell.x0 and z.worte \
                and abs(z.x0 - aktuell.x0) <= 3 and re.match(r"(?:Schachteln?|Bände|Band|Mappen?|Ordner)\b.{0,12}\bNr\.",
                                                             aktuell.roh or "") \
                and re.match(r"(?:Drucksachen?|Broschüren?|Zeitschriften?|Plakate?|Flugblätter|Flugblatt)\s+\S",
                             z.text.strip()):
            stueck_ohne_nummer(z)
        # fette Gruppenüberschrift ohne Signatur links der letzten Einheit, nach der keine Signatur mehr folgt: «Mappe –
        # Porträt (Grossformat)» / «Porträt von Hans Pestalozzi, gestochen …» nach «20. Dankesschreiben …» (VII.75.) –
        # bleibt im Darin, mit Hinweis
        if probe is None and not im_schluss and aktuell is not None and aktuell.x0 and z.worte \
                and all("Bold" in w.font for w in z.worte) \
                and z.x0 <= SIGNATUR_SPALTE_MAX and z.x0 + 20 < aktuell.x0 and 1 < len(z.worte) <= 8 \
                and not ist_schlussvermerk(z.text.strip(), vor, z) and not TABELLENKOPF_RE.match(z.text.strip()) \
                and not ist_tabellenkopf(z.text.strip()) \
                and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
            stueck_ohne_nummer(z)
        # Zahl am Anfang einer Inhaltszeile in der Textspalte der laufenden Einheit, die nicht deren nächste Nummer
        # ist: «1. Akten» (x 71, 14 pt) / «7 Einladungen zur Erinnerung …» (x 128, 12 pt) … «2. Drucksachen»
        # (V.L.80.; ebenso «3 Auszüge aus dem Urkundenregister», V.L.37.) – eine Stückzahl, keine Signatur
        # (auch die nächste Nummer, wenn sie eine Liste derselben Spalte fortsetzt: «7. Bericht über die Tätigkeit …»
        # bei x 71 / eingerückt «1.» … «7. Wildberg», «8. Verschiedene Auszüge …» … «21.» bei x 107 / «8. Nachträge»
        # bei x 71, VII.67.)
        if probe is not None and aktuell is not None and aktuell.x0 and probe.typ != "voll" \
                and len(probe.pfad) == len(aktuell.pfad) == 1 and probe.pfad[0].isdigit() \
                and aktuell.pfad[0].isdigit() and z.x0 > aktuell.x0 + 25 and not gl.einrueck_x and not gl.registratur \
                and any(abs(x.x0 - z.x0) <= 3 for x in aktuell.zeilen[1:]) \
                and (int(probe.pfad[0]) != int(aktuell.pfad[0]) + 1
                     or any(abs(x.x0 - z.x0) <= 3 and re.match(rf"{int(probe.pfad[0]) - 1}\.?\s", x.text)
                            for x in aktuell.zeilen[1:])):
            inhaltsliste = True
        # Fortsetzung eines Verweises: «Siehe auch unten Aktiver Luftschutz V.B. c.57.:6. und Passiver Luftschutz» /
        # «V.B. c.57.:10.» (V.B.c.57.) – keine Einheit ohne Titel
        if probe is not None and probe.typ == "voll" and (probe.rest is None or not probe.rest.text.strip()) \
                and vor is not None and VERWEIS_ZEILE_RE.search(vor.text) and abs(vor.x0 - z.x0) <= 3 \
                and aktuell is not None and aktuell.x0 and z.x0 > aktuell.x0 + 20:
            inhaltsliste = True
        # Einheit, deren Inhalt die eigene Signatur für alles Folgende nennt: «2. Pläne („Zeichnungsmappen“)» /
        # «Signatur: Stadtarchiv Zürich V.G. c.42.:2» / Tabelle «Code Nr. Bezeichung» mit 192 Mappen (V.G.c.42.): die
        # Nummern der Tabelle («10 Apparatenhaus I», «X 28 Gasbehälter I») sind Inhalt – bis zur nächsten Nummer
        # derselben Stufe («3. Pläne in Mappen») oder einer Vollsignatur
        if aktuell is not None and gesperrt is not aktuell and gl.bestand and aktuell.anzeige:
            m_sig = re.match(r"Signatur:\s*(?:Stadtarchiv Zürich\s*)?(\S.*)$", z.text.strip())
            if m_sig and re.sub(r"[\s.:]", "", m_sig.group(1)) == re.sub(r"[\s.:]", "", gl.bestand + aktuell.anzeige):
                gesperrt = aktuell
        if probe is not None and gesperrt is not None and gesperrt is aktuell and probe.typ != "voll" \
                and not (len(probe.pfad) == len(aktuell.pfad) and probe.pfad[:-1] == aktuell.pfad[:-1]
                         and probe.pfad[-1].isdigit() and aktuell.pfad[-1].isdigit()
                         and int(probe.pfad[-1]) == int(aktuell.pfad[-1]) + 1):
            inhaltsliste = True
        treffer = None if eingerueckt or zurueck or inhaltsliste \
            else lies_signatur(z, gl.kopie() if im_schluss else gl)
        # im Schlussblock «Der Bestand umfasst:» / «5 Grf. Schachteln 0, 90 lfm»: Umfang, keine Signatur (VII.270.)
        if treffer and im_schluss and re.fullmatch(r"\d{1,4}", treffer.roh.strip()) \
                and re.search(r"\b(?:lfm|Laufmeter)\b|(?:Norm|Grf\.\s*)?(?:Schachteln|Mappen)\b", z.text):
            treffer = None
        elif treffer and im_schluss:
            treffer = lies_signatur(z, gl)  # echte Signatur: jetzt mit Zustand übernehmen
        if treffer:
            im_schluss = False
            liste_im_inhalt = None
            kopfblock = False
            resttext = treffer.rest.text.strip() if treffer.rest else ""
            s = SCHACHTEL_RE.match(resttext)
            typ = "buchstabe_nr" if " " in treffer.anzeige else treffer.typ
            if s and treffer.pfad in gesehen:
                # «11.1. Schachtel 2» (Signatur schon bekannt) ist ein Schachtelwechsel, keine Einheit;
                # «VI.HO.B.1.:1 Schachtel 1» (neue Signatur) dagegen eine Einheit
                marke_setzen(z, s.group(1), (treffer.pfad, treffer.anzeige, treffer.roh, typ))
                continue
            # Tippfehler in der vorletzten Stelle: «6.1.3.4. 1978/79 Saisonprospekt (fehlt)» nach 6.1.4.1.–6.1.4.3. – die
            # Nummer gibt es unter 6.1.3. schon, sie setzt aber die Zählung von 6.1.4. fort: 6.1.4.4. (VII.209.)
            lp_t = aktuell.pfad if aktuell is not None else ()
            if treffer.pfad in gesehen and gl.modus == "dezimal" and len(treffer.pfad) == len(lp_t) >= 3 \
                    and all(k.isdigit() for k in treffer.pfad + lp_t) and treffer.pfad[:-2] == lp_t[:-2] \
                    and treffer.pfad[-2] != lp_t[-2] and int(treffer.pfad[-1]) == int(lp_t[-1]) + 1 \
                    and lp_t[:-1] + (treffer.pfad[-1],) not in gesehen:
                neu_t = lp_t[:-1] + (treffer.pfad[-1],)
                treffer.hinweis = " ".join(filter(None, (treffer.hinweis, f"Im Findmittel «{treffer.roh}» nach "
                                                         f"{pfad_text(lp_t)} – als {pfad_text(neu_t)} gelesen "
                                                         "(Tippfehler?), bitte prüfen.")))
                treffer.pfad, treffer.anzeige = neu_t, pfad_text(neu_t)
            # Tippfehler in einer vorderen Stelle (Muster 10 der NP12): die Nummer gehört nach ihrem Präfix zu einer
            # fremden Gruppe, steht im PDF aber zwischen zwei Geschwistern einer anderen Gruppe und unterscheidet sich
            # nur in einer Ziffer von der Nummer, die dort fehlt: «20.1.2.19. Gastspiel … in Athen 1984» zwischen
            # 20.1.3.18. und 20.1.3.20. ist 20.1.3.19. (VII.12.B.; ebenso «3.3.7.» zwischen 3.4.6. und 3.4.8., VII.298.;
            # «1.224.3..» zwischen 1.2.25.2. und 1.2.25.4., VII.111.) – vor dem ersten Eintrag einer Reihe («28.1.1.3.
            # Gebundene Aufführungsplakate …» vor «27.1.1.3. Aufführungsplakate …») ihr Kopf, mitten in einer Reihe
            # derselben Nummer («1.1.2.1.1. Programme 1949/50» zwischen zwei «1.2.1.1. Programme …», VII.237.) ein Teil
            elif gl.modus == "dezimal" and len(lp_t) >= 2 and treffer.pfad != lp_t and treffer.pfad[:-1] != lp_t[:-1] \
                    and all(k.isdigit() for k in treffer.pfad + lp_t):
                k_n = bisect.bisect_right(dezimal_zeilen, i)
                m_n = re.fullmatch(r"(\d{1,3}(?:\.\d{1,3})+)\.?", zeilen[dezimal_zeilen[k_n]].worte[0].text) \
                    if k_n < len(dezimal_zeilen) else None
                nach_t = tuple(m_n.group(1).split(".")) if m_n else ()
                neu_t = ()
                if len(nach_t) == len(lp_t) and nach_t[:-1] == lp_t[:-1] and nach_t[-1].isdigit():
                    a_n, b_n, n_t = int(lp_t[-1]), int(nach_t[-1]), treffer.pfad[-1]
                    kand = lp_t[:-1] + (n_t,)
                    if b_n == a_n + 2 and int(n_t) == a_n + 1 and kand not in alle_dezimal and kand not in gesehen:
                        neu_t = kand
                    elif b_n == a_n + 1 and n_t == nach_t[-1] and nach_t not in gesehen:
                        neu_t = nach_t
                    elif b_n == a_n and n_t == lp_t[-1]:
                        neu_t = lp_t
                if neu_t and _eine_ziffer_anders("".join(treffer.pfad), "".join(neu_t)):
                    lage = f"zwischen {pfad_text(lp_t)} und {pfad_text(nach_t)}" if lp_t != nach_t \
                        else f"mitten unter den Einträgen {pfad_text(lp_t)}"
                    treffer.hinweis = " ".join(filter(None, (treffer.hinweis, f"Im Findmittel «{treffer.roh}» {lage} – "
                                                             f"als {pfad_text(neu_t)} gelesen (Tippfehler?), bitte "
                                                             "prüfen.")))
                    treffer.pfad, treffer.anzeige = neu_t, pfad_text(neu_t)
            wiederholt = treffer.pfad in gesehen
            # dieselbe Liste ein zweites Mal, anders geordnet: «2. Auswahl aus Theaterkritiken 1945 – 1977» (chronologisch)
            # … / «2. Auswahl aus Theaterkritiken (alphabetisch nach Autor) 1945 – 1977» (VII.266.) – kein Teil, sondern
            # weiter Darin derselben Einheit
            if wiederholt and aktuell is not None and aktuell.pfad == treffer.pfad and not aktuell.ist_teil \
                    and aktuell.zeilen and treffer.rest is not None and re.search(
                        r"\([^)]*\b(?:alphabetisch|chronologisch|nach (?:Autor(?:en)?|Titeln?|Jahren|Namen|Orten|Daten))\b"
                        r"[^)]*\)", resttext) \
                    and _titelanfang(re.sub(r"\(.*?\)", " ", resttext)) == _titelanfang(aktuell.zeilen[0].text):
                aktuell.zeilen.append(treffer.rest)
                aktuell.hinweise.append(f"Die Liste steht im Findmittel ein zweites Mal, anders geordnet («{z.text.strip()}») "
                                        "– im Darin angehängt, kein eigener Teil.")
                merke(z, "einheit", aktuell)
                continue
            # wiederholte Gruppensignatur direkt vor ihrer ersten Untersignatur: Zwischenüberschrift, kein Teil
            # («VIII. Nachträge:» … «VIII. Nachtrag A vom 28. August 2000» / «A. Abgabe von Materialien …», VII.191.)
            # (nur wenn seit der ersten Nennung nur deren Untereinheiten kamen und die erste Nennung nicht schwächer
            # gesetzt ist – sonst war sie ein Listenpunkt und erst die fette Wiederholung die Überschrift:
            # «2. Zusammenstellung der Aufführungen …» / «2. Drucksachen» fett, VII.99.)
            erste_i = next((n for n, v in enumerate(vorkommen) if v.pfad == treffer.pfad and not v.ist_teil), None) \
                if wiederholt else None
            erste_v = vorkommen[erste_i] if erste_i is not None else None
            if erste_v is not None and nach is not None and not (z.schachtel or z.umfang or z.datum) \
                    and not (treffer.fett and not erste_v.fett) \
                    and not (erste_v.zeilen and erste_v.zeilen[0].worte
                             and z.worte[0].size > erste_v.zeilen[0].worte[0].size + 0.5) \
                    and all(v.pfad[:len(treffer.pfad)] == treffer.pfad for v in vorkommen[erste_i + 1:]):
                kind = lies_signatur(nach, gl.kopie())
                if kind is not None and len(kind.pfad) > len(treffer.pfad) and kind.pfad not in gesehen \
                        and kind.pfad[:len(treffer.pfad)] == treffer.pfad:
                    merke(z, "ueberschrift")
                    zwischentitel = z.text.strip()
                    continue
            # Bereichsüberschrift auf einer Zeile «7.1. – 26. Detailverzeichnis zur Porträtgalerie …», «7.1. – 8.
            # Sammelrahmen I (Format …)», wenn die Einheiten des Bereichs danach einzeln folgen («7.1. Johannes Weber
            # …», VII.93.): keine Einheit, Überschrift für die folgende Einheit
            # (Gedankenstrich «– 26.» oder angehängter Bindestrich «-14.»; nicht «- 70. Geburtstag von …», VII.200.)
            m_bereich = BEREICH_ENDE_RE.match(resttext) if gl.modus == "dezimal" else None
            if m_bereich and treffer.pfad[-1].isdigit() and int(m_bereich.group(1)) > int(treffer.pfad[-1]):
                for x in zeilen[i + 1:i + 16]:
                    if not x.worte or x.x0 > z.x0 + 3:
                        continue
                    t_x = lies_signatur(x, gl.kopie())
                    if t_x is None:
                        continue
                    rest_x = t_x.rest.text.strip() if t_x.rest else ""
                    if t_x.pfad == treffer.pfad and not BEREICH_ENDE_RE.match(rest_x):
                        break  # die erste Einheit des Bereichs folgt einzeln
                    if not (t_x.pfad[:len(treffer.pfad) - 1] == treffer.pfad[:-1] and BEREICH_ENDE_RE.match(rest_x)):
                        m_bereich = None  # eine andere Einheit folgt
                        break
                else:
                    m_bereich = None
                if m_bereich is not None:
                    merke(z, "ueberschrift")
                    zwischentitel = z.text.strip()
                    continue
                # die Einheiten folgen nicht einzeln: eine Bereichseinheit «19.13.8.-19.13.13.» wie «10.1. –» /
                # «10.48.» («19.13.8.–13. Tonhalle – Kongresshaus Mappe 10», VII.151.)
                m_e = BEREICH_ENDE_RE.match(resttext)
                w_r = treffer.rest.worte if treffer.rest else []
                weg = 1 if w_r and re.fullmatch(r"[–-]\d{1,3}\.", w_r[0].text) else \
                    2 if len(w_r) > 2 and w_r[0].text in ("–", "-") and re.fullmatch(r"\d{1,3}\.", w_r[1].text) else 0
                if m_e and weg and not wiederholt and len(w_r) > weg:
                    bis = treffer.pfad[:-1] + (m_e.group(1),)
                    treffer = SigTreffer(treffer.pfad[:-1] + (f"{treffer.pfad[-1]}-{m_e.group(1)}",),
                                         f"{treffer.anzeige}-{pfad_text(bis)}", treffer.roh, treffer.rest.ab(weg),
                                         treffer.fett, treffer.typ, treffer.hinweis)
                    resttext = treffer.rest.text.strip()
            # Bereich über zwei Zeilen: «10.1. –» / «10.48.», «11.1. – ohne Beschreibung» / «11.20.» (VII.389.):
            # eine Einheit «10.1.-10.48.»
            if gl.modus == "dezimal" and resttext[:1] in ("–", "-") and nach is not None and len(treffer.pfad) >= 2 \
                    and treffer.pfad[-1].isdigit() and not wiederholt:
                m_bis = re.fullmatch(r"(\d{1,3}(?:\.\d{1,4})+)\.?", nach.text.strip())
                bis = tuple(m_bis.group(1).split(".")) if m_bis else ()
                if bis and bis[:-1] == treffer.pfad[:-1] and bis[-1].isdigit() \
                        and int(bis[-1]) > int(treffer.pfad[-1]) and abs(nach.x0 - z.x0) <= 3:
                    treffer = SigTreffer(treffer.pfad[:-1] + (f"{treffer.pfad[-1]}-{bis[-1]}",),
                                         f"{treffer.anzeige}-{pfad_text(bis)}", f"{treffer.roh} – {nach.text.strip()}",
                                         treffer.rest, treffer.fett, treffer.typ, treffer.hinweis)
                    ueberspringen = nach
            # «5.2.4.1. - Early Morning (Trauer zu früh), Komödie von Edward Bond (02.10.1969)» (VII.200.): der Strich
            # trennt nur Signatur und Titel – kein Listenpunkt, sonst wird der Titel zum Darin (nicht beim Bereich
            # «1.2.1. – ohne Auswertung» / «1.2.14.», VII.389., und nicht vor einer Zahl)
            # (und nicht, wenn darunter eine «-»-Liste weitergeht: dann ist es ihr erster Punkt, VII.368., VII.397.)
            if not (nach is not None and ueberspringen is nach) and not _liste_folgt(zeilen, i):
                while treffer.rest is not None and len(treffer.rest.worte) > 1 \
                        and treffer.rest.worte[0].text in ("-", "–", "—") and not _zahl_nach_strich(treffer.rest):
                    treffer.rest = treffer.rest.ab(1)  # (auch doppelt: «5.2.4.3. - - Die Hebamme …»)
            if treffer.eltern and treffer.eltern[0] not in gesehen:  # «II) A) …»: die Gruppe II. selbst anlegen
                vor_neuer_einheit()
                gruppe = Vorkommen(treffer.eltern[0], pfad_text(treffer.eltern[0]), treffer.eltern[1], z.seite, [],
                                   fett=treffer.fett, typ="roem", x0=z.x0)
                gruppe.hinweise.append(f"Gruppe {pfad_text(treffer.eltern[0])} hat im Findmittel keinen eigenen Titel "
                                       "(nur Doppelmarke wie «II) A)») – Titel ergänzen.")
                neue_einheit(gruppe)
                vorkommen.append(gruppe)
                gesehen.add(treffer.eltern[0])
                erste_x0.setdefault(treffer.eltern[0], z.x0)
            gesehen.add(treffer.pfad)
            erste_x0.setdefault(treffer.pfad, z.x0)
            vor_neuer_einheit()
            vorige = aktuell
            # neue Signatur, nach der nur die Schachtel steht, Titel auf der nächsten Zeile: «V.J.W. c.12.:1. ¦ Schachtel 1»
            # / «Akten ¦ 1893-1896» / «Schachtel 2» / «Akten ¦ 1897-1900» … (V.J.W.c.12.) – Schachtel 1, Titel «Akten»
            # (nicht, wenn gleich die nächste Signatur folgt: «VI.HO.B.1.:1 Schachtel 1» / «VI.HO.B.1.:2 Schachtel 2»)
            # (und nicht, wenn die nächste Zeile eine Bemerkung ist: «Mit Inventarium über das Gemeindegut 1889», VI.HO.,
            # «Soweit datierbar, handelt es sich um …», «Provenienz dieser Zeichnungen: …», VII.159.)
            nur_box = s is not None and not wiederholt and not z.schachtel and not resttext[s.end():].strip() \
                and nach is not None and nach.worte and not SCHACHTEL_RE.match(nach.text.strip()) \
                and len(nach.worte) <= 10 and not nach.text.rstrip().endswith(".") and nach.x0 < 380 \
                and re.search(r"[A-Za-zÄÖÜäöü]{3,}", nach.text) is not None \
                and not re.match(r"(?:Mit|Ohne|Soweit|Provenienz|Enthält|Darin|Inkl|Bemerkung|Hinweis|Siehe|Vgl)\b",
                                 nach.text.strip()) \
                and lies_signatur(nach, gl.kopie()) is None and nach.x0 >= z.x0 + 15 \
                and re.fullmatch(r"\d{1,4}[a-z]?", s.group(1)) is not None
            aktuell = Vorkommen(treffer.pfad, treffer.anzeige, treffer.roh, z.seite,
                                [treffer.rest] if treffer.rest and not nur_box else [], fett=treffer.fett, typ=typ,
                                schachtel=(s.group(1) if nur_box else z.schachtel) or None, datum=z.datum,
                                umfang=[z.umfang] if z.umfang else [], ist_teil=wiederholt, x0=z.x0)
            # Signatur allein, vertikal mittig neben einem zweizeiligen Titel: dessen erste Zeile steht knapp vor
            # der Signaturzeile und überlappt sie («Glasscheibe …» / «16.2.» / «(Wappenscheibe; …)», VII.371.)
            if not treffer.rest and vor is not None and vorige is not None and len(vorige.zeilen) >= 2 \
                    and vorige.zeilen[-1] is vor and vor.seite == z.seite and vor.bottom > z.top + 2 \
                    and vor.x0 > z.x0 + 15 and not vor.datum:
                vorige.zeilen.pop()
                aktuell.zeilen.append(vor)
                aktuell.titel_neben = bool(z.datum)
                for vb in reversed(verbleib):
                    if vb.zeile is vor:
                        vb.vorkommen = aktuell
                        break
            # Eintrag einer weiteren Spalte knapp über der Signaturzeile (eigene Zeile im PDF): «I - LXV» (x 266, 3 pt
            # höher) / «1 Kleine Stadt ¦ W 22 : 1» / «44 rot - 87 rot» (Spalte Assekuranznummern, VII.330.) – gehört zur
            # neuen Einheit, nicht zur vorigen bzw. in den Vorspann
            elif treffer.rest is not None and vor is not None and vor.seite == z.seite and vor.bottom > z.top + 2 \
                    and vor.x0 > z.x0 + 15 and not vor.datum and len(vor.worte) <= 6 \
                    and not any(w.x0 < vor.x1 and w.x1 > vor.x0 for w in z.worte) \
                    and (vorige is None or vorige.zeilen and vorige.zeilen[-1] is vor):
                if vorige is not None:
                    vorige.zeilen.pop()
                aktuell.zeilen.append(vor)
                for vb in reversed(verbleib):
                    if vb.zeile is vor:
                        vb.art, vb.vorkommen = "einheit", aktuell
                        break
            neue_einheit(aktuell)
            if len(kopf_darin) > 1:
                # Bereichskopf mit Beschreibung: hinter den Titel der ersten Einheit (VII.400.)
                for x_k in kopf_darin[1:]:
                    aktuell.zeilen.append(x_k)
                    merke(x_k, "einheit", aktuell)
                aktuell.hinweise.append(f"Steht im Findmittel unter dem Bereichskopf «{kopf_darin[0].text.strip()}»; dessen "
                                        "Beschreibung hier im Darin übernommen.")
                if zwischentitel and zwischentitel == kopf_darin[0].text.strip():
                    zwischentitel = ""
            kopf_darin = []
            # Beschreibung unter einer Gruppenzeile ohne Signatur – ein Satz «Vgl. die vollständige Serie …» oder in
            # Klammern «(Die Bände enthalten Notizen vorwiegend zum Rechnungswesen, …)» (VII.24.): ins Darin jeder
            # Einheit der Gruppe (Konvention NP12, K162); die Gruppenzeile selbst bleibt Hinweis
            # (so viele Einheiten, wie die Gruppenzeile nennt: «Buchhaltungsabschlüsse (29 Hefte)» 4.2.22.–4.2.50.,
            # «Notizen (2 Bände)» 4.2.51.–4.2.52.; ohne Anzahl nur die erste, IV.A.45.)
            if gruppe_darin is not None and not zwischentitel and not aktuell.ist_teil:
                if aktuell.pfad[:-1] == gruppe_darin[1] and len(aktuell.pfad) == gruppe_darin[2] and gruppe_darin[3] > 0:
                    gruppen_nachtrag.append((aktuell, gruppe_darin[0]))
                    gruppe_darin = gruppe_darin[:3] + (gruppe_darin[3] - 1,)
                elif len(aktuell.pfad) <= gruppe_darin[2] or aktuell.pfad[:len(gruppe_darin[1])] != gruppe_darin[1]:
                    gruppe_darin = None
            if zwischentitel:
                aktuell.hinweise.append(f"Steht im Findmittel unter der Zwischenüberschrift «{zwischentitel}».")
                zwischentitel_alt, zwischentitel = zwischentitel, ""
                beschreibung: list[Zeile] = []
                for x_b in zt_zeilen:
                    t_b = x_b.text.strip()
                    if not beschreibung and not (re.match(r"(?:Vgl\.|vgl\.)\s*\S", t_b)
                                                 or t_b.startswith("(") and len(t_b.split()) >= 5):
                        continue  # (nicht die Umfangsangabe «(2 Bände)» der Gruppenzeile)
                    beschreibung.append(x_b)
                    if re.search(r"(?:[a-zäöüß]{2,}|\d{2,}|[)“”»\]])[.!?]?\)?$", t_b) and re.search(r"[.!?)]$", t_b):
                        break
                m_anz = re.search(r"\((\d{1,3})\s+(?:Bände|Bändchen|Hefte|Mappen|Schachteln|Ordner|Dossiers)\b", zwischentitel_alt)
                gruppe_darin = (beschreibung, aktuell.pfad[:-1], len(aktuell.pfad),
                                int(m_anz.group(1)) - 1 if m_anz else 0) if beschreibung and not aktuell.ist_teil else None
                if gruppe_darin is not None:
                    gruppen_nachtrag.append((aktuell, beschreibung))
            zt_zeilen = []
            if z.schachtel and not box["marke"] and spalte_fortfuehren:  # nur bei der ersten Einheit angegeben
                box.update(nr=z.schachtel, abschnitt=bereich(aktuell))
            if not aktuell.schachtel:
                aktuell.schachtel = box_fuer(aktuell)
                aktuell.schachtel_geerbt = aktuell.schachtel is not None
            if treffer.hinweis:
                aktuell.hinweise.append(treffer.hinweis)
            vorkommen.append(aktuell)
            merke(z, "einheit", aktuell)
            continue
        text = z.text.strip()
        # Notiz zu den folgenden Nummern ohne Signatur: «Mappe 6:» / «Bei den Nummern 28.4.25. – 29. handelt es sich um
        # Pläne von Karl Knell und Otto Dürr. …» oben auf S. 16 vor «28.4.25.» (VII.12.B.) – ins Darin von 28.4.25.,
        # nicht der Einheit davor
        m_bei = re.match(r"(?:Bei|Zu|Für) den Nummern\s+(\d{1,3}(?:\.\d{1,4})+)\.?", text) \
            if not kopfblock and aktuell is not None and probe is None else None
        if m_bei and any((t_b := lies_signatur(x, gl.kopie())) is not None
                         and pfad_text(t_b.pfad).rstrip(".") == m_bei.group(1) for x in zeilen[i + 1:i + 25]):
            kopfblock, zwischentitel = True, ""
            kopf_darin = [z]
            if vor is not None and aktuell.zeilen and aktuell.zeilen[-1] is vor \
                    and re.fullmatch(r"(?:Mappe|Schachtel|Karton)\s+\d{1,3}[a-z]?\s*:?", vor.text.strip()):
                aktuell.zeilen.pop()  # «Mappe 6:» gehört zum Folgenden (als Zwischenüberschrift)
                for vb in reversed(verbleib):
                    if vb.zeile is vor:
                        vb.art, vb.vorkommen = "ueberschrift", None
                        break
                zwischentitel = vor.text.strip().rstrip(":")
            kopf_darin.append(z)
            continue
        if kopfblock and aktuell is not None:
            if kopf_darin:  # Beschreibung unter dem Bereichskopf: ins Darin der ersten Einheit des Bereichs
                kopf_darin.append(z)
                continue
            merke(z, "ueberschrift")
            zwischentitel = f"{zwischentitel} / {text}"
            zt_zeilen.append(z)
            continue
        # Übersicht mitten im Verzeichnis: «7. Diapositive und Photonegative …» / «Übersicht bzw. Aufteilung:» /
        # «7.1. …», «7.1.1.-7.1.4. 4 Holzkassetten» … / «7. Diapositive und Photonegative» (VII.277.): alles bis zur
        # Wiederholung der Abschnittssignatur gehört ins Darin des Abschnitts, die Unternummern kommen danach
        # (nur Dezimalverzeichnisse: bei Vollsignaturen ist die Übersichtszeile «VI.SB.D.1.:1 Schachtel 1: a-d» der
        # Titel der Gruppe, die Einträge a)–d) folgen als Teile, VI.SB.)
        if aktuell is not None and re.match(r"Übersicht\b", text) and len(text) <= 60 and not aktuell.ist_teil \
                and gl.modus == "dezimal" and aktuell.typ != "voll":
            in_uebersicht: set[tuple] = set()  # («4. Verschiedenes» / «Übersicht» / «4.1.» … «4.6.» / «4.1. Heraldik»)
            for j in range(i + 1, min(len(zeilen), i + 200)):
                t = lies_signatur(zeilen[j], gl.kopie())
                if t is None:
                    continue
                if t.pfad == aktuell.pfad or t.pfad in in_uebersicht:
                    uebersicht_bis, uebersicht_kopf = j, t.pfad == aktuell.pfad
                    break
                if t.pfad[:len(aktuell.pfad)] != aktuell.pfad or len(t.pfad) <= len(aktuell.pfad):
                    break  # anderer Abschnitt: keine Übersicht dieses Abschnitts
                in_uebersicht.add(t.pfad)
            if uebersicht_bis is not None and not uebersicht_kopf and len(in_uebersicht) < 2:
                uebersicht_bis = None  # eine einzelne Nummer ist noch keine Übersicht
            if uebersicht_bis is not None:
                aktuell.zeilen.append(z)
                merke(z, "einheit", aktuell)
                continue
        # «Stadtarchiv Zürich» als Eintrag einer Liste («Ständerat» / «Stadtarchiv Zürich» / «Stadtkanzlei», Briefliste
        # S. 20, VII.109.) ist kein Schlussvermerk
        stadtarchiv_eintrag = re.fullmatch(r"Stadtarchiv Zürich|STADTARCHIV ZÜRICH", text) is not None \
            and vor is not None and nach is not None and abs(vor.x0 - z.x0) <= 3 and abs(nach.x0 - z.x0) <= 3 \
            and z.seite < letzte_seite - 1 and not SCHLUSS_DATUM_RE.match(nach.text.strip())
        # (im Schlussblock auch eine zentrierte Überschrift in grösserer Schrift: «Verzeichnis der Diplome aus dem
        # Nachlass …» / «Bibliothek Nc» 14 pt vor der Nc-Liste, VII.75.)
        # im Schlussblock bzw. auf den letzten Zeilen ein Stück ohne Nummer: fett «Reproduktionen (Beilage):» mit den
        # Stücken darunter (VII.336.), «Drei Archivschachteln enthalten Drucksachen des Heizamtes ab 1945.» (V.G.b.903.)
        # – zur Zeile für den Bestand, nicht ins Blatt Info
        if probe is None and aktuell is not None and aktuell.typ != "bestand" and z.worte \
                and z.x0 <= SIGNATUR_SPALTE_MAX and (
                    (im_schluss or luft(vor, z) > 20) and all("Bold" in w.font for w in z.worte)
                    and STUECK_KOPF_RE.match(text)
                    or STUECK_SATZ_RE.match(text) and (im_schluss or i > len(zeilen) - 15)) \
                and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
            im_schluss = False
            stueck_ohne_nummer(z)
        if (ist_schlussvermerk(text, vor, z) and not stadtarchiv_eintrag) \
                or (im_schluss and (z.x0 <= SIGNATUR_SPALTE_MAX or z.worte[0].size >= 13.5)):
            info.setdefault("schluss", []).append(schlusszeile(z, text))
            merke(z, "schluss")
            im_schluss = True
            # «Der Bestand umfasst:» mit den eingerückten Umfangszeilen «108 Normschachteln 10,80 lfm» … und den
            # Bearbeitungsvermerken darunter (VII.237., VII.151., VII.376.): alles ins Blatt Info
            if re.match(r"(?:Der (?:Archiv)?[Bb]estand|Dieser Bestand) umfasst\b.{0,40}:$", text) \
                    and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i + 1:]):
                im_anhang = True
            continue
        # Schlussblock nach der letzten Einheit, der in der Signaturspalte beginnt, während der Text der Einheit
        # eingerückt ist: «Beilagen:» / «1 Rapport des Polizeiinspektorates …» (VII.65.), «Zu diesem Bestand vgl.
        # auch: „Schenkungsurkunde …“» (VII.37.) – nach einem Absatz auf den letzten Zeilen und ohne weitere
        # Signatur danach: Schlussvermerk, nicht Darin der letzten Einheit
        #   (nur wenn er wie eine Notiz zum Bestand beginnt – nicht die Beschreibung der letzten Einheit «Messingpokal,
        #   versilbert, mit Deckel» (VII.10.), «Nc 4-6 mit Beilage in grüner … Mappe» (V.C.b.368.) oder eine Liste)
        # (auch links von einer Unternummer in der Titelspalte: «7.4 Korrespondenz …» bei x 184 / «Vgl. auch V.J. b.202.
        # Jahresrechnungen der Heime:» bei x 71, V.J.W.c.15.)
        if aktuell is not None and aktuell.x0 and vor is not None \
                and (abs(z.x0 - aktuell.x0) <= 3 or z.x0 <= SIGNATUR_SPALTE_MAX and z.x0 + 30 < aktuell.x0) \
                and aktuell.zeilen and (aktuell.zeilen[0].x0 > aktuell.x0 + 15 or links_vom_darin(z, aktuell)) \
                and luft(vor, z) > 25 and not ist_aufzaehlung(z) and SCHLUSSNOTIZ_RE.search(text) \
                and (z.seite == zeilen[-1].seite or i > len(zeilen) - 15 or z.seite >= letzte_seite - 1) \
                and not any(lies_signatur(x, gl.kopie()) is not None for x in zeilen[i:]):
            info.setdefault("schluss", []).append(schlusszeile(z, text))
            merke(z, "schluss")
            im_schluss = True
            continue
        # (auch mit Bemerkung in Klammern: «Schachteln 7 bis 12 (Aufteilung formatbedingt, vgl. die Aufstellung am
        # Schluss.)» vor «10. Bilder und Skulpturen», VII.118. – die Bemerkung als Hinweis bei der folgenden Einheit)
        m_kb = re.match(r"^((?:Schachtel|Schachteln)\s+\d+[a-z]?(?:\s*(?:[–-]|\+|,|und|bis)\s*\d+[a-z]?)*)\s*"
                        r"(\([^()]{3,120}\))\.?\s*$", text)
        if m_kb and folgt_signatur(nach):
            merke(z, "ueberschrift")
            zwischentitel = text
            continue
        s = SCHACHTEL_RE.match(text) or re.match(r"^\d{1,4}\s+Schachtel\s+(\d+[a-z]?)\s*$", text)
        # auch «2 ¦ Schachtel 14» mit abgetrennter Spalte (2. Schachtel der Gruppe, VII.179.)
        nr_box = s.group(1) if s else z.schachtel if z.schachtel and re.fullmatch(r"\d{1,3}", text) else None
        if nr_box:  # «Schachtel 3», «9 Schachtel 19» – gilt für das Folgende
            marke_setzen(z, nr_box, None)
            continue
        # Zuordnungsliste «Schachtel 2: 4.1.2. – 4.1.5.» (VII.12.A.): gilt am Ende für diese Signaturen
        m = ZUORDNUNG_RE.fullmatch(text)
        if m:
            zuordnung.append((m.group(1), tuple(m.group(2).split(".")),
                              tuple(m.group(3).split(".")) if m.group(3) else None, merke(z, "schachtel", None, None,
                                                                                          m.group(1))))
            continue
        m = re.match(r"(?:Schachtel|Schachteln)\s+(\d{1,4}[a-z]?)\s*:\s*(?=\S)", text)
        if m and aktuell is not None:  # «Schachtel 201: Ski-Kurse ¦ 1957-1970»: Schachtel mit eigenem Titel
            n_worte, laenge = 0, 0
            while n_worte < len(z.worte) and laenge < m.end() - 1:
                laenge += len(z.worte[n_worte].text) + 1
                n_worte += 1
            rest = z.ab(n_worte)
            if rest is not None:
                marke_setzen(z, m.group(1), None)
                inhalt_beginnt(rest)
                aktuell.zeilen.append(rest)
                merke(rest, "einheit", aktuell)
                continue
        if box["marke"] and box["marke"][1] is None and box["datum"] and z.x0 >= 300 and ist_reiner_zeitausdruck(text):
            box["datum"] = f"{box['datum']} / {text}"  # 2. Zeile der Datumsspalte («Schachtel 1 ¦ 1952–1969» / «1978–1980»)
            box["extra"].append(merke(z, "einheit"))
            continue
        if aktuell is not None and box["nr"] and AUFBEWAHRUNG_RE.match(text):
            box.update(nr=None, abschnitt=None)  # «Mappe»: was folgt, liegt nicht mehr in der Schachtel
        if aktuell is None:
            merke(z, "vorlauf")
            continue  # Überschrift «DETAILVERZEICHNIS», Tabellenkopf u. Ä.
        # Spaltenköpfe am rechten Rand hinter Text: «Doppelgrösse ¦ Jahre ¦ Schachtel» (VII.191.) – nur «Jahre
        # Schachtel» ist Tabellenkopf, «Doppelgrösse» gehört ins Darin
        n_kopf = 0
        while n_kopf < len(z.worte) and z.worte[-1 - n_kopf].text.strip(".,:;/()").lower() in KOPFWORTE:
            n_kopf += 1
        if 2 <= n_kopf < len(z.worte) and len(z.worte) - n_kopf <= 3 and z.worte[-n_kopf].x0 >= 400 \
                and z.worte[-n_kopf].x0 - z.worte[-n_kopf - 1].x1 >= SPALTEN_LUECKE:
            merke(Zeile(z.seite, z.top, z.bottom, z.worte[-n_kopf:]), "ueberschrift")
            z = Zeile(z.seite, z.top, z.bottom, z.worte[:-n_kopf], z.datum, z.umfang, z.schachtel, z.spalten)
            text = z.text.strip()
        # (nicht ein Name in Grossbuchstaben mitten in einer Liste: «Rote Hilfe Schweiz» / «SATUS» / «Schaffhausen,
        # Stadt», gleiche Spalte, kein Absatz, VII.109.)
        in_liste = vor is not None and nach is not None and abs(vor.x0 - z.x0) <= 2 and abs(nach.x0 - z.x0) <= 2 \
            and luft(z, nach) <= ABSATZ_ABSTAND and len(z.worte) <= 2 and z.x0 > SIGNATUR_SPALTE_MAX - 30 \
            and lies_signatur(nach, gl.kopie()) is None  # (vor «SATUS» die Lücke zwischen R und S)
        if TABELLENKOPF_RE.match(text) or ist_tabellenkopf(text) or not in_liste and GROSSWORT_RE.match(text.split(" ")[-1]) and len(text) < 40 \
                and text.isupper() and not z.datum and not re.match(r"\d{1,3}\.\s", text) \
                or (re.fullmatch(r"[A-ZÄÖÜ][A-ZÄÖÜ0-9/.,&\- ]{5,59}", text) and "/" in text and not z.datum
                    and folgt_signatur(nach)):
            # (auch «VERBANDSTAETIGKEIT/MILITÄRDIENST/ETC.» nach «Schachtel 18» direkt vor «7. Pflanzwerk …», VII.190.)
            # (nicht «4. NSDAP ¦ 27. Jan. 1965» – Listeneintrag mit Datum, VII.103.)
            merke(z, "ueberschrift")
            if text.isupper() and not ist_verzeichniswort(text):
                zwischentitel = text  # «FAMILIÄRES», «VERBANDSTAETIGKEIT/MILITÄRDIENST/ETC.»
            continue
        # fette Zwischenüberschrift ohne Signatur direkt vor einer Einheit («Energie- und Verkehrsfragen, Radio,
        # Fernsehen», VII.109.): nicht ins Darin der vorigen Einheit, sondern als Hinweis zur folgenden
        # (auch in grösserer Schrift: «Stadtschreiber» / «10. Dr. Willy Bosshard», V.L.136.b.)
        # (nicht die letzte Zeile einer nummerierten Liste, die eben als Listenpunkt verworfen wurde: «10 Enthüllung
        # des Denkmals ¦ 26 - 32» / «11 Denkschrift ¦ 33, 34, 35» fett vor «4. Drucksachen», VII.11.)
        listenzeile = bool(gl.listen_nr and aktuell is not None and z.worte
                           and re.fullmatch(r"\d{1,3}\.?", z.worte[0].text)
                           and gl.listen_nr[0] == int(z.worte[0].text.rstrip(".")) and gl.listen_nr[2] == z.seite
                           and abs(gl.listen_nr[1] - z.worte[0].x0) <= 3
                           and any(x.worte and x.worte[0].text.rstrip(".") == str(gl.listen_nr[0] - 1)
                                   and abs(x.worte[0].x0 - z.worte[0].x0) <= 3 for x in aktuell.zeilen[-40:]))
        # fetter Vermerk zu den folgenden Nummern direkt unter einer Einheit: «V.B.3.:56. ‒ 65. sind nicht vorhanden. Die
        # nachfolgende Auflistung richtet sich nach dem zeitgenössischen Verzeichnis.» (V.B.c.3.) – Hinweis bei der
        # folgenden Einheit, nicht Teil des Titels von 55.
        if aktuell is not None and z.worte and all("Bold" in w.font for w in z.worte) \
                and not all("Bold" in w.font for w in (aktuell.zeilen[0].worte if aktuell.zeilen else [])) \
                and re.search(r"\bsind\s+nicht\s+(?:mehr\s+)?vorhanden\b", text) and len(z.worte) >= 4:
            block_v, j_v = [z], i + 1
            while j_v < len(zeilen) and j_v <= i + 3 and not folgt_signatur(zeilen[j_v]) \
                    and all("Bold" in w.font for w in zeilen[j_v].worte):
                block_v.append(zeilen[j_v])
                j_v += 1
            if j_v < len(zeilen) and folgt_signatur(zeilen[j_v]):
                for x in block_v:
                    merke(x, "ueberschrift")
                ueberspringen_bis = j_v
                zwischentitel = " ".join(x.text.strip() for x in block_v)
                continue
        # Titelblock einer weiteren Serie oben auf einer Seite: «Stadtarchiv Zürich V.G. c.50., 2. Serie» (14 pt) /
        # «Akten und Pläne des Bauwesens II …» (20 pt) / «1930 – 1936» / «(Detailverzeichnis)» (V.G.c.50.) – Überschrift
        # für das Folgende, nicht Darin der letzten Einheit davor
        if aktuell is not None and z.worte and z.seite > zeilen[0].seite and z.worte[0].size >= 13.5 \
                and re.match(r"Stadtarchiv Zürich\s+[IVX]{1,4}\.", text):
            serienkopf = True
        # ebenso ein Titelblatt in grosser Schrift oben auf einer Seite vor dem zweiten Nachlass: «Frau Myrthe
        # Wedekind-Güttinger (1906 – 1990)» (20 pt) / «Nachlass» / «Mitglied des Dramatischen Vereins Zürich» (16 pt)
        # vor «2. Myrthe Wedekind-Güttinger» (VII.232.)
        if aktuell is not None and probe is None and z.worte and z.seite > zeilen[0].seite \
                and (vor is None or vor.seite != z.seite) and z.worte[0].size >= grund_groesse + 6:
            serienkopf = True
            # (die Zeilen zählen weiter für den rechten Rand der Textspalte wie früher im Darin der letzten Einheit)
            if any(x.datum or x.umfang for x in aktuell.zeilen):
                k_t = i
                while k_t < len(zeilen) and zeilen[k_t].worte and lies_signatur(zeilen[k_t], gl.kopie()) is None \
                        and max(w.size for w in zeilen[k_t].worte) >= grund_groesse + 2:
                    info.setdefault("rand_zusatz", []).append(zeilen[k_t])
                    k_t += 1
        if serienkopf and probe is None \
                and (max(w.size for w in z.worte) >= grund_groesse + 2 or DETAIL_RE.fullmatch(text.strip("() "))
                     or text.startswith("Stadtarchiv Zürich")):
            merke(z, "ueberschrift")
            zwischentitel = f"{zwischentitel} / {text}" if zwischentitel else text
            continue
        serienkopf = False
        # Überschrift mit Folgezeilen vor der nächsten Signatur: fett «V.B.3.:56. ‒ 65. sind nicht vorhanden. Die
        # nachfolgende Auflistung …» / «zeitgenössischen Verzeichnis.» vor «V.B.c.3.:56.» (V.B.c.3.); kursiv «Porträts
        # von August Benziger (1857 – 1955):» / «Fotografien der gerahmten Porträts von» / «– Alfred …» / «– Anna …» vor
        # «1.14.» (VII.455.); fett «Gemeindegutsrechnungen, Rechnungsbeilagen» / «(Es wurden die Jahrgänge 1893–1900
        # behalten, …)» vor «IV.A.45.» (IV.A.) – Hinweis bei der folgenden Einheit, Erläuterung in Klammern in ihr Darin;
        # nicht, wenn die Zeilen davor in derselben Schrift eine Liste bilden («Die Rebellen …» / «Das Armband …» fett
        # vor «2.8.», VII.228.)
        def schrift(x: Zeile) -> str:
            return "fett" if all("Bold" in w.font for w in x.worte) else "kursiv" if all(
                "Italic" in w.font or "Kursiv" in w.font or "Oblique" in w.font for w in x.worte) else ""
        if aktuell is not None and probe is None and not listenzeile and z.worte and schrift(z) \
                and luft(vor, z) > ABSATZ_ABSTAND and not ist_aufzaehlung(z) and not SCHACHTEL_RE.match(text) \
                and not ist_tabellenkopf(text) and not TABELLENKOPF_RE.match(text) \
                and not (not text.endswith(":") and any(
                    x.worte and schrift(x) == schrift(z) and abs(x.x0 - z.x0) <= 3 for x in aktuell.zeilen[1:][-4:])) \
                and (z.x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG or text.endswith(":")):
            block_k, j_k = [], i + 1
            while j_k < len(zeilen) and j_k <= i + 4 and not folgt_signatur(zeilen[j_k]):
                block_k.append(zeilen[j_k])
                j_k += 1
            schrift_gleich = all(schrift(x) == schrift(z) for x in block_k)
            klammer = bool(block_k) and block_k[0].text.strip().startswith("(") \
                and block_k[-1].text.strip().rstrip(".").endswith(")")
            # (mit Doppelpunkt nur eine kurze Überschrift, kein Satz: nicht «Aufführungsplakate … wurden unter Sign.:» /
            # «VII.12.B. … archiviert!» unter «13. Plakate», VII.200.)
            doppelpunkt_kopf = text.endswith(":") and not re.search(r"\.\s*:$", text) and len(z.worte) <= 10 \
                and not (block_k and re.search(r"[.!?]$", block_k[-1].text.strip()))
            # (nicht mit einer Schachtelangabe im Block: «Der Bestand enthält auch …» / «Blätter.» / «Schachtel 4:»,
            # V.B.b.46.; nicht zwischen dem Titel der Einheit und ihrer ersten Unternummer: «Porträts der Zürcher
            # Bürgermeister …» / «(6.1.1.-6.1.5.)» nach «6.1. Escher vom Glas …» bleibt ihr Darin, VII.277.)
            if 1 <= len(block_k) <= 3 and j_k < len(zeilen) and folgt_signatur(zeilen[j_k]) \
                    and not any(SCHACHTEL_RE.match(x.text.strip()) or BEHAELTER_RE.match(x.text.strip()) for x in block_k) \
                    and not erstes_kind(lies_signatur(zeilen[j_k], gl.kopie()), aktuell) \
                    and (schrift_gleich or klammer) and (schrift(z) == "fett" or doppelpunkt_kopf):
                merke(z, "ueberschrift")
                kopf_t = [z.text.strip()]
                for x in block_k:  # (auch die Erläuterung in Klammern: als Hinweis bei der folgenden Einheit)
                    merke(x, "ueberschrift")
                    kopf_t.append(x.text.strip())
                ueberspringen_bis = j_k
                zwischentitel = " ".join(kopf_t)
                zt_zeilen = list(block_k)
                continue
        # kurze Gruppenüberschrift in Textschrift in der Signaturspalte direkt vor der nächsten Signatur derselben Spalte,
        # während der Inhalt der Einheit davor eingerückt ist: «Diverses» vor «64 Urkunde …» (VII.109.; die übrigen
        # Gruppenüberschriften sind fett)
        if aktuell is not None and probe is None and z.worte and 1 <= len(z.worte) <= 3 \
                and not re.search(r"[\d:]", text) and text[:1].isupper() and nach is not None and nach.worte \
                and abs(nach.x0 - z.x0) <= 3 and folgt_signatur(nach) and luft(vor, z) > ABSATZ_ABSTAND \
                and aktuell.x0 and abs(z.x0 - aktuell.x0) <= 3 and not (z.schachtel or z.datum or z.umfang) \
                and any(x.worte for x in aktuell.zeilen[1:]) \
                and all(x.x0 > z.x0 + 15 for x in aktuell.zeilen[1:] if x.worte) \
                and text.lower().strip(".") not in KOPFWORTE \
                and not re.fullmatch(r"(?:Übersicht|Inhalt|Inhaltsübersicht|Verzeichnis|Detailverzeichnis|Register)\s*:?",
                                     text):
            merke(z, "ueberschrift")
            zwischentitel = text
            continue
        # kursive Gruppen- oder Ortsüberschrift in der Textspalte direkt vor der nächsten Signatur, nach einem Abstand:
        # «Zug» / «1.7. Karl Kaiser, Rede …» (VII.510.), «Lose Protokolle» / «2.1.8. Lose Protokolle der Vorstands-
        # sitzung …» (VII.376.), «Lose Kassarapporte / Vorstellungsrapporte» vor den losen Teilen (VII.12.B.); ebenso
        # eine fett nummerierte Gliederungsüberschrift in der Textspalte «2. Werke anderer Autoren» vor «3 Binder,
        # Walter. …» wie «1. Werke von Werner Morf» (VII.359.) – Hinweis bei der folgenden Einheit, nicht Darin davor
        vt_k = vor.text.rstrip() if vor is not None and vor.worte else ""
        if aktuell is not None and probe is None and z.worte and nach is not None and nach.worte and vt_k \
                and luft(vor, z) > ABSATZ_ABSTAND and len(z.worte) <= 6 and len(text) <= 60 \
                and not text.startswith("(") and not text.endswith((".", ";", ",")) \
                and not (vt_k[-1] in ",(/&+„«‚:;-–" or vt_k.split()[-1] in ANSCHLUSS_WOERTER
                         or vt_k.split()[-1].lower() in ANSCHLUSS_KLEIN) \
                and nach.x0 < z.x0 - 20 and lies_signatur(nach, gl.kopie()) is not None \
                and not erstes_kind(lies_signatur(nach, gl.kopie()), aktuell) \
                and (schrift(z) == "kursiv" and not re.search(r"\d", text) and kursiv_selten(z.x0)
                     and not any(x.worte and schrift(x) == "kursiv" for x in aktuell.zeilen[-5:])
                     or schrift(z) == "fett" and re.match(r"\d{1,2}\.\s+[A-ZÄÖÜ]", text) is not None
                     and any(re.match(r"\d{1,2}\.\s+[A-ZÄÖÜ]", x.text.strip()) and abs(x.x0 - z.x0) <= 3
                             and schrift(x) == "fett" for x in zeilen[max(0, i - 400):i])):
            merke(z, "ueberschrift")
            zwischentitel = text.rstrip(":").strip()
            continue
        def fett_k(x: Zeile) -> bool:
            """fett – oder fett bis zu einer Klammerbemerkung («Villa Sans-Souci» / «(1941; Drehbuch …)», VII.228.)"""
            vk = x.worte[:next((n for n, w in enumerate(x.worte) if w.text.startswith("(")), len(x.worte))]
            return bool(vk) and all("Bold" in w.font for w in vk) and (len(vk) == len(x.worte)
                                                                        or x.text.strip().endswith(")"))
        fette_liste = vor is not None and bool(vor.worte) and fett_k(vor) and fett_k(z) and abs(vor.x0 - z.x0) <= 3 \
            and aktuell is not None and vor in aktuell.zeilen[1:]
        # (fett bis zu einer Klammerbemerkung genügt: «Grossformate» fett / «(ausserhalb der Schachteln)», VII.47.)
        vor_klammer = [w for w in z.worte[:next((n for n, w in enumerate(z.worte) if w.text.startswith("(")),
                                                 len(z.worte))]]
        fett_bis_klammer = bool(vor_klammer) and all("Bold" in w.font for w in vor_klammer) \
            and z.text.strip().endswith(")")
        if not listenzeile and not fette_liste and (all("Bold" in w.font for w in z.worte) or fett_bis_klammer
            or nach is not None and nach.worte
                and min(w.size for w in z.worte) >= max(grund_groesse, max(w.size for w in nach.worte)) + 1.5) \
                and len(text) <= 100 and (z.x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG
                                          # auch eine kurze fette Ortsüberschrift in der Textspalte: «Fluntern» /
                                          # «X.E. 18. Gemeindrath Fluntern» (X.E.); auch länger ohne Ziffern:
                                          # «Ledermesse Zürich, Stempel für die Lederballen» (X.E.)
                                          or (len(z.worte) <= 3 and len(text) <= 40
                                              or len(z.worte) <= 8 and len(text) <= 60 and not re.search(r"\d", text)
                                              and (all("Bold" in w.font for w in z.worte) or fett_bis_klammer))
                                          and nach is not None
                                          and (nach.x0 < z.x0 - 20 or abs(nach.x0 - z.x0) <= 3)
                                          and not text.startswith("(")
                                          and text.strip(".:").lower() not in KOPFWORTE) \
                and luft(vor, z) > ABSATZ_ABSTAND and nach is not None and not ist_aufzaehlung(z) \
                and not SCHACHTEL_RE.match(text) and lies_signatur(nach, gl.kopie()) is not None \
                and not (gl.buchstaben and _ist_buchstabenabschnitt(nach)) \
                and not re.fullmatch(r"\(.*\)\W*", text):  # (Vermerk «(Enthält Patientendaten!)» zur Einheit davor, VII.423.)
            # (nicht vor einer Abschnittsüberschrift «08 FOTOGRAPHIEN …»: dann gehört die Zeile zum Eintrag davor,
            # «alle Negative vom obigen Katalog Firmengeschichte», VII.174.)
            merke(z, "ueberschrift")
            zwischentitel = text
            continue
        # ebenso eine kurze Zeile mit Doppelpunkt als eigener Absatz direkt vor der nächsten Signatur («Russland:» /
        # «13.6. General-Karte …», VII.494.; «Intérieurs (Salon, Musikzimmer, Zimmer der Tochter):» / «1.8. …»,
        # VII.455.): Hinweis bei der folgenden Einheit statt Darin der vorigen
        if text.endswith(":") and (len(z.worte) <= 8 or len(z.worte) <= 14 and all(
                "Italic" in w.font or "Bold" in w.font for w in z.worte)) and not (z.datum or z.schachtel or z.umfang) \
                and aktuell is not None and nach is not None and luft(vor, z) > 4 and not ist_aufzaehlung(z) \
                and not re.match(r"(?:Darin|Inhalt|Enthält|Beschriftung|Bemerkung|Anmerkung|Vgl\.|Siehe)", text, re.I) \
                and not re.search(r"\b(?:enthält|enthalten|enthaltend|folgende[nr]?|wie folgt|umfasst|bestehend)\b", text) \
                and folgt_signatur(nach) \
                and not (gl.buchstaben and _ist_buchstabenabschnitt(nach)) \
                and not (abs(nach.x0 - z.x0) <= 2 and sum(1 for x in aktuell.zeilen if abs(x.x0 - z.x0) <= 2) >= 10):
            # (nicht mitten in einer langen Liste derselben Einrückung: «Musikanten:» / «1. Eduard …» ist dort eine
            # Kurzliste im Inhalt, siehe inhaltsliste, VII.191.)
            merke(z, "ueberschrift")
            zwischentitel = text.rstrip(":").strip()
            continue
        # Gruppenüberschrift mit Bandzahl als eigener Absatz vor den Einheiten der Gruppe: «Kassenbelege (2 Bände)» /
        # «4.2.6. Bd. 1: 1873» / «4.2.7. Bd. 2: 1874», auch zweizeilig «Zahlungen an Unternehmer … / (2 Bände)» oder mit
        # Erläuterung «Notizen (2 Bände) (Die Bände enthalten …)» (VII.24.) – Hinweis bei der folgenden Einheit statt
        # Darin der vorigen
        bandzeile = re.search(r"\(\d{1,2}\s+(?:Bände|Bändchen|Hefte)\b[^)]*\)\s*$", z.text) is not None
        if aktuell is not None and z.x0 > SIGNATUR_SPALTE_MAX and vor is not None \
                and (luft(vor, z) > ABSATZ_ABSTAND
                     # (auch direkt unter einer abgeschlossenen Klammerzeile: «[Enthält u. a. Kapitalzinsen …]» /
                     # «Buchhaltungsjournal (2 Bände)» / «4.2.17. Bd. 1: …», VII.24.)
                     or bandzeile and vor.text.rstrip()[-1:] in ".)]»“" and nach is not None
                     and luft(z, nach) > ABSATZ_ABSTAND) \
                and not ist_aufzaehlung(z) and not (z.datum or z.schachtel or z.umfang):
            j = i
            while j + 1 < len(zeilen) and j - i < 4 and zeilen[j + 1].seite == z.seite \
                    and zeilen[j + 1].x0 > SIGNATUR_SPALTE_MAX and abs(zeilen[j + 1].x0 - z.x0) <= 15 \
                    and luft(zeilen[j], zeilen[j + 1]) <= ABSATZ_ABSTAND:
                j += 1
            block = " ".join(x.text.strip() for x in zeilen[i:j + 1])
            # (nicht die letzte Untergruppe im Inhalt mit ihren Bänden «Protokoll der Direktion (3 Bände)» / «Bd. 1 (26.
            # September 1872 bis …)» … vor «2.2.», VII.24.)
            if j + 1 < len(zeilen) and re.search(r"\(\d{1,2}\s+(?:Bände|Bändchen|Hefte)\b", block) \
                    and not any(re.match(r"(?:Bd\.|Band|Bände)\s*\d", x.text.strip()) for x in zeilen[i:j + 1]) \
                    and len(block) <= 300 and re.match(r"[A-ZÄÖÜ(]", block) \
                    and re.match(r"\S+\s+(?:(?:Bd\.|Band)\s*1\b|a[.)]\s)", zeilen[j + 1].text.strip()) \
                    and lies_signatur(zeilen[j + 1], gl.kopie()) is not None:
                # (nur vor dem ersten Glied der Gruppe «4.2.6. Bd. 1: 1873», «4.2.8. a. "Conto-Corrent …"» – nicht
                # «1937-1948 gebunden (6 Bände)» / «11.2. Publikationen», VII.150.)
                merke(z, "ueberschrift")
                zwischentitel = block
                zt_zeilen = list(zeilen[i + 1:j + 1])
                gruppenkopf_bis = j
                continue
        # Bearbeitungsvermerk am Ende eines Abschnitts mitten im Findmittel: «29. Juli 1999 / RD» nach den
        # Zeichnungsmappen (V.G.c.42.), «16. März 1992 / RD / 185B» (VII.48.) – ins Info-Blatt, nicht ins Darin der
        # letzten Einheit (sonst reicht deren geschätzter Zeitraum bis 1999)
        if z.x0 <= SIGNATUR_SPALTE_MAX and len(z.worte) <= 8 and i <= len(zeilen) - 15 \
                and VERMERK_DATUM_RE.match(text) and (vor is None or luft(vor, z) > ABSATZ_ABSTAND):
            info.setdefault("schluss", []).append(schlusszeile(z, text))
            merke(z, "schluss")
            continue
        # langer Text in der Signaturspalte nach grossem Abstand am Ende: Schlussbemerkung, kein Darin mehr;
        # ebenso «12. Juni 2007 / Dr. Robert Dünki» auf den letzten Zeilen
        if (z.x0 <= SIGNATUR_SPALTE_MAX and (abstand(vor, z) or 0) > 40 and len(text) > 60 and not ist_aufzaehlung(z)
                and (nach is None or lies_signatur(nach, gl.kopie()) is None)
                and (z.seite == zeilen[-1].seite or i > len(zeilen) - 15)) \
                or (i > len(zeilen) - 15 and (SCHLUSS_DATUM_RE.match(text) or SCHLUSS_ORT_DATUM_RE.match(text))):
            info.setdefault("schluss", []).append(schlusszeile(z, text))
            merke(z, "schluss")
            im_schluss = True
            continue
        # «Teil 1» bzw. «Bewerbungen mit Fotos 1987–1988, Teil 3» ohne Signatur = weiterer Teil
        luft_davor = luft(vor, z) > ABSATZ_ABSTAND
        luft_danach = luft(z, nach) > ABSATZ_ABSTAND
        teil_m = TEIL_NUR_RE.match(text) or (TEIL_ZEILE_RE.match(text) if luft_davor and luft_danach
                                              and len(text) <= 100 and not ist_aufzaehlung(z) else None)
        if teil_m and int(teil_m.groups()[-1]) < 100:  # nicht «Teil 1928» (Jahr, Titelzeile, VII.308.C.a.)
            nr = int((TEIL_NUR_RE.match(text) or TEIL_ZEILE_RE.match(text)).groups()[-1])
            vor_neuer_einheit()
            aktuell = Vorkommen(aktuell.pfad, aktuell.anzeige, aktuell.roh, z.seite, [z], teil_nr=nr,
                                datum=z.datum, typ=aktuell.typ, ist_teil=True)
            neue_einheit(aktuell)
            aktuell.schachtel = z.schachtel or aktuell.schachtel or box_fuer(aktuell)
            if z.umfang:
                aktuell.umfang.append(z.umfang)
            vorkommen.append(aktuell)
            merke(z, "einheit", aktuell)
            continue
        # Überschrift mit Schachtelangabe am rechten Rand: «Büchlein aus Reclam's Universal-Bibliothek: Nummer: ¦
        # Schachtel 6», «b) mit Schreibmaschine geschriebene Texte: ¦ Schachtel 8» (VII.175.), wo die übrigen Wechsel
        # «Schachtel 5» allein stehen – Schachtelwechsel, die Überschrift beginnt den neuen Teil
        # (nur wo die Schachtelwechsel der Datei Teile bilden, die laufende Einheit also selbst ein Schachtel-Teil ist –
        # nicht «Bauabrechnungen Q - Z: ¦ Schachtel 13» im Darin von 02.3.1.25., VII.174.)
        if aktuell is not None and probe is None and z.schachtel and re.fullmatch(r"\d{1,3}[a-z]?", z.schachtel) \
                and text.rstrip().endswith(":") and not box["marke"] and box["nr"] and z.schachtel != box["nr"] \
                and (aktuell.schachtel or "") != z.schachtel and aktuell.aus_marke:
            marke_setzen(z, z.schachtel, None)
        inhalt_beginnt(z)
        # Datums- oder Umfangsangabe allein auf einer Zeile («1916» rechtsbündig, «4 Bände»)
        if ist_reiner_zeitausdruck(text) and z.x0 >= 300 and len(aktuell.zeilen) >= 2 \
                and aktuell.zeilen[-1] is vor and vor.x1 >= z.x0 - 5 and not vor.datum:
            aktuell.zeilen.append(z)  # «Schluss-Akkord ¦ 12./ 19./ 26. Okt./» / «2. Nov. 1998»: Fortsetzung im Darin
            merke(z, "einheit", aktuell)
            continue
        # offene Spanne eines Inhaltseintrags, deren Ende allein in der Datumsspalte darunter steht: «33. Diverse
        # Begrüssungen von Sportlern ¦ 1939 –» / «¦ 1946» (Liste unter 3.17., VII.76.) – das Ende gehört zum Eintrag,
        # nicht zum Zeitraum der Einheit
        if ist_reiner_zeitausdruck(text) and z.x0 >= 300 and len(aktuell.zeilen) >= 2 and aktuell.zeilen[-1] is vor \
                and vor.datum and re.search(r"[-–]\s*$", vor.datum) and not re.search(r"[-–]", text):
            vor.datum = f"{vor.datum.rstrip()} {text}"
            merke(z, "einheit", aktuell)
            continue
        if ist_reiner_zeitausdruck(text) and z.x0 >= 300:
            if not aktuell.datum:
                aktuell.datum = text
            else:  # zweite Zeile der Datumsspalte («1893–1955» / «1961–1985»)
                aktuell.weitere_daten.append(text)
            merke(z, "einheit", aktuell)
            continue
        def umfang_mit_datum(x: Zeile | None) -> bool:
            return x is not None and bool(x.datum) and bool(UMFANG_RE.match(x.text.strip()))
        if umfang_mit_datum(z) and (umfang_mit_datum(vor) or umfang_mit_datum(nach)):
            aktuell.zeilen.append(z)  # «1 Buch ¦ 1918 - 1920» / «1 Heft ¦ 1920 - 1922»: einzelne Stücke im Darin
            merke(z, "einheit", aktuell)
            continue
        # Stückzahl eines Eintrags tief in einer langen Liste: «23.10.1988 27.11.1988 - 6 Plakate» / «3 Fotos»
        # (VII.411. 10.3.) – Inhalt, nicht Umfang der Einheit
        if UMFANG_RE.match(text) and len(aktuell.zeilen) >= 10 and vor is not None \
                and re.search(r"(?:^|\s)-\s+\d+\s+\S", vor.text):
            aktuell.zeilen.append(z)
            merke(z, "einheit", aktuell)
            continue
        if UMFANG_RE.match(text) or z.umfang and not text:
            aktuell.umfang.append(text if UMFANG_RE.match(text) else z.umfang)
            if z.datum:  # «69 Bände ¦ 1981»: das Datum gehört zur Einheit
                aktuell.weitere_daten.append(z.datum)
            merke(z, "einheit", aktuell)
            continue
        if z.umfang:
            aktuell.umfang.append(z.umfang)
        # Signatur versehentlich im Text («5.2.4.25.Aufführungen im Schauspielhaus:»)
        m = DEZIMAL_ANGEKLEBT_RE.match(z.worte[0].text) or DEZIMAL_RE.match(z.worte[0].text)
        if m and "." in m.group(1) and tuple(m.group(1).split(".")) == aktuell.pfad[-len(m.group(1).split(".")):] \
                and gl.modus == "dezimal" and tuple(m.group(1).split(".")) == aktuell.pfad:
            rest = z.ab(1)
            if DEZIMAL_ANGEKLEBT_RE.match(z.worte[0].text):
                w0 = z.worte[0]
                rest = Zeile(z.seite, z.top, z.bottom,
                             [Wort(m.group(2), w0.x0, w0.x1, w0.font, w0.size)] + (rest.worte if rest else []),
                             z.datum, z.umfang, z.schachtel)
            while rest is not None and len(rest.worte) > 1 and rest.worte[0].text in ("-", "–", "—") \
                    and not _zahl_nach_strich(rest) and not _liste_folgt(zeilen, i):
                rest = rest.ab(1)  # «5.2.4.3. - - Die Hebamme, Theaterstück …» (VII.200.): Strich nach der Signatur
            if aktuell.x0 and abs(z.x0 - aktuell.x0) <= 5 and rest and not aktuell.aus_marke:
                # in der Signaturspalte wie die Einheit selbst: ein weiterer Eintrag mit derselben Nummer
                # («1.2.5. 5. Generation …» / «1.2.5. 6. Generation …», VII.199.) – eigener Teil mit Hinweis
                vor_neuer_einheit()
                nur_zeit = ist_reiner_zeitausdruck(rest.text)  # «4.2. 1946 – 1960»: nächster Zeitabschnitt (VII.151.)
                aktuell = Vorkommen(aktuell.pfad, aktuell.anzeige, z.worte[0].text, z.seite,
                                    [] if nur_zeit else [rest], typ=aktuell.typ, ist_teil=True, x0=z.x0,
                                    datum=rest.text.strip() if nur_zeit else z.datum,
                                    schachtel=z.schachtel or None)
                if not nur_zeit:
                    aktuell.hinweise.append(f"Signatur {aktuell.anzeige} steht im Findmittel zweimal hintereinander "
                                            "– Tippfehler? Als weiterer Teil übernommen, bitte prüfen.")
                vorkommen.append(aktuell)
                merke(rest, "einheit", aktuell)
                continue
            aktuell.hinweise.append("Signatur stand zusätzlich im Text und wurde entfernt.")
            if rest:
                aktuell.zeilen.append(rest)
                merke(rest, "einheit", aktuell)
            continue
        # «–»-Eintrag genau am Signaturrand nach einem Unterpunkt, dessen Titel weiter rechts beginnt, und danach
        # keine Untersignatur dieses Punkts: gehört (samt Folgezeilen, bis zur nächsten Signatur) zum Abschnitt
        # darüber («2.2.7. Eduard Osenbrüggen …» / «– Iwan Tschudi’s Schweizerführer …» / «3. …»: zu 2.2.,
        # VII.494.); folgt «2.2.1.», ist der Punkt selbst ein Abschnitt («2.2. Reiseführer …» / «– H. Stüssi …»)
        if (umleitung is None or umleitung[0] is not aktuell) and len(aktuell.pfad) >= 2 and not aktuell.ist_teil \
                and not aktuell.aus_marke and vor is not None:
            eltern = None
            # Zwischenüberschrift mit Doppelpunkt nach einer Liste, die selbst so eingeleitet wurde («Acht
            # Aktenstücke enthaltend:» / «1.» … «8.» / «Weitere Handschriften:», VII.191. III) A)): das Folgende
            # gehört wieder zur Gruppe, nicht zum letzten Listenpunkt
            if aktuell.pfad[-1].isdigit() and text.endswith(":") and len(z.worte) <= 6 and not z.datum \
                    and not z.schachtel and luft(vor, z) > 4 and not folgt_signatur(nach) \
                    and aktuell.x0 and abs(z.x0 - aktuell.x0) <= 3:
                kandidat = next((v for v in reversed(vorkommen) if v.pfad == aktuell.pfad[:-1] and not v.ist_teil),
                                None)
                if kandidat is not None and kandidat.zeilen and kandidat.zeilen[-1].text.rstrip().endswith(":") \
                        and abs(kandidat.zeilen[-1].x0 - z.x0) <= 3:
                    eltern = kandidat
            # wieder auf der Höhe der Marke nach eingerücktem Inhalt: der Punkt ist zu Ende («d) Friedrich Leonhard
            # Salomon Schweizer …» / eingerückt «1 Büchlein …» / links «Carte de membre étranger de M.Francis
            # Schwyzer …», «Sämtliche Akten …»: gehören zu IV) A), VII.191.)
            elif gl.modus == "gliederung" and aktuell.x0 and len(aktuell.zeilen) >= 2 and aktuell.zeilen[-1] is vor \
                    and vor is not aktuell.zeilen[0] and vor.x0 >= aktuell.x0 + 4 and z.x0 <= aktuell.x0 + 1 \
                    and z.text[:1].isupper() and not re.search(r"[-,(/]$", vor.text.rstrip()) \
                    and not ist_aufzaehlung(z) \
                    and not (all("Bold" in x.font for x in z.worte) and nach is not None and nach.x0 >= aktuell.x0 + 4):
                # (nicht eine fette Zwischenüberschrift, unter der wieder eingerückt weitergeht: «B. Zeitschriften-
                # aufsätze» / … / «Artikel in der Gewerkschaftlichen Rundschau» / eingerückt «Wohnungsbau …», VII.109.)
                # (nur wenn der ganze Inhalt nach dem Titelabsatz eingerückt war – nicht bei gemischtem Inhalt wie
                # «A. Abgabe von Materialien …» mit «Drucksachen (I)» am Rand, VII.191. VIII.)
                zs = aktuell.zeilen
                k = next((n for n in range(1, len(zs)) if luft(zs[n - 1], zs[n]) > 4), len(zs))
                eltern = next((v for v in reversed(vorkommen) if v.pfad == aktuell.pfad[:-1] and not v.ist_teil),
                              None) if k < len(zs) and all(x.x0 >= aktuell.x0 + 4 for x in zs[k:]) else None
                if eltern is not None and aktuell.typ in gl.rang:
                    r = gl.rang[aktuell.typ]
                    while gl.stapel and gl.stapel[-1][0] >= r:
                        gl.stapel.pop()  # die nächste Nummer gehört zur Gruppe, nicht mehr zu diesem Punkt
            if eltern is not None:
                umleitung = (aktuell, eltern)
        ziel = aktuell
        if umleitung is not None and umleitung[0] is aktuell:
            ziel = umleitung[1]
        elif gl.modus == "dezimal" and striche_am_rand and ist_aufzaehlung(z) and len(aktuell.pfad) >= 2 \
                and not aktuell.fett and aktuell.x0 and abs(z.x0 - aktuell.x0) <= 3 and aktuell.zeilen \
                and aktuell.zeilen[0].x0 > z.x0 + 20:  # fette Unterpunkte sind Gruppen («1.1. Urkunden», VII.360.)
            folgend = next((t for t in (lies_signatur(x, gl.kopie()) for x in zeilen[i + 1:i + 200]) if t), None)
            oben_v = None
            if folgend is None or folgend.pfad[:len(aktuell.pfad)] != aktuell.pfad:
                oben_v = next((v for v in reversed(vorkommen) if v.pfad == aktuell.pfad[:-1]
                               and v.bestand == aktuell.bestand and not v.ist_teil), None)
            umleitung = (aktuell, oben_v or aktuell)
            ziel = umleitung[1]
        ziel.zeilen.append(z)
        merke(z, "einheit", ziel)
    if box["marke"] and aktuell is not None:  # letzte Zeile «Schachtel 400» (VII.181.): gilt für die letzte Einheit
        nummer, quelle, vb = box["marke"]
        if quelle is not None:  # «10.2. Schachtel 8» als letzte Zeile einer Zuordnungsliste
            bekannt = next((v for v in reversed(vorkommen) if v.pfad == quelle[0]), None)
            if bekannt is not None and not bekannt.schachtel:
                bekannt.schachtel, vb.vorkommen = nummer, bekannt
        elif box["datum"]:
            schachtel_als_teil()
        else:
            inhalt_beginnt(vb.zeile)
    for vb in box["extra"]:  # nicht zuzuordnende Datumszeilen (sollte nicht vorkommen)
        vb.art = "vorlauf"
    for nummer, von, bis, vb in zuordnung:
        def im_bereich(p: tuple) -> bool:
            if bis is None or len(bis) != len(von) or not (von[-1].isdigit() and bis[-1].isdigit()):
                return p[:len(von)] == von
            return len(p) >= len(von) and p[:len(von) - 1] == von[:-1] and p[len(von) - 1].isdigit() \
                and int(von[-1]) <= int(p[len(von) - 1]) <= int(bis[-1])
        betroffen = [v for v in vorkommen if im_bereich(v.pfad) and not v.ist_teil]
        for v in betroffen:
            v.schachtel = nummer
        if betroffen:
            vb.vorkommen = betroffen[0]
        else:
            vb.art = "ueberschrift"
    # Absatz ohne Signatur in der Signaturspalte nach der letzten Einheit, deren Folgezeilen eingerückt sind, der im
    # Darin gelandet ist: «272 Neujahrsblatt …» / «Mit Kommentar (3 Seiten)» (x 110) / «Messingpokal, versilbert, mit
    # Deckel» (x 71) / «Höhe 22 cm» … (VII.10.) – Hinweis
    letzte_v = [v for v in vorkommen if v.typ != "bestand"]
    if letzte_v and letzte_v[-1].x0 and len(letzte_v[-1].zeilen) >= 3 and letzte_v[-1] is vorkommen[-1]:
        v_l = letzte_v[-1]
        for k_l in range(1, len(v_l.zeilen)):
            x_l, vor_l = v_l.zeilen[k_l], v_l.zeilen[k_l - 1]
            if abs(x_l.x0 - v_l.x0) <= 3 and x_l.seite == vor_l.seite and luft(vor_l, x_l) > ABSATZ_ABSTAND \
                    and x_l.text.strip()[:1].isupper() and k_l >= 2 \
                    and all(y.x0 > v_l.x0 + 20 for y in v_l.zeilen[1:k_l]):
                block_l = v_l.zeilen[k_l:]
                text_l = " ".join(x.text for x in block_l)
                # ein Stück ohne Nummer: «Schachtel II. Anträge der Verwaltungs- und Dienstabteilungen» (V.A.c.23.),
                # «Messingpokal, versilbert, mit Deckel» / «Höhe 22 cm» (VII.10.) – zur Zeile für den Bestand
                if v_l.typ != "bestand" and (
                        re.match(r"(?:Schachtel|Mappe|Karton)\s+[IVXL]{1,5}\.?\s", x_l.text.strip())
                        or re.search(r"\b(?:liegt bei|liegen bei|beiliegend|beigelegt|beigefügt)\b", text_l)
                        or re.search(r"\b\d+(?:,\d+)?\s*(?:x\s*\d+(?:,\d+)?\s*)*cm\b|\bHöhe\s+\d", text_l)):
                    v_s = sammelzeile(x_l)
                    v_s.hinweise.append(f"Stück ohne Nummer im Findmittel («{x_l.text.strip()[:70]}», S. {x_l.seite}) – "
                                        "hier beim Bestand übernommen (keine Signatur erfunden); in scope beim Bestand "
                                        "ergänzen oder von Hand als Einheit anlegen.")
                    ids_l = {id(x) for x in block_l}
                    v_s.zeilen.extend(block_l)
                    del v_l.zeilen[k_l:]
                    for vb in verbleib:
                        if vb.vorkommen is v_l and id(vb.zeile) in ids_l:
                            vb.vorkommen = v_s
                    break
                v_l.hinweise.append(f"Nach der letzten Einheit steht im Findmittel ein Absatz ohne Signatur "
                                    f"(«{x_l.text.strip()[:60]}» …) – hier im Darin übernommen, bitte prüfen.")
                break
    for v in vorkommen:  # Schachtelübersicht am Schluss (VII.11.): die genaueste genannte Nummer gilt
        passend = [p for p in box_uebersicht if v.pfad[:len(p)] == p]
        if passend and not v.ist_teil:
            v.schachtel = schachtel_liste(list(dict.fromkeys(box_uebersicht[max(passend, key=len)])))
            v.schachtel_geerbt = False
    for v, zeilen_g in gruppen_nachtrag:  # Beschreibung der Gruppe hinter das eigene Darin der Einheit
        if not v.zeilen:
            continue  # (leere Nummer «IV.A.62.» ohne Titel: nicht die Beschreibung als Titel)
        if not v.titel_bis:
            v.titel_bis = len(v.zeilen)  # (nie Teil des Titels, auch nicht als Klammer «(Es wurden …)», IV.A.)
        # (als eigener Absatz, nicht an die letzte Darin-Zeile der Einheit angehängt)
        v.zeilen.extend(Zeile(x.seite, x.top + 10000, x.bottom + 10000, x.worte, x.datum, x.umfang, x.schachtel,
                              x.spalten) for x in zeilen_g)
    return vorkommen


# ----------------------------------------------------------------------------- Text flicken

ANSCHLUSS_WOERTER = {
    "und", "oder", "sowie", "bzw.", "resp.", "der", "die", "das", "des", "dem", "den", "ein", "eine", "einer",
    "eines", "einem", "einen", "von", "vom", "zu", "zum", "zur", "mit", "für", "über", "in", "im", "an", "am",
    "auf", "aus", "bei", "nach", "gegen", "durch", "zwischen", "u.", "z.", "Nr.", "Sign.", "Dr.", "Prof.", "St.",
    "betreffend", "betr.", "bezüglich", "inkl.", "ca.", "&", "+", "/", "–",
    "bis",  # «… vom 1. August 1822 bis» / «31. Dezember 1823, Winterthur …» (VII.510.)
}
KONJUNKTIONEN = {"und", "oder", "bzw.", "sowie", "resp.", "u."}
# Artikel und Präpositionen beenden nie einen Eintrag – auch nicht gross geschrieben
ANSCHLUSS_KLEIN = {"der", "die", "das", "des", "dem", "den", "ein", "eine", "einer", "eines", "einem", "einen",
                   "und", "oder", "von", "vom", "zu", "zum", "zur", "mit", "für", "über", "im", "am", "auf", "aus",
                   "bei", "nach"}


# «… an den Stadtpräsidenten» / «R. Billeter, 13. November 1910» (VII.37.)
PERSONENBEZEICHNUNG_AM_ENDE_RE = re.compile(
    r"(?:präsident(?:en)?|Herrn?|Herren|Frau|Fräulein|Direktor[s]?|[Rr]eferent(?:en)?|[Ss]tadtrat|[Rr]egierungsrat"
    r"|Pfarrer|[Bb]aumeister[s]?|[Ii]ngenieur[s]?|Dr\.|Prof\."
    # «… im Seitenprofil; Künstler:» / «A. Engelhardt» (VII.109.)
    r"|(?:Künstler|Fotograf|Photograph|Autor|Verfasser|Architekt|Maler|Bildhauer)(?:in)?:)$")


def _namensliste_umbruch(vt: str, nt: str) -> bool:
    """«Maria Thorgevsky, Dan Wiener, Will Quadflieg, Cole Porter, Gert» + «Westphal, …»: in einer Liste von
    Namen (je mindestens zwei gross geschriebene Wörter) steht am Zeilenende nur ein Vorname oder ein Initial."""
    teile = vt.split(", ")
    if len(teile) < 3:
        return False
    if not re.fullmatch(r"[A-ZÄÖÜ][\w'’\-]+|(?:[A-ZÄÖÜ][\w'’\-]+\s)+[A-ZÄÖÜ]\.", teile[-1]):
        return False
    for teil in teile[-3:-1]:
        w = teil.split()
        if len(w) < 2 or not w[0][:1].isupper() or not w[-1][:1].isupper():
            return False
    return re.match(r"[A-ZÄÖÜ][\w'’]+(?:-[A-ZÄÖÜ][\w'’]+)?(?:,|\s+u\.\s?a\.|$)", nt) is not None


def ist_umbruch(vorher: Zeile, z: Zeile, bisher: str, rand: float) -> bool:
    """True, wenn z die Fortsetzung von vorher ist (weicher Umbruch) und nicht ein neuer Eintrag."""
    vt, nt = vorher.text.rstrip(), z.text.lstrip()
    if not nt or not vt:
        return True
    if ist_aufzaehlung_mit_marke(z):
        return False
    # nummerierte Liste: «53. Mileva mit Söhnen … in Zürich» (bis an den Rand) / «54. Mileva auf ihrer Terrasse»
    # – auch ohne Punkt über einen Seitenwechsel («19 Plakette aus Holz …» / «20 Plakette, zwei Knaben …», VII.222.)
    #   und in Klammern («(3) René Peter …» / «(4) Inge Spillmann-Weber …», V.L.156.)
    for muster in (r"(\d{1,3})\.\s", r"(\d{1,3})\s(?=\D)", r"\((\d{1,3})\)\s"):
        m_bisher, m_neu = re.match(muster, bisher.lstrip()), re.match(muster, nt)
        if m_bisher and m_neu and int(m_neu.group(1)) == int(m_bisher.group(1)) + 1:
            return False
    # chronologische Liste: «1814 Proklamation …» / «1815 Publication …» (V.L.14.)
    j_bisher, j_neu = re.match(rf"({JAHR})\s+\D", bisher.lstrip()), re.match(rf"({JAHR})\s+\D", nt)
    if j_bisher and j_neu and int(j_neu.group(1)) >= int(j_bisher.group(1)):
        return False
    letztes = vt.split()[-1]
    if re.search(r"[A-Za-zÄÖÜäöüß]-$", vt) or re.search(r"\d\s?[–-]$", vt):
        return True
    # auch gross geschrieben: «… Fot. Serda) Die» + «Launen der Donna Belisa»
    if vt[-1] in ",(/&+„«‚:;" or letztes in ANSCHLUSS_WOERTER or letztes.lower() in ANSCHLUSS_KLEIN:
        return True
    if re.search(rf"{MONAT_MUSTER}$", vt) and re.match(rf"{JAHR}\b", nt):
        return True  # «vom 15. Okt.» + «1952, Abschrift»
    if re.search(r"(?:^|\s)\d{1,2}\.$", vt) and re.match(MONAT_MUSTER, nt):
        return True  # «vom 6.» + «Juni 1971»
    if nt[0].islower() or nt[0] in "()]»“":
        return True
    if bisher.count("(") > bisher.count(")") or bisher.count("„") > bisher.count("“"):
        return True
    # Namensliste über den Umbruch, auch wenn das erste Wort noch Platz gehabt hätte: «…, Cole Porter, Gert» /
    # «Westphal, Dietmar …», «…, Peter W.» / «Loosli, …», «… Tourneetheater» / «E. Grabowsky» (VII.200.)
    if vorher.x1 >= 0.8 * rand and (_namensliste_umbruch(vt, nt) or (
            PERSONENBEZEICHNUNG_AM_ENDE_RE.search(vt) and re.match(r"[A-ZÄÖÜ]\.\s?[A-ZÄÖÜ][\w'’\-]{2,}", nt))):
        return True
    w = z.worte[0]
    rand_hier = rand if not vorher.datum else min(rand, 470)  # Zeile mit Datumsspalte endet früher
    return vorher.x1 + 4 + (w.x1 - w.x0) > rand_hier - 2  # erstes Wort hätte nicht mehr Platz gehabt


def verbinde(a: str, b: str) -> str:
    a, b = a.rstrip(), b.lstrip()
    if not a:
        return b
    if not b:
        return a
    if re.search(r"[A-Za-zÄÖÜäöüß]-$", a):
        erstes = b.split()[0]
        if b[0].islower() and erstes not in KONJUNKTIONEN:
            return a[:-1] + b  # Silbentrennung «Probenrap-» + «porte»
        if erstes in KONJUNKTIONEN:
            return a + " " + b  # «Kinder-» + «und Jugendtheater»
        return a + b  # «Schauspielhaus-» + «Keller-Bühne»
    if re.search(r"\d\s?[–-]$", a) and b[:1].isdigit():
        return a + b  # «1940–» + «1952»
    return a + " " + b


def saeubere(text: str) -> str:
    text = re.sub(r"\s*\.{4,}\s*\d*\s*$", "", text)  # Punktleitern im Inhaltsverzeichnis
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,;.:)])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    return text


@dataclass
class Eintrag:
    text: str
    start_x0: float
    letzte: Zeile
    zusatz: list[str] = field(default_factory=list)  # Datum/Schachtel aus der rechten Spalte seiner Zeilen
    stueck_ab: int = 0  # Beginn des letzten «; »-Teilstücks im Text
    text_x0: float | None = None  # Einzug des Textes nach dem Aufzählungszeichen

    def schliesse_stueck(self) -> None:
        """Spaltenangaben ans Ende des laufenden Teilstücks setzen (vor dem nächsten «; »)."""
        if self.zusatz:
            vorn, stueck = self.text[:self.stueck_ab], self.text[self.stueck_ab:]
            self.text = vorn + _mit_zusatz(stueck.rstrip(" ;"), self.zusatz)
            self.zusatz = []


def _spalten_zusatz(z: Zeile, ohne: set[tuple[int, str]]) -> list[str]:
    """Rechte Spalte einer Zeile («1890-1916», «Schachtel 301»), sofern sie nicht schon der Zeitraum bzw.
    die Schachtel der Einheit ist (ohne = {(id(zeile), "datum"|"schachtel")})."""
    teile = []
    if z.datum and (id(z), "datum") not in ohne:
        teile.append(z.datum)
    if z.schachtel and (id(z), "schachtel") not in ohne:
        teile.append(f"Schachtel {z.schachtel}")
    if z.umfang and (id(z), "umfang") not in ohne:
        teile.append(z.umfang)
    if z.spalten:
        teile.append(z.spalten)
    return teile


def _mit_zusatz(text: str, zusatz: list[str]) -> str:
    """«Hausordnung … 1891, 1901» + Spalte «1891-1901» -> «…, 1891-1901»; steht derselbe Zeitraum schon
    im Text, wird er nicht wiederholt."""
    for z in zusatz:
        if finde_zeitraeume(z, False):
            im_text = vereinige(finde_zeitraeume(text, False))
            if im_text and _jahre(im_text) == _jahre(vereinige(finde_zeitraeume(z, False))):
                continue
        text = f"{text}, {z}" if text else z
    return text


# Listen mit einem Eintrag je Zeile: «Titel von Autor» (Fotos der Aufführungen, VII.200. 8.1.1.) bzw.
# «Titel (Szenenfotos, Porträts, Fot. …)» (Negative, VII.200. 8.3.)
# die Zeile endet mit dem Autor (und allenfalls dem Premierendatum): «Zorn von Ria Endres, 20. März 1993 (…)»
VON_EINTRAG_RE = re.compile(
    r"^[^()]*\S\s+[Vv]on\s+(?:(?:[A-ZÄÖÜ][\w'’´.\-]*,?|de|da|del|di|du|van|von|le|la|und|&|/)\s*)+"
    r"(?:,\s*\d{1,2}\.\s?[^,()]*?\d{4}(?:\s+[A-ZÄÖÜ][\w'’\-]*|\s*\([^()]*\))?)?$")
ARTIKEL_ANFANG = {"Der", "Die", "Das", "Ein", "Eine", "Des"}
# klein geschriebene Anfänge eines Listeneintrags («- einzelne Zeitungsartikel …», «- diverse Formulare u. a.»)
LISTENANFANG_KLEIN = {"diverse", "div.", "einzelne", "verschiedene", "weitere", "zahlreiche", "statistisches",
                      "statistische", "kurze", "kleine", "private", "gedruckte", "handschriftliche", "undatierte",
                      "unidentifizierte", "allgemeine", "sonstige", "übrige"}
VERBINDUNG_AM_ENDE_RE = re.compile(r"(?:[,;:/(&+–-]|\b(?:und|oder|von|vom|der|die|das|des|dem|den|mit|für|zu|zum|"
                                   r"zur|im|in|an|am|auf|aus|bei|über|u\.))\s*$")


def _listenart(zeilen: list[Zeile]) -> str | None:
    texte = [z.text.strip() for z in zeilen if z.text.strip() and not ist_aufzaehlung(z)]
    if len(texte) < 4:
        return None
    if sum(1 for t in texte if VON_EINTRAG_RE.match(t)) >= 0.6 * len(texte):
        return "von"
    if sum(1 for t in texte if KLAMMEREINTRAG_RE.match(t)) >= 0.5 * len(texte):
        return "klammer"
    return None


def _eintrag_vollstaendig(text: str, art: str) -> bool:
    t = text.strip()
    if art == "von":
        if VON_EINTRAG_RE.match(t) is None or VERBINDUNG_AM_ENDE_RE.search(t):
            return False
        # der Autor hat Vor- und Nachnamen (nicht «… Hans im Unglück von Jürg» / «Federspiel / …», VII.200. 8.1.1.42.),
        # ausser bei einem bekannten Einzelnamen («Prometheus von Aischylos») oder mit Datum dahinter
        autor = re.split(r"\s[Vv]on\s", t)[-1]
        if re.search(r",\s*\d", autor):
            return True
        letzter = re.split(r",|\s(?:und|&)\s|\s/\s", autor)[-1].split()
        return len(letzter) >= 2 or bool(letzter and re.fullmatch(_EINZELNAME + r"\.?", letzter[0]))
    return KLAMMEREINTRAG_RE.match(t) is not None


def richte_verschobene_anfaenge(zeilen: list[Zeile], art: str, ohne: set[tuple[int, str]]) -> list[Zeile]:
    """Im PDF ist das erste Wort eines Listeneintrags ans Ende der Vorzeile gerutscht: «Der lebende Leichnam von
    Leo N. Tolstoi Regen» / «und Wind von Merton Hodge», «… Fot. René Haury) Der» / «leere Stuhl (…)» (VII.200.)."""
    neu = list(zeilen)
    for k in range(len(neu) - 1):
        z, n = neu[k], neu[k + 1]
        if len(z.worte) < 3 or not n.worte or n.seite != z.seite or abs(z.x0 - n.x0) > 3 \
                or ist_aufzaehlung(z) or ist_aufzaehlung(n):
            continue
        w = z.worte[-1]
        if not w.text[:1].isalpha() or not w.text[0].isupper() or w.text.endswith("-") or w.text.isupper():
            continue
        rest, nt = " ".join(x.text for x in z.worte[:-1]), n.text.strip()
        jahr_am_ende = re.search(rf"{JAHR}\)?$", rest) is not None
        if not (_eintrag_vollstaendig(rest, art) or jahr_am_ende):
            continue
        if art == "von":
            if nt.startswith("von "):
                verschieben = True  # «Mandragola von Max Christian Feiler Kolportage» / «von Georg Kaiser»
            elif not _eintrag_vollstaendig(nt, art):
                continue
            else:
                verschieben = nt[:1].islower() or w.text in ARTIKEL_ANFANG or jahr_am_ende
        else:
            verschieben = rest.endswith(")") and "(" in nt
        if not verschieben:
            continue
        z_neu = Zeile(z.seite, z.top, z.bottom, z.worte[:-1], z.datum, z.umfang, z.schachtel, z.spalten)
        w_neu = Wort(w.text, n.x0, n.x0 + (w.x1 - w.x0), w.font, w.size)
        n_neu = Zeile(n.seite, n.top, n.bottom, [w_neu] + n.worte, n.datum, n.umfang, n.schachtel, n.spalten)
        for alt_z, neu_z in ((z, z_neu), (n, n_neu)):
            for art_o in ("datum", "schachtel", "umfang"):
                if (id(alt_z), art_o) in ohne:
                    ohne.add((id(neu_z), art_o))
        neu[k], neu[k + 1] = z_neu, n_neu
    return neu


def baue_eintraege(zeilen: list[Zeile], rand: float, erste_ist_aufzaehlung: bool = False,
                   inline_teilen: bool = True, unterzeilen: bool = True,
                   ohne: set[tuple[int, str]] | None = None) -> list[str]:
    """Zeilen zu Einträgen: Aufzählungen, weiche Umbrüche, eingerückte Unterzeilen.

    unterzeilen=False: eine eingerückte Zeile nach hartem Umbruch wird ein eigener Eintrag
    (für Titelblöcke – sonst hinge «Juni-Festwochen 1959 …» mit «; » am Titel).
    Datum und Schachtel aus der rechten Spalte kommen ans Ende des Eintrags (ausser bei Zeilen in «ohne»)."""
    ohne = ohne if ohne is not None else set()
    art = _listenart(zeilen) if unterzeilen else None
    if art:
        zeilen = richte_verschobene_anfaenge(zeilen, art, ohne)
    eintraege: list[Eintrag] = []
    mit_strichliste = sum(1 for z in zeilen if z.worte and z.worte[0].text == "-") >= 2
    for i, z in enumerate(zeilen):
        if not z.text.strip():
            continue
        zusatz = _spalten_zusatz(z, ohne)
        if eintraege and ist_aufzaehlung(z) and z.worte[0].text in ("-", "–") and "“" in z.text.split("„")[0] \
                and eintraege[-1].text.count("„") > eintraege[-1].text.count("“"):
            akt = eintraege[-1]  # «„Hans Sahl» / «– Ein Narr der Aufrichtigkeit“» (VII.200. 5.2.5.14.)
            akt.text, akt.letzte = verbinde(akt.text, z.text), z
            akt.zusatz.extend(zusatz)
            continue
        if ist_aufzaehlung(z) or (i == 0 and erste_ist_aufzaehlung):
            rest = z.ab(1) if ist_aufzaehlung(z) else z
            text_x0 = rest.x0 if ist_aufzaehlung(z) and rest and rest.worte else None
            eintraege.append(Eintrag(rest.text if rest else "", z.x0, z, zusatz, text_x0=text_x0))
            continue
        if not eintraege or ist_aufzaehlung_mit_marke(z):
            eintraege.append(Eintrag(z.text, z.x0, z, zusatz))
            continue
        akt = eintraege[-1]
        a = abstand(akt.letzte, z)
        neue_tabellenzeile = (z.datum and (id(z), "datum") not in ohne
                              and any(finde_zeitraeume(t, False) for t in akt.zusatz))
        letzte = akt.letzte.worte
        # (ein Gedankenstrich «–» nur in einer Aufzählung und nicht als zweiter eines Paars: «Es sind 2 Photographien
        # – mit Beschriftung … –» / «enthalten.», VII.277.)
        erstes = z.worte[0].text
        strich_am_ende = (len(letzte) > 1 and letzte[-1].text == "-" and letzte[-2].text not in AUFZAEHLUNG
                          and "Italic" not in letzte[-2].font and letzte[-2].text not in KONJUNKTIONEN
                          and not MONAT_WORT_RE.match(letzte[-2].text) and not re.match(r"[\d(]", letzte[-2].text)
                          and akt.text.count("„") <= akt.text.count("“")
                          and (erstes in LISTENANFANG_KLEIN
                               or (erstes[:1].isupper() and not MONAT_WORT_RE.match(erstes) and mit_strichliste
                                   and not re.search(r"\s[–-]\s", z.text))))
        if (a is not None and a > ABSATZ_ABSTAND) or neue_tabellenzeile:
            eintraege.append(Eintrag(z.text, z.x0, z, zusatz))
        elif strich_am_ende:
            # das Aufzählungszeichen des nächsten Eintrags ist ans Zeilenende gerutscht: «… Direktion des
            # Burgtheaters -» / «einzelne Zeitungsartikel über Gerhard Klingenberg» (VII.200. 2.3.2.10.)
            akt.text = re.sub(r"\s*[-–]\s*$", "", akt.text)
            eintraege.append(Eintrag(z.text, z.x0, z, zusatz, text_x0=z.x0))
        elif art and _eintrag_vollstaendig(akt.text, art) and _eintrag_vollstaendig(z.text, art) \
                and z.x0 <= akt.start_x0 + 4 and re.match(r"[A-ZÄÖÜ„\"«\d]", z.text.lstrip()) \
                and not z.worte[0].text.endswith(","):
            eintraege.append(Eintrag(z.text, z.x0, z, zusatz))  # je Zeile ein Stück «Titel von Autor»
        elif ist_umbruch(akt.letzte, z, akt.text, rand):
            akt.text, akt.letzte = verbinde(akt.text, z.text), z
            akt.zusatz.extend(zusatz)
        elif unterzeilen and z.x0 > akt.start_x0 + 4:  # eingerückte Unterzeile desselben Eintrags
            akt.schliesse_stueck()
            akt.text = akt.text.rstrip(" ;") + "; "
            akt.stueck_ab = len(akt.text)
            akt.text, akt.letzte = akt.text + z.text, z
            akt.zusatz.extend(zusatz)
        else:
            eintraege.append(Eintrag(z.text, z.x0, z, zusatz))
    for e in eintraege:
        e.schliesse_stueck()
    texte = [saeubere(e.text) for e in eintraege]
    return teile_inline(texte) if inline_teilen else [t for t in texte if t]


def teile_inline(texte: list[str]) -> list[str]:
    """Im PDF zusammengerutschte Aufzählungen trennen: «… Trauerfeier - Nachruf Emmie …»."""
    neu = []
    for t in texte:
        teile, anfang = [], 0
        for m in re.finditer(r"\s+-\s+(?=[A-ZÄÖÜ„\"«])", t):
            if re.search(rf"\b{JAHR}\s*$", t[:m.start()]) and re.match(rf"{MONAT_MUSTER}\s+{JAHR}", t[m.end():]):
                continue  # «Raumprogramme Juni 1955 - August 1959»: Datumsbereich
            davor = t[anfang:m.start()]
            if davor.count("„") > davor.count("“") or davor.count('"') % 2 or davor.count("«") > davor.count("»"):
                continue  # «"Frankenstein - Entstehung, Vorläufer …"» (VII.200. 4.2.6.8.): Strich im Werktitel
            if NAMENSEINTRAG_STRENG_RE.match(davor) and not NAMENSEINTRAG_RE.match(t[m.end():]):
                continue  # «Grumberg, Jean-Claude: Morgen - Ein Fenster zur Strasse» (VII.200. 6.32.)
            teile.append(t[anfang:m.start()])
            anfang = m.end()
        teile.append(t[anfang:])
        if re.match(r"\d{1,3}\.\s", t):
            teile = [t]  # nummerierter Eintrag «18. Burri - Germane, 29. April 1948»: Gedankenstrich im Text
        for teil in teile:
            teil = teil.strip(" -–")
            if teil:
                neu.append(teil)
    return neu


# Rollenbücher u. Ä.: «Name, Vorname: Titel»; im PDF ist der Nachname oft ans Ende der
# vorherigen Zeile gerutscht («… Schuld und Sühne Goethe,» / «Johann Wolfgang von: Götz …»).
# (weitere Wörter ohne Punkt ausser Initialen: «Marco Antonio de la», nicht «Wunschvorstellung Schweizer Frau.
# Lizentiatarbeit», VII.237.)
_VORNAME = (r"[A-ZÄÖÜ][\w'’.\-]*(?:\s(?:[A-ZÄÖÜ][\w'’\-]*|[A-ZÄÖÜ]\.|von|van|de|du|la|le|zu|der|da|di|y))"
            r"{0,3}?")
_PARTIKEL = r"(?:de|di|da|del|della|du|van|von|le|la)\s"
_AUTOR = rf"(?:{_PARTIKEL})?[A-ZÄÖÜ][\w'’\-]+,\s?{_VORNAME}"  # auch «de Vega,Lope» (VII.200. 6.4.)
_AUTOREN = rf"{_AUTOR}(?:\s?;\s{_AUTOR})*"
# Autoren mit nur einem Namen, die in Rollenbuchlisten ohne Vornamen stehen («… liebe Gott Molière: Tartuffe»)
_EINZELNAME = r"(?:Molière|Moliere|Sophokles|Aischylos|Euripides|Aristophanes|Plautus|Terenz|Seneca|Menander|Voltaire)"
# zum Erkennen eines Eintrags dürfen Nachnamen mehrteilig sein («Calderon de la Barca, Pedro: …»)
_AUTOR_LANG = (rf"(?:{_PARTIKEL})?[A-ZÄÖÜ][\w'’\-]+(?:\s(?:de|da|del|della|di|du|la|le|van|von|der|den|ten|y"
               rf"|[A-ZÄÖÜ][\w'’\-]+)){{0,3}},\s?{_VORNAME}")
_AUTOREN_LANG = rf"{_AUTOR_LANG}(?:\s?(?:;|/)\s{_AUTOR_LANG})*"
NAMENSEINTRAG_RE = re.compile(rf"^(?:{_AUTOREN_LANG}(?:\s?;\s[^:;]{{2,40}})?|[A-ZÄÖÜ][\w'’\-]+):\s")
# streng: nur «Name, Vorname:» oder ein bekannter Einzelname – nicht «Sonntagsmatinee: …» (VII.200. 5.2.5.12.)
NAMENSEINTRAG_STRENG_RE = re.compile(rf"^(?:{_AUTOREN_LANG}(?:\s?;\s[^:;]{{2,40}})?|{_EINZELNAME}):\s")
NAMENSGRENZE_RE = re.compile(rf"(?<=[^\s,;])\s+(?=(?:{_AUTOREN}|{_EINZELNAME}):\s)")


def ist_namensliste(eintraege: list[str]) -> bool:
    passend = sum(1 for e in eintraege if NAMENSEINTRAG_RE.match(e))
    return len(eintraege) >= 1 and passend >= max(1, len(eintraege) * 0.5)


VORNAME_STOP = {"Manuskript", "Manuskripte", "Typoskript", "Text", "Texte", "Brief", "Briefe", "Programm", "Programme",
                "Korrespondenz", "Notizen", "Foto", "Fotos", "Zeitungsartikel", "Kritik", "Kritiken", "Plakat",
                "Plakate", "Flugblatt", "Prospekt", "Einladung", "Rede", "Reden", "Vortrag", "Lesung", "Interview",
                "Akten", "Inhalt", "Darin", "Titel", "Verlag", "Druck", "Bericht", "Berichte", "Plan", "Pläne",
                "Regie", "Musik", "Leitung", "Solist", "Solistin", "Bühnenbild", "Kostüme", "Fassung", "Produktion"}


def trenne_namenseintraege(text: str) -> list[str]:
    """«… Schuld und Sühne Goethe, Johann Wolfgang von: Götz …» -> zwei Einträge.

    Getrennt wird nur, wenn das linke Stück schon ein vollständiger Eintrag «Name: Titel» ist –
    «Moss Hart, George S. Kaufman: …» oder «Calderon de la Barca, Pedro: …» bleiben ganz."""
    teile, anfang = [], 0
    for m in NAMENSGRENZE_RE.finditer(text):
        links = text[anfang:m.start()]
        # der «Vorname» muss nach einem Namen aussehen: nicht «… über Hannah Arendt, Manuskript: …» (VII.200.
        # 5.2.5.12.) oder «… II: Presseberichte, III: Anton Largiadèr …» (VII.159.)
        vorname = re.match(r"[^,:]*,\s?([^\s:,;]+)", text[m.end():])
        if vorname and (vorname.group(1) in VORNAME_STOP
                        or not re.search(r"[a-zäöüßé]|^[A-ZÄÖÜ]\.$", vorname.group(1))):
            continue
        if ": " in links and NAMENSEINTRAG_RE.match(links.strip() + " "):
            teile.append(links.strip())
            anfang = m.end()
    teile.append(text[anfang:].strip())
    return [t for t in teile if t]


# Fotolisten u. Ä.: «Stücktitel (Szenenfotos, Porträts, Fot. …)»; auch hier rutscht der Anfang des
# nächsten Eintrags ans Zeilenende («… Fot. Peter Zimmermann) Als der» / «Krieg zu Ende war (…)»).
KLAMMEREINTRAG_RE = re.compile(r"^[^()]{2,120}\([^()]+\)\.?$")
KLAMMERGRENZE_RE = re.compile(r"(?<=\))[\s;]+(?=[A-ZÄÖÜ„\"«][^()]{0,80}\([^()]+\))")


def flicke_klammerlisten(eintraege: list[str]) -> tuple[list[str], bool]:
    neu = []
    for e in eintraege:
        neu.extend(t.strip() for t in KLAMMERGRENZE_RE.split(e) if t.strip())
    if neu == eintraege or sum(1 for t in neu if KLAMMEREINTRAG_RE.match(t)) < max(2, len(neu) * 0.6):
        return eintraege, False
    return neu, True


def flicke_listen(eintraege: list[str]) -> tuple[list[str], bool]:
    if ist_namensliste(eintraege):
        neu = []
        for e in eintraege:
            neu.extend(trenne_namenseintraege(e))
        return neu, neu != eintraege
    return flicke_klammerlisten(eintraege)


# ----------------------------------------------------------------------------- Einheiten


@dataclass
class Einheit:
    id: int
    pfad: tuple[str, ...]
    anzeige: str
    roh: str
    seite: int
    art: str  # «knoten» (erste Nennung einer Signatur) oder «teil»
    titel: str = ""
    titel_uebernommen: bool = False
    darin: list[str] = field(default_factory=list)
    verweise: list[str] = field(default_factory=list)
    schachtel: str | None = None
    umfang: list[str] = field(default_factory=list)
    teil_nr: int | None = None
    eltern: "Einheit | None" = None
    kinder: list["Einheit"] = field(default_factory=list)
    teile_liste: list["Einheit"] = field(default_factory=list)
    zeitraum: Zeitraum | None = None
    ereignis_zeitraum: Zeitraum | None = None
    spalten_zeitraum: Zeitraum | None = None
    zeitraum_quelle: str = ""
    undatiert: bool = False
    hinweise: list[str] = field(default_factory=list)
    herkunft: Einheit | None = None  # «Teil 1», abgespalten von dieser Einheit (spalte_teil1_ab)
    entfernt: str = ""  # Grund, wenn die Einheit nicht ins Excel kommt (Übersichtszeile)
    doppelpunkt: str = ""  # Signatur mit ergänztem «:» («VII. 47.1.» -> «VII.47.:1.», siehe ergaenze_doppelpunkte)
    behaelter: bool = False  # Mappe/Schachtel ohne Signatur: der Titel ist nur ihre erste Zeile
    titel_mit_datum: str = ""  # Titel vor dem Entfernen des Zeitraums (zeitraum_aus_titel)
    bestand: str = ""  # nur bei Findmitteln für mehrere Bestände (sonst gilt der Bestand des Findmittels)
    schachtel_geerbt: bool = False  # siehe Vorkommen.schachtel_geerbt
    darin_spalte: Zeitraum | None = None  # Vereinigung der Datumsspalten der Einträge im Darin
    darin_spalte_traegt: bool = False  # mindestens die Hälfte der Einträge hat ein Spaltendatum
    darin_funde: list = field(default_factory=list)  # die einzelnen Spaltendaten des Darin
    darin_ohne_spalte: str = ""  # Text der Inhaltszeilen ohne Spaltendatum (für die ergänzende Schätzung)
    spalte_erweitert: bool = False  # Datumsspalte der Titelzeile um Darin-Daten erweitert
    darin_erweiterung: "Zeitraum | None" = None  # der Teil aus dem Darin, um den die Spalte erweitert wurde
    beginnt_mit_punkt: bool = False  # die erste Zeile (nach der Signatur) ist ein Aufzählungspunkt «- …»
    strichliste: bool = False  # das Darin enthält Aufzählungspunkte «- …»

    @property
    def tiefe(self) -> int:
        # (Tiefe im Baum: Bereiche «50-58» / «57-58» / «58» haben gleich lange Pfade, VII.80.)
        n, e = 1, self
        while e.eltern is not None and n < 60:
            n, e = n + 1, e.eltern
        return max(n, len(self.pfad) + (1 if self.art == "teil" else 0))


def datumszeile_setzt_fort(zeilen: list[Zeile], i: int, rand: float) -> bool:
    """Setzt Zeile i (mit eigener Datumsspalte) den Titel davor fort? Nur bei deutlichem Anschluss («… und» /
    klein beginnend, IV.A.55.) oder direkt nach der Titelzeile, genau in der Titelspalte, wenn diese voll ist
    («… seit 1970» / «Sozialamt ¦ 1961–1985», IV.A.54.). Sonst ist es ein eigener Eintrag mit eigenem Datum."""
    vorher, z = zeilen[i - 1], zeilen[i]
    vt, nt = vorher.text.rstrip(), z.text.lstrip()
    if not vt or not nt:
        return False
    letztes = vt.split()[-1]
    bisher = " ".join(x.text for x in zeilen[:i])
    if (nt[0].islower() or re.search(r"[A-Za-zÄÖÜäöüß]-$", vt) or vt[-1] in "(/&+" or letztes in ANSCHLUSS_WOERTER
            or letztes.lower() in ANSCHLUSS_KLEIN or bisher.count("(") > bisher.count(")")):
        return True
    w = z.worte[0]
    return i == 1 and abs(z.x0 - zeilen[0].x0) <= 6 and vorher.x1 + 4 + (w.x1 - w.x0) > min(rand, 470) - 2


# Unterlagen einer Produktion (VII.200.): beginnt eine Zeile so, ist sie Inhalt, nicht Fortsetzung des Titels
UNTERLAGEN_MUSTER = (r"(?:Korrespondenz|Bühnenpl|Bühnenbild|Besetzung|Notizen|Skizze|Akten|Aktennotiz|Aktenvermerk|"
                     r"Probe|Programm|Foto|Szenarium|Vertr[aä]g|Aufführungsvertr|Pressemat|Presse|Zeitungs|Kritik|"
                     r"Beleuchtung|Kosten|Kostüm|Informationsblatt|Unterlagen|Brief|Ankündigung|Plakat|Manuskript|"
                     r"Lebenslauf|Liste der|Verzeichnis der|Textbuch|Stückeinteilung|Regiebuch|Tonband|Strichfassung|"
                     r"Auszug|Einladung|Mitteilung|Vereinbarung|Ablauf|Entwurf|Stückvertr|Bauprobe)")
UNTERLAGEN_RE = re.compile(UNTERLAGEN_MUSTER)
# nach «… von X:» nur typische Unterlagen einer Produktion oder Bewerbung (nicht «Plakatserie …», «Entwurf für …»)
UNTERLAGEN_DOPPELPUNKT = (r"(?:Korrespondenz|Besetzung|Notizen|Akten|Aktennotiz|Aktenvermerk|Probe|Programm|Szenarium|"
                          r"Vertr[aä]g|Aufführungsvertr|Presse|Zeitungs|Kritik|Beleuchtung|Informationsblatt|"
                          r"Unterlagen|Brief|Einladung|Mitteilung|Vereinbarung|Ablauf|Stückvertr|Bauprobe|Auszug|"
                          r"Bühnenpl|Skizzen)")
# bei Teilen (Produktionen, Anlässe) auch ohne «von X» vor dem «:» (VII.200.: «Nachtessen aus Anlass …: Einladung,
# Menü-Karte, Tischordnung», «Circus Helvetia, Projekt: Konzept, Gutachten, …», «… Lesung: Mitteilung»)
UNTERLAGEN_TEIL = (r"(?:Korrespondenz|Besetzung|Notiz|Akten|Aktennotiz|Aktenvermerk|Probe|Programm|Szenarium|"
                   r"Vertr[aä]g|Aufführungsvertr|Presse|Zeitungs|Kritik|Beleuchtung|Informations|Unterlagen|Brief|"
                   r"Einladung|Mitteilung|Vereinbarung|Ablauf|Stückvertr|Bauprobe|Auszug|Bühnenpl|Skizze|Flugbl|"
                   r"Konzept|Projekt-?[Kk]onzept|Projektbeschreibung|Gutachten|Texte\b|Fotos?\b|Planungsskizze|"
                   r"Liste der|Verlauf de|Entwurf|Ansprache|Gedächtnisrede|Kurze Biografie|Teilnehmerliste|"
                   r"Todesanzeige|Tischordnung|Menü|Gesprächsnotiz|Gespräch- und)")
TITEL_KLAMMERDATUM_RE = re.compile(r"\((?:\d{1,2}\.\d{1,2}\.\d{4}|undatiert|nicht aufgeführt|o\.\s?J\.)\)\s*$")


BEREICH_ENDE_RE = re.compile(r"(?:–\s*|-)(\d{1,3})\.\s+\S")  # «– 26. Detailverzeichnis …», «-14. Pläne …»


def _zahl_nach_strich(rest: Zeile) -> bool:
    """Folgt dem Strich eine Signatur oder ein Jahr (Bereich «1.2.1. - 1.2.14.», «4.2. - 1946 – 1960»)? Eine
    Ordnungszahl mit Text («- 70. Geburtstag von Carl J. Burckhardt», VII.200.) zählt nicht."""
    w = rest.worte[1].text if len(rest.worte) > 1 else ""
    if re.fullmatch(rf"\d{{1,4}}(?:\.\d{{1,4}})+\.?|{JAHR}\W?", w):
        return True
    # Gedankenstrich und Zahl sind ein Bereich («7.1. – 26. Detailverzeichnis …», VII.93.; «14.1.1. – 3.», VII.494.);
    # nur nach dem Bindestrich ist es eine Ordnungszahl vor einem gross geschriebenen Wort
    return bool(re.fullmatch(r"\d{1,4}\.?", w)) and not (rest.worte[0].text == "-" and len(rest.worte) > 2
                                                         and rest.worte[2].text[:1].isupper())


def _liste_folgt(zeilen: list[Zeile], i: int, weit: int = 12) -> bool:
    """Folgen unter der Signaturzeile zeilen[i] weitere «-»-Punkte (auch nach einer umbrochenen Zeile), bevor die
    nächste Signatur am linken Rand kommt? Dann ist «3.2. - Beschluss …» der erste Punkt einer Liste (VII.397.)."""
    # (auch ein ans Zeilenende gerutschtes Aufzählungszeichen «… Künstlern und Agenturen -» / «diverse
    # Veranstaltungen: …», VII.200. 5.4.5.4.)
    if len(zeilen[i].worte) > 2 and zeilen[i].worte[-1].text == "-":
        return True
    for z in zeilen[i + 1:i + 1 + weit]:
        if not z.worte or z.x0 <= zeilen[i].x0 + 3:
            return False  # nächste Signatur (oder Zeile am Rand)
        if ist_aufzaehlung(z) or (len(z.worte) > 2 and z.worte[-1].text == "-"):
            return True
    return False


def _allein_vor_absatz(zeilen: list[Zeile], i: int) -> bool:
    """Steht zeilen[i] allein vor einem neuen Absatz (Untertitel «Vermietung, Verpachtung, … ¦ 1873 bis 1902» unter
    «Akten zu Liegenschaften (2):», VII.24.) – und nicht als erster Punkt einer dichten Liste («Zürcher Theaterverein
    ¦ 1918 – 1923» / «Zürcher Theatergemeinde …» unter «Jahres-Abschlüsse:», VII.352.)?"""
    if i + 1 >= len(zeilen):
        return True
    a = abstand(zeilen[i], zeilen[i + 1])
    return a is None or a > ABSATZ_ABSTAND or abs(zeilen[i + 1].x0 - zeilen[i].x0) > 3


def kopf_und_rumpf(zeilen: list[Zeile], rand: float, doppelpunkt: bool = False) -> tuple[list[Zeile], list[Zeile], bool]:
    """Teilt die Zeilen einer Einheit in Kopf (Titelblock) und Rumpf (Darin). doppelpunkt: Titel mit «:» am
    Zeilenende vor einer Aufzählung trennen (nur Einheiten mit eigener Signatur, nicht Teile aus Schachtelangaben).

    Rückgabe: (kopf, rumpf, rumpf_beginnt_mit_aufzaehlung)."""
    if not zeilen:
        return [], [], False
    if ist_aufzaehlung(zeilen[0]):
        return [], zeilen, False
    kopf = [zeilen[0]]
    if TEIL_NUR_RE.match(zeilen[0].text.strip()):
        return kopf, zeilen[1:], False
    for i in range(1, len(zeilen)):
        vorher, z = zeilen[i - 1], zeilen[i]
        if re.search(r"\s[-–]$", vorher.text) and not (re.search(rf"{JAHR}\s?[-–]$", vorher.text)
                                                       and re.match(rf"{JAHR}\b", z.text)):
            # «… von Bertolt Brecht -» / «…-Forum: -» – nicht «… Erinnerungen 1937 –» / «1961 (1 Heft)» (VII.371.)
            return kopf, zeilen[i:], True
        a = abstand(vorher, z)
        if i == 1 and a is not None and a <= ABSATZ_ABSTAND + 1.5 and not (z.datum or z.schachtel or z.umfang) \
                and not re.fullmatch(r"(?:dito|ditto|do|id|idem|detto)\.?", z.text.strip(), re.I) \
                and len(z.worte) <= 4 and z.x0 > vorher.x0 + 30 and any(abs(w.x0 - z.x0) <= 3 for w in vorher.worte[1:]) \
                and not ist_aufzaehlung(z) and (len(zeilen) == 2 or abstand(z, zeilen[2]) is None
                                                or abstand(z, zeilen[2]) > ABSATZ_ABSTAND):
            kopf.append(z)  # (danach folgt ein neuer Absatz oder nichts mehr)
            continue
        if ist_aufzaehlung(z) or ist_aufzaehlung_mit_marke(z) or (a is not None and a > ABSATZ_ABSTAND):
            return kopf, zeilen[i:], False
        # Titel endet mit dem Datum in Klammern: «… Komödie von Edward Bond (02.10.1969)» / eingerückt «Notizen,
        # Besetzungsliste, Programmheft» (VII.200.) – die Folgezeile ist Inhalt
        if TITEL_KLAMMERDATUM_RE.search(vorher.text):
            return kopf, zeilen[i:], False
        # Produktion «Affabulazione oder Der Königsmord, Theaterstück von Pier Paolo Pasolini» / «Szenarium,
        # Aktenvermerk über Proben, Besetzungsliste» (VII.200.): die Zeile mit den Unterlagen ist Inhalt
        letztes_v = vorher.text.rstrip().split()[-1] if vorher.text.split() else ""
        vt_u = vorher.text
        if i == 1 and " von " in vt_u and (letztes_v[:1].isupper() or letztes_v.endswith(")")) \
                and not letztes_v.endswith((",", "-", "–", ":", "/")) and UNTERLAGEN_RE.match(z.text) \
                and vt_u.count("„") <= vt_u.count("“") and vt_u.count("«") <= vt_u.count("»") \
                and vt_u.count("(") <= vt_u.count(")") and vt_u.count('"') % 2 == 0:
            # (nicht im offenen Zitat «„Versuche mit … Betäubungsmitteln.» / «Entwurf einer Resolution …“», VII.423.)
            return kopf, zeilen[i:], False
        # kurzer Titel mit Doppelpunkt am Ende: was folgt, ist die Liste («Zeitungsausschnitte:» / «Franz Schwyzer,
        # Kaufmann, Shanghai …», «FOTOS wie folgt:» / «Fotos von Nr. 274 …», VII.191.)
        #   – oder es folgt eine Aufzählung («Blutspuren 5: Richard III.:» / «Besetzungsliste, Bühnenpläne …»),
        #   nicht aber ein Untertitel («Zürcher Freilager A.G.:» / «Gewährung einer Hypothek») oder in Anführung
        vt = vorher.text.rstrip()
        # (nicht bei «…, in:» / «Schweizerische Ärztezeitung …» (Zitat, VII.423.), «Bach: Prismen, Sergej
        # Rachmaninow:» / «Sonate, Suite …» (Werkliste mit mehreren «:»), offener Klammer «[Peter Schlegel:»
        # (VII.12.B.), wenn erst die Folgezeile das Datum trägt («Akten zu Liegenschaften (2):» / «Vermietung, … ¦
        # 1873 bis 1902», VII.24.), und nicht vor nur einer einzigen Zeile («Fotografie (…):» / «Villa Diana
        # Thalwil, untere grosse Grotte», VII.455.))
        if doppelpunkt and i == 1 and vt.endswith(":") and z.text[:1].isupper() and not ist_aufzaehlung(vorher) \
                and vt.count("„") <= vt.count("“") and vt.count("«") <= vt.count("»") and vt.count("(") <= vt.count(")") \
                and vt.count("[") <= vt.count("]") and ":" not in vt[:-1] and not re.search(r"\bin:$", vt) \
                and not (z.datum and not vorher.datum and _allein_vor_absatz(zeilen, i)) \
                and (len(vorher.worte) <= 3 or len(zeilen) - i >= 2) \
                and (len(vorher.worte) == 1 or not re.search(rf"{JAHR}\s*(?:[-–]|bis)\s*{JAHR}\s*$", z.text.strip())) \
                and not re.match(r"\S*[.:]\d", z.worte[0].text) and len(vorher.worte) <= 8 \
                and (len(vorher.worte) == 1 or len(vorher.worte) <= 3 and vorher.worte[0].text.isupper()
                     or re.search(r",\s|;\s|\s/\s", z.text)
                     # Liste datierter Einträge («5.1. Persönliche Dokumente:» / «Kursausweis … ¦ (1923)», «… Zürich
                     # (1928)», «Heft … (1937)», VII.239.; «1.3. Trauscheine, Familienscheine:» / «… (1765)», VII.388.)
                     or sum(1 for x in zeilen[i:] if re.search(
                         r"\(\s*(?:ca\.\s*)?\d{4}(?:\s*[-–/]\s*\d{2,4})?\s*\)\.?$", x.text.strip())) >= 2
                     # dichte Liste datierter Einträge («b) Lehrer 1832-1933:» / «Arbeitslehrerinnen … ¦ 1877-1932» /
                     # «Besoldungen ¦ 1841-1932», VI.SB.)
                     or z.datum and not _allein_vor_absatz(zeilen, i) and zeilen[i + 1].datum):
            return kopf, zeilen[i:], False
        # fetter Titel, darunter eine normale Beschreibungszeile mit eigenem Datum bzw. eingerückt («6. Akten betr.
        # Übergabe des Nachlasses ans Stadtarchiv Zürich» fett / «Korrespondenz und Verzeichnis … ¦ 2003‒2011»,
        # VII.380.): die Beschreibung ist Darin
        if i == 1 and all("Bold" in w.font for w in vorher.worte) and not any("Bold" in w.font for w in z.worte) \
                and (z.datum or z.x0 > vorher.x0 + 8) and not (z.text[:1] in "(„«\"'[" or z.text[:1].islower()
                                                               or vorher.text.rstrip()[-1:] in ",-–/&+(:"):
            # (nicht die Fortsetzung «(Generalversammlung, Vorstand, Kommissionen)», VII.150.)
            return kopf, zeilen[i:], False
        # eigene Datumsspalte: eigener Eintrag («Protokolle:» / «Protokoll der Munizipalität ¦ 1799-1803») –
        # ausser die Zeile setzt den Titel fort («… seit 1970» / «Sozialamt ¦ 1961–1985», IV.A.54.)
        if z.datum and zeilen[0].datum and (vorher.text.rstrip().endswith(":")
                                            or not datumszeile_setzt_fort(zeilen, i, rand)):
            return kopf, zeilen[i:], False
        if a is None and not ist_umbruch(vorher, z, " ".join(k.text for k in kopf), rand):
            return kopf, zeilen[i:], False  # Seitenwechsel ohne Fortsetzung
        kopf.append(z)
    return kopf, [], False


# Personenname vor einem Werk «Benjamin Britten: …», «Erns von Dohnányi: …» (am Anfang oder nach Komma/Strichpunkt)
WERKNAME_RE = re.compile(r"(?:^|[,;]\s)(?:[A-ZÄÖÜ][\w'’\-.]+\s(?:(?:von|van|de|di|da|del|der|du|le|la)\s)?){1,3}"
                         r"[A-ZÄÖÜ][\w'’\-]+:\s")


def teile_langen_titel(titel: str) -> tuple[str, list[str]]:
    """Sehr lange Titel am ersten «: » teilen («Matinee vom 16. März 1975: biografische Texte …»)."""
    if len(titel) <= TITEL_MAX or NAMENSEINTRAG_STRENG_RE.match(titel):
        return titel, []
    # «Sonntagsmatinee: Hannah Arendt und Martin Heidegger, Koproduktion mit …: Korrespondenz, Protokoll …» (VII.200.):
    # nach dem Doppelpunkt folgt die Liste der Unterlagen
    m = re.search(rf":\s+(?={UNTERLAGEN_DOPPELPUNKT}\w*,)", titel)
    if m and m.start() >= 15:
        vorn = titel[:m.start()]
        if vorn.count("(") == vorn.count(")") and vorn.count("„") == vorn.count("“"):
            return vorn.strip(), [titel[m.end():].strip()]
    if NAMENSEINTRAG_RE.match(titel):
        return titel, []
    # Werkliste «Benjamin Britten: Simple Symphony, Erns von Dohnányi: Variationen …» (VII.12.B.) bleibt ganz
    if len(WERKNAME_RE.findall(titel)) >= 2:
        return titel, []
    m = re.search(r":\s", titel)
    if m and 15 <= m.start() <= 150:
        return titel[:m.start()].strip(), [titel[m.end():].strip()]
    return titel, []


def ist_verweis(text: str) -> bool:
    return re.match(r"^\[?(siehe|vgl\.)\b", text, re.I) is not None


def _in_schachteln(nr: str, schachteln: str) -> bool:
    """Steht die Schachtel nr in der Angabe «42», «42-43» oder «55-61, 68-73»?"""
    if nr == schachteln:
        return True
    if not nr.isdigit():
        return nr in [x.strip() for x in schachteln.split(",")]
    for teil in schachteln.split(","):
        m = re.fullmatch(r"\s*(\d{1,4})\s*(?:-\s*(\d{1,4}))?\s*", teil)
        if m and int(m.group(1)) <= int(nr) <= int(m.group(2) or m.group(1)):
            return True
    return False


def schachtel_liste(werte: list[str]) -> str:
    """Schachteln einer Einheit knapp: «8», «9-11», «12-14», «14» -> «8-14»; «138», «150», «151-152» ->
    «138, 150-152». Nicht rein numerische Angaben bleiben als Liste."""
    nummern: set[int] = set()
    for w in werte:
        m = re.fullmatch(r"(\d{1,4})(?:-(\d{1,4}))?", w)
        if not m or (m.group(2) and not int(m.group(1)) <= int(m.group(2)) <= int(m.group(1)) + 2000):
            return ", ".join(dict.fromkeys(werte))  # «69/70», «12a» oder ein verdrehter Bereich: wörtlich
        nummern.update(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1))  # auch «163-360» (V.G.c.50.)
    teile, folge = [], sorted(nummern)
    a = b = folge[0]
    for n in folge[1:] + [None]:
        if n is not None and n == b + 1:
            b = n
            continue
        teile.append(str(a) if a == b else f"{a}-{b}")
        if n is not None:
            a = b = n
    return ", ".join(teile)


def verarbeite(v: Vorkommen, e: Einheit, rand: float, rand_spalte: float | None = None) -> None:
    # Hat die Einheit eine Datumsspalte, ist die Textspalte schmal (Word-Tabelle): Zeilen brechen dann
    # schon am Rand dieser Spalte um, nicht erst am rechten Seitenrand.
    if rand_spalte and v.zeilen and (v.titel_neben or any(z.datum or z.umfang for z in v.zeilen)):
        rand = min(rand, rand_spalte)  # titel_neben: Datum auf der Signaturzeile, Titel daneben (VII.416.: 1.1.22.)
    doppelpunkt = e.art == "knoten" and not v.aus_marke
    # Teil mit Unterlagen nach einem Tabulator auf der Titelzeile («… Drama von William Shakespeare ⟨26 pt⟩ Briefe,» /
    # «Aufführungsfotos», «Verschiedene Projekte 1985/86 ⟨24 pt⟩ Korrespondenz», VII.200.): sie sind Inhalt
    tab_z = None
    if e.art == "teil" and v.zeilen and not v.titel_bis and not v.titel_vorgabe and len(v.zeilen[0].worte) >= 3:
        z0 = v.zeilen[0]
        for k in range(2, len(z0.worte)):
            if z0.worte[k].x0 - z0.worte[k - 1].x1 > 15 \
                    and re.match(UNTERLAGEN_TEIL, " ".join(w.text for w in z0.worte[k:])):
                z_a = Zeile(z0.seite, z0.top, z0.bottom, z0.worte[:k], z0.datum, z0.umfang, z0.schachtel, z0.spalten)
                tab_z = Zeile(z0.seite, z0.top, z0.bottom, z0.worte[k:])
                v.zeilen = [z_a, tab_z] + v.zeilen[1:]
                break
    if v.titel_bis and 0 < v.titel_bis < len(v.zeilen):
        kopf, rumpf, rumpf_aufz = kopf_und_rumpf(v.zeilen[:v.titel_bis], rand, doppelpunkt)
        rumpf, rumpf_aufz = rumpf + v.zeilen[v.titel_bis:], rumpf_aufz and bool(rumpf)
    else:
        kopf, rumpf, rumpf_aufz = kopf_und_rumpf(v.zeilen, rand, doppelpunkt)
    if tab_z is not None and any(x is tab_z for x in kopf):
        k_t = next(n for n, x in enumerate(kopf) if x is tab_z)
        kopf, rumpf, rumpf_aufz = kopf[:k_t], kopf[k_t:] + rumpf, False
    e.beginnt_mit_punkt = bool(v.zeilen) and ist_aufzaehlung(v.zeilen[0])
    e.strichliste = any(ist_aufzaehlung(z) for z in v.zeilen)
    v.kopf_ids = {id(z) for z in kopf}
    # Die Datumsspalte der Titelzeile ist der Zeitraum der Einheit, ihre Schachtelspalte die Schachtel;
    # Spaltenangaben aller anderen Zeilen gehören zu deren Eintrag im Darin
    if v.datum:
        quelle = v.zeilen[0] if v.zeilen and v.zeilen[0].datum == v.datum else None
    elif v.titel_vorgabe:
        quelle = None  # alle Zeilen sind Darin: ihre Spaltendaten gehören zu den Einträgen
    else:
        quelle = next((z for z in kopf if z.datum), None)
    ohne = {(id(quelle), "datum")} if quelle is not None else set()
    # weitere Zeilen der Datumsspalte im Titelblock gehören zum Zeitraum der Einheit, nicht in den Titel
    weitere = list(v.weitere_daten)
    if quelle is not None and quelle in kopf:
        q = kopf.index(quelle)
        for k in range(q + 1, len(kopf)):
            z = kopf[k]
            if z.datum and not datumszeile_setzt_fort(kopf, k, rand):
                break  # eigener Eintrag mit eigenem Datum (VII.179.: «Zuteilungen ¦ 1416-1527»)
            if not z.datum and not ist_umbruch(kopf[k - 1], z, " ".join(x.text for x in kopf[:k]), rand):
                break
            if z.datum:
                weitere.append(z.datum)
                ohne.add((id(z), "datum"))
    for z in v.zeilen:  # die eigene Schachtel bzw. der eigene Umfang steht schon in «Schachtel-Nr.»/«Umfang»
        if z.schachtel and (z.schachtel == v.schachtel or z is v.zeilen[0] and v.schachtel
                            and re.fullmatch(rf"{re.escape(z.schachtel)}-\d+", v.schachtel)):
            ohne.add((id(z), "schachtel"))
        if z.umfang and z.umfang in v.umfang:
            ohne.add((id(z), "umfang"))
    titel, darin = "", []
    if v.titel_vorgabe:  # Mappe/Schachtel ohne eigenen Titel oder ganzer Bestand: alle Zeilen sind Darin
        titel, darin = v.titel_vorgabe, baue_eintraege(v.zeilen, rand, ohne=ohne)
        kopf, rumpf, v.kopf_ids = [], [], set(v.vorgabe_ids)
    elif kopf and TEIL_NUR_RE.match(kopf[0].text.strip()):
        e.teil_nr = int(TEIL_NUR_RE.match(kopf[0].text.strip()).group(1))
        darin = baue_eintraege(kopf[1:], rand, ohne=ohne)
    elif kopf:
        logisch = baue_eintraege(kopf, rand, inline_teilen=False, unterzeilen=False, ohne=ohne)
        # kurzer Rest («Brecht») nach hartem Umbruch gehört noch zum Titel – nicht aber eine eigene
        # Tabellenzeile («III. Zunft-Rechnungen ¦ 1565-1910» / «51 Zunft-Rechnungen ¦ 1565-1600»)
        if len(logisch) == 2 and len(logisch[1].split()) <= 2 and not NAMENSEINTRAG_RE.match(logisch[1]) \
                and not logisch[0].endswith((".", ":")) and not re.match(r"\d", logisch[1]) \
                and not any(z.datum or z.umfang for z in kopf[1:]):
            logisch = [logisch[0] + " " + logisch[1]]
        erste_ist_name = NAMENSEINTRAG_RE.match(logisch[0]) is not None
        if e.art == "knoten" or v.aus_marke:
            if len(logisch) >= 2 and erste_ist_name and ist_namensliste(logisch) \
                    and sum(1 for x in logisch if NAMENSEINTRAG_RE.match(x)) >= 2:
                # (mindestens zwei Einträge «Name: Werk» – nicht «Reisebericht: Besuch beim Barden …», VII.146.)
                darin = logisch  # «6.63.1.» besteht nur aus einer Liste – Titel wird übernommen
            else:
                titel, darin = logisch[0], teile_inline(logisch[1:])
        else:
            geflickt, _ = flicke_listen(logisch)
            if len(geflickt) == 1:
                titel = geflickt[0]
            elif not NAMENSEINTRAG_RE.match(geflickt[0]) and ist_namensliste(geflickt[1:]):
                titel, darin = geflickt[0], geflickt[1:]  # Überschrift + Liste ohne Leerzeile
            elif (ist_namensliste(geflickt) and sum(1 for g in geflickt if NAMENSEINTRAG_RE.match(g)) >= 2) \
                    or sum(1 for g in geflickt if KLAMMEREINTRAG_RE.match(g)) >= max(2, 0.6 * len(geflickt)):
                # (mindestens zwei «Name: Werk» – nicht «Engelchens Sturmlied, Theaterstück von Harald Kuhlmann:
                # Korrespondenz, …» mit einer Zeile Inhalt, VII.200., oder «Seeuntersuchungen: Walensee», V.F.c.204.)
                darin = teile_inline(geflickt)  # Kopf ist eine Liste (Rollenbücher/Fotos einer Schachtel)
            else:  # «124 Gerlafingen Escher Wyss & Cie …» / «Dampfturbinenfundamente»: eigener Titel
                titel, darin = geflickt[0], teile_inline(geflickt[1:])
    if v.teil_nr and not e.teil_nr:
        e.teil_nr = v.teil_nr
    m = TEIL_ZEILE_RE.match(titel)
    if m and not e.teil_nr and e.art == "teil":
        e.teil_nr = int(m.group("nr"))
    m_offen = re.search(r"(?:^|(\S*[A-Za-zäöüÄÖÜß)»“\"])\s)(?:1[0-9]|20)\d\d\s?[-–]$", titel)
    if m_offen and not v.datum and not (m_offen.group(1) and MONAT_WORT_RE.match(m_offen.group(1))):
        titel = titel.rstrip(" :;,")  # «Kongresse und Tagungen 2005-»: offenes Ende bleibt für den Zeitraum (V.L.105.)
    else:
        titel = re.sub(r"\s[-–]$", "", titel).rstrip(" :;,-–")
    titel, rest = teile_langen_titel(titel)
    darin = rest + darin + baue_eintraege(rumpf, rand, erste_ist_aufzaehlung=rumpf_aufz, ohne=ohne)
    # Liste über einen Seitenwechsel: der vermeintliche Titel ist ihr erster Eintrag
    # («6.2. Calderon de la Barca, Pedro: Der Richter von Zalamea» / S. 289 «Sophokles: Antigone» …) – nicht bei
    # einer fetten Überschrift («D. Ingenieurbüro und Tiefbau (rot)» / «D.a. Akten … (Schachteln 3 und 4)», VII.308.A.)
    if titel and darin and not v.titel_vorgabe and not v.fett and (
            (NAMENSEINTRAG_RE.match(titel) and len(darin) >= 2 and ist_namensliste(darin))
                            or (KLAMMEREINTRAG_RE.match(titel)
                                and sum(1 for d in darin if KLAMMEREINTRAG_RE.match(d))
                                >= max(2 if e.art == "teil" else 3, len(darin) * 0.6))):
        # (bei einer Einheit mit eigener Signatur mindestens drei Klammereinträge: nicht «15.3. Wappen der
        # Quartiervereine (1995)» / «27 Wappen: … (rechts der Limmat)» / «A 4 Blatt, farbig (Vorrat …)», V.L.167.;
        # ein Teil nach dem Seitenwechsel schon mit zweien, VII.200. 8.3.2.12.)
        darin, titel = [titel] + darin, ""
    # «Engelchens Sturmlied, Theaterstück von Harald Kuhlmann: Korrespondenz, Aufführungsvertrag, Aktennotizen»
    # (VII.200.): nach dem Doppelpunkt folgen die Unterlagen – sie sind Inhalt, nicht Titel
    m_u = re.match(rf"(?P<t>.+?\bvon\s[^:]{{2,80}}?):\s+(?P<r>{UNTERLAGEN_DOPPELPUNKT}.*)$", titel) if titel else None
    if m_u and m_u.group("t").count("[") == m_u.group("t").count("]") \
            and m_u.group("t").count("(") == m_u.group("t").count(")"):
        titel, darin = m_u.group("t"), [m_u.group("r")] + darin
    elif titel and e.art == "teil" and not NAMENSEINTRAG_STRENG_RE.match(titel):
        m_t = re.match(rf"(?P<t>.{{8,}}?):\s+(?P<r>{UNTERLAGEN_TEIL}.*)$", titel)
        if m_t:
            vorn, hinten = m_t.group("t"), m_t.group("r")
            if vorn.count("(") == vorn.count(")") and vorn.count("[") == vorn.count("]") \
                    and vorn.count("„") <= vorn.count("“") and hinten.count(")") <= hinten.count("("):
                titel, darin = vorn, [hinten] + darin
    # ebenso nach dem Premierendatum in derselben Zeile: «Der Preis von Arthur Miller (03.05.1968) Bühnenpläne und
    # Skizzen», auch mit fehlender Klammer «… Nestroy (16.09.1971 Bühnenpläne …» (VII.200.)
    m_k = re.match(rf"(?P<t>.+?\(\d{{1,2}}\.\d{{1,2}}\.\d{{4}})\)?\s+(?P<r>{UNTERLAGEN_MUSTER}.*)$", titel) \
        if titel else None
    if m_k:
        titel, darin = m_k.group("t") + ")", [m_k.group("r")] + darin
    darin = [d for d in darin if d.strip()]
    darin, geflickt = flicke_listen(darin)
    if geflickt:
        e.hinweise.append("Verschobene Zeilenumbrüche in Listen repariert – Stichprobe prüfen.")
    e.titel = titel
    # Datumszeile direkt unter dem Titel («17. Oktober 1830 bis 22. Dezember 1833») ist der Zeitraum
    if darin and not v.datum and quelle is None and ist_reiner_zeitausdruck(darin[0]) \
            and finde_zeitraeume(darin[0], False):
        jahreszeilen = [d for d in darin if ist_reiner_zeitausdruck(d) and finde_zeitraeume(d, False)]
        zr_listen = vereinige([f for d in jahreszeilen for f in finde_zeitraeume(d, False)])
        if len(jahreszeilen) >= 2 and zr_listen and zr_listen.von and zr_listen.bis:
            # Jahresüberschriften einer Liste («1873» … «1968» … «1977», VII.151. 17.1.): sie bleiben im Darin,
            # der Zeitraum umfasst alle
            v.datum = f"{zr_listen.von.jahr} – {zr_listen.bis.jahr}"
        else:
            v.datum = darin.pop(0)
    for d in darin:
        (e.verweise if ist_verweis(d) else e.darin).append(d)
    if any(re.search(r"keine Unterlagen", d, re.I) for d in e.darin) or re.fullmatch(r"fehl(?:t|en)\.?", titel):
        e.hinweise.append("Laut Findmittel keine Unterlagen vorhanden.")
    e.schachtel, e.schachtel_geerbt = v.schachtel, v.schachtel_geerbt
    if (not e.schachtel or e.schachtel_geerbt) and not v.titel_vorgabe:
        # Schachtel nur bei den Einträgen («I) URKUNDEN» / «Ordnung über die Verwaltung … ¦ 1758 ¦ 1», VII.191.):
        # die Einheit liegt in diesen Schachteln (beim Eintrag im Darin bleibt sie zusätzlich stehen); eine
        # weitergezogene Schachtel gilt nur, wenn die erste Schachtel erst mitten im Inhalt steht
        inhalt = [z for z in v.zeilen[1:] if z.text.strip()]
        boxen = list(dict.fromkeys(z.schachtel for z in inhalt if z.schachtel))
        erste = next((k for k, z in enumerate(inhalt) if z.schachtel), 0)
        if boxen and e.schachtel and any(z.datum or ist_aufzaehlung(z) for z in inhalt[:erste]):
            boxen = list(dict.fromkeys([e.schachtel] + boxen))  # Einträge vor der ersten Schachtel: in der alten
        if boxen:
            e.schachtel, e.schachtel_geerbt = schachtel_liste(boxen), False
    elif e.schachtel and e.schachtel.isdigit() and not v.titel_vorgabe:
        # eigene Schachtel und lückenlos anschliessende Schachteln in den Inhaltszeilen: «C) Bahnhoferweiterung 1946 ¦
        # Schachtel 9» / «Bahnhoferweiterung ¦ Schachtel 10» … «Schachtel 13» (V.G.c.107.) – die Einheit liegt in 9-13
        boxen = [b for b in dict.fromkeys(z.schachtel for z in v.zeilen[1:] if z.text.strip() and z.schachtel)
                 if b != e.schachtel]
        folge = [int(e.schachtel)] + [int(b) for b in boxen if b.isdigit()]
        if boxen and len(folge) == len(boxen) + 1 and all(b == a + 1 for a, b in zip(folge, folge[1:])):
            e.schachtel = schachtel_liste([e.schachtel] + boxen)
    e.umfang = v.umfang
    e.behaelter = v.typ == "behaelter"
    e.hinweise.extend(v.hinweise)
    datum = v.datum or (quelle.datum if quelle is not None else "")
    if weitere:  # weitere Zeilen der Datumsspalte, auch ohne Datum in der Titelzeile
        datum = " / ".join([d for d in [datum] + weitere if d])
    if datum:
        if UNDATIERT_RE.search(datum) and not finde_zeitraeume(datum, klammern_ignorieren=False):
            e.undatiert = True
        else:
            zr = vereinige(finde_zeitraeume(datum, klammern_ignorieren=False))
            if zr:
                zr.original = datum
                e.spalten_zeitraum = zr
    # Datumsspalten der Einträge im Darin gehören auch zum Zeitraum der Einheit; sie bleiben zusätzlich beim Eintrag
    # stehen («Personendossiers 1886» / «Nüssli, Emil … ¦ 1886 – 1928», VII.158.; «Schachtel 302 ¦ 1958» / «Stucki …
    # ¦ 1943», VII.191.; Teile mit mehreren Datumsblöcken, VII.151.)
    # (nicht Verweise und Fortsetzungsnotizen «… 1794-1806 siehe V.H. b.4.», «(Fortsetzung im Bestand Schulamt …
    # 1812 – 1833)», III.R./III.Q., und keine Fussnoten)
    fuss = re.compile(r"Fussnote \d+:")
    # Verweis auch über zwei Zeilen: «Schülerinnenverzeichnis … ¦ 1790-1797» / «siehe Abteilung V.H. b.3.» (III.R.)
    # Ein zusätzlicher Hinweis «siehe auch …», «vgl. …» macht aus dem Eintrag keinen Verweis: die Unterlagen sind hier
    # («- Protokolle der Vorsteherschaft ¦ 2000 – 2001» / «Siehe auch Akten und Korrespondenz.», VII.371.; «1988 - 2001,
    # 4. April 2007. Maschinenschriftliches Manuskript; siehe» / «auch Sign. VII. 298.7.», VII.298.) – nur der Text ab
    # dem Hinweis zählt nicht
    verweis, auch_ab = set(), {}
    for k, z in enumerate(v.zeilen):
        if not VERWEIS_ZEILE_RE.search(z.text):
            continue
        naechste = v.zeilen[k + 1].text.lstrip() if k + 1 < len(v.zeilen) else ""
        m_a = VERWEIS_AUCH_RE.search(z.text)
        if m_a is None and re.search(r"\bsiehe\s*$", z.text, re.I) and re.match(r"auch\b", naechste, re.I):
            m_a = re.search(r"\bsiehe\s*$", z.text, re.I)
        if m_a is not None and not VERWEIS_ZEILE_RE.search(z.text[:m_a.start()] + " " + z.text[m_a.end():]):
            auch_ab[id(z)] = m_a.start()
            if m_a.group(0).lower().startswith("siehe") and not re.search(r"auch", m_a.group(0), re.I) \
                    and k + 1 < len(v.zeilen):
                auch_ab[id(v.zeilen[k + 1])] = 0  # «auch Sign. …» auf der nächsten Zeile gehört zum Hinweis
            continue
        verweis.add(id(z))
        # (auch «Die Rechnungen … 1773-1831 sind in den Bestand Schulamt,» / «V.H. b.2., eingegliedert.», III.Q.)
        if k and (z.text[:1].islower() or re.match(r"(?:siehe|s\.\s?auch|vgl\.)\b", z.text, re.I)
                  or v.zeilen[k - 1].text.rstrip().endswith(",")) and id(v.zeilen[k - 1]) not in v.kopf_ids:
            verweis.add(id(v.zeilen[k - 1]))
    alle_z = [z for z in v.zeilen if id(z) not in verweis and not fuss.match(z.text)]

    def todesjahr(d: str, text: str) -> str:
        """Nachruf mit Lebensdaten («Nachruf Edouard Chardon ¦ 1882 - 1945», VII.190.): nur das Todesjahr – nicht
        bei einer kurzen Laufzeit, in der ein Nachruf nur vorkommt («Städtebau …, mit Plänen und Nachruf auf Dr.» /
        «Hermann Fietz ¦ 1928 – 1938», V.B.c.59.)."""
        m_n = re.match(rf"^.*?({JAHR})\s*[–-]\s*(?=({JAHR}))", d)
        if m_n and NACHRUF_RE.search(text) and int(m_n.group(2)) - int(m_n.group(1)) >= 20:
            return d[m_n.end():]
        return d
    darin_daten = [todesjahr(z.datum, z.text) for z in alle_z if z.datum and z is not quelle
                   and (id(z), "datum") not in ohne and not _ist_jubilaeum(z.text, z.datum)]
    # ebenso reine Jahreszeilen einer chronologischen Liste im Darin («1988 – 1989» / «Akten betreffend …», VII.151.;
    # auch das Jahr, das ein umbrochenes Datum abschliesst) – aber keine Satzenden und halben Bereiche; Lebensdaten
    # unter einem Nachruf zählen nur mit dem Todesjahr («Todesanzeige und Denkschrift: In Memoriam Hans Fretz» /
    # «1863 – 1925», VII.12.B.)
    vorher_z = {id(z): v.zeilen[k - 1] if k else None for k, z in enumerate(v.zeilen)}
    jahreszeilen = {id(z) for z in alle_z if id(z) not in v.kopf_ids and not z.datum
                    and _ist_jahreszeile(z, vorher_z[id(z)])}
    #   (nur eine einzelne Jahreszeile – nicht eine chronologische Liste «1947 – 1968» / «1963 – 1965» / … unter
    #   «Korrespondenz und Akten enthalten u. a. Todesanzeigen …», VII.151. 7.5.1.)
    nach_z = {id(z): v.zeilen[k + 1] if k + 1 < len(v.zeilen) else None for k, z in enumerate(v.zeilen)}
    darin_daten += [todesjahr(z.text.strip(), (vorher_z[id(z)].text + " " if vorher_z[id(z)] is not None
                                               and not (nach_z[id(z)] is not None and id(nach_z[id(z)]) in jahreszeilen)
                                               else "") + z.text)
                    for z in alle_z if id(z) in jahreszeilen]
    funde = [f for d in darin_daten for f in finde_zeitraeume(d, klammern_ignorieren=False)
             if not (f.von and f.bis and f.von.schluessel() > f.bis.schluessel(ende=True))]  # «1995-1897»
    zr_darin = vereinige(funde) if funde else None
    if zr_darin and zr_darin.von:
        zr_darin.original = ""
        e.darin_spalte, e.darin_funde = zr_darin, funde
        # allein trägt die Spalte nur, wenn die meisten Einträge ein Spaltendatum haben – nicht ein einzelnes
        # Spaltendatum unter 2000 Briefen mit dem Datum im Text (VII.142. 1.6.3.); gezählt werden die Einträge
        eintraege = [d for d in e.darin if not d.startswith("Fussnote ")]
        e.darin_spalte_traegt = len(darin_daten) >= 0.5 * max(1, len(eintraege))
        # Jahre im Text der Zeilen ohne Spaltendatum («1987+1988», «1919 - 1934*», «NZZ 2.6.1975», «… Revisionsberichte
        # 1934 – 1996,» / «2006 – 2017»): sie ergänzen die Spalte als Schätzung. Laufnummern nummerierter Dossiers
        # am Zeilenanfang («144 Anschaffung von Bluttransportwagen», V.F.c.150.) sind keine Jahre.
        # – nur Einträge ohne Spaltendatum: Folgezeilen eines datierten Eintrags («… bei Beginn der Amtsperiode
        # 1942 – 1946 ¦ 1942», VII.76.; Buchtitel «… Betriebszeit: April 1990 bis März 1991“ ¦ 1991», VII.423.), und
        # keine Übergabe-, Zuordnungs- oder Archivvermerke («… am 24. März 2017 … dem Stadtarchiv übergeben»,
        # VII.388.; «bis 2006 unter der Archivsignatur», VII.409.) oder Spielzeit-Überschriften (VII.209.)
        #   Die Datumsspalte steht auf der ersten Zeile eines Eintrags; als Folgezeile gilt nur, was danach kommt und
        #   klar weiterläuft (eingerückt, klein oder mit Anführungszeichen beginnend, nach Trennstrich oder Komma) –
        #   sonst ist es eher ein eigener Eintrag ohne Datum («Finanzinspektorat, … Prüfungen 1983+1984», V.C.c.81.;
        #   «Verschiedene fremde Inserate 1947-1954 Sch. 52» vor «Saks Fifth Avenue ¦ 1956», VII.409.)
        rumpf_z = [z for z in v.zeilen if id(z) not in v.kopf_ids and z.text.strip()]
        datiert = set()
        for k, z0 in enumerate(rumpf_z):
            if not (z0.datum and (id(z0), "datum") not in ohne):
                continue
            for n in range(k + 1, len(rumpf_z)):
                z, vor = rumpf_z[n], rumpf_z[n - 1]
                t, a_z = z.text.lstrip(), abstand(vor, z)
                if z.datum or ist_aufzaehlung(z) or ist_aufzaehlung_mit_marke(z) \
                        or (a_z is not None and a_z > ABSATZ_ABSTAND) \
                        or not (z.x0 > z0.x0 + 4 or t[0].islower() or t[0] in "„‚\"'«»‹›([–-,;:/"
                                or vor.text.rstrip().endswith(("-", ",", "„", "‚", "(", "/", "–"))):
                    break
                datiert.add(id(z))
        #   Vermerke auch über zwei, drei Zeilen («Die Bücher wurden am 24. März 2017 von Frau Barbara» / «von Beust
        #   dem Stadtarchiv übergeben.»)
        for k in range(len(rumpf_z)):
            teile_v = [x.text for x in rumpf_z[k:k + 3]]
            m_v = VERMERK_RE.search(" ".join(teile_v))
            if m_v and m_v.start() < len(teile_v[0]):
                pos = 0
                for x, t in zip(rumpf_z[k:k + 3], teile_v):
                    if pos <= m_v.end():
                        datiert.add(id(x))
                    pos += len(t) + 1
        ohne_z = [z for z in alle_z if not z.datum and id(z) not in jahreszeilen and z is not quelle
                  and id(z) not in datiert and not VERMERK_RE.search(z.text)
                  and not SPIELZEIT_KOPF_RE.fullmatch(z.text.strip())]
        nummern = [int(m.group(1)) for z in ohne_z for m in [re.match(r"(\d{1,4})[a-z]?\.?\s+\S", z.text)] if m]
        laufnummern = len(nummern) >= 3 and min(nummern) < 1000
        texte_c = [z.text[:auch_ab[id(z)]] if id(z) in auch_ab else z.text for z in ohne_z]  # ohne «siehe auch …»
        # ohne eindeutige Lebensdaten «(-1838)» («Ludwig Heinrich Friedrich von Podewils (-1838)» / «Vertrag … ¦ 1810»,
        # VII.388.)
        texte_c = [LEBENSDATEN_KLAMMER_RE.sub(" ", t) for t in texte_c]
        e.darin_ohne_spalte = "\n".join(
            re.sub(r"^\d{1,4}[a-z]?\.?\s+", "", t) if laufnummern else t for t in texte_c)
    elif darin_daten and not e.spalten_zeitraum and all(UNDATIERT_RE.search(d) for d in darin_daten):
        e.undatiert = True  # «o.D.» in der Datumsspalte der Beschreibungszeile (VII.423.)
    e.undatiert = e.undatiert or bool(UNDATIERT_RE.search(titel))


BEHAELTER_RE = re.compile(r"^(Schachtel|Mappe|Karton|Ordner|Kassette|Couvert|Umschlag|Bündel|Paket)\s+(?:Nr\.?\s*)?"
                          r"(\d{1,4}[a-z]?|[IVXL]{1,6})(?=$|[\s:.,;–-])[:.,;]?")
BEHAELTER_ENDE_RE = re.compile(r"^(?P<titel>.+?)\s+(?P<label>Schachteln?|Mappen?|Kartons?|Ordner)\s+(?:Nr\.?\s*)?"
                               r"(?P<nr>\d{1,4}[a-z]?)(?P<weitere>(?:\s*(?:\+|–|-|,|und|bis)\s*\d{1,4}[a-z]?)*)\s*$")
POSTEN_RE = re.compile(r"^(?:\d{1,3}[.)]|[a-z]\)|[-–•])\s")  # «1. Quell- und …», «a) …», «- …»
# mehrere Behälter in einer Marke: «Schachteln 8 und 9» / «Bilder» (VII.189.)
BEHAELTER_MEHRERE_RE = re.compile(r"^(Schachteln|Mappen|Kartons|Ordner)\s+(\d{1,4}[a-z]?)\s*(?:und|\+|&|,|bis|-|–)\s*"
                                  r"(\d{1,4}[a-z]?)(?=$|[\s:.,;])[:.,;]?")


def _grundschrift(zeilen: list[Zeile]) -> float:
    groessen = Counter(round(w.size) for z in zeilen for w in z.worte)
    return groessen.most_common(1)[0][0] if groessen else 12


def ohne_spaltenkoepfe(text: str) -> str:
    """«Friedhöfe Jahr Fach Mappe Allg. Nr.» -> «Friedhöfe» (Sachgruppe mit Tabellenkopf in einer Zeile)."""
    worte = text.split()
    while len(worte) > 1 and worte[-1].strip(".,:;/()").lower() in KOPFWORTE:
        worte.pop()
    return " ".join(worte)


def _ist_ueberschrift(z: Zeile, grund: float) -> bool:
    text = z.text.strip()
    return (z.x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG and len(text) <= 150 and not ist_aufzaehlung(z)
            and (max(w.size for w in z.worte) >= grund + 1.5 or all("Bold" in w.font for w in z.worte))
            and not TABELLENKOPF_RE.match(text) and not DETAIL_RE.fullmatch(text) and "Stadtarchiv" not in text
            and text.strip(" :").upper() not in VERZEICHNISWORT)


def baue_behaelter(zeilen: list[Zeile], info: dict) -> list[Vorkommen]:
    """Findmittel ohne Signaturen, gegliedert nach Mappen/Schachteln («Mappe 3», «Schachtel 17 ¦ 1946 – 1947»):
    jede Mappe/Schachtel wird eine Einheit mit der Signatur Bestand:Nummer. Beginnt die Zählung in einem
    neuen Abschnitt («Hilfe für Strassburg …») wieder bei 1, steht der Abschnitt im Titel."""
    verbleib: list[Verbleib] = info.setdefault("verbleib", [])
    grund = _grundschrift(zeilen)
    marken, ueberschriften, ende_marken, mehrere = [], {}, {}, {}
    band_marken: list[tuple] = []
    # Tabelle mit Spaltenkopf «Mappe: Inhalt: Zeitraum:» und den Nummern in der ersten Spalte («1 - Verzeichnis der
    # Fürstäbte …», «2 - Quellen des Stadtarchivs …», V.L.88.): jede Nummer ist eine Mappe
    kopf_spalte = next(((re.sub(r"\W", "", z.worte[0].text), z.x0) for z in zeilen[:60] if z.worte
                        and re.fullmatch(r"(?:Mappe|Schachtel|Karton|Ordner):?", z.worte[0].text)
                        and len(z.worte) >= 2 and ist_tabellenkopf(z.text)), None)
    for i, z in enumerate(zeilen):
        if kopf_spalte and len(z.worte) >= 2 and re.fullmatch(r"\d{1,3}[a-z]?", z.worte[0].text) \
                and abs(z.x0 - kopf_spalte[1]) <= 3 and z.worte[1].x0 - z.worte[0].x1 >= 15:
            marken.append((i, kopf_spalte[0], z.worte[0].text, 1))
            continue
        m = BEHAELTER_RE.match(z.text.strip())
        m_band = re.fullmatch(r"Band\s+(\d{1,3})", z.text.strip())
        if m_band and z.x0 <= 160 and all("Bold" in w.font for w in z.worte):
            band_marken.append((i, "Band", m_band.group(1), 2))
            if _ist_ueberschrift(z, grund):
                ueberschriften[i] = z.text.strip()
            continue
        m2 = BEHAELTER_ENDE_RE.match(" ".join(filter(None, (z.text, z.schachtel and f"Schachtel {z.schachtel}"))))
        m3 = BEHAELTER_MEHRERE_RE.match(z.text.strip())
        if m3 and z.x0 <= 160:
            label = {"Schachteln": "Schachtel", "Mappen": "Mappe", "Kartons": "Karton"}.get(m3.group(1), m3.group(1))
            marken.append((i, label, m3.group(2), len(z.text.strip()[:m3.end()].split())))
            a, b = m3.group(2), m3.group(3)
            mehrere[i] = (f"{a}-{b}" if a.isdigit() and b.isdigit() and int(b) > int(a) else f"{a}, {b}",
                          m3.group(0).rstrip(":.,; "))
        elif m and z.x0 <= 160:
            marken.append((i, m.group(1), m.group(2), len(z.text.strip()[:m.end()].split())))
        elif m2 and _ist_ueberschrift(z, grund):
            label = "Schachtel" if m2.group("label").startswith("Schachtel") else m2.group("label").rstrip("n")
            marken.append((i, label, m2.group("nr"), 0))
            ende_marken[i] = (m2.group("titel"), (m2.group("nr") + m2.group("weitere")).strip(), m2.group("label"))
        elif _ist_ueberschrift(z, grund):
            ueberschriften[i] = z.text.strip()
    # Sammelmarke «Mappen 2 - 3 1. Überblick», deren Nummern danach auch einzeln als Marken folgen («Mappe 2 Erster
    # Teil: Zeittafel», VII.48.): eine Bereichseinheit 2-3 über den einzelnen Mappen – ihr Titel und Inhalt gehören
    # nicht zur Mappe davor; ohne Bereich («Mappen 2, 5») bleibt sie eine Inhaltszeile
    einzeln = {nr for i, _, nr, _ in marken if i not in mehrere}
    sammel: set[int] = set()
    for i in list(mehrere):
        m_b = re.fullmatch(r"(\d+)-(\d+)", mehrere[i][0])
        abgedeckt = {str(n) for n in range(int(m_b.group(1)), int(m_b.group(2)) + 1)} if m_b \
            else set(mehrere[i][0].split(", "))
        if abgedeckt & einzeln:
            if m_b and abgedeckt <= einzeln:
                sammel.add(i)
                continue
            marken = [mk for mk in marken if mk[0] != i]
            del mehrere[i]
    # zweistufig «Schachtel 1: Mappe 1: Protokollauszüge» / «Mappe 2: Korrespondenzen» … / «Schachtel 2: Mappe 1: …»
    # (V.L.72.): die Mappen zählen je Schachtel neu und stehen eingerückt – die Schachteln sind die Einheiten, die Mappen
    # ihr Inhalt
    x_sch = [zeilen[i].x0 for i, label, _, _ in marken if label == "Schachtel"]
    mappen = [(i, nr) for i, label, nr, _ in marken if label == "Mappe"]
    if len(x_sch) >= 2 and len(mappen) >= 2 and len({nr for _, nr in mappen}) < len(mappen) \
            and min(zeilen[i].x0 for i, _ in mappen) > max(x_sch) + 30:
        marken = [mk for mk in marken if mk[1] != "Mappe"]
    if len(marken) < 2:
        return []
    # «Band 1» als eigener Behälter neben «Schachtel 1», «Schachtel 2» (VII.2.): nur fett und in derselben Spalte wie
    # die übrigen Marken; Signatur «Bd.1», damit sie nicht mit Schachtel 1 zusammenfällt
    xs = [zeilen[i].x0 for i, _, _, _ in marken]
    if band_marken and all("Bold" in zeilen[i].worte[0].font for i, _, _, _ in marken):
        for bm in band_marken:
            if min(abs(zeilen[bm[0]].x0 - x) for x in xs) <= 2:
                marken.append(bm)
                ueberschriften.pop(bm[0], None)
        marken.sort()
    marken_idx = {i for i, _, _, _ in marken}

    def naechste(k: int) -> int:
        """Nächste Zeile nach k, die kein Tabellenkopf ist."""
        k += 1
        while k < len(zeilen) and (TABELLENKOPF_RE.match(zeilen[k].text.strip()) or ist_tabellenkopf(zeilen[k].text)):
            k += 1
        return k
    # Abschnitt: Überschrift direkt vor einer Marke («Hilfe für Strassburg …» / «Schachtel 1»); eine Überschrift
    # mitten im Inhalt ist eine Sachgruppe der laufenden Schachtel (V.G.c.105.: «Geologische Untersuchungen»)
    # (nicht die letzte Zeile eines Absatzes, die zufällig fett ist: «PS: Alle Turicensia …» / fett «einverleibt,
    # alle übrigen Bücher verkauft.» / «Schachtel 6», VII.189.)
    ueberschriften = {k: t for k, t in ueberschriften.items() if naechste(k) in marken_idx and not t[:1].islower()}
    # dieselbe Schachtel direkt noch einmal, ohne Abschnittsüberschrift dazwischen: «Schachtel 2: Mappe 1: …» / «Mappe 2:
    # …» / «Schachtel 2: Mappe 3: …» (V.L.72.) – die Schachtel läuft weiter, kein zweiter Teil
    marken = [mk for n, mk in enumerate(marken)
              if n == 0 or (mk[1], mk[2]) != marken[n - 1][1:3] or mk[0] in mehrere or mk[0] in ende_marken
              or marken[n - 1][0] in mehrere or any(marken[n - 1][0] < k < mk[0] for k in ueberschriften)]
    abschnitt_von: dict[int, tuple[int, str]] = {}
    for i, _, _, _ in marken:
        vorher = [k for k in ueberschriften if k < i]
        k = max(vorher) if vorher else -1
        abschnitt_von[i] = (sorted(ueberschriften).index(k) + 1 if k >= 0 else 0, ueberschriften.get(k, ""))
    je_abschnitt: dict[str, set[int]] = {}
    for i, _, nr, _ in marken:
        je_abschnitt.setdefault(nr, set()).add(abschnitt_von[i][0])
    gestaffelt = any(len(a) > 1 for a in je_abschnitt.values())
    vorkommen: list[Vorkommen] = []
    uebertrag: list[Zeile] = []  # Vorbemerkung zu den folgenden Schachteln (ins Darin der nächsten)
    uebertrag_kopf = ""
    erste = marken[0][0]
    for i in range(erste):
        verbleib.append(Verbleib(zeilen[i], "ueberschrift" if i in ueberschriften else "vorlauf"))
    for n_marke, (i, label, nr, n_worte) in enumerate(marken):
        z = zeilen[i]
        ende = marken[n_marke + 1][0] if n_marke + 1 < len(marken) else len(zeilen)
        if i in ende_marken:  # Titel vorn, Schachtel(n) am Ende der Überschrift
            titel_text, alle_nr, label_im_pdf = ende_marken[i]
            n_titel = len(titel_text.split())
            rest = Zeile(z.seite, z.top, z.bottom, z.worte[:n_titel], z.datum, z.umfang)
        else:
            rest, alle_nr = z.ab(n_worte), mehrere[i][0] if i in mehrere else nr
            if rest is not None and rest.worte[0].text in ("=", ":", "–", "-") and len(rest.worte) > 1:
                rest = rest.ab(1)  # «Schachtel 10 = grf. Schachtel mit Porträtbild der Anna Asper» (VII.189.)
        resttext = rest.text.strip() if rest else ""
        nur_datum = bool(resttext) and ist_reiner_zeitausdruck(re.sub(r"\((?:I{1,3}|IV|V)\)", "", resttext))
        # (auch eine Mappe als erster Inhalt: «Schachtel 1: Mappe 1: Protokollauszüge», V.L.72. – Titel «Schachtel 1»)
        posten = bool(resttext) and (bool(POSTEN_RE.match(resttext)) or bool(BEHAELTER_RE.match(resttext))) \
            and not nur_datum
        m_kap = re.match(r"(\d{1,2})\.\s+[A-ZÄÖÜ„\"]", resttext)
        if posten and m_kap and i + 1 < ende and zeilen[i + 1].text.strip().startswith(f"{m_kap.group(1)}.1.") \
                and not any(re.match(rf"{int(m_kap.group(1)) + 1}\.\s", zeilen[j].text.strip()) for j in range(i + 1, ende)):
            # Kapitel mit Unterkapiteln als einziger Inhalt: «Mappe 12 2. Siedlungsentwicklung» / «2.1. Zürich um 1850»
            # (VII.48.) – nicht «Schachtel 3 1. Drucksachen» / «1.1. …» / «2. Zeitungen» (V.L.71.)
            posten = False
        nr_abschnitt, abschnitt = abschnitt_von[i]
        abschnitt = re.sub(r"\s*\((?:\d+\s+)?(?:Mappen|Schachteln|Kartons|Ordner)\b[^)]*\)\s*$", "", abschnitt)
        sig_nr = alle_nr if i in sammel else nr
        if label == "Band":
            sig_nr = f"Bd.{nr}"
        v = Vorkommen((str(nr_abschnitt), sig_nr) if gestaffelt else (sig_nr,), sig_nr,
                      mehrere[i][1] if i in sammel else f"{label} {nr}", z.seite, [],
                      typ="behaelter", schachtel=alle_nr if label == "Schachtel" else (z.schachtel or None),
                      datum="" if posten else (z.datum or (resttext if nur_datum else "")))
        if i in ende_marken:  # «Korrespondenz ¦ Schachteln 5 + 6»: Angabe wörtlich im Umfang
            v.umfang.append(f"{label_im_pdf} {alle_nr}")
        elif i in mehrere:  # «Mappen 7 – 10 30 Photographien …» (VII.410.): ebenso
            v.umfang.append(mehrere[i][1])
        if i in sammel:
            v.hinweise.append(f"Sammelmarke «{mehrere[i][1]}» über den einzeln verzeichneten {label}n – als Bereich "
                              f"{alle_nr} übernommen, bitte prüfen.")
        elif alle_nr != nr:
            v.hinweise.append(f"Umfasst {label}n {alle_nr}; Signatur aus der ersten Nummer gebildet.")
        v.hinweise.append(f"Signatur aus «Band {nr}» gebildet (Findmittel ohne Signaturen, Band neben den Schachteln) – "
                          "bitte prüfen." if label == "Band" else
                          f"Signatur aus der Nummer der {label} gebildet (Findmittel ohne Signaturen) – bitte prüfen.")
        if gestaffelt and len(je_abschnitt[nr]) > 1:
            v.hinweise.append(f"{label} {nr} kommt in mehreren Abschnitten vor – Signatur doppelt, bitte prüfen.")
        # Überschrift direkt nach der Marke: Sachgruppe der Schachtel («Schachtel 17» / «Friedhöfe Jahr Fach …»)
        k_nach = naechste(i)
        kopf_nach = ""
        if k_nach < ende and _ist_ueberschrift(zeilen[k_nach], grund) and not BEHAELTER_RE.match(zeilen[k_nach].text):
            kopf_nach = ohne_spaltenkoepfe(zeilen[k_nach].text.strip()).rstrip(" :")
        klammer = bool(re.fullmatch(r"\(.*\)", resttext))  # «Schachtel 4 (27.8.82 fehlt)»: Bemerkung, kein Titel
        if resttext and not posten and not nur_datum and not klammer:
            v.zeilen = [rest]  # «Schachtel 1 Kriegsschadenfürsorge …, Akten 1943 - 1946»: eigener Titel
        else:
            marke_text = mehrere[i][1] if i in mehrere else f"{label} {nr}"  # «Schachteln 8 und 9»
            v.titel_vorgabe = (f"{abschnitt}: {kopf_nach}" if abschnitt and kopf_nach else kopf_nach
                               or (f"{abschnitt}, {marke_text}" if abschnitt else marke_text))
            v.zeilen = [rest] if rest and not nur_datum else []
            if kopf_nach:
                v.vorgabe_ids = {id(zeilen[k_nach])}
        verbleib.append(Verbleib(z, "einheit", v))
        # Vorbemerkung für die folgenden Schachteln vor ihrer ersten Marke: «JAHRESDOKUMENTATION» / «Vorbemerkungen zu
        # den Schachteln 1 bis 5 (1803 - 1892):» / «Die Jahrgänge vor 1874 umfassen …» (V.L.5.) – ins Darin der
        # folgenden Schachtel, nicht der vorigen
        if uebertrag:
            abschnitt_kopf = ""
            if re.fullmatch(r"[A-ZÄÖÜ]{6,}(?:\s+[A-ZÄÖÜ]{2,})*", uebertrag[0].text.strip()):
                abschnitt_kopf = uebertrag[0].text.strip()
                verbleib.append(Verbleib(uebertrag[0], "ueberschrift"))
                uebertrag = uebertrag[1:]
            v.zeilen.extend(uebertrag)
            for x_u in uebertrag:
                verbleib.append(Verbleib(x_u, "einheit", v))
            v.hinweise.append((f"Steht im Findmittel unter der Überschrift «{abschnitt_kopf}». " if abschnitt_kopf else "")
                              + f"Die Vorbemerkung «{uebertrag_kopf[:70]}» steht im Findmittel vor dieser {label} – hier "
                              "im Darin übernommen.")
            uebertrag, uebertrag_kopf = [], ""
        ende_inhalt = ende
        if n_marke + 1 < len(marken):
            k_vb = next((k for k in range(i + 1, ende) if re.match(r"Vorbemerkung(?:en)?\s+zu\s+den\s+(?:Schachteln|Mappen)\b",
                                                                   zeilen[k].text.strip())), None)
            if k_vb is not None:
                uebertrag_kopf = zeilen[k_vb].text.strip()
                if k_vb - 1 > i and re.fullmatch(r"[A-ZÄÖÜ]{6,}(?:\s+[A-ZÄÖÜ]{2,})*", zeilen[k_vb - 1].text.strip()):
                    k_vb -= 1  # Abschnittsüberschrift «JAHRESDOKUMENTATION» direkt davor
                uebertrag, ende_inhalt = list(zeilen[k_vb:ende]), k_vb
        letzte_marke, im_schlussteil, nach_vermerk = n_marke + 1 == len(marken), False, False
        im_stueck = False
        for j in range(i + 1, ende_inhalt):
            zz, text = zeilen[j], zeilen[j].text.strip()
            # Stück ohne Nummer in der Spalte der Marken: «Grossformate: Hedwig Strehler (Bleistiftzeichnung …); …» nach
            # dem Inhalt von «Schachtel 10 (Nachträge):» (VII.242.) – zur Zeile für den Bestand, nicht in die Schachtel
            if not im_stueck and zz.worte and abs(zz.x0 - z.x0) <= 3 and STUECK_BEHAELTER_RE.match(text):
                im_stueck = True
                v_b = info.get("_bestandszeile")
                if v_b is None:
                    v_b = info["_bestandszeile"] = Vorkommen(("Bestand",), "", "", zz.seite, [], typ="bestand")
                v_b.hinweise.append(f"Stück ohne Nummer im Findmittel («{text[:70]}», S. {zz.seite}) – hier beim "
                                    "Bestand übernommen (keine Signatur erfunden); in scope beim Bestand ergänzen oder "
                                    "von Hand als Einheit anlegen.")
            if im_stueck and zz.worte and zz.x0 >= z.x0 - 3 and not (
                    ist_schlussvermerk(text, zeilen[j - 1], zz) or SCHLUSS_DATUM_RE.match(text)
                    or ist_schlusskopf(zz, grund)):
                info["_bestandszeile"].zeilen.append(zz)
                verbleib.append(Verbleib(zz, "einheit", info["_bestandszeile"]))
                continue
            im_stueck = False
            # nach der letzten Schachtel/Mappe ein Schlussabschnitt: Überschrift «Verweise auf andere Bestände» (14 pt,
            # V.L.71.), «Bemerkungen» (fett, V.L.126.), «Hauptwerke von H. Strehler [in der Bibliothek des
            # Stadtarchivs]:» (VII.242.) oder eine Notiz zum Bestand in der Spalte der Marken, links vom eingerückten
            # Inhalt («Lagerung: 1 Normschachtel», VII.48.) – ab hier Info-Blatt, nicht Darin der letzten Schachtel
            # (auch ein Absatz zur Bestandsgeschichte nach grossem Abstand: «Die Genossenschaft wurde 1890 vom
            # Grütliverein … gegründet.» / «Der Grütliverein löste sich 1925 auf.» …, VII.124.)
            if letzte_marke and not im_schlussteil and zz.worte and zz.x0 <= SIGNATUR_SPALTE_MAX \
                    and luft(zeilen[j - 1], zz) > 40 and len(text) >= 50 and ist_prosa_bis_schluss(zeilen[j:]):
                im_schlussteil = True
            if letzte_marke and not im_schlussteil and zz.worte and zz.x0 <= SIGNATUR_SPALTE_MAX \
                    and j != k_nach and (ist_schlusskopf(zz, grund)
                                         or v.zeilen and all(x.x0 > zz.x0 + 15 for x in v.zeilen if x.worte)
                                         and luft(zeilen[j - 1], zz) > 25 and SCHLUSSNOTIZ_RE.search(text)
                                         and not ist_aufzaehlung(zz)
                                         and (zz.seite >= zeilen[-1].seite - 1 or j > len(zeilen) - 15)):
                im_schlussteil = True
            # nach einem Schlussvermerk der letzten Schachtel weitere Zeilen in der Spalte der Marken: «Archivierung
            # abgeschlossen: …» / «Briefwechsel Stehler-Ragaz: 17. Dezember 2010 / RD» / «Letzte Änderung: …» (VII.242.)
            if im_schlussteil or nach_vermerk and zz.worte and (zz.x0 <= SIGNATUR_SPALTE_MAX or zz.worte[0].size >= 13.5):
                info.setdefault("schluss", []).append(schlusszeile(zz, text))
                verbleib.append(Verbleib(zz, "schluss"))
                continue
            if kopf_nach and j == k_nach:
                n_kopf = len(kopf_nach.split())
                if n_kopf < len(zz.worte):  # «Friedhöfe | Jahr Fach Mappe Allg. Nr.»
                    verbleib.append(Verbleib(Zeile(zz.seite, zz.top, zz.bottom, zz.worte[:n_kopf]), "einheit", v))
                    verbleib.append(Verbleib(Zeile(zz.seite, zz.top, zz.bottom, zz.worte[n_kopf:]), "ueberschrift"))
                else:
                    verbleib.append(Verbleib(zz, "einheit", v))
            elif j in ueberschriften or TABELLENKOPF_RE.match(text) or ist_tabellenkopf(text) or DETAIL_RE.fullmatch(text):
                verbleib.append(Verbleib(zz, "ueberschrift"))  # auch «Detailverzeichnis» nach der Zusammenfassung
            elif ist_schlussvermerk(text, zeilen[j - 1], zz) or (j >= len(zeilen) - 15 and SCHLUSS_DATUM_RE.match(text)):
                # auch «11. Dezember 1990 / Dr. Robert Dünki» auf den letzten Zeilen (VII.222.)
                info.setdefault("schluss", []).append(text)
                verbleib.append(Verbleib(zz, "schluss"))
                nach_vermerk = letzte_marke
            elif UMFANG_RE.match(text):
                v.umfang.append(text)
                verbleib.append(Verbleib(zz, "einheit", v))
            elif _ist_ueberschrift(zz, grund) and 0 < len(ohne_spaltenkoepfe(text).split()) < len(zz.worte):
                # Sachgruppe mitten in der Schachtel mit Tabellenkopf in derselben Zeile («Kläranlagen Jahr Fach
                # Mappe Allg. Nr.», V.G.c.105.): nur die Sachgruppe ins Darin, der Kopf ist keine Inhaltszeile
                n_kopf = len(ohne_spaltenkoepfe(text).split())
                gruppe = Zeile(zz.seite, zz.top, zz.bottom, zz.worte[:n_kopf])
                v.zeilen.append(gruppe)
                verbleib.append(Verbleib(gruppe, "einheit", v))
                verbleib.append(Verbleib(Zeile(zz.seite, zz.top, zz.bottom, zz.worte[n_kopf:]), "ueberschrift"))
            else:
                v.zeilen.append(zz)
                verbleib.append(Verbleib(zz, "einheit", v))
        vorkommen.append(v)
    if info.get("_bestandszeile") is not None:
        vorkommen.append(info.pop("_bestandszeile"))
    return vorkommen


def verteile_chronologisch(behaelter: list[Vorkommen], verbleib: list[Verbleib]) -> bool:
    """Schachteln nach Jahren («Schachtel 1 Materialien 1730–1797», «Schachtel 2 … 1798–1815», …) und danach ein
    chronologisches Verzeichnis («1730 Donnstags-Nachrichten …», V.L.14.): jeder Eintrag kommt in die Schachtel
    seines Jahres (Folgezeilen mit ihm), statt alles in die letzte."""
    bereiche = []
    for v in behaelter:
        funde = finde_zeitraeume(v.zeilen[0].text) if v.zeilen else []
        if len(funde) != 1 or not (funde[0].von and funde[0].bis):
            return False
        bereiche.append((funde[0].von.jahr, funde[0].bis.jahr))
    if len(bereiche) < 2 or any(b[0] <= a[1] for a, b in zip(bereiche, bereiche[1:])):
        return False
    inhalt = [(v, z) for v in behaelter for z in v.zeilen[1:]]
    jahr_zeilen = [z for _, z in inhalt if re.fullmatch(rf"{JAHR}", z.worte[0].text) and len(z.worte) >= 2]
    if len(jahr_zeilen) < 10:
        return False
    rand = min(z.x0 for z in jahr_zeilen)
    jahr_zeilen = [z for z in jahr_zeilen if z.x0 <= rand + 3]
    innen = sum(1 for z in jahr_zeilen if bereiche[0][0] - 50 <= int(z.worte[0].text) <= bereiche[-1][1])
    if innen < 0.8 * len(jahr_zeilen):
        return False

    def ziel(jahr: int) -> int:
        for k, (a, b) in enumerate(bereiche):
            if jahr <= b:
                return k  # auch Einträge vor der ersten Schachtel («1706 …») in die erste
        return len(bereiche) - 1

    neu: list[list[Zeile]] = [v.zeilen[:1] for v in behaelter]
    k_akt = None
    ids_jahr = {id(z) for z in jahr_zeilen}
    letzte = max(k for k, (_, z) in enumerate(inhalt) if id(z) in ids_jahr)
    grund = Counter(round(w.size) for _, z in inhalt for w in z.worte).most_common(1)[0][0]
    for k_z, (v, z) in enumerate(inhalt):
        if id(z) in ids_jahr:
            k_akt = ziel(int(z.worte[0].text))
        elif k_akt is None and z.x0 <= rand + 3 and z.worte[0].text in ("–", "-") and k_z < letzte:
            k_akt = ziel(int(jahr_zeilen[0].worte[0].text))  # «– Einige Fragmente … 1586» ohne Jahr vor «1706 …»
        elif k_z > letzte and max(w.size for w in z.worte) >= grund + 1:
            k_akt = None  # nach dem Verzeichnis eine Überschrift («Anmerkung zu 1757 …»): ab hier wie bisher
        k = behaelter.index(v) if k_akt is None else k_akt
        neu[k].append(z)
    ort = {id(z): behaelter[k] for k, zs in enumerate(neu) for z in zs}
    for v, zs in zip(behaelter, neu):
        v.zeilen = zs
    for vb in verbleib:
        if vb.art == "einheit" and id(vb.zeile) in ort:
            vb.vorkommen = ort[id(vb.zeile)]
    return True


def baue_behaelter_am_ende(zeilen: list[Zeile], info: dict) -> list[Vorkommen]:
    """Listen ohne Signaturen mit Schachtelangabe am rechten Rand: je Schachtel eine Einheit Bestand:N.
    - Endet die Angabe jeweils einen Absatz (Leerzeile oder Seitenwechsel danach; V.F.c.119.: «… Offerten
      Schachtel 1»), gehören die Zeilen davor zur Schachtel; sonst beginnt sie ihre Zeilen (Tabelle mit Spalte
      «Schachtel-Nr.»: die folgenden Zeilen ohne Nummer gehören dazu).
    - Wiederholt sich die erste Zeile der Gruppen («Verschiedene Materialien des Stadtarztes», «Gerollte Pläne
      (II)»), steht sie als Vorsatz im Titel vor der zweiten.
    - Haben mehrere Tabellenzeilen nacheinander dieselbe Nummer, werden sie eine Einheit «Schachtel N»."""
    marken = [i for i, z in enumerate(zeilen) if z.schachtel and SCHACHTEL_NR_RE.fullmatch(z.schachtel)]
    if len(marken) < 2:
        return []
    verbleib: list[Verbleib] = info.setdefault("verbleib", [])
    nach = [luft(zeilen[i], zeilen[i + 1] if i + 1 < len(zeilen) else None) for i in marken]
    am_ende = sum(1 for x in nach if x > ABSATZ_ABSTAND) >= 0.8 * len(marken)
    # Tabelle mit Spaltenkopf «Akte / Dossier ¦ Schachtel-Nr.» (V.J.c.65., V.C.c.208.): die Nummer steht in der ersten
    # Zeile eines Eintrags, Folgezeilen ohne Nummer gehören zu ihr – auch wenn jede Zeile einen eigenen Absatz bildet
    if am_ende and any(re.search(r"\bSchachtel-?Nr\.?\s*$", z.text.strip()) for z in zeilen[:marken[0]]):
        am_ende = False
    if am_ende:
        gruppen, anfang = [], 0
        for i in marken:
            gruppen.append(list(range(anfang, i + 1)))
            anfang = i + 1
        rest_danach = list(range(anfang, len(zeilen)))
        erste = gruppen[0]  # Titelblock vor der ersten Gruppe: alles bis zur letzten Leerzeile darin
        schnitt = max((k for k in range(1, len(erste)) if luft(zeilen[erste[k - 1]], zeilen[erste[k]]) > ABSATZ_ABSTAND),
                      default=0)
        davor, gruppen[0] = erste[:schnitt], erste[schnitt:]
    else:
        davor, rest_danach = list(range(marken[0])), []
        gruppen = [list(range(i, marken[n + 1] if n + 1 < len(marken) else len(zeilen))) for n, i in enumerate(marken)]
    # Tabellenzeilen mit derselben Nummer zusammenfassen – auch über eingestreute Zeilen anderer Schachteln hinweg
    # (alphabetische Liste: «32 · 33-34 · 32 · 33-34», «79 · 79a · 79», V.G.c.7.)
    zusammen: list[list[list[int]]] = []
    # Tippfehler in der Schachtelspalte: eine einzelne Zeile «101» zwischen Zeilen der Schachtel 10, weit über der
    # höchsten übrigen Nummer (V.G.c.7., Schachteln 1–82) – gehört zu 10
    nummern_g = [zeilen[g[-1] if am_ende else g[0]].schachtel for g in gruppen]
    zahlen_g = [n for n in nummern_g if n and n.isdigit()]
    tippfehler: dict[int, str] = {}
    for idx in range(1, len(gruppen) - 1):
        nr, vor_nr, nach_nr = nummern_g[idx], nummern_g[idx - 1], nummern_g[idx + 1]
        if nr and vor_nr and nr.isdigit() and vor_nr == nach_nr and len(gruppen[idx]) == 1 \
                and nr.startswith(vor_nr) and len(nr) == len(vor_nr) + 1 \
                and int(nr) > max((int(n) for n in zahlen_g if n != nr), default=0) + 5:
            tippfehler[idx] = vor_nr
    tipp_hinweis: dict[str, list[str]] = {}
    for idx, g in enumerate(gruppen):
        nr = zeilen[g[-1] if am_ende else g[0]].schachtel
        if idx in tippfehler:
            tipp_hinweis.setdefault(tippfehler[idx], []).append(
                f"Schachtel «{nr}» bei «{zeilen[g[0]].text.strip()[:60]}» zwischen Zeilen der Schachtel "
                f"{tippfehler[idx]} – als {tippfehler[idx]} gelesen (Tippfehler?), bitte prüfen.")
            nr = tippfehler[idx]
        frueher = next((e for e in reversed(zusammen[-3:]) if e[0] == nr), None)
        if frueher is not None:
            frueher[1].append(g)
        else:
            zusammen.append((nr, [g]))
    for k in davor:
        text = zeilen[k].text.strip()
        verbleib.append(Verbleib(zeilen[k], "ueberschrift" if ist_tabellenkopf(text) or TABELLENKOPF_RE.match(text)
                                 else "vorlauf"))

    def kern(text: str) -> str:
        return re.sub(r"\s*\((?:[IVX]+|\d+)\)$", "", text.strip())
    ersten = Counter(kern(zeilen[g[0]].text) for _, gs in zusammen for g in gs if len(g) >= 2)
    vorkommen = []
    for nr, gs in zusammen:
        v = Vorkommen((nr,), nr, f"Schachtel {nr}", zeilen[gs[0][0]].seite, [], typ="behaelter", schachtel=nr)
        v.hinweise.append("Signatur aus der Nummer der Schachtel gebildet (Findmittel ohne Signaturen) – bitte prüfen.")
        v.hinweise.extend(tipp_hinweis.get(nr, []))
        zeilen_v = [k for g in gs for k in g]
        if len(gs) > 1:
            v.titel_vorgabe = f"Schachtel {nr}"  # mehrere Tabellenzeilen: alle ins Darin
        elif len(gs[0]) >= 2 and ersten[kern(zeilen[gs[0][0]].text)] >= 3:  # wiederkehrende Sammelbezeichnung
            g = gs[0]
            v.titel_vorgabe = f"{zeilen[g[0]].text.strip()}: {saeubere(zeilen[g[1]].text).rstrip(' :;,')}"
            verbleib.append(Verbleib(zeilen[g[0]], "einheit", v))
            verbleib.append(Verbleib(zeilen[g[1]], "einheit", v))
            v.vorgabe_ids = {id(zeilen[g[0]]), id(zeilen[g[1]])}
            zeilen_v = g[2:]
        for k in zeilen_v:
            text = zeilen[k].text.strip()
            if ist_tabellenkopf(text) or TABELLENKOPF_RE.match(text):
                verbleib.append(Verbleib(zeilen[k], "ueberschrift"))
            elif SCHLUSS_RE.match(text):
                info.setdefault("schluss", []).append(text)
                verbleib.append(Verbleib(zeilen[k], "schluss"))
            else:
                v.zeilen.append(zeilen[k])
                verbleib.append(Verbleib(zeilen[k], "einheit", v))
        vorkommen.append(v)
    for k in rest_danach:  # nach der letzten Schachtelangabe: Schlussnotizen u. Ä.
        text = zeilen[k].text.strip()
        if SCHLUSS_RE.match(text):
            info.setdefault("schluss", []).append(text)
        verbleib.append(Verbleib(zeilen[k], "schluss" if SCHLUSS_RE.match(text) else "vorlauf"))
    return vorkommen


# Abschnitt einer Bestandsbeschreibung (Titel einer nummerierten Überschrift, siehe «beschreibung» in verarbeite_pdf)
BESCHREIBUNG_RE = re.compile(r"(?:Herkunft|Provenienz|Hinweise?|Bemerkung(?:en)?|Anmerkung(?:en)?|Vorbemerkung(?:en)?|"
                             r"Einleitung|Gliederung|Ordnung|Bestandes?geschichte|Benut?zung|Zugang|Umfang|"
                             r"Inhalt(?:sübersicht)?|Literatur|Quellen|Verweise?|Abkürzungen)\b(?:\s+(?:des|der|zum|zur)\s+"
                             r"\w+)?\s*:?$")
REGISTERKOPF_RE = re.compile(r"Schachtel\(n\)|Schachteln?|Sch\.|Schachtel-?Nr\.?")
REGISTERNR_RE = re.compile(r"(\d{1,3})(?:\s*-\s*(\d{1,3}))?[,.;]?")


def baue_behaelter_aus_register(zeilen: list[Zeile], info: dict) -> list[Vorkommen]:
    """Alphabetisches Register «Titel ¦ Schachtel(n)» ohne Signaturen: «Aargau ¦ 7-10», «Alt-Zürich ¦ 66, 67»,
    «Artikel, lokalgeschichtlich ¦ 34 (Verzeichnis: 46, 6-7)» (VII.177.). Je Schachtel eine Einheit Bestand:N mit den
    Stichworten, die auf sie verweisen, im Darin (ein Bereich «7-10» gilt für jede seiner Schachteln). Was nach dem
    Register folgt, steht im Blatt Info."""
    kopf = next((k for k, z in enumerate(zeilen[:60]) if 2 <= len(z.worte) <= 6
                 and z.worte[0].text.strip(":") in ("Titel", "Stichwort", "Stichworte", "Thema", "Gegenstand", "Inhalt")
                 and any(REGISTERKOPF_RE.fullmatch(w.text) and w.x0 >= 200 for w in z.worte[1:])), None)
    if kopf is None:
        return []
    x_s = next(w.x0 for w in zeilen[kopf].worte[1:] if REGISTERKOPF_RE.fullmatch(w.text) and w.x0 >= 200)

    def eintrag(z: Zeile) -> tuple[list[str], int, int] | None:
        """Schachtelnummern ab der Spalte x_s, Index ihres ersten und hinter ihrem letzten Wort."""
        k = next((n for n, w in enumerate(z.worte) if n > 0 and abs(w.x0 - x_s) <= 6), None)
        if k is None:
            return None
        nummern, n = [], k
        while n < len(z.worte):
            m = REGISTERNR_RE.fullmatch(z.worte[n].text)
            if not m and n + 2 < len(z.worte) and z.worte[n + 1].text in ("-", "–"):
                m = REGISTERNR_RE.fullmatch(z.worte[n].text + "-" + z.worte[n + 2].text)
                if m:
                    n += 2
            if not m:
                break
            a, b = int(m.group(1)), int(m.group(2)) if m.group(2) else None
            nummern += [str(x) for x in range(a, b + 1)] if b is not None and a < b <= a + 20 else [str(a)]
            n += 1
        return (nummern, k, n) if nummern else None
    funde = [(j, e) for j in range(kopf + 1, len(zeilen)) if (e := eintrag(zeilen[j]))]
    if len(funde) < 10 or len(funde) < 0.8 * (funde[-1][0] - kopf):
        return []
    verbleib: list[Verbleib] = info.setdefault("verbleib", [])
    for z in zeilen[:kopf]:
        verbleib.append(Verbleib(z, "vorlauf"))
    verbleib.append(Verbleib(zeilen[kopf], "ueberschrift"))
    boxen: dict[str, Vorkommen] = {}
    letzte = funde[-1][0]
    for j in range(kopf + 1, letzte + 1):
        z = zeilen[j]
        e = eintrag(z)
        if e is None:  # Folgezeile eines Stichworts oder Zwischentitel: beim vorigen Stichwort
            verbleib.append(Verbleib(z, "ueberschrift"))
            continue
        nummern, k, n = e
        stichwort = Zeile(z.seite, z.top, z.bottom, z.worte[:k] + z.worte[n:], z.datum, z.umfang)
        for nr in nummern:
            v = boxen.get(nr)
            if v is None:
                v = boxen[nr] = Vorkommen((nr,), nr, f"Schachtel {nr}", z.seite, [], typ="behaelter", schachtel=nr,
                                          titel_vorgabe=f"Schachtel {nr}")
                v.hinweise.append("Signatur aus der Nummer der Schachtel gebildet (Findmittel ohne Signaturen, Darin aus "
                                  "dem alphabetischen Register «Titel ¦ Schachtel(n)») – bitte prüfen.")
            v.zeilen.append(stichwort)
            verbleib.append(Verbleib(z, "schachtel", v, wert=nr))  # die Nummer steckt in der Schachtel der Einheit
        verbleib.append(Verbleib(stichwort, "einheit", boxen[nummern[0]]))
    # nach dem Register: Notizen zum Bestand, Bearbeitervermerk – ein Absatz über ein Stück ohne Nummer («Der Bestand
    # enthält aus dem Nachlass von Paul Nussberger des weitern ein Geschäftsbuch …», VII.177.) zur Zeile für den Bestand
    bestand_v: Vorkommen | None = None
    im_stueck = False
    rest_z = zeilen[letzte + 1:]
    for k_r, z in enumerate(rest_z):
        t_r = z.text.strip()
        vor_r = rest_z[k_r - 1] if k_r else None
        if im_stueck and (luft(vor_r, z) > ABSATZ_ABSTAND or ist_schlussvermerk(t_r) or VERMERK_DATUM_RE.match(t_r)):
            im_stueck = False
        if not im_stueck and STUECK_SCHLUSS_RE.match(t_r):
            im_stueck = True
            if bestand_v is None:
                bestand_v = Vorkommen(("Bestand",), "", "", z.seite, [], typ="bestand")
            bestand_v.hinweise.append(f"Stück ohne Nummer im Findmittel («{t_r[:70]}», S. {z.seite}) – hier beim "
                                      "Bestand übernommen (keine Signatur erfunden); in scope beim Bestand ergänzen oder "
                                      "von Hand als Einheit anlegen.")
        if im_stueck:
            bestand_v.zeilen.append(z)
            verbleib.append(Verbleib(z, "einheit", bestand_v))
            continue
        info.setdefault("schluss", []).append(t_r)
        verbleib.append(Verbleib(z, "schluss"))
    return [boxen[nr] for nr in sorted(boxen, key=int)] + ([bestand_v] if bestand_v is not None else [])


def bestandstitel(koerper: list[Zeile], eintrag: dict | None) -> str:
    """Titel des Bestands: aus dem Online-Archiv («V.G.c.63. Hochbauamt. Akten, 1911-1941 (Bestand)» → «Hochbauamt.
    Akten, 1911-1941»), sonst der Titelblock in grosser Schrift oben auf der ersten Seite."""
    if eintrag and eintrag.get("titel"):
        t_k = re.sub(r"^[IVX]{1,4}\.\S*\s+", "", eintrag["titel"].strip())
        t_k = re.sub(r"\s*\((?:Teil)?[Bb]estand\)\s*$", "", t_k).strip()
        if t_k:
            return t_k
    grund = _grundschrift(koerper)
    erste_seite = koerper[0].seite if koerper else 1
    titel = []
    for z in koerper:
        if z.seite != erste_seite or max(w.size for w in z.worte) < grund + 2:
            break
        if "Stadtarchiv" not in z.text and not DETAIL_RE.fullmatch(z.text.strip()):
            titel.append(z.text)
    t = saeubere(" ".join(titel))
    if not t and eintrag and eintrag.get("titel"):
        t = re.sub(r"^\S+\s+", "", eintrag["titel"]).strip()
    return t or "Gesamtbestand"


def baue_bestandszeile(koerper: list[Zeile], start: int, info: dict, ersatztitel: str) -> list[Vorkommen]:
    """Findmittel ganz ohne Signaturen und ohne Mappen/Schachteln (reine Inhaltsliste): eine Zeile für den
    Bestand selbst mit dem ganzen Inhalt als Darin – es werden keine Signaturen erfunden."""
    verbleib: list[Verbleib] = info.setdefault("verbleib", [])
    detail = koerper[start:]
    grund = _grundschrift(detail or koerper)
    erste_seite = koerper[0].seite if koerper else 1
    titelzeilen = []
    for z in koerper:  # Titelblock: grosse Schrift zuoberst auf der ersten Seite
        if z.seite != erste_seite or max(w.size for w in z.worte) < grund + 2:
            break
        if "Stadtarchiv" not in z.text and not DETAIL_RE.fullmatch(z.text.strip()):
            titelzeilen.append(z)
    titel = saeubere(" ".join(z.text for z in titelzeilen)) or ersatztitel or "Gesamtbestand"
    v = Vorkommen(("Bestand",), "", "", detail[0].seite if detail else erste_seite, [], typ="bestand",
                  titel_vorgabe=titel)
    v.hinweise.append("Findmittel ohne Signaturen: ganzer Inhalt in einer Zeile für den Bestand – in scope beim "
                      "Bestand ergänzen, keine neue Einheit anlegen.")
    im_schluss = False  # nur in den letzten Zeilen: «Archiviert … / STADTARCHIV ZÜRICH / Dr. Robert Dünki» (VII.479.)
    for k, z in enumerate(detail):
        text = z.text.strip()
        am_ende = k >= len(detail) - 15
        if z in titelzeilen:
            verbleib.append(Verbleib(z, "einheit", v))
        elif z.seite == erste_seite and "Stadtarchiv" in text and max(w.size for w in z.worte) >= grund + 1:
            verbleib.append(Verbleib(z, "vorlauf"))
        elif TABELLENKOPF_RE.match(text) or ist_tabellenkopf(text) or DETAIL_RE.fullmatch(text):
            verbleib.append(Verbleib(z, "ueberschrift"))
        elif ist_schlussvermerk(text, detail[k - 1] if k else None, z) or (am_ende and (im_schluss and z.x0 <= SIGNATUR_SPALTE_MAX
                                                     or SCHLUSS_DATUM_RE.match(text))):
            info.setdefault("schluss", []).append(text)
            verbleib.append(Verbleib(z, "schluss"))
            im_schluss = im_schluss or am_ende
        else:
            v.zeilen.append(z)
            verbleib.append(Verbleib(z, "einheit", v))
    return [v] if v.zeilen else []


def rand_der_textspalte(vorkommen: list[Vorkommen], zusatz: list[Zeile] | None = None) -> float | None:
    """Rechter Rand der Textspalte in Einheiten mit Datumsspalte (95. Perzentil der Zeilenenden)."""
    enden = sorted([z.x1 for v in vorkommen if any(z.datum or z.umfang for z in v.zeilen) for z in v.zeilen]
                   + [z.x1 for z in zusatz or []])
    return enden[int(len(enden) * 0.95)] + 3 if len(enden) >= 10 else None


def baue_einheiten(vorkommen: list[Vorkommen], rand: float, modus: str, info: dict) -> list[Einheit]:
    # Schlüssel (Bestand, Pfad): bei Findmitteln für mehrere Bestände sind V.L.156.:1 und V.L.162.:1 verschieden
    knoten: dict[tuple, Einheit] = {}
    einheiten: list[Einheit] = []
    letzter = None
    rand_spalte = rand_der_textspalte(vorkommen, info.get("rand_zusatz"))
    for v in vorkommen:
        alt = knoten.get((v.bestand, v.pfad))
        getrennt = letzter is not None and letzter != (v.bestand, v.pfad) \
            and (letzter[0] != v.bestand or letzter[1][:len(v.pfad)] != v.pfad)
        # (nicht, wenn unter der ersten Nennung schon Untereinheiten mit Inhalt oder Datum standen: «6. Anbau eines
        # Ausstellungsraumes» mit 6.1.–6.3., danach im PDF noch einmal «5.», «6.» statt 7., 8., VII.383.)
        def mit_unter() -> bool:
            if alt not in einheiten:
                return False
            return any(u.pfad[:len(alt.pfad)] == alt.pfad and len(u.pfad) > len(alt.pfad) and u.bestand == alt.bestand
                       and (u.darin or u.spalten_zeitraum or u.undatiert)
                       for u in einheiten[einheiten.index(alt) + 1:])
        if alt is not None and getrennt and modus == "dezimal" and not alt.darin and not alt.teile_liste \
                and not alt.verweise and not mit_unter():
            # die erste Nennung war nur eine Zeile in einer Übersicht (VII.12.A.: «5.1. Theaterzettel»
            # vor dem eigentlichen Verzeichnis) – sie fällt weg, die jetzige Nennung gilt
            einheiten.remove(alt)
            del knoten[(v.bestand, v.pfad)]
            info.setdefault("uebersicht", []).append(f"{alt.anzeige} (S. {alt.seite})")
            alt.entfernt = "Übersichtszeile"
            alt = None
        if alt is None:
            e = Einheit(len(einheiten) + 1, v.pfad, v.anzeige, v.roh, v.seite, "knoten", bestand=v.bestand)
            if v.signatur_fest:
                e.doppelpunkt = v.signatur_fest
            knoten[(v.bestand, v.pfad)] = e
        else:
            e = Einheit(len(einheiten) + 1, v.pfad, v.anzeige, v.roh, v.seite, "teil", eltern=alt,
                        bestand=v.bestand)
            if getrennt:
                e.hinweise.append("Signatur taucht erneut auf, nachdem schon andere Signaturen folgten.")
            alt.teile_liste.append(e)
            alt.kinder.append(e)
        letzter = (v.bestand, v.pfad)
        verarbeite(v, e, rand, rand_spalte)
        v.einheit = e
        einheiten.append(e)
    # Hierarchie über die Pfade; «A.1.-8.» umfasst A.1. bis A.8.
    bereiche = {}
    for b, p in knoten:
        m = re.fullmatch(r"(\d+)[a-z]?-(\d+)[a-z]?", p[-1])  # auch «6-7a» mit 6, 7, 7a (VII.4.)
        if m:
            bereiche.setdefault((b, p[:-1]), []).append((int(m.group(1)), int(m.group(2)), knoten[(b, p)]))
    for e in einheiten:
        if e.art != "knoten" or len(e.pfad) == 1 and not bereiche.get((e.bestand, ())):
            continue
        letzte_komp = e.pfad[-1]
        # (der engste Bereich: «57 – 58 Zeitungsausschnitte» in «50 – 58 Publikationen …», VII.80.; auch ein Bereich
        # in einem weiteren)
        m_lk = re.fullmatch(r"(\d+)[a-z]?", letzte_komp)
        m_lb = re.fullmatch(r"(\d+)[a-z]?-(\d+)[a-z]?", letzte_komp)
        # (ein Abschnitt mit Bereichssignatur nimmt nur Schachteln auf, die allein zu ihm gehören: «VI.SB.D.6.:6-7 d)
        # …» über «Schachtel 6: d.1», «Schachtel 7: d.2» – aber «Schachtel 1: a-f» und «Schachtel 2: f-g» der Übersicht
        # gehören nicht unter «VI.SB.D.5.:1-2 f) Arbeitslosenfürsorge», VI.SB.)
        def nur_dieser_abschnitt(b: Einheit) -> bool:
            m_ab = re.match(r"([a-z])\)\s", b.titel or "")
            m_sch = re.match(r"Schachtel\s+\d+[a-z]?\s*:\s*([a-z])(?:\.\d+)?(?:\s*[-–]\s*([a-z])(?:\.\d+)?)?\b",
                             e.titel or "")
            return not (m_ab and m_sch) or {m_sch.group(1), m_sch.group(2) or m_sch.group(1)} == {m_ab.group(1)}
        umfassend = [(z - a, b) for a, z, b in bereiche.get((e.bestand, e.pfad[:-1]), []) if b is not e
                     and nur_dieser_abschnitt(b) and (
            m_lk and a <= int(m_lk.group(1)) <= z
            # («3a. Tabellarisches Hauptbuch» nach «1-3. Sitzungsprotokolle» / «3. Band» gehört nicht in den Bereich,
            # VII.15. – wohl aber «7a» in «6-7a», VII.4.)
            and not (letzte_komp[-1:].isalpha() and int(m_lk.group(1)) == z and not b.pfad[-1][-1:].isalpha())
            or m_lb and a <= int(m_lb.group(1)) and int(m_lb.group(2)) <= z
            and z - a > int(m_lb.group(2)) - int(m_lb.group(1)))]
        bereich = min(umfassend, key=lambda x: x[0])[1] if umfassend else None
        if bereich:
            e.eltern = bereich
            bereich.kinder.append(e)
            continue
        if len(e.pfad) == 1:
            continue
        for n in range(len(e.pfad) - 1, 0, -1):
            kandidat = knoten.get((e.bestand, e.pfad[:n]))
            if kandidat:
                e.eltern = kandidat
                kandidat.kinder.append(e)
                if n != len(e.pfad) - 1:
                    e.hinweise.append(f"Übergeordnete Signatur {pfad_text(e.pfad[:-1])} fehlt im Findmittel; "
                                      f"eingehängt unter {kandidat.anzeige}")
                break
        else:
            e.hinweise.append(f"Keine übergeordnete Signatur gefunden (erwartet {pfad_text(e.pfad[:-1])}).")
    # Wortsignatur im Abschnitt einer Hauptnummer: «1. Kontrollen und Register» / «V.G. c.42.:Reg. Register» / «Reg. 1»
    # … «Reg. 5» / «V.G. c.42.:1.1. Ammoniakfabrikation» (V.G.c.42.): «Reg.» gehört unter 1.
    for k, e in enumerate(einheiten):
        if e.art != "knoten" or e.eltern is not None or len(e.pfad) != 1 \
                or not re.fullmatch(r"[A-Z][a-z]{1,3}", e.pfad[0]):
            continue
        vor_e = next((x for x in reversed(einheiten[:k]) if x.art == "knoten" and x.bestand == e.bestand
                      and x.pfad[:1] != e.pfad[:1]), None)
        nach_e = next((x for x in einheiten[k + 1:] if x.art == "knoten" and x.bestand == e.bestand
                       and x.pfad[:1] != e.pfad[:1]), None)
        if vor_e is not None and nach_e is not None and len(vor_e.pfad) == 1 and vor_e.pfad[0].isdigit() \
                and len(nach_e.pfad) == 2 and nach_e.pfad[:1] == vor_e.pfad:
            e.eltern = vor_e
            vor_e.kinder.append(e)
            e.hinweise.append(f"Signatur {e.anzeige} steht im Findmittel im Abschnitt {vor_e.anzeige} – dort "
                              "eingehängt, bitte prüfen.")
    # Vollsignatur unter einer Kategorie mit Buchstabenmarke: «d) Rechnungen» / «III.S. 1. Rechnungen des
    # Pfarrpfrundfonds 1788-1797» / «e) Akten keine» (III.S.): die Einheit gehört zur Kategorie davor
    def kategorie(x: Einheit) -> bool:
        return x.art == "knoten" and len(x.pfad) == 1 and re.fullmatch(r"[a-z]", x.pfad[0]) is not None
    for k, e in enumerate(einheiten[1:], 1):
        if e.art != "knoten" or e.eltern is not None or len(e.pfad) != 1 or not e.pfad[0][:1].isdigit() \
                or not re.match(r"[IVX]{1,4}\.", normalisiere_signatur(e.roh)):
            continue
        vor_e = einheiten[k - 1]
        ziel = vor_e if kategorie(vor_e) and not vor_e.kinder else \
            vor_e.eltern if vor_e.eltern is not None and kategorie(vor_e.eltern) and len(vor_e.pfad) == 1 else None
        if ziel is not None:
            e.eltern = ziel
            ziel.kinder.append(e)
    # leere Kategorie, die schon als Bereich aus der Übersicht da ist («III.G.1.-3. a) Kopialbücher» und im Verzeichnis
    # nochmals «a) Kopialbücher» ohne Inhalt, III.G.): nicht doppelt
    bereich_buchstaben = {m.group(1) for x in einheiten if x.art == "knoten" and not kategorie(x)
                          for m in [re.match(r"([a-z])\)\s", x.titel or "")] if m}
    for e in [x for x in einheiten if kategorie(x) and not x.kinder and not x.darin and not x.teile_liste
              and x.pfad[0] in bereich_buchstaben]:
        einheiten.remove(e)
        e.entfernt = "Kategorie schon als Bereich aus der Übersicht"
        info.setdefault("uebersicht", []).append(f"{e.anzeige} (S. {e.seite})")
    # (die Übersichtszeile einer leeren Kategorie im Darin davor – «b) Amtsordnungen» mit «c) Urbare, Offnungen und
    # Wirtschaftsordnungen (keine)», III.R. – bleibt stehen, zählt hier aber nicht als eigener Inhalt)
    leer_buchstaben = {x.pfad[0] for x in einheiten if kategorie(x)}

    def nur_leere_kategorien(x: Einheit) -> bool:
        return all((m_d := re.match(r"([a-z])\)\s.*\(keine\)\.?$", d)) and m_d.group(1) in leer_buchstaben
                   for d in x.darin)
    # Kategorie aus der Übersicht mit nur einer Nummer («e) Akten ¦ III.P.21.»): sie trägt sonst die Signatur ihrer
    # einzigen Einheit, und diese wird zu «Teil 2» (III.P., III.Q., III.R.) – die Kategorie bekommt die
    # Buchstaben-Signatur wie die leeren Kategorien («III.P.:e.»), die Einheit steht darunter
    for x in [x for x in einheiten if x.art == "knoten" and not kategorie(x) and len(x.pfad) == 1
              and x.pfad[0].isdigit() and len(x.teile_liste) == 1 and nur_leere_kategorien(x)
              and not [k for k in x.kinder if k is not x.teile_liste[0]]]:
        m_k = re.match(r"([a-z])\)\s", x.titel or "")
        t = x.teile_liste[0]
        if not m_k or any(kategorie(y) and y.pfad[0] == m_k.group(1) for y in einheiten):
            continue
        buchstabe = m_k.group(1)
        x.pfad, x.anzeige = (buchstabe,), f"{buchstabe}."  # (roh bleibt «III.P. 21.» für «Nr. im PDF»)
        x.teile_liste = []
        t.art, t.teil_nr = "knoten", None
        t.hinweise = [h for h in t.hinweise if "taucht erneut auf" not in h]
        x.hinweise.append(f"Kategorie aus der Übersicht mit nur einer Nummer ({t.anzeige}) – als Gruppe "
                          f"«{buchstabe})» mit Buchstaben-Signatur übernommen.")
    # Gruppe ohne eigene Schachtelangabe, deren erste Untereinheit eine andere Schachtel nennt («3 Bauabrechnungen» /
    # «1 Bauabrechnungen 1923 … Schachtel 320», VII.179.): die weitergezogene Schachtel davor gilt für sie nicht
    for e in einheiten:
        erstes = next((k for k in e.kinder if k.art == "knoten"), None)
        if e.schachtel_geerbt and erstes is not None and erstes.schachtel and not erstes.schachtel_geerbt \
                and erstes.schachtel != e.schachtel:
            e.schachtel, e.schachtel_geerbt = None, False
    # Reihenfolge der Nummern prüfen (nur Zahlen; oberste Ebene je Bestand)
    for k, b in [*[(None, b) for b in dict.fromkeys(x.bestand for x in einheiten)],
                 *[(x, x.bestand) for x in einheiten if x.art == "knoten"]]:
        # (nur direkte Unternummern: eine eingehängte «1.2.1.» unter «1.», weil 1.2. fehlt, ist keine zweite «1»,
        # V.B.c.32.)
        geschwister = [x for x in (k.kinder if k else einheiten) if x.art == "knoten" and x.bestand == b
                       and (len(x.pfad) == 1 if k is None else len(x.pfad) == len(k.pfad) + 1)
                       and re.fullmatch(r"\d+(?:/\d+)?", x.pfad[-1])]
        # (Doppelnummern «20/21» zählen mit, Bereiche «11-33» aus Übersichten nicht)
        erwartet = None
        for g in geschwister:
            m_nr = re.fullmatch(r"(\d+)(?:[-/](\d+))?", g.pfad[-1])
            nr, nr_bis = int(m_nr.group(1)), int(m_nr.group(2) or m_nr.group(1))
            m_sch = re.fullmatch(r"(\d+)-(\d+)", g.schachtel or "") if g.behaelter else None
            if m_sch and int(m_sch.group(1)) == nr:
                nr_bis = int(m_sch.group(2))  # «Schachteln 8 und 9» als Einheit 8: danach folgt 10
            if erwartet is not None and nr != erwartet and not (info.get("freie_nummern") and nr > erwartet):
                tipp = " Möglicher Tippfehler in der Signatur." if nr > erwartet + 3 or nr < erwartet else ""
                if nr == erwartet - 1:  # «594/595» und danach «595» (VII.308.D.a.), «1.2.» zweimal
                    g.hinweise.append(f"Nummer {nr} kommt im Findmittel zweimal vor – bitte prüfen.")
                else:
                    g.hinweise.append(f"Nummerierung springt: nach {erwartet - 1} folgt {nr}.{tipp}")
            elif erwartet is None and nr != 1 and modus == "dezimal" and not re.fullmatch(r"\d{3}", g.pfad[-1]):
                g.hinweise.append(f"Nummerierung beginnt bei {nr}.")  # (nicht bei Codes «021» eines Registraturplans)
            erwartet = nr_bis + 1
    return spalte_teil1_ab(einheiten)


def spalte_teil1_ab(einheiten: list[Einheit]) -> list[Einheit]:
    """«3.3.3.2. B Personaldossiers, Teil 1» + «3.3.3.2. …, Teil 2»: Teil 1 wird Geschwister von Teil 2."""
    neu: list[Einheit] = []
    for e in einheiten:
        neu.append(e)
        m = TEIL_ZEILE_RE.match(e.titel) if e.art == "knoten" and e.teile_liste else None
        if m and m.group("nr") == "1":
            t = Einheit(0, e.pfad, e.anzeige, e.roh, e.seite, "teil", titel=e.titel, darin=e.darin,
                        verweise=e.verweise, schachtel=e.schachtel, teil_nr=1, eltern=e,
                        spalten_zeitraum=e.spalten_zeitraum, herkunft=e, bestand=e.bestand)
            e.titel, e.darin, e.verweise = m.group("titel").rstrip(" ,"), [], []
            e.teile_liste.insert(0, t)
            e.kinder.insert(0, t)
            neu.append(t)
    return ordne_baum(neu)


def _initiale(text: str) -> str:
    t = text.lstrip(" „\"«(['").upper()
    return {"Ä": "A", "Ö": "O", "Ü": "U"}.get(t[:1], t[:1])


def korrigiere_jahrnummern(vorkommen: list["Vorkommen"]) -> None:
    """Zahlendreher und Tippfehler im Jahr einer Signatur «Jahr.Laufnummer»: «1974.7 Brüttisellen …» / «1947.7 Wangen
    …» / «1974.8 Kemptthal …» (VII.308.D.a.), «1969.17» / «1967.18» / «1969.19» (VII.308.F.a.) – das Jahr der Nachbarn
    gilt, mit Hinweis."""
    def teile(v: "Vorkommen") -> tuple[str, str] | None:
        m = re.fullmatch(r"(\d{4})\.(\d{1,4}[a-z]?)", v.pfad[0]) if len(v.pfad) == 1 else None
        return (m.group(1), m.group(2)) if m else None
    for k in range(1, len(vorkommen) - 1):
        v, a, b = vorkommen[k], teile(vorkommen[k - 1]), teile(vorkommen[k + 1])
        t = teile(v)
        if not (t and a and b) or a[0] != b[0] or t[0] == a[0]:
            continue
        if sorted(t[0]) != sorted(a[0]) and not _ein_zeichen_anders(t[0], a[0]):
            continue
        zahl = lambda x: int(re.match(r"\d+", x).group())
        if not zahl(a[1]) <= zahl(t[1]) <= zahl(b[1]):
            continue  # (die Laufnummer muss zwischen die Nachbarn passen – sonst ein verstellter, aber echter Eintrag)
        neu = f"{a[0]}.{t[1]}"
        v.hinweise.append(f"Im Findmittel «{v.pfad[0]}» zwischen {vorkommen[k - 1].pfad[0]} und "
                          f"{vorkommen[k + 1].pfad[0]} – als «{neu}» gelesen (Tippfehler im Jahr?), bitte prüfen.")
        v.pfad, v.anzeige = (neu,), neu


def verteile_detaillisten(vorkommen: list["Vorkommen"], info: dict) -> None:
    """Detailverzeichnisse nach der letzten Einheit, die nur über die Schachtelnummer mit den Einheiten verbunden sind
    («DETAILVERZEICHNIS ZU DEN ROLLENBÜCHERN» / «"Winkelgässli 7" 1954 ¦ 55» …, «DETAILVERZEICHNIS ZU DEN TEXTBÜCHERN
    Schachtel 62», VII.197.): jede Zeile zur Einheit, deren Schachteln die Nummer enthalten (VIII.1. 55–61, VIII.2.
    62–67); was in die Schachteln der letzten Einheit fällt, bleibt dort."""
    if len(vorkommen) < 3:
        return
    letzte = vorkommen[-1]
    verbleib = info.get("verbleib", [])
    pos = lambda z: (z.seite, z.top)
    kopf_re = re.compile(r"Detailverzeichnis(?:se)?\s+zu", re.I)
    koepfe = [vb.zeile for vb in verbleib if vb.art == "ueberschrift" and kopf_re.match(vb.zeile.text.strip())] \
        + [z for z in letzte.zeilen[1:] if kopf_re.match(z.text.strip())]
    if not letzte.zeilen or not koepfe:
        return
    start = min((pos(k) for k in koepfe if pos(k) > pos(letzte.zeilen[0])), default=None)
    if start is None:
        return
    # (samt grösserem Titel direkt davor: «Dramatischer Verein Zürich» 16 pt über «Detailverzeichnisse zu den …»)
    davor = [z for z in letzte.zeilen if pos(z) < start]
    if davor and davor[-1].seite == start[0] and davor[-1].worte and davor[-1].worte[0].size >= 14 \
            and len(davor) >= 2:
        start = pos(davor[-1])
    eigen = [z for z in letzte.zeilen if pos(z) < start]
    rest = [z for z in letzte.zeilen if pos(z) >= start]
    if len(eigen) < 2 or len(rest) < 10:
        return

    def nummern(text: str | None) -> set[int]:
        aus: set[int] = set()
        for a, b in re.findall(r"(\d{1,4})(?:\s*-\s*(\d{1,4}))?", text or ""):
            if b and int(a) <= int(b) <= int(a) + 50:
                aus.update(range(int(a), int(b) + 1))
            else:
                aus.add(int(a))
        return aus
    boxen: dict[int, set[int]] = {}
    for k, v in enumerate(vorkommen):
        zs = eigen if v is letzte else v.zeilen
        boxen[k] = nummern(v.schachtel) | {n for z in zs for n in nummern(z.schachtel)}
    # Schachtelangaben der Köpfe («… TEXTBÜCHERN Schachtel 62», «Verzeichnis zu Schachtel 70») nach Lage
    marken = sorted((pos(vb.zeile), int(m.group(1))) for vb in verbleib if vb.art == "ueberschrift"
                    and pos(vb.zeile) >= start
                    and (m := re.search(r"(?:Schachtel\s+|^)(\d{1,4})\s*$", " ".join(
                        filter(None, (vb.zeile.text.strip(), vb.zeile.schachtel and f"Schachtel {vb.zeile.schachtel}"))))))
    laufend, zuordnung, offen, m_idx = None, [], [], 0
    for z in rest:
        while m_idx < len(marken) and marken[m_idx][0] <= pos(z):
            laufend = marken[m_idx][1]
            m_idx += 1
        eigene = sorted(nummern(z.schachtel))
        m_v = re.fullmatch(r"(?:Detail)?[Vv]erzeichnis\b.*\bSchachtel\s+(\d{1,4})(?:\s*\(.*\))?", z.text.strip())
        k_r = rest.index(z)
        if not eigene and not m_v and z.text.strip().isupper() and k_r + 1 < len(rest) \
                and re.fullmatch(r"(?:Detail)?[Vv]erzeichnis\b.*\bSchachtel\s+\d{1,4}.*", rest[k_r + 1].text.strip()):
            offen.append(z)  # «BÜCHER DER BIBLIOTHEK DES D.V.Z.» / «Verzeichnis zu Schachtel 70»
            continue
        if eigene:
            laufend = eigene[0]
        elif m_v:  # «Verzeichnis zu Schachtel 70», «Verzeichnis zu Schachtel 72 (Grossformat)»
            laufend = int(m_v.group(1))
        ziel_k = [k for k, b in boxen.items() if laufend is not None and laufend in b]
        if len(ziel_k) != 1:
            offen.append(z)
            continue
        zuordnung.extend((ziel_k[0], x) for x in offen + [z])
        offen = []
    zuordnung.extend((len(vorkommen) - 1, x) for x in offen)
    if not any(vorkommen[k] is not letzte for k, _ in zuordnung):
        return
    # Kopf vor der ersten Schachtelangabe («Dramatischer Verein Zürich / Detailverzeichnisse zu den Rollenbüchern …
    # / Die Bücher sind NICHT in alphabetischer Reihenordnung …»): Überschrift, Hinweis bei der ersten Einheit
    erste_box = next((k for k, (_, x) in enumerate(zuordnung) if x.schachtel or x is not rest[0] and False), None)
    kopf = []
    for k_z, (k, x) in enumerate(zuordnung):
        if x.schachtel or re.fullmatch(r"(?:Detail)?[Vv]erzeichnis\b.*\bSchachtel\s+\d{1,4}.*", x.text.strip()):
            break
        kopf.append(x)
    if kopf and len(kopf) <= 8:
        ziel_kopf = vorkommen[zuordnung[len(kopf)][0]] if len(kopf) < len(zuordnung) else letzte
        ids_kopf = {id(x) for x in kopf}
        zuordnung = [(k, x) for k, x in zuordnung if id(x) not in ids_kopf]
        for vb in verbleib:
            if vb.art == "einheit" and id(vb.zeile) in ids_kopf:
                vb.art, vb.vorkommen = "ueberschrift", None
        if any(kopf_re.match(x.text.strip()) for x in kopf):
            ziel_kopf.hinweise.append("Steht im Findmittel unter der Überschrift der Detailverzeichnisse am Schluss: «"
                                      + saeubere(" ".join(x.text.strip() for x in kopf)) + "».")
    letzte.zeilen = list(eigen)
    letzte.hinweise = [h for h in letzte.hinweise if not h.startswith("Nach der letzten Einheit steht im Findmittel ein "
                                                                     "Absatz ohne Signatur")]
    neu_ort: dict[int, Vorkommen] = {}
    for k, z in zuordnung:
        vorkommen[k].zeilen.append(z)
        neu_ort[id(z)] = vorkommen[k]
    for vb in verbleib:
        if vb.art == "einheit" and id(vb.zeile) in neu_ort:
            vb.vorkommen = neu_ort[id(vb.zeile)]
    for k in sorted({k for k, _ in zuordnung}):
        if vorkommen[k] is not letzte:
            vorkommen[k].hinweise.append("Einträge aus den Detailverzeichnissen am Schluss über die Schachtelnummer "
                                         "zugeordnet, bitte prüfen.")


def verteile_buchstabenlisten(vorkommen: list[Vorkommen], info: dict) -> None:
    """«55 Briefe an und von Emil Klöti I A – M» / «56 … II N – Z» und danach die ganze Absenderliste A–Z unter 56
    (VII.109.): die Zeilen nach den Anfangsbuchstaben auf die beiden Einheiten verteilen (vor dem Darin, damit die
    Vollständigkeitsprüfung die Zeilen der richtigen Einheit zuordnet)."""
    bereich_re = re.compile(r"\b([A-Z])\s*[–-]\s*([A-Z])\s*$")
    verbleib: list[Verbleib] = info.setdefault("verbleib", [])
    for k in range(len(vorkommen) - 1):
        v1, v2 = vorkommen[k], vorkommen[k + 1]
        if v1.ist_teil or v2.ist_teil or len(v1.zeilen) != 1 or len(v2.zeilen) < 21 or v1.bestand != v2.bestand \
                or len(v1.pfad) != len(v2.pfad) or v1.pfad[:-1] != v2.pfad[:-1]:
            continue
        m1, m2 = bereich_re.search(v1.zeilen[0].text.strip()), bereich_re.search(v2.zeilen[0].text.strip())
        if not (m1 and m2) or not (m1.group(2) < m2.group(1) <= m2.group(2)):
            continue
        zeilen = v2.zeilen[1:]
        inits = [_initiale(z.text) for z in zeilen]
        nr1, nr2 = re.escape(v1.pfad[-1]), re.escape(v2.pfad[-1])
        # die Wiederholung der zweiten Überschrift im Detail («56 Briefe an und von Emil Klöti II N – Z») trennt
        split = next((i for i, z in enumerate(zeilen) if i and re.match(rf"{nr2}\.?\s", z.text.strip())), None)
        if split is None:
            split = next((i for i in range(1, len(inits)) if m2.group(1) <= inits[i] <= m2.group(2)
                          and m1.group(1) <= inits[i - 1] <= m1.group(2)), None)
        if split is None \
                or sum(1 for x in inits[split:] if m2.group(1) <= x <= m2.group(2)) < 0.8 * (len(inits) - split) \
                or sum(1 for x in inits[:split] if m1.group(1) <= x <= m1.group(2)) < 0.7 * split:
            continue
        wiederholt = {id(z) for z in zeilen if re.match(rf"(?:{nr1}|{nr2})\.?\s", z.text.strip())}
        nach_v1 = {id(z) for z in zeilen[:split]}
        v1.zeilen = v1.zeilen + [z for z in zeilen[:split] if id(z) not in wiederholt]
        v2.zeilen = v2.zeilen[:1] + [z for z in zeilen[split:] if id(z) not in wiederholt]
        for vb in verbleib:
            if vb.vorkommen is v2 and id(vb.zeile) in wiederholt:
                vb.art, vb.vorkommen = "ueberschrift", None  # wiederholte Überschrift = Titel
            elif vb.vorkommen is v2 and id(vb.zeile) in nach_v1:
                vb.vorkommen = v1
        for v, von, bis in ((v1, m1.group(1), m1.group(2)), (v2, m2.group(1), m2.group(2))):
            v.hinweise.append(f"Liste nach den Anfangsbuchstaben verteilt ({von} – {bis} nach Titel), bitte prüfen.")


def verteile_lange_darin(einheiten: list[Einheit]) -> list[Einheit]:
    """Ein Darin über DARIN_MAX Zeichen (eine Excel-Zelle fasst 32 767) wird auf weitere Teile derselben
    Signatur verteilt statt gekürzt – typisch für Tabellen-Findmittel (Plakat- oder Programmlisten)."""
    ergebnis: list[Einheit] = []
    geteilt = False
    for e in einheiten:
        ergebnis.append(e)
        if len("\n".join(e.darin)) <= DARIN_MAX:
            continue
        stuecke: list[list[str]] = [[]]
        laenge = 0
        for d in e.darin:
            if stuecke[-1] and laenge + len(d) + 1 > DARIN_MAX:
                stuecke.append([])
                laenge = 0
            stuecke[-1].append(d)
            laenge += len(d) + 1
        knoten = e if e.art == "knoten" else e.eltern
        e.darin = stuecke[0]
        hinweis = f"Darin zu lang für eine Excel-Zelle – auf {len(stuecke)} Teile verteilt (vermutlich eine Tabelle)."
        e.hinweise.append(hinweis)
        pos = 0 if knoten is e else knoten.teile_liste.index(e) + 1
        for n, stueck in enumerate(stuecke[1:]):
            t = Einheit(0, e.pfad, e.anzeige, e.roh, e.seite, "teil", darin=stueck, schachtel=e.schachtel,
                        eltern=knoten, herkunft=e, hinweise=[hinweis], bestand=e.bestand)
            knoten.teile_liste.insert(pos + n, t)
            knoten.kinder.append(t)
            ergebnis.append(t)
        geteilt = True
    return ordne_baum(ergebnis) if geteilt else einheiten


def ordne_baum(einheiten: list[Einheit]) -> list[Einheit]:
    """Zeilen so ordnen, dass jede Einheit nach ihrer übergeordneten steht (Tiefensuche in PDF-Reihenfolge)."""
    pos = {id(e): i for i, e in enumerate(einheiten)}
    ergebnis: list[Einheit] = []
    besucht: set[int] = set()

    def besuche(e: Einheit) -> None:
        if id(e) in besucht:
            return
        besucht.add(id(e))
        ergebnis.append(e)
        for k in sorted(e.kinder, key=lambda k: pos.get(id(k), 0)):
            besuche(k)

    for e in einheiten:
        if e.eltern is None:
            besuche(e)
    for e in einheiten:  # Sicherheitsnetz: nichts geht verloren
        besuche(e)
    for i, e in enumerate(ergebnis, start=1):
        e.id = i
    return ergebnis


# ----------------------------------------------------------------------------- Inhaltsverzeichnis


SPALTEN_DATUM_RE = re.compile(r"((?:\d{1,2}\.\s?){0,2}(?:1[0-9]|20)\d\d(?:\s*[-–]\s*(?:\d{1,2}\.\s?){0,2}\d{2,4})?)"
                              r"\s+(\S.*)$")


def einheiten_nur_im_vorspann(vorspann: list[Zeile], modus: str, bestand: str, buchstaben: bool,
                              vorhanden: set[tuple]) -> list[Vorkommen]:
    """Positionen, die nur in der Zusammenfassung stehen, wenn das Verzeichnis selbst darauf verweist («Nicht im Detail
    verzeichnet (Vgl. Zusammenfassung vorn.)», VII.174.: 08.9. Bilder, 09 NACHTRÄGE): als Einheiten übernehmen,
    mit den Zeilen bis zur nächsten Signatur der Zusammenfassung."""
    gl = Gliederung(modus, bestand)
    gl.buchstaben = buchstaben and modus == "dezimal"
    gesehen: list[Vorkommen] = []
    aktuell = None
    for z in vorspann:
        t = lies_signatur(z, gl)
        if t is not None:
            aktuell = Vorkommen(t.pfad, t.anzeige, t.roh, z.seite, [t.rest] if t.rest else [], typ=t.typ,
                                schachtel=z.schachtel or None, datum=z.datum, x0=z.x0)
            gesehen.append(aktuell)
        elif aktuell is not None and z.text.strip() and not ist_verzeichniswort(z.text) \
                and not DETAIL_RE.fullmatch(z.text.strip()):
            aktuell.zeilen.append(z)
    # je Signatur die ausführlichste Nennung (Zusammenfassung S. 10 statt Kurzliste S. 2 «VII.174.09 NACHTRÄGE»)
    beste: dict[tuple, Vorkommen] = {}
    for v in gesehen:
        if v.pfad not in beste or len(v.zeilen) > len(beste[v.pfad].zeilen):
            beste[v.pfad] = v
    neu = []
    for v in gesehen:
        if v is not beste[v.pfad] or v.pfad in vorhanden or not v.zeilen:
            continue
        if len(v.pfad) > 1 and v.pfad[:-1] not in vorhanden and not any(x.pfad == v.pfad[:-1] for x in neu):
            continue  # ohne übergeordnete Einheit im Verzeichnis: eher ein Tippfehler der Zusammenfassung
        if v.pfad[-1] in ("l", "I", "O", "o") and modus == "dezimal":
            continue  # «3.l. Neubau Tonwarenfabrik» (l statt 1, VII.174.): Tippfehler, die Position steht im Verzeichnis
        v.hinweise.append(f"Nur in der Zusammenfassung verzeichnet (S. {v.seite}; im Verzeichnis «Nicht im Detail "
                          "verzeichnet») – von dort übernommen, bitte prüfen.")
        neu.append(v)
    return neu


def lese_inhaltsverzeichnis(zeilen: list[Zeile], modus: str, bestand: str,
                            buchstaben: bool = False) -> dict[tuple, Zeitraum | None]:
    """Signaturpfad -> Zeitraum aus Übersicht und Inhaltsverzeichnis (buchstaben: Abschnitte mit eigener Zählung
    wie im Detailverzeichnis, «02 NEUBAUTEN» / «2. Neubauten Fabrik …» = 02.2., VII.174.)."""
    eintraege: dict[tuple, list[str]] = {}
    gl = Gliederung(modus, bestand)
    gl.buchstaben = buchstaben and modus == "dezimal"
    akt = None

    def markiert(x: Zeile | None) -> str:
        """Spaltenwerte ⟦…⟧ markieren: reine Datumsabschnitte zwischen Lücken («Mitgliederverzeichnis ¦ 1877 – 1911 ¦
        Schachtel 3»), reine Datums-Folgezeilen («1903 – 1920» / «1921 – 1947», VII.188.) und ein Datum am Anfang
        eines Spaltenabschnitts («Rechnungen über die Verwaltung ¦ 1801 – 1955 103 – 109», VII.191.)."""
        teile_x = x.text_mit_luecken().split(" ¦ ") if x else []
        aus = []
        for k, s in enumerate(teile_x):
            m = SPALTEN_DATUM_RE.match(s) if k else None
            aus.append(f"⟦{s}⟧" if ist_reiner_zeitausdruck(s) else
                       f"⟦{m.group(1)}⟧ {m.group(2)}" if m and not finde_zeitraeume(m.group(2), False) else s)
        return " ¦ ".join(aus)

    for z in zeilen:
        t = lies_signatur(z, gl)
        if t is None and modus == "dezimal" and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX \
                and DEZIMAL_RE.match(z.worte[0].text):
            nummer = DEZIMAL_RE.match(z.worte[0].text).group(1)
            if "." not in nummer and z.ab(1) and not MONAT_WORT_RE.match(z.worte[1].text):
                t = SigTreffer((nummer,), nummer + ".", nummer, z.ab(1), False)  # Übersicht nach Inhaltsverz.
        if t:
            akt = t.pfad
            eintraege.setdefault(akt, []).append("¶" + markiert(t.rest) + (f" ⟦{z.datum}⟧" if z.datum else ""))
        elif akt and z.worte[0].x0 > SIGNATUR_SPALTE_MAX:
            eintraege[akt].append(markiert(z) + (f" ⟦{z.datum}⟧" if z.datum else ""))
    ergebnis: dict[tuple, Zeitraum | None] = {}
    for pfad, teile in eintraege.items():
        for block in " ".join(teile).split("¶"):  # gleiche Signatur in Übersicht und Inhaltsverzeichnis
            text = saeubere(re.sub(r"⟦([^⟧]*)⟧", r" ¦ \1", block))
            if not text:
                continue
            funde = jahr_klammer_laufzeit(text) or [f for f in finde_zeitraeume(text) if not f.ereignis]
            # alle Spaltendaten zusammen (nicht bloss das letzte Datum): mehrzeilige Datumsspalte (VII.188.),
            # Unterzeile «Belege dazu ¦ 1852 – 1942» (VII.191.); Lebensdaten oder Amtszeiten im Titel zählen
            # nicht («Heinrich Treichler-Pétua (1879 – 1946), des Delegierten … 1926 – 1938» ¦ 1922-1941)
            spalte = [f for teil in re.findall(r"⟦([^⟧]*)⟧", block) for f in finde_zeitraeume(teil) if not f.ereignis]
            zr = vereinige(spalte) if spalte else (funde[-1] if funde else None)
            if ergebnis.get(pfad) is None and zr is not None or pfad not in ergebnis:
                ergebnis[pfad] = zr
    return ergebnis


# ----------------------------------------------------------------------------- Zeiträume

ZUVERLAESSIG = {"Datumsspalte", "Titel", "Inhaltsverzeichnis", "Untereinheiten", "übergeordnete Einheit",
                "Titel (Ereignisdatum)"}


def _ist_premierendatum(titel: str, f: Zeitraum) -> bool:
    """Ein einzelnes Tagesdatum in Klammern am Titelende: «… Theaterstück von Tom Stoppard (03.02.1977)»."""
    return bool(f.von and f.von.tag and f.von == f.bis and titel[:f.start].rstrip().endswith("(")
                and re.fullmatch(r"\)\s*[.:]?\s*", titel[f.ende:]))


def _spielzeit_fuer_teil(e: Einheit, knoten_zr: Zeitraum | None) -> Zeitraum | None:
    """Spielzeit der Serie für einen Teil mit eigenem Titel («5.2.4.6. - Der Tag, an dem der Papst gekidnappt wurde …»
    unter «Produktionen … 1974/75», VII.200.): Zeitraum der übergeordneten Einheit aus Spalte, Titel oder
    Inhaltsverzeichnis über genau zwei aufeinanderfolgende Jahre («1974/75», «1997–1998»). Nicht, wenn der Teil die
    Einheit fortsetzt (gleicher Titel): dann hat er eigene Jahre («Gemeindegesetz ¦ 1938–1940» nach «Gemeindegesetz ¦
    1934–1935», V.G.c.50.; zweite Ausgabe eines Buchs, X.G.)."""
    if e.art != "teil" or e.titel_uebernommen or e.eltern is None or knoten_zr is None \
            or not (knoten_zr.von and knoten_zr.bis) or knoten_zr.bis.jahr != knoten_zr.von.jahr + 1:
        return None
    # (auch nicht bei einer anderen Einheit mit derselben Nummer weiter hinten: «Signatur taucht erneut auf»)
    if any("taucht erneut auf" in h for h in e.hinweise) or _ist_fortsetzung(e.eltern, e):
        return None
    return knoten_zr


def _lage_zur_spielzeit(zr: Zeitraum, spielzeit: Zeitraum) -> str:
    """Wie liegt ein Zeitraum zur Spielzeit? «aussen» (keine Überschneidung), «punkt» (ein einzelnes Datum oder Jahr
    darin), «innen» (eine Spanne darin), «ueber» (eine Spanne, die die Spielzeit schneidet und über sie hinausreicht),
    «offen» (ohne Beginn oder Ende)."""
    if not (zr.von and zr.bis):
        return "offen"
    if zr.bis.schluessel(ende=True) < spielzeit.von.schluessel() \
            or zr.von.schluessel() > spielzeit.bis.schluessel(ende=True):
        return "aussen"
    if zr.von == zr.bis:
        return "punkt"
    return "innen" if _innerhalb(zr, spielzeit) else "ueber"


def jahr_klammer_laufzeit(text: str) -> list:
    """Laufzeit in Klammern am Ende, direkt nach einem Jahr, das zum Namen gehört: «Jahrgängerverein 1786 (1834 –
    1863)» (VII.254.), «Eingemeindung von 1934 (1919 – 1935)» (V.E.c.53.) – die Klammer ist die Laufzeit, keine
    Lebensdaten; Stellen bezogen auf den ganzen Text."""
    m = re.search(rf"(?<![–-])(?<![–-]\s)\b{JAHR}\s*\(\s*({JAHR}(?:\s*[–-]\s*{JAHR})?)\s*\)\s*$", text)
    if not m:
        return []
    funde = finde_zeitraeume(m.group(1))
    for f in funde:
        f.start, f.ende = f.start + m.start(1), f.ende + m.start(1)
    return funde


def zeitraum_aus_titel(e: Einheit, rahmen: tuple[int, int] | None = None) -> None:
    """Zeitraum aus Datumsspalte bzw. Titel lesen und – falls gewünscht – aus dem Titel entfernen.
    rahmen: Zeitraum des Bestands laut Online-Archiv (für die Daten im Darin)."""
    plausibel = _darin_plausibel(e, rahmen) if e.darin_funde else []
    rahmen_b = rahmen if not e.bestand else None
    if e.spalten_zeitraum and e.spalten_zeitraum.von and plausibel:
        # Datumsspalten der Einträge erweitern die Datumsspalte der Titelzeile («Schachtel 302 ¦ 1958» / «Stucki …
        # ¦ 1943», VII.191.) – nur wenn sie in andere Jahre reichen (sonst bleibt das genaue «3.7.1921»); ohne
        # Tippfehler («1993» unter «1883-1884», VII.15.)
        zr_d = _anschliessend(e.spalten_zeitraum, plausibel, rahmen_b)
        if zr_d and _ausserhalb(zr_d, e.spalten_zeitraum):
            gesamt = vereinige([e.spalten_zeitraum, zr_d])
            gesamt.original = f"{e.spalten_zeitraum.original}; Darin: {_spanne(zr_d)}"
            e.spalten_zeitraum, e.spalte_erweitert, e.darin_erweiterung = gesamt, True, zr_d
    funde = finde_zeitraeume(e.titel) if e.titel else []
    # Daten in einer Klammer mitten im Titel zählen sonst nicht (meist Lebensdaten o. Ä.): ohne anderes Titeldatum gilt
    # ein volles Datum daraus («E. Utzinger, Die finanziellen Beziehungen … (Vortrag … vom 14. August 1938 in Stäfa),
    # Broschüre, 40 Seiten», VII.55. 5.9.3.) – nicht Lebensdaten «(16. Oktober 1718 – 17. März 1767)» (VII.277.)
    klammer_rueckfall = False
    if not funde and e.titel and "(" in e.titel and not e.spalten_zeitraum:
        klammern = _klammer_bereiche(e.titel)
        funde = [f for f in finde_zeitraeume(e.titel, klammern_ignorieren=False)
                 if f.von and f.bis and f.von.tag and f.bis.tag and f.bis.jahr - f.von.jahr <= 1
                 and any(a < f.start and f.ende <= b for a, b in klammern)]
        klammer_rueckfall = bool(funde)
    klammer_laufzeit = jahr_klammer_laufzeit(e.titel) if e.titel and not e.spalten_zeitraum else []
    if klammer_laufzeit:
        funde = klammer_laufzeit
    if PERSON_RE.search(e.titel) and not klammer_laufzeit:
        # Personen-Überschrift «Oskar Wälterlin (1895–1961), Direktor … 1938–1961»: weitere
        # Jahreszahlen sind Amtszeiten, keine Laufzeit der Unterlagen; die Lebensdaten selbst zählen gar nicht – auch
        # nicht als Ersatz vor den Daten im Darin («Ludwig Heinrich Friedrich von Podewils (-1838)» / «Vertrag über das
        # Rittergut Weisdorf ¦ 1810», VII.388.)
        lebensdaten = [(m.start(), m.end()) for m in LEBENSDATEN_KLAMMER_RE.finditer(e.titel)]
        funde = [f for f in funde if not any(a <= f.start and f.ende <= b for a, b in lebensdaten)]
        for f in funde:
            f.ereignis = True
    # gefeierte Spanne «Zürich 600 Jahre im Bund der Eidgenossen 1352 – 1952», «100 Jahre Studentengesangverein
    # 1849 – 1949» (V.L.111., VII.267.): keine Laufzeit – es zählt das Endjahr (Jubiläums- bzw. Erscheinungsjahr)
    funde = [_jubilaeum_ende(f) if f.von and f.bis and f.bis.jahr > f.von.jahr and re.search(
        rf"\b{f.bis.jahr - f.von.jahr}\s*(?:Jahre|years|ans|anni)\b", e.titel, re.I) else f for f in funde]
    laufzeit = [f for f in funde if not f.ereignis]
    ereignisse = [f for f in funde if f.ereignis]
    # Teil mit eigenem Titel und Premierendatum am Ende («Travesties oder Zürich 1917, Theaterstück von Tom Stoppard
    # (03.02.1977)», «Aus dem Leben der Regenwürmer. Ein Familiengemälde von 1856, … (01.04.1984)», VII.200.): nur das
    # Premierendatum zählt, die übrigen Jahre gehören zum Werktitel
    if e.art == "teil" and len(laufzeit) > 1 and _ist_premierendatum(e.titel, laufzeit[-1]):
        laufzeit = laufzeit[-1:]
    if rahmen and not e.bestand:
        # Jahre weit vor dem Bestandszeitraum sind ein Bezug, keine Laufzeit («Zürichs Beitritt zur Eidgenossenschaft,
        # 1. Mai 1351. Denkschrift … am 1. Mai 1851», VII.381.) – nur wenn noch ein anderes Datum bleibt
        a_r = rahmen[0] - RAHMEN_VORLAUF
        weit = [f for f in laufzeit if all(d.jahr < a_r for d in (f.von, f.bis) if d)]
        if weit and len(weit) < len(laufzeit) + len(ereignisse):
            laufzeit = [f for f in laufzeit if f not in weit]
    if ereignisse:
        e.ereignis_zeitraum = vereinige(ereignisse)
    if e.spalten_zeitraum:
        e.zeitraum, e.zeitraum_quelle = e.spalten_zeitraum, "Datumsspalte"
        # genauere Angabe im Titel («Protokolle 4. Juni 1890 – 23. Sept. 1916» + Spalte «1890-1916»);
        # bei mehreren Angaben die genaueste mit denselben Jahren («… 1961/62, Teil 1 ab 2. Sept. 1961
        # bis 28. Jan. 1962» + Spalte «1961-1962») – nicht die Vereinigung, die auf ganze Jahre aufrundet
        # Liegt eine Angabe mit Tag/Monat innerhalb der Spalte, gilt die genaueste («… 1961/62, Teil 2 ab
        # 30. Jan. 1962 bis 1. Juli 1962» + Spalte «1961-1962»); Ereignisdaten nur bei gleichen Jahren
        spalte = e.spalten_zeitraum
        innen = [f for f in laufzeit if _innerhalb(f, spalte) and f.von != f.bis]
        beste = max((_genauigkeit(f) for f in innen), default=0)
        if beste:
            genutzt = [f for f in innen if _genauigkeit(f) == beste]
            titel_zr = vereinige(genutzt)
        else:
            kandidaten = laufzeit or ereignisse
            passend = [f for f in kandidaten if _jahre(f) == _jahre(spalte)]
            if passend and 0 < max(_genauigkeit(f) for f in passend) <= _genauigkeit(spalte) \
                    and not any(_innerhalb(f, spalte) for f in passend):
                return  # anderes, nicht genaueres Datum im Titel (Briefdatum): die Spalte gilt, der Titel bleibt
            genutzt = [max(passend, key=_genauigkeit)] if passend else kandidaten
            titel_zr = vereinige(genutzt)
            if not (titel_zr and _jahre(titel_zr) == _jahre(spalte)):
                return
        # Wortlaut des Titels in die Anmerkung, wenn er mehr sagt als von/bis («1891/92 – 1920/21»)
        # (eine um das Darin erweiterte Spalte nennt beides: «1949 – 1960; Darin: 1961–1975», VII.171.)
        original = titel_zr.original if titel_zr.original and titel_zr.anmerkung_noetig else spalte.original
        e.zeitraum = Zeitraum(titel_zr.von, titel_zr.bis, original, ca=titel_zr.ca)
        if e.spalte_erweitert and e.darin_erweiterung is not None and _ausserhalb(e.darin_erweiterung, e.zeitraum):
            # das genauere Titeldatum ersetzt nur die Spalte der Titelzeile, nicht deren Erweiterung aus dem Darin
            # («Sept./Okt. 1935» + Darin 1938 → 09.1935–1938, nicht 09.–10.1935 mit Anmerkung «…; Darin: 1938»,
            # VII.12.B. 26.2.4.)
            g = vereinige([e.zeitraum, e.darin_erweiterung])
            eigen = titel_zr.original or spalte.original.split("; Darin:")[0]
            e.zeitraum = Zeitraum(g.von, g.bis, f"{eigen}; Darin: {_spanne(e.darin_erweiterung)}", ca=g.ca)
        if not laufzeit or not (laufzeit[-1] in genutzt or _jahre_abgedeckt(laufzeit[-1], e.zeitraum)):
            return  # die letzte Zeitangabe im Titel steckt nicht im Zeitraum – sie bleibt im Titel
    elif not laufzeit:
        return
    else:
        e.zeitraum, e.zeitraum_quelle = vereinige(laufzeit), "Titel"
        if len(laufzeit) > 1:
            e.hinweise.append(f"Mehrere Zeitangaben im Titel ({', '.join(f.original for f in laufzeit)}).")
        if klammer_rueckfall and e.darin:
            # das Klammerdatum nennt oft nur einen Anlass: nahe Jahre im Darin zählen mit («Tagesseminar … (3. April
            # 1992)» / «… (8. März 1993)», V.F.c.28.; «Chlaus Lymbacher … (02.10.1990), Akten» / «1989–1991:
            # Besetzungsliste …», VII.200.)
            zr_d = jahre_im_text(_darin_text(e), rahmen_b)
            g = vereinige([e.zeitraum, zr_d]) if zr_d and _ausserhalb(zr_d, e.zeitraum) else None
            if g is not None and g.von and g.bis and e.zeitraum.von.jahr - g.von.jahr <= 10 \
                    and g.bis.jahr - e.zeitraum.bis.jahr <= 10:
                e.zeitraum, e.zeitraum_quelle = Zeitraum(g.von, g.bis), "Titel und Darin (geschätzt)"
                e.hinweise.append("Zeitraum aus dem Datum in der Titelklammer und den Jahreszahlen im Darin geschätzt.")
        # «Personendossiers 1886» / «Nüssli, Emil … ¦ 1886 – 1928» (VII.158.): die Spaltendaten der Einträge zählen
        # mit, wenn sie lückenlos anschliessen (kein Tippfehler «Kreis III ¦ 1995-1897», V.H.c.53.); die Anmerkung
        # nennt beide Angaben, das Titeldatum kommt wie sonst aus dem Titel
        zr_d = _anschliessend(e.zeitraum, plausibel, rahmen_b) if e.darin_spalte_traegt and plausibel else None
        if zr_d and _ausserhalb(zr_d, e.zeitraum):
            gesamt = vereinige([e.zeitraum, zr_d])
            jahrgang = e.zeitraum.von == e.zeitraum.bis and e.zeitraum.von is not None and not e.zeitraum.von.monat
            e.zeitraum = Zeitraum(gesamt.von, gesamt.bis,
                                  f"Titel: {e.zeitraum.original}; Darin: {_spanne(zr_d)}",
                                  ca=gesamt.ca)
            if jahrgang:
                return  # ein einzelnes Jahr bezeichnet die Einheit («Personendossiers 1886», VII.158.) – es bleibt
    if not TITEL_OHNE_ZEITRAUM:
        return
    f = laufzeit[-1]
    vorn, hinten = e.titel[:f.start].rstrip(), e.titel[f.ende:]
    if vorn.endswith("(") and re.fullmatch(r"\)\s*[.:]?\s*", hinten) and f.von is not None and f.von.monat \
            and f.bis is not None and f.bis.jahr - f.von.jahr <= 2:
        # (nur ein Datum wie die Premiere, nicht Lebensdaten «(16. Oktober 1718 – 17. März 1767)», VII.277.)
        # «Early Morning (Trauer zu früh), Komödie von Edward Bond (02.10.1969)» (VII.200.): Datum samt Klammer weg
        vorn, hinten = vorn[:-1].rstrip(), ""
    letztes = vorn.split()[-1].lower() if vorn.split() else ""
    if letztes in {"von", "vom", "am", "im", "bis", "seit", "um", "der", "des", "spielzeit", "saison", "jahr",
                   "jahre", "jahren", "jahrgang", "jg.", "jg", "sommer", "winter", "frühling", "herbst", "ende",
                   "anfang", "ws", "ss", "semester", "wintersemester", "sommersemester"}:
        return
    if re.search(r"(?:(?<![\d.])\d{1,2}\.?|(?<!\d)\d{4})\s?[/–-]\s*$", vorn):
        return  # «… vom 13 – 15. September», «1853 – ca. 1873»: sonst bliebe ein halber Bereich stehen (V.E.c.53.)
    if re.fullmatch(r"\s*(\([^()]*\))?\s*[.:]?\s*", hinten):
        neu = (vorn.rstrip(" ,;/–-") + (" " + hinten.strip() if hinten.strip(" .:") else "")).strip()
    elif re.fullmatch(r",\s*(?:[^\d]+|\(?Teil\s+\d+\)?)", hinten) \
            and hinten.strip(" ,.;").lower() not in {"in", "im", "und", "u.", "mit", "von", "an", "auf", "für", "bei"}:
        neu = vorn.rstrip(" ,;/–-") + hinten
    else:
        return
    if len(neu) >= 3:
        e.titel_mit_datum, e.titel = e.titel, saeubere(neu)


def ergaenze_zeitraeume(einheiten: list[Einheit], toc: dict, rahmen: tuple[int, int] | None = None) -> None:
    """rahmen: Zeitraum des Bestands laut Online-Archiv (für die Schätzungen aus dem Darin)."""
    # Inhaltsverzeichnis für Knoten ohne eigenen Zeitraum; Abweichungen melden
    for e in einheiten:
        toc_zr = toc.get(e.pfad) if e.art == "knoten" else None
        if toc_zr is None:
            continue
        if e.zeitraum is None:
            e.zeitraum, e.zeitraum_quelle = toc_zr, "Inhaltsverzeichnis"
        elif _jahre(e.zeitraum) != _jahre(toc_zr):
            e.hinweise.append(f"Zeitraum weicht vom Inhaltsverzeichnis ab ({toc_zr.original}).")
    # von unten nach oben, damit Gruppen die Zeiträume ihrer Untereinheiten kennen
    for e in sorted(einheiten, key=lambda x: -x.tiefe):
        knoten = e.eltern if e.art == "teil" else None
        knoten_zr = knoten.zeitraum if knoten and knoten.zeitraum_quelle in (
            "Datumsspalte", "Titel", "Inhaltsverzeichnis") else None
        sicher = [k.zeitraum for k in e.kinder if k.zeitraum and k.zeitraum_quelle in ZUVERLAESSIG]
        if e.kinder:  # Gruppe: Untereinheiten, sonst deren Schätzungen, zuletzt Datum im Titel
            alle = [k.zeitraum for k in e.kinder if k.zeitraum]
            nur_eigene_spalte = not alle
            # eigener Inhalt der ersten Nennung (= Teil 1) zählt mit – als Schätzung aus dem Darin
            eigen = jahre_im_text(_darin_text(e), rahmen if not e.bestand else None) \
                if e.darin and e.teile_liste and not e.undatiert else None
            spalte = _darin_spalte(e, rahmen) if e.darin_spalte and e.darin_spalte_traegt and not e.undatiert \
                else None
            if spalte is not None:  # Spaltendaten im eigenen Darin: sicher wie eine Untereinheit
                zr_d, geschaetzt = spalte
                if not geschaetzt:
                    sicher.append(zr_d)
                alle.append(zr_d)
                eigen = None
            if eigen:
                alle.append(eigen)
            # nur sichere Untereinheiten, wenn alle sicher sind – sonst alle, als Schätzung (D3018 07.: 07.1.
            # geschätzt 1919–1959, 07.2. = 1963, 07.3. 1986 → 1919–1986, nicht bloss 1963)
            if e.zeitraum is None and sicher and not eigen and len(sicher) == len(alle):
                gesamt = vereinige(sicher)
                e.zeitraum = Zeitraum(gesamt.von, gesamt.bis, ca=gesamt.ca)
                # (nur aus der eigenen Datumsspalte, ohne datierte Untereinheiten: Quelle «Datumsspalte», VII.327.)
                e.zeitraum_quelle = "Datumsspalte" if nur_eigene_spalte else "Untereinheiten"
            if e.zeitraum is None and alle:
                gesamt = vereinige(alle)
                e.zeitraum, e.zeitraum_quelle = Zeitraum(gesamt.von, gesamt.bis), "Untereinheiten (geschätzt)"
                e.hinweise.append("Zeitraum aus geschätzten Zeiträumen der Untereinheiten.")
            if e.zeitraum is None and e.ereignis_zeitraum:
                e.zeitraum, e.zeitraum_quelle = e.ereignis_zeitraum, "Titel (Ereignisdatum)"
        else:  # einzelne Einheit: Datum im Titel, geerbter Zeitraum, Schätzung aus dem Darin
            # Teil mit eigenem Titel in einer Spielzeit: ohne Premierendatum gilt die Spielzeit der Serie – Jahre aus
            # dem Werktitel («Das verschonte Land / … / Landi-Wiese 1939–1945, diverse Projekte», «(Wiederaufnahme von
            # 1973)») und einzelne Jahre im Darin («Die Verborgenen 1948», «Radierung von 1893») sind kein Zeitraum der
            # Unterlagen (VII.200.)
            #   Ein Tages- oder Monatsdatum (Premiere, Gastspiel) bleibt, ebenso eine Spanne, die über die Spielzeit
            #   hinausreicht («Professor Bernhardi … (Akten 1989–1991)», «Requiem für eine Nonne (1955/56–1956/57)»)
            spielzeit = _spielzeit_fuer_teil(e, knoten_zr)
            if spielzeit is not None and e.zeitraum is not None and e.zeitraum_quelle == "Titel":
                lage = _lage_zur_spielzeit(e.zeitraum, spielzeit)
                genau = e.zeitraum.von is not None and e.zeitraum.von.monat is not None
                if lage == "aussen" and not (genau and e.zeitraum.von.tag) or lage == "punkt" and not genau:
                    e.zeitraum, e.zeitraum_quelle = None, ""
                    e.titel = e.titel_mit_datum or e.titel  # die Jahre bleiben im Titel
                    e.hinweise = [h for h in e.hinweise if not h.startswith("Mehrere Zeitangaben im Titel")]
            if e.zeitraum is None and e.ereignis_zeitraum and not e.undatiert:
                e.zeitraum, e.zeitraum_quelle = e.ereignis_zeitraum, "Titel (Ereignisdatum)"
            if e.zeitraum is None and knoten_zr and e.titel_uebernommen and not e.undatiert:
                e.zeitraum, e.zeitraum_quelle = knoten_zr, "übergeordnete Einheit"
            spalte = _darin_spalte(e, rahmen) if e.zeitraum is None and e.darin_spalte and e.darin_spalte_traegt \
                and not e.undatiert else None
            if spalte is not None:
                # Spaltendaten der Einträge; Jahre im Text der Einträge ohne Spaltendatum ergänzen sie als Schätzung
                e.zeitraum, geschaetzt = spalte
                e.zeitraum_quelle = "Datumsspalte und Darin (geschätzt)" if geschaetzt else "Datumsspalte"
                if geschaetzt:
                    e.hinweise.append("Zeitraum aus der Datumsspalte und den Jahreszahlen im Darin geschätzt.")
            # «o. J.» im Titel gilt für den ersten Eintrag; eine datierte Liste im Darin zählt trotzdem
            nur_erster = bool(re.search(r"\bo\.\s?[JD]\.", e.titel)) and not re.search(r"undatiert", e.titel, re.I)
            if e.zeitraum is None and (not e.undatiert or (nur_erster and len(e.darin) >= 2)):
                zr = jahre_im_text(_darin_text(e), rahmen if not e.bestand else None)
                if zr and spielzeit is not None and _lage_zur_spielzeit(zr, spielzeit) in ("aussen", "punkt", "offen"):
                    # Teil einer Spielzeit-Serie: ein einzelnes Jahr oder Datum im Darin («Papier zur Klausur vom 17.
                    # Mai 1994», «Theatertreffen Berlin 1999») oder eines ausserhalb («Die Verborgenen 1948», «Radierung
                    # von 1893») ist kein Zeitraum – es gilt die Spielzeit; eine genauere Spanne darin bleibt
                    # («Züglete …, S’Süess Gheimnis … (16.10./01.12.1982)», VII.200.)
                    e.zeitraum, e.zeitraum_quelle = spielzeit, "übergeordnete Einheit"
                elif zr and spielzeit is not None and _lage_zur_spielzeit(zr, spielzeit) == "ueber":
                    # eine Spanne im Darin, die über die Spielzeit hinausreicht: beides («Korrespondenz … über geplante
                    # Gastspiele 1997/98» in der Spielzeit 1996/97 → 1996–1998)
                    g = vereinige([spielzeit, Zeitraum(zr.von, zr.bis)])
                    e.zeitraum, e.zeitraum_quelle = Zeitraum(g.von, g.bis), "übergeordnete Einheit und Darin (geschätzt)"
                    e.hinweise.append("Zeitraum aus der Spielzeit der Serie und den Jahreszahlen im Darin geschätzt.")
                elif zr:
                    e.zeitraum, e.zeitraum_quelle = Zeitraum(zr.von, zr.bis), "Darin (geschätzt)"
                    e.hinweise.append("Zeitraum aus den Jahreszahlen im Darin geschätzt.")
                elif rahmen and not e.bestand and jahre_im_text(_darin_text(e)):
                    e.hinweise.append(f"Jahreszahlen im Darin liegen weit vor dem Bestandszeitraum laut "
                                      f"Online-Archiv ({rahmen[0]}–{rahmen[1]}) oder nach heute – vermutlich "
                                      "Bezüge oder Nummern, nicht als Zeitraum übernommen.")
            if e.zeitraum is None and knoten_zr and not e.undatiert:
                e.zeitraum, e.zeitraum_quelle = knoten_zr, "übergeordnete Einheit"
            # Mappe/Schachtel: das Datum im Titel gehört nur zur ersten Zeile, das Darin zählt mit
            if e.behaelter and e.zeitraum and e.zeitraum_quelle.startswith("Titel") and e.darin and not e.undatiert:
                zr = jahre_im_text(_darin_text(e), rahmen if not e.bestand else None)
                gesamt = vereinige([e.zeitraum, zr]) if zr and _ausserhalb(zr, e.zeitraum) else None
                nah = gesamt is not None and e.zeitraum.von and e.zeitraum.bis and gesamt.von and gesamt.bis \
                    and e.zeitraum.von.jahr - gesamt.von.jahr <= 10 and gesamt.bis.jahr - e.zeitraum.bis.jahr <= 10
                # offenes Titeldatum «Drucksachen 1881 ff.»: das Ende aus dem Darin (V.B.c.9.)
                offen_bis = e.zeitraum.von and e.zeitraum.bis is None and zr is not None and zr.bis \
                    and zr.bis.jahr >= e.zeitraum.von.jahr and zr.bis.jahr - e.zeitraum.von.jahr <= 30
                if nah:
                    e.zeitraum, e.zeitraum_quelle = Zeitraum(gesamt.von, gesamt.bis), "Titel und Darin (geschätzt)"
                    e.hinweise.append("Zeitraum aus den Jahreszahlen in Titel und Darin geschätzt.")
                    e.titel = e.titel_mit_datum or e.titel  # das Titeldatum gilt nur für die erste Zeile
                elif offen_bis:
                    e.zeitraum = Zeitraum(e.zeitraum.von, zr.bis, e.zeitraum.original)
                    e.zeitraum_quelle = "Titel und Darin (geschätzt)"
                    e.hinweise.append("Offenes Ende im Titel – Ende aus den Jahreszahlen im Darin geschätzt.")
        # Teile derselben Signatur gehören zur Einheit: ihr Zeitraum umfasst auch die Teile (VII.151. 4.2.: Teil 1
        # 1880–1970, Teil 2 bis 1987)
        # – nur Fortsetzungen, nicht andere Einheiten mit derselben Nummer, ausser das Inhaltsverzeichnis nennt den
        # ganzen Zeitraum («12.4. Diverse Veranstaltungen 1965 – 1996» mit Symposium 1979 und Tournee 1985–1996,
        # VII.151.); das eigene Datum bleibt in der Anmerkung
        teil_alle = [t.zeitraum for t in e.teile_liste if t.zeitraum and t.zeitraum_quelle in ZUVERLAESSIG]
        toc_e = toc.get(e.pfad) if e.art == "knoten" else None
        if not (teil_alle and e.zeitraum is not None and toc_e is not None
                and _jahre(vereinige([e.zeitraum] + teil_alle)) == _jahre(toc_e)):
            teil_alle = [t.zeitraum for t in e.teile_liste if t.zeitraum and t.zeitraum_quelle in ZUVERLAESSIG
                         and _ist_fortsetzung(e, t)]
        teil_zr = teil_alle
        if e.zeitraum is not None and teil_zr and e.zeitraum_quelle in ZUVERLAESSIG \
                and _ausserhalb(vereinige(teil_zr), e.zeitraum):
            gesamt = vereinige([e.zeitraum] + teil_zr)
            eigen_txt = e.zeitraum.original or _spanne(e.zeitraum)
            e.zeitraum = Zeitraum(gesamt.von, gesamt.bis, f"erste Nennung: {eigen_txt}", ca=e.zeitraum.ca)
        if e.zeitraum is None:
            continue
        if sicher and e.zeitraum_quelle in ("Datumsspalte", "Titel", "Inhaltsverzeichnis"):
            gesamt = vereinige(sicher)
            if _ausserhalb(gesamt, e.zeitraum):
                e.hinweise.append(f"Untereinheiten reichen über den Zeitraum hinaus "
                                  f"({_text(gesamt.von)}–{_text(gesamt.bis)}).")
        z = e.zeitraum
        if z.von and z.bis and z.von.schluessel() > z.bis.schluessel(ende=True):
            e.hinweise.append("Zeitraum: Beginn liegt nach dem Ende.")
    # mit den Teilen entspricht der Zeitraum jetzt dem Inhaltsverzeichnis: der Hinweis von oben ist überholt (VII.151.)
    for e in einheiten:
        toc_zr = toc.get(e.pfad) if e.art == "knoten" else None
        if toc_zr is not None and e.zeitraum is not None and _jahre(e.zeitraum) == _jahre(toc_zr):
            e.hinweise = [h for h in e.hinweise if not h.startswith("Zeitraum weicht vom Inhaltsverzeichnis ab")]
    # Locher «Jahr.Laufnummer» (VII.308.F.a.: «1939.37 Schulhaus Zeltweg»): ohne Datum das Jahr der Nummer, ca.
    jahr_sig = [e for e in einheiten if re.fullmatch(rf"{JAHR}\.\d{{1,4}}[a-z]?\.?", e.anzeige or "")]
    if len(jahr_sig) >= 5:
        for e in jahr_sig:
            if e.zeitraum is None and not e.undatiert:
                jahr = int(e.anzeige[:4])
                e.zeitraum, e.zeitraum_quelle = Zeitraum(Datum(jahr), Datum(jahr), ca=True), "Signatur (Jahr)"
    # «Kein Zeitraum» nur bei der obersten betroffenen Einheit melden, nicht bei jedem Teil darunter
    for e in einheiten:
        if e.zeitraum is None and not e.undatiert and not (e.eltern and e.eltern.zeitraum is None) \
                and "Laut Findmittel keine Unterlagen vorhanden." not in e.hinweise:
            e.hinweise.append("Kein Zeitraum gefunden" + (" (auch nicht in den Untereinheiten)." if e.kinder else "."))


def _jahre(z: Zeitraum) -> tuple:
    return (z.von.jahr if z.von else None, z.bis.jahr if z.bis else None)


def _innerhalb(innen: Zeitraum, aussen: Zeitraum) -> bool:
    """Liegt «innen» (mit Beginn und Ende) ganz im Zeitraum «aussen»?"""
    if not (innen.von and innen.bis and aussen.von and aussen.bis):
        return False
    return (innen.von.schluessel() >= aussen.von.schluessel()
            and innen.bis.schluessel(ende=True) <= aussen.bis.schluessel(ende=True))


def _jahre_abgedeckt(f: Zeitraum, zr: Zeitraum) -> bool:
    """Ein Bereich in Jahren («1901 – 1904»), den der Zeitraum ganz abdeckt – er darf aus dem Titel weg.
    Einzeldaten («Altdorf, 1934») bleiben stehen: der Zeitraum sagt nicht, dass es genau 1934 war."""
    if not (f.von and f.bis and zr.von and zr.bis) or f.von == f.bis or f.von.monat or f.bis.monat:
        return False
    return zr.von.jahr <= f.von.jahr and f.bis.jahr <= zr.bis.jahr


def _genauigkeit(z: Zeitraum) -> int:
    """Tag > Monat > Jahr, für Beginn und Ende zusammen."""
    return sum(bool(d.monat) + bool(d.tag) for d in (z.von, z.bis) if d)


def _text(d: Datum | None) -> str:
    return d.text() if d else "?"


def _spanne(z: Zeitraum) -> str:
    """«1891–1922», bei gleichem Beginn und Ende nur «1920»."""
    return _text(z.von) if z.von == z.bis or z.bis is None else f"{_text(z.von)}–{_text(z.bis)}"


def _ausserhalb(innen: Zeitraum, aussen: Zeitraum) -> bool:
    if innen.von and aussen.von and innen.von.jahr < aussen.von.jahr:
        return True
    return bool(innen.bis and aussen.bis and innen.bis.jahr > aussen.bis.jahr)


DARIN_LUECKE = 35  # Jahre: weiter entfernte Darin-Daten erweitern einen Zeitraum nicht («März 1947» unter 1846–1848)


def _darin_plausibel(e: "Einheit", rahmen: tuple[int, int] | None) -> list[Zeitraum]:
    """Spaltendaten des Darin ohne Unmögliches: nach heute, weit vor dem Bestandszeitraum (Plannummern «1274»,
    Dossiernummern «1517»)."""
    a = rahmen[0] - RAHMEN_VORLAUF if rahmen and not e.bestand else None
    ok = []
    for f in e.darin_funde:
        jahre = [d.jahr for d in (f.von, f.bis) if d]
        if jahre and max(jahre) <= HEUTE_JAHR and (a is None or min(jahre) >= a):
            ok.append(f)
    return ok


RAHMEN_NACHLAUF = 5  # Jahre: so weit nach dem Ende des Bestandszeitraums (Online-Archiv) gilt ein Datum noch als echt


def _tippfehler_jahre(jahr: int, lo: int, hi: int, rand: int = 5) -> list[int]:
    """Jahre in lo–hi (± rand), die aus «jahr» durch eine andere Ziffer oder zwei vertauschte Nachbarziffern
    entstehen – die vermutlich gemeinten bei einem Tippfehler («1947» statt «1847», VII.12.A.; «1990» statt «1920»,
    VII.197.; «1987» statt «1907», VII.31.)."""
    s = f"{jahr:04d}"
    kand = {int(s[:i] + z + s[i + 1:]) for i in range(4) for z in "0123456789" if z != s[i]}
    kand |= {int(s[:i] + s[i + 1] + s[i] + s[i + 2:]) for i in range(3) if s[i] != s[i + 1]}
    return sorted(k for k in kand if lo - rand <= k <= hi + rand)


def _anschliessend(basis: Zeitraum | None, funde: list[Zeitraum],
                   rahmen: tuple[int, int] | None = None) -> Zeitraum | None:
    """Vereinigung der Darin-Daten. Kern: was lückenlos (höchstens DARIN_LUECKE Jahre) an basis bzw. aneinander
    anschliesst; ohne basis zählt der mittlere Fund als Kern. Weiter entfernte Daten bleiben nur draussen, wenn sie
    wie ein Tippfehler aussehen – eine Ziffer anders als ein Jahr im Kern und dazu nach dem Ende des Bestandszeitraums
    laut Online-Archiv («25.09.1990» zwischen 1920 und 1922, VII.197.) bzw. bei einer langen Spanne mit einem Ende im
    Kern so, dass die berichtigte Spanne kurz ist («Oktober 1846 bis März 1947» unter Halbjahren, VII.12.A. 5.6.).
    Echt sind dagegen ganze Spannen und Gruppen von Einträgen («1961–1980» unter 1894, IV.A.; Bücher 1948–1959 unter
    1901, VII.191.), einzelne ältere Stücke («Kochbuch ¦ 1746», VII.388.) und lange Spannen wie «Seeauffüllung
    1830 – 1925» (V.G.c.105.) – sie erweitern den Zeitraum."""
    stuecke = []  # (von-Jahr, bis-Jahr, Zeitraum, Nummer der zerlegten langen Spanne oder None)
    funde = [f for f in funde if f.von or f.bis]
    spannen = sorted((f.bis or f.von).jahr - (f.von or f.bis).jahr for f in funde)
    ueblich = spannen[len(spannen) // 2] if spannen else 0
    for nr, f in enumerate(funde):
        a, b = (f.von or f.bis).jahr, (f.bis or f.von).jahr
        if b - a > 60 and b - a > 5 * max(1, ueblich) and f.von and f.bis:
            # eine einzelne, ungewöhnlich lange Spanne: für den Kern zählen die Enden einzeln (unten wird sie ganz
            # behalten, wenn das ferne Ende kein Tippfehler ist) – lange Reihen wie «1835-1933» neben «1832-1933»
            # bleiben ganz (VI.SB.)
            stuecke += [(a, a, Zeitraum(f.von, f.von, ca=f.ca), nr), (b, b, Zeitraum(f.bis, f.bis, ca=f.ca), nr)]
        else:
            stuecke.append((a, b, f, None))
    if not stuecke:
        return None
    if basis is not None and (basis.von or basis.bis):
        lo, hi = (basis.von or basis.bis).jahr, (basis.bis or basis.von).jahr
    else:
        mitte = sorted(stuecke, key=lambda s: (s[0], s[1]))[len(stuecke) // 2]
        lo, hi = mitte[0], mitte[1]
    geaendert = True
    while geaendert:
        geaendert = False
        for a, b, _, _ in stuecke:
            if (a < lo or b > hi) and b >= lo - DARIN_LUECKE and a <= hi + DARIN_LUECKE:
                lo, hi, geaendert = min(lo, a), max(hi, b), True
    im_kern = [lo <= a and b <= hi for a, b, _, _ in stuecke]
    if basis is None and sum(im_kern) < 3:
        zr = vereinige(funde)  # ohne klaren Kern kein Ausreisser («1891-1940», «1983-1984», VII.12.B.)
        if zr is not None:
            zr.original = ""
        return zr
    ende = rahmen[1] + RAHMEN_NACHLAUF if rahmen else None
    behalten, zerlegt, weg = [], {}, 0
    for (a, b, f, nr), k in zip(stuecke, im_kern):
        if nr is not None:
            zerlegt.setdefault(nr, []).append((a, f, k))
        elif k or a != b:
            behalten.append(f)  # im Kern – oder eine ganze ferne Spanne: ein Tippfehler träfe nur eine Zahl
        elif any(not k2 and nr2 is None and f2 is not f and a2 - DARIN_LUECKE <= a <= b2 + DARIN_LUECKE
                 for (a2, b2, f2, nr2), k2 in zip(stuecke, im_kern)):
            behalten.append(f)  # mit weiteren fernen Einträgen: eine eigene Gruppe, kein Tippfehler
        elif ende is not None and a > ende and _tippfehler_jahre(a, lo, hi):
            weg += 1  # einzelnes Datum nach dem Bestandszeitraum, eine Ziffer anders als ein Jahr im Kern
        else:
            behalten.append(f)  # älteres Einzelstück oder Nachtrag im Bestandszeitraum
    for nr, enden in zerlegt.items():
        innen = [x for x in enden if x[2]]
        fern = [x for x in enden if not x[2]]
        if len(innen) == 1 and len(fern) == 1:
            x, y = innen[0][0], fern[0][0]
            kand = _tippfehler_jahre(y, lo, hi)
            kurz = [j for j in kand if (j - x) * (y - x) >= 0 and abs(j - x) <= max(5, 3 * ueblich)]
            if kand and ((ende is not None and y > ende) or kurz):
                behalten.append(innen[0][1])  # nur das Ende im Kern
                weg += 1
                continue
        behalten.append(funde[nr])  # die ganze Spanne
    if weg > len(funde) // 2:
        behalten = funde  # mehr Tippfehler als echte Daten: eher ist der Kern falsch – nichts verwerfen
    zr = vereinige(behalten)
    if zr is not None:
        zr.original = ""
    return zr


def _darin_spalte(e: "Einheit", rahmen: tuple[int, int] | None) -> tuple[Zeitraum, bool] | None:
    """Zeitraum aus den Datumsspalten des Darin (plausibel, lückenlos) und ob er geschätzt ist: Jahre im Text der
    Einträge ohne Spaltendatum («1987+1988», «1919 - 1934*», «NZZ 2.6.1975 und 25.1.1978») erweitern ihn als
    Schätzung, statt wegzufallen. Stimmen die Jahre mit den Daten im Text überein, gelten deren Tage
    («29. August 1989 … 5. September 1989» bei Spalte «1989», VII.423.)."""
    r = rahmen if not e.bestand else None
    zr_d = _anschliessend(None, _darin_plausibel(e, rahmen), r)
    if zr_d is None or zr_d.von is None:
        return None
    extra = jahre_im_text(e.darin_ohne_spalte, r) if e.darin_ohne_spalte else None
    if extra and _ausserhalb(extra, zr_d):
        gesamt = vereinige([zr_d, extra])
        von, bis = gesamt.von, gesamt.bis
        # bei gleichem Jahr gilt das genauere Datum («19. Juni 1903» statt «1903», V.G.c.43.)
        if von and extra.von and von.jahr == extra.von.jahr and _genauigkeit(Zeitraum(extra.von, None)) > \
                _genauigkeit(Zeitraum(von, None)):
            von = extra.von
        if bis and extra.bis and bis.jahr == extra.bis.jahr and _genauigkeit(Zeitraum(None, extra.bis)) > \
                _genauigkeit(Zeitraum(None, bis)):
            bis = extra.bis
        return Zeitraum(von, bis, ca=zr_d.ca), True
    zr_t = jahre_im_text(_darin_text(e), r)
    if zr_t is not None and _jahre(zr_t) == _jahre(zr_d):
        return Zeitraum(zr_t.von, zr_t.bis, ca=zr_d.ca), False
    return zr_d, False


ZITAT_RE = re.compile(r"\bIn:\s+\S")
ORT_JAHR_RE = re.compile(rf"\b[A-ZÄÖÜ][a-zäöüß]+,?\s+{JAHR}\b")


def _darin_text(e: "Einheit") -> str:
    """Darin für die Schätzung aus dem Text – ohne Fussnoten (Abrufdatum einer Webquelle, V.F.c.28.).

    Bibliografie (meist «…; In: Zeitschrift, Jahr, S. …»): nur die Erscheinungsjahre zählen – der Teil ab «In:»
    bzw. «Zürich 1922» bei Büchern –, nicht Jahre im Titel eines Aufsatzes (Lebensdaten, «1600-1800», VII.327. 2.3.)."""
    darin = [d for d in e.darin if not re.match(r"Fussnote \d+:", d)]
    zitate = [d for d in darin if ZITAT_RE.search(d)]
    if len(zitate) >= 4 and len(zitate) >= 0.6 * len(darin):
        teile = []
        for d in darin:
            m = ZITAT_RE.search(d)
            teile.extend([d[m.start():]] if m else [x.group(0) for x in ORT_JAHR_RE.finditer(d)])
        darin = teile
    return "\n".join(darin)


def _ist_fortsetzung(k: "Einheit", t: "Einheit") -> bool:
    """Setzt der Teil die Einheit fort (ohne eigenen Titel oder mit demselben, direkt anschliessend)? Nicht bei einer
    anderen Einheit mit derselben Nummer: Zählung je Abschnitt (VII.76.), andere Objekte einer Locher-Nummer
    (VII.308.), Bücher einer Schachtel (VII.359.), Tippfehler (VI.HO.C.25.)."""
    # (die Signatur zweimal direkt hintereinander – «… zweimal hintereinander – Tippfehler? Als weiterer Teil
    # übernommen» – ist gerade eine Fortsetzung, VII.151. 5.5.3.)
    if any("taucht erneut auf" in h or ("Tippfehler" in h and "zweimal hintereinander" not in h) for h in t.hinweise):
        return False
    def norm(s: str) -> str:
        return re.sub(r"[\W_]+", " ", re.sub(r",\s*Teil\s+\d+$", "", s)).strip().lower()
    a, b = norm(t.titel), norm(k.titel)
    # gleicher Titel oder der eine beginnt mit dem anderen («Kolben Papierfabrik Perlen» / «… Wasserkraftanlage»)
    if t.titel_uebernommen or a == b or (min(len(a), len(b)) >= 12 and (a.startswith(b) or b.startswith(a))):
        return True
    def kern(s: str) -> str:
        s = re.sub(r",\s*Teil\s+\d+$", "", s)
        s = re.sub(r"\((?:[IVX]{1,4}|\d{1,2})\)", " ", s)
        s = re.sub(r"\b(?:Nachtrag|Nachträge|Fortsetzung|Forts\.)", " ", s, flags=re.I)
        s = re.sub(rf"{JAHR}(?:\s*/\s*\d{{2,4}})?", " ", s)
        return re.sub(r"[\W\d_]+", " ", s).strip().lower()
    ka, kb = kern(t.titel), kern(k.titel)
    # gleicher Titel ohne Jahreszahlen, Zählung «(I)», «(II)» und «Nachtrag» («Konzerte (I)» / «Konzerte 1926 - 1967
    # (II), Nachtrag», VII.269.; «Jahresberichte … von 1924,1926,1927,1928» / «… von 1959-1961, 1963-1966», VII.212.)
    if ka and ka == kb:
        return True
    # der Teil hat nur eine Zählung oder Zeitangabe als Titel: «(I)» (VII.151. 5.5.3.), «Saison 1985/86» (VII.298.)
    if not ka or re.fullmatch(r"(?:saison|spielzeit|jahrgang|jahr|jahre|band|bd|heft|teil|nr)", ka):
        return True
    # der Titel der Einheit, gefolgt von einer Zeitangabe: «Akten» / «Akten 2000 – 2005: Statuten» (VII.93.)
    return bool(k.titel.strip()) and re.match(rf"{re.escape(k.titel.strip())}\s*,?\s*(?:[(\[]\s*)?{JAHR}", t.titel) is not None


# ----------------------------------------------------------------------------- Titel ergänzen


# Teil-Titel, der nur einen Zeitabschnitt nennt: «Saison 1981/82», «Spielzeit 1938/39», «1946 – 1960», «Jahr 1990»
ZEITABSCHNITT_RE = re.compile(rf"(?:(?:Saison|Spielzeit|Jahrgang|Jahr|Jahre|Amtsperiode|Semester)\s+)?"
                              rf"{JAHR}(?:\s*[/–-]\s*(?:\d{{2}}|{JAHR}))?(?:\s*[/–-]\s*{JAHR}(?:/\d{{2}})?)?")


def ergaenze_titel(einheiten: list[Einheit]) -> None:
    """Teile ohne eigenen Titel übernehmen ihn (mit «, Teil n»); Knoten ohne Titel vom Elternteil."""
    for k in [e for e in einheiten if e.teile_liste]:
        # Teil-Nummern in der Reihenfolge des PDFs, eindeutig je Signatur (die erste Nennung ist Teil 1); im PDF
        # genannte Nummern («Teil 3») bleiben. Früher begann die Zählung nach jedem Teil mit eigenem Titel neu bei 2
        # – das ergab doppelte Schlüssel (VII.200., VII.228., VII.270.).
        belegt = {t.teil_nr for t in k.teile_liste if t.teil_nr} | {1}
        naechste = 2
        for t in k.teile_liste:
            if not t.teil_nr:
                while naechste in belegt:
                    naechste += 1
                t.teil_nr = naechste
                belegt.add(naechste)
        zwischen = ""  # laufende Zwischenüberschrift «Saison 1981/82» (VII.151.)
        # Titel der Einheit bzw. des letzten Teils mit eigenem Titel und eigener Strichliste: ein titelloser Teil, der
        # mit einem Punkt «- …» beginnt, setzt diese Liste fort («Korrespondenz und Akten 1970–1981» / «2.3.2.9. -
        # Korrespondenz betreffend …» → «Korrespondenz und Akten, Teil 3», VII.200.)
        fortsetzung = k.titel if k.strichliste else ""
        letzter = ""  # letzter eigener Titel eines Teils davor
        for t in k.teile_liste:
            if re.fullmatch(r"[A-ZÄÖÜ](?:\s*[-–]\s*[A-ZÄÖÜ])?\.?", t.titel):
                t.darin.insert(0, t.titel)  # «3.1.2. A» / «Jürg Acklin, …» (VII.298.): Buchstabe der Liste, kein Titel
                t.titel = ""
            if t.titel and not TEIL_NUR_RE.match(t.titel):
                zwischen = t.titel if ZEITABSCHNITT_RE.fullmatch(t.titel) else ""
                fortsetzung = t.titel if t.strichliste else ""
                letzter = t.titel
                continue
            # titellose Teile tragen den Titel der Einheit, nicht den des letzten Teils mit eigenem Titel: der ist
            # meist ein anderes Stück («Der Rattenfänger» bekam «Der Büchsenöffner …, Teil 8», VII.200., Z291) –
            # ausser er ist nur ein Zeitabschnitt wie «Saison 1981/82»: dann setzt der Teil ihn fort (VII.151.)
            # (nie der Titel eines späteren Teils: «7.1. Johannes Weber …» ist eine andere Einheit, VII.93.)
            if t.beginnt_mit_punkt and fortsetzung:
                basis = re.sub(r",\s*Teil\s+\d+$", "", fortsetzung)
            else:
                eltern_titel = k.eltern.titel if k.art == "knoten" and k.eltern and k.eltern.titel else ""
                basis = zwischen or k.titel or eltern_titel or letzter
            if not basis:
                continue  # bleibt «[ohne Titel]» mit Hinweis
            t.titel = f"{basis}, Teil {t.teil_nr}" if TEIL_IM_TITEL else basis
            t.titel_uebernommen = True
    for e in einheiten:
        if not e.titel and e.art == "knoten" and e.eltern and e.eltern.titel:
            e.titel, e.titel_uebernommen = e.eltern.titel, True
            e.hinweise.append("Kein eigener Titel im Findmittel – Titel der übergeordneten Einheit übernommen.")
        if e.eltern and e.eltern.undatiert and e.zeitraum is None and e.spalten_zeitraum is None:
            e.undatiert = True  # «6.63. Undatierte Rollenbücher» -> auch 6.63.1. ff.
        if not e.titel:
            e.titel = "[ohne Titel]"
            e.hinweise.append("Kein Titel erkannt.")
        if len(e.titel) > 200:
            e.hinweise.append("Sehr langer Titel – evtl. Darin-Text im Titel.")


# ----------------------------------------------------------------------------- Vollständigkeit

WORT_RE = re.compile(r"[^\W\d_]+|\d+")
TRENNUNG_RE = re.compile(r"[A-Za-zÄÖÜäöüß]-$")
# In diesen Spalten muss der Text einer PDF-Zeile wieder auftauchen
PRUEF_FELDER = ("Signatur", "Nr. im PDF", "Titel", "Teil", "von", "bis", "Entstehungszeitraum, Anm.", "Darin",
                "Verwandte Verzeichnungseinheiten", "Umfang", "Schachtel-Nr.")
# Bindewörter von Datumsangaben («ab 2. Sept. 1961 bis …») verschwinden mit dem Datum aus dem Titel
VERBINDUNGSWOERTER = {"ab", "bis", "seit", "vom", "am", "um", "ca", "circa", "zirka", "und", "u", "von"}
NICHT_UEBERNOMMEN = {"ueberschrift": "Überschrift/Tabellenkopf ohne Signatur",
                     "wiederholung": "Wiederholte Abschnittsüberschrift nach einer Übersicht",
                     "vorlauf": "Text vor der ersten Signatur", "fussnote": "Fussnote"}


def vergleichswoerter(text: str) -> list[str]:
    """Wörter für den Vergleich PDF–Excel: klein, ohne Satzzeichen, Monatsnamen als Zahl («Okt.» = 10),
    Zahlen ohne führende Null («05» = 5), «o. D.»/«o. J.» = «undatiert»."""
    woerter = []
    for w in WORT_RE.findall(UNDATIERT_RE.sub(" undatiert ", text).lower()):
        if w in MONATE:
            w = str(MONATE[w])
        elif w.isdecimal():
            w = str(int(w))
        woerter.append(w)
    return woerter


def _woerter_der_excelzeile(z: dict) -> Counter:
    vorrat: Counter = Counter()
    for name in PRUEF_FELDER:
        if z.get(name) not in (None, ""):
            vorrat.update(vergleichswoerter(str(z[name])))
    if z.get("Schachtel-Nr."):
        vorrat["schachtel"] += 1
    for name in ("von", "bis"):  # Spielzeit «1938/39»: auch die Kurzform des Jahres zählt
        jahr = str(z.get(name) or "")[-4:]
        if jahr.isdecimal():
            vorrat[str(int(jahr[2:]))] += 1
    return vorrat


def pruefe_vollstaendigkeit(verbleib: list[Verbleib], einheiten: list[Einheit], excel_zeilen: list[dict]) -> dict:
    """Sucht jedes Wort des Detailverzeichnisses in der Excel-Zeile der Einheit, zu der seine PDF-Zeile gehört.

    Ergebnis: Wörter gesamt/gefunden, Zeilen mit fehlenden Wörtern («luecken»), bewusst nicht übernommene
    Zeilen (Überschriften ohne Signatur, Text vor der ersten Signatur) sowie die Zahl der Schlussvermerke
    (stehen im Info-Blatt) und der Übersichtszeilen (doppelt, ignoriert)."""
    excel_von = {id(e): z for e, z in zip(einheiten, excel_zeilen)}
    abgespalten: dict[int, list[dict]] = {}
    for e in einheiten:
        if e.herkunft is not None:
            abgespalten.setdefault(id(e.herkunft), []).append(excel_von[id(e)])
    erg: dict = {"woerter": 0, "gefunden": 0, "luecken": [], "nicht_uebernommen": [], "schluss": 0,
                 "uebersicht": 0}

    def luecke(z: Zeile, art: str, text: str, fehlt: list[str], e: Einheit | None) -> None:
        ez = excel_von.get(id(e)) if e else None
        erg["luecken"].append({"seite": z.seite, "art": art, "zeile": text, "fehlt": " ".join(fehlt),
                               "id": ez["ID"] if ez else "", "signatur": ez["Signatur"] if ez else ""})

    je_vorkommen: dict[int, list[Verbleib]] = {}
    for vb in verbleib:
        if vb.art == "einheit":
            je_vorkommen.setdefault(id(vb.vorkommen), []).append(vb)
        elif vb.art == "schachtel":  # die Einheit, für die die Schachtelangabe gilt, muss sie tragen
            erg["woerter"] += 1
            e = vb.vorkommen.einheit if vb.vorkommen else None
            ziele = [e, *[t for t in e.teile_liste if t.herkunft is e]] if e and not e.entfernt else []
            if any(_in_schachteln(vb.wert, str(excel_von[id(t)]["Schachtel-Nr."])) for t in ziele if id(t) in excel_von):
                erg["gefunden"] += 1
            else:
                luecke(vb.zeile, "Schachtelangabe", vb.zeile.text, [f"Schachtel {vb.wert}"], e)
            if vb.zeile.datum:  # «Schachtel 17 ¦ 1946 – 1947»: das Datum muss bei der Einheit stehen
                datumsworte = [w for w in vergleichswoerter(vb.zeile.datum) if w not in VERBINDUNGSWOERTER]
                da: set[str] = set()
                for t in ziele:
                    if id(t) in excel_von:
                        da |= set(_woerter_der_excelzeile(excel_von[id(t)]))
                fehlt = [w for w in datumsworte if w not in da]
                erg["woerter"] += len(datumsworte)
                erg["gefunden"] += len(datumsworte) - len(fehlt)
                if fehlt:
                    luecke(vb.zeile, "Datum der Schachtelangabe", f"{vb.zeile.text}  ¦ {vb.zeile.datum}", fehlt, e)
        elif vb.art == "schluss":
            erg["schluss"] += 1
        else:
            erg["nicht_uebernommen"].append({"seite": vb.zeile.seite, "art": NICHT_UEBERNOMMEN.get(vb.art, vb.art),
                                             "zeile": vb.zeile.text})
    for gruppe in je_vorkommen.values():
        e = gruppe[0].vorkommen.einheit
        if e is None or e.entfernt:
            erg["uebersicht"] += len(gruppe)
            continue
        excel = [excel_von[id(e)], *abgespalten.get(id(e), [])]
        vorrat: Counter = Counter()
        datumswoerter: set[str] = set()  # von/bis: Datumsangaben dürfen im PDF beliebig oft vorkommen
        for ez in excel:
            vorrat.update(_woerter_der_excelzeile({k: v for k, v in ez.items() if k not in ("von", "bis")}))
            datumswoerter.update(_woerter_der_excelzeile({k: ez.get(k) for k in ("von", "bis")}))
        vorhanden = set(vorrat) | datumswoerter
        spalte = e.spalten_zeitraum.original if e.spalten_zeitraum else None
        zeilen = []
        for vb in gruppe:
            z = vb.zeile
            # (wie Zeile.text, also mit angehängtem Bindestrich «Bauabrech-»)
            teil_z = z.ab(1) if z.worte and ist_aufzaehlung(z) else z
            text = teil_z.text if teil_z is not None and teil_z.worte else ""
            zusatz = " ".join(t for t in (z.datum, z.umfang, z.spalten) if t)  # die Schachtel prüft Schritt 3
            zeilen.append((z, text, zusatz, vergleichswoerter(text), vergleichswoerter(zusatz)))
        verbraucht: set[tuple[int, int]] = set()
        fehlt_je: dict[int, list[str]] = {}

        # Zeilen, deren Datum im Zeitraum (von/bis) aufgehen darf: Titelblock, Zeile mit der Datumsspalte
        # der Einheit, reine Datumszeilen («ab 2. Sept. 1961 bis 28. Jan. 1962»)
        kopf = gruppe[0].vorkommen.kopf_ids
        quelle = {0} | {k for k, zeile in enumerate(zeilen)
                        if id(zeile[0]) in kopf or (zeile[0].datum and zeile[0].datum == spalte)
                        or ist_reiner_zeitausdruck(zeile[1])}

        def gefunden(w: str, k: int) -> bool:
            if w in datumswoerter and k in quelle:
                return True
            if vorrat[w] > 0:
                vorrat[w] -= 1
                return True
            return False

        # 1) Text der Zeilen
        for k, (z, text, zusatz, worte, zusatzworte) in enumerate(zeilen):
            for j, w in enumerate(worte):
                if (k, j) in verbraucht or w in VERBINDUNGSWOERTER:
                    continue
                erg["woerter"] += 1
                # Silbentrennung wie in verbinde(): «Probenrap-» + «porte» = ein Wort, «Tonhalle-» + «Orchester» nicht
                naechste = zeilen[k + 1] if k + 1 < len(zeilen) else None
                if j == len(worte) - 1 and TRENNUNG_RE.search(text) and naechste and naechste[3]:
                    erstes = naechste[1].split()[0]
                    verbunden = (vergleichswoerter(w + naechste[3][0]) or [""])[0]
                    if erstes[:1].islower() and erstes not in KONJUNKTIONEN and vorrat[verbunden] > 0:
                        vorrat[verbunden] -= 1
                        verbraucht.add((k + 1, 0))
                        erg["woerter"] += 1
                        erg["gefunden"] += 2
                        continue
                if gefunden(w, k):
                    erg["gefunden"] += 1
                else:
                    fehlt_je.setdefault(k, []).append(w)
        # 2) rechte Spalte (Datum, Umfang, Schachtel): darf den Text wiederholen («Programme 1989 – 1991 ¦ 1989-1991»)
        for k, (z, text, zusatz, worte, zusatzworte) in enumerate(zeilen):
            # Wiederholung im Text derselben Einheit («Geschäftsordnung … ¦ 1905» / «vom 17. November 1905»)
            textworte = {w for zeile in zeilen for w in zeile[3]}
            wiederholt = False
            if z.datum:
                im_text, in_spalte = (vereinige(finde_zeitraeume(t, False)) for t in (text, z.datum))
                wiederholt = bool(im_text and in_spalte and _jahre(im_text) == _jahre(in_spalte))
            for w in zusatzworte:
                if w in VERBINDUNGSWOERTER:
                    continue
                erg["woerter"] += 1
                if gefunden(w, k) or wiederholt or w in textworte or (z.datum == spalte and w in vorhanden):
                    erg["gefunden"] += 1
                else:
                    fehlt_je.setdefault(k, []).append(w)
        # 3) Schachtel der Zeile (rechte Spalte oder blosse Zahl): Schachtel-Nr. der Einheit oder im Darin
        eigene = {str(ez.get("Schachtel-Nr.") or "") for ez in excel}
        for wert in list(eigene):  # auch Nummern in Bereichen «42-43», «55-61, 68-73»
            for a, b in re.findall(r"(\d{1,4})\s*-\s*(\d{1,4})", wert):
                if int(a) <= int(b) <= int(a) + 500:
                    eigene.update(str(n) for n in range(int(a), int(b) + 1))
                    eigene.update(f"{n:0{len(a)}d}" for n in range(int(a), int(b) + 1))
        for k, (z, *_) in enumerate(zeilen):
            if not z.schachtel:
                continue
            erg["woerter"] += 1
            nr = (vergleichswoerter(z.schachtel) or [z.schachtel])[0]
            if z.schachtel in eigene or gefunden(nr, k):
                erg["gefunden"] += 1
            else:
                fehlt_je.setdefault(k, []).append(f"Schachtel {z.schachtel}")
        for k, fehlt in fehlt_je.items():
            z, text, zusatz = zeilen[k][:3]
            zusatz = " ".join(t for t in (zusatz, f"Schachtel {z.schachtel}" if z.schachtel else "") if t)
            luecke(z, "Text", (text + ("  ¦ " + zusatz if zusatz else "")).strip(), fehlt, e)
    erg["anteil"] = erg["gefunden"] / erg["woerter"] if erg["woerter"] else 1.0
    return erg


def pruefe_rahmen(alle: list[Zeile], koerper: list[Zeile], start: int, vorkommen: list[Vorkommen],
                  toc: dict, modus: str) -> dict:
    """Was ausserhalb des Detailverzeichnisses liegt: Vorspann (Einleitung, Inhaltsverzeichnis), dort
    genannte Signaturen, die im Detailverzeichnis fehlen, und nicht wiederkehrende «Kopf-/Fusszeilen»."""
    erg: dict = {"vorspann_zeilen": start, "vorspann_seiten": "", "nur_im_vorspann": [], "kopf_fuss_einmalig": []}
    if start:
        erg["vorspann_seiten"] = f"{koerper[0].seite}–{koerper[start - 1].seite}"
    if modus == "dezimal":
        im_detail = {v.pfad for v in vorkommen}
        erg["nur_im_vorspann"] = [pfad_text(p) for p in toc if p not in im_detail]
    if start < len(koerper):
        ab = (koerper[start].seite, koerper[start].top)
        weg = [z for z in alle if (z.seite, z.top) >= ab and ist_kopf_oder_fuss(z)]
        muster = Counter(re.sub(r"\d+", "#", z.text) for z in weg)
        if koerper[-1].seite - koerper[start].seite >= 2:
            erg["kopf_fuss_einmalig"] = [{"seite": z.seite, "art": "Kopf-/Fusszeile (kommt nur einmal vor)",
                                          "zeile": z.text}
                                         for z in weg if muster[re.sub(r"\d+", "#", z.text)] == 1]
    return erg


# ----------------------------------------------------------------------------- Excel

SPALTEN = [
    # (Überschrift, Breite, Hilfsspalte?)
    ("ID", 7, False),
    ("Parent-ID", 9, False),
    ("Signatur", 20, False),
    ("Titel", 60, False),
    ("Stufe", 12, False),
    ("Ebene", 7, False),
    ("Teil", 6, False),
    ("Übergeordnete Signatur", 20, False),
    ("Entstehungszeitraum", 21, False),
    ("von", 11, False),
    ("bis", 11, False),
    ("Entstehungszeitraum, Anm.", 22, False),
    ("Darin", 80, False),
    ("Verwandte Verzeichnungseinheiten", 40, False),
    ("Umfang", 14, False),
    ("Schachtel-Nr.", 10, False),
    ("Nr. im PDF", 12, True),
    ("PDF-Seite", 9, True),
    ("Zeitraum-Quelle", 18, True),
    ("Prüfhinweise", 60, True),
]


def stufe(e: Einheit) -> str:
    if not e.anzeige and e.art == "knoten":
        return "Bestand"
    if e.art == "teil":
        return STUFE_EINHEIT
    if len(e.pfad) == 1 and e.eltern is None:
        if not e.kinder:
            return STUFE_EINHEIT
        # nur Teile derselben Nummer («124 Astrakhan …», «124 Limoges …») sind keine Gliederungsebene
        return STUFE_GRUPPE if all(k.art == "teil" for k in e.kinder) else STUFE_TIEFE_1
    return STUFE_GRUPPE if e.kinder else STUFE_EINHEIT


def ergaenze_doppelpunkte(einheiten: list[Einheit], bestand: str) -> None:
    """Schreibt das Findmittel seine Vollsignaturen (fast) immer «Bestand:Nummer», sind einzelne ohne «:» ein
    Schreibfehler: «VII. 47.1. Protokolle» neben «VII. 47.:2. Akten» (VII.47.), «V.J. c.402.16.» nach «V.J. c.402.:15.»
    (V.J.c.402.), «V.C. c.52. 54.» (V.C.c.52.), «V.J.P. b.53..5» (V.J.P.b.53.). Nicht bei Beständen, die das
    Findmittel nie mit «:» schreibt («III.G. 1.», «X.C. 1.»)."""
    def voll(e: Einheit) -> str:
        b = e.bestand or bestand
        n = normalisiere_signatur(e.roh) if e.roh else ""
        return n if b and n.startswith(b) and len(n) > len(b) and re.match(r"[\d:.]", n[len(b):]) else ""
    alle = [e for e in einheiten if voll(e)]
    mit = sum(1 for e in alle if ":" in e.roh)
    if len(alle) < 4 or mit < 0.75 * len(alle) or mit == len(alle):
        return
    for e in alle:
        if ":" in e.roh:
            continue
        b = e.bestand or bestand
        rest = voll(e)[len(b):].lstrip(".")
        if not re.fullmatch(r"\d{1,4}[a-z]?(?:\.\d{1,4}[a-z]?)*\.?(?:/\d{1,4})?", rest):
            continue
        e.doppelpunkt = b + ":" + rest
        e.hinweise.append(f"Signatur im Findmittel «{e.roh}» ohne Doppelpunkt – als «{e.doppelpunkt}» übernommen "
                          "(wie die übrigen Signaturen), bitte prüfen.")


def signatur(e: Einheit, bestand: str) -> str:
    bestand = e.bestand or bestand  # Findmittel für mehrere Bestände: der Bestand der Einheit
    if not e.anzeige:
        return bestand  # Findmittel ohne Signaturen: Zeile für den Bestand selbst
    if e.doppelpunkt:
        return e.doppelpunkt
    if len(e.pfad) == 1 and re.fullmatch(r"[a-z]", e.pfad[0]) and e.anzeige == f"{e.pfad[0]}.":
        return (bestand if bestand.endswith(":") else bestand + ":") + e.anzeige  # Kategorie «III.P.:e.»
    if normalisiere_signatur(e.roh).startswith(bestand) or (
            ":" in e.roh and normalisiere_signatur(e.roh).split(".")[:2] == bestand.split(".")[:2]
            and e.anzeige.startswith(":")):
        return normalisiere_signatur(e.roh)  # Vollsignatur aus dem PDF, ohne Leerzeichen/Doppelpunkte
    if e.anzeige[:1].isdigit() and re.match(r"[IVX]{1,4}\.", normalisiere_signatur(e.roh)) \
            and any("Tippfehler" in h for h in e.hinweise):
        return bestand + e.anzeige  # «V.B. 439.» in IV.B.: Bestandsteil berichtigt (Hinweis nennt die PDF-Form)
    if e.anzeige.startswith(":") and not bestand.endswith(":"):
        return bestand + e.anzeige  # «V.G. c.45.:10.» in V.H.c.45.: berichtigt, nicht «V.H.c.45.::10.»
    return (bestand if bestand.endswith(":") else bestand + ":") + e.anzeige


def ebene(e: Einheit) -> int:
    """Ebene unter dem Bestand = Zahl der übergeordneten Einheiten + 1 (auch unter Bereichen «VII.3.:6-16»)."""
    n, x = 1, e.eltern
    while x is not None:
        n, x = n + 1, x.eltern
    return n


def zeilen_fuer_excel(einheiten: list[Einheit], bestand: str, oben: str = "") -> list[dict]:
    """oben = übergeordnete Einheit des Bestands (aus dem Katalog) – nur für die Zeile des Bestands selbst."""
    zeilen = []
    for e in einheiten:
        sig = signatur(e, bestand)
        if e.art == "teil" and SIGNATUR_TEIL_MUSTER and e.teil_nr:
            sig = SIGNATUR_TEIL_MUSTER.format(sig=sig, teil=e.teil_nr)
        zr = e.zeitraum
        op = von = bis = anm = ""
        if zr and (zr.von or zr.bis):
            von, bis = (zr.von.text() if zr.von else ""), (zr.bis.text() if zr.bis else "")
            if von and von == bis:
                op, bis = OP_GENAU, ""  # wie in der Vorlage: bei «Genau» nur «von»
            else:
                op = OP_VON_BIS
                if not (von and bis):
                    e.hinweise.append("Offener Zeitraum (nur Beginn oder nur Ende).")
            if zr.original and zr.anmerkung_noetig and e.zeitraum_quelle in ("Datumsspalte", "Titel",
                                                                               "Inhaltsverzeichnis"):
                anm = zr.original
            if zr.ca and "ca" not in anm:
                anm = ("ca. " + anm).strip()
        if e.undatiert:
            anm = (anm + "; undatiert").strip("; ")
        darin = "\n".join(e.darin)
        if len(darin) > DARIN_MAX:  # Excel-Zelle fasst höchstens 32 767 Zeichen
            darin = darin[:DARIN_MAX].rsplit("\n", 1)[0] + f"\n[… gekürzt, Rest im PDF ab S. {e.seite}]"
            e.hinweise.append(f"Darin gekürzt ({len(e.darin)} Einträge) – vermutlich eine Tabelle; "
                              "evtl. in einzelne Einheiten aufteilen.")
        zeilen.append({
            "ID": e.id,
            "Parent-ID": e.eltern.id if e.eltern else "",
            "Signatur": sig,
            "Titel": e.titel,
            "Stufe": stufe(e),
            "Ebene": ebene(e),
            "Teil": e.teil_nr if e.art == "teil" and e.teil_nr else "",
            "Übergeordnete Signatur": (signatur(e.eltern, bestand) if e.eltern else
                                       (e.bestand or bestand) if e.anzeige else oben),
            "Entstehungszeitraum": op,
            "von": von,
            "bis": bis,
            "Entstehungszeitraum, Anm.": anm,
            "Darin": darin,
            "Verwandte Verzeichnungseinheiten": "\n".join(e.verweise),
            "Umfang": "; ".join(u for u in e.umfang if u),
            "Schachtel-Nr.": e.schachtel or "",
            "Nr. im PDF": e.roh,
            "PDF-Seite": e.seite,
            "Zeitraum-Quelle": e.zeitraum_quelle,
            "Prüfhinweise": "\n".join(dict.fromkeys(e.hinweise)),
            "_tiefe": ebene(e),
        })
    return zeilen


def _stile():
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    return {
        "schrift": Font(name="Arial", size=10),
        "fett": Font(name="Arial", size=10, bold=True),
        "kopf": Font(name="Arial", size=10, bold=True, color="FFFFFF"),
        "link": Font(name="Arial", size=10, color="0563C1", underline="single"),
        "titel": Font(name="Arial", size=12, bold=True),
        "abschnitt": Font(name="Arial", size=11, bold=True),
        "kopf_import": PatternFill("solid", fgColor="1F4E78"),
        "kopf_hilfe": PatternFill("solid", fgColor="7F7F7F"),
        "tb": PatternFill("solid", fgColor="DDEBF7"),
        "serie": PatternFill("solid", fgColor="F2F2F2"),
        "pruefen": PatternFill("solid", fgColor="FCE4D6"),
        "fehler": PatternFill("solid", fgColor="F8CBAD"),
        "linie": Border(bottom=Side(style="thin", color="BFBFBF")),
        "oben": Alignment(vertical="top", wrap_text=True),
        "mitte": Alignment(vertical="center", wrap_text=True),
    }


def _sauber(v):
    from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

    return ILLEGAL_CHARACTERS_RE.sub("", v) if isinstance(v, str) else v


def schreibe_excel(zeilen: list[dict], ziel: Path, meta: dict, pruefung: dict | None = None) -> None:
    from openpyxl import Workbook
    from openpyxl.comments import Comment
    from openpyxl.styles import Alignment
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.properties import Outline

    st = _stile()
    wb = Workbook()
    ws = wb.active
    ws.title = "scope-Import"
    namen = [s[0] for s in SPALTEN]
    breiten = {s[0]: s[1] for s in SPALTEN}
    for c, (name, breite, hilfe) in enumerate(SPALTEN, start=1):
        zelle = ws.cell(row=1, column=c, value=name)
        zelle.font, zelle.fill, zelle.alignment = st["kopf"], st["kopf_hilfe" if hilfe else "kopf_import"], st["mitte"]
        ws.column_dimensions[get_column_letter(c)].width = breite
        if hilfe:
            zelle.comment = Comment("Hilfsspalte zur Kontrolle – nicht importieren.", "findmittel_zu_scope")
    ws.row_dimensions[1].height = 30
    ws.sheet_properties.outlinePr = Outline(summaryBelow=False, summaryRight=False)
    sp = {n: i for i, n in enumerate(namen, start=1)}
    for r, z in enumerate(zeilen, start=2):
        stufe_ = z["Stufe"]
        gruppe = stufe_ in (STUFE_TIEFE_1, STUFE_GRUPPE)
        for name in namen:
            zelle = ws.cell(row=r, column=sp[name], value=_sauber(z[name]))
            zelle.font = st["fett"] if gruppe and name in ("Signatur", "Titel", "Stufe") else st["schrift"]
            zelle.alignment, zelle.border = st["oben"], st["linie"]
            if name in ("von", "bis", "Signatur", "Übergeordnete Signatur", "Nr. im PDF", "Schachtel-Nr."):
                zelle.number_format = "@"
            if stufe_ == STUFE_TIEFE_1:
                zelle.fill = st["tb"]
            elif stufe_ == STUFE_GRUPPE:
                zelle.fill = st["serie"]
        ws.cell(row=r, column=sp["Titel"]).alignment = Alignment(
            vertical="top", wrap_text=True, indent=min(max(z["_tiefe"] - 1, 0), 15))
        if z["Prüfhinweise"]:
            ws.cell(row=r, column=sp["Prüfhinweise"]).fill = st["pruefen"]
        ws.row_dimensions[r].outline_level = min(max(z["_tiefe"] - 1, 0), 7)
        ws.row_dimensions[r].height = _zeilenhoehe(z, breiten)
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(namen))}{len(zeilen) + 1}"

    wp = wb.create_sheet("Prüfliste")
    p_spalten = [("ID", 7), ("Signatur", 20), ("Titel", 60), ("PDF-Seite", 9), ("Prüfhinweise", 90)]
    for c, (name, breite) in enumerate(p_spalten, start=1):
        zelle = wp.cell(row=1, column=c, value=name)
        zelle.font, zelle.fill = st["kopf"], st["kopf_import"]
        wp.column_dimensions[get_column_letter(c)].width = breite
    r = 2
    for i, z in enumerate(zeilen, start=2):
        if not z["Prüfhinweise"]:
            continue
        for c, v in enumerate([z["ID"], z["Signatur"], z["Titel"], z["PDF-Seite"], z["Prüfhinweise"]], start=1):
            zelle = wp.cell(row=r, column=c, value=_sauber(v))
            zelle.font, zelle.alignment, zelle.border = st["schrift"], st["oben"], st["linie"]
        link = wp.cell(row=r, column=1)
        link.hyperlink, link.font = f"#'scope-Import'!A{i}", st["link"]
        wp.row_dimensions[r].height = 13.5 * max(z["Prüfhinweise"].count("\n") + 1,
                                                 -(-len(z["Prüfhinweise"]) // 95)) + 2
        r += 1
    wp.freeze_panes = "A2"
    wp.auto_filter.ref = f"A1:E{max(r - 1, 1)}"

    if pruefung is not None:
        _schreibe_vollstaendigkeit(wb.create_sheet("Vollständigkeit"), pruefung, st)
    _schreibe_info(wb.create_sheet("Info"), meta, st)
    wb.save(ziel)


def vollstaendigkeit_kurz(p: dict) -> dict:
    """Zusammenfassung der Vollständigkeitsprüfung (für das Blatt «Vollständigkeit» und das Info-Blatt)."""
    return {
        "Wörter im Detailverzeichnis": p["woerter"],
        "davon im Import gefunden": f"{p['gefunden']} ({p['anteil']:.2%})",
        "Zeilen mit fehlenden Wörtern": len(p["luecken"]) or "keine",
        "Nicht übernommen": (f"{len(p['nicht_uebernommen'])} Zeilen (Überschriften ohne Signatur, Text vor der "
                             "ersten Signatur – siehe Liste)" if p["nicht_uebernommen"] else "nichts"),
        "Schlussvermerke": f"{p['schluss']} Zeilen (stehen im Blatt «Info»)" if p["schluss"] else "–",
        "Übersichtszeilen": (f"{p['uebersicht']} Zeilen (Übersicht vor dem Verzeichnis, Einheiten kommen "
                             "im Verzeichnis nochmals)" if p["uebersicht"] else "–"),
        "Vorspann (nicht importiert)": (f"{p['vorspann_zeilen']} Zeilen auf S. {p['vorspann_seiten']} (Titelblatt, "
                                        "Einleitung, Inhaltsverzeichnis)" if p["vorspann_zeilen"] else "–"),
        "Signaturen nur im Vorspann": ", ".join(p["nur_im_vorspann"][:40]) or "–",
        "Kopf-/Fusszeilen, die nur einmal vorkommen": len(p["kopf_fuss_einmalig"]) or "–",
    }


def _schreibe_vollstaendigkeit(wv, p: dict, st: dict) -> None:
    from openpyxl.utils import get_column_letter

    wv.cell(row=1, column=1, value="Vollständigkeitsprüfung").font = st["titel"]
    erkl = wv.cell(row=2, column=1, value=(
        "Jedes Wort des Detailverzeichnisses wird in der Excel-Zeile der Einheit gesucht, zu der seine PDF-Zeile "
        "gehört (Signatur, Titel, Darin, Zeitraum, Anmerkung, Umfang, Schachtel). Datumsangaben zählen auch als "
        "gefunden, wenn sie in von/bis stecken. Unten stehen alle Zeilen, bei denen etwas fehlt, und alle Zeilen, "
        "die bewusst nicht übernommen wurden."))
    erkl.font, erkl.alignment = st["schrift"], st["oben"]
    wv.merge_cells(start_row=2, start_column=1, end_row=2, end_column=6)
    wv.row_dimensions[2].height = 42
    r = 4
    for k, v in vollstaendigkeit_kurz(p).items():
        a, b = wv.cell(row=r, column=1, value=k), wv.cell(row=r, column=3, value=_sauber(v))
        a.font, b.font, b.alignment = st["fett"], st["schrift"], st["oben"]
        wv.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
        wv.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
        r += 1
    r += 1
    spalten = [("PDF-Seite", 9), ("Art", 26), ("Zeile im PDF", 80), ("Fehlt im Import", 40), ("ID", 8),
               ("Signatur", 22)]
    for c, (name, breite) in enumerate(spalten, start=1):
        zelle = wv.cell(row=r, column=c, value=name)
        zelle.font, zelle.fill = st["kopf"], st["kopf_import"]
        wv.column_dimensions[get_column_letter(c)].width = breite
    kopf = r
    for eintrag in p["luecken"] + p["nicht_uebernommen"] + p["kopf_fuss_einmalig"]:
        r += 1
        werte = [eintrag["seite"], eintrag["art"], eintrag["zeile"], eintrag.get("fehlt", ""), eintrag.get("id", ""),
                 eintrag.get("signatur", "")]
        for c, v in enumerate(werte, start=1):
            zelle = wv.cell(row=r, column=c, value=_sauber(v))
            zelle.font, zelle.alignment, zelle.border = st["schrift"], st["oben"], st["linie"]
        if eintrag.get("fehlt"):
            wv.cell(row=r, column=4).fill = st["pruefen"]
        if eintrag.get("id"):
            link = wv.cell(row=r, column=5)
            link.hyperlink, link.font = f"#'scope-Import'!A{int(eintrag['id']) + 1}", st["link"]
    if r == kopf:
        wv.cell(row=r + 1, column=1, value="Keine Lücken – alles übernommen.").font = st["fett"]
    wv.freeze_panes = wv.cell(row=kopf + 1, column=1)


def _schreibe_info(wi, meta: dict, st: dict) -> None:
    wi.column_dimensions["A"].width = 36
    wi.column_dimensions["B"].width = 110
    r = 1
    for k, v in meta.items():
        if isinstance(v, dict):
            r += 1
            wi.cell(row=r, column=1, value=k).font = st["abschnitt"]
            r += 1
            for k2, v2 in v.items():
                a = wi.cell(row=r, column=1, value=k2)
                a.font, a.alignment = st["fett"], st["oben"]
                b = wi.cell(row=r, column=2, value=_sauber(v2))
                b.font, b.alignment = st["schrift"], st["oben"]
                wi.row_dimensions[r].height = 13.5 * max(1, -(-len(str(v2)) // 120) + str(v2).count("\n")) + 2
                r += 1
        else:
            a = wi.cell(row=r, column=1, value=k)
            a.font = st["titel"] if r == 1 else st["fett"]
            b = wi.cell(row=r, column=2, value=_sauber(v))
            b.font, b.alignment = st["schrift"], st["oben"]
            wi.row_dimensions[r].height = 13.5 * max(1, -(-len(str(v)) // 120) + str(v).count("\n")) + 2
            r += 1


def _zeilenhoehe(z: dict, breiten: dict) -> float:
    zeilen = 1
    for name in ("Titel", "Darin", "Prüfhinweise", "Verwandte Verzeichnungseinheiten"):
        text = str(z.get(name) or "")
        if text:
            zeichen = max(10, int(breiten[name] * 1.1))
            zeilen = max(zeilen, sum(max(1, -(-len(t) // zeichen)) for t in text.split("\n")))
    return min(13.5 * zeilen + 2, 180)


def schreibe_uebersicht(ergebnisse: list[dict], ziel: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter

    st = _stile()
    wb = Workbook()
    ws = wb.active
    ws.title = "Übersicht"
    spalten = [("PDF", 16), ("Bestand", 14), ("Status", 10), ("Gliederung", 13), ("Seiten", 8), ("Einheiten", 10),
               ("Teile", 8), ("mit Prüfhinweisen", 12), ("Anteil geprüft", 10), ("Text erfasst", 10),
               ("Zeilen mit Lücken", 10), ("nicht übernommen", 11), ("Excel", 28), ("Bemerkungen", 90),
               ("Online-Archiv", 60)]
    for c, (name, breite) in enumerate(spalten, start=1):
        zelle = ws.cell(row=1, column=c, value=name)
        zelle.font, zelle.fill, zelle.alignment = st["kopf"], st["kopf_import"], st["mitte"]
        ws.column_dimensions[get_column_letter(c)].width = breite
    for r, e in enumerate(ergebnisse, start=2):
        werte = [e["pdf"], e.get("bestand", ""), e["status"], e.get("gliederung", ""), e.get("seiten", ""),
                 e.get("einheiten", ""), e.get("teile", ""), e.get("hinweise", ""), e.get("anteil", ""),
                 e.get("text", ""), e.get("luecken", ""), e.get("nicht_uebernommen", ""),
                 e.get("excel", ""), "\n".join(e.get("bemerkungen", [])), e.get("katalog", "")]
        for c, v in enumerate(werte, start=1):
            zelle = ws.cell(row=r, column=c, value=_sauber(v))
            zelle.font, zelle.alignment, zelle.border = st["schrift"], st["oben"], st["linie"]
        ws.cell(row=r, column=9).number_format = "0%"
        ws.cell(row=r, column=10).number_format = "0.0%"
        if e["status"] != "OK":
            ws.cell(row=r, column=3).fill = st["fehler" if e["status"] == "Fehler" else "pruefen"]
        if e.get("luecken"):
            ws.cell(row=r, column=11).fill = st["pruefen"]
        if e.get("excel_pfad"):
            ws.cell(row=r, column=13).hyperlink = os.path.relpath(e["excel_pfad"], ziel.parent.resolve())
            ws.cell(row=r, column=13).font = st["link"]
        ws.row_dimensions[r].height = 13.5 * max(1, len(e.get("bemerkungen", []))) + 2
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = f"A1:O{len(ergebnisse) + 1}"
    wb.save(ziel)


# ----------------------------------------------------------------------------- Ablauf je PDF

BESTAND_RE = re.compile(r"(?<![\w.])([IVX]{1,4}\.\s?(?:(?:\d{1,4}|[A-Z]{1,3}|[a-z])\.\s?){1,5})(?![\w])")
# Überschrift eines Bestands in einem Findmittel für mehrere Bestände: «V.L. 150. Richard Wagner (1813 – 1883)»
BESTAND_KOPF_RE = re.compile(r"([IVX]{1,4}\.\s?[A-Z]{1,3}\.\s?(?:[a-z]\.\s?)?)(\d{1,4})\.\s+(?=[A-ZÄÖÜ\"„«])")


def finde_bestandswechsel(zeilen: list[Zeile], bestand: str) -> list[tuple[Zeile, str]]:
    """Findmittel für mehrere Bestände («V.L. 149. bis V.L. 162. Dokumentationen von W. G. Zimmermann»): je Bestand
    eine Überschrift «V.L. 150. Richard Wagner …» am linken Rand. Nur wenn der eigene Bestand und mindestens zwei
    weitere derselben Reihe so erscheinen, jeder einmal und in aufsteigender Folge. Ergebnis: (Zeile, Bestand)."""
    m = re.fullmatch(r"(.*?)(\d{1,4})\.", bestand)
    if not m or not zeilen:
        return []
    familie, links = m.group(1), min(z.x0 for z in zeilen)
    treffer = []
    for z in zeilen:
        mz = BESTAND_KOPF_RE.match(z.text) if z.x0 <= links + 5 else None
        if mz and re.sub(r"\s", "", mz.group(1)) == familie:
            treffer.append((z, f"{familie}{int(mz.group(2))}."))
    nummern = [int(s[len(familie):-1]) for _, s in treffer]
    if bestand not in {s for _, s in treffer} or len(set(nummern)) < 3 or nummern != sorted(set(nummern)):
        return []
    return treffer


def zusatz_aus_titel(aus_pdf: str, aus_katalog: str, titel: str) -> bool:
    """Ist der Teil der PDF-Signatur nach der Katalogsignatur nur der Anfang des Titels? Initialen eines Namens
    («VII. 241. J. H. Füssli» bei «Johann Heinrich Füssli (1741-1825)», «VII. 149. M. C. Wirth») oder eine Nummer
    im Titel («V.L. 146. 64. Eidgenössisches Turnfest»). Echte Unterbestände wie VII.308.A. oder VII.12.B. nicht."""
    extra = [k for k in aus_pdf[len(aus_katalog):].split(".") if k]
    if not extra:
        return False
    m = re.match(r"\s*" + r"\s*".join(re.escape(c) for c in aus_katalog), titel)  # Signatur vorn im Titel
    rest = titel[m.end():].strip() if m else titel.strip()
    if all(k.isdigit() for k in extra):
        return rest.startswith(f"{extra[0]}.")
    if not all(re.fullmatch(r"[A-Z]", k) for k in extra):
        return False
    muster = r"\s+".join(rf"{k}[a-zäöü]+" for k in extra)  # «Johann Heinrich», «Carl Anton» – mit Lebensdaten
    return re.search(rf"\b{muster}\b[^()]{{0,40}}\(\s*\d{{4}}", rest) is not None


def finde_bestand(zeilen: list[Zeile], alle: list[Zeile], meta: dict, pdf: Path) -> str | None:
    """Bestandssignatur aus dem Kopf von Seite 1 («Stadtarchiv Zürich VII. 143.»); eine längere Fassung
    aus der Kopfzeile der Folgeseiten («VII.12.B. Stadttheater …») gewinnt, wenn sie sie fortsetzt."""
    def treffer(text: str) -> str | None:
        m = BESTAND_RE.search(text)
        return re.sub(r"\s", "", m.group(1)) if m else None

    seite1 = [z for z in alle if z.seite == 1]
    basis = next((t for z in seite1 if "Stadtarchiv" in z.text and (t := treffer(z.text))), None) \
        or next((t for z in seite1[:8] if (t := treffer(z.text))), None)
    kopf = [t for z in alle if 2 <= z.seite <= 3 and z.top < 70 and all(w.size <= 10.5 for w in z.worte)
            and (t := treffer(z.text))]
    if basis:
        laengere = [k for k in kopf if k.startswith(basis) and len(k) > len(basis)]
        return max(laengere, key=len) if laengere else basis
    if kopf:
        return kopf[0]
    for quelle in (str(meta.get("Title", "")), pdf.stem):  # «Findmittel_VII-200_…», «VII. 143. Frieda …»
        m = re.search(r"Findmittel_([IVX]{1,4}(?:-[A-Za-z0-9]{1,4}){1,5})(?=[_.\s]|$)", quelle)
        if m:
            return m.group(1).replace("-", ".") + "."
        if t := treffer(quelle):
            return t
    return None


INHALT_RE = re.compile(r"(?:Inhalt|INHALT|Inhaltsverzeichnis|INHALTSVERZEICHNIS|Inhaltsübersicht)\s*:?")
DETAIL_RE = re.compile(r"^(?:[A-Z]\.\s+|[IVX]{1,4}\.\s+)?(DETAILVERZEICHNISSE|Detailverzeichnisse|"
                       r"DETAILVERZEICHNIS|Detailverzeichnis|Verzeichnis|VERZEICHNIS|"
                       r"Inventar|INVENTAR|Detailinventar)$")


def _titelkern(t: SigTreffer) -> tuple[str, ...]:
    """Die ersten drei Wörter des Titels («Statuten der Theater…»), ohne Punktleitern und Seitenzahlen."""
    text = saeubere(t.rest.text) if t.rest else ""
    text = re.sub(r"\s*\.{2,}.*$|\s+\d{1,3}$", "", text)
    return tuple(w.lower() for w in re.findall(r"[^\W\d_]{2,}", text)[:3])


def _sieht_aus_wie_verzeichnis(block: list[Zeile]) -> bool:
    """Seitenzahlen bzw. Punktleitern rechts in vielen Zeilen, keine Aufzählungen: Inhaltsverzeichnis."""
    if not block:
        return False
    seiten = sum(1 for z in block if re.search(r"\.{4,}|…{2,}", z.text) or (
        len(z.worte) >= 2 and re.fullmatch(r"\d{1,3}", z.worte[-1].text) and z.worte[-1].x0 - z.worte[-2].x1 >= 10))
    aufz = sum(1 for z in block if ist_aufzaehlung(z))
    return seiten >= 0.3 * len(block) and aufz <= 0.05 * len(block)


def finde_detailbeginn(zeilen: list[Zeile], modus: str, bestand: str) -> tuple[int, str]:
    """Index der ersten Zeile des Detailverzeichnisses (davor: Titelblatt, Einleitung, Übersicht/Inhaltsverzeichnis).

    Ohne Überschrift «Detailverzeichnis» gilt eine frühere Nennung der ersten Signatur nur dann als Übersicht
    bzw. Inhaltsverzeichnis, wenn mindestens die Hälfte ihrer Einträge später mit gleicher Signatur und gleichem
    Titelanfang wiederkommt oder der Abschnitt klar wie ein Verzeichnis aussieht (Seitenzahlen, Punktleitern).
    Sonst beginnt das Verzeichnis am Anfang – lieber eine doppelte Übersichtszeile als verschluckte Einheiten
    (eine Mengenangabe «1 Schachtel …» oder eine neu beginnende Zählung «1.» weiter hinten ist kein Beginn)."""
    eintraege: list[tuple[int, tuple, tuple]] = []
    voll_bei: set[int] = set()  # Zeilen mit Vollsignatur («III.Q. 2.-4. b) Amtsordnungen»)
    for i, z in enumerate(zeilen):
        t = lies_signatur(z, Gliederung(modus, bestand, nur_pruefen=True))
        if t is not None:
            eintraege.append((i, t.pfad, _titelkern(t)))
            if t.typ == "voll":
                voll_bei.add(i)

    def nur_verzeichnis_davor(i: int) -> bool:
        """Stehen vor Zeile i keine Einheiten – oder nur solche, die danach wiederkommen (Inhaltsverzeichnis)?"""
        davor = [(pfad, kern) for j, pfad, kern in eintraege if j < i and kern]
        danach = {(pfad, kern) for j, pfad, kern in eintraege if j > i and kern}
        return not davor or sum(1 for e in davor if e in danach) >= 0.5 * len(davor)

    def nach_inhalt(start: int) -> int:
        """«Detailverzeichnis» / «Inhalt» / «1. … 8», «2. … 8», «3. … 13»: das Verzeichnis beginnt erst, wo der erste
        Eintrag wiederkommt (VII.494.)."""
        if start >= len(zeilen) or not INHALT_RE.fullmatch(zeilen[start].text.strip()):
            return start
        nach = [(i, pfad) for i, pfad, _ in eintraege if i > start]
        wieder = next((i for i, pfad in nach[1:] if pfad == nach[0][1]), None) if nach else None
        if wieder is not None and _sieht_aus_wie_verzeichnis(zeilen[nach[0][0]:wieder]):
            return wieder
        return start

    # «Detailverzeichnis», «Inventar» gelten immer – und vor einem blossen «Verzeichnis» weiter oben (VII.163.:
    # «VERZEICHNIS» / «A. INVENTARÜBERSICHT» … / «B. DETAILVERZEICHNIS»); ein blosses «Verzeichnis» kann auch
    # mitten im Inhalt stehen
    treffer_detail = [(i, m) for i, z in enumerate(zeilen) if (m := DETAIL_RE.fullmatch(z.text.strip()))]
    stark = [i for i, m in treffer_detail if "etail" in m.group(1) or "ETAIL" in m.group(1)]
    if stark:
        # «Detailverzeichnis» / «Allgemeine Hinweise» 1.–7. / «Findmittel» … / «Detailverzeichnis Archivbestand»
        # (VII.47.): erst die zweite Überschrift beginnt das Verzeichnis, davor steht die Einleitung
        einleitung = any(re.fullmatch(r"(?:Allgemeine Hinweise|Einleitung|Vorbemerkungen?|Bestandesgeschichte)\s*:?",
                                      z.text.strip()) for z in zeilen[stark[0] + 1:stark[0] + 6])
        spaeter = next((i for i, z in enumerate(zeilen) if i > stark[0] and re.fullmatch(
            r"Detail(?:verzeichnis|inventar)\s+(?:des\s+|zum\s+)?(?:Archivbestand|Bestand)(?:es|s)?", z.text.strip())), None)
        if einleitung and spaeter is not None:
            return nach_inhalt(spaeter + 1), ""
        return nach_inhalt(stark[0] + 1), ""
    basis = 0
    for i, m in treffer_detail:  # «Inventar», «Verzeichnis»: nur ohne Einheiten davor (bzw. nur Inhaltsverzeichnis)
        if m.group(1) in ("Inventar", "INVENTAR") and i < 3 or nur_verzeichnis_davor(i):
            basis = nach_inhalt(i + 1)
            break
    # auch nach «Verzeichnis» kann noch eine Übersicht stehen, deren Einträge im Verzeichnis wiederkommen
    # («Verzeichnis» / «1. Kopie der Gründungsakten» … «5. Jahresrechnungen und Berichte» / Einleitung / fett
    # «1. Kopie der Gründungsakten Schachtel 1», VII.236.)
    eintraege = [e for e in eintraege if e[0] >= basis]
    if not eintraege:
        return basis, ""
    # «Vorbemerkung» / «1. Die fortlaufenden Aktennummern korrespondieren …» / «2. In den Akten finden sich auch: …» /
    # Tabellenkopf «Signatur ¦ Inhalt ¦ Jahre» / «V.J.W. c.12.:1. ¦ Schachtel 1» (V.J.W.c.12.): die nummerierten
    # Bemerkungen sind Vorspann, das Verzeichnis beginnt nach dem Tabellenkopf
    kopf_v = next((k for k in range(basis, min(len(zeilen), basis + 60))
                   if re.match(r"Signatur\b.*\b(?:Inhalt|Titel)\b", zeilen[k].text.strip())), None)
    if kopf_v is not None and any(re.fullmatch(r"(?:Vorbemerkung(?:en)?|Bemerkungen|Hinweise|Anmerkungen)\s*:?",
                                               zeilen[k].text.strip()) for k in range(basis, kopf_v)):
        nach_kopf = [i for i, _, _ in eintraege if i > kopf_v]
        if nach_kopf and nach_kopf[0] in voll_bei and any(i < kopf_v for i, _, _ in eintraege):
            return kopf_v + 1, (f"Vorbemerkung mit nummerierten Punkten vor dem Tabellenkopf «{zeilen[kopf_v].text.strip()}» "
                                "als Vorspann übersprungen.")
    erste = eintraege[0][1]
    positionen = [i for i, pfad, _ in eintraege if pfad == erste]
    start = 0
    nach_gruppen = False  # Übersicht mit eigener Zählung: ihre Zeiträume gelten nicht für die Einheiten
    for a, b in zip(positionen, positionen[1:]):
        block = [(pfad, kern) for i, pfad, kern in eintraege if a <= i < b and kern]
        nachher = {(pfad, kern) for i, pfad, kern in eintraege if i >= b and kern}
        wiederholt = sum(1 for e in block if e in nachher)
        # viele Aufzählungen im Block: ein echtes Verzeichnis, das sich wiederholt (V.G.c.50.: Ämter A.–P. für
        # 1931–1933 und nochmals für 1937–1948), keine Übersicht
        aufz = sum(1 for z in zeilen[a:b] if ist_aufzaehlung(z))
        if b - a >= 80 and aufz >= 0.15 * (b - a):
            break  # (nur lange Blöcke – eine kurze Übersicht mit «–»-Listen bleibt Übersicht, VII.277. S. 4)
        # kurze Liste direkt unter «Übersicht», deren Zählung im Verzeichnis neu beginnt («Übersicht» / «1. Amtliches
        # 1869 – 1908», «2. Privates», «3. Gratulationsdiplome» / S. 2 «Schachtel 1 – Amtliches» / «1. Weisungen und
        # Berichte …», VII.75.): eine Übersicht nach Gruppen, auch wenn die Titel nicht wiederkommen
        # (nur bei eigener Zählung der Übersicht, nicht bei Vollsignaturen «III.Q. 1. a) Kopialbücher», III.Q.)
        uebersicht_kopf = a == positionen[0] and len(block) >= 2 and b - a <= 40 \
            and not any(a <= i < b for i in voll_bei) and any(
            re.fullmatch(r"(?:[a-z]\)\s*|[A-Z]\.\s*)?(?:Übersicht|ÜBERSICHT|Inhaltsübersicht|INHALTSÜBERSICHT|"
                         r"Inventarübersicht|INVENTARÜBERSICHT)\s*:?", zeilen[k].text.strip())
            for k in range(max(basis, a - 3), a))
        # (nach einer Überschrift «Verzeichnis» nur bei echter Wiederholung: eine Bände-Spalte «1. Protokoll ¦ 1 ¦
        # 1861-1873» sieht sonst wie Seitenzahlen aus, VII.65.)
        if (len(block) >= 2 and wiederholt >= 0.5 * len(block)) \
                or (not basis and _sieht_aus_wie_verzeichnis(zeilen[a:b])):
            start = b
        elif uebersicht_kopf:
            start, nach_gruppen = b, True
        else:
            break
    if not start:
        return basis, ""
    while start > 0 and SCHACHTEL_RE.match(zeilen[start - 1].text.strip()):
        start -= 1  # «Schachtel 1a» direkt über der ersten Einheit gehört dazu (VII.179.)
    if nach_gruppen:
        return start, (f"Übersicht nach Gruppen bis S. {zeilen[start - 1].seite} übersprungen (eigene Zählung; ihre "
                       "Zeiträume wurden nicht übernommen).")
    return start, ("Überschrift «Detailverzeichnis» fehlt – Übersicht/Inhaltsverzeichnis bis S. "
                   f"{zeilen[start - 1].seite if start else 1} übersprungen (Einträge kommen im Verzeichnis wieder).")


def lies_katalog(pfad: Path) -> dict[str, dict]:
    """Liste aus findmittel_laden.py: Dateiname (D….pdf) -> {signatur, titel, ve_id}. Liegt daneben der Rundgang
    durch den Archivplan (verzeichnis.rundgang.jsonl), kommt die übergeordnete Einheit dazu («eltern_signatur»,
    z. B. V.A.c.17.a. -> V.A.c.) – für die Zeile des Bestands selbst (Findmittel ohne Signaturen)."""
    import csv

    with pfad.open(encoding="utf-8-sig") as f:
        katalog = {Path(z["pfad"]).name: z for z in csv.DictReader(f, delimiter=";")}
    rundgang = pfad.with_name(pfad.stem + ".rundgang.jsonl")
    if rundgang.exists():
        knoten = {}
        with rundgang.open(encoding="utf-8") as f:
            for zeile in f:
                if zeile.strip():
                    r = json.loads(zeile)
                    knoten[str(r["ve_id"])] = r
        eltern: dict[str, str] = {}  # «kind» = erstes Kind, «naechster» = nächstes Geschwister
        for ve_id, r in knoten.items():
            k = r.get("kind")
            while k is not None and str(k) in knoten and str(k) not in eltern:
                eltern[str(k)] = ve_id
                k = knoten[str(k)].get("naechster")
        for z in katalog.values():
            oben = knoten.get(eltern.get(str(z.get("ve_id", "")), ""))
            if oben and oben.get("signatur"):
                z["eltern_signatur"] = re.sub(r"\s", "", oben["signatur"])
    return katalog


def registraturgruppen(vorkommen: list[Vorkommen]) -> None:
    """Registraturplan mit dreistelligen Codes: fett «430.1.020 Organisatorische Grundlagen» (14 pt) / «430.1.021
    Gesetzliche Grundlagen», «430.1.022 …», «430.1.023.1 …» / fett «430.1.600 Personelles» / «430.1.601 …» (V.F.c.29.):
    ein fetter Code mit Endnull ist die Gruppe der folgenden Codes seines Zehner- bzw. Hunderterbereichs (wie 011 unter
    010) – sonst stehen alle Codes gleich tief nebeneinander."""
    def code(v: Vorkommen, k: int) -> str | None:
        return v.pfad[k] if len(v.pfad) > k and re.fullmatch(r"\d{3}", v.pfad[k]) else None
    dreistellig = [v for v in vorkommen if v.typ == "zahl" and any(re.fullmatch(r"\d{3}", k) for k in v.pfad)]
    # (nur echte Codes: alle Geschwister dreistellig, also «020», «021» – nicht eine fortlaufende Zählung «11.99.»,
    # «11.100.», «11.101.», V.E.c.53.)
    geschwister: dict[tuple, set[int]] = {}
    for v in vorkommen:
        if v.typ == "zahl" and v.pfad and v.pfad[-1].isdigit():
            geschwister.setdefault(v.pfad[:-1], set()).add(len(v.pfad[-1]))
    kandidaten = [v for v in dreistellig if v.fett and re.fullmatch(r"\d{2}0", v.pfad[-1])
                  and geschwister.get(v.pfad[:-1]) == {3}]
    if len(dreistellig) < 5 or len(kandidaten) < 2:
        return
    stapel: list[tuple[tuple, int, str]] = []  # (neuer Pfad der Gruppe, Stelle des Codes, Code)

    def im_bereich(g_code: str, c: str) -> bool:
        if g_code.endswith("00"):
            return c[0] == g_code[0] and c != g_code
        return c[:2] == g_code[:2] and c != g_code
    for v in vorkommen:
        if v.typ != "zahl" or v.ist_teil:
            continue
        while stapel:
            g_pfad, k, g_code = stapel[-1]
            c = code(v, k)
            if c is not None and v.pfad[:k] == g_pfad[:k] and im_bereich(g_code, c):
                break
            stapel.pop()
        alt = v.pfad
        if stapel:
            g_pfad, k, _ = stapel[-1]
            v.pfad = g_pfad + alt[k:]
        if v.fett and len(alt) >= 1 and re.fullmatch(r"\d{2}0", alt[-1]) and geschwister.get(alt[:-1]) == {3}:
            stapel.append((v.pfad, len(alt) - 1, alt[-1]))


def gruppen_unter_letzter_schachtel(vorkommen: list[Vorkommen]) -> None:
    """«Schachtel 5» / «Verhandlungen im Gemeinderat 1946 - 1971» / … «Die Aktensammlung ist gegliedert in folgende
    Gruppen:» / «I. Vorstösse im Gemeinderat …» … «XV. Y-Diskussion …» (V.B.c.34.): die Gruppen nach der letzten
    Schachtel sind deren Faszikel – Kinder der Schachtel und mit ihrer Nummer, nicht Geschwister der Schachteln."""
    boxen = [v for v in vorkommen if (v.aus_marke or v.typ == "behaelter") and not v.ist_teil and len(v.pfad) == 1]
    if not boxen:
        return
    b = max(boxen, key=lambda v: (v.seite, int(re.match(r"\d*", v.pfad[0]).group() or 0)))
    rest = [v for v in vorkommen if v not in boxen]
    if not rest or not all(v.typ == "roem" for v in rest if len(v.pfad) == 1) \
            or not all(v.seite >= b.seite for v in rest) \
            or not any(re.search(r"\bgegliedert in (?:die )?folgenden? Gruppen\b|\bfolgende Gruppen\s*:", x.text)
                       for x in b.zeilen):
        return
    b.hinweise.append("Die Gruppen nach dieser Schachtel («Die Aktensammlung ist gegliedert in folgende Gruppen:») als "
                      "ihre Untereinheiten übernommen.")
    for v in rest:
        v.pfad = b.pfad + v.pfad
        if not v.schachtel:
            v.schachtel, v.schachtel_geerbt = b.schachtel, True


def buchstaben_unter_einziger_nummer(vorkommen: list[Vorkommen]) -> None:
    """Einzige Vollsignatur mit Nummer, danach nur Buchstaben: «V.B. c.12.:1 Allgemeines» / «a) Gebühren, Formelles» /
    «b) Informationen betreffend Bürgerrecht» (V.B.c.27., einzige Nummer im Findmittel) – a) und b) sind 1.a und 1.b,
    nicht Kategorien am Bestand (anders die Kategorien a)–e) unter vielen Vollsignaturen in III.G., III.P.)."""
    voll = [v for v in vorkommen if v.typ == "voll"]
    if len(voll) != 1 or len(voll[0].pfad) != 1 or not voll[0].pfad[0].isdigit():
        return
    k = vorkommen.index(voll[0])
    rest = vorkommen[k + 1:]
    if not rest or vorkommen[:k] or not all(v.typ == "klein" and len(v.pfad) == 1 for v in rest):
        return
    for v in rest:
        v.pfad = voll[0].pfad + v.pfad


def korrigiere_buchstaben_geschwister(vorkommen: list[Vorkommen]) -> None:
    """Vollsignatur «n.a» mit demselben Titel wie «n.» direkt davor: «VII. 7.:18. Totenregister (Gräberverzeichnis) ¦
    1874-1886 ¦ 1 Band» / «VII. 7.:18.a Totenregister (Gräberverzeichnis) ¦ 1839-1891 ¦ 3 Bände» / «:18.a:1 Band 1» …
    (VII.7.) – ein zweites Register neben 18. (wie «3a.» neben «3.»), kein Kind von 18.; seine Bände hängen darunter.
    Ebenso mehrere Buchstaben in Folge und bei Dezimalsignaturen («5.6.13. Journal 1860/61» / «5.6.13.a. Journal
    1864/65» … «5.6.13.w.», als Nachträge einsortiert, VII.12.A.), mit anderem Titel, wenn beide als Listeneintrag eigenen
    Umfang bzw. eigenes Datum haben («IV.B.1. Rechnungen der Stadtkanzlei ¦ 1840–1861 ¦ 22 Bände» / «IV.B.1.a) Rechnung
    über den Kasernenbau im Talacker ¦ 1798–1799 ¦ 1 Band», IV.B.) – immer in derselben Spalte wie «n.» und nur, wenn
    «n.» keine anderen Unternummern hat."""
    def titel(v: Vorkommen) -> str:  # (ohne Jahreszahlen: «Journal 1839/40» / «Journal 1840/41»)
        return _titelanfang(re.sub(r"\d+", " ", v.zeilen[0].text)) if v.zeilen and v.zeilen[0].worte else ""

    def eigene_angaben(v: Vorkommen) -> bool:
        return bool(v.umfang or v.datum)
    k = 0
    while k < len(vorkommen) - 1:
        p_v = vorkommen[k]
        basis = p_v.pfad
        k += 1
        if p_v.typ not in ("voll", "zahl") or p_v.ist_teil or not basis or not basis[-1].isdigit():
            continue
        lauf, j = [], k
        while j < len(vorkommen) and len(vorkommen[j].pfad) > len(basis) and vorkommen[j].pfad[:len(basis)] == basis \
                and re.fullmatch(r"[a-z]", vorkommen[j].pfad[len(basis)]):
            lauf.append(vorkommen[j])
            j += 1
        direkt = [v for v in lauf if len(v.pfad) == len(basis) + 1 and not v.ist_teil]
        if not direkt or direkt[0] is not lauf[0] or direkt[0].pfad[-1] != "a" or any(v.typ != p_v.typ for v in direkt):
            continue
        if any(v.pfad[:len(basis)] == basis and len(v.pfad) > len(basis) for v in vorkommen[:k - 1] + vorkommen[j:]):
            continue  # n. hat weitere Kinder: die Buchstaben sind doch eine Unterstufe
        if not all((not p_v.x0 or not v.x0 or abs(v.x0 - p_v.x0) <= 3)
                   and (titel(p_v) and titel(p_v) == titel(v) or eigene_angaben(p_v) and eigene_angaben(v))
                   for v in direkt):
            continue
        for v in lauf:
            v.pfad = basis[:-1] + (basis[-1] + v.pfad[len(basis)],) + v.pfad[len(basis) + 1:]
        k = j


def unternummern_im_text(vorkommen: list[Vorkommen], info: dict, bestand: str) -> None:
    """Unternummern einer Vollsignatur im Text: eingerückt am Zeilenanfang «X.G.93. * Zender, Rudolf. Drahtschmidli.
    Lithographie (Grf.):» / «X.G.93.:1 « Blauer Himmel » , Zürich 1958 (1 Expl.)» / «X.G.93.:2 …», in Klammern am
    Zeilenende «X.G.200. Zürich. Stadtführer …, 1977 (X.G.200.:1)» / «Zurich City Guide … (X.G.200.:2)» oder im
    Fliesstext «… (200 Stück) (X.G.209.:1); flache Taschenmesser (X.G.209.:2); …» (X.G.) – eigene Einheiten darunter."""
    ergebnis: list[Vorkommen] = []
    for v in vorkommen:
        ergebnis.append(v)
        if v.typ != "voll" or v.ist_teil or len(v.pfad) != 1 or not v.zeilen:
            continue
        sig = f"{bestand}{v.anzeige}"
        marke_re = re.compile(rf"^\(?{re.escape(sig)}:(\d{{1,3}})\)?[;,.]?$")
        worte = [(k, w) for k, z in enumerate(v.zeilen) for w in z.worte]
        marken = [(n, int(marke_re.match(w.text).group(1))) for n, (k, w) in enumerate(worte) if marke_re.match(w.text)]
        if len(marken) < 2 or [m for _, m in marken] != list(range(1, len(marken) + 1)):
            continue
        am_anfang = all(n > 0 and worte[n - 1][0] != worte[n][0] for n, _ in marken)
        items: list[tuple[int, list]] = []
        if am_anfang:
            for i_m, (n, m) in enumerate(marken):
                ende_m = marken[i_m + 1][0] if i_m + 1 < len(marken) else len(worte)
                items.append((m, worte[n + 1:ende_m]))
            kopf = worte[:marken[0][0]]
        else:
            anfang = 0
            for n, m in marken:
                items.append((m, worte[anfang:n]))
                anfang = n + 1
            if worte[anfang:]:  # Text nach der letzten Marke gehört zur letzten Unternummer
                items[-1] = (items[-1][0], items[-1][1] + worte[anfang:])
            kopf = []
        if any(not ws for _, ws in items):
            continue
        def als_zeile(ws: list) -> Zeile:
            z0 = v.zeilen[ws[0][0]]
            return Zeile(z0.seite, z0.top, z0.bottom, [w for _, w in ws], z0.datum, z0.umfang)
        kinder = []
        for m, ws in items:
            kind = Vorkommen(v.pfad + (str(m),), f"{v.anzeige}:{m}", f"{sig}:{m}", v.zeilen[ws[0][0]].seite,
                             [als_zeile(ws)], typ="voll", x0=v.x0, schachtel=v.schachtel)
            kind.hinweise.append(f"Unternummer «{sig}:{m}» steht im Findmittel im Text von {sig} – als eigene Einheit "
                                 "übernommen, bitte prüfen.")
            kinder.append((kind, {k for k, _ in ws}))
        if kopf:
            v.zeilen = [als_zeile(kopf)]
        else:
            v.zeilen = [als_zeile(items[0][1])]
            v.hinweise.append("Titel aus der ersten Unternummer übernommen (das Findmittel nennt nur die Unternummern) – "
                              "Sammeltitel bitte prüfen.")
        # Zeilenzuordnung für die Vollständigkeit: jede Zeile zur Unternummer mit den meisten ihrer Wörter (ausser der
        # Titelzeile von X.G.93., die beim Kopf bleibt)
        kopf_ids = {id(w) for _, w in kopf} if kopf else {id(w) for w in v.zeilen[0].worte}
        for vb in info.get("verbleib", []):
            if vb.vorkommen is not v or not vb.zeile.worte:
                continue
            ids = {id(w) for w in vb.zeile.worte}
            if kopf and ids & kopf_ids:
                continue
            bester = max(kinder, key=lambda kk: len(ids & {id(w) for w in kk[0].zeilen[0].worte}))
            if ids & {id(w) for w in bester[0].zeilen[0].worte}:
                vb.vorkommen = bester[0]
        ergebnis.extend(kind for kind, _ in kinder)
    vorkommen[:] = ergebnis


def nummern_aus_eingeschobener_uebersicht(vorkommen: list[Vorkommen]) -> None:
    """Nummer, die nur in einer eingeschobenen Übersicht im Darin eines Bereichs steht: «50 – 58 Publikationen und
    Zeitungsausschnitte» / «Übersicht …: 50 Offizielle Publikationen …» … «57 Zeitungsausschnitte (1)» / «58
    Zeitungsausschnitte (2)», im Detail nur «57 – 58 Zeitungsausschnitte (2 Schachteln)» und «58 …» (VII.80.) – Einheit
    57 aus der Übersicht, vor 58."""
    def bereich(v: Vorkommen) -> tuple[int, int] | None:
        m = re.fullmatch(r"(\d{1,4})-(\d{1,4})", v.pfad[0]) if len(v.pfad) == 1 else None
        return (int(m.group(1)), int(m.group(2))) if m and int(m.group(1)) < int(m.group(2)) else None
    pfade = {v.pfad for v in vorkommen}
    for v in list(vorkommen):
        b_v = bereich(v)
        if b_v is None or v.ist_teil:
            continue
        for z in v.zeilen[1:]:
            m = re.match(r"(?:.*:\s)?(\d{1,4})\s+([A-ZÄÖÜ„“\"«].{2,80})$", z.text.strip())
            if not m or not b_v[0] <= int(m.group(1)) <= b_v[1] or (m.group(1),) in pfade:
                continue
            n = int(m.group(1))
            # nur in einem engeren Bereich des Details, dem diese Nummer fehlt («57 – 58» mit nur 58)
            innen = [x for x in vorkommen if x is not v and bereich(x) and bereich(x)[0] <= n <= bereich(x)[1]
                     and b_v[0] <= bereich(x)[0] and bereich(x)[1] <= b_v[1]]
            if not innen:
                continue
            nach_k = next((k for k, x in enumerate(vorkommen) if len(x.pfad) == 1 and x.pfad[0].isdigit()
                           and int(x.pfad[0]) > n and vorkommen.index(innen[0]) < k), None)
            if nach_k is None:
                continue
            titel_w = z.worte[next(k for k, w in enumerate(z.worte) if w.text == m.group(1)) + 1:] \
                if any(w.text == m.group(1) for w in z.worte) else z.worte[1:]
            if not titel_w:
                continue
            folge = vorkommen[nach_k]  # (Schreibweise wie die Nachbarn: «58.» → «57.»)
            anzeige_n = m.group(1) + ("." if folge.anzeige.endswith(".") else "")
            neu_v = Vorkommen((m.group(1),), anzeige_n, m.group(1), z.seite,
                              [Zeile(z.seite, z.top, z.bottom, list(titel_w), z.datum, z.umfang)], x0=innen[0].x0)
            neu_v.hinweise.append(f"Nur in der Übersicht im Bereich {v.anzeige} verzeichnet («{z.text.strip()[:60]}», "
                                  f"S. {z.seite}) – als Einheit übernommen, bitte prüfen.")
            vorkommen.insert(nach_k, neu_v)
            pfade.add(neu_v.pfad)


def aufzaehlung_unter_jahrnummer(vorkommen: list[Vorkommen], info: dict) -> None:
    """Aufzählung a)–c) in der Textspalte unter einer Jahr.Laufnummer mit Schachtel: «1966.19 Zürich, Hürlimann
    Brauerei AG, Brandschenkestrasse 150 ¦ 118» / «a) Lagerhalle Nr. 4 neue Tankbelegung» / «b) Velounterstand» / «c)
    …» (VII.308.F.a.) – ohne eigene Schachtel keine Unterstufen, sondern Darin der Einheit."""
    weg: set[int] = set()
    for k, v in enumerate(vorkommen):
        if v.typ != "klein" or len(v.pfad) != 2 or not re.fullmatch(r"\d{4}\.\d{1,4}", v.pfad[0]) or v.schachtel \
                or len(v.zeilen) != 1:
            continue
        eltern = next((x for x in reversed(vorkommen[:k]) if x.pfad == v.pfad[:1] and not x.ist_teil), None)
        if eltern is None or not eltern.schachtel or not (v.x0 and eltern.x0 and v.x0 > eltern.x0 + 20):
            continue
        z_v = v.zeilen[0]
        zeile_neu = Zeile(z_v.seite, z_v.top, z_v.bottom, [Wort(v.roh, z_v.x0 - 15, z_v.x0 - 3, z_v.worte[0].font,
                                                                 z_v.worte[0].size)] + list(z_v.worte),
                          z_v.datum, z_v.umfang)
        eltern.zeilen.append(zeile_neu)
        for vb in info.get("verbleib", []):
            if vb.vorkommen is v:
                vb.vorkommen = eltern
        weg.add(id(v))
    if weg:
        vorkommen[:] = [v for v in vorkommen if id(v) not in weg]


def hinweis_doppelte_signatur(vorkommen: list[Vorkommen]) -> None:
    """Dieselbe Signatur genau zweimal hintereinander mit ganz anderem Titel: «7.4.1.26. „Evaluation der kantonalen
    Aktivitäten im Kampf gegen HIV / AIDS“, Projektbeschrieb» / «7.4.1.26. „Pathologies somatiques liées à la
    Toxicomanie“» (VII.423.) – nach der Konvention ein Teil, aber wohl ein Tippfehler: Hinweis."""
    def erstes_wort(v: Vorkommen) -> str:
        t = re.sub(r"[^\w\s]", " ", v.zeilen[0].text).lower().split() if v.zeilen and v.zeilen[0].worte else []
        return t[0] if t else ""
    zaehl = Counter(v.pfad for v in vorkommen if v.typ in ("zahl", "voll"))
    # (nur, wo Teile die Ausnahme sind – in VII.200. mit fast der Hälfte Teilen sind sie die Form des Verzeichnisses)
    if sum(1 for v in vorkommen if v.ist_teil) > 0.02 * len(vorkommen):
        return
    for a, b in zip(vorkommen, vorkommen[1:]):
        if b.ist_teil and not a.ist_teil and a.pfad == b.pfad and zaehl[a.pfad] == 2 and a.typ in ("zahl", "voll") \
                and erstes_wort(a) and erstes_wort(b) and erstes_wort(a) != erstes_wort(b) \
                and not any(re.match(r"(?:Teil|Band|Bd\.|Mappe|Schachtel|Heft|Nr\.|\d)", (v.zeilen[0].text.strip()
                                                                                       if v.zeilen else ""))
                            for v in (a, b)) \
                and not any("zweimal" in h or "erneut" in h for h in b.hinweise):
            b.hinweise.append(f"Signatur {b.anzeige} steht im Findmittel zweimal hintereinander mit anderem Titel – "
                              "Tippfehler? Als Teil übernommen, bitte prüfen.")


def korrigiere_doppelnummern(vorkommen: list[Vorkommen]) -> None:
    """Tippfehler in einer laufenden Nummernfolge: eine Nummer fehlt, die Nachbarnummer steht doppelt – «V.G. a.13.:111
    … 1951», «:113 … 1952», «:113 … 1953», «:114 … 1954» (V.G.a.13.; ebenso «:13», «:15», «:15», «:16», V.G.a.15.): die
    erste 113 ist 112 (sonst Teil 2 von 113 und ein Sprung 111 → 113); ebenso «:111», «:111», «:113» → zweite 111 ist 112.
    Nur bei einstelligen Pfaden derselben Art, je mit eigenem Titel."""
    def nr(v: Vorkommen) -> int | None:
        return int(v.pfad[0]) if len(v.pfad) == 1 and v.pfad[0].isdigit() else None

    def setze(v: Vorkommen, neu: int, alt: int, zwischen: tuple[int, int]) -> None:
        v.hinweise.append(f"Im Findmittel «{v.roh}» zwischen {zwischen[0]} und {zwischen[1]}, die Nummer {alt} steht "
                          f"doppelt und {neu} fehlt – als {neu} gelesen, bitte prüfen.")
        v.pfad = (str(neu),)
        v.anzeige = re.sub(rf"{alt}(\.?)$", rf"{neu}\1", v.anzeige)
        v.signatur_fest = normalisiere_signatur(re.sub(rf"{alt}(\.?)$", rf"{neu}\1", v.roh))  # «Nr. im PDF» bleibt
        v.ist_teil = False
    haupt = [v for v in vorkommen if len(v.pfad) == 1 and not v.aus_marke]
    for k in range(1, len(haupt) - 1):
        a, b, c = haupt[k - 1], haupt[k], haupt[k + 1]
        na, nb, nc = nr(a), nr(b), nr(c)
        # (nur Vollsignaturen mit lückenloser Zählung davor – blosse Nummern mit Lücken und Teilen wie «175.» in 13 Teilen,
        # VII.308.C.a., bleiben; für blosse Nummern gilt die Folgeprüfung in lies_signatur)
        if None in (na, nb, nc) or {a.typ, b.typ, c.typ} != {"voll"} or not (a.zeilen and b.zeilen and c.zeilen) \
                or k < 2 or nr(haupt[k - 2]) != na - 1:
            continue
        nd = nr(haupt[k + 2]) if k + 2 < len(haupt) else None
        if nb == na + 2 and nc == nb and c.ist_teil and (nd is None or nd == nb + 1):
            setze(b, na + 1, nb, (na, nb))  # 111, 113, 113, 114
            c.ist_teil = False
        elif nb == na and b.ist_teil and nc == na + 2 and not c.ist_teil:
            setze(b, na + 1, nb, (na, nc))  # 111, 111, 113


def nummern_aus_textspalte(koerper: list[Zeile], bestand: str) -> tuple[list[Zeile], str]:
    """Tabelle «Signatur | Inhalt | Jahre», in deren Signaturspalte nur einmal der Bestand steht, während die Einheiten
    in der Inhaltsspalte nummeriert sind: «V.G. c.63. ¦ 1. Brunnen u. Plastiken …» / «2. Notstandsaktion …» … «22.»
    (V.G.c.63.), «V.C. c. 71. ¦ a) Protokoll …» / «b) Kommission …» … «f)» (V.C.c.71.). Die Nummern sind die
    Einheiten: sie rücken in die Signaturspalte, der Bestand vorn fällt weg. (Nicht «V.G. c.64.:1. ¦ 1. Überbauung …»:
    dort steht eine eigene Signatur, die Nummern zählen deren Inhalt.)"""
    for k, z in enumerate(koerper[:80]):
        w = z.worte
        if len(w) < 3 or not re.match(r"[IVX]{1,4}\.", w[0].text) or z.x0 > SIGNATUR_SPALTE_MAX:
            continue
        for n in (1, 2, 3):
            if len(w) <= n + 1 or normalisiere_signatur(" ".join(x.text for x in w[:n])) != bestand:
                continue
            nr = w[n]
            if nr.x0 - w[n - 1].x1 < 15 or not re.fullmatch(r"1\.|a\)", nr.text):
                continue
            zahlen = nr.text == "1."
            erwartet, folge = 2, []
            for j in range(k + 1, len(koerper)):
                x = koerper[j]
                if not x.worte:
                    continue
                if x.x0 < nr.x0 - 20 and (re.match(r"[IVX]{1,4}\.", x.worte[0].text) or re.fullmatch(
                        r"\d{1,3}\.|[a-z]\)", x.worte[0].text)):
                    return koerper, ""  # eigene Signaturen in der Signaturspalte: anderer Aufbau
                soll = f"{erwartet}." if zahlen else f"{chr(ord('a') + erwartet - 1)})"
                if abs(x.x0 - nr.x0) <= 3 and x.worte[0].text == soll and len(x.worte) >= 2:
                    folge.append(j)
                    erwartet += 1
            if len(folge) < 2:
                return koerper, ""
            spalte = w[0].x0

            def verschoben(zz: Zeile, ab: int) -> Zeile:
                ww = zz.worte[ab:]
                return Zeile(zz.seite, zz.top, zz.bottom, [Wort(ww[0].text, spalte, spalte + (ww[0].x1 - ww[0].x0),
                                                               ww[0].font, ww[0].size)] + ww[1:],
                             zz.datum, zz.umfang, zz.schachtel, zz.spalten)
            neu = list(koerper)
            neu[k] = verschoben(z, n)
            for j in folge:
                neu[j] = verschoben(koerper[j], 0)
            return neu, (f"In der Signaturspalte steht nur der Bestand («{' '.join(x.text for x in w[:n])}»); die "
                         f"Nummern {nr.text} bis {koerper[folge[-1]].worte[0].text} der Inhaltsspalte als Signaturen "
                         "übernommen – bitte prüfen.")
        return koerper, ""
    return koerper, ""


def inhaltsangaben_der_uebersicht(vorspann: list[Zeile], modus: str, bestand: str) -> dict[tuple, list[Zeile]]:
    """Inhaltsangaben, die nur in der Übersicht stehen: «1.4. Stadtrat» / «[Enthält Artikel über «7 statt 9 Stadträte»]»
    (V.L.199.) – je Signatur die eingerückten «[Enthält …]»-Zeilen (bis zur schliessenden Klammer)."""
    erg: dict[tuple, list[Zeile]] = {}
    pfad, offen = None, False
    for z in vorspann:
        t = lies_signatur(z, Gliederung(modus, bestand, nur_pruefen=True)) if z.worte else None
        if t is not None:
            pfad, offen = t.pfad, False
            continue
        text = z.text.strip()
        if pfad is not None and (re.match(r"\[?Enthält\b", text) or offen):
            erg.setdefault(pfad, []).append(z)
            offen = text.startswith("[") and "]" not in text or offen and "]" not in text
            continue
        if not offen:
            pfad = None
    return erg


def schachtel_am_zeilenende(koerper: list[Zeile]) -> tuple[list[Zeile], str]:
    """Schachtelangabe am Ende einer Überschriftszeile: «Büchlein aus Reclam's Universal-Bibliothek: Nummer: ¦
    Schachtel 6», «b) mit Schreibmaschine geschriebene Texte: ¦ Schachtel 8» (VII.175.), wo sonst «Schachtel 5» allein
    steht – die Angabe wird eine eigene Zeile vor der Überschrift (Schachtelwechsel, die Überschrift beginnt den Teil)."""
    allein = [int(m.group(1)) for z in koerper if (m := re.fullmatch(r"Schachtel\s+(\d{1,3})", z.text.strip()))]
    if len(allein) < 2:
        return koerper, ""
    neu, n = [], 0
    for z in koerper:
        w = z.worte
        if len(w) >= 4 and w[-2].text == "Schachtel" and re.fullmatch(r"\d{1,3}", w[-1].text) \
                and w[-3].text.endswith(":") and w[-2].x0 - w[-3].x1 >= 15 \
                and max(allein) < int(w[-1].text) <= max(allein) + 5:
            neu.append(Zeile(z.seite, z.top - 0.01, z.top, w[-2:]))
            neu.append(Zeile(z.seite, z.top, z.bottom, w[:-2], z.datum, z.umfang, z.schachtel, z.spalten))
            allein.append(int(w[-1].text))
            n += 1
            continue
        neu.append(z)
    return (neu, f"{n} Schachtelangaben am Ende einer Überschriftszeile als Schachtelwechsel gelesen.") if n else (koerper, "")


def nummern_mit_nr(koerper: list[Zeile]) -> tuple[list[Zeile], str]:
    """Tabelle «Nummer ¦ Bauherr/ Bauprojekt/ Adresse ¦ Jahr» mit Zeilen «Nr. 15 ¦ Edwin Lee, Einfamilienhaus, Rümlang ¦
    1950», «Nr. 16 …», «Nr. 29A …» (VII.287.): «Nr. 15» ist die Nummer 15 der Einheit (sonst eine einzige Bestandszeile)."""
    kopf = next((k for k, z in enumerate(koerper[:60]) if len(z.worte) >= 2 and z.worte[0].text in ("Nummer", "Nr.")
                 and ist_tabellenkopf(" ".join(w.text for w in z.worte if not w.text.endswith("/")))), None)
    if kopf is None:
        kopf = next((k for k, z in enumerate(koerper[:60]) if len(z.worte) >= 2 and z.worte[0].text == "Nummer"), None)
    if kopf is None:
        return koerper, ""
    x_k = koerper[kopf].x0
    treffer = [j for j in range(kopf + 1, len(koerper)) if len(koerper[j].worte) >= 3
               and koerper[j].worte[0].text == "Nr." and abs(koerper[j].x0 - x_k) <= 3
               and re.fullmatch(r"\d{1,4}[A-Za-z]?", koerper[j].worte[1].text)]
    if len(treffer) < 5:
        return koerper, ""
    neu = list(koerper)
    for j in treffer:
        z = koerper[j]
        w0, w1 = z.worte[0], z.worte[1]
        neu[j] = Zeile(z.seite, z.top, z.bottom, [Wort(w1.text, w0.x0, w1.x1, w1.font, w1.size)] + z.worte[2:],
                       z.datum, z.umfang, z.schachtel, z.spalten)
    return neu, (f"Tabelle «{koerper[kopf].text.strip()[:40]}» mit «Nr. n»: {len(treffer)} Nummern als Signaturen "
                 "übernommen (ohne «Nr.»).")


def nummern_unter_abschnitt(koerper: list[Zeile]) -> tuple[list[Zeile], str]:
    """Nummerierte Dossiers unter einem Abschnitt, Nummer in der Signaturspalte, je mit Jahren und Schachtel: «9. Akten
    zum Schlachthof, nummerierte Dossiers» / «144 Anschaffung von Bluttransportwagen ¦ 1932 ¦ 44» / «145 …» … «2501 …»
    (V.F.c.150.) – die Nummern sind Signaturen unter dem Abschnitt (9.144., Muster 8 der NP11); die Nummer wird zur
    Dezimalnummer des Abschnitts, damit sie unter ihm steht."""
    neu = list(koerper)
    meldung = []
    k = 0
    while k < len(koerper):
        z = koerper[k]
        m_a = re.match(r"(\d{1,2})\.\s+\S", z.text.strip())
        if not (m_a and z.worte and (all("Bold" in w.font for w in z.worte) or z.worte[0].size >= 13.5)
                and re.search(r"\bnummeriert", z.text)):
            k += 1
            continue
        abschnitt, x_a = m_a.group(1), z.x0
        zeilen_n = []
        j = k + 1
        while j < len(koerper):
            x = koerper[j]
            if re.match(r"\d{1,2}\.\s+\S", x.text.strip()) and x.worte \
                    and (all("Bold" in w.font for w in x.worte) or x.worte[0].size >= 13.5):
                break  # nächster Abschnitt
            if x.worte and len(x.worte) >= 2 and re.fullmatch(r"\d{1,4}", x.worte[0].text) and abs(x.x0 - x_a) <= 5 \
                    and x.worte[1].x0 - x.worte[0].x1 >= 6:
                # (zweite Nummer eines Dossiers auf der Folgezeile: «412 Revision der Geschäftordnung des Gesundheits-
                # und» / «415 Landwirtschaftswesens im Zusammenhang …» ohne eigene Schachtel – Fortsetzung)
                vt_n = koerper[j - 1].text.rstrip()
                if not x.schachtel and zeilen_n and (vt_n.endswith(("-", ",")) or vt_n.split()[-1] in ANSCHLUSS_WOERTER):
                    j += 1
                    continue
                zeilen_n.append(j)
            j += 1
        mit_box = sum(1 for j_n in zeilen_n if koerper[j_n].schachtel)
        if len(zeilen_n) >= 10 and mit_box >= 0.8 * len(zeilen_n):
            for j_n in zeilen_n:
                x = koerper[j_n]
                w0 = x.worte[0]
                neu[j_n] = Zeile(x.seite, x.top, x.bottom, [Wort(f"{abschnitt}.{w0.text}.", w0.x0, w0.x1, w0.font, w0.size)]
                                 + x.worte[1:], x.datum, x.umfang, x.schachtel, x.spalten)
            meldung.append(f"«{z.text.strip()[:50]}»: {len(zeilen_n)} nummerierte Dossiers als {abschnitt}.n übernommen")
        k = j
    return neu, ("; ".join(meldung) + " (Nummer im PDF ohne Abschnitt).") if meldung else ""


def nummern_unter_schachteln(koerper: list[Zeile]) -> tuple[list[Zeile], str]:
    """Tabelle «Schachtel ¦ Nr. ¦ Inhalt ¦ Jahre», deren Nummern über die Schachteln hinweg weiterzählen: «Schachtel 1: ¦
    1. Quell- und Sodbrunnen-Untersuchungen» / «2. …» … «8.» / «Schachtel 2: ¦ 9. Bändlibach …» (V.F.c.199.). Die
    Nummern sind die Einheiten, die Schachtel gilt bis zur nächsten: «Schachtel 1» wird eine eigene Zeile, die Nummern
    rücken in die Signaturspalte. (Nicht, wenn die Zählung je Schachtel neu bei 1 beginnt – dann sind es Listen im
    Inhalt der Schachtel.)"""
    kopf = next((k for k, z in enumerate(koerper[:80]) if len(z.worte) >= 3 and z.worte[0].text == "Schachtel"
                 and z.worte[1].text in ("Nr.", "Nr") and ist_tabellenkopf(z.text)), None)
    if kopf is None:
        return koerper, ""
    x_nr = koerper[kopf].worte[1].x0
    spalte = koerper[kopf].x0
    marken, nummern = {}, {}
    for j in range(kopf + 1, len(koerper)):
        w = koerper[j].worte
        if len(w) >= 3 and w[0].text == "Schachtel" and re.fullmatch(r"\d{1,3}[a-z]?:?", w[1].text) \
                and re.fullmatch(r"\d{1,3}\.", w[2].text) and abs(w[2].x0 - x_nr) <= 4:
            marken[j] = 2
            nummern[j] = int(w[2].text[:-1])
        elif len(w) >= 2 and re.fullmatch(r"\d{1,3}\.", w[0].text) and abs(w[0].x0 - x_nr) <= 4:
            nummern[j] = int(w[0].text[:-1])
    folge = [nummern[j] for j in sorted(nummern)]
    if len(marken) < 2 or len(folge) < 4 or folge != list(range(1, len(folge) + 1)):
        return koerper, ""
    neu: list[Zeile] = []
    for j, z in enumerate(koerper):
        if j in marken:
            n = marken[j]
            w = z.worte
            neu.append(Zeile(z.seite, z.top, z.bottom, [Wort(w[0].text, w[0].x0, w[0].x1, w[0].font, w[0].size),
                                                          Wort(w[1].text.rstrip(":"), w[1].x0, w[1].x1, w[1].font,
                                                               w[1].size)]))
            z = Zeile(z.seite, z.top + 0.01, z.bottom, w[n:], z.datum, z.umfang, z.schachtel, z.spalten)
        if j in nummern:
            w = z.worte
            z = Zeile(z.seite, z.top, z.bottom, [Wort(w[0].text, spalte, spalte + (w[0].x1 - w[0].x0), w[0].font,
                                                      w[0].size)] + w[1:], z.datum, z.umfang, z.schachtel, z.spalten)
        neu.append(z)
    return neu, (f"Tabelle «Schachtel ¦ Nr. ¦ Inhalt»: die Nummern 1. bis {folge[-1]}. zählen über die Schachteln "
                 "hinweg – als Signaturen übernommen, die Schachtel gilt bis zur nächsten.")


def verarbeite_pdf(pdf: Path, ziel: Path, bestand: str | None, cache: Path | None,
                   katalog: dict | None = None) -> dict:
    ergebnis = {"pdf": pdf.name, "status": "OK", "bemerkungen": []}
    eintrag = (katalog or {}).get(pdf.name)
    if eintrag:
        ergebnis["katalog"] = f"{eintrag['signatur']} {eintrag.get('titel', '')}".strip()
    alle, meta = lade_oder_lese(pdf, cache)
    ergebnis["seiten"] = meta.get("Seiten", "")
    if meta.get("OCR"):
        ergebnis["bemerkungen"].append("Scan: Text per Texterkennung (tesseract) gelesen – Lesefehler möglich.")
    roh = [z for z in alle if not ist_kopf_oder_fuss(z)]
    zahlenspalte = finde_schachtelspalte(roh, alle)
    if zahlenspalte:
        ergebnis["bemerkungen"].append(
            "Blosse Zahlen in der rechten Spalte als Schachtel-Nr. gelesen (Spaltenkopf bzw. Vorwort «Schachtel»)."
            if zahlenspalte[1] == "schachtel" else
            "Blosse Zahlen in der rechten Spalte als Anzahl Exemplare gelesen (Spaltenkopf «Expl.»), im Umfang.")
    tabstopps = lerne_tabstopps(roh)
    koerper = richte_teilsignaturen(verbinde_versetzte_nummern([trenne_spalten(z, zahlenspalte, tabstopps)
                                                                for z in teile_tabellenspalten(roh)]))
    if sum(len(z.text) for z in koerper) < 40:  # auch die Texterkennung fand nichts Brauchbares
        ergebnis.update(status="Fehler", bemerkungen=["Kein lesbarer Text (Scan ohne Textebene, Texterkennung "
                                                      "nicht möglich) – von Hand erfassen."])
        return ergebnis
    rand = rechter_rand(koerper)
    if not bestand:
        aus_pdf = finde_bestand(koerper, alle, meta, pdf)
        aus_katalog = re.sub(r"\s", "", eintrag["signatur"]) if eintrag and eintrag.get("signatur") else None
        if aus_pdf and aus_katalog and (not aus_pdf.startswith(aus_katalog)
                                        or zusatz_aus_titel(aus_pdf, aus_katalog, eintrag.get("titel", ""))):
            ergebnis["bemerkungen"].append(f"Bestand im PDF «{aus_pdf}», im Online-Archiv «{aus_katalog}» – "
                                           "Signatur aus dem Online-Archiv verwendet.")
            bestand = aus_katalog
        else:
            bestand = aus_pdf or aus_katalog
    if not bestand:
        ergebnis.update(status="Fehler", bemerkungen=["Bestandssignatur nicht erkannt – mit --bestand angeben."])
        return ergebnis
    bestand = re.sub(r"\s", "", bestand)
    bestand = bestand if bestand.endswith(".") else bestand + "."
    ergebnis["bestand"] = bestand
    koerper, hinweis_textspalte = nummern_aus_textspalte(koerper, bestand)
    if hinweis_textspalte:
        ergebnis["bemerkungen"].append(hinweis_textspalte)
    koerper, hinweis_textspalte = nummern_unter_schachteln(koerper)
    if hinweis_textspalte:
        ergebnis["bemerkungen"].append(hinweis_textspalte)
    koerper, hinweis_textspalte = nummern_mit_nr(koerper)
    if hinweis_textspalte:
        ergebnis["bemerkungen"].append(hinweis_textspalte)
    koerper, hinweis_textspalte = nummern_unter_abschnitt(koerper)
    if hinweis_textspalte:
        ergebnis["bemerkungen"].append(hinweis_textspalte)

    modus = bestimme_modus(koerper)
    # Registraturplan: dreistellige Codes auf zwei Einrückungsstufen («010 Gesetzliche Grundlagen» / «011 …», V.F.c.28.)
    codes = [(i, z.x0) for i, z in enumerate(koerper)
             if len(z.worte) > 1 and re.fullmatch(r"\d{3}(?:/\d{3})?", z.worte[0].text)]
    registratur = sum(1 for _, x in codes if x <= 95) >= 8 and sum(1 for _, x in codes if 105 <= x <= 140) >= 8
    if registratur:  # das Verzeichnis beginnt beim ersten Code (die Nummern «1.» wiederholen sich je Code)
        start, bemerkung = next(i for i, x in codes if x <= 95), ""
    else:
        start, bemerkung = finde_detailbeginn(koerper, modus, bestand)
    modus = bestimme_modus(koerper[start:])
    if bemerkung:
        ergebnis["bemerkungen"].append(bemerkung)
    # Teile mit eigener Gliederung unter grossen nummerierten Überschriften («1. Alfred G. C. Wedekind-Güttinger»
    # mit A.–F., «2. Myrthe Wedekind-Güttinger» mit A.–N., VII.232.): das Verzeichnis beginnt beim ersten Teil
    teil_groesse = 0.0
    if modus == "gliederung":
        groessen = Counter(round(w.size) for z in koerper for w in z.worte)
        grund = groessen.most_common(1)[0][0] if groessen else 12
        teil_zeilen = [(i, int(z.worte[0].text[:-1])) for i, z in enumerate(koerper)
                       if len(z.worte) >= 2 and re.fullmatch(r"\d{1,2}\.", z.worte[0].text)
                       and z.x0 <= SIGNATUR_SPALTE_MAX and min(w.size for w in z.worte) >= grund + 3]
        # nur wenn unter den Teilen dieselben Marken neu beginnen (A.–F. und A.–N.), nicht bei Hauptnummern mit
        # eigener Unterzählung («1. Kontrollen …» / «1.1.», «2. Pläne» / «10», V.G.c.42.)
        grenzen = [i for i, _ in teil_zeilen] + [len(koerper)]
        marken_je_teil = [{z.worte[0].text for z in koerper[a + 1:b] if z.x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG
                           and re.fullmatch(r"[A-Z]\.|[IVX]{1,4}\.|[a-z]\)", z.worte[0].text)}
                          for a, b in zip(grenzen, grenzen[1:])]
        gemeinsam = set.intersection(*marken_je_teil) if marken_je_teil else set()
        if len(teil_zeilen) >= 2 and [n for _, n in teil_zeilen] == list(range(1, len(teil_zeilen) + 1)) \
                and any(i >= start for i, _ in teil_zeilen) and len(gemeinsam) >= 2:
            teil_groesse = min(min(w.size for w in koerper[i].worte) for i, _ in teil_zeilen)
            start = min(start, teil_zeilen[0][0])
    buchstaben = modus != "gliederung" and lerne_buchstabenabschnitte(koerper[start:])
    toc = {} if bemerkung.startswith("Übersicht nach Gruppen") else \
        lese_inhaltsverzeichnis(koerper[:start], modus, bestand, buchstaben)
    info: dict = {}
    gl = Gliederung(modus, bestand)
    if modus == "gliederung":
        gl.rang = lerne_raenge(koerper[start:])
        gl.marken_groesse = lerne_markengroessen(koerper[start:])
        gl.freie_nummern, gl.jahr_nummern = lerne_nummern(koerper[start:])
        gl.einrueck_x = lerne_unterzaehlung(koerper[start:])
        gl.mengenzahlen = lerne_mengenzahlen(koerper[start:])
        gl.punktnummern = lerne_punktnummern(koerper[start:])
        gl.doppelmarken = sum(1 for z in koerper[start:] if "Bold" in z.worte[0].font
                              and re.match(r"[IVX]{1,4}\)\s+[A-Z]\)\s", z.text)) >= 2
        # Klammermarken in der Spalte der fetten römischen Stufen: «II) Zürcher Eisenbahnverkehrsfragen» / «A) Akten,
        # Protokolle» … «O) …», «VII) National- und Express-Strassen» / «1) Nationalstrassen» (V.G.c.107.)
        roem_x = [round(z.worte[0].x0) for z in koerper[start:] if "Bold" in z.worte[0].font and len(z.worte) > 1
                  and re.fullmatch(r"[IVX]{1,4}\)", z.worte[0].text)]
        if len(roem_x) >= 2:
            gl.klammer_x = float(Counter(roem_x).most_common(1)[0][0])
        # fette «1) Oberstadtgass» … «8) Polizist Wäckerli» über eingerückten «a)» (VII.170.)
        fette_zahlen = [int(z.worte[0].text[:-1]) for z in koerper[start:] if "Bold" in z.worte[0].font
                        and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX and len(z.worte) > 1
                        and re.fullmatch(r"\d{1,2}\)", z.worte[0].text) and z.worte[1].text[:1].isupper()]
        gl.klammer_zahlen = fette_zahlen[:3] == [1, 2, 3]
        # eine einzige römische Marke, nicht fett: «4. Drucksachen» / «Das Alfred Escher-Denkmal …» / «I. Verzeichniss
        # der … Subscriptionen …» (VII.11.) ist Text, keine Gliederungsstufe
        roem_zeilen = [z for z in koerper[start:] if len(z.worte) > 1 and z.worte[0].x0 <= SIGNATUR_SPALTE_MAX_GLIEDERUNG
                       and ROEMISCH_RE.match(z.worte[0].text) and z.worte[1].text[:1].isupper()]
        gl.roem_einzeln = len(roem_zeilen) == 1 and "Bold" not in roem_zeilen[0].worte[0].font
        if teil_groesse:
            gl.teil_groesse = teil_groesse
            gl.rang = {**gl.rang, "teil": min(gl.rang.values()) - 1}
        if gl.einrueck_x:
            gl.rang = {**gl.rang, "zahl2": gl.rang["zahl"] + 0.5}
    else:
        gl.buchstaben = buchstaben
        gl.text_x0 = lerne_textspalte(koerper[start:])
        # ab S. 23 «1933.416 Feuerthalen Gemeinde» nach «45.0 Thun EMD …» (VII.308.E.a.): auch im dezimalen Findmittel
        # Signaturen «Jahr.Laufnummer»
        gl.jahr_nummern = lerne_nummern(koerper[start:])[1]
    gl.registratur = registratur
    # Signaturen nur in Klammern bei den Behältern: «Schachtel 1 (V.F. c.18.:1)», «Mappe (V.F. c.18.:3)» (V.F.c.18.)
    gl.klammer_voll = sum(1 for z in koerper[start:] if len(z.worte) <= 14 and all("Bold" in w.font for w in z.worte)
                          and (m_kv := re.search(r"\(\s*([IVX]{1,4}\.\s?[^()]{1,40}?)\s*\)\s*$", z.text))
                          and normalisiere_signatur(m_kv.group(1)).startswith(bestand)) >= 2
    info["freie_nummern"] = gl.freie_nummern or gl.jahr_nummern
    wechsel = finde_bestandswechsel(koerper[start:], bestand)  # Findmittel für mehrere Bestände (D2614)
    gl.weitere_bestaende = frozenset(s for _, s in wechsel if s != bestand)
    gl.gruppen_buchstaben = frozenset(m.group(1) for z in koerper[start:] if z.x0 <= SIGNATUR_SPALTE_MAX
                                      and (m := re.match(r"([A-Z])\.(?:[a-z]|\d{1,3})\.\s", z.text)))
    vorkommen = baue_vorkommen(koerper[start:], gl, info)
    if start:  # Inhaltsangaben nur in der Übersicht ins Darin der Einheit (V.L.199.)
        angaben = inhaltsangaben_der_uebersicht(koerper[:start], modus, bestand)
        for v in vorkommen:
            zeilen_a = angaben.get(v.pfad) if not v.ist_teil and v.typ != "bestand" else None
            if zeilen_a and not any(_titelanfang(x.text) == _titelanfang(zeilen_a[0].text) for x in v.zeilen):
                v.zeilen.extend(zeilen_a)
                v.hinweise.append("Inhaltsangabe aus der Übersicht übernommen («"
                                  f"{zeilen_a[0].text.strip()[:60]}»), im Detailverzeichnis fehlt sie.")
                angaben.pop(v.pfad)
    korrigiere_doppelnummern(vorkommen)
    korrigiere_buchstaben_geschwister(vorkommen)
    hinweis_doppelte_signatur(vorkommen)
    aufzaehlung_unter_jahrnummer(vorkommen, info)
    nummern_aus_eingeschobener_uebersicht(vorkommen)
    if gl.bestand:
        unternummern_im_text(vorkommen, info, gl.bestand)
    buchstaben_unter_einziger_nummer(vorkommen)
    # Beschreibung eines Stücks ohne Nummer vor der ersten Signatur: «Protokoll der Commission für Einrichtung eines
    # Zwinglidenkmals» / «19. Juli 1872 bis 23. Januar 1886» / «1 Band (schwarz, …)» / «35 x 24 cm», dann «Verzeichnis
    # der nummerierten Akten …» / «1 Protokoll der ersten Versammlung» (VII.10.) – ins Darin der ersten Einheit, mit
    # Hinweis (keine erfundene Signatur)
    vorn_block = []
    for vb in info.get("verbleib", []):
        if vb.art == "einheit":
            break
        if vb.art == "vorlauf":
            vorn_block.append(vb)
    # (nur bis zur nächsten Überschrift: «Verzeichnis der nummerierten Akten und Materialien» (fett), «Nr. Gegenstand
    # Datum» bleiben Überschriften)
    for k_vb, vb in enumerate(vorn_block):
        t_vb = vb.zeile.text.strip()
        if all("Bold" in w.font for w in vb.zeile.worte) or TABELLENKOPF_RE.match(t_vb) or ist_tabellenkopf(t_vb):
            vorn_block = vorn_block[:k_vb]
            break
    # (auch eine einzelne Zeile mit Werktitel in Anführung und Datum direkt vor der ersten Signatur: «“Summarisches
    # Curiculum vitae in Stichworten”, alt Stadtrat Stirnemann Ende 1961» vor «1. 1. Fortifikation …», VII.76.)
    if vorn_block and len(vorn_block) > 1 and re.match(r"[“„\"«]", vorn_block[-1].zeile.text.strip()) \
            and finde_zeitraeume(vorn_block[-1].zeile.text) and not re.match(r"[“„\"«]", vorn_block[0].zeile.text.strip()):
        vorn_block = vorn_block[-1:]
    if vorkommen and (2 <= len(vorn_block) <= 8 and any(UMFANG_RE.match(vb.zeile.text.strip()) for vb in vorn_block)
                      or len(vorn_block) == 1 and re.match(r"[“„\"«][^”“\"»]{5,}[”“\"»]", vorn_block[0].zeile.text.strip())) \
            and any(finde_zeitraeume(vb.zeile.text) for vb in vorn_block) \
            and not any(len(vb.zeile.text) > 90 for vb in vorn_block):
        # (Stück ohne Nummer: zur Zeile für den Bestand, nicht ins Darin der ersten Einheit)
        erste_v = next((v for v in vorkommen if v.typ == "bestand"), None)
        if erste_v is None:
            erste_v = Vorkommen(("Bestand",), "", "", vorn_block[0].zeile.seite, [], typ="bestand")
            vorkommen.append(erste_v)
        for k_vb, vb in enumerate(vorn_block):
            erste_v.zeilen.insert(k_vb, vb.zeile)
            vb.art, vb.vorkommen = "einheit", erste_v
        erste_v.hinweise.insert(0, f"Stück ohne Nummer im Findmittel vor der ersten Signatur («"
                                   f"{vorn_block[0].zeile.text.strip()[:70]}», S. {vorn_block[0].zeile.seite}) – hier "
                                   "beim Bestand übernommen (keine Signatur erfunden); in scope beim Bestand ergänzen "
                                   "oder von Hand als Einheit anlegen.")
    verteile_buchstabenlisten(vorkommen, info)
    verteile_detaillisten(vorkommen, info)
    if gl.jahr_nummern:
        korrigiere_jahrnummern(vorkommen)
    if start and any(re.search(r"nicht im Detail verzeichnet", z.text, re.I) for z in koerper[start:]):
        nur_vorn = einheiten_nur_im_vorspann(koerper[:start], modus, bestand, buchstaben,
                                             {v.pfad for v in vorkommen})
        if nur_vorn:
            vorkommen += nur_vorn
            ergebnis["bemerkungen"].append(f"{len(nur_vorn)} Positionen nur in der Zusammenfassung "
                                           "(«Nicht im Detail verzeichnet») – von dort übernommen.")
            # Posten der Kurzliste nach «Nicht im Detail verzeichnet», die in der Zusammenfassung fehlen: «Cakeplatte
            # (Keramik) ¦ 1 Mappe» (VII.174.) – ins Darin der letzten übernommenen Einheit statt nur ins Blatt Info
            def wichtige(text: str) -> set[str]:
                return {x.lower() for x in re.findall(r"[A-Za-zÄÖÜäöüß]{4,}", text)} - {"mappe", "mappen", "schachtel"}
            bekannt_w = set().union(*(wichtige(" ".join(x.text for x in v.zeilen)) for v in nur_vorn))
            kurz = []
            gesehen_marke = False
            for vb in info.get("verbleib", []):
                if vb.art == "schluss" and re.match(r"Nicht im Detail verzeichnet\b", vb.zeile.text.strip(), re.I):
                    gesehen_marke = True
                    continue
                if not gesehen_marke or vb.art != "schluss":
                    continue
                if ist_schlussvermerk(vb.zeile.text.strip()):
                    break
                w_z = wichtige(vb.zeile.text)
                if w_z and not w_z & bekannt_w:
                    kurz.append(vb)
            for vb in kurz:
                ziel_v = nur_vorn[-1]
                ziel_v.zeilen.append(vb.zeile)
                vb.art, vb.vorkommen = "einheit", ziel_v
                txt = schlusszeile(vb.zeile, vb.zeile.text.strip())
                if txt in info.get("schluss", []):
                    info["schluss"].remove(txt)
                ziel_v.hinweise.append(f"«{vb.zeile.text.strip()}» steht nur in der Kurzliste S. {vb.zeile.seite} – hier "
                                       "angefügt, bitte prüfen.")
    # Tippfehler in der Hauptnummer: «1. Verschiedene Verzeichnisse» direkt vor «2.1.», und «2.» fehlt (VII.122.)
    if modus == "dezimal":
        pfade = {v.pfad for v in vorkommen}
        for a, b in zip(vorkommen, vorkommen[1:]):
            if a.ist_teil and len(a.pfad) == 1 and a.pfad[0].isdigit() and len(b.pfad) == 2 and b.pfad[0].isdigit() \
                    and int(b.pfad[0]) == int(a.pfad[0]) + 1 and (b.pfad[0],) not in pfade:
                a.hinweise.append(f"Im Findmittel «{a.anzeige}», nach der Folge aber «{b.pfad[0]}.» – Signatur "
                                  "angepasst, bitte prüfen.")
                a.pfad, a.anzeige, a.ist_teil = (b.pfad[0],), b.pfad[0] + ".", False
                pfade.add(a.pfad)
        # «3. Werbefilme» zwischen «1.2. Dokumentarfilme» und «1.4. Diverses» ist «1.3.»; das spätere
        # «3. Filmzettel» ist dann die echte 3. (VII.163.)
        for k, b in enumerate(vorkommen):
            if len(b.pfad) != 1 or not b.pfad[0].isdigit() or b.ist_teil:
                continue
            a = next((x for x in reversed(vorkommen[:k]) if x.pfad != b.pfad), None)
            c = next((x for x in vorkommen[k + 1:] if x.pfad != b.pfad), None)
            if a is None or c is None or len(a.pfad) != 2 or len(c.pfad) != 2 or a.pfad[0] != c.pfad[0] \
                    or not (a.pfad[1].isdigit() and c.pfad[1].isdigit()):
                continue
            neu = (a.pfad[0], b.pfad[0])
            if int(c.pfad[1]) == int(a.pfad[1]) + 2 == int(b.pfad[0]) + 1 and neu not in pfade:
                alt = b.pfad
                b.hinweise.append(f"Im Findmittel «{b.anzeige}», nach der Folge aber «{pfad_text(neu)}» – "
                                  "Signatur angepasst, bitte prüfen.")
                if not b.schachtel and a.schachtel and a.pfad[:1] == neu[:1]:
                    b.schachtel = a.schachtel  # liegt beim vorigen Unterpunkt («Schachtel 4» / 1.2. / 1.3.)
                for x in vorkommen[k:]:
                    if x.pfad == alt and (x is b or x.aus_marke):  # samt Teilen aus Schachtelangaben
                        x.pfad, x.anzeige = neu, pfad_text(neu)
                    elif x.pfad == alt:
                        x.ist_teil = False  # spätere echte Nennung
                        break
                pfade.add(neu)
    # übergeordnete Position nur in der Übersicht: «1. Archiv Anne-Marie Blanc» in Vorbemerkung und Übersicht, das
    # Detailverzeichnis beginnt mit «1.1. Biografisches» (VII.237.) – als Einheit von dort, vor ihren Unternummern
    # (nur, wenn es für den Bestand kein weiteres Findmittel gibt: «19. Pläne und Skizzen» hat VII.151. im
    # Hauptverzeichnis, das eigene Verzeichnis D4058 beginnt mit 19.1.)
    mehrere_findmittel = bool(eintrag) and sum(1 for e in (katalog or {}).values()
                                               if e.get("signatur") == eintrag.get("signatur")) > 1
    if start and modus == "dezimal" and vorkommen and not mehrere_findmittel:
        pfade_v = {v.pfad for v in vorkommen}
        fehlend = {v.pfad[:-1] for v in vorkommen if v.typ == "zahl" and not v.ist_teil and len(v.pfad) >= 2
                   and all(k.isdigit() for k in v.pfad) and v.pfad[:-1] not in pfade_v}
        if fehlend:
            for v_n in einheiten_nur_im_vorspann(koerper[:start], modus, bestand, buchstaben, pfade_v):
                if v_n.pfad not in fehlend:
                    continue
                v_n.hinweise = [f"Nur in der Übersicht verzeichnet (S. {v_n.seite}), das Detailverzeichnis beginnt mit "
                                "den Unternummern – als übergeordnete Einheit von dort übernommen, bitte prüfen."]
                v_n.zeilen = v_n.zeilen[:1]  # nur der Titel (die Vorbemerkung dazu bleibt im Blatt Info)
                # (Schachtelangabe am Ende der Übersichtszeile: «6. Rationierung im Weltkrieg 1917-1947 Schacht.16-17»,
                # VII.190.)
                if v_n.zeilen and v_n.zeilen[0].worte:
                    t_n = v_n.zeilen[0].text.strip()
                    m_s = re.search(r"\s(?:Schachteln?|Schacht\.?)\s*(\d{1,4}(?:\s*[-–]\s*\d{1,4})?)\s*$", t_n)
                    if m_s:
                        n_s = len(m_s.group(0).split())
                        z_n = v_n.zeilen[0]
                        if n_s < len(z_n.worte):
                            v_n.zeilen[0] = Zeile(z_n.seite, z_n.top, z_n.bottom, z_n.worte[:-n_s], z_n.datum, z_n.umfang)
                            v_n.schachtel = re.sub(r"\s+", "", m_s.group(1)).replace("–", "-")
                k_v = next(k for k, v in enumerate(vorkommen) if v.pfad[:len(v_n.pfad)] == v_n.pfad)
                vorkommen.insert(k_v, v_n)
                fehlend.discard(v_n.pfad)
    # ein ganzer Abschnitt nur im Inhaltsverzeichnis: «X. Biographische Informationen zu Alice Boner und Uday Shankar» /
    # «X.1. Alice Boner und die Kunst Indiens …» … «X.4. …» vor «1. Korrespondenz» (VII.389.) – als Einheiten vorn
    if start and modus == "dezimal" and vorkommen and not any(not k.isdigit() for v in vorkommen for k in v.pfad[:1]):
        abschnitt_v: list[Vorkommen] = []
        for z_a in koerper[:start]:
            m_a = re.match(r"([A-Z])\.(?:(\d{1,2})\.)?\s+(\S.*)$", z_a.text.strip())
            if m_a and (not abschnitt_v and m_a.group(2) is None
                        or abschnitt_v and m_a.group(1) == abschnitt_v[0].pfad[0] and m_a.group(2)
                        and int(m_a.group(2)) == len(abschnitt_v) and abs(z_a.x0 - abschnitt_v[0].x0) <= 3):
                pfad_a = (m_a.group(1),) + ((m_a.group(2),) if m_a.group(2) else ())
                rest_a = Zeile(z_a.seite, z_a.top, z_a.bottom, z_a.worte[1:], z_a.datum, z_a.umfang)
                abschnitt_v.append(Vorkommen(pfad_a, pfad_text(pfad_a), z_a.worte[0].text, z_a.seite, [rest_a],
                                             x0=z_a.x0))
            elif abschnitt_v and len(abschnitt_v) < 3:
                abschnitt_v = []
            elif abschnitt_v and z_a.x0 > abschnitt_v[0].x0 + 20 and z_a.text.strip():
                abschnitt_v[-1].zeilen.append(z_a)  # Folgezeile eines Eintrags
            elif abschnitt_v:
                break
        if len(abschnitt_v) >= 3:
            for v_a in abschnitt_v:
                v_a.hinweise.append(f"Nur im Inhaltsverzeichnis verzeichnet (S. {v_a.seite}), im Detailverzeichnis "
                                    "fehlt der Abschnitt – von dort übernommen, bitte prüfen.")
            vorkommen[0:0] = abschnitt_v
    if len(vorkommen) == 1 and re.fullmatch(r"\d{1,3}", vorkommen[0].roh.strip()):
        vorkommen = []  # eine einzelne «1 Collagenbuch …» (VII.487.) ist keine Gliederung, sondern eine Liste
    # die Zeile für den Bestand (Stücke ohne Nummer) steht immer am Schluss, auch wenn das Stück mitten in der Liste
    # stand («Drucksache …» unter I., VII.60.)
    vorkommen = [v for v in vorkommen if v.typ != "bestand"] + [v for v in vorkommen if v.typ == "bestand"]
    # Ohne (brauchbare) Signaturen: nach Mappen/Schachteln gegliedert? Sonst eine Zeile für den ganzen Bestand
    ersatz = ""
    vorlauf = sum(1 for vb in info["verbleib"] if vb.art == "vorlauf")
    vk_ohne_b = [v for v in vorkommen if v.typ != "bestand"]  # ohne die Zeile für Stücke ohne Nummer
    marken = sum(1 for z in koerper[start:] if BEHAELTER_RE.match(z.text.strip()) and z.x0 <= 160)
    # nur «a)», «b)» als Signaturen, aber gegliedert nach Schachteln: das sind Listenzeichen (VII.189.)
    nur_klein = bool(vk_ohne_b) and marken >= 2 and all(v.typ == "klein" for v in vk_ohne_b)
    # (nicht, wenn die Schachteln eingerückt unter den Buchstaben stehen: «Sch. Bez. Inhalt Jahre» / «a) Beilagen …» bei x
    # 101 / «Schachtel 1 1913-1922» bei x 137, VII.101. – dann sind a)–c) die Einheiten)
    if nur_klein:
        x_klein = min((v.x0 for v in vk_ohne_b if v.x0), default=0.0)
        x_marken = min((z.x0 for z in koerper[start:] if BEHAELTER_RE.match(z.text.strip()) and z.x0 <= 160), default=0.0)
        if x_klein and x_marken > x_klein + 20:
            nur_klein = False
    # nur blosse Nummern, die mehrmals neu bei 1 beginnen, und davor Schachteln mit Titel («Schachtel 1 Manuskripte
    # …», «Schachtel 2 Publikationen», dann die Listen 1.–55., 1.–6., 1–172, VII.222.): Listen im Inhalt, keine
    # Signaturen – die Schachteln sind die Einheiten
    vor_erster = []
    for vb in info["verbleib"]:
        if vb.art == "einheit":
            break
        vor_erster.append(vb.zeile)
    listen = modus == "gliederung" and bool(vk_ohne_b) \
        and all(len(v.pfad) == 1 and v.pfad[0].isdigit() for v in vk_ohne_b) \
        and sum(1 for v in vk_ohne_b if v.pfad == ("1",)) >= 3 \
        and sum(1 for z in vor_erster if BEHAELTER_RE.match(z.text.strip()) and z.x0 <= 160) >= 2
    # wenige blosse Nummern, eingerückt unter Schachtelüberschriften («Schachtel 1» / «- Akten zur Rechnung 1879» /
    # «- 1. Drucksachen» / «2. Entwürfe …» / «3. Zirkulare», VII.2.): Aufzählung im Inhalt einer Schachtel
    marken_x = min((z.x0 for z in koerper[start:] if BEHAELTER_RE.match(z.text.strip()) and z.x0 <= 160), default=0.0)
    kleine_liste = marken >= 2 and bool(vk_ohne_b) and len(vk_ohne_b) <= 5 \
        and all(len(v.pfad) == 1 and v.pfad[0].isdigit() and v.x0 > marken_x + 15 for v in vk_ohne_b)
    # nur nummerierte Abschnitte einer Bestandsbeschreibung: «1. Herkunft des Bestandes», «2. Hinweise», «3. Gliederung»
    # / «Haushaltungsbücher 1917-1933 ¦ Schachtel 1» … (VII.134.) – die Schachteln sind die Einheiten
    beschreibung = bool(vk_ohne_b) and len(vk_ohne_b) <= 8 and all(
        len(v.pfad) == 1 and v.zeilen and BESCHREIBUNG_RE.match(v.zeilen[0].text.strip()) for v in vk_ohne_b)
    if not vk_ohne_b or vorlauf > 0.5 * len(koerper[start:]) or nur_klein or listen or kleine_liste or beschreibung:
        info_b: dict = {"freie_nummern": info["freie_nummern"]}
        behaelter = baue_behaelter(koerper[start:], info_b)
        if not behaelter:
            info_b = {"freie_nummern": info["freie_nummern"]}
            behaelter = baue_behaelter_am_ende(koerper[start:], info_b)
        if not behaelter and not vk_ohne_b:
            info_b = {"freie_nummern": info["freie_nummern"]}
            behaelter = baue_behaelter_aus_register(koerper[start:], info_b)
        vorlauf_b = sum(1 for vb in info_b.get("verbleib", []) if vb.art == "vorlauf")
        if behaelter and (not vk_ohne_b or vorlauf_b < vorlauf or nur_klein or listen or kleine_liste or beschreibung):
            if beschreibung:
                ergebnis["bemerkungen"].append(
                    "Die nummerierten Abschnitte " + ", ".join(f"«{v.anzeige} {v.zeilen[0].text.strip()}»" for v in vk_ohne_b)
                    + " beschreiben den Bestand – keine Einheiten; die Schachteln sind die Einheiten.")
            if listen:
                behaelter[-1].hinweise.append(
                    f"Die nummerierten Listen nach dieser Schachtel ({sum(1 for v in vorkommen if v.pfad == ('1',))} "
                    "Folgen, die je bei 1 beginnen) stehen im Darin – bitte prüfen, ob sie zu dieser Schachtel "
                    "gehören oder eigene Einheiten sind.")
            vorkommen, info, ersatz, modus = behaelter, info_b, "Mappen/Schachteln", "gliederung"
            if verteile_chronologisch(vorkommen, info.get("verbleib", [])):
                ergebnis["bemerkungen"].append("Chronologisches Verzeichnis nach den Jahresbereichen der Schachteln "
                                               "auf die Schachteln verteilt.")
    # Findmittel für mehrere Bestände: jede Einheit gehört zum Bestand der letzten Überschrift davor
    def bestand_an(stelle: tuple) -> str:
        b = ""
        for z, s in wechsel:
            if (z.seite, z.top) <= stelle:
                b = "" if s == bestand else s
        return b

    if wechsel:
        for v in vorkommen:
            v.bestand = bestand_an(min(((z.seite, z.top) for z in v.zeilen), default=(v.seite, 0.0)))
    # Schachteln vor der ersten Signatur (V.B.c.34.: «Schachtel 1» … «Schachtel 5», dann «I. Vorstösse …»);
    # bei mehreren Beständen je Bestand getrennt (D2614: V.L.156. Schachtel 1–3, dann «V.L. 157. …»)
    if not ersatz and vorkommen:
        fuehrend = []
        for vb in info["verbleib"]:
            if vb.art == "einheit":
                break
            fuehrend.append(vb)
        abschnitte: list[list[Verbleib]] = [[]]
        for vb in fuehrend:
            if abschnitte[-1] and any(vb.zeile is z for z, _ in wechsel):
                abschnitte.append([])
            abschnitte[-1].append(vb)
        vorn_alle: list[Vorkommen] = []
        verbleib_v: list[Verbleib] = []
        schluss_v: list = []
        for teil in abschnitte:
            zeilen_v = [vb.zeile for vb in teil]
            b_teil = bestand_an((zeilen_v[0].seite, zeilen_v[0].top)) if wechsel and zeilen_v else ""
            marken_v = [k for k, z in enumerate(zeilen_v) if BEHAELTER_RE.match(z.text.strip()) and z.x0 <= 160]
            # mit Inhalt unter den Marken («Schachtel 1» / «Generalverkehrsplan Zürich» …), nicht bloss eine
            # Lagerungsangabe «Schachtel 1 Filme Nummern 448 bis 463» / «Schachtel 2 …» (III.T.)
            mit_inhalt = sum(1 for a, b in zip(marken_v, marken_v[1:] + [len(zeilen_v)]) if b - a > 1) >= 2
            # ein weiterer Bestand des Findmittels ohne eigene Signaturen: seine Schachteln sind seine Einheiten
            fremd = bool(b_teil) and not any(v.bestand == b_teil for v in vorkommen)
            vorn: list[Vorkommen] = []
            if len(marken_v) >= 2 and (mit_inhalt or fremd):
                info_v: dict = {}
                vorn = baue_behaelter(zeilen_v, info_v)
                signaturen = {v.pfad for v in vorkommen if v.bestand == b_teil}
                if any(v.pfad in signaturen for v in vorn):
                    vorn = []  # «Schachtel 1» und Signatur «1.» – nicht vermischen
            if vorn:
                for v in vorn:
                    v.bestand = b_teil
                    if not fremd:
                        v.hinweise.append("Schachtel vor der ersten Signatur – als eigene Einheit übernommen, "
                                          "bitte prüfen.")
                vorn_alle += vorn
                verbleib_v += info_v["verbleib"]
                schluss_v += info_v.get("schluss", [])
            else:
                verbleib_v += teil
        if vorn_alle:
            vorkommen = vorn_alle + vorkommen
            info["verbleib"] = verbleib_v + info["verbleib"][len(fuehrend):]
            info.setdefault("schluss", []).extend(schluss_v)
    # Zusammenfassung «Schachtel 1 1.1.» / «Schachtel 2 1.2., 1.3.» / «Schachtel 5 2.1. - 2.5.» (V.L.111.): eine
    # Zuordnung der Schachteln zu den Signaturen des Verzeichnisses – keine eigenen Einheiten
    zuordnung_vorn: dict[tuple, list[str]] = {}
    for z in koerper[:start]:
        m_z = re.match(r"Schachtel\s+(\d{1,4}[a-z]?)\s*(?:\([^)]*\))?\s+(\d{1,3}(?:\.\d{1,4})+\..*)$", z.text.strip())
        if not m_z or z.x0 > 160:
            continue
        for von_s, bis_s in re.findall(r"(\d{1,3}(?:\.\d{1,4})+)\.?(?:\s*[-–]\s*(\d{1,3}(?:\.\d{1,4})+)\.?)?",
                                       m_z.group(2)):
            von_p, bis_p = tuple(von_s.split(".")), tuple(bis_s.split(".")) if bis_s else None
            for v in vorkommen:
                if v.ist_teil or len(v.pfad) != len(von_p) or not v.pfad[-1].isdigit():
                    continue
                if v.pfad == von_p or (bis_p and len(bis_p) == len(von_p) and v.pfad[:-1] == von_p[:-1]
                                        and von_p[-1].isdigit() and bis_p[-1].isdigit()
                                        and int(von_p[-1]) <= int(v.pfad[-1]) <= int(bis_p[-1])):
                    zuordnung_vorn.setdefault(v.pfad, []).append(m_z.group(1))
    if zuordnung_vorn:
        for v in vorkommen:
            if v.pfad in zuordnung_vorn and not v.ist_teil and (not v.schachtel or v.schachtel_geerbt):
                v.schachtel = schachtel_liste(list(dict.fromkeys(zuordnung_vorn[v.pfad])))
                v.schachtel_geerbt = False
                v.hinweise.append("Schachtel aus der Aufteilung in der Zusammenfassung übernommen.")
    # Schachteln nur in der Zusammenfassung vor dem Detailverzeichnis (VII.189.: Schachtel 3, 4, 7–10)
    if start and vorkommen and not zuordnung_vorn and sum(1 for z in koerper[:start]
                                                         if BEHAELTER_RE.match(z.text.strip()) and z.x0 <= 160) >= 2:
        info_z: dict = {}
        zusammenfassung = baue_behaelter(koerper[:start], info_z)
        bekannt = {v.schachtel for v in vorkommen if v.schachtel} | {v.pfad[-1] for v in vorkommen
                                                                     if v.typ == "behaelter"}
        def nummern(sch: str) -> set[str]:
            m_b = re.fullmatch(r"(\d+)-(\d+)", sch)
            return {str(n) for n in range(int(m_b.group(1)), int(m_b.group(2)) + 1)} if m_b \
                else {x.strip() for x in sch.split(",")}
        belegte_pfade = {v.pfad for v in vorkommen}
        neu = [v for v in zusammenfassung if v.schachtel and not (nummern(v.schachtel) & bekannt)
               and v.pfad not in belegte_pfade]
        if neu:
            for v in neu:
                v.hinweise.append("Schachtel steht nur in der Zusammenfassung vor dem Detailverzeichnis – von dort "
                                  "übernommen, bitte prüfen.")
            ids = {id(v) for v in neu}
            info["verbleib"].extend(vb for vb in info_z["verbleib"] if vb.vorkommen is not None
                                    and id(vb.vorkommen) in ids)
            # Block ohne Überschrift nach grossem Abstand am Ende einer Detail-Schachtel, der zu einer Schachtel nur aus
            # der Zusammenfassung passt: «Schachtel 10 = grf. Schachtel mit Porträtbild der Anna Asper» / S. 8 unter
            # Schachtel 6 «Porträtbild von Anna Asper 1964 / Signiert “Stefanoff 64” …» (VII.189.) – gehört zu 10
            def lange_worte(text: str) -> set[str]:
                return {x.lower() for x in re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", text)} - {"schachtel", "schachteln"}
            leer = [v for v in neu if not any(x.text.strip() for x in v.zeilen[1:])]
            for v_d in [v for v in vorkommen if id(v) not in ids]:
                zs = v_d.zeilen
                k_b = next((k for k in range(len(zs) - 1, 0, -1) if zs[k].seite == zs[k - 1].seite
                            and zs[k].top - zs[k - 1].bottom >= 100), None)
                if k_b is None:
                    continue
                block_worte = lange_worte(zs[k_b].text)
                passend_v = [v for v in leer if v.zeilen and len(block_worte & lange_worte(v.zeilen[0].text)) >= 2]
                if len(passend_v) != 1:
                    continue
                block = zs[k_b:]
                v_d.zeilen = zs[:k_b]
                passend_v[0].zeilen.extend(block)
                ids_block = {id(x) for x in block}
                for vb in info["verbleib"]:
                    if id(vb.zeile) in ids_block:
                        vb.vorkommen = passend_v[0]
                passend_v[0].hinweise.append(f"Inhalt aus dem Detailverzeichnis S. {block[0].seite} (ohne Überschrift, nach "
                                        f"Schachtel {v_d.anzeige}) – über den Titel zugeordnet, bitte prüfen.")
                leer.remove(passend_v[0])
            vorkommen = vorkommen + neu
            if ersatz == "Mappen/Schachteln":
                vorkommen.sort(key=lambda v: (int(re.match(r"\d*", v.pfad[-1]).group() or 0), v.pfad))
    # Erste Gruppe ohne Nummer («Akten und Drucksachen» … vor «2. Pläne», V.L.45.): wird Einheit 1
    if not ersatz and vorkommen and vorkommen[0].pfad == ("2",):
        grund = _grundschrift(koerper[start:])
        inhalt = [vb for vb in info["verbleib"] if vb.art == "vorlauf" and "Stadtarchiv" not in vb.zeile.text
                  and max(w.size for w in vb.zeile.worte) < grund + 1.5 and not DETAIL_RE.fullmatch(vb.zeile.text.strip())]
        if len(inhalt) >= 3:
            erste = vorkommen[0]
            v1 = Vorkommen(("1",), erste.anzeige.replace("2", "1", 1), "", inhalt[0].zeile.seite,
                           [vb.zeile for vb in inhalt], typ=erste.typ)
            v1.hinweise.append("Nummer 1 fehlt im Findmittel – die Zeilen vor der ersten Signatur «2» als Einheit 1 "
                               "übernommen; bitte prüfen.")
            for vb in inhalt:
                vb.art, vb.vorkommen = "einheit", v1
            # Titel: die Abschnittsüberschrift direkt davor («Detailverzeichnis» / «Akten und Drucksachen», V.L.45.)
            k_erst = next(k for k, vb in enumerate(info["verbleib"]) if vb is inhalt[0])
            kopf = info["verbleib"][k_erst - 1] if k_erst else None
            if kopf is not None and kopf.art == "vorlauf" and kopf.zeile.seite == inhalt[0].zeile.seite \
                    and abs(kopf.zeile.x0 - inhalt[0].zeile.x0) <= 30 \
                    and max(w.size for w in kopf.zeile.worte) >= grund + 1.5 and len(kopf.zeile.worte) <= 8 \
                    and not DETAIL_RE.fullmatch(kopf.zeile.text.strip()) and "Stadtarchiv" not in kopf.zeile.text:
                v1.titel_vorgabe = kopf.zeile.text.strip().rstrip(":")
                v1.vorgabe_ids = {id(kopf.zeile)}
                kopf.art, kopf.vorkommen = "einheit", v1
            vorkommen.insert(0, v1)
    if wechsel:
        bereich = f"{wechsel[0][1]} bis {wechsel[-1][1]}"
        mit_einheiten = {v.bestand or bestand for v in vorkommen}
        for v in vorkommen:
            if v.bestand and len(v.pfad) == 1 and not v.ist_teil:
                v.hinweise.append(f"Findmittel für mehrere Bestände ({bereich}): Einheit gehört zum Bestand "
                                  f"{v.bestand} (Spalte «Übergeordnete Signatur»).")
        ohne = [s for _, s in wechsel if s not in mit_einheiten]
        ergebnis["bemerkungen"].append(
            f"Findmittel für mehrere Bestände ({bereich}): Einheiten für "
            f"{', '.join(s for _, s in wechsel if s in mit_einheiten) or '–'} (Spalte «Übergeordnete Signatur»)"
            + (f"; nur beschrieben, ohne Einheiten (Text nicht übernommen): {', '.join(ohne)}." if ohne else "."))
    # «1. Kuvert (Seidenkuvert)» / «2. Kuvert (Seidenkuvert)» nach einer langen Objektbeschreibung (V.L.223.): zwei, drei
    # gleich betitelte Nummern zählen Stücke eines Objekts auf – keine Signaturen, eine Zeile für den Bestand
    if vorkommen and not ersatz and 2 <= len(vorkommen) <= 3 \
            and all(len(v.pfad) == 1 and v.pfad[0].isdigit() and v.zeilen for v in vorkommen) \
            and len({_titelanfang(v.zeilen[0].text) for v in vorkommen}) == 1 \
            and sum(1 for vb in info["verbleib"] if vb.art == "vorlauf") >= 8:
        vorkommen = []
    if not vorkommen:
        info_c: dict = {}
        titel = re.sub(r"^\S+\s|\s*\((?:Bestand|Teilbestand)\)$|,?\s*\d{4}\s*[-–]\s*\d{4}$", "",
                       (eintrag or {}).get("titel", "")).strip()
        vorkommen = baue_bestandszeile(koerper, start, info_c, titel)
        if vorkommen:
            info, ersatz, modus = info_c, "ohne Signaturen", "gliederung"
    for v in vorkommen:  # Zeile für den Bestand mit Stücken ohne Nummer: Titel des Bestands
        if v.typ == "bestand" and not v.titel_vorgabe:
            v.titel_vorgabe = bestandstitel(koerper, eintrag)
    gruppen_unter_letzter_schachtel(vorkommen)
    if modus == "dezimal":
        registraturgruppen(vorkommen)
    einheiten = verteile_lange_darin(baue_einheiten(vorkommen, rand, modus, info))
    # Zeitraum des Bestands laut Online-Archiv («… Firmenarchiv, 1820-1964 (Bestand)»): Rahmen für Schätzungen
    titel_kat = re.sub(r"\s*\(ca\.\)", "", (eintrag or {}).get("titel", ""))  # «1863 (ca.)-1989 (Bestand)»
    m_r = re.search(r"(?:(\d{4})\s*[-–]\s*)?(\d{4})\s*\([^()]*\)\s*$", titel_kat)
    rahmen = (int(m_r.group(1) or m_r.group(2)), int(m_r.group(2))) if m_r else None
    if rahmen and rahmen[0] > rahmen[1]:
        rahmen = None
    for e in einheiten:
        zeitraum_aus_titel(e, rahmen)
        if re.search(r"\d\s?[-–]$", e.titel):  # «… 2005-» stand nur für das offene Ende im Titel; sonst weg
            e.titel = re.sub(r"\s?[-–]$", "", e.titel).rstrip(" :;,")
    ergaenze_titel(einheiten)
    ergaenze_zeitraeume(einheiten, toc, rahmen)
    n_jahr = sum(1 for e in einheiten if e.zeitraum_quelle == "Signatur (Jahr)")
    if n_jahr:
        ergebnis["bemerkungen"].append(f"{n_jahr} Einheiten ohne Datum: Zeitraum «ca.» aus dem Jahr der Nummer "
                                       "«Jahr.Laufnummer» (Zeitraum-Quelle «Signatur (Jahr)»).")
    oben = eintrag.get("eltern_signatur", "") if eintrag and re.sub(r"\s", "", eintrag.get("signatur", "")) \
        .rstrip(".") == bestand.rstrip(".") else ""
    ergaenze_doppelpunkte(einheiten, bestand)
    excel_zeilen = zeilen_fuer_excel(einheiten, bestand, oben)
    if not excel_zeilen:
        ergebnis.update(status="Fehler",
                        bemerkungen=ergebnis["bemerkungen"] + ["Keine Signaturen erkannt – Aufbau des PDFs prüfen."])
        return ergebnis
    pruefung = pruefe_vollstaendigkeit(info.get("verbleib", []), einheiten, excel_zeilen)
    pruefung.update(pruefe_rahmen(alle, koerper, start, vorkommen, toc, modus))
    ergebnis["pruefung"] = pruefung
    typen = Counter(v.typ for v in vorkommen)
    if ersatz:
        schema = ersatz
        ergebnis["bemerkungen"].append(
            "Findmittel ohne Signaturen, nach Mappen/Schachteln gegliedert: je Mappe/Schachtel eine Einheit "
            "(Signatur Bestand:Nummer) – bitte prüfen." if ersatz == "Mappen/Schachteln" else
            "Findmittel ohne Signaturen: ganzer Inhalt in einer Zeile für den Bestand (in scope beim Bestand "
            "ergänzen, keine neue Einheit).")
    elif typen.get("voll", 0) >= len(vorkommen) * 0.5:
        schema = "Vollsignatur"
    elif typen.get("buchstabe_nr") and not (typen.get("roem") or typen.get("klein")):
        schema = "Buchstabe+Nr."
        ergebnis["bemerkungen"].append("Signaturen «Buchstabe Nummer» (z. B. «B 3») – Schreibweise in scope prüfen.")
    elif typen.get("roem") or typen.get("klein") or (typen.get("gross") and modus == "gliederung"):
        schema = "römisch/Buchstaben"
        ergebnis["bemerkungen"].append("Gliederung mit römischen Zahlen/Buchstaben – Signaturen sind aus dem "
                                       "Gliederungspfad gebildet (z. B. «II.A.3.»), bitte prüfen.")
    elif modus == "dezimal":
        schema = "dezimal"
    else:
        schema = "fortlaufend"
    ergebnis["gliederung"] = schema

    stufen = Counter(z["Stufe"] for z in excel_zeilen)
    arten: Counter = Counter()
    for z in excel_zeilen:
        for h in z["Prüfhinweise"].split("\n"):
            if h:
                arten[re.sub(r"\s*\(.*|:.*| \d.*", "", h).strip().rstrip(".")] += 1
    quellen = Counter(z["Zeitraum-Quelle"] or "(kein Zeitraum)" for z in excel_zeilen)
    teile = sum(1 for e in einheiten if e.art == "teil")
    mit_hinweis = sum(1 for z in excel_zeilen if z["Prüfhinweise"])
    meta_info = {
        "Findmittel -> scope-Import": f"{pdf.name}  ->  {ziel.name}",
        "Bestand": bestand,
        "Gliederung": schema,
        "Erzeugt": dt.datetime.now().strftime("%d.%m.%Y %H:%M") + " mit findmittel_zu_scope.py",
        "Schlussvermerke im Findmittel": "\n".join(info.get("schluss", [])) or "–",
        "Übersichtszeilen ignoriert": ", ".join(info.get("uebersicht", [])) or "–",
        "Vollständigkeit": vollstaendigkeit_kurz(pruefung),
        "Statistik": {
            "Zeilen (Verzeichnungseinheiten)": len(excel_zeilen),
            **{f"Stufe {k}": v for k, v in sorted(stufen.items())},
            "davon Teile (wiederholte Signaturen)": teile,
            "Zeilen mit Prüfhinweisen": mit_hinweis,
            **{f"Hinweis: {k}": v for k, v in arten.most_common()},
            **{f"Zeitraum aus {k}": v for k, v in quellen.most_common()},
        },
        "Konventionen": {
            "Hierarchie": "ID/Parent-ID verknüpfen die Zeilen; zusätzlich «Übergeordnete Signatur». " + (
                f"Die Zeile des Bestands {bestand} selbst nennt als übergeordnete Signatur "
                f"{oben or 'nichts (nicht im Katalog)'} – sie ergänzt den Bestand in scope, keine neue Einheit."
                if ersatz == "ohne Signaturen" else
                f"Die erste Ebene hängt direkt am Bestand {bestand} (Parent-ID leer)"
                + (" bzw. am Bestand, den die Spalte «Übergeordnete Signatur» nennt (Findmittel für mehrere "
                   "Bestände)." if wechsel and any(e.bestand for e in einheiten) else ".")),
            "Stufen": f"{STUFE_TIEFE_1} = oberste Gliederungsebene; {STUFE_GRUPPE} = Einheiten mit Untereinheiten "
                      f"oder Teilen; {STUFE_EINHEIT} = alle übrigen Einheiten und alle Teile.",
            "Teile": "Kommt eine Signatur im Findmittel mehrfach vor (mehrere Schachteln bzw. Einheiten mit derselben "
                     "Nummer) oder steht «…, Teil n» ohne Signatur, wird jede weitere Nennung ein «Teil» unter der "
                     "ersten Nennung. Der eigene Inhalt der ersten Nennung bleibt bei ihr (zählt als Teil 1). Teile "
                     "ohne eigenen Titel übernehmen den Titel der übergeordneten Einheit bzw. des vorherigen Teils "
                     "mit «, Teil n» und deren Zeitraum. "
                     + ("Teile tragen dieselbe Signatur wie im PDF – eindeutig ist die ID."
                        if not SIGNATUR_TEIL_MUSTER else f"Signaturen der Teile nach Muster {SIGNATUR_TEIL_MUSTER}."),
            "Zeitraum": "Aus der Datumsspalte bzw. dem Titel (Zeitangabe am Titelende wird entfernt), sonst aus dem "
                        "Inhaltsverzeichnis, den Untereinheiten, der übergeordneten Einheit oder geschätzt aus den "
                        "Jahreszahlen im Darin. Amtszeiten in Personen-Überschriften gelten nicht als Laufzeit. "
                        "Spielzeiten «1938/39» zählen als 1938–1939. von/bis als Text in der Genauigkeit des "
                        "Findmittels (JJJJ, MM.JJJJ oder TT.MM.JJJJ); Spielzeiten, Listen und «ab/ca.» stehen "
                        "wörtlich in «Entstehungszeitraum, Anm.».",
            "Darin": "Eine Zeile pro Aufzählungspunkt; Aufzählungszeichen entfernt, Zeilenumbrüche repariert, "
                     "eingerückte Unterzeilen mit «; » angehängt. Ein Datum (bzw. eine Schachtel) in der rechten "
                     "Spalte einer Darin-Zeile steht mit «, » am Ende ihres Eintrags. «Siehe auch …» steht in "
                     "«Verwandte Verzeichnungseinheiten». Ein Darin über "
                     f"{DARIN_MAX} Zeichen (Grenze einer Excel-Zelle) wird auf weitere Teile verteilt.",
            "Schachteln": "Eine Schachtelangabe («Schachtel 3», «11.1. Schachtel 2») gilt für das, was folgt: "
                          "für die nächsten Einheiten (bei abschnittsweise neu beginnender Zählung nur im "
                          "selben Abschnitt). Folgt direkt Text statt einer Signatur, wird er ein eigener Teil in "
                          "dieser Schachtel.",
            "Gliederung": "dezimal / fortlaufend = Signatur wie im PDF (Bestand + «:» + Nummer). Vollsignatur = "
                          "Signatur steht samt Bestand im PDF und wird unverändert übernommen. Buchstabe+Nr. = "
                          "«B 3» wird zu Bestand + «:B 3». römisch/Buchstaben = I. > A. > a) > 1.; die Signatur wird "
                          "aus dem Gliederungspfad gebildet (z. B. «II.A.3.») – bitte mit der Signaturpraxis abgleichen.",
            "Hilfsspalten": "Nr. im PDF, PDF-Seite, Zeitraum-Quelle und Prüfhinweise (grau) dienen nur der Kontrolle.",
            "Datumsoperatoren": f"«{OP_GENAU}» bei einem einzelnen Datum (nur «von» gefüllt), sonst «{OP_VON_BIS}» "
                                "(Wortlaut aus der StAZH-Erfassungsvorlage; bei Bedarf im Skript anpassen).",
        },
    }
    schreibe_excel(excel_zeilen, ziel, meta_info, pruefung)
    anteil = mit_hinweis / len(excel_zeilen)
    if pruefung["luecken"]:
        ergebnis["bemerkungen"].append(f"Nicht alles übernommen: {len(pruefung['luecken'])} PDF-Zeilen mit fehlenden "
                                       f"Wörtern (Blatt «Vollständigkeit»).")
    if pruefung["nur_im_vorspann"]:
        ergebnis["bemerkungen"].append("Signaturen nur im Inhaltsverzeichnis, nicht im Detailverzeichnis: "
                                       + ", ".join(pruefung["nur_im_vorspann"][:10]))
    if anteil > 0.4 and len(excel_zeilen) >= 5:
        ergebnis["status"] = "Prüfen"
        ergebnis["bemerkungen"].append("Viele Prüfhinweise – Aufbau weicht evtl. vom erwarteten Schema ab.")
    elif schema in ("römisch/Buchstaben", "Buchstabe+Nr.", "Mappen/Schachteln", "ohne Signaturen"):
        ergebnis["status"] = "Prüfen"
    if pruefung["anteil"] < 0.995 or any(x["art"] == "Schachtelangabe" for x in pruefung["luecken"]) \
            or meta.get("OCR"):
        ergebnis["status"] = "Prüfen"
    vorlauf = sum(1 for x in pruefung["nicht_uebernommen"] if x["art"] == NICHT_UEBERNOMMEN["vorlauf"])
    if vorlauf > 20 and vorlauf > 0.1 * max(1, len(koerper) - start):
        ergebnis["status"] = "Prüfen"
        ergebnis["bemerkungen"].append(f"{vorlauf} Zeilen Text vor der ersten Signatur (nicht übernommen) – "
                                       "Aufbau prüfen, evtl. nach Mappen/Schachteln gegliedert.")
    if any(len(e.darin) > 150 for e in einheiten):
        ergebnis["status"] = "Prüfen"
        ergebnis["bemerkungen"].append("Sehr lange Darin-Listen – vermutlich Tabellen-Findmittel (Zeilen ohne "
                                       "Signatur), Einheiten evtl. von Hand aufteilen.")
    if len(excel_zeilen) < 3:
        ergebnis["bemerkungen"].append("Nur wenige Einheiten erkannt.")
    ergebnis.update(einheiten=len(excel_zeilen), teile=teile, hinweise=mit_hinweis, anteil=round(anteil, 3),
                    excel=ziel.name, excel_pfad=str(ziel.resolve()), text=round(pruefung["anteil"], 4),
                    luecken=len(pruefung["luecken"]), nicht_uebernommen=len(pruefung["nicht_uebernommen"]))
    haeufigste = ", ".join(f"{k} ({v})" for k, v in arten.most_common(3))
    if haeufigste:
        ergebnis["bemerkungen"].append("Häufigste Hinweise: " + haeufigste)
    return ergebnis


# ----------------------------------------------------------------------------- Hauptprogramm


def sammle_pdfs(pfade: list[Path]) -> list[Path]:
    pdfs: list[Path] = []
    for p in pfade:
        if p.is_dir():
            pdfs.extend(sorted(x for x in p.rglob("*") if x.suffix.lower() == ".pdf" and not x.name.startswith(".")))
        elif p.suffix.lower() == ".pdf" and p.exists():
            pdfs.append(p)
    return list(dict.fromkeys(pdfs))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Findmittel-PDF(s) -> Excel für den scope-Import")
    ap.add_argument("eingabe", type=Path, nargs="+", help="PDF-Dateien und/oder Ordner mit PDFs")
    ap.add_argument("-o", "--output", type=Path,
                    help="Ziel: .xlsx-Datei (nur bei einem PDF) oder Ordner (Standard: neben dem PDF)")
    ap.add_argument("--bestand", help="Signatur des Bestands, z. B. VII.200. (nur bei einem PDF; "
                                      "Standard: aus Seite 1 bzw. Kopfzeile, PDF-Titel oder Dateiname)")
    ap.add_argument("--cache", type=Path, help="Ordner für einen Zeilen-Cache (schnellere Wiederholungen)")
    ap.add_argument("--katalog", type=Path, help="Liste aus findmittel_laden.py (verzeichnis.csv): liefert die "
                                                 "Bestandssignatur aus dem Online-Archiv zur Kontrolle bzw. als Ersatz")
    args = ap.parse_args(argv)
    katalog = lies_katalog(args.katalog) if args.katalog else None

    pdfs = sammle_pdfs(args.eingabe)
    if not pdfs:
        print("Keine PDF-Dateien gefunden.", file=sys.stderr)
        return 2
    einzeln = len(pdfs) == 1
    if args.bestand and not einzeln:
        print("--bestand geht nur zusammen mit einem einzelnen PDF.", file=sys.stderr)
        return 2
    ziel_datei = args.output if (einzeln and args.output and args.output.suffix.lower() == ".xlsx") else None
    ziel_ordner = args.output if (args.output and not ziel_datei) else None
    if ziel_ordner:
        ziel_ordner.mkdir(parents=True, exist_ok=True)

    ergebnisse = []
    for nr, pdf in enumerate(pdfs, start=1):
        ziel = ziel_datei or (ziel_ordner or pdf.parent) / f"{pdf.stem}_scope_import.xlsx"
        print(f"[{nr}/{len(pdfs)}] {pdf.name} …", end=" ", flush=True)
        try:
            e = verarbeite_pdf(pdf, ziel, args.bestand, args.cache, katalog)
        except Exception as ex:  # ein kaputtes PDF soll den Stapel nicht anhalten
            e = {"pdf": pdf.name, "status": "Fehler", "bemerkungen": [f"{type(ex).__name__}: {ex}"]}
            if einzeln:
                traceback.print_exc()
        ergebnisse.append(e)
        if e["status"] == "Fehler":
            print("FEHLER –", "; ".join(e["bemerkungen"]))
        else:
            print(f"{e['bestand']} {e['gliederung']}: {e['einheiten']} Einheiten ({e['teile']} Teile), "
                  f"Prüfhinweise bei {e['hinweise']} ({e['anteil']:.0%}), Text erfasst {e['text']:.1%}"
                  + (f" ({e['luecken']} Zeilen mit Lücken)" if e["luecken"] else "") + f" -> {e['excel']}"
                  + ("  [prüfen]" if e["status"] == "Prüfen" else ""))
    if not einzeln:
        uebersicht = (ziel_ordner or Path.cwd()) / "uebersicht_scope_import.xlsx"
        schreibe_uebersicht(ergebnisse, uebersicht)
        print(f"Übersicht: {uebersicht}")
    return 1 if any(e["status"] == "Fehler" for e in ergebnisse) else 0


if __name__ == "__main__":
    sys.exit(main())
