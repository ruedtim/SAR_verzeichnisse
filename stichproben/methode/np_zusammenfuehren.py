"""Nachprüfung: Ergebnisse der Prüfgruppen (roh/np_gruppe_*.csv) zusammenführen.

Schreibt stichproben/funde_nachpruefung.csv (Spalten wie funde.csv plus status, neu_ist) und gibt
Zählungen für nachpruefung.md aus (als JSON nach stdout bzw. Datei, wenn ein Pfad angegeben ist).
Die ersten acht Spalten der Paketzeilen kommen unverändert aus funde.csv bzw. zusatzfunde_gesamtscan.csv,
damit sich die Zeilen mit diesen Dateien verbinden lassen.
Aufruf: python3 -I np_zusammenfuehren.py [ZAEHLUNG.json]
"""
import csv, os, re, sys, json, collections, glob

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
SPALTEN = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung"]
STATUS_ALT = {"behoben", "teilweise", "offen", "entfällt"}


def lies(pfad):
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def hm(text):
    m = re.match(r"\s*\[(M\d\d)\]", text or "")
    return m.group(1) if m else "M19"


liste = lies(os.path.join(HIER, "np_pruefliste.csv"))
quelle = {}
for i, r in enumerate(lies(os.path.join(STP, "funde.csv")), 1):
    quelle[f"F{i}"] = r
for i, r in enumerate(lies(os.path.join(STP, "zusatzfunde_gesamtscan.csv")), 1):
    quelle[f"Z{i}"] = r

ergebnis, neu, fehler = {}, [], []
for pfad in sorted(glob.glob(os.path.join(STP, "roh", "np_gruppe_*.csv"))):
    g = os.path.basename(pfad)
    for r in lies(pfad):
        nr = (r.get("nr") or "").strip()
        st = (r.get("status") or "").strip().lower().replace("entfaellt", "entfällt")
        if nr in ("", "neu") or st == "neu":
            if st != "neu":
                fehler.append(f"{g}: neue Zeile ohne Status neu: {r}")
            r["status"] = "neu"
            r["_gruppe"] = g
            neu.append(r)
            continue
        if st not in STATUS_ALT:
            fehler.append(f"{g}: {nr} ungültiger Status {r.get('status')!r}")
        if nr in ergebnis:
            fehler.append(f"{g}: {nr} doppelt (auch in {ergebnis[nr]['_gruppe']})")
        r["status"] = st
        r["_gruppe"] = g
        ergebnis[nr] = r

fehlend = [z["nr"] for z in liste if z["nr"] not in ergebnis]
fremd = [nr for nr in ergebnis if nr not in {z["nr"] for z in liste}]
if fehlend:
    fehler.append(f"fehlende Paketzeilen: {len(fehlend)}: {fehlend[:20]}")
if fremd:
    fehler.append(f"unbekannte nr: {fremd[:20]}")

aus = []
for z in liste:
    e = ergebnis.get(z["nr"])
    if not e:
        continue
    q = quelle[z["nr"]]
    zeile = {k: q[k] for k in SPALTEN}
    zeile["status"] = e["status"]
    zeile["neu_ist"] = (e.get("neu_ist") or "").strip()
    zeile["_auswahl"] = z["auswahl"].split(" (")[0]
    zeile["_muster"] = z["muster"]
    zeile["_nr"] = z["nr"]
    aus.append(zeile)
for r in sorted(neu, key=lambda r: (r.get("pdf", ""), r.get("seite", ""))):
    zeile = {k: (r.get(k) or "").strip() for k in SPALTEN}
    zeile["status"] = "neu"
    zeile["neu_ist"] = (r.get("neu_ist") or "").strip()
    zeile["_auswahl"] = "neu"
    zeile["_muster"] = hm(zeile["bemerkung"])
    zeile["_nr"] = "neu"
    aus.append(zeile)

with open(os.path.join(STP, "funde_nachpruefung.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=SPALTEN + ["status", "neu_ist"], delimiter=";", extrasaction="ignore")
    w.writeheader()
    for z in aus:
        w.writerow(z)

zaehl = {
    "fehler": fehler,
    "zeilen": len(aus),
    "auswahl_status": collections.Counter(f"{z['_auswahl']}|{z['status']}" for z in aus),
    "muster_status": collections.Counter(f"{z['_muster']}|{z['status']}" for z in aus),
    "pdf_status": collections.Counter(f"{z['pdf']}|{z['status']}" for z in aus),
    "neu_schwere": collections.Counter(z["schwere"] for z in aus if z["status"] == "neu"),
    "neu_muster": collections.Counter(f"{z['_muster']}|{z['schwere']}" for z in aus if z["status"] == "neu"),
    "krit_muster_status": collections.Counter(f"{z['_muster']}|{z['status']}" for z in aus if z["_auswahl"] == "kritisch"),
}
text = json.dumps(zaehl, ensure_ascii=False, indent=1)
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(text)
print(text if len(sys.argv) == 1 else f"{len(aus)} Zeilen, {len(fehler)} Probleme: {fehler[:5]}")
