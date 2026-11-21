"""Zeigt Einheiten zweier Läufe und den PDF-Text ihrer Seite. Aufruf: python -I zeige.py <alt> <neu> PDF:ID[,ID…] …"""
import sys, subprocess, openpyxl, re
alt, neu = sys.argv[1:3]
P = "/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse/findmittel_pdf/pdf"
for arg in sys.argv[3:]:
    pdf, ids = arg.split(":"); ids = [int(x) for x in ids.split(",")]
    for lauf in (alt, neu):
        wb = openpyxl.load_workbook(f"{lauf}/{pdf}_scope_import.xlsx", read_only=True)
        rows = {r[0]: r for r in wb["scope-Import"].iter_rows(min_row=2, values_only=True) if r and r[0] is not None}
        pl = list(wb["Prüfliste"].iter_rows(values_only=True)); k = pl[0]
        seiten = {dict(zip(k, r)).get("ID"): dict(zip(k, r)) for r in pl[1:]}
        for i in ids:
            r = rows.get(i)
            if r is None: print(lauf, pdf, i, "FEHLT"); continue
            print(f"{lauf.split('/')[-1]:12} {pdf} {i} {r[2]} | {(r[3] or '')[:80]} | {r[9]}–{r[10]} | Anm {r[11]} | Hinweise: {str((seiten.get(str(i)) or seiten.get(i) or {}).get('Prüfhinweise'))[:150]}")
    print("   DARIN:", (rows[ids[0]][12] or "")[:700].replace("\n", " ¶ "))
