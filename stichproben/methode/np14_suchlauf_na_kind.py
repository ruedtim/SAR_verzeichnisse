"""Suchlauf «n.a als Kind» (Muster 3 der NP12/NP13; Skript von Prüfer G3 der NP13, unverändert übernommen): Einheiten, deren
Signatur auf einen Buchstaben endet («n.a», «n.a.», «n.a)», «n a») und die als Kind von «n.» stehen. Ausgabe je Treffer:
Datei;ID;Signatur;Titel;Eltern-ID und -Signatur;Eltern-Titel;PDF-Seite. Die Treffer sind zu sichten: Teile derselben Sache und
Buchstaben mit eigener Schachtel in der Titelspalte bleiben Kinder (Konvention Runde 11), eigene Gegenstände mit eigenem Datum
in derselben Spalte wie «n.» sind Geschwister (Regel 10).
Aufruf: python -I suchlauf_na_kind.py <excel_ordner> > aus.txt"""
import sys, re, os, openpyxl
d = sys.argv[1]
out = []
for fn in sorted(os.listdir(d)):
    if not fn.endswith('_scope_import.xlsx'):
        continue
    try:
        wb = openpyxl.load_workbook(os.path.join(d, fn), read_only=True)
        ws = wb['scope-Import']
        rows = ws.iter_rows(values_only=True)
        hdr = next(rows)
        allr = [dict(zip(hdr, r)) for r in rows]
    except Exception as e:
        print(fn, 'FEHLER', e); continue
    byid = {str(r['ID']): r for r in allr}
    for r in allr:
        sig = str(r.get('Signatur') or '')
        m = re.match(r'^(.*?[0-9])\.?\s?([a-z])\)?\.?$', sig)
        if not m:
            continue
        p = byid.get(str(r.get('Parent-ID')))
        if not p:
            continue
        ps = str(p.get('Signatur') or '')
        base = m.group(1)
        if ps.rstrip('.') == base.rstrip('.'):
            out.append(f"{fn.split('_')[0]};{r['ID']};{sig};{str(r.get('Titel'))[:50]};P {p['ID']} {ps};{str(p.get('Titel'))[:50]};S.{r.get('PDF-Seite')}")
print('\n'.join(out))
