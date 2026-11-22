"""Nachprüfung 15 zusammenführen: Urteile G1–G2, Funde G1–G2 + D1–D8 + Z1–Z3 + ZL1 + S1 + V1 (Vorfunde der Prüfsession),
Dateiurteile (G, Z, D), offen_kritisch.csv mit stabilen K-Nummern (behobene Zeilen fallen weg, neue kritische Zeilen bekommen
die nächsten freien Nummern), Restrate aus der dritten Zufallsstichprobe und aus allen drei zusammen.
Doppelte neue Funde (dieselbe Datei und Signatur aus mehreren Paketen, z. B. Z und D) werden zusammengelegt: Es bleibt der
Fund des Pakets mit Vorrang G > Z > D > S > V; die anderen bekommen «entfällt (doppelt zu …)».
Aufruf: python -I zusammen15.py <pakete> <offen_kritisch_alt.csv> <aus_ordner>"""
import collections, csv, glob, math, re, sys

pakete, ok_alt, aus = sys.argv[1:4]
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";"))
F = ["pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung", "status", "neu_ist", "muster", "paket", "k_alt",
     "entscheid"]
N_STRATUM = 572   # Stichprobe 3: 715 − 120 (Stichproben 1, 2) − 16 (offen_kritisch NP14) − 10 (von Runde 12 geändert)
FRUEHER = [("Stichprobe 1 (NP13)", 4, 60), ("Stichprobe 2 (NP14)", 3, 60)]
ERST = "NP15"

# Entscheide der Prüfsession nach Rückkehr der Pakete
HERAB = {}        # (Paket, B-Nr.) -> Begründung: kritischer Teil behoben, Rest mittel
HERAB_NEU = {}    # (Paket, pdf, Signaturanfang) -> Begründung: neuer Fund wird mittel
ENTFAELLT = {}    # (Paket, pdf, Signaturanfang) -> Begründung: doppelt zu einer anderen Zeile oder kein Fund
NOTIZ = {         # (Paket, pdf, Signaturanfang) -> Begründung, Schwere bleibt
    ("D1", "D1481.pdf", ""): "Gleiche Familie wie Regel 6 der Runde 11 («Die Protokolle von … bis … sind lose verschachtelt.»), andere Satzform («lückenhaft in einer Archivschachtel»); NP11 hatte den Satz als Bestandsnotiz durchgelassen",
    ("D2", "D1759.pdf", ""): "Konventionsfall: K110 (NP12) hatte als Soll den ganzen Schlussabsatz im Blatt Info; nach Entscheid 1 der Runde 12 (K207, D152401) gehört ein Stück ohne Nummer, das das Findmittel zum Bestand zählt (hier vier CDs), in die Bestandszeile. Bitte bestätigen",
    ("D3", "D2575.pdf", ""): "Neu: Stück ohne Nummer ohne Menge («vereinzelte Dokumente, die nicht ins Acten-Verzeichnis aufgenommen wurden»)",
    ("D3", "D2508.pdf", ""): "Umwertung: NP10 mittel; kritisch wie K75 (D144909, Umfangssatz zum Bestand im Darin der letzten Einheit)",
    ("D4", "D2630.pdf", ""): "Umwertung: NP12 (P3) mittel, vor K169; kritisch nach K169. Unabhängig auch Vorfund V1 der Prüfsession (suchlauf_vermerk_im_darin.py)",
    ("D5", "D3231.pdf", ""): "Grenzfall: Bearbeitervermerk mitten im Verzeichnis, im Darin von Teil 12 statt bei der Gruppe 2.8.; bestimmt den Zeitraum von Teil 12 (NP12: nur Zeitraum als mittel). Anders als D140969 59–81, wo «neu archiviert …» unter dem Kopf der Gruppe steht (kein Fund)",
    ("D7", "D3604.pdf", ""): "Umwertung: NP10 mittel; kritisch nach K169 (Bearbeitervermerk mit Datum und Name im Darin der letzten Schachtel)",
    ("D7", "D3742.pdf", ""): "Umwertung: NP10 mittel; «Letztes Blatt (schwarz kalligraphiert):» beschreibt das Album, nicht Porträt 22, und die Inschrift steht in keinem importierten Feld",
    ("D7", "D3767.pdf", ""): "Umwertung: in NP11 von der Hauptsession herabgestuft, vor dem Entscheid zur Bestandszeile; «Beilagen (3 Farbbildchen)» sind Beilagen des Albums (S. 1). Bitte bestätigen",
    ("D8", "D631.pdf", ""): "Umwertung: NP12 mittel; kritisch nach K169 (Bearbeitervermerk «Ende Juli 2004 / Dr. Robert Dünki» im Darin der Bestandszeile)",
    ("D8", "D414.pdf", ""): "Grenzfall: Der Absatz nach XV. beschreibt die Faszikel I.–XV. von Schachtel 5 (Markierung «rotes D + Datum», 36 Sitzungstage): Inhalt, keine Bestandsgeschichte. Seit NP13 als «Schlussabsatz im Info» bekannt. Bitte bestätigen",
    ("Z1", "D845.pdf", ""): "Wie D3190 9. (NP11 kritisch, behoben): Die Regel «erste Nennung war nur eine Übersichtszeile» gilt nur im Modus dezimal; D845 läuft als Vollsignatur. Fünf leere Teile ohne Darin und Kinder",
}
BEWUSST = {}      # (Paket, pdf, Signaturanfang) -> Begründung: neue kritische Zeile ist bewusst offen
ENTFAELLT_K = {}  # K-Zeilen ohne Paket, die nach einem Entscheid wegfallen
VORRANG = {"G": 0, "Z": 1, "D": 2, "S": 3, "V": 4}

bk = {}
for p in glob.glob(f"{pakete}/G*_altzeilen.csv"):
    pk = re.search(r"/(G\d)_altzeilen", p).group(1)
    for i, r in enumerate(lies(p), 1):   # Altzeilen tragen die K-Nummer in «nr»; Prüfer schreiben [K…] oder [B<i>]
        bk[(pk, r["nr"])] = r["nr"]
        bk[(pk, f"B{i}")] = r["nr"]

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


def befund(r):
    b = (r.get("neu_ist") or "").strip()
    return r.get("ist") if not b or b.lower().startswith(("gleich", "unverändert", "wie vorher")) else b


def signorm(s):
    """Erste Signatur des Felds, ohne «(ID n)», Zusätze nach «;» und Schlusspunkt («V.L.186.:9. (ID 9)» = «V.L.186.:9.»)."""
    s = re.split(r"\s*[;(]|\s+Teil\b|\s+T\d", str(s or ""))[0]
    return re.sub(r"\s+", "", s).rstrip(".").lower()


funde = []
for p in sorted(glob.glob(f"{pakete}/[GZSDV]*_funde.csv")):
    pk = re.search(r"/([GZSDV]L?\d*)_funde", p).group(1)
    for r in lies(p):
        b = r.get("bemerkung") or ""
        m = re.match(r"\s*\[(B\d+|K\d+)\]", b)
        r["paket"] = pk
        mm = re.match(r"\s*(D\d+)", r.get("pdf") or "")
        r["pdf"] = (mm.group(1) if mm else (r.get("pdf") or "").strip()) + ".pdf"
        kn = (r.get("k_nr") or "").strip()
        r["k_alt"] = kn if re.fullmatch(r"K\d+b?", kn) else (bk.get((pk, m.group(1)), m.group(1) if m.group(1).startswith("K") else "") if m else "")
        r["status"] = (r.get("status") or "").strip().lower()
        r["schwere"] = (r.get("schwere") or "").strip().lower()
        r["signatur"] = r.get("signatur") or ""
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

OFFEN = ("neu", "offen", "teilweise", "schlechter")
# doppelte neue Funde zusammenlegen
gruppe = collections.defaultdict(list)
for r in funde:
    if not r["k_alt"] and r["status"] in OFFEN:
        gruppe[(r["pdf"], signorm(r["signatur"]))].append(r)
doppelt = []
for key, rr in gruppe.items():
    if len({x["paket"] for x in rr}) < 2:
        continue
    rr.sort(key=lambda x: (VORRANG.get(x["paket"][0], 9), x["schwere"] != "kritisch"))
    for x in rr[1:]:
        if x["paket"] == rr[0]["paket"]:
            continue
        x["status"] = "entfällt"
        x["entscheid"] = ((x["entscheid"] or "") + f" doppelt zu {rr[0]['paket']}").strip()
        if x["schwere"] == "kritisch" and rr[0]["schwere"] != "kritisch":
            rr[0]["schwere"] = "kritisch"
            rr[0]["entscheid"] = ((rr[0]["entscheid"] or "") + f" kritisch nach {x['paket']}").strip()
        doppelt.append((key, rr[0]["paket"], x["paket"]))

with open(f"{aus}/funde_nachpruefung15.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=F, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(funde)

krit = {r["pdf"].replace(".pdf", "") for r in funde if r["schwere"] == "kritisch" and r["status"] in OFFEN}
du = []
for p in sorted(glob.glob(f"{pakete}/[GZ]*_dateien_urteil.csv")):
    pk = re.search(r"/([GZ]L?\d+)_dateien_urteil", p).group(1)
    for r in lies(p):
        r["paket"] = pk
        r["datei"] = (r.get("datei") or "").replace(".pdf", "").strip()
        du.append(r)
dd = []
for p in sorted(glob.glob(f"{pakete}/D[0-9]*_dateien.csv")):
    pk = re.search(r"/(D\d+)_dateien", p).group(1)
    for r in lies(p):
        r["paket"] = pk
        r["datei"] = (r.get("datei") or "").replace(".pdf", "").strip()
        dd.append(r)

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
        a = dict(a, befund_jetzt=befund(r), status=r["status"], in_arbeit_hauptsession="",
                 paket=r["paket"], entscheid=((a.get("entscheid") or "") + " " + (r.get("entscheid") or "")
                                              + f" {ERST}: in der Gegenprüfung noch kritisch").strip())
    neu.append(a)
nr = max(int(re.sub(r"\D", "", a["nr"])) for a in alt)
for r in funde:
    if r["k_alt"] or r["schwere"] != "kritisch" or r["status"] not in OFFEN:
        continue
    nr += 1
    m = re.search(r"Ursache:\s*([^.;]+)", r.get("bemerkung") or "")
    neu.append({"nr": f"K{nr}", "datei": r["pdf"].replace(".pdf", ""), "signatur_id": r["signatur"], "seite": r["seite"],
                "feld": r["feld"], "befund_jetzt": befund(r), "soll": r["soll"],
                "ursache": m.group(1).strip() if m else "", "status": r["status"], "erstmeldung": ERST,
                "bewusst_offen": "ja" if r.get("bewusst") else "", "in_arbeit_hauptsession": "", "k_alt": "", "paket": r["paket"],
                "muster": r.get("muster", ""), "entscheid": r.get("entscheid", ""), "bemerkung": r.get("bemerkung", "")})
with open(f"{aus}/offen_kritisch.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(neu)

okdat = {z["datei"] for z in neu}
for r in du + dd:
    r["urteil_jetzt"] = "kritisch" if (r["datei"] in krit or r["datei"] in okdat) else "ohne kritischen Fehler"
with open(f"{aus}/dateien_urteil15.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "paket", "einheiten", "umfang_geprueft", "kritisch", "mittel", "gering", "urteil",
                                      "urteil_jetzt", "signale", "schluss", "info", "nicht_uebernommen", "bemerkung"],
                       delimiter=";", extrasaction="ignore")
    w.writeheader(); w.writerows(du + dd)


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
print("doppelt zusammengelegt:", doppelt)
print("K-Prüfung:", {k: (pruef[k]["status"], pruef[k]["schwere"]) for k in sorted(pruef, key=lambda x: int(re.sub(r'\D', '', x)))})
print("weg (behoben):", len(weg), weg)
lo, hi = wilson(k_z, len(z_du))
print(f"Stichprobe 3: {len(z_du)} Dateien, {k_z} kritisch ({k_z / max(1, len(z_du)):.0%}, KI {lo:.0%}–{hi:.0%});"
      f" hochgerechnet auf {N_STRATUM} Dateien: {k_z / max(1, len(z_du)) * N_STRATUM:.0f} (KI {lo * N_STRATUM:.0f}–{hi * N_STRATUM:.0f})")
kk, nn = k_z + sum(k for _, k, _ in FRUEHER), len(z_du) + sum(n for _, _, n in FRUEHER)
lo2, hi2 = wilson(kk, nn)
print(f"Alle drei Stichproben: {kk} von {nn} ({kk / nn:.1%}, KI {lo2:.1%}–{hi2:.1%})")
print(f"Gegenprüfung: {len(g_du)} Dateien mit Urteil, {k_g} kritisch")
dk = collections.Counter(r["urteil_jetzt"] for r in dd)
print(f"Durchsicht D: {len(dd)} Dateizeilen ({len({r['datei'] for r in dd})} Dateien), Urteil jetzt: {dict(dk)};"
      f" Abschnitte mit Fund: {collections.Counter(k for r in dd for k in ('schluss', 'info', 'nicht_uebernommen') if (r.get(k) or '').strip().lower() == 'fund')}")
print("offen_kritisch:", len(neu), "Zeilen in", len(okdat), "Dateien; neu", ERST + ":", sum(1 for z in neu if z["erstmeldung"] == ERST),
      "; bewusst offen:", sum(1 for z in neu if z["bewusst_offen"] == "ja"), "; nicht bewusst offen:",
      sum(1 for z in neu if z["bewusst_offen"] != "ja"), "in", len({z["datei"] for z in neu if z["bewusst_offen"] != "ja"}), "Dateien",
      "; Muster neu:", collections.Counter(z["muster"] for z in neu if z["erstmeldung"] == ERST).most_common())
