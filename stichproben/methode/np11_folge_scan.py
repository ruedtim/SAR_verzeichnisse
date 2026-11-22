"""Suchlauf «Nummernfolge im Darin» (Muster D175561): Einheit, deren Signatur auf die Nummer n endet und deren Darin mit
mindestens drei Zeilen «n+1», «n+2», «n+3» … (am Zeilenanfang, mit Punkt oder Leerzeichen) weitergeht, als ob die Folge der
Signaturen dort fortgesetzt würde. Aufruf: python -I folge_scan.py <ordner> <aus.csv>"""
import csv, glob, os, re, sys
import openpyxl
o, aus = sys.argv[1:3]
out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    for r in rows[1:]:
        if not r or r[0] is None:
            continue
        e = dict(zip(h, r))
        m = re.search(r"(\d+)\.?$", str(e["Signatur"] or ""))
        if not m:
            continue
        n0 = int(m.group(1))
        dz = [x.strip() for x in str(e.get("Darin") or "").split("\n") if x.strip()]
        nums = []
        for x in dz:
            mm = re.match(r"(\d{1,4})[.\s]", x)
            nums.append(int(mm.group(1)) if mm else None)
        # längste Folge n0+1, n0+2, ... in Darin-Reihenfolge (Lücken durch andere Zeilen erlaubt)
        erwart, treffer = n0 + 1, []
        for x, v in zip(dz, nums):
            if v == erwart:
                treffer.append(x[:60]); erwart += 1
        if len(treffer) >= 3:
            out.append({"datei": d, "id": e["ID"], "signatur": e["Signatur"], "seite": e["PDF-Seite"], "folge": f"{n0 + 1}–{erwart - 1}",
                        "anzahl": len(treffer), "beispiel": " | ".join(treffer[:3])})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "id", "signatur", "seite", "folge", "anzahl", "beispiel"], delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Treffer in", len({x['datei'] for x in out}), "Dateien")
for x in out:
    print(f"{x['datei']:<8} ID {x['id']:<5} {x['signatur'][:28]:<28} S.{x['seite']:<3} Folge {x['folge']:<9} | {x['beispiel'][:110]}")
