"""Nachprüfung 14 zusammenführen: Urteile G1–G2, Funde G1–G2 + Z1–Z3 + ZL1–ZL2 + S1 + S (Prüfsession), Dateiurteile, offen_kritisch.csv mit
stabilen K-Nummern (behobene Zeilen fallen weg, neue kritische Zeilen bekommen die nächsten freien Nummern), Restrate aus der
Zufallsstichprobe.
Aufruf: python -I zusammen14.py <pakete> <offen_kritisch_alt.csv> <aus_ordner>"""
import collections, csv, glob, math, re, sys

pakete, ok_alt, aus = sys.argv[1:4]
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"))
F = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist", "muster", "paket", "k_alt",
     "entscheid"]
N_STRATUM = 628   # Stichprobe 2: ohne Stichprobe 1, ohne Änderung in Runde 11, ohne Zeile in offen_kritisch.csv (Stand NP13)
Z1_NP13 = (4, 60)  # Stichprobe 1 (NP13): 4 von 60 kritisch

# Entscheide der Prüfsession nach Rückkehr der Pakete
HERAB = {}        # (Paket, B-Nr.) -> Begründung: kritischer Teil behoben, Rest mittel
HERAB_NEU = {}    # (Paket, pdf, Signaturanfang) -> Begründung: neuer Fund wird mittel
ENTFAELLT = {}    # (Paket, pdf, Signaturanfang) -> Begründung: doppelt zu einer anderen Zeile oder kein Fund
NOTIZ = {         # (Paket, pdf, Signaturanfang) -> Begründung, Schwere bleibt
    ("S1", "D3099.pdf", ""): "Grenzfall: Der Vermerk steht auf der Höhe der Untereinheiten (x 119, nicht eingerückt wie die Beschreibung von 7.5.1. bei x 167) und nennt auch «Magazin Klus» (7.3.6.); wie K196 der Gruppe zugeordnet",
    ("ZL1", "D151210.pdf", ""): "Grenzfall: eigener Plakat-Eintrag ohne Nummer (kein Abstimmungsplakat), mit dem Abstand eines neuen Eintrags, als letzter Eintrag der Gruppe 13.4; unter 13.5. stehen solche Einträge im Darin der Gruppe. NP6 D4: «fraglich, nicht gemeldet». Ohne diesen Fall wäre die Datei ohne kritischen Fehler",
    ("S1", "D175949.pdf", ""): "Wie K169 (Bearbeitervermerk mit Datum und Name im Darin einer Einheit)",
}
BEWUSST = {}      # (Paket, pdf, Signaturanfang) -> Begründung: neue kritische Zeile ist bewusst offen
ENTFAELLT_K = {   # K-Zeilen ohne Paket, die nach einem Entscheid wegfallen
    k: "Entscheid der Hauptsession (AENDERUNGEN_RUNDE11, Konvention 2): Buchstaben in der Titelspalte mit eigener Schachtel bleiben Einheiten (D3012, D3038, D3089 wie bisher)"
    for k in ("K200", "K201", "K202")}

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
    pk = re.search(r"/([GZS]L?\d*)_funde", p).group(1)
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
with open(f"{aus}/funde_nachpruefung14.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=F, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(funde)

OFFEN = ("neu", "offen", "teilweise", "schlechter")
krit = {r["pdf"].replace(".pdf", "") for r in funde if r["schwere"] == "kritisch" and r["status"] in OFFEN}
du = []
for p in sorted(glob.glob(f"{pakete}/[GZ]*_dateien_urteil.csv")):
    pk = re.search(r"/([GZ]L?\d+)_dateien_urteil", p).group(1)
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
    if k in ENTFAELLT_K:
        weg.append((k, a["datei"], "entfällt", ENTFAELLT_K[k][:40]))
        continue
    if k in pruef:
        r = pruef[k]
        if r["status"] in ("behoben", "entfällt") or r["schwere"] != "kritisch":
            weg.append((k, a["datei"], r["status"], r["schwere"]))
            continue
        a = dict(a, befund_jetzt=r.get("neu_ist") or r.get("ist"), status=r["status"], in_arbeit_hauptsession="",
                 paket=r["paket"], entscheid=((a.get("entscheid") or "") + " " + (r.get("entscheid") or "")
                                              + " NP14: in der Gegenprüfung noch kritisch").strip())
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
                "ursache": m.group(1).strip() if m else "", "status": r["status"], "erstmeldung": "NP14",
                "bewusst_offen": "ja" if r.get("bewusst") else "", "in_arbeit_hauptsession": "", "k_alt": "", "paket": r["paket"],
                "muster": r.get("muster", ""), "entscheid": r.get("entscheid", ""), "bemerkung": r.get("bemerkung", "")})
with open(f"{aus}/offen_kritisch.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(neu)

okdat = {z["datei"] for z in neu}
for r in du:
    r["urteil_jetzt"] = "kritisch" if (r["datei"] in krit or r["datei"] in okdat) else "ohne kritischen Fehler"
with open(f"{aus}/dateien_urteil14.csv", "w", encoding="utf-8", newline="") as f:
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
k1, n1 = Z1_NP13
lo2, hi2 = wilson(k_z + k1, len(z_du) + n1)
print(f"Beide Stichproben zusammen: {k_z + k1} von {len(z_du) + n1} ({(k_z + k1) / (len(z_du) + n1):.1%}, KI {lo2:.1%}–{hi2:.1%})")
print(f"Gegenprüfung: {len(g_du)} Dateien mit Urteil, {k_g} kritisch")
print("offen_kritisch:", len(neu), "Zeilen in", len(okdat), "Dateien; neu NP14:", sum(1 for z in neu if z["erstmeldung"] == "NP14"),
      "; bewusst offen:", sum(1 for z in neu if z["bewusst_offen"] == "ja"), "; nicht bewusst offen:",
      sum(1 for z in neu if z["bewusst_offen"] != "ja"), "in", len({z["datei"] for z in neu if z["bewusst_offen"] != "ja"}), "Dateien",
      "; Muster neu:", collections.Counter(z["muster"] for z in neu if z["erstmeldung"] == "NP14").most_common())
