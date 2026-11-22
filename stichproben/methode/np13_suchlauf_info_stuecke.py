"""Suchlauf «Stück ohne Nummer im Blatt Info» (NP13): Sätze in den Schlussvermerken des Blatts Info, die Archivgut nennen,
das nicht verzeichnet ist (lose, verschachtelt, ferner, liegt bei, befindet sich …). Nach Regel 4 der Runde 10 gehört so ein
Satz ins Darin der Bestandszeile. Bearbeitungsvermerke («Nachlieferung eingearbeitet», «Stand», «Letzte Änderung») zählen nicht.
Aufruf: python -I suchlauf_info_stuecke.py <excel_ordner> <aus.csv>"""
import csv, glob, os, re, sys
import openpyxl

o, aus = sys.argv[1:3]
MUSTER = re.compile(r"\b(lose|verschachtelt|unverzeichnet|nicht verzeichnet|nicht erschlossen|ungeordnet|befinde[nt] sich|"
                    r"liegen bei|liegt bei|beigelegt|enthält (auch|ferner|ausserdem|zudem)|ferner|ausserdem|zudem|gehör(t|en) (auch|ferner)|"
                    r"Beilage|Nachtr(ag|äge) (in|im)|weitere[rns]? (Akten|Bände|Unterlagen|Material|Schachtel)|ohne Signatur|nicht signiert)\b", re.I)
WEG = re.compile(r"eingearbeitet|Letzte Änderung|^Stand\b|verzeichnet (von|durch)|Bearbeit|neu (umgebrochen|formatiert)|gelayoutet|"
                 r"Signaturen? (wurden|sind) |Ablieferung|abgeliefert", re.I)
out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    wb = openpyxl.load_workbook(p, read_only=True)
    info = {}
    for x in wb["Info"].iter_rows(values_only=True):
        if x and x[0]:
            info.setdefault(str(x[0]), x[1])
    sv = str(info.get("Schlussvermerke im Findmittel") or "")
    hat_bestandszeile = False
    for r in wb["scope-Import"].iter_rows(min_row=2, values_only=True):
        pass
    ws = wb["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    for r in rows[1:]:
        if r and r[0] is not None and dict(zip(h, r)).get("Stufe") == "Bestand":
            hat_bestandszeile = True
    for satz in re.split(r"(?<=[.!?])\s+|\n", sv):
        s = satz.strip()
        if len(s) > 8 and MUSTER.search(s) and not WEG.search(s):
            out.append({"datei": d, "bestandszeile": "ja" if hat_bestandszeile else "", "satz": s[:300]})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "bestandszeile", "satz"], delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Sätze in", len({x["datei"] for x in out}), "Dateien")
