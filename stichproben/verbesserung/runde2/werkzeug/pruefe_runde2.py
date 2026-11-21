"""Prüft die Fälle der Verbesserungsrunde 2 (runde2_faelle.csv) an den Excel-Ausgaben eines oder mehrerer Läufe.
Aufruf: python -I pruefe_runde2.py runde2_faelle.csv ordner1 [ordner2 …]
Felder: Einheiten (Anzahl Zeilen), Anzahl (Vorkommen der Signatur), Titel, Darin, von, bis, Schluss (Schlussvermerke im
Blatt Info), NichtUebernommen (Info «Nicht übernommen»). Operatoren: =, enthält, nicht, beginnt, endet."""
import collections, csv, sys, openpyxl
faelle = list(csv.DictReader(open(sys.argv[1], encoding="utf-8", newline=""), delimiter=";"))
ordner = sys.argv[2:]
cache = {}
def lade(o, pdf):
    if (o, pdf) not in cache:
        wb = openpyxl.load_workbook(f"{o}/{pdf}_scope_import.xlsx", read_only=True)
        rows = list(wb["scope-Import"].iter_rows(values_only=True))
        kopf = [str(k) for k in rows[0]]
        einh = [dict(zip(kopf, r)) for r in rows[1:] if r and r[0] is not None]
        info = {str(x[0]): x[1] for x in wb["Info"].iter_rows(values_only=True) if x and x[0]}
        cache[(o, pdf)] = (einh, info)
    return cache[(o, pdf)]
def wert(o, f):
    einh, info = lade(o, f["pdf"])
    feld = f["feld"]
    if feld == "Einheiten": return str(len(einh))
    if feld == "Anzahl": return str(sum(1 for e in einh if e["Signatur"] == f["signatur"]))
    if feld == "Schluss": return str(info.get("Schlussvermerke im Findmittel") or "")
    if feld == "NichtUebernommen": return str(info.get("Nicht übernommen") or "")
    treffer = [e for e in einh if e["Signatur"] == f["signatur"]]
    n = int(f["n"] or 1)
    if len(treffer) < n: return None
    v = treffer[n - 1].get(feld)
    return "" if v is None else str(v)
def ok(f, w):
    if w is None: return False
    s, op = f["soll"], f["op"]
    return {"=": w == s, "enthält": s in w, "nicht": s not in w, "beginnt": w.startswith(s), "endet": w.endswith(s)}[op]
gut = [0] * len(ordner)
for f in faelle:
    teile = []
    for k, o in enumerate(ordner):
        w = wert(o, f); t = ok(f, w); gut[k] += t
        kurz = "FEHLT" if w is None else (w if len(w) <= 40 else w[:37] + "…").replace("\n", " ⏎ ")
        teile.append(f"{'ok' if t else 'XX'} {kurz}")
    print(f"{f['pdf']:8} {f['signatur'][:22]:22} {f['feld']:9} {f['op']:7} {f['soll'][:30]!r:32} | " + " | ".join(teile))
print("richtig:", " / ".join(f"{g} von {len(faelle)}" for g in gut))
