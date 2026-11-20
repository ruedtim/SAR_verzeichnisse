"""Vierte Nachprüfung: Ergebnisse zusammenführen -> stichproben/funde_nachpruefung4.csv (+ Zählungen als JSON).

Quellen: methode/np4_pruefliste.csv (Auswahl), roh/np4_vorbewertet.csv (automatisch: PDF seit 08:25 inhaltlich
unverändert -> vorheriger Status bleibt, «neu» wird «offen»), roh/np4_gruppe_N.csv (Prüfagenten und Hauptprüfung,
inkl. neuer Fehler), roh/np4_gruppe_N_regeln.csv (Regelstichprobe: geprüfte Einheiten mit Urteil).
Spalten wie funde_nachpruefung3.csv. Bedeutung hier: «ist» = Stand 08:25 (= neu_ist der dritten Nachprüfung bzw. bei
neuen Fehlern der Stand 08:25), «neu_ist» = Stand 11:30 mit Fundstelle. pdf/seite/signatur/feld/schwere/soll/bemerkung
der Paketzeilen unverändert aus funde_nachpruefung3.csv.
Aufruf: python3 -I np4_zusammenfuehren.py [ZAEHLUNG.json]
"""
import csv, os, re, sys, json, glob, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
SPALTEN = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung"]
GUELTIG = {"behoben", "teilweise", "offen", "schlechter", "entfällt"}
REGELN = ("vor 08:25", "a", "b", "c", "d", "e", "f", "g", "h", "unklar")


def lies(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def hm(text):
    m = re.match(r"\s*\[(M\d\d)", text or "")
    return m.group(1) if m else "M19"


def regel(text):
    """Vermutliche Ursache aus «Regel: …» in der Bemerkung (erste genannte Regel; «a/g» -> «a/g»)."""
    m = re.search(r"Regel:\s*([^;)\]]+)", text or "")
    if not m:
        return "unklar"
    r = m.group(1).strip().lower()
    if r.startswith("vor 08"):
        return "vor 08:25"
    m2 = re.match(r"([a-h](?:\s*/\s*[a-h])*)\b", r)
    if m2:
        return re.sub(r"\s+", "", m2.group(1))
    return "unklar"


liste = lies(os.path.join(HIER, "np4_pruefliste.csv"))
ergebnis, neu, fehler = {}, [], []
quellen = [os.path.join(STP, "roh", "np4_vorbewertet.csv")] + sorted(
    p for p in glob.glob(os.path.join(STP, "roh", "np4_gruppe_*.csv")) if not p.endswith("_regeln.csv"))
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
    zeile["ist"] = z["stand_0825"]
    zeile.update(status=e["status"], neu_ist=(e.get("neu_ist") or "").strip(), _a=z["auswahl"], _m=z["muster"],
                 _v=z["status_vorher"], _q=e["_q"], _nr=z["nr"], _h=z["herkunft"], _g=z["pdf_geaendert"])
    aus.append(zeile)
for r in sorted(neu, key=lambda r: (r.get("pdf", ""), r.get("seite", ""))):
    zeile = {k: (r.get(k) or "").strip() for k in SPALTEN}
    if ";" in zeile["pdf"]:  # Sammelzeile über mehrere PDFs: erstes PDF in die Spalte, die übrigen in die Bemerkung
        teile = [t.strip() for t in zeile["pdf"].split(";") if t.strip()]
        zeile["pdf"] = teile[0]
        zeile["bemerkung"] += f" (betrifft auch {', '.join(teile[1:])})"
    zeile.update(status="neu", neu_ist=(r.get("neu_ist") or "").strip(), _a="neu", _m=hm(zeile["bemerkung"]), _v="",
                 _q=r["_q"], _nr="neu", _h="neu", _g="ja")
    aus.append(zeile)

with open(os.path.join(STP, "funde_nachpruefung4.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=SPALTEN + ["status", "neu_ist"], delimiter=";", extrasaction="ignore")
    w.writeheader()
    for z in aus:
        w.writerow(z)

# Regelstichprobe
urteile = []
for p in sorted(glob.glob(os.path.join(STP, "roh", "np4_gruppe_*_regeln.csv"))):
    for r in lies(p):
        r["_q"] = os.path.basename(p)
        urteile.append(r)

C = collections.Counter
nz = [z for z in aus if z["status"] == "neu"]
zaehl = dict(
    fehler=fehler, zeilen=len(aus),
    auswahl_status=C(f"{z['_a']}|{z['status']}" for z in aus),
    auswahl_schwere_status=C(f"{z['_a']}|{z['schwere']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    schwere_status=C(f"{z['schwere']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    herkunft_status=C(f"{z['_h']}|{z['schwere']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    vorher_status=C(f"{z['_v']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    bewusst_offen=C(z["status"] for z in aus if z["neu_ist"].startswith("[bewusst offen]")),
    muster_status=C(f"{z['_m']}|{z['status']}" for z in aus),
    pdf_status=C(f"{z['pdf']}|{z['status']}" for z in aus),
    neu_schwere=C(z["schwere"] for z in nz),
    neu_regel=C(regel(z["bemerkung"]) for z in nz),
    neu_regel_schwere=C(f"{regel(z['bemerkung'])}|{z['schwere']}" for z in nz),
    neu_herkunft=C(next((h for h in ("Gesamtvergleich", "Regelstichprobe", "Nachprüfung") if h in z["bemerkung"]), "?")
                   for z in nz),
    quelle=C(z["_q"] for z in aus),
    regel_urteile=C(f"{(r.get('regel') or '').strip()}|{(r.get('urteil') or '').strip().lower()}" for r in urteile),
    regel_urteile_gesamt=C((r.get("urteil") or "").strip().lower() for r in urteile),
    regel_pdfs=C((r.get("regel") or "").strip() for r in {(r.get("regel"), r.get("pdf")): r for r in urteile}.values()),
)
text = json.dumps(zaehl, ensure_ascii=False, indent=1)
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(text)
print(text if len(sys.argv) == 1 else f"{len(aus)} Zeilen, {len(fehler)} Probleme: {fehler[:5]}")
