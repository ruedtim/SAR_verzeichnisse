"""Wo steht ein Wort in zwei Läufen? Aufruf: python -I wo_wort.py <alt> <neu> PDF wort [wort …]"""
import sys, openpyxl
alt, neu, pdf, *ww = sys.argv[1:]
for lauf in (alt, neu):
    wb = openpyxl.load_workbook(f"{lauf}/{pdf}_scope_import.xlsx", read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True)); kopf = [str(k) for k in rows[0]]
    info = {str(x[0]): x[1] for x in wb["Info"].iter_rows(values_only=True) if x and x[0]}
    for w in ww:
        for r in rows[1:]:
            if not r or r[0] is None: continue
            for k in ("Titel", "Darin", "Entstehungszeitraum, Anm."):
                t = str(r[kopf.index(k)] or "")
                if w in t:
                    p = t.find(w)
                    print(f"{lauf.split('/')[-1]:12} {pdf} {r[2]} [{k}] …{t[max(0,p-120):p+80]!r}")
        s = str(info.get("Schlussvermerke im Findmittel") or "")
        if w in s:
            p = s.find(w); print(f"{lauf.split('/')[-1]:12} {pdf} [Schlussvermerke] …{s[max(0,p-120):p+80]!r}")
