"""Titel «… 1786 (1834 – 1863)»: Jahr direkt vor einer Jahres-Klammer. Aufruf: python -I jahrklammer_scan.py <ordner>"""
import glob, os, re, sys
import openpyxl
J = r"(?:1[2-9]\d\d|20[0-2]\d)"
pat = re.compile(rf"\b{J}\s*\(\s*{J}(?:\s*[–-]\s*{J})?\s*\)")
n = 0
for p in sorted(glob.glob(f"{sys.argv[1]}/D*_scope_import.xlsx")):
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    for r in rows[1:]:
        r = dict(zip(h, r))
        t = str(r.get("Titel") or "")
        if r.get("ID") and pat.search(t):
            n += 1
            print(os.path.basename(p).split("_")[0], r["Signatur"], "|", t[:80], "|", r["von"], r["bis"], r["Zeitraum-Quelle"])
print(n, "Treffer")
