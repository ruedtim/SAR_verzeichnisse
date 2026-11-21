"""Einheiten nach Signatur-Muster zeigen: python sig.py <xlsx> <regex> [darin_zeilen] [breite]
regex wird auf die Signatur angewandt (re.search); «#a-b» zeigt die IDs a bis b."""
import re
import sys

import openpyxl

wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
rows = list(wb["scope-Import"].iter_rows(values_only=True))
h = rows[0]
muster = sys.argv[2]
nd = int(sys.argv[3]) if len(sys.argv) > 3 else 4
br = int(sys.argv[4]) if len(sys.argv) > 4 else 90
m = re.fullmatch(r"#(\d+)-(\d+)", muster)
for r in rows[1:]:
    d = dict(zip(h, r))
    if m:
        if not (int(m.group(1)) <= int(d["ID"]) <= int(m.group(2))):
            continue
    elif not re.search(muster, str(d["Signatur"])):
        continue
    zr = d["Entstehungszeitraum"] or ""
    print(f"ID {d['ID']} P{d['Parent-ID']} {d['Signatur']} [{d['Stufe']}/E{d['Ebene']}{'/T' + str(d['Teil']) if d['Teil'] else ''}]"
          f" S.{d['PDF-Seite']} Sch {d['Schachtel-Nr.'] or '-'} | {zr} ({d['Zeitraum-Quelle'] or ''})")
    print(f"   Titel: {str(d['Titel'])[:br]}")
    if d["Umfang"]:
        print(f"   Umfang: {d['Umfang']}")
    darin = (d["Darin"] or "").split("\n") if d["Darin"] else []
    for z in darin[:nd]:
        print(f"   D: {z[:br]}")
    if len(darin) > nd:
        print(f"   D: … ({len(darin)} Zeilen)")
    if d["Prüfhinweise"]:
        print(f"   H: {str(d['Prüfhinweise'])[:300]}")
