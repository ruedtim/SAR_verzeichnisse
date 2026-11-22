"""Suchlauf «Nr.-Spalte durchlaufend» (Muster D1391): Findmittel, deren Einheiten aus Schachtelnummern gebildet sind
(Hinweis «Signatur aus der Nummer der Schachtel/Mappe»), während die Darin-Zeilen aller Schachteln eine durchlaufende
Nummernfolge 1, 2, 3 … über die Schachtelgrenzen tragen. Dann sind die Nummern Signaturen, nicht Positionen.
Aufruf: python -I nrspalte_scan.py <ordner> <aus.csv>"""
import csv, glob, os, re, sys
import openpyxl
o, aus = sys.argv[1:3]
out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    beh = [e for e in ee if re.search(r"Nummer der (Schachtel|Mappe)", str(e.get("Prüfhinweise") or ""))]
    if len(beh) < 2:
        continue
    folge = []
    for e in beh:
        for x in str(e.get("Darin") or "").split("\n"):
            m = re.match(r"\s*(\d{1,4})[.\s]", x)
            if m:
                folge.append((int(m.group(1)), e["Signatur"]))
    if len(folge) < 4:
        continue
    # durchlaufend = jede Zahl ist Vorgänger + 1, über mindestens zwei Einheiten, ohne Neubeginn bei 1
    neu_anfang = sum(1 for (a, _), (b, _) in zip(folge, folge[1:]) if b <= a)
    steigend = sum(1 for (a, _), (b, _) in zip(folge, folge[1:]) if b == a + 1)
    einheiten = len({s for _, s in folge})
    if einheiten >= 2 and neu_anfang <= 1 and steigend >= 0.8 * (len(folge) - 1):
        out.append({"datei": d, "schachtel_einheiten": len(beh), "nummern": len(folge), "von": folge[0][0], "bis": folge[-1][0],
                    "neubeginne": neu_anfang, "beispiel": ", ".join(f"{n}@{s.split(':')[-1]}" for n, s in folge[:6])})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "schachtel_einheiten", "nummern", "von", "bis", "neubeginne", "beispiel"], delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Dateien")
for x in out:
    print(f"{x['datei']:<8} {x['schachtel_einheiten']:>3} Schachtel-Einheiten, Nummern {x['von']}–{x['bis']} ({x['nummern']}), Neubeginne {x['neubeginne']} | {x['beispiel']}")
