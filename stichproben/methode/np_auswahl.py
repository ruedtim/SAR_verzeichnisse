"""Nachprüfung (Stand findmittel_excel/ 19.11.2026, 23:05): Prüfliste aus funde.csv und zusatzfunde_gesamtscan.csv.

Auswahl:
  - alle Fundzeilen mit Schwere «kritisch» aus funde.csv
  - alle Zeilen aus zusatzfunde_gesamtscan.csv
  - mittlere Fundzeilen der Hauptmuster M05, M06, M07, M09, M11, M12, M14: je PDF und Muster höchstens 5.
    Vorrang haben Zeilen, deren Seite auf einer Prüfseite aus pruefseiten.csv liegt («alle» = jede Seite);
    innerhalb dieser Klassen entscheidet der Zufall (Startwert 20261119). Nur wenn ein PDF auf seinen
    Prüfseiten weniger als 5 Zeilen eines Musters hat, wird mit Zeilen von anderen Seiten aufgefüllt.
Zeilennummer «nr»: F<n> = n-te Datenzeile von funde.csv, Z<n> = n-te Datenzeile von zusatzfunde_gesamtscan.csv.
Aufruf: python3 -I np_auswahl.py   (schreibt np_pruefliste.csv neben dieses Skript)
"""
import csv, random, re, os, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
ZIEL = ["M05", "M06", "M07", "M09", "M11", "M12", "M14"]
START = 20261119


def lies(pfad):
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def muster(r):
    m = re.match(r"\[(M\d\d)\]", r["bemerkung"])
    return m.group(1) if m else ""


def seiten(text):
    out = set()
    for teil in re.split(r"[,;/]| und ", text):
        zahlen = [int(z) for z in re.findall(r"\d+", teil)]
        if len(zahlen) >= 2 and re.search(r"\d\s*[–-]\s*\d", teil):
            out.update(range(zahlen[0], zahlen[1] + 1))
        else:
            out.update(zahlen)
    return out


pruef = {}
for r in lies(os.path.join(HIER, "pruefseiten.csv")):
    s = r["Prüfseiten (Zufall)"].strip()
    pruef[r["PDF"]] = None if s == "alle" else {int(x) for x in s.split(",") if x.strip()}

funde = lies(os.path.join(STP, "funde.csv"))
zusatz = lies(os.path.join(STP, "zusatzfunde_gesamtscan.csv"))
aus = []
for i, r in enumerate(funde, 1):
    if r["schwere"] == "kritisch":
        aus.append(dict(nr=f"F{i}", auswahl="kritisch", muster=muster(r), **r))
ZUSATZ_MUSTER = {  # Musterbezeichnung der Zusatzfunde («Muster: …» in der Bemerkung) -> Hauptmuster
    "Einheiten im Vorspann verschluckt": "M01", "Erste Gruppe ohne Nummer verloren": "M01",
    "Mengenangabe als Signatur": "M03", "Aufzählung im Darin als Signatur": "M03",
    "Vierstellige Schachtel als Jahr": "M09", "Eigener Teil-Titel ins Darin verschoben": "M13",
}
for i, r in enumerate(zusatz, 1):
    m = re.match(r"Muster: ([^.]*)\.", r["bemerkung"])
    aus.append(dict(nr=f"Z{i}", auswahl="zusatz", muster=ZUSATZ_MUSTER.get(m.group(1) if m else "", "M01"), **r))

rng = random.Random(START)
gruppen = collections.defaultdict(list)
for i, r in enumerate(funde, 1):
    if r["schwere"] == "mittel" and muster(r) in ZIEL:
        gruppen[(r["pdf"], muster(r))].append((i, r))
for (pdf, m) in sorted(gruppen):
    zeilen = gruppen[(pdf, m)]
    ps = pruef.get(pdf)
    auf = [z for z in zeilen if ps is None or seiten(z[1]["seite"]) & ps]
    rest = [z for z in zeilen if z not in auf]
    rng.shuffle(auf)
    rng.shuffle(rest)
    for i, r in sorted((auf + rest)[:5]):
        lage = "Prüfseite" if (i, r) in auf else "andere Seite"
        aus.append(dict(nr=f"F{i}", auswahl=f"mittel-Stichprobe ({lage})", muster=m, **r))

felder = ["nr", "auswahl", "muster", "pdf", "seite", "signatur", "feld", "schwere", "soll", "ist", "bemerkung"]
with open(os.path.join(HIER, "np_pruefliste.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader()
    for r in aus:
        w.writerow({k: r[k] for k in felder})
z = collections.Counter(r["auswahl"].split(" (")[0] for r in aus)
print(len(aus), dict(z))
print(collections.Counter(r["auswahl"] for r in aus))
print(collections.Counter(r["muster"] for r in aus if r["auswahl"].startswith("mittel")))
