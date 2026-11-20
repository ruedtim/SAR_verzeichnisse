"""Fünfte Nachprüfung: Ergebnisse zusammenführen -> stichproben/funde_nachpruefung5.csv (+ Zählungen als JSON).

Quellen: methode/np5_pruefliste.csv (Auswahl), roh/np5_vorbewertet.csv (automatisch: PDF seit 11:30 inhaltlich
unverändert -> vorheriger Status bleibt, «neu» wird «offen»), roh/np5_gruppe_N.csv (Prüfagenten und Hauptprüfung,
inkl. neuer Fehler), roh/np5_gruppe_N_regeln.csv (Regelstichprobe: geprüfte Einheiten mit Urteil).
Spalten wie funde_nachpruefung4.csv. Bedeutung hier: «ist» = Stand 11:30 (= neu_ist der vierten Nachprüfung bzw. bei
neuen Fehlern der Stand 11:30), «neu_ist» = Stand 13:15 mit Fundstelle. pdf/seite/signatur/feld/schwere/soll/bemerkung
der Paketzeilen unverändert aus funde_nachpruefung4.csv.
Regelurteile: doppelte Urteile derselben Einheit (gleiche Regel, gleiches PDF, gleiche Signatur und ID) zählen einmal.
Aufruf: python3 -I np5_zusammenfuehren.py [ZAEHLUNG.json]
"""
import csv, os, re, sys, json, glob, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
SPALTEN = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung"]
GUELTIG = {"behoben", "teilweise", "offen", "schlechter", "entfällt"}
BUCHST = "abcdefghijklmnopqrstu"


def lies(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def hm(text):
    m = re.match(r"\s*\[(M\d\d)", text or "")
    return m.group(1) if m else "M19"


def regel(text):
    """Vermutliche Ursache aus «Regel: …» in der Bemerkung: Buchstabe(n) a–u («a/b» bleibt «a/b»), «vor 11:30»,
    «nicht angekündigt»; sonst «unklar»."""
    m = re.search(r"Regel:\s*([^;)\]]+)", text or "")
    if not m:
        return "unklar"
    r = m.group(1).strip().lower()
    if r.startswith("vor 11") or r.startswith("vor 13"):
        return "vor 11:30"
    if r.startswith("nicht angek") or r.startswith("unklar") or r.startswith("unangek"):
        return "nicht angekündigt"
    m2 = re.match(rf"([{BUCHST}](?:\s*[/,+]\s*[{BUCHST}])*)(?![a-zäöü])", r)
    if m2:
        return re.sub(r"\s+", "", m2.group(1)).replace(",", "/").replace("+", "/")
    return "unklar"


# Bereinigung doppelt gemeldeter neuer Fehler (dieselbe Einheit von mehreren Gruppen): jede Einheit zählt einmal.
# (Gruppendatei, PDF, Anfang der Signatur) -> Grund; die behaltene Zeile bekommt einen Vermerk (VERMERK).
WEG = {
    ("np5_gruppe_3.csv", "D1180.pdf", "V.E.c.53.:20. (ID 194); D176367"):
        "dieselben Fälle wie Gruppe 5 (D1180 20.) und Gruppe 6 (D176367 7.1., D3313 4.)",
    ("np5_gruppe_3.csv", "D10675.pdf", "V.F.c.28.:700.5"): "dieselben Einheiten wie Gruppe 2 (Regel u)",
    ("np5_gruppe_3.csv", "D3647.pdf", "VII.381.:5.4."): "dieselbe Einheit wie Gruppe 5",
    ("np5_gruppe_6.csv", "D3647.pdf", "VII.381.:5.4."): "dieselbe Einheit wie Gruppe 5",
    ("np5_gruppe_5.csv", "D2141.pdf", "V.H.c.53."): "in der Sammelzeile von Gruppe 3 (D2141, D3087, D2960)",
}
VERMERK = {
    ("np5_gruppe_3.csv", "D867.pdf", "V.C.c.81.:8."): dict(
        signatur="V.C.c.81.:8. (ID 8), :32. (ID 32), :41. (ID 41); D2894 VII.122.:3.1. (ID 11); D149888 VII.159.:1.2.1. (ID 7)",
        anhang=" [Bereinigung: D3429 1.2., D3063 3.4., D3718 4.2.15./4.2.19., D1746 XIV. und D3077 17. sind eigene Zeilen von "
               "Gruppe 6 – hier noch 5 Fälle in 3 PDFs]"),
    ("np5_gruppe_5.csv", "D1180.pdf", "V.E.c.53.:20."): dict(
        anhang=" [Bereinigung: D9983 3.3.4. ist eigene Zeile von Gruppe 1, hier 1 Fall; gleiches Muster D176367 7.1. und "
               "D3313 4. (Gruppe 6); auch von Gruppe 3 gemeldet]"),
    ("np5_gruppe_3.csv", "D2141.pdf", "V.H.c.53."): dict(
        anhang=" [auch von Gruppe 5 gemeldet: deshalb bleibt die Jahresangabe zusätzlich im Titel]"),
    ("np5_gruppe_2.csv", "D10675.pdf", "V.F.c.28.:700.5"): dict(anhang=" [auch von Gruppe 3 gemeldet]"),
    ("np5_gruppe_5.csv", "D3647.pdf", "VII.381.:5.4."): dict(
        anhang=" [auch von Gruppe 6 (Regel k) und Gruppe 3 (dort Regel i) gemeldet]"),
}


def bereinige(gruppe, r):
    """None = Zeile fällt als Dublette weg; sonst die (evtl. ergänzte) Zeile."""
    for (g, pdf, anfang), grund in WEG.items():
        if g == gruppe and r.get("pdf", "").strip() == pdf and r.get("signatur", "").strip().startswith(anfang):
            BEREINIGT.append(f"{gruppe}: {pdf} {anfang} entfernt – {grund}")
            return None
    for (g, pdf, anfang), v in VERMERK.items():
        if g == gruppe and r.get("pdf", "").strip() == pdf and r.get("signatur", "").strip().startswith(anfang):
            if "signatur" in v:
                r["signatur"] = v["signatur"]
            r["bemerkung"] = (r.get("bemerkung") or "").rstrip() + v["anhang"]
            BEREINIGT.append(f"{gruppe}: {pdf} {anfang} ergänzt")
    return r


BEREINIGT = []
liste = lies(os.path.join(HIER, "np5_pruefliste.csv"))
ergebnis, neu, fehler = {}, [], []
quellen = [os.path.join(STP, "roh", "np5_vorbewertet.csv")] + sorted(
    p for p in glob.glob(os.path.join(STP, "roh", "np5_gruppe_*.csv")) if not p.endswith("_regeln.csv"))
for p in quellen:
    g = os.path.basename(p)
    for r in lies(p):
        nr = (r.get("nr") or "").strip()
        st = (r.get("status") or "").strip().lower().replace("entfaellt", "entfällt")
        if nr in ("", "neu") or st == "neu":
            r = bereinige(g, r)
            if r is None:
                continue
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
    zeile["ist"] = z["stand_1130"]
    zeile.update(status=e["status"], neu_ist=(e.get("neu_ist") or "").strip(), _a=z["auswahl"], _m=z["muster"],
                 _v=z["status_vorher"], _q=e["_q"], _nr=z["nr"], _h=z["herkunft"], _g=z["pdf_geaendert"])
    aus.append(zeile)
for r in sorted(neu, key=lambda r: (r.get("pdf", ""), r.get("seite", ""))):
    zeile = {k: (r.get(k) or "").strip() for k in SPALTEN}
    if ";" in zeile["pdf"] or "," in zeile["pdf"]:  # Sammelzeile über mehrere PDFs: erstes PDF in die Spalte, Rest in die Bemerkung
        teile = [t.strip() for t in re.split(r"[;,]", zeile["pdf"]) if t.strip()]
        zeile["pdf"] = teile[0]
        zeile["bemerkung"] += f" (betrifft auch {', '.join(teile[1:])})"
    if zeile["pdf"] and not zeile["pdf"].endswith(".pdf"):
        zeile["pdf"] += ".pdf"
    if not zeile["schwere"] in ("kritisch", "mittel", "gering"):
        fehler.append(f"{r['_q']}: neue Zeile {zeile['pdf']} {zeile['signatur'][:30]} Schwere {zeile['schwere']!r}")
    zeile.update(status="neu", neu_ist=(r.get("neu_ist") or "").strip(), _a="neu", _m=hm(zeile["bemerkung"]), _v="",
                 _q=r["_q"], _nr="neu", _h="neu", _g="ja")
    aus.append(zeile)

with open(os.path.join(STP, "funde_nachpruefung5.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=SPALTEN + ["status", "neu_ist"], delimiter=";", extrasaction="ignore")
    w.writeheader()
    for z in aus:
        w.writerow(z)

# Regelstichprobe (doppelte Urteile derselben Einheit nur einmal)
urteile, gesehen, doppelt = [], set(), 0
for p in sorted(glob.glob(os.path.join(STP, "roh", "np5_gruppe_*_regeln.csv"))):
    for r in lies(p):
        r["_q"] = os.path.basename(p)
        rg = (r.get("regel") or "").strip().lower()
        r["regel"] = rg
        k = (rg, (r.get("pdf") or "").strip().replace(".pdf", ""), (r.get("signatur") or "").strip(), (r.get("id") or "").strip())
        if k in gesehen and k[3]:
            doppelt += 1
            continue
        gesehen.add(k)
        urteile.append(r)

C = collections.Counter
nz = [z for z in aus if z["status"] == "neu"]
fehlend_weg = [k for k in WEG if not any(b.startswith(f"{k[0]}: {k[1]} {k[2]} entfernt") for b in BEREINIGT)]
fehlend_verm = [k for k in VERMERK if not any(b.startswith(f"{k[0]}: {k[1]} {k[2]} ergänzt") for b in BEREINIGT)]
if fehlend_weg or fehlend_verm:
    fehler.append(f"Bereinigung nicht angewendet: {fehlend_weg + fehlend_verm}")
zaehl = dict(
    fehler=fehler, bereinigt=BEREINIGT, zeilen=len(aus), urteile=len(urteile), urteile_doppelt=doppelt,
    auswahl_status=C(f"{z['_a']}|{z['status']}" for z in aus),
    auswahl_schwere_status=C(f"{z['_a']}|{z['schwere']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    schwere_status=C(f"{z['schwere']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    herkunft_status=C(f"{z['_h']}|{z['schwere']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    vorher_status=C(f"{z['_v']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    vorher_schwere_status=C(f"{z['_v']}|{z['schwere']}|{z['status']}" for z in aus if z["_a"] != "neu"),
    bewusst_offen=C(z["status"] for z in aus if z["neu_ist"].startswith("[bewusst offen]")),
    muster_status=C(f"{z['_m']}|{z['status']}" for z in aus),
    pdf_status=C(f"{z['pdf']}|{z['status']}" for z in aus),
    neu_schwere=C(z["schwere"] for z in nz),
    neu_regel=C(regel(z["bemerkung"]) for z in nz),
    neu_regel_schwere=C(f"{regel(z['bemerkung'])}|{z['schwere']}" for z in nz),
    neu_herkunft=C(next((h for h in ("Gesamtvergleich", "Regelstichprobe", "Nachprüfung") if h in z["bemerkung"]), "?")
                   for z in nz),
    quelle=C(z["_q"] for z in aus),
    regel_urteile=C(f"{r['regel']}|{(r.get('urteil') or '').strip().lower()}" for r in urteile),
    regel_urteile_gesamt=C((r.get("urteil") or "").strip().lower() for r in urteile),
    regel_pdfs=C(r["regel"] for r in {(r["regel"], (r.get("pdf") or "").replace(".pdf", "")): r for r in urteile}.values()),
)
text = json.dumps(zaehl, ensure_ascii=False, indent=1)
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(text)
print(text if len(sys.argv) == 1 else f"{len(aus)} Zeilen, {len(fehler)} Probleme: {fehler[:5]}")
