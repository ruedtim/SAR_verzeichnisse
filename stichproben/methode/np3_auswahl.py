"""Dritte Nachprüfung (Stand findmittel_excel/ 20.11.2026, 08:25): Prüfliste aus funde_nachpruefung2.csv.

Auswahl (nur Zeilen mit Status «offen», «teilweise» oder «neu»):
  - alle kritischen Zeilen
  - alle mittleren/geringen Zeilen mit Status «neu» (neue Fehler der zweiten Nachprüfung; die Runde 01:45 zielt
    ausdrücklich auf viele von ihnen)
  - übrige mittlere/geringe Zeilen: je PDF und Hauptmuster höchstens 2, Zufall mit Startwert 20261121
Zeilennummer «nr»: Z<n> = n-te Datenzeile von funde_nachpruefung2.csv.
Spalte «stand_0015» = neu_ist der zweiten Nachprüfung (Stand 00:15); «ist» bleibt der Wert aus
funde_nachpruefung2.csv (= Stand 23:05).
Aufruf: python3 -I np3_auswahl.py   (schreibt np3_pruefliste.csv neben dieses Skript)
"""
import csv, os, re, random, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)
START = 20261121
JE_GRUPPE = 2


def lies(pfad):
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


np2 = lies(os.path.join(STP, "funde_nachpruefung2.csv"))
liste2 = lies(os.path.join(HIER, "np2_pruefliste.csv"))
for r, z in zip(np2, liste2):  # Hauptmuster der nachgeprüften Zeilen aus der zweiten Prüfliste (gleiche Reihenfolge)
    assert (r["pdf"], r["seite"], r["signatur"]) == (z["pdf"], z["seite"], z["signatur"])
    r["_m"], r["_a"] = z["muster"], z["auswahl"].split(" (")[0]
for r in np2[len(liste2):]:
    assert r["status"] == "neu"
    m = re.match(r"\s*\[(M\d\d)", r["bemerkung"])
    r["_m"], r["_a"] = (m.group(1) if m else "M19"), "neu"

aus = []
for i, r in enumerate(np2, 1):
    r["_nr"] = f"Z{i}"
    if r["status"] not in ("offen", "teilweise", "neu"):
        continue
    if r["schwere"] == "kritisch":
        aus.append((r, "kritisch"))
    elif r["status"] == "neu":
        aus.append((r, "neu (2. Nachprüfung)"))
rng = random.Random(START)
gruppen = collections.defaultdict(list)
for r in np2:
    if r["status"] in ("offen", "teilweise") and r["schwere"] != "kritisch":
        gruppen[(r["pdf"], r["_m"])].append(r)
for k in sorted(gruppen):
    zeilen = gruppen[k][:]
    rng.shuffle(zeilen)
    for r in zeilen[:JE_GRUPPE]:
        aus.append((r, "mittel-Stichprobe"))
aus.sort(key=lambda t: int(t[0]["_nr"][1:]))

felder = ["nr", "auswahl", "muster", "status_vorher", "pdf", "seite", "signatur", "feld", "schwere", "soll", "ist",
          "bemerkung", "stand_0015"]
with open(os.path.join(HIER, "np3_pruefliste.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader()
    for r, a in aus:
        w.writerow(dict(nr=r["_nr"], auswahl=a, muster=r["_m"], status_vorher=r["status"], pdf=r["pdf"], seite=r["seite"],
                        signatur=r["signatur"], feld=r["feld"], schwere=r["schwere"], soll=r["soll"], ist=r["ist"],
                        bemerkung=r["bemerkung"], stand_0015=r["neu_ist"]))
print(len(aus), collections.Counter(a for _, a in aus))
print("Gruppen mittel:", len(gruppen), "Zeilen mittel offen/teilw.:", sum(len(v) for v in gruppen.values()))
