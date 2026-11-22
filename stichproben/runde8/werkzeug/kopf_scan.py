"""Tabellenköpfe mit Spalte «Schachtel» und Zeilen, deren letzte Zahl unter dem Kopfwort steht.
Aufruf: python -I kopf_scan.py <cache_ordner>"""
import glob, json, os, re, sys
for p in sorted(glob.glob(f"{sys.argv[1]}/D*.zeilen.json")):
    zz = json.load(open(p, encoding="utf-8"))["zeilen"]
    kopf = None
    treffer = []
    for z in zz:
        w = z["worte"]
        t = [x[0] for x in w]
        if "Schachtel" in t and any(k in t for k in ("Titel", "Inhalt", "Jahre", "Jahr", "Nr.", "Signatur", "Datum")):
            i = t.index("Schachtel")
            kopf = (w[i][1], w[i][2])
            continue
        if kopf and len(w) >= 3 and re.fullmatch(r"\d{1,3}[a-z]?", w[-1][0]) and abs(w[-1][1] - kopf[0]) <= 8:
            treffer.append(" ".join(t)[:70])
    if treffer:
        print(os.path.basename(p).split(".")[0], len(treffer), "|", treffer[0], "|", treffer[-1])
