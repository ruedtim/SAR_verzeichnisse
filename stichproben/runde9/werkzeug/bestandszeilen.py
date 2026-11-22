"""Ausgaben, die nur aus einer Bestandszeile bestehen: Anzahl Darin-Zeilen und Muster im Darin.
Aufruf: python -I bestandszeilen.py <ausgabeordner>"""
import glob
import re
import sys

import openpyxl

for p in sorted(glob.glob(sys.argv[1] + "/D*_scope_import.xlsx")):
    wb = openpyxl.load_workbook(p, read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    if len(rows) != 2:
        continue
    d = dict(zip(h, rows[1]))
    darin = (d["Darin"] or "").split("\n") if d["Darin"] else []
    vollsig = sum(1 for z in darin if re.match(r"[IVX]{1,4}\.\s?[A-Z]", z))
    zahl = sum(1 for z in darin if re.match(r"\d{1,3}\.?\s", z))
    endzahl = sum(1 for z in darin if re.search(r"\s\d{1,3}$", z))
    print(p.split("/")[-1].split("_")[0], d["Signatur"], f"Darin {len(darin)}", f"voll {vollsig}", f"zahl {zahl}",
          f"endzahl {endzahl}", "|", (darin[0] if darin else "")[:60], "|", (darin[1] if len(darin) > 1 else "")[:50])
