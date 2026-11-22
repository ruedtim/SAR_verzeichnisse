"""Verdachtsliste für kritische Fehler über alle Dateien (ungeprüft, nur Signale aus dem Blatt Info/Vollständigkeit
und dem Zeilen-Cache):
  V  Vorspann mit >= 25 Zeilen und Signaturen, die nur im Vorspann stehen   -> Verzeichnisteil evtl. verworfen
  S  Schlussvermerke mit >= 20 Zeilen                                       -> Inhalt evtl. im Blatt Info
  N  «Nicht übernommen» >= 10 Zeilen                                        -> Überschriften/Text nicht zugeordnet
  W  Text erfasst < 100 %                                                   -> Wörter fehlen
  Z  Einheit, deren «Nr. im PDF» auf ihrer Seite an keinem Zeilenanfang steht -> evtl. erfunden
Aufruf: python -I verdacht.py <cache> <ordner> <stichproben_ordner> <aus.csv>"""
import collections, csv, glob, json, os, re, sys
import openpyxl

cache, o, stp, aus = sys.argv[1:5]
geprueft = set()
for f in glob.glob(f"{stp}/funde*.csv") + glob.glob(f"{stp}/zusatzfunde*.csv"):
    for r in csv.DictReader(open(f, encoding="utf-8"), delimiter=";"):
        geprueft.add(r["pdf"].replace(".pdf", ""))


def zahl(s):
    m = re.match(r"\s*(\d+)", str(s or ""))
    return int(m.group(1)) if m else 0


def norm(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


zeilen = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    wb = openpyxl.load_workbook(p, read_only=True)
    voll = {}
    for x in wb["Vollständigkeit"].iter_rows(values_only=True):
        if x and x[0] and str(x[0]) not in voll:
            voll[str(x[0])] = x[1] if x[1] is not None else (x[2] if len(x) > 2 else None)
    sig_vor = str(voll.get("Signaturen nur im Vorspann") or "–")
    vor = zahl(voll.get("Vorspann (nicht importiert)"))
    schl = zahl(voll.get("Schlussvermerke"))
    nicht = zahl(voll.get("Nicht übernommen"))
    m = re.search(r"\(([\d.]+)%\)", str(voll.get("davon im Import gefunden") or ""))
    proz = float(m.group(1)) if m else 100.0
    signale = []
    if vor >= 25 and sig_vor not in ("–", "", "None"):
        signale.append(f"V: Vorspann {vor} Zeilen, Signaturen nur im Vorspann: {sig_vor[:80]}")
    if schl >= 20:
        signale.append(f"S: {schl} Schlussvermerk-Zeilen")
    if nicht >= 10:
        signale.append(f"N: {nicht} Zeilen nicht übernommen")
    if proz < 100:
        signale.append(f"W: Text erfasst {proz} %")
    try:
        zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
        seiten = collections.defaultdict(list)
        for z in zz:
            seiten[z["seite"]].append(norm(" ".join(w[0] for w in z["worte"][:4])))
        rows = list(wb["scope-Import"].iter_rows(values_only=True))
        h = rows[0]
        ohne = []
        for r in rows[1:]:
            if not r or r[0] is None:
                continue
            e = dict(zip(h, r))
            nr = norm(e["Nr. im PDF"])
            if nr and not any(t.startswith(nr) for t in seiten.get(e["PDF-Seite"], [])):
                ohne.append(str(e["Signatur"]))
        if ohne:
            signale.append(f"Z: {len(ohne)} Einheiten ohne Zeilenanfang im PDF, z. B. {', '.join(ohne[:3])}")
    except FileNotFoundError:
        pass
    for s in signale:
        zeilen.append({"datei": d, "geprueft": "ja" if d in geprueft else "nein", "signal": s[0], "befund": s})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "geprueft", "signal", "befund"], delimiter=";")
    w.writeheader()
    w.writerows(zeilen)
c = collections.Counter((z["signal"], z["geprueft"]) for z in zeilen)
print("Signale (Signal, schon geprüft):", dict(sorted(c.items())))
print("Dateien mit Signal:", len({z["datei"] for z in zeilen}), "davon nie geprüft:", len({z["datei"] for z in zeilen if z["geprueft"] == "nein"}))
