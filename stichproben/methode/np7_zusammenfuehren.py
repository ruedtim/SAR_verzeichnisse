"""Siebte Nachprüfung: Ergebnisse der Prüfer (roh/np7_*.csv) zu stichproben/funde_nachpruefung7.csv zusammenführen und
zählen. Aufruf: python -I np7_zusammenfuehren.py [zaehlung.json]

Reihenfolge: die 76 D151210-Zeilen aus funde_nachpruefung6.csv (#1–#76), dann die Zeilen aus Runde 6 in den übrigen
geänderten Dateien (O1/O2), dann die neuen Zeilen. Spalten wie in funde_nachpruefung6.csv; `ist` = Stand 15:43, `neu_ist`
= Stand 18:11."""
import csv, collections, glob, json, os, re, sys

STP = "/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse/stichproben"
SPALTEN = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist"]
GUELTIG = {"behoben", "teilweise", "offen", "schlechter", "entfällt"}
# doppelt gemeldete neue Zeilen: (Datei, pdf, Signatur-Anfang, Teil der Bemerkung) -> Grund
WEG: dict[tuple, str] = {}
# bewusst offen (Hauptsession), Nummern der D151210-Zeilen in funde_nachpruefung6.csv
BO = {5, 14, 20, 26, 30, 34, 35, 3, 4, 7, 11, 18, 21, 25, 37, 56, 61, 64, 67, 71, 73, 74, 76, 15, 49, 50, 51, 63, 65, 66,
      68, 69, 70, 72}


def lies(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


f6 = lies(os.path.join(STP, "funde_nachpruefung6.csv"))
d_nr, k = {}, 0
for i, r in enumerate(f6, 1):
    if r["pdf"] == "D151210.pdf":
        k += 1
        d_nr[i] = k
fehler, bereinigt = [], []
ergebnis, neu = {}, []
quellen = sorted(glob.glob(os.path.join(STP, "roh", "np7_d151210_D?.csv")) + glob.glob(os.path.join(STP, "roh", "np7_O?.csv"))
                 + glob.glob(os.path.join(STP, "roh", "np7_gruppe_0.csv")))
for p in quellen:
    g = os.path.basename(p)
    for r in lies(p):
        nr = (r.get("nr") or "").strip()
        st = (r.get("status") or "").strip().lower().replace("entfaellt", "entfällt")
        if nr in ("", "neu") or st == "neu":
            sig, bem = (r.get("signatur") or "").strip(), r.get("bemerkung") or ""
            grund = next((v for (gg, pdf, anf, teil), v in WEG.items() if gg == g and (r.get("pdf") or "").strip() == pdf
                          and sig.startswith(anf) and teil in bem), None)
            if grund:
                bereinigt.append(f"{g}: {r.get('pdf')} {sig[:40]} entfernt – {grund}")
                continue
            r["status"], r["_q"] = "neu", g
            neu.append(r)
            continue
        m = re.match(r"[ZN](\d+)$", nr)
        if not m:
            fehler.append(f"{g}: unbekannte nr {nr!r}")
            continue
        i = int(m.group(1))
        if st not in GUELTIG:
            fehler.append(f"{g}: {nr} ungültiger Status {r.get('status')!r}")
        if i in ergebnis:
            fehler.append(f"{g}: {nr} doppelt (auch in {ergebnis[i]['_q']})")
        r["status"], r["_q"] = st, g
        ergebnis[i] = r

# erwartete Zeilen: alle D151210-Zeilen und die Paketzeilen O1/O2
erwartet = set(d_nr)
for p in glob.glob("/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/"
                   "8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/np7/pakete/O?_funde6.csv"):
    erwartet |= {int(r["nr"][1:]) for r in lies(p)}
fehlend = sorted(erwartet - set(ergebnis))
if fehlend:
    fehler.append(f"fehlende Zeilen ({len(fehlend)}): {fehlend[:30]}")

aus = []
for i in sorted(erwartet & set(ergebnis), key=lambda i: (f6[i - 1]["pdf"] != "D151210.pdf", i)):
    z, e = f6[i - 1], ergebnis[i]
    zeile = {k: z[k] for k in SPALTEN[:6]}
    zeile["ist"] = z["neu_ist"]
    vor = f"#{d_nr[i]}; " if i in d_nr else ""
    zeile["bemerkung"] = vor + z["bemerkung"]
    ni = (e.get("neu_ist") or "").strip()
    if i in d_nr and d_nr[i] in BO and not ni.startswith("[bewusst offen (Hauptsession)]"):
        ni = "[bewusst offen (Hauptsession)] " + ni
    zeile.update(status=e["status"], neu_ist=ni, _q=e["_q"], _nr=f"#{d_nr[i]}" if i in d_nr else f"Z{i}",
                 _v=z["status"], _bo=i in d_nr and d_nr[i] in BO)
    aus.append(zeile)
for r in sorted(neu, key=lambda r: (r.get("pdf", ""), r.get("seite", ""))):
    zeile = {k: (r.get(k) or "").strip() for k in SPALTEN}
    if zeile["pdf"] and not zeile["pdf"].endswith(".pdf"):
        zeile["pdf"] += ".pdf"
    if zeile["schwere"] not in ("kritisch", "mittel", "gering"):
        fehler.append(f"{r['_q']}: neue Zeile {zeile['pdf']} {zeile['signatur'][:30]} Schwere {zeile['schwere']!r}")
    zeile.update(status="neu", _q=r["_q"], _nr="neu", _v="", _bo=False)
    aus.append(zeile)
with open(os.path.join(STP, "funde_nachpruefung7.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=SPALTEN, delimiter=";", extrasaction="ignore")
    w.writeheader()
    w.writerows(aus)


def ursache(b):
    m = re.search(r"Ursache:\s*([^;]+)", b)
    return m.group(1).strip() if m else "?"


def art(b):
    m = re.search(r"Art:\s*([^;]+)", b)
    return m.group(1).strip() if m else "?"


urteile = []
for p in sorted(glob.glob(os.path.join(STP, "roh", "np7_*_urteile.csv"))):
    for r in lies(p):
        r["_q"] = os.path.basename(p)
        urteile.append(r)
C = collections.Counter
alt = [z for z in aus if z["_nr"] != "neu"]
nz = [z for z in aus if z["_nr"] == "neu"]
zaehl = dict(
    fehler=fehler, bereinigt=bereinigt, zeilen=len(aus), alt=len(alt), neu=len(nz),
    d151210_status=C(z["status"] for z in alt if z["pdf"] == "D151210.pdf"),
    d151210_status_schwere=C(f"{z['schwere']}|{z['status']}" for z in alt if z["pdf"] == "D151210.pdf"),
    d151210_status_vorher=C(f"{z['_v']}|{z['status']}" for z in alt if z["pdf"] == "D151210.pdf"),
    d151210_bewusst_offen=C(z["status"] for z in alt if z["_bo"]),
    andere_status=C(z["status"] for z in alt if z["pdf"] != "D151210.pdf"),
    andere_status_vorher=C(f"{z['_v']}|{z['status']}" for z in alt if z["pdf"] != "D151210.pdf"),
    neu_gruppe=C(z["_q"] for z in nz),
    neu_schwere=C(z["schwere"] for z in nz),
    neu_d151210=C(z["schwere"] for z in nz if z["pdf"] == "D151210.pdf"),
    neu_ursache=C(ursache(z["bemerkung"]) for z in nz),
    neu_ursache_schwere=C(f"{ursache(z['bemerkung'])}|{z['schwere']}" for z in nz),
    neu_art_d151210=C(art(z["bemerkung"]) for z in nz if z["pdf"] == "D151210.pdf"),
    neu_pdf=C(z["pdf"] for z in nz),
    urteile=len(urteile),
    urteile_gruppe=C(f"{r['_q']}|{(r.get('urteil') or '').strip().lower()}" for r in urteile),
    urteile_gesamt=C((r.get("urteil") or "").strip().lower() for r in urteile),
    urteile_ursache=C(f"{(r.get('ursache') or '').strip()}|{(r.get('urteil') or '').strip().lower()}" for r in urteile),
    urteile_d151210=C((r.get("urteil") or "").strip().lower() for r in urteile if (r.get("pdf") or "").startswith("D151210")),
    urteile_andere=C((r.get("urteil") or "").strip().lower() for r in urteile if not (r.get("pdf") or "").startswith("D151210")),
)
text = json.dumps(zaehl, ensure_ascii=False, indent=1)
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(text)
print(text if len(sys.argv) == 1 else f"{len(aus)} Zeilen, {len(fehler)} Probleme: {fehler[:5]}")
