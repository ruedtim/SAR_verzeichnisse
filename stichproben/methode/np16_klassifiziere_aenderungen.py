"""Änderungen Runde 12 -> Runde 13 je Einheit einordnen (NP16): Welche Änderungen sind nur der Leerschlag nach dem Strich
(Regel 8, «1962 –1. Juli» -> «1962 – 1. Juli»), welche sind sachlich? Verglichen wird über Signatur und n-tes Vorkommen, wie
np8/vgl.py. Hilfsspalten («Nr. im PDF», «PDF-Seite», «Zeitraum-Quelle») und «Prüfhinweise» zählen getrennt.
Aufruf: python -I klassifiziere_aenderungen.py <alt_ordner> <neu_ordner> <dateiliste> <aus.csv>
Schreibt je geänderter Zelle eine Zeile und druckt je Datei, ob sie nur Leerschlag-Änderungen hat."""
import collections, csv, re, sys
import openpyxl

alt, neu, liste, aus = sys.argv[1:5]
HILF = {"Nr. im PDF", "PDF-Seite", "Zeitraum-Quelle", "ID", "Parent-ID"}


def lade(p):
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    n = collections.Counter(); out = {}
    for e in ee:
        s = str(e.get("Signatur") or "")
        n[s] += 1
        out[(s, n[s])] = e
    return out, h


def strichnorm(s):
    return re.sub(r"\s*([–—-])\s*", r"\1", str(s if s is not None else ""))


zeilen, je_datei = [], {}
for d in [l.strip() for l in open(liste) if l.strip()]:
    a, h = lade(f"{alt}/{d}_scope_import.xlsx")
    b, _ = lade(f"{neu}/{d}_scope_import.xlsx")
    c = collections.Counter()
    for k in sorted(set(a) | set(b), key=lambda x: (x[0], x[1])):
        ea, eb = a.get(k), b.get(k)
        if ea is None or eb is None:
            art = "NEU" if ea is None else "WEG"
            c["sachlich"] += 1
            zeilen.append({"datei": d, "signatur": k[0], "n": k[1], "feld": "(Einheit)", "art": art, "alt": "" if ea is None else str(ea.get("Titel"))[:150],
                           "neu": "" if eb is None else str(eb.get("Titel"))[:150]})
            continue
        for f in h:
            if f in HILF:
                continue
            va, vb = ea.get(f), eb.get(f)
            if (va or "") == (vb or ""):
                continue
            if f == "Prüfhinweise":
                art = "hinweis"
            elif strichnorm(va) == strichnorm(vb) and f in ("Titel", "Darin", "Entstehungszeitraum, Anm.", "Umfang"):
                art = "leerschlag"
            else:
                art = "sachlich"
            c[art] += 1
            zeilen.append({"datei": d, "signatur": k[0], "n": k[1], "feld": f, "art": art, "alt": str(va if va is not None else "")[:300],
                           "neu": str(vb if vb is not None else "")[:300]})
    je_datei[d] = c
with open(aus, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["datei", "signatur", "n", "feld", "art", "alt", "neu"], delimiter=";")
    w.writeheader(); w.writerows(zeilen)
nur = sorted(d for d, c in je_datei.items() if c["sachlich"] == 0)
print("Dateien:", len(je_datei), "| nur Leerschlag/Hinweis:", len(nur), "| mit sachlicher Änderung:", len(je_datei) - len(nur))
print("sachlich je Datei:", {d: c["sachlich"] for d, c in sorted(je_datei.items(), key=lambda x: -x[1]["sachlich"]) if c["sachlich"]})
print("Zellen gesamt:", dict(sum(je_datei.values(), collections.Counter())))
open(aus.replace(".csv", "_nur_leerschlag.txt"), "w").write("\n".join(nur) + "\n")
