"""Blatt Info: Schlusszeilen zeigen. Aufruf: python -I info_schluss.py <xlsx> [max]"""
import sys
import openpyxl
wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
for r in wb["Info"].iter_rows(values_only=True):
    if r and r[0] and str(r[0]).startswith("Schluss"):
        t = str(r[1] or "").split("\n")
        print(f"{r[0]}: {len(t)} Zeilen")
        for x in t[:n]:
            print("   ", x[:120])
