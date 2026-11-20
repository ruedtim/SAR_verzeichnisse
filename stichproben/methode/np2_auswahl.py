"""Zweite Nachprüfung (Stand findmittel_excel/ 20.11.2026, 00:15): Prüfliste aus funde_nachpruefung.csv.

Auswahl:
  - alle Zeilen mit Status «neu» (neue Fehler der ersten Nachprüfung)
  - alle kritischen Zeilen mit Status «offen» oder «teilweise» (aus funde.csv und Zusatzfunden)
  - mittlere Zeilen mit Status «offen» oder «teilweise»: je PDF und Hauptmuster höchstens 3, Zufall mit Startwert 20261120
Zeilennummer «nr»: N<n> = n-te Datenzeile von funde_nachpruefung.csv.
Spalte «stand_2305» = neu_ist der ersten Nachprüfung (Stand 23:05); «ist» bleibt der Wert aus funde_nachpruefung.csv.
Aufruf: python3 -I np2_auswahl.py   (schreibt np2_pruefliste.csv neben dieses Skript)
"""
import csv, os, re, random, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
START = 20261120


def lies(pfad):
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


np1 = lies(os.path.join(STP, "funde_nachpruefung.csv"))
liste1 = lies(os.path.join(HIER, "np_pruefliste.csv"))
for r, z in zip(np1, liste1):  # Hauptmuster der Paketzeilen aus der ersten Prüfliste (gleiche Reihenfolge)
    assert (r["pdf"], r["seite"], r["signatur"]) == (z["pdf"], z["seite"], z["signatur"])
    r["_m"], r["_a"] = z["muster"], z["auswahl"].split(" (")[0]
for r in np1[len(liste1):]:
    m = re.match(r"\s*\[(M\d\d)", r["bemerkung"])
    r["_m"], r["_a"] = (m.group(1) if m else "M19"), "neu"

aus = []
for i, r in enumerate(np1, 1):
    r["_nr"] = f"N{i}"
    if r["status"] == "neu":
        aus.append((r, "neu (1. Nachprüfung)"))
    elif r["status"] in ("offen", "teilweise") and r["schwere"] == "kritisch":
        aus.append((r, "kritisch offen/teilweise"))
rng = random.Random(START)
gruppen = collections.defaultdict(list)
for r in np1:
    if r["status"] in ("offen", "teilweise") and r["schwere"] != "kritisch" and r["_a"] != "neu":
        gruppen[(r["pdf"], r["_m"])].append(r)
for k in sorted(gruppen):
    zeilen = gruppen[k][:]
    rng.shuffle(zeilen)
    for r in sorted(zeilen[:3], key=lambda r: int(r["_nr"][1:])):
        aus.append((r, "mittel-Stichprobe"))

felder = ["nr", "auswahl", "muster", "status_vorher", "pdf", "seite", "signatur", "feld", "schwere", "soll", "ist",
          "bemerkung", "stand_2305"]
with open(os.path.join(HIER, "np2_pruefliste.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader()
    for r, a in aus:
        w.writerow(dict(nr=r["_nr"], auswahl=a, muster=r["_m"], status_vorher=r["status"], pdf=r["pdf"], seite=r["seite"],
                        signatur=r["signatur"], feld=r["feld"], schwere=r["schwere"], soll=r["soll"], ist=r["ist"],
                        bemerkung=r["bemerkung"], stand_2305=r["neu_ist"]))
print(len(aus), collections.Counter(a for _, a in aus))
print("Gruppen mittel:", len(gruppen), "Zeilen mittel offen/teilw.:", sum(len(v) for v in gruppen.values()))
