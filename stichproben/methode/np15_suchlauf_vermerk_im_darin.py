"""Suchlauf «Bearbeitervermerk im Darin» (NP15, Muster K169/K203): Darin-Zeilen aller Einheiten, die wie ein Schluss- oder
Bearbeitervermerk aussehen (Datum mit Name oder Kürzel, «Stand:», «Letzte Änderung», «Archivierung beendet», Fusszeile).
Solche Zeilen gehören ins Blatt Info; im Darin einer Einheit oder der Bestandszeile sind sie kritisch (K169). Gemeldet wird jede
Zeile mit Datei, ID, Signatur, Stufe, ob es die letzte Einheit in PDF-Folge ist (nach PDF-Seite) und dem Muster.
Aufruf: python -I suchlauf_vermerk_im_darin.py <excel_ordner> <aus.csv>"""
import csv, glob, os, re, sys
import openpyxl

o, aus = sys.argv[1:3]
MON = r"(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember|Jan\.|Febr?\.|Aug\.|Sept?\.|Okt\.|Nov\.|Dez\.)"
MUSTER = [
    ("Änderungsvermerk", re.compile(r"\b(Letzte|Erste|Zweite)\s+(Änderung|Ergänzung|Bearbeitung|Revision|Überarbeitung)\b", re.I)),
    ("Stand", re.compile(r"(^|\s)Stand\s*(:|per|vom)?\s*\d{1,2}\.\s*(\d{1,2}\.|" + MON + r")\s*\d{2,4}", re.I)),
    ("Bearbeiter", re.compile(r"\b(bearbeitet|verzeichnet|erschlossen|erfasst|erstellt|geordnet|überarbeitet|revidiert)\s+(von|durch)\s+[A-ZÄÖÜ]", re.I)),
    ("Archivierung", re.compile(r"\b(Archivierung|Neuarchivierung|Verzeichnung)\s+(beendet|abgeschlossen)\b", re.I)),
    ("Datum / Kürzel", re.compile(r"\b(\d{1,2}\.\s*(\d{1,2}\.|" + MON + r")\s*)?(19|20)\d\d\s*/\s*([A-ZÄÖÜ]{2,4}|[a-zäöü]{2,4})\b(\s*/|\s*$)")),
    ("Datum Name klein", re.compile(r"\b\d{1,2}\.\s*" + MON + r"\s+(19|20)\d\d\s+[a-zäöüé]{3,}\s+[a-zäöüé]{3,}")),
    ("Fusszeile", re.compile(r"©\s*Stadtarchiv|Seite \d+ von \d+")),
]
out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    if not ee:
        continue
    letzte = max(ee, key=lambda e: (e.get("PDF-Seite") or 0, e["ID"]))["ID"]
    for e in ee:
        for k, z in enumerate(str(e.get("Darin") or "").split("\n")):
            if not z.strip():
                continue
            for name, rx in MUSTER:
                if rx.search(z):
                    out.append({"datei": d, "id": e["ID"], "signatur": e["Signatur"], "stufe": e["Stufe"],
                                "letzte": "ja" if e["ID"] == letzte else "", "darin_zeile": k + 1, "muster": name, "text": z.strip()[:200]})
                    break
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "id", "signatur", "stufe", "letzte", "darin_zeile", "muster", "text"], delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Zeilen in", len({x["datei"] for x in out}), "Dateien; davon in der letzten Einheit:", sum(1 for x in out if x["letzte"]))
