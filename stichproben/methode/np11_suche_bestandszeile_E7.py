"""Suchlauf: Dateien mit nur einer Bestandszeile («ohne Signaturen»), deren Darin
(a) Zeilen mit einer Signatur des Bestands beginnt (wie D1263 «V.F. b.13.c:1 …») oder
(b) eine Schachtel-/Mappen-Nummernspalte zeigt (wie D2372 «… 1», «… 2», «… 3» bzw. Kopf «Schachtel-Nr.»).
Aufruf: uv run --quiet --with openpyxl python -I suche_bestandszeile.py <ordner aus_neu>"""
import glob
import os
import re
import sys

import openpyxl

ordner = sys.argv[1]


def norm(s):
    return re.sub(r"[\s.]", "", s or "")


for pfad in sorted(glob.glob(os.path.join(ordner, "*_scope_import.xlsx"))):
    d = os.path.basename(pfad).split("_")[0]
    try:
        wb = openpyxl.load_workbook(pfad, read_only=True)
        rows = list(wb["scope-Import"].iter_rows(values_only=True))
    except Exception as e:  # noqa: BLE001
        print(d, "FEHLER", e)
        continue
    if len(rows) != 2:
        continue
    h = rows[0]
    e = dict(zip(h, rows[1]))
    if e.get("Stufe") != "Bestand":
        continue
    best = norm(str(e["Signatur"]))
    darin = (e.get("Darin") or "").split("\n")
    a = [z for z in darin if norm(z).startswith(best) and re.match(r"^\S+\s*\S*:\s*\d", z)]
    nummern = [int(m.group(1)) for z in darin for m in [re.search(r"\s(\d{1,3})$", z.strip())] if m]
    kopf = [z for z in darin if re.search(r"Schachtel|Mappe|Karton", z) and re.search(r"Nr\.?|Nummer", z)]
    folge = len(nummern) >= 2 and nummern[:3] == list(range(nummern[0], nummern[0] + min(3, len(nummern))))
    if a or kopf or folge:
        print(f"{d}\t{e['Signatur']}\tDarin {len(darin)} Z.\t(a) {len(a)} Signaturzeilen\t(b) Kopf {len(kopf)}, Nummernfolge {nummern[:6] if folge else '-'}")
        for z in (a[:2] + kopf[:1]):
            print("      ", z[:110])
