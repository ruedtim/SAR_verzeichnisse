"""Dateien, deren Schlussvermerke im Blatt Info sich zwischen zwei Läufen unterscheiden. Aufruf: python -I info_vergleich.py alt neu"""
import glob, sys
from pathlib import Path
import openpyxl
def schluss(p):
    wb = openpyxl.load_workbook(p, read_only=True)
    return [r[1] for r in wb["Info"].iter_rows(values_only=True) if r and r[0] == "Schlussvermerke im Findmittel"]
alt, neu = Path(sys.argv[1]), Path(sys.argv[2])
for f in sorted(glob.glob(str(neu / "D*_scope_import.xlsx"))):
    n = Path(f).name
    if (alt / n).exists() and schluss(alt / n) != schluss(f):
        print(n.split("_")[0])
