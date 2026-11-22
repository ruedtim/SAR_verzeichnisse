"""Nachprüfung 11 zusammenführen: Urteile N1, Funde N1 + E1–E10 (+ S), Dateiurteile, offen_kritisch.csv mit stabilen
K-Nummern (behobene Zeilen fallen weg, neue kritische Zeilen bekommen die nächsten freien Nummern).
Aufruf: python -I zusammen11.py <pakete> <offen_kritisch_alt.csv> <aus_ordner>"""
import collections, csv, glob, math, re, sys

pakete, ok_alt, aus = sys.argv[1:4]
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"))
F = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist", "muster", "paket", "k_alt",
     "entscheid"]

# Entscheide der Prüfsession nach Gegenprüfung (werden nach Rückkehr der Pakete gefüllt)
HERAB = {        # (paket, B-Nr.) -> Grund (kritischer Teil behoben, Rest mittel)
    ("N2", "B5"): "K7: alle 25 Unternummern A.1–Q.1 sind Einheiten; Rest nicht kritisch (mittel)",
    ("N2", "B6"): "K10: Schachtel 5/6 wie Soll; Rest nicht kritisch (mittel)",
    ("N2", "B17"): "K23: IV.2a/IV.2b sind Einheiten unter IV.2.; Rest nicht kritisch (mittel)",
    ("N1", "B6"): "K15: Mindest-Soll aus NP10 erfüllt (Anhang ganz im Blatt Info, 30. leer, 32. Einheit); die Regesten «in 17.6.»/«in 18.» zusätzlich ins Darin dieser Einheiten wäre besser (mittel)",
}
HERAB_NEU = {    # (paket, pdf, Signaturanfang) -> Grund (Fund nur mittel)
    ("E2", "D2516.pdf", "V.L.103."): "Nummern im Fliesstext ohne Signaturspalte; ob Einheiten, ist eine Konventionsfrage (mittel, unsicher)",
    ("N2", "D3767.pdf", "VII.437.:37."): "die Beilagen gehören zum Album 37. (richtige Einheit); nur Hinweis/Darin-Form (mittel, wie NP10)",
    ("N2", "D3271.pdf", "VII.24.:4.2.9."): "Grenzfall: Registerzeile im Titel von 4.2.9. (mittel)",
}
KONVENTION = [  # (pdf, Signaturanfang) -> Konventionsentscheid «Stück ohne Nummer» (Regel 50)
    ("D149825.pdf", "(ohne Nummer"), ("D3943.pdf", "X.G.219."), ("D260.pdf", "V.A.c.23.:120"), ("D3277.pdf", "VII.242.:10 (ID 10); erwartet"),
    ("D3557.pdf", "VII.336.:4.4."), ("D1726.pdf", "V.G.b.903."), ("D3826.pdf", "VII.75.:20."),
]
KTEXT = "Konventionsentscheid «Stück ohne Nummer» (Regel 50) offen: eigene Einheit, Darin einer Bestandszeile oder Darin der Nachbareinheit; Prüfsession: Darin einer fremden Einheit ist Inhalt bei falscher Einheit"
ENTFAELLT = {    # (paket, pdf, Signaturanfang) -> Grund (kein Fehler mehr / doppelt)
    ("N1", "D3472.pdf", "VII.308.F.a.:1967.18"): "am Stand bb4c9588 behoben (Nachtrag 2: eigene Einheit 1969.18 mit Hinweis); = K28",
}
BEWUSST_NEU = {   # (pdf) -> Grund
    "D3190.pdf": "bewusst offen laut AENDERUNGEN_RUNDE7 (Übersichtszeile 9. als Einheit)",
    "D3894.pdf": "bewusst offen laut AENDERUNGEN_RUNDE7 (Abschnitte und Siegel mit gleicher Nummer)",
}

bk = {}       # (Paket, B-Nr.) -> K-Nr.
bquelle = {}  # (Paket, B-Nr.) -> Schlüssel des E-Fundes, den die Altzeile nachprüft
for p in glob.glob(f"{pakete}/N*_altzeilen.csv"):
    pk = re.search(r"/(N\d)_altzeilen", p).group(1)
    for r in lies(p):
        bk[(pk, r["nr"])] = r["k_nr"]
        if not r["k_nr"] and r["quelle"].startswith("NP11 E"):
            bquelle[(pk, r["nr"])] = (r["pdf"].replace(".pdf", ""), r["signatur"], r["soll"][:60])

urteile = collections.Counter()
for p in sorted(glob.glob(f"{pakete}/N*_urteile.csv")):
    for r in lies(p):
        t = (r.get("urteil") or "").strip().lower()
        k = "besser" if t.startswith("besser") else "schlechter" if t.startswith("schlechter") else "gleich" if t.startswith("gleich") else t[:20]
        try:
            nn = int(str(r.get("n") or 1).strip() or 1)
        except ValueError:
            nn = 1
        urteile[k] += nn

funde = []
for p in sorted(glob.glob(f"{pakete}/[NES]*_funde.csv")):
    pk = re.search(r"/([NES]\d*)_funde", p).group(1)
    for r in lies(p):
        b = r.get("bemerkung") or ""
        m = re.match(r"\s*\[(B\d+)\]", b)
        r["paket"] = pk
        r["k_alt"] = bk.get((pk, m.group(1)), "") if m else ""
        r["prueft_e"] = bquelle.get((pk, m.group(1))) if m else None
        r["status"] = (r.get("status") or "").strip().lower()
        r["schwere"] = (r.get("schwere") or "").strip().lower()
        r["entscheid"] = ""
        key = (pk, m.group(1)) if m else None
        if key in HERAB and r["schwere"] == "kritisch":
            r["schwere"] = "mittel"; r["entscheid"] = HERAB[key]
        for (q, pdf, sig), grund in HERAB_NEU.items():
            if q == pk and r["pdf"] == pdf and r["signatur"].startswith(sig) and r["schwere"] == "kritisch":
                r["schwere"] = "mittel"; r["entscheid"] = grund
        for (q, pdf, sig), grund in ENTFAELLT.items():
            if q == pk and r["pdf"] == pdf and r["signatur"].startswith(sig):
                r["status"] = "entfällt"; r["entscheid"] = grund
        funde.append(r)
for r in funde:
    pdfn = r["pdf"] if r["pdf"].endswith(".pdf") else r["pdf"] + ".pdf"
    if r["schwere"] == "kritisch" and any(pdfn == q and r["signatur"].startswith(sig) for q, sig in KONVENTION):
        r["entscheid"] = ((r.get("entscheid") or "") + " " + KTEXT).strip()
ersetzt = {}
for r in funde:
    if r.get("prueft_e"):
        ersetzt[r["prueft_e"]] = r
for r in funde:
    if r["paket"].startswith("E"):
        k = (r["pdf"].replace(".pdf", ""), r["signatur"], r["soll"][:60])
        if k in ersetzt:
            n2 = ersetzt[k]
            r["entscheid"] = (r.get("entscheid") or "") + f" Nachgeprüft in {n2['paket']} am Stand bb4c9588: {n2['status']}"
            r["status"] = "ersetzt"
            if n2["status"] in ("neu", "offen", "teilweise", "schlechter") and n2["schwere"] == "kritisch":
                n2["status"] = "neu"; n2["prueft_e"] = None  # bleibt als neue kritische Zeile (aus N2)
with open(f"{aus}/funde_nachpruefung11.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=F, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(funde)

du = []
for p in sorted(glob.glob(f"{pakete}/[EN]*_dateien_urteil.csv")):
    pk = re.search(r"/([EN]\d+)_dateien_urteil", p).group(1)
    for r in lies(p):
        r["paket"] = pk
        du.append(r)
krit = {r["pdf"].replace(".pdf", "") for r in funde if r["schwere"] == "kritisch" and r["status"] in ("neu", "offen", "teilweise", "schlechter")}
for r in du:
    r["urteil_jetzt"] = "kritisch" if r["datei"] in krit else "ohne kritischen Fehler"
with open(f"{aus}/dateien_urteil11.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "paket", "einheiten", "umfang_geprueft", "kritisch", "mittel", "gering", "urteil",
                                      "urteil_jetzt", "signale", "bemerkung"], delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(du)

# offen_kritisch mit stabilen Nummern
alt = lies(ok_alt)
felder = list(alt[0].keys())
pruef = {}
for r in funde:
    if r["k_alt"]:
        pruef[r["k_alt"]] = r
neu, weg = [], []
for a in alt:
    k = a["nr"]
    if k in pruef:
        r = pruef[k]
        if r["status"] in ("behoben", "entfällt") or r["schwere"] != "kritisch":
            weg.append((k, a["datei"], r["status"], r["schwere"]))
            continue
        a = dict(a, befund_jetzt=r.get("neu_ist") or r.get("ist"), status=r["status"], in_arbeit_hauptsession="",
                 paket=r["paket"], entscheid=(r.get("entscheid") or "") + " NP11: in der Gegenprüfung noch kritisch")
    neu.append(a)
nr = max(int(a["nr"][1:]) for a in alt)
for r in funde:
    if r["k_alt"] or r["schwere"] != "kritisch" or r["status"] not in ("neu", "offen", "teilweise", "schlechter"):
        continue
    if re.match(r"\s*\[B\d+\]", r.get("bemerkung") or "") and not (r["paket"] == "N2" and r["status"] == "neu"):
        continue
    nr += 1
    m = re.search(r"Ursache:\s*([^.;]+)", r.get("bemerkung") or "")
    pdfn = r["pdf"] if r["pdf"].endswith(".pdf") else r["pdf"] + ".pdf"
    bo = BEWUSST_NEU.get(pdfn, "")
    neu.append({"nr": f"K{nr}", "datei": r["pdf"].replace(".pdf", ""), "signatur_id": r["signatur"], "seite": r["seite"], "feld": r["feld"],
                "befund_jetzt": r.get("neu_ist") or r.get("ist"), "soll": r["soll"], "ursache": m.group(1).strip() if m else "",
                "status": r["status"], "erstmeldung": "NP11", "bewusst_offen": "ja" if bo else "", "in_arbeit_hauptsession": "", "k_alt": "",
                "paket": r["paket"], "muster": r.get("muster", ""), "entscheid": " ".join(x for x in (r.get("entscheid", ""), bo) if x),
                "bemerkung": r.get("bemerkung", "")})
with open(f"{aus}/offen_kritisch.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(neu)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


e_du = [r for r in du if r["paket"].startswith("E")]
k_e = sum(1 for r in e_du if r["urteil_jetzt"] == "kritisch")
print("Urteile N1:", dict(urteile))
print("Funde:", len(funde), collections.Counter((r["status"], r["schwere"]) for r in funde).most_common())
print("K-Prüfung:", {k: (pruef[k]["status"], pruef[k]["schwere"]) for k in sorted(pruef, key=lambda x: int(x[1:]))})
print("weg (behoben):", weg)
lo, hi = wilson(k_e, len(e_du))
print(f"E-Pakete: {len(e_du)} Dateien, {k_e} kritisch ({k_e / max(1, len(e_du)):.0%}, KI {lo:.0%}–{hi:.0%})")
print("offen_kritisch:", len(neu), "Zeilen in", len({z['datei'] for z in neu}), "Dateien; neu NP11:",
      sum(1 for z in neu if z["erstmeldung"] == "NP11"), "; bewusst offen:", sum(1 for z in neu if z["bewusst_offen"] == "ja"),
      "; in Arbeit:", sum(1 for z in neu if z["in_arbeit_hauptsession"]),
      "; Muster neu:", collections.Counter(z["muster"] for z in neu if z["erstmeldung"] == "NP11").most_common())
