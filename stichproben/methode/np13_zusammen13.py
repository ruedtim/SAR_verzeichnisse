"""Nachprüfung 13 zusammenführen: Urteile G1–G5, Funde G1–G5 + Z1–Z3 + S (Prüfsession), Dateiurteile, offen_kritisch.csv mit
stabilen K-Nummern (behobene Zeilen fallen weg, neue kritische Zeilen bekommen die nächsten freien Nummern), Restrate aus der
Zufallsstichprobe.
Aufruf: python -I zusammen13.py <pakete> <offen_kritisch_alt.csv> <aus_ordner>"""
import collections, csv, glob, math, re, sys

pakete, ok_alt, aus = sys.argv[1:4]
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"))
F = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist", "muster", "paket", "k_alt",
     "entscheid"]
N_STRATUM = 642   # Dateien ohne Änderung in Runde 10 und ohne Zeile in offen_kritisch.csv (Grundgesamtheit der Stichprobe)

# Entscheide der Prüfsession nach Rückkehr der Pakete
HERAB = {         # (Paket, B-Nr.) -> Begründung: kritischer Teil behoben, Rest mittel
    ("G5", "B3"): "K121: neun Unternummern als eigene Einheiten wie Soll; Rest Titel der Vollsignatur = Titel der ersten Unternummer, in AENDERUNGEN_RUNDE10 als mittlerer Rest genannt (mittel)",
    ("G5", "B9"): "K163: 57. als Einheit wie Soll; Rest 58. ohne Übersichtstitel, 57. ohne Umfang (gering)",
    ("G4", "B1"): "K99: Notiz und Verweis wie Soll im Blatt Info bzw. Darin; Rest nur mittel (Prüfer G4)",
    ("G1", "B4"): "K100: die drei «Drucksache …»-Zeilen in der Bestandszeile wie Soll; Rest Signatur/Zeitraum (mittel)",
    ("G1", "B5"): "K114: alle vier Inventare im Darin von 3. wie Soll; Rest Zeitraum 1890–1981 aus Lebensdaten, in AENDERUNGEN_RUNDE10 als mittlerer Rest genannt (mittel)",
    ("G2", "B15"): "K161: Anhang S. 26 wie Soll im Blatt Info; Rest Zeitraum von 7. aus einem Literaturzitat (mittel)",
    ("G2", "B10"): "K135: Regel 17 der Runde 10 (Teil mit Hinweis «… zweimal hintereinander mit anderem Titel – Tippfehler? Als Teil übernommen») als Konvention der Hauptsession übernommen. Die Nachbarnummern 7.4.1.25. und 7.4.1.27. sind da, ein Tippfehler ist nicht eindeutig. Eine eigene Einheit nach Entscheid 5 wäre genauer; Konventionsfrage im Bericht (mittel)",
}
HERAB_NEU = {}    # (Paket, pdf, Signaturanfang) -> Begründung: neuer Fund wird mittel
ENTFAELLT = {}    # (Paket, pdf, Signaturanfang) -> Begründung: doppelt zu einer anderen Zeile oder kein Fund
NOTIZ = {         # (Paket, pdf, Signaturanfang) -> Begründung, Schwere bleibt
    ("G3", "D152810.pdf", ""): "Nur Testdaten (D152810 gehört nicht zu den 715 Findmitteln); gleiche Regellücke wie D152817 VI.SB.C.33.a",
    ("G1", "D3808.pdf", ""): "Wie K169 (Bearbeitungs-/Schlussvermerk im Darin einer Einheit) kritisch; anders als K72 ist es ein Schlussvermerk mit Bearbeiterkürzel und Datum",
}
BEWUSST = {}      # (Paket, pdf, Signaturanfang) -> Begründung: neue kritische Zeile ist bewusst offen

bk = {}
for p in glob.glob(f"{pakete}/G*_altzeilen.csv"):
    pk = re.search(r"/(G\d)_altzeilen", p).group(1)
    for r in lies(p):
        bk[(pk, r["nr"])] = r["k_nr"]

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


def passt(tab, r):
    for (q, pdf, sig), grund in tab.items():
        if q == r["paket"] and r["pdf"] == pdf and r["signatur"].startswith(sig):
            return grund
    return None


funde = []
for p in sorted(glob.glob(f"{pakete}/[GZS]*_funde.csv")):
    pk = re.search(r"/([GZS]\d*)_funde", p).group(1)
    for r in lies(p):
        b = r.get("bemerkung") or ""
        m = re.match(r"\s*\[(B\d+)\]", b)
        r["paket"] = pk
        mm = re.match(r"\s*(D\d+)", r["pdf"] or "")
        r["pdf"] = (mm.group(1) if mm else r["pdf"].strip()) + ".pdf"
        r["k_alt"] = bk.get((pk, m.group(1)), "") if m else (r.get("k_nr") or "")
        r["status"] = (r.get("status") or "").strip().lower()
        r["schwere"] = (r.get("schwere") or "").strip().lower()
        r["entscheid"] = ""
        key = (pk, m.group(1)) if m else None
        if key in HERAB and r["schwere"] == "kritisch":
            r["schwere"] = "mittel"; r["entscheid"] = HERAB[key]
        g = passt(HERAB_NEU, r)
        if g and r["schwere"] == "kritisch":
            r["schwere"] = "mittel"; r["entscheid"] = g
        g = passt(ENTFAELLT, r)
        if g:
            r["status"] = "entfällt"; r["entscheid"] = g
        g = passt(NOTIZ, r)
        if g and r["schwere"] == "kritisch":
            r["entscheid"] = ((r["entscheid"] or "") + " " + g).strip()
        g = passt(BEWUSST, r)
        if g and r["schwere"] == "kritisch":
            r["entscheid"] = ((r["entscheid"] or "") + " " + g).strip(); r["bewusst"] = "ja"
        funde.append(r)
with open(f"{aus}/funde_nachpruefung13.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=F, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(funde)

OFFEN = ("neu", "offen", "teilweise", "schlechter")
krit = {r["pdf"].replace(".pdf", "") for r in funde if r["schwere"] == "kritisch" and r["status"] in OFFEN}
du = []
for p in sorted(glob.glob(f"{pakete}/[GZ]*_dateien_urteil.csv")):
    pk = re.search(r"/([GZ]\d+)_dateien_urteil", p).group(1)
    for r in lies(p):
        r["paket"] = pk
        r["datei"] = r["datei"].replace(".pdf", "")
        du.append(r)

# offen_kritisch mit stabilen Nummern
alt = lies(ok_alt)
felder = list(alt[0].keys())
pruef = {r["k_alt"]: r for r in funde if r["k_alt"]}
neu, weg = [], []
for a in alt:
    k = a["nr"]
    if k in pruef:
        r = pruef[k]
        if r["status"] in ("behoben", "entfällt") or r["schwere"] != "kritisch":
            weg.append((k, a["datei"], r["status"], r["schwere"]))
            continue
        a = dict(a, befund_jetzt=r.get("neu_ist") or r.get("ist"), status=r["status"], in_arbeit_hauptsession="",
                 paket=r["paket"], entscheid=((a.get("entscheid") or "") + " " + (r.get("entscheid") or "")
                                              + " NP13: in der Gegenprüfung noch kritisch").strip())
    neu.append(a)
nr = max(int(a["nr"][1:]) for a in alt)
for r in funde:
    if r["k_alt"] or r["schwere"] != "kritisch" or r["status"] not in OFFEN:
        continue
    if re.match(r"\s*\[B\d+\]", r.get("bemerkung") or ""):
        continue
    nr += 1
    m = re.search(r"Ursache:\s*([^.;]+)", r.get("bemerkung") or "")
    neu.append({"nr": f"K{nr}", "datei": r["pdf"].replace(".pdf", ""), "signatur_id": r["signatur"], "seite": r["seite"],
                "feld": r["feld"], "befund_jetzt": r.get("neu_ist") or r.get("ist"), "soll": r["soll"],
                "ursache": m.group(1).strip() if m else "", "status": r["status"], "erstmeldung": "NP13",
                "bewusst_offen": "ja" if r.get("bewusst") else "", "in_arbeit_hauptsession": "", "k_alt": "", "paket": r["paket"],
                "muster": r.get("muster", ""), "entscheid": r.get("entscheid", ""), "bemerkung": r.get("bemerkung", "")})
with open(f"{aus}/offen_kritisch.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(neu)

okdat = {z["datei"] for z in neu}
for r in du:
    r["urteil_jetzt"] = "kritisch" if (r["datei"] in krit or r["datei"] in okdat) else "ohne kritischen Fehler"
with open(f"{aus}/dateien_urteil13.csv", "w", encoding="utf-8", newline="") as f:
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


z_du = [r for r in du if r["paket"].startswith("Z")]
k_z = sum(1 for r in z_du if r["urteil_jetzt"] == "kritisch")
g_du = [r for r in du if r["paket"].startswith("G")]
k_g = sum(1 for r in g_du if r["urteil_jetzt"] == "kritisch")
print("Urteile G:", dict(urteile))
print("Funde:", len(funde), collections.Counter((r["status"], r["schwere"]) for r in funde).most_common())
print("K-Prüfung:", {k: (pruef[k]["status"], pruef[k]["schwere"]) for k in sorted(pruef, key=lambda x: int(x[1:]))})
print("weg (behoben):", len(weg), weg)
lo, hi = wilson(k_z, len(z_du))
print(f"Stichprobe: {len(z_du)} Dateien, {k_z} kritisch ({k_z / max(1, len(z_du)):.0%}, KI {lo:.0%}–{hi:.0%});"
      f" hochgerechnet auf {N_STRATUM} Dateien: {k_z / max(1, len(z_du)) * N_STRATUM:.0f} (KI {lo * N_STRATUM:.0f}–{hi * N_STRATUM:.0f})")
print(f"Gegenprüfung: {len(g_du)} Dateien mit Urteil, {k_g} kritisch")
print("offen_kritisch:", len(neu), "Zeilen in", len(okdat), "Dateien; neu NP13:", sum(1 for z in neu if z["erstmeldung"] == "NP13"),
      "; bewusst offen:", sum(1 for z in neu if z["bewusst_offen"] == "ja"), "; nicht bewusst offen:",
      sum(1 for z in neu if z["bewusst_offen"] != "ja"), "in", len({z["datei"] for z in neu if z["bewusst_offen"] != "ja"}), "Dateien",
      "; Muster neu:", collections.Counter(z["muster"] for z in neu if z["erstmeldung"] == "NP13").most_common())
