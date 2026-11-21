"""Sechste Nachprüfung: Ergebnisse zusammenführen -> stichproben/funde_nachpruefung6.csv (+ Zählungen als JSON).

Quellen: methode/np6_pruefliste.csv (Auswahl), roh/np6_vorbewertet.csv (automatisch: PDF seit 13:15 inhaltlich
unverändert -> vorheriger Status bleibt, «neu» wird «offen»), roh/np6_gruppe_N.csv (Prüfagenten und Hauptprüfung,
inkl. neuer Fehler), roh/np6_d151210_Dn.csv (Vollprüfung D151210, nur neue Fehler), roh/np6_*_regeln.csv
(Regelstichprobe: geprüfte Einheiten mit Urteil).
Spalten wie funde_nachpruefung5.csv. Bedeutung hier: «ist» = Stand 13:15 (= neu_ist der fünften Nachprüfung bzw. bei
neuen Fehlern der Stand 13:15), «neu_ist» = Stand 15:43 mit Fundstelle. pdf/seite/signatur/feld/schwere/soll/bemerkung
der Paketzeilen unverändert aus funde_nachpruefung5.csv.
Regelurteile: doppelte Urteile derselben Einheit (gleiche Regel, gleiches PDF, gleiche Signatur und ID) zählen einmal.
Aufruf: python3 -I np6_zusammenfuehren.py [ZAEHLUNG.json]
"""
import csv, os, re, sys, json, glob, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
SPALTEN = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung"]
GUELTIG = {"behoben", "teilweise", "offen", "schlechter", "entfällt"}
BUCHST = "ABCDEFGHIJKLMNOP"


def lies(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def hm(text):
    m = re.match(r"\s*\[(M\d\d)", text or "")
    return m.group(1) if m else "M19"


def regel(text):
    """Vermutliche Ursache aus «Regel: …» in der Bemerkung: Buchstabe(n) A–P («A/B» bleibt «A/B»), «vor 13:15»,
    «nicht angekündigt»; sonst «unklar»."""
    m = re.search(r"Regel:\s*([^;)\]]+)", text or "")
    if not m:
        return "unklar"
    r = m.group(1).strip()
    rl = r.lower()
    if rl.startswith("vor 13") or rl.startswith("vor 15") or rl.startswith("vor 11") or "greift nicht" in rl:
        return "vor 13:15"  # («O (greift nicht) / vor 13:15»: alter Fehler, den die Regel nicht behebt)
    if rl.startswith("nicht angek") or rl.startswith("unklar") or rl.startswith("unangek"):
        return "nicht angekündigt"
    m2 = re.match(rf"([{BUCHST}](?:\s*[/,+]\s*[{BUCHST}])*)(?![A-Za-zäöü])", r.upper() if len(r) <= 3 or re.match(r"[a-pA-P](?:\W|$)", r) else r)
    if m2:
        return re.sub(r"\s+", "", m2.group(1)).replace(",", "/").replace("+", "/")
    return "unklar"


# Bereinigung doppelt gemeldeter neuer Fehler (dieselbe Einheit von mehreren Gruppen): jede Einheit zählt einmal.
# (Gruppendatei, PDF, Anfang der Signatur) -> Grund; die behaltene Zeile bekommt einen Vermerk (VERMERK).
WEG = {
    ("np6_gruppe_0.csv", "D1739.pdf", "V.G.c.105.:27", ""): "in der B-Sammelzeile von Gruppe 2",
    ("np6_gruppe_6.csv", "D2620.pdf", "V.L.167.:10.2.", ""): "dieselbe Einheit wie Gruppe 2 (Regel D)",
    ("np6_gruppe_6.csv", "D3363.pdf", "VII.272.:2.2.18.", ""): "in der B-Sammelzeile von Gruppe 2",
    ("np6_gruppe_6.csv", "D176795.pdf", "VII.388.:5.", ""): "in der B-Sammelzeile von Gruppe 2 und der C-Sammelzeile von Gruppe 3",
    ("np6_gruppe_6.csv", "D2940.pdf", "VII.141.:6.", ""): "in der C-Sammelzeile von Gruppe 3",
    ("np6_gruppe_6.csv", "D176151.pdf", "VII.371.:11.1.", ""): "in der C-Sammelzeile von Gruppe 3",
    ("np6_gruppe_6.csv", "D176060.pdf", "VII.423.:7.3.4.", ""): "in der C-Sammelzeile von Gruppe 3",
    ("np6_gruppe_2.csv", "D2534.pdf", "V.L.111.:2.1.", ""): "in der A-Zeile von Gruppe 6 (Jubiläum)",
    ("np6_gruppe_5.csv", "D4054.pdf", "VII.151.:12.4. Teil 2", ""): "dieselben 3 Einheiten wie die B/E-Zeile von Gruppe 2",
    ("np6_gruppe_5.csv", "D4054.pdf", "VII.151.:14.3.3.", "Regel: C"): "in der C-Sammelzeile von Gruppe 3",
    ("np6_gruppe_1.csv", "D3170.pdf", "VII.209.:6.4.", ""): "in der C-Sammelzeile von Gruppe 3",
    ("np6_gruppe_3.csv", "D3077.pdf", "VII.194.:16.", ""): "in der B-Sammelzeile von Gruppe 2",
    ("np6_gruppe_3.csv", "D3063.pdf", "VII.190.:6.2.", ""): "in der F-Sammelzeile von Gruppe 5",
    ("np6_gruppe_3.csv", "D149628.pdf", "VII.12.B.:26.2.4.", ""): "dieselben Einheiten wie die B/E-Zeile von Gruppe 2",
    ("np6_gruppe_3.csv", "D3793.pdf", "VII.55.:5.8.23.", ""): "in der J-Zeile von Gruppe 2",
    ("np6_gruppe_4.csv", "D149628.pdf", "VII.12.B.:26.2.4.", ""): "dieselben Einheiten wie die B/E-Zeile von Gruppe 2",
    ("np6_gruppe_4.csv", "D3793.pdf", "VII.55.:5.8.23.", ""): "in der J-Zeile von Gruppe 2",
    ("np6_gruppe_4.csv", "D9983.pdf", "VII.12.A.:5.8.1.", ""): "in der J-Zeile von Gruppe 2",
    ("np6_gruppe_4.csv", "D150589.pdf", "VII.142.:16.2.10.", ""): "in der A-Zeile von Gruppe 6 (Jubiläum)",
    ("np6_gruppe_4.csv", "D3225.pdf", "VII.227.:9.", ""): "dieselbe Einheit wie die Paketzeile Z323 («schlechter»)",
}
VERMERK = {
    ("np6_gruppe_2.csv", "D1877.pdf", "V.G.c.43.:1.", ""): dict(anhang=(
        " [auch gemeldet: D1739 27 (Gruppe 0), D3077 16. (Gruppe 3), D3363 2.2.18. und D176795 5. (Gruppe 6); D3018 05.2.1., "
        "D3067 V.B. Teil 3 und D175994 IV.A.65. sind zugleich Paketzeilen («schlechter»); D176795 5. steht auch in der "
        "C-Sammelzeile von Gruppe 3]")),
    ("np6_gruppe_2.csv", "D2620.pdf", "V.L.167.:10.2.", ""): dict(anhang=" [auch von Gruppe 6 gemeldet]"),
    ("np6_gruppe_6.csv", "D2534.pdf", "V.L.111.:2.1.", ""): dict(anhang=(
        " [dazu D150589 VII.142.:16.2.10. (ID 1440, Gedenkteller 1959; von Gruppe 2 und 4 gemeldet) – zusammen 4 Fälle]")),
    ("np6_gruppe_2.csv", "D149628.pdf", "VII.12.B.:26.2.4.", ""): dict(anhang=(
        " [auch von Gruppe 3 (Regel E mit I), Gruppe 4 (Regel I) und Gruppe 5 (Regel E, gering) gemeldet]")),
    ("np6_gruppe_3.csv", "D176795.pdf", "VII.388.:5.", ""): dict(anhang=(
        " [auch gemeldet: D2940 6., D176151 11.1., D176060 7.3.4. (Gruppe 6), D4054 14.3.3. (Gruppe 5), D3170 6.4. (Gruppe 1); "
        "D176795 5. steht auch in der B-Sammelzeile von Gruppe 2]")),
    ("np6_gruppe_5.csv", "D3861.pdf", "VII.93.:3.2.1.", ""): dict(anhang=" [D3063 6.2. auch von Gruppe 3 gemeldet]"),
    ("np6_gruppe_2.csv", "D9983.pdf", "VII.12.A.:5.8.1.", ""): dict(anhang=" [auch gemeldet: D3793 5.8.23. von Gruppe 3 (Regel I mit J) und Gruppe 4 (Regel J), D9983 5.8.1. von Gruppe 4]"),
}
# D151210: Teile mit dem Titel des Nachbarteils sind der Rest der Paketzeile Z291 (dort zusammengefasst)
NACHBAR_Z291 = "Art: Titel (Nachbarteil)"
# D151210: Stand der betroffenen Einheiten in der neueren Ausgabe regress92 (16:16) – nur Vergleich, nicht am PDF geprüft
REGRESS = {}
_rp = os.path.join(STP, "roh", "np6_d151210_regress92.txt")
if os.path.exists(_rp):
    for _l in open(_rp, encoding="utf-8"):
        _f = _l.rstrip("\n").split("|")
        if len(_f) >= 6:
            REGRESS[(_f[0], _f[1], _f[2])] = (_f[3], _f[4], _f[5])


def bereinige(gruppe, r):
    """None = Zeile fällt als Dublette weg; sonst die (evtl. ergänzte) Zeile."""
    sig, bem = r.get("signatur", "").strip(), r.get("bemerkung") or ""
    if gruppe.startswith("np6_d151210_") and NACHBAR_Z291 in bem:
        BEREINIGT.append(f"{gruppe}: {r.get('pdf')} {sig[:40]} entfernt – Rest von Z291 (dort zusammengefasst)")
        return None
    for (g, pdf, anfang, teil), grund in WEG.items():
        if g == gruppe and r.get("pdf", "").strip() == pdf and sig.startswith(anfang) and teil in bem:
            BEREINIGT.append(f"{gruppe}: {pdf} {anfang} entfernt – {grund}")
            return None
    for (g, pdf, anfang, teil), v in VERMERK.items():
        if g == gruppe and r.get("pdf", "").strip() == pdf and sig.startswith(anfang) and teil in bem:
            if "signatur" in v:
                r["signatur"] = v["signatur"]
            r["bemerkung"] = bem.rstrip() + v["anhang"]
            BEREINIGT.append(f"{gruppe}: {pdf} {anfang} ergänzt")
    if gruppe.startswith("np6_d151210_"):
        k = (gruppe, (r.get("seite") or ""), sig[:60])
        if k in REGRESS:
            n_ids, geae, felder = REGRESS[k]
            n_g = int(geae.split()[-1]) if geae.split() and geae.split()[-1].isdigit() else -1
            if n_g == 0:
                r["bemerkung"] = (r.get("bemerkung") or "").rstrip() + " [regress92 (16:16): betroffene Einheiten unverändert]"
            elif n_g > 0:
                r["bemerkung"] = (r.get("bemerkung") or "").rstrip() + (
                    f" [regress92 (16:16): {n_g} von {n_ids.split()[-1]} Einheiten geändert ({felder}), nicht am PDF geprüft]")
    return r


BEREINIGT = []
liste = lies(os.path.join(HIER, "np6_pruefliste.csv"))
ergebnis, neu, fehler = {}, [], []
quellen = [os.path.join(STP, "roh", "np6_vorbewertet.csv")] + sorted(
    p for p in glob.glob(os.path.join(STP, "roh", "np6_gruppe_*.csv")) + glob.glob(os.path.join(STP, "roh", "np6_d151210_D?.csv"))
    if not p.endswith("_regeln.csv"))
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

# Auftrag 4: bewusst/bekannt offene Punkte (die 11 aus Runde 5, dazu D1858) – Marke einheitlich vorn in neu_ist
BEWUSST = {"Z3", "Z4", "Z5", "Z6", "Z44", "Z48", "Z50", "Z54", "Z128", "Z134", "Z139", "Z302"}
aus = []
for z in liste:
    e = ergebnis.get(z["nr"])
    if not e:
        continue
    zeile = {k: z[k] for k in SPALTEN}
    zeile["ist"] = z["stand_1315"]
    zeile.update(status=e["status"], neu_ist=(e.get("neu_ist") or "").strip(), _a=z["auswahl"], _m=z["muster"],
                 _v=z["status_vorher"], _q=e["_q"], _nr=z["nr"], _h=z["herkunft"], _g=z["pdf_geaendert"])
    if z["nr"] in BEWUSST and not zeile["neu_ist"].startswith("[bewusst offen]"):
        zeile["neu_ist"] = "[bewusst offen] " + zeile["neu_ist"].replace("[bewusst offen] ", "").replace("[bewusst offen]", "")
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

with open(os.path.join(STP, "funde_nachpruefung6.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=SPALTEN + ["status", "neu_ist"], delimiter=";", extrasaction="ignore")
    w.writeheader()
    for z in aus:
        w.writerow(z)

# Regelstichprobe (doppelte Urteile derselben Einheit nur einmal)
urteile, gesehen, doppelt = [], set(), 0
for p in sorted(glob.glob(os.path.join(STP, "roh", "np6_gruppe_*_regeln.csv")) + glob.glob(os.path.join(STP, "roh", "np6_d151210_D?_regeln.csv"))):
    for r in lies(p):
        r["_q"] = os.path.basename(p)
        rg = (r.get("regel") or "").strip().upper()
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
    bewusst_offen=C(z["status"] for z in aus if z["_nr"] in BEWUSST),
    bewusst_marke=sum(z["neu_ist"].startswith("[bewusst offen]") for z in aus),
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
    d151210_art=C(next((m.group(1).strip() for m in [re.search(r"Art:\s*([^;]+)", z['bemerkung'])] if m), '?') for z in nz if 'D151210-Vollprüfung' in z['bemerkung']),
    d151210_schwere=C(z['schwere'] for z in nz if 'D151210-Vollprüfung' in z['bemerkung']),
    regel_pdfs=C(r["regel"] for r in {(r["regel"], (r.get("pdf") or "").replace(".pdf", "")): r for r in urteile}.values()),
)
text = json.dumps(zaehl, ensure_ascii=False, indent=1)
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(text)
print(text if len(sys.argv) == 1 else f"{len(aus)} Zeilen, {len(fehler)} Probleme: {fehler[:5]}")
