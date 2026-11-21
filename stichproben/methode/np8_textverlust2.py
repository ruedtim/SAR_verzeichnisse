"""Textverlust alt -> neu über alle Textspalten und das Blatt Info, abgeglichen mit der Häufigkeit im PDF.
Ein Wort gilt nur als verloren, wenn es im neuen Stand seltener vorkommt als min(alt, PDF).
So zählen entfernte Dubletten (Übersicht doppelt gelesen) nicht als Verlust.
Aufruf: python -I textverlust2.py <alt> <neu> <cache_ordner> <ausgabe.csv> [D ...]"""
import collections, csv, glob, json, os, re, sys
import openpyxl

alt, neu, cache, aus, *nur = sys.argv[1:]
OHNE = {"ID", "Parent-ID", "Ebene", "Stufe", "Teil", "Übergeordnete Signatur", "Prüfhinweise", "PDF-Seite",
        "Zeitraum-Quelle"}
INFO_OHNE = {"Erzeugt"}
TRENN = re.compile(r"[\s–—\-/]+")
RAND = ".,;:()[]«»„“\"'"


def woerter(t):
    return collections.Counter(w.strip(RAND) for w in TRENN.split(t) if w.strip(RAND))


def lies(p):
    wb = openpyxl.load_workbook(p, read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    kopf = [str(k) for k in rows[0]]
    texte = []
    for r in rows[1:]:
        if not r or r[0] is None:
            continue
        texte += [str(v) for k, v in zip(kopf, r) if k not in OHNE and v not in (None, "")]
    for x in wb["Info"].iter_rows(values_only=True):
        if x and x[0] and str(x[0]) not in INFO_OHNE:
            texte += [str(v) for v in x[1:] if v not in (None, "")]
    t = " ".join(texte)
    # Trennstriche am Zeilenende: beide Lesarten
    return woerter(t) | woerter(re.sub(r"-\n", "", t))


def pdfwoerter(d):
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    t = "\n".join(" ".join(w[0] for w in z["worte"]) for z in zz)
    return woerter(t) | woerter(re.sub(r"-\n", "", t))


zeilen = []
for pa in sorted(glob.glob(f"{alt}/D*_scope_import.xlsx")):
    d = os.path.basename(pa).split("_")[0]
    if nur and d not in nur:
        continue
    wa, wn, wp = lies(pa), lies(f"{neu}/{d}_scope_import.xlsx"), pdfwoerter(d)
    verloren = {w: min(wa[w], wp[w]) - wn[w] for w in wa if min(wa[w], wp[w]) > wn[w]}
    dubletten = {w: wa[w] - max(wn[w], wp[w]) for w in wa if wa[w] > wn[w] and wa[w] > wp[w] and wn[w] >= min(wa[w], wp[w])}
    zeilen.append({"pdf": d, "verloren": " ".join(f"{w}×{n}" if n > 1 else w for w, n in sorted(verloren.items())),
                   "n_verloren": sum(verloren.values()),
                   "dubletten_weg": sum(dubletten.values()),
                   "neu_mehr": sum((wn - wa).values())})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(zeilen[0]), delimiter=";")
    w.writeheader()
    w.writerows(zeilen)
for z in zeilen:
    print(f"{z['pdf']:8} verloren {z['n_verloren']:4}  Dubletten weg {z['dubletten_weg']:4}  neu mehr {z['neu_mehr']:4}  "
          f"{z['verloren'][:240]}")
