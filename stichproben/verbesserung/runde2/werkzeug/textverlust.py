"""Textverlust zwischen zwei Läufen: Wörter aus Titel, Darin, Entstehungszeitraum-Anm. und Schlussvermerken, die im
neuen Lauf in derselben Datei fehlen (Multimenge), sowie neue Schlussvermerk-Zeilen je Datei.
Aufruf: python -I textverlust.py <alt> <neu> <ausgabe.csv>"""
import collections, csv, glob, os, re, sys, openpyxl
alt, neu, aus = sys.argv[1:4]
def lies(p):
    wb = openpyxl.load_workbook(p, read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    kopf = [str(k) for k in rows[0]]
    ix = {k: kopf.index(k) for k in ("Titel", "Darin", "Entstehungszeitraum, Anm.")}
    texte = []
    for r in rows[1:]:
        if not r or r[0] is None: continue
        texte += [str(r[ix[k]] or "") for k in ix]
    info = {str(x[0]): x[1] for x in wb["Info"].iter_rows(values_only=True) if x and x[0]}
    schluss = str(info.get("Schlussvermerke im Findmittel") or "")
    return texte, schluss
def woerter(t):
    return collections.Counter(w.strip(".,;:()[]«»„“\"'") for w in re.split(r"\s+", t) if w.strip(".,;:()[]«»„“\"'"))
zeilen = []
for pa in sorted(glob.glob(f"{alt}/*_scope_import.xlsx")):
    name = os.path.basename(pa)
    if name.startswith("uebersicht"): continue
    pn = f"{neu}/{name}"
    ta, sa = lies(pa); tn, sn = lies(pn)
    # Schlussvermerke stehen roh im Blatt Info (Trennstriche am Zeilenende nicht repariert): beide Lesarten zählen
    wa = woerter(" ".join(ta) + " " + sa)
    wn = woerter(" ".join(tn) + " " + re.sub(r"-\n", "", sn)) | woerter(" ".join(tn) + " " + re.sub(r"-\n", "-", sn)) \
        | woerter(" ".join(tn) + " " + sn)
    fehlt = wa - wn; dazu = wn - wa
    neu_s = [x for x in sn.split("\n") if x and x not in sa.split("\n")]
    weg_s = [x for x in sa.split("\n") if x and x not in sn.split("\n")]
    if fehlt or neu_s or weg_s:
        zeilen.append({"pdf": name.split("_")[0], "fehlende_woerter": " ".join(f"{w}×{n}" if n > 1 else w for w, n in fehlt.items()),
                       "neue_woerter": " ".join(f"{w}×{n}" if n > 1 else w for w, n in dazu.items())[:300],
                       "neue_schlusszeilen": len(neu_s), "weg_schlusszeilen": len(weg_s),
                       "neu_schluss": " ⏎ ".join(neu_s)[:600], "weg_schluss": " ⏎ ".join(weg_s)[:300]})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(zeilen[0]) if zeilen else ["pdf"], delimiter=";")
    w.writeheader(); w.writerows(zeilen)
print(f"{len(zeilen)} Dateien; mit fehlenden Wörtern: {sum(1 for z in zeilen if z['fehlende_woerter'])}; "
      f"mit neuen Schlusszeilen: {sum(1 for z in zeilen if z['neue_schlusszeilen'])}; "
      f"neue Schlusszeilen gesamt: {sum(z['neue_schlusszeilen'] for z in zeilen)}")
for z in zeilen:
    if z["fehlende_woerter"]:
        print("FEHLT", z["pdf"], z["fehlende_woerter"][:300])
