"""Nachprüfung 12 zusammenführen: Urteile G1–G3, Funde G1–G3 + P1–P7 + L1–L2 (+ S), Dateiurteile, offen_kritisch.csv mit stabilen
K-Nummern (behobene Zeilen fallen weg, neue kritische Zeilen bekommen die nächsten freien Nummern).
Aufruf: python -I zusammen12.py <pakete> <offen_kritisch_alt.csv> <aus_ordner>"""
import collections, csv, glob, math, re, sys

pakete, ok_alt, aus = sys.argv[1:4]
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"))
F = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist", "muster", "paket", "k_alt",
     "entscheid"]

# Entscheide der Prüfsession nach Gegenprüfung (werden nach Rückkehr der Pakete gefüllt)
HERAB = {
    ("G2", "B55"): "K67: Einheiten wie Soll; Rest Zeitraum (mittel)",
    ("G2", "B58"): "K72: 26 Einheiten wie Soll; Rest nur der Bearbeitungsvermerk «KOMMENTAR FEHLT NOCH», kein Archivinhalt (mittel)",
    ("G2", "B60"): "K74: Einheiten wie Soll; Rest Titel (mittel)",
    ("G2", "B68"): "K101: 14 Einheiten wie Soll; Rest Titel (mittel)",
    ("G1", "B3"): "K63: Bereichsköpfe wie angekündigt; Rest Beschreibung nur bei der ersten Einheit des Bereichs, in AENDERUNGEN_RUNDE9 als offen genannt (mittel)",
    ("G3", "B91"): "K85: Gliederung wie Soll (a/b unter «Allgemeines»); Rest Signaturform «:a.»/«:b.» statt «:1.a.»/«:1.b.» (mittel)",
}
HERAB_NEU = {
    ("P7", "D3951.pdf", "X.T.2.:8"): "nur das Wort «(Band)» aus einer als Kopf verworfenen Zeile fehlt (mittel; Regelfrage Tabellenkopf)",
    ("P5", "D3657.pdf", ""): "NP6 hatte «Teil 2» für die doppelten 5./6. als Soll zugelassen (mittel)",
    ("P3", "D9978.pdf", "VII.12.B.:28.1., :28.2."): "Eltern 28. steht in einer anderen Datei (D149628); innerhalb der Datei nicht lösbar, Hinweis «erwartet 28.» genügt (mittel)",
    ("P4", "D9985.pdf", "VII.12.B.:27.2.1."): "Eltern 27.2. steht in einer anderen Datei (D149628); innerhalb der Datei nicht lösbar (mittel)",
    ("P4", "D3271.pdf", "VII.24.:4.2.9."): "Grenzfall: Registerzeile im Titel von 4.2.9. (mittel, wie NP11)",
    ("P4", "D140969.pdf", "VII.80.:87."): "PDF widersprüchlich (Übersicht «82 – 87», Detailkopf «82 – 86»); mittel wie NP10",
    ("P2", "D152390.pdf", "V.J.W.b.53.:6"): "ein Überleitungssatz, kein Textverlust (mittel)",
    ("G3", "D4058.pdf", "VII.151.:19.1.–19.13."): "Eltern VII.151.:19. steht im Hauptverzeichnis D4054; innerhalb der Datei nicht lösbar, jede Einheit hat den Hinweis «erwartet 19.» (mittel, wie D9978/D9985)",
    ("P2", "D150296.pdf", "VII.298.:6.8."): "wiederholte Signatur = Teil nach Konvention; keine Nummer fehlt, also kein Tippfehler-Fall wie K80 (mittel)",
}
KONVENTION = []
KTEXT = "Konventionsentscheid «Stück ohne Nummer» (Regel 50) offen: eigene Einheit, Darin einer Bestandszeile oder Darin der Nachbareinheit; Prüfsession: Darin einer fremden Einheit ist Inhalt bei falscher Einheit"
ENTFAELLT = {
    ("P3", "D3208.pdf", "VII.222.:2 (ID 2)"): "= K42 (bewusst offen, Abzeichensammlung); wird dort weitergeführt",
}
BEWUSST_NEU = {   # (pdf) -> Grund; gilt für neue kritische Zeilen dieser Datei
    "D1874.pdf": "bewusst offen laut AENDERUNGEN_RUNDE7 («Bewusst offen»: Code «-» Planmappe nicht mehr vorhanden fällt als Aufzählungszeichen weg)",
}
KONVFRAGE = [  # (pdf, Signaturanfang) -> offene Konventionsfrage, bleibt kritisch
    ("D3774.pdf", "VII.47. (Bestandszeile fehlt)"), ("D2894.pdf", "VII.122. (Bestandszeile fehlt)"),
    ("D3828.pdf", ""),
]
KONVFRAGE.append(("D3271.pdf", "VII.24.:4.2.22."))
NOTIZ = {  # (Paket, pdf, Signaturanfang) -> Begründung, Schwere bleibt
    ("G1", "D2710.pdf", "V.L.5.:1 Teil 2"): "Konventionsfrage: In Findmitteln ohne Signaturen beginnt die Schachtelzählung neu (Jahresdokumentation); die zweite Folge sind andere Behälter, nicht Teile der ersten. Bis zum Entscheid kritisch",
    ("L2", "D151150.pdf", "V.F.c.150.:9."): "Nach Muster 8 der NP11 (Nr.-Spalte über Schachteln = Signaturen, Regel 14, wie D1391 K101) kritisch; NP5/NP6 hatten nur den Zeitraum beanstandet",
    ("L2", "D175996.pdf", "IV.B.1.a)"): "Wie D3816 K79 und D9983: «n.a)» neben «n.» in derselben Spalte, mit eigenem Gegenstand und Umfang, ist Geschwister; Regel 25 verlangt heute gleichen Titel",
}
KFTEXT = "Konventionsfrage: Gilt Regel 31 (Stück ohne Nummer → Bestandszeile) auch für Stücke mit Behälter, die nur im Vorspann oder in der Übersicht stehen? Bis zum Entscheid kritisch"

bk = {}       # (Paket, B-Nr.) -> K-Nr.
bquelle = {}  # (Paket, B-Nr.) -> Schlüssel des E-Fundes, den die Altzeile nachprüft
for p in glob.glob(f"{pakete}/G*_altzeilen.csv"):
    pk = re.search(r"/(G\d)_altzeilen", p).group(1)
    for r in lies(p):
        bk[(pk, r["nr"])] = r["k_nr"]
        if not r["k_nr"] and r["quelle"].startswith("NP11 E"):
            bquelle[(pk, r["nr"])] = (r["pdf"].replace(".pdf", ""), r["signatur"], r["soll"][:60])

urteile = collections.Counter()
for p in sorted(glob.glob(f"{pakete}/G*_urteile.csv")):
    for r in lies(p):
        t = (r.get("urteil") or "").strip().lower()
        k = ("besser" if t.startswith("besser") else "schlechter" if t.startswith("schlechter") else "gleich" if t.startswith("gleich")
             else "teilweise besser" if t.startswith("teilweise") else t[:20])
        try:
            nn = int(str(r.get("n") or 1).strip() or 1)
        except ValueError:
            nn = 1
        urteile[k] += nn

funde = []
for p in sorted(glob.glob(f"{pakete}/[GPLRS]*_funde.csv")):
    pk = re.search(r"/([GPLRS]\d*)_funde", p).group(1)
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
    if r["schwere"] == "kritisch" and pdfn in BEWUSST_NEU and r["status"] == "neu":
        r["entscheid"] = ((r.get("entscheid") or "") + " " + BEWUSST_NEU[pdfn]).strip()
    if r["schwere"] == "kritisch" and pdfn == "D3271.pdf" and r["signatur"].startswith("VII.24.:4.2.22."):
        r["entscheid"] = "Grenzfall: Die K8-Konvention (Gruppenzeile als Hinweis bei der folgenden Einheit) deckt nur die Überschrift; die Beschreibung darunter steht in keinem importierten Feld. Bis zum Entscheid kritisch"
    elif r["schwere"] == "kritisch" and any(pdfn == q and r["signatur"].startswith(sig) for q, sig in KONVFRAGE):
        r["entscheid"] = ((r.get("entscheid") or "") + " " + KFTEXT).strip()
    if r["schwere"] == "kritisch" and any(pdfn == q and r["signatur"].startswith(sig) for q, sig in KONVENTION):
        r["entscheid"] = ((r.get("entscheid") or "") + " " + KTEXT).strip()
for r in funde:
    for (q, pdf, sig), grund in NOTIZ.items():
        if q == r["paket"] and r["pdf"] == pdf and r["signatur"].startswith(sig) and r["schwere"] == "kritisch":
            r["entscheid"] = ((r.get("entscheid") or "") + " " + grund).strip()
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
with open(f"{aus}/funde_nachpruefung12.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=F, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(funde)

du = []
for p in sorted(glob.glob(f"{pakete}/[GPLR]*_dateien_urteil.csv")):
    pk = re.search(r"/([GPLR]\d+)_dateien_urteil", p).group(1)
    for r in lies(p):
        r["paket"] = pk
        du.append(r)
krit = {r["pdf"].replace(".pdf", "") for r in funde if r["schwere"] == "kritisch"
        and (r["status"] in ("neu", "offen", "teilweise", "schlechter") or r["status"].startswith("bekannt"))}
for r in du:
    r["urteil_jetzt"] = "kritisch" if r["datei"] in krit else "ohne kritischen Fehler"
with open(f"{aus}/dateien_urteil12.csv", "w", encoding="utf-8", newline="") as f:
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
bekannt = collections.defaultdict(list)   # K-Nr. -> Pakete, die eine bekannte offene Zeile wiedergefunden haben
for r in funde:
    m = re.match(r"bekannt\s*\((k\d+)\)", r["status"])
    if m and r["schwere"] == "kritisch":
        bekannt[m.group(1).upper()].append(r["paket"])
for a in alt:
    k = a["nr"]
    if k in bekannt and k not in pruef:
        a = dict(a, entscheid=((a.get("entscheid") or "") + f" NP12: im Durchgang ({', '.join(sorted(set(bekannt[k])))}) noch kritisch").strip())
    if k in pruef:
        r = pruef[k]
        if r["status"] in ("behoben", "entfällt") or r["schwere"] != "kritisch":
            weg.append((k, a["datei"], r["status"], r["schwere"]))
            continue
        a = dict(a, befund_jetzt=r.get("neu_ist") or r.get("ist"), status=r["status"], in_arbeit_hauptsession="",
                 paket=r["paket"], entscheid=(r.get("entscheid") or "") + " NP12: in der Gegenprüfung noch kritisch")
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
                "status": r["status"], "erstmeldung": "NP12", "bewusst_offen": "ja" if bo else "", "in_arbeit_hauptsession": "", "k_alt": "",
                "paket": r["paket"], "muster": r.get("muster", ""), "entscheid": " ".join(x for x in (r.get("entscheid", ""), "" if bo in (r.get("entscheid") or "") else bo) if x),
                "bemerkung": r.get("bemerkung", "")})
with open(f"{aus}/offen_kritisch.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(neu)

# Dateiurteil endgültig: kritisch, wenn die Datei eine neue/offene kritische Zeile hat oder in offen_kritisch steht (z. B. K42 bewusst offen)
okdat = {z["datei"] for z in neu}
for r in du:
    r["urteil_jetzt"] = "kritisch" if (r["datei"] in krit or r["datei"] in okdat) else "ohne kritischen Fehler"
with open(f"{aus}/dateien_urteil12.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "paket", "einheiten", "umfang_geprueft", "kritisch", "mittel", "gering", "urteil",
                                      "urteil_jetzt", "signale", "bemerkung"], delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(du)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


e_du = [r for r in du if r["paket"][0] in "PLG"]
k_e = sum(1 for r in e_du if r["urteil_jetzt"] == "kritisch")
print("Urteile G:", dict(urteile))
print("Funde:", len(funde), collections.Counter((r["status"], r["schwere"]) for r in funde).most_common())
print("K-Prüfung:", {k: (pruef[k]["status"], pruef[k]["schwere"]) for k in sorted(pruef, key=lambda x: int(x[1:]))})
print("weg (behoben):", weg)
lo, hi = wilson(k_e, len(e_du))
print(f"Durchgang (P, L, G-Vollprüfung): {len(e_du)} Dateien, {k_e} kritisch ({k_e / max(1, len(e_du)):.0%}, KI {lo:.0%}–{hi:.0%})")
print("offen_kritisch:", len(neu), "Zeilen in", len({z['datei'] for z in neu}), "Dateien; neu NP12:",
      sum(1 for z in neu if z["erstmeldung"] == "NP12"), "; bewusst offen:", sum(1 for z in neu if z["bewusst_offen"] == "ja"),
      "; in Arbeit:", sum(1 for z in neu if z["in_arbeit_hauptsession"]),
      "; Muster neu:", collections.Counter(z["muster"] for z in neu if z["erstmeldung"] == "NP12").most_common())
