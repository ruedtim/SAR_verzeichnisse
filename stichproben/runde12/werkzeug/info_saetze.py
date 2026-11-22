"""Alle Texte im Blatt Info (Schlussvermerke u. ä.) aller Dateien; Sätze mit Behälter/Menge herausfiltern."""
import openpyxl, glob, os, re, sys, csv
verz = sys.argv[1]
aus = sys.argv[2]
keys = set()
BEH = re.compile(r"\b(?:Archiv|Norm)?(?:[Ss]chachtel(?:n)?|Bände?n?|Mappen?|Ordner|Kartons?|Kisten?|Couverts?|Umschläge?n?|"
                 r"Hefte?n?|Rollen?|Pläne|Fotos?|Fotografien|Dossiers?|Faszikel|Laufmeter|Bündel|Registraturen?|Register)\b")
MENGE = re.compile(r"\b(?:eine?n?|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|einige|mehrere|weitere|\d{1,4})\s+"
                   r"(?:\w+\s+){0,2}?(?:Archiv|Norm)?(?:[Ss]chachtel(?:n)?|Bände?n?|Mappen?|Ordner|Kartons?|Kisten?|Couverts?|"
                   r"Umschläge?n?|Hefte?n?|Rollen?|Pläne|Fotos?|Fotografien|Dossiers?|Faszikel|Laufmeter|Bündel|Register)\b")
rows = []
for f in sorted(glob.glob(os.path.join(verz, "D*_scope_import.xlsx"))):
    d = os.path.basename(f).split("_")[0]
    wb = openpyxl.load_workbook(f, read_only=True)
    ws = wb["Info"]
    for r in ws.iter_rows(values_only=True):
        if not r or r[0] is None or r[1] is None:
            continue
        k = str(r[0])
        keys.add(k)
        if k in ("Schlussvermerke im Findmittel", "Anhang", "Notizen") or "Schluss" in k or "Anhang" in k or "Notiz" in k:
            txt = str(r[1])
            # Zeilen zu Absätzen zusammenziehen: Satz endet mit . ! ? :
            buf = ""
            for zl in txt.split("\n"):
                buf = (buf + " " + zl).strip() if buf else zl.strip()
                if re.search(r"[.!?:]\s*$", zl) or len(buf) > 600:
                    rows.append((d, k, buf)); buf = ""
            if buf:
                rows.append((d, k, buf))
    wb.close()
treffer = [(d, k, s) for d, k, s in rows if MENGE.search(s)]
with open(aus, "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, delimiter=";")
    w.writerow(["datei", "feld", "satz"])
    w.writerows(treffer)
print("Info-Schlüssel:", sorted(keys)[:80])
print(len(rows), "Sätze,", len(treffer), "mit Menge+Behälter")
