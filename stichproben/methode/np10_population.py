"""Grundgesamtheit der nie geprüften Dateien und ihre Merkmale (Gliederung, Einheiten, Seiten, Verdachtssignale).
Aufruf: python -I population.py <excel_ordner> <stichproben> <geaenderte_dateien.txt> <aus.csv>"""
import csv, glob, os, re, sys
import openpyxl
o, stp, geae, aus = sys.argv[1:5]
geprueft = {}
for f in sorted(glob.glob(f"{stp}/funde*.csv") + glob.glob(f"{stp}/zusatzfunde*.csv") + [f"{stp}/offen_kritisch.csv"]):
    for r in csv.DictReader(open(f, encoding="utf-8"), delimiter=";"):
        d = (r.get("pdf") or r.get("datei") or "").replace(".pdf", "")
        if d:
            geprueft.setdefault(d, os.path.basename(f))
geaendert = {l.split("_")[0] for l in open(geae, encoding="utf-8") if l.strip()}
verd = {}
for r in csv.DictReader(open(f"{stp}/roh/np9_verdacht.csv", encoding="utf-8"), delimiter=";"):
    verd.setdefault(r["datei"], []).append(r["signal"])
zeilen = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    wb = openpyxl.load_workbook(p, read_only=True)
    info = {}
    for x in wb["Info"].iter_rows(values_only=True):
        if x and x[0]:
            info.setdefault(str(x[0]), x[1])
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    einh = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    seiten = max([e["PDF-Seite"] or 0 for e in einh] or [0])
    ebenen = max([e["Ebene"] or 0 for e in einh] or [0])
    zeilen.append({"datei": d, "gliederung": info.get("Gliederung"), "einheiten": len(einh), "max_seite": seiten,
                   "max_ebene": ebenen, "geprueft": geprueft.get(d, ""), "geaendert_r8": "ja" if d in geaendert else "",
                   "verdacht": ",".join(verd.get(d, []))})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(zeilen[0]), delimiter=";")
    w.writeheader(); w.writerows(zeilen)
nie = [z for z in zeilen if not z["geprueft"]]
print(len(zeilen), "Dateien,", len(nie), "nie in einer Fundliste;", sum(1 for z in nie if z["geaendert_r8"]), "davon in Runde 8 geändert;",
      sum(1 for z in nie if z["verdacht"]), "mit Verdachtssignal")
