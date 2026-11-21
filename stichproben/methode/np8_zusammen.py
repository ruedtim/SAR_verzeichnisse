"""Pakete zusammenführen: Urteile zählen (je Paket, Datei, Regel), Funde zu funde_nachpruefung8.csv.
Aufruf: python -I zusammen.py <pakete_ordner> <aus_funde.csv>"""
import collections, csv, glob, re, sys

ordner, aus = sys.argv[1:3]
urteile = []
for p in sorted(glob.glob(f"{ordner}/paket_*_urteile.csv")):
    n = re.search(r"paket_(\d+)", p).group(1)
    for r in csv.DictReader(open(p, encoding="utf-8", newline=""), delimiter=";"):
        r["paket"] = n
        try:
            r["_n"] = int(str(r.get("n") or "1").strip() or 1)
        except ValueError:
            r["_n"] = 1
        urteile.append(r)
funde = []
for p in sorted(glob.glob(f"{ordner}/paket_*_funde.csv")):
    n = re.search(r"paket_(\d+)", p).group(1)
    for r in csv.DictReader(open(p, encoding="utf-8", newline=""), delimiter=";"):
        r["paket"] = n
        funde.append(r)


def u(x):
    x = (x or "").strip().lower()
    return "besser" if x.startswith("bess") else "schlechter" if x.startswith("schl") else "gleich" if x.startswith("gl") else x


ges = collections.Counter()
je_datei = collections.defaultdict(collections.Counter)
je_regel = collections.defaultdict(collections.Counter)
for r in urteile:
    k = u(r["urteil"])
    ges[k] += r["_n"]
    je_datei[r["pdf"].replace(".pdf", "")][k] += r["_n"]
    for rg in re.findall(r"\d+|nicht angekündigt", r.get("regel") or "") or ["?"]:
        je_regel[rg][k] += r["_n"]
print("Urteile gesamt (Einheiten):", dict(ges), "Zeilen:", len(urteile))
print("\nje Datei:")
for d in sorted(je_datei):
    c = je_datei[d]
    print(f"  {d:9} besser {c['besser']:4} gleich {c['gleich']:4} schlechter {c['schlechter']:4}")
print("\nje Regel:")
for rg in sorted(je_regel, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else 0, x)):
    c = je_regel[rg]
    print(f"  {rg:18} besser {c['besser']:4} gleich {c['gleich']:4} schlechter {c['schlechter']:4}")
st = collections.Counter((r["status"] or "").strip() for r in funde)
sw = collections.Counter(((r["status"] or "").strip(), (r["schwere"] or "").strip()) for r in funde)
print("\nFunde:", len(funde), dict(st))
print("Status × Schwere:", dict(sw))
felder = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist"]
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader()
    for r in sorted(funde, key=lambda r: ((r["status"] or "") == "neu", r["pdf"])):
        r = dict(r)
        if r["pdf"] and not r["pdf"].endswith(".pdf"):
            r["pdf"] += ".pdf"
        w.writerow(r)
