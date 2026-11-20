"""Vierte Nachprüfung (Stand findmittel_excel/ 20.11.2026, 11:30): Prüfliste aus funde_nachpruefung3.csv.

Auswahl: alle Zeilen mit Status «offen», «teilweise», «neu» oder «schlechter» (Zeilen «behoben» nicht).
  - kritisch                    : alle kritischen Zeilen (Auftrag 1, 58 Zeilen)
  - mittel/gering, geändert      : alle übrigen Zeilen in PDFs, deren Excel sich seit 08:25 inhaltlich geändert hat
                                   (Auftrag 2; Liste np4_geaendert.txt = Inhaltsvergleich aller Blätter, zellen.py)
  - mittel/gering, unverändert   : übrige Zeilen in PDFs ohne inhaltliche Änderung – werden nicht neu angesehen,
                                   der Befund 08:25 bleibt (offen/teilweise; «neu» -> «offen»)
Zeilennummer «nr»: Z<n> = n-te Datenzeile von funde_nachpruefung3.csv.
Spalte «stand_0825» = neu_ist der dritten Nachprüfung (Stand 08:25); «ist» bleibt der Wert aus
funde_nachpruefung3.csv (= Stand 00:15). «herkunft»: «neu 3. Nachprüfung» (Zeile war dort neu) oder «älter».
Aufruf: python3 -I np4_auswahl.py   (schreibt np4_pruefliste.csv neben dieses Skript)
"""
import csv, os, re, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)


def lies(pfad):
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


np3 = lies(os.path.join(STP, "funde_nachpruefung3.csv"))
liste3 = lies(os.path.join(HIER, "np3_pruefliste.csv"))
geaendert = {z.strip() for z in open(os.path.join(HIER, "np4_geaendert.txt"), encoding="utf-8") if z.strip()}
for r, z in zip(np3, liste3):  # Hauptmuster der nachgeprüften Zeilen aus der dritten Prüfliste (gleiche Reihenfolge)
    assert (r["pdf"], r["seite"], r["signatur"]) == (z["pdf"], z["seite"], z["signatur"])
    r["_m"], r["_h"] = z["muster"], "älter"
for r in np3[len(liste3):]:
    assert r["status"] == "neu"
    m = re.match(r"\s*\[(M\d\d)", r["bemerkung"])
    r["_m"], r["_h"] = (m.group(1) if m else "M19"), "neu 3. Nachprüfung"

aus = []
for i, r in enumerate(np3, 1):
    r["_nr"] = f"Z{i}"
    if r["status"] not in ("offen", "teilweise", "neu", "schlechter"):
        continue
    pdf = r["pdf"][:-4] if r["pdf"].endswith(".pdf") else r["pdf"]
    if r["schwere"] == "kritisch":
        a = "kritisch"
    elif pdf in geaendert:
        a = "mittel/gering, geändert"
    else:
        a = "mittel/gering, unverändert"
    aus.append((r, a, "ja" if pdf in geaendert else "nein"))

felder = ["nr", "auswahl", "pdf_geaendert", "herkunft", "muster", "status_vorher", "pdf", "seite", "signatur", "feld",
          "schwere", "soll", "ist", "bemerkung", "stand_0825"]
with open(os.path.join(HIER, "np4_pruefliste.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader()
    for r, a, g in aus:
        w.writerow(dict(nr=r["_nr"], auswahl=a, pdf_geaendert=g, herkunft=r["_h"], muster=r["_m"], status_vorher=r["status"],
                        pdf=r["pdf"], seite=r["seite"], signatur=r["signatur"], feld=r["feld"], schwere=r["schwere"],
                        soll=r["soll"], ist=r["ist"], bemerkung=r["bemerkung"], stand_0825=r["neu_ist"]))
print(len(aus), collections.Counter(a for _, a, _ in aus))
print("kritisch in geänderten PDFs:", sum(1 for _, a, g in aus if a == "kritisch" and g == "ja"))
