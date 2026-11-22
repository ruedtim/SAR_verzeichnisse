"""Liste aller offenen kritischen Fehler am Stand e896fb6c aus den Prüferpaketen Q1–Q5 (Status nicht behoben,
Schwere jetzt kritisch) plus eigene Zusatzzeilen. Ergänzt die Runde der Erstmeldung aus den Fundlisten NP1–NP8.
Aufruf: python -I offen_kritisch.py <pakete> <stichproben> <zusatz.csv> <aus.csv>"""
import csv, glob, re, sys

pakete, stp, zusatz, aus = sys.argv[1:5]
IN_ARBEIT = {  # laut Hauptsession (Nachricht vom 22.11.2026) parallel in Arbeit
    "D2850": "55/56", "D140969": "50a/88/89", "D152817": "Abschnitte als Eltern", "D134644": "2.",
    "D845": "1.2", "D151730": "19.5.", "D3826": "20."}


def lies(f):
    return list(csv.DictReader(open(f, encoding="utf-8"), delimiter=";"))


# Erstmeldung: früheste Runde, in der (pdf, feld, soll[:60]) vorkommt
runden = [("NP0", "funde.csv"), ("NP0", "zusatzfunde_gesamtscan.csv"), ("NP1", "funde_nachpruefung.csv")] + \
         [(f"NP{k}", f"funde_nachpruefung{k}.csv") for k in range(2, 9)]
erst = {}
for q, f in runden:
    for r in lies(f"{stp}/{f}"):
        erst.setdefault((r["pdf"], r["feld"], r["soll"][:60]), q)

bnr = {}
for p in glob.glob(f"{pakete}/Q*_altzeilen.csv") + glob.glob(f"{pakete}/Q*_kritisch.csv"):
    for r in lies(p):
        bnr[r["nr"]] = (r["pdf"], r["feld"], r["soll"][:60])
HERAB = {"B8": "mittel"}  # D2850 65.A.: kritischer Teil behoben (Q1), Rest Zeitraum 65
ARBEITSKOPIE = {"D152404": "VIII./VIIIa. behoben in der Arbeitskopie der Hauptsession (noch nicht im Projekt)",
                "D1874": "Reg. unter 1. behoben in der Arbeitskopie der Hauptsession (noch nicht im Projekt)"}
zeilen = []
for p in sorted(glob.glob(f"{pakete}/Q*_funde.csv")):
    paket = re.search(r"(Q\d)_funde", p).group(1)
    for r in lies(p):
        st = (r.get("status") or "").strip().lower()
        sw = (r.get("schwere") or "").strip().lower()
        b = r.get("bemerkung") or ""
        mb = re.match(r"\s*\[(B\d+)\]", b)
        if mb and mb.group(1) in HERAB:
            sw = HERAB[mb.group(1)]
        if st in ("behoben", "ungeprüft", "entfällt") or sw != "kritisch":
            continue
        d = r["pdf"].replace(".pdf", "")
        m = re.search(r"Ursache:\s*([^.;]+(?:\.[^.;]+)?)", b)
        zeilen.append({
            "datei": d, "signatur_id": r["signatur"], "seite": r["seite"], "feld": r["feld"],
            "befund_jetzt": r.get("neu_ist") or r.get("ist") or "", "soll": r["soll"],
            "ursache": (m.group(1).strip() if m else ""), "status": st,
            "erstmeldung": erst.get(bnr.get(mb.group(1)) if mb else (r["pdf"], r["feld"], r["soll"][:60]),
                                    "NP9" if st == "neu" else "?"),
            "bewusst_offen": "ja" if re.search(r"\[bewusst offen|bewusst offen \(hauptsession|bewusst offen laut",
                                               (b + " " + (r.get("neu_ist") or "")).lower()) else "",
            "in_arbeit_hauptsession": ARBEITSKOPIE.get(d) or IN_ARBEIT.get(d, ""), "paket": paket, "bemerkung": b})
for r in lies(zusatz):
    zeilen.append(r)
felder = ["nr", "datei", "signatur_id", "seite", "feld", "befund_jetzt", "soll", "ursache", "status", "erstmeldung",
          "bewusst_offen", "in_arbeit_hauptsession", "paket", "bemerkung"]
zeilen.sort(key=lambda z: (z["in_arbeit_hauptsession"] != "", z["bewusst_offen"] == "ja", z["datei"]))
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader()
    for i, z in enumerate(zeilen, 1):
        w.writerow(dict(z, nr=f"K{i}"))
print(len(zeilen), "offene kritische Zeilen in", len({z["datei"] for z in zeilen}), "Dateien;",
      sum(1 for z in zeilen if z["in_arbeit_hauptsession"]), "in Arbeit,",
      sum(1 for z in zeilen if z["bewusst_offen"] == "ja"), "bewusst offen,",
      sum(1 for z in zeilen if z["status"] == "neu"), "neu")
