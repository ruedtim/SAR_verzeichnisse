"""Zweite Nachprüfung: Ergebnisse zusammenführen -> stichproben/funde_nachpruefung2.csv (+ Zählungen als JSON).

Quellen: methode/np2_pruefliste.csv (Auswahl), roh/np2_vorbewertet.csv (automatisch: PDF seit 23:05 unverändert,
auch Prüfhinweise -> vorheriger Status bleibt), roh/np2_gruppe_*.csv (Prüfagenten, inkl. neuer Fehler).
Spalten wie funde_nachpruefung.csv. Bedeutung hier: «ist» = Stand 23:05 (= neu_ist der ersten Nachprüfung bzw. bei
neuen Fehlern der Stand 23:05), «neu_ist» = Stand 00:15 mit Fundstelle. pdf/seite/signatur/feld/schwere/soll/bemerkung
der Paketzeilen unverändert aus funde_nachpruefung.csv.
Aufruf: python3 -I np2_zusammenfuehren.py [ZAEHLUNG.json]
"""
import csv, os, re, sys, json, glob, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
SPALTEN = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung"]
GUELTIG = {"behoben", "teilweise", "offen", "entfällt"}


def lies(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def hm(text):
    m = re.match(r"\s*\[(M\d\d)", text or "")
    return m.group(1) if m else "M19"


liste = lies(os.path.join(HIER, "np2_pruefliste.csv"))
ergebnis, neu, fehler = {}, [], []
quellen = [os.path.join(STP, "roh", "np2_vorbewertet.csv")] + sorted(glob.glob(os.path.join(STP, "roh", "np2_gruppe_*.csv")))
for p in quellen:
    g = os.path.basename(p)
    for r in lies(p):
        nr = (r.get("nr") or "").strip()
        st = (r.get("status") or "").strip().lower().replace("entfaellt", "entfällt")
        if nr in ("", "neu") or st == "neu":
            r["status"], r["_q"] = "neu", g
            neu.append(r)
            continue
        if st not in GUELTIG:
            fehler.append(f"{g}: {nr} ungültiger Status {r.get('status')!r}")
        if nr in ergebnis:
            fehler.append(f"{g}: {nr} doppelt (auch in {ergebnis[nr]['_q']})")
        r["status"], r["_q"] = st, g
        ergebnis[nr] = r
bekannt = {z["nr"] for z in liste}
fehlend = [z["nr"] for z in liste if z["nr"] not in ergebnis]
if fehlend:
    fehler.append(f"fehlende Paketzeilen ({len(fehlend)}): {fehlend[:20]}")
fremd = [n for n in ergebnis if n not in bekannt]
if fremd:
    fehler.append(f"unbekannte nr: {fremd[:20]}")

aus = []
for z in liste:
    e = ergebnis.get(z["nr"])
    if not e:
        continue
    zeile = {k: z[k] for k in SPALTEN}
    zeile["ist"] = z["stand_2305"]
    zeile.update(status=e["status"], neu_ist=(e.get("neu_ist") or "").strip(), _a=z["auswahl"], _m=z["muster"],
                 _v=z["status_vorher"], _q=e["_q"])
    aus.append(zeile)
for r in sorted(neu, key=lambda r: (r.get("pdf", ""), r.get("seite", ""))):
    zeile = {k: (r.get(k) or "").strip() for k in SPALTEN}
    zeile.update(status="neu", neu_ist=(r.get("neu_ist") or "").strip(), _a="neu", _m=hm(zeile["bemerkung"]), _v="",
                 _q=r["_q"])
    aus.append(zeile)

with open(os.path.join(STP, "funde_nachpruefung2.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=SPALTEN + ["status", "neu_ist"], delimiter=";", extrasaction="ignore")
    w.writeheader()
    for z in aus:
        w.writerow(z)

C = collections.Counter
zaehl = dict(
    fehler=fehler, zeilen=len(aus),
    auswahl_status=C(f"{z['_a']}|{z['status']}" for z in aus),
    vorher_status=C(f"{z['_v']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    muster_status=C(f"{z['_m']}|{z['status']}" for z in aus),
    pdf_status=C(f"{z['pdf']}|{z['status']}" for z in aus),
    neu_schwere=C(z["schwere"] for z in aus if z["status"] == "neu"),
    neu_herkunft=C(("Gesamtvergleich" if "Gesamtvergleich" in z["bemerkung"] else "Nachprüfung") for z in aus if z["status"] == "neu"),
    quelle=C(z["_q"] for z in aus),
)
text = json.dumps(zaehl, ensure_ascii=False, indent=1)
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(text)
print(text if len(sys.argv) == 1 else f"{len(aus)} Zeilen, {len(fehler)} Probleme: {fehler[:5]}")
