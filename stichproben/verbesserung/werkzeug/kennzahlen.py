"""Kennzahlen eines Laufs: Einheiten, «[ohne Titel]», Text erfasst 100 %, doppelte Schlüssel, Übersichtszeilen.
Aufruf: python -I kennzahlen.py <ordner> [<ordner2>]"""
import sys, glob, os, collections, openpyxl
def zahlen(o):
    k = collections.Counter(); txt = {}
    for p in sorted(glob.glob(f"{o}/*_scope_import.xlsx")):
        if os.path.basename(p).startswith("uebersicht"): continue
        wb = openpyxl.load_workbook(p, read_only=True)
        rows = [r for r in wb["scope-Import"].iter_rows(min_row=2, values_only=True) if r and r[0] is not None]
        k["Dateien"] += 1; k["Einheiten"] += len(rows)
        k["[ohne Titel]"] += sum(1 for r in rows if (r[3] or "").startswith("[ohne Titel]"))
        schl = collections.Counter((r[2], r[6]) for r in rows)
        k["doppelte Schlüssel (überzählig)"] += sum(n - 1 for n in schl.values() if n > 1)
        info = {str(x[0]): x[1] for x in wb["Info"].iter_rows(values_only=True) if x and x[0]}
        t = str(info.get("davon im Import gefunden", "")); txt[os.path.basename(p)] = t
        if "(100.00%)" in t: k["Text erfasst 100 %"] += 1
        k["mit Übersichtszeilen"] += info.get("Übersichtszeilen ignoriert", "–") not in ("–", None, "")
    return k, txt
erg = [zahlen(o) for o in sys.argv[1:]]
for key in erg[0][0]:
    print(f"{key:34}", " | ".join(str(e[0][key]) for e in erg))
if len(erg) == 2:
    d = [(f, erg[0][1][f], erg[1][1].get(f)) for f in erg[0][1] if erg[0][1][f] != erg[1][1].get(f)]
    print("Text erfasst geändert:", d[:20])
