"""Textverlust zwischen zwei Läufen: Wörter der importierten Felder, die im neuen Lauf fehlen bzw. neu sind, und
Schlussvermerke im Blatt Info. Aufruf: python -I textverlust.py alt neu dateiliste aus.csv"""
import csv, re, sys
from collections import Counter
from pathlib import Path
import openpyxl
FELDER = ("Titel", "Darin", "Umfang", "Entstehungszeitraum, Anm.", "Verwandte Verzeichnungseinheiten")
def lies(p):
    wb = openpyxl.load_workbook(p, read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True)); h = rows[0]
    w = Counter()
    for r in rows[1:]:
        d = dict(zip(h, r))
        for f in FELDER:
            if d.get(f):
                w.update(re.findall(r"\w+", str(d[f]).lower()))
    schluss = [r[1] for r in wb["Info"].iter_rows(values_only=True) if r and r[0] == "Schlussvermerke im Findmittel"]
    sw = Counter(re.findall(r"\w+", " ".join(str(x) for x in schluss if x).lower()))
    return w, sw
alt, neu, liste, aus = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
with open(aus, "w", newline="", encoding="utf-8") as f:
    out = csv.writer(f, delimiter=";")
    out.writerow(["pdf", "fehlende_woerter", "anzahl_fehlend", "neue_woerter", "anzahl_neu", "info_neu", "info_weg"])
    for d in open(liste).read().split():
        a, b = alt / f"{d}_scope_import.xlsx", neu / f"{d}_scope_import.xlsx"
        if not a.exists() or not b.exists():
            continue
        (wa, sa), (wb_, sb) = lies(a), lies(b)
        fehlt, neu_w = wa - wb_, wb_ - wa
        info_neu, info_weg = sb - sa, sa - sb
        if fehlt or info_weg:
            out.writerow([d, " ".join(f"{k}×{n}" if n > 1 else k for k, n in fehlt.most_common(30)), sum(fehlt.values()),
                          " ".join(f"{k}×{n}" if n > 1 else k for k, n in neu_w.most_common(15)), sum(neu_w.values()),
                          sum(info_neu.values()), sum(info_weg.values())])
