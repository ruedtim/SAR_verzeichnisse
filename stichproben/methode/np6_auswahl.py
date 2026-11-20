"""Sechste Nachprüfung (Stand findmittel_excel/ 20.11.2026, 15:43): Prüfliste aus funde_nachpruefung5.csv.

Auswahl: alle Zeilen mit Status ≠ «behoben» (offen, teilweise, neu, schlechter).
  - kritisch                    : alle kritischen Zeilen (Auftrag 1, zuerst; 11 neu, 18 teilweise, 4 offen)
  - schlechter                  : die drei Zeilen «schlechter» aus Runde 5 (Z121, Z221, Z316)
  - mittel/gering, geändert      : alle übrigen Zeilen in PDFs, deren Excel sich seit 13:15 inhaltlich geändert hat
                                   (Liste np6_geaendert.txt = Inhaltsvergleich aller Blätter ohne Zeile «Erzeugt»)
  - mittel/gering, unverändert   : übrige Zeilen in PDFs ohne inhaltliche Änderung – Befund 13:15 bleibt
                                   (offen/teilweise/schlechter; «neu» -> «offen»)
Kritische Zeilen in unveränderten PDFs werden ebenfalls übernommen (Spalte pdf_geaendert = nein).
Zeilennummer «nr»: Z<n> = n-te Datenzeile von funde_nachpruefung5.csv.
Spalte «stand_1315» = neu_ist der fünften Nachprüfung (Stand 13:15); «ist» bleibt der Wert aus
funde_nachpruefung5.csv (= Stand 11:30). «herkunft»: «neu 5. Nachprüfung» (Zeile war dort neu) oder «älter».
Aufruf: python3 -I np6_auswahl.py   (schreibt np6_pruefliste.csv neben dieses Skript)
"""
import csv, os, re, collections

HIER = os.path.dirname(os.path.abspath(__file__))
STP = os.path.dirname(HIER)


def lies(pfad):
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


np4 = lies(os.path.join(STP, "funde_nachpruefung5.csv"))
liste4 = lies(os.path.join(HIER, "np5_pruefliste.csv"))
geaendert = {z.strip() for z in open(os.path.join(HIER, "np6_geaendert.txt"), encoding="utf-8") if z.strip()}
for r, z in zip(np4, liste4):  # Hauptmuster der nachgeprüften Zeilen aus der vierten Prüfliste (gleiche Reihenfolge)
    assert (r["pdf"], r["seite"], r["signatur"]) == (z["pdf"], z["seite"], z["signatur"])
    r["_m"], r["_h"] = z["muster"], "älter"
for r in np4[len(liste4):]:
    assert r["status"] == "neu"
    m = re.match(r"\s*\[(M\d\d)", r["bemerkung"])
    r["_m"], r["_h"] = (m.group(1) if m else "M19"), "neu 5. Nachprüfung"

aus = []
for i, r in enumerate(np4, 1):
    r["_nr"] = f"Z{i}"
    if r["status"] == "behoben":
        continue
    assert r["status"] in ("offen", "teilweise", "neu", "schlechter"), r["status"]
    pdf = r["pdf"][:-4] if r["pdf"].endswith(".pdf") else r["pdf"]
    if r["schwere"] == "kritisch":
        a = "kritisch"
    elif r["status"] == "schlechter":
        a = "schlechter"
    elif pdf in geaendert:
        a = "mittel/gering, geändert"
    else:
        a = "mittel/gering, unverändert"
    aus.append((r, a, "ja" if pdf in geaendert else "nein"))

felder = ["nr", "auswahl", "pdf_geaendert", "herkunft", "muster", "status_vorher", "pdf", "seite", "signatur", "feld",
          "schwere", "soll", "ist", "bemerkung", "stand_1315"]
with open(os.path.join(HIER, "np6_pruefliste.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader()
    for r, a, g in aus:
        w.writerow(dict(nr=r["_nr"], auswahl=a, pdf_geaendert=g, herkunft=r["_h"], muster=r["_m"], status_vorher=r["status"],
                        pdf=r["pdf"], seite=r["seite"], signatur=r["signatur"], feld=r["feld"], schwere=r["schwere"],
                        soll=r["soll"], ist=r["ist"], bemerkung=r["bemerkung"], stand_1315=r["neu_ist"]))
print(len(aus), collections.Counter(a for _, a, _ in aus))
print("nach Auswahl und Status vorher:", collections.Counter((a, r["status"]) for r, a, _ in aus))
print("kritisch in geänderten PDFs:", sum(1 for _, a, g in aus if a == "kritisch" and g == "ja"),
      "| in unveränderten:", sorted({r["pdf"] for r, a, g in aus if a == "kritisch" and g == "nein"}))
