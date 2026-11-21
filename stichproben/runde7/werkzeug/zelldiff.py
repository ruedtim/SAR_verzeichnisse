"""Zellunterschiede einer Datei zwischen zwei Läufen: python -I zelldiff.py <alt> <neu> <D-Nummer> [max] [breite]"""
import sys, openpyxl
alt, neu, d = sys.argv[1], sys.argv[2], sys.argv[3]
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 30
br = int(sys.argv[5]) if len(sys.argv) > 5 else 110
def lade(o):
    rows = list(openpyxl.load_workbook(f"{o}/{d}_scope_import.xlsx", read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    return h, [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
h, a = lade(alt); _, b = lade(neu)
ka = {(r["Signatur"], r["Teil"]): r for r in a}; kb = {(r["Signatur"], r["Teil"]): r for r in b}
n = 0
for k in [k for k in ka if k not in kb]:
    print("WEG ", k, str(ka[k]["Titel"])[:br]); n += 1
for k in [k for k in kb if k not in ka]:
    print("NEU ", k, str(kb[k]["Titel"])[:br]); n += 1
for k in [k for k in ka if k in kb]:
    for c in h:
        if c in ("ID", "Parent-ID"): continue
        if ka[k][c] != kb[k][c]:
            print(f"{k[0]}{'/T'+str(k[1]) if k[1] else ''} {c}: {str(ka[k][c])[:br]!r} => {str(kb[k][c])[:br]!r}"); n += 1
    if n > mx: break
