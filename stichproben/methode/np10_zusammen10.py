"""Nachprüfung 10 zusammenführen: Urteile zählen, Funde zu funde_nachpruefung10.csv, Dateiurteile der Stichprobe,
neue offen_kritisch.csv (offene kritische Fehler am Stand 7fa7e161).
Aufruf: python -I zusammen10.py <pakete> <offen_kritisch_alt.csv> <stichprobe10.csv> <aus_ordner>"""
import collections, csv, glob, math, os, re, sys

pakete, ok_alt, stp, aus = sys.argv[1:5]
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"))
F = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist", "muster", "paket", "k_alt", "entscheid", "in_arbeit"]

# Altzeilen: B-Nummer -> K-Nummer
bk = {}
for p in glob.glob(f"{pakete}/A*_altzeilen.csv"):
    for r in lies(p):
        bk[r["nr"]] = r["k_nr"]

# Urteile
urteile = []
for p in sorted(glob.glob(f"{pakete}/A*_urteile.csv")):
    pk = re.search(r"(A\d)_urteile", p).group(1)
    for r in lies(p):
        r["paket"] = pk
        try:
            r["n"] = int(str(r.get("n") or 1).strip() or 1)
        except ValueError:
            r["n"] = 1
        urteile.append(r)
u = collections.Counter()
for r in urteile:
    t = (r.get("urteil") or "").strip().lower()
    k = "besser" if t.startswith("besser") else "schlechter" if t.startswith("schlechter") else "gemischt" if t.startswith("teils") else "gleich" if t.startswith("gleich") else "ohne kritischen fehler" if t.startswith("ohne") else t[:20]
    r["urteil_kat"] = k
    u[(r["paket"], k)] += r["n"]

# Funde
funde = []
for p in sorted(glob.glob(f"{pakete}/[ACS]*_funde.csv")):
    pk = re.search(r"/([ACS]\d?)_funde", p).group(1)
    for r in lies(p):
        b = r.get("bemerkung") or ""
        m = re.match(r"\s*\[(B\d+)\]", b)
        r["paket"] = pk
        r["k_alt"] = bk.get(m.group(1), "") if m else ""
        r["status"] = (r.get("status") or "").strip().lower()
        r["schwere"] = (r.get("schwere") or "").strip().lower()
        funde.append(r)

# Entscheide der Nachprüfung (Gegenprüfung am PDF durch die Prüfsession)
HERAB = {  # (paket, B-Nr.) -> Grund: kritischer Teil behoben, Rest mittel
    ("A2", "B23"): "K4: kritischer Teil behoben; Rest «Cakeplatte» als eigener neuer Fund",
    ("A4", "B52"): "kritischer Teil behoben, Rest Zeitraum 65 (mittel)",
    ("A4", "B53"): "K27: kritischer Teil behoben, Rest Zeitraum 55/56 aus Namen (mittel)",
    ("A4", "B61"): "K19: kritischer Teil behoben, Rest Schachtel von 1.2. (mittel)",
    ("A4", "B62"): "K21: kritischer Teil behoben, Rest Titel/Zeitraum 50a. (mittel)",
    ("A4", "B63"): "K22: kritischer Teil behoben, Rest Titel/Zeitraum 88. (mittel)",
    ("A4", "B66"): "K29: kritischer Teil behoben, Rest Zeitraum 1.2 (mittel)",
}
HERAB_NEU = {  # (paket, pdf, Signaturanfang) -> Grund
    ("A4", "D140969.pdf", "VII.80.:87."): "PDF widersprüchlich (Übersicht «82 – 87», Detailkopf «82 – 86 … später beigefügtes Material»); E1 vertretbar, Hinweis genügt (mittel)",
    ("C1", "D176772.pdf", "VII.192.:2.5."): "Findmittel mehrdeutig (2.5. und 2.6. stehen ohne Inhalt untereinander, dann Schachtel 8); das Skript folgt dem Layout; Hinweis empfohlen (mittel)",
    ("C2", "D175827.pdf", "VII.260.:2.2."): "Detailverzeichnis nennt 2.2. nicht (Aufzählungspunkt unter 2.1.); dem Detailverzeichnis folgen, Hinweis (mittel)",
    ("A2", "D3462.pdf", "VII.307.:1.3."): "nur der Querverweis «vgl. unter 1.8.)» fehlt im Titel (mittel)",
}
BEWUSST = {("A5", "B70"): "K14 bewusst offen (Hauptsession)", ("A2", "B38"): "K28: Runde 8 Regel 5 lässt das Porträt bewusst im Darin von 20.; Entscheid Nutzer"}
IN_ARBEIT = [  # Arbeitskopie der Hauptsession, Nachricht vom 22.11.2026 (nicht im Projekt)
    ("D2960.pdf", ""), ("D2951.pdf", ""), ("D10744.pdf", ""), ("D10675.pdf", ""), ("D434.pdf", ""), ("D3170.pdf", ""),
    ("D3472.pdf", "VII.308.F.a.:1973.9a"),
    ("D3470.pdf", "VII.308.E.a.:12.53a"), ("D3470.pdf", "VII.308.E.a.:1937.524a"), ("D3470.pdf", "VII.308.E.a.:1937.524b"),
    ("D3470.pdf", "VII.308.E.a.:1938.583a"), ("D3470.pdf", "VII.308.E.a.:1938.583b"),
]
for r in funde:
    b = re.match(r"\s*\[(B\d+)\]", r.get("bemerkung") or "")
    key = (r["paket"], b.group(1)) if b else None
    r["entscheid"] = ""
    r["in_arbeit"] = ""
    if key in HERAB and r["schwere"] == "kritisch":
        r["schwere_vorher"] = r["schwere"]; r["schwere"] = "mittel"; r["entscheid"] = HERAB[key]
    for (pk, pdf, sig), grund in HERAB_NEU.items():
        if r["paket"] == pk and r["pdf"] == pdf and r["signatur"].startswith(sig) and r["schwere"] == "kritisch":
            r["schwere_vorher"] = r["schwere"]; r["schwere"] = "mittel"; r["entscheid"] = grund
    if key in BEWUSST:
        r["entscheid"] = BEWUSST[key]; r["bewusst"] = "ja"
    for pdf, sig in IN_ARBEIT:
        if r["pdf"] == pdf and r["signatur"].startswith(sig) and r["schwere"] == "kritisch" and r["status"] == "neu":
            if pdf == "D3472.pdf" and not sig and "1967.18" in r["signatur"]:
                continue
            r["in_arbeit"] = "behoben in der Arbeitskopie der Hauptsession (noch nicht im Projekt)"

# Dubletten (gleiche Datei, Signatur, Feld, Status neu) nur einmal
gesehen, ohne_dub, dub = set(), [], []
for r in funde:
    k = (r["pdf"], re.sub(r"\s+", "", r["signatur"])[:40], r["feld"], r["status"])
    if r["status"] == "neu" and k in gesehen:
        dub.append(r)
        continue
    gesehen.add(k)
    ohne_dub.append(r)
funde = ohne_dub
with open(f"{aus}/funde_nachpruefung10.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=F, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(funde)

# Dateiurteile der Stichprobe
st = {r["datei"]: r for r in lies(stp)}
du = []
for p in sorted(glob.glob(f"{pakete}/[AC]*_dateien_urteil.csv")):
    pk = re.search(r"/([AC]\d)_dateien_urteil", p).group(1)
    for r in lies(p):
        r["paket"] = pk
        r["grund"] = st.get(r["datei"], {}).get("grund", "Runde-8-Datei (Erstprüfung)")
        du.append(r)
with open(f"{aus}/dateien_urteil10.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "paket", "grund", "einheiten", "umfang_geprueft", "kritisch", "mittel", "gering",
                                      "urteil", "signale", "bemerkung"], delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(du)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


krit_dat = {r["pdf"].replace(".pdf", "") for r in funde if r["schwere"] == "kritisch" and r["status"] in ("neu", "offen", "teilweise", "schlechter")}
gr = collections.defaultdict(lambda: [0, 0])
for r in du:
    g = "zufall" if r["grund"].startswith("zufall") else ("verdacht" if r["grund"].startswith("verdacht") else "runde8")
    k = r["datei"] in krit_dat
    gr[g][0] += 1
    gr[g][1] += int(k)

# offen_kritisch neu
alt = lies(ok_alt)
neu = []
erledigt = {}
for r in funde:
    if r["k_alt"]:
        erledigt[r["k_alt"]] = r
for a in alt:
    k = a["nr"]
    if k in erledigt:
        r = erledigt[k]
        if r["status"] in ("behoben", "entfällt") or r["schwere"] != "kritisch":
            continue
        neu.append({"datei": a["datei"], "signatur_id": r["signatur"], "seite": r["seite"], "feld": r["feld"],
                    "befund_jetzt": r.get("neu_ist") or r.get("ist"), "soll": r["soll"], "status": r["status"],
                    "erstmeldung": a["erstmeldung"], "bewusst_offen": "ja" if (a["bewusst_offen"] == "ja" or r.get("bewusst")) else "",
                    "k_alt": k, "paket": r["paket"], "muster": r.get("muster", "") or a.get("muster", ""),
                    "in_arbeit_hauptsession": r.get("in_arbeit", ""), "entscheid": r.get("entscheid", ""), "bemerkung": r.get("bemerkung", "")})
    else:
        neu.append({"datei": a["datei"], "signatur_id": a["signatur_id"], "seite": a["seite"], "feld": a["feld"],
                    "befund_jetzt": "Datei in Runde 8 unverändert: " + (a["befund_jetzt"] or ""), "soll": a["soll"],
                    "status": a["status"], "erstmeldung": a["erstmeldung"], "bewusst_offen": a["bewusst_offen"], "k_alt": k,
                    "paket": "–", "muster": "", "in_arbeit_hauptsession": "", "entscheid": "Datei in Runde 8 unverändert", "bemerkung": a["bemerkung"]})
for r in funde:
    if r["k_alt"] or r["schwere"] != "kritisch" or r["status"] not in ("neu", "offen", "teilweise", "schlechter"):
        continue
    if re.match(r"\s*\[B\d+\]", r.get("bemerkung") or ""):  # Altzeile ohne K-Nummer, aber kritisch offen
        erst = "vor NP10"
    else:
        erst = "NP10"
    m = re.search(r"Ursache:\s*([^.;]+)", r.get("bemerkung") or "")
    neu.append({"datei": r["pdf"].replace(".pdf", ""), "signatur_id": r["signatur"], "seite": r["seite"], "feld": r["feld"],
                "befund_jetzt": r.get("neu_ist") or r.get("ist"), "soll": r["soll"], "ursache": m.group(1).strip() if m else "",
                "status": r["status"], "erstmeldung": erst, "bewusst_offen": "", "k_alt": "", "paket": r["paket"],
                "muster": r.get("muster", ""), "in_arbeit_hauptsession": r.get("in_arbeit", ""), "entscheid": r.get("entscheid", ""),
                "bemerkung": r.get("bemerkung", "")})
neu.sort(key=lambda z: (z.get("in_arbeit_hauptsession", "") != "", z["bewusst_offen"] == "ja", z["k_alt"] == "", z["datei"]))
felder = ["nr", "datei", "signatur_id", "seite", "feld", "befund_jetzt", "soll", "ursache", "status", "erstmeldung",
          "bewusst_offen", "in_arbeit_hauptsession", "k_alt", "paket", "muster", "entscheid", "bemerkung"]
with open(f"{aus}/offen_kritisch.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader()
    for i, z in enumerate(neu, 1):
        w.writerow(dict(z, nr=f"K{i}"))

print("Urteile je Paket:", dict(sorted(u.items())))
print("Funde:", len(funde), "Dubletten entfernt:", len(dub),
      collections.Counter((r["status"], r["schwere"]) for r in funde).most_common())
print("K alt:", {k: (erledigt[k]["status"], erledigt[k]["schwere"]) for k in sorted(erledigt, key=lambda x: int(x[1:]))})
print("Dateiurteile:", len(du), {g: f"{v[1]} von {v[0]} mit kritischem Fehler" for g, v in gr.items()})
if gr["zufall"][0]:
    lo, hi = wilson(gr["zufall"][1], gr["zufall"][0])
    print(f"Zufallsteil: {gr['zufall'][1]}/{gr['zufall'][0]} = {gr['zufall'][1] / gr['zufall'][0]:.0%}, 95%-KI {lo:.0%}–{hi:.0%}")
print("in Arbeit:", sum(1 for z in neu if z.get("in_arbeit_hauptsession")), "| kritische Dateien der Stichprobe:", sorted(d for d in krit_dat if d in st))
print("offen_kritisch:", len(neu), "Zeilen in", len({z['datei'] for z in neu}), "Dateien;",
      sum(1 for z in neu if z["bewusst_offen"] == "ja"), "bewusst offen;", sum(1 for z in neu if z["erstmeldung"] == "NP10"), "neu in NP10;",
      collections.Counter(z["muster"] for z in neu).most_common())
