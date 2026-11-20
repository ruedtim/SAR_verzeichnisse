"""Zeigt, was das Skript auf einer PDF-Seite «sieht»: Zeilen mit x-Position jedes Worts
(gleiche Parameter wie findmittel_zu_scope.lese_zeilen: x_tolerance=1.5, y_tolerance=2, Zeilen bei |Δtop|<=2.5).
Nur lesen. Aufruf:  uv run --with pdfplumber python -I woerter.py DATEI.pdf SEITE [--fonts]
Ausgabe je Zeile: top | x0 der Zeile | Wörter als  text@x0  (bei --fonts zusätzlich Schrift/Grösse)."""
import sys
import pdfplumber

pdf_pfad, seite_nr = sys.argv[1], int(sys.argv[2])
fonts = "--fonts" in sys.argv
with pdfplumber.open(pdf_pfad) as pdf:
    seite = pdf.pages[seite_nr - 1]
    ws = seite.extract_words(extra_attrs=["fontname", "size"], x_tolerance=1.5, y_tolerance=2)
    ws.sort(key=lambda w: (w["top"], w["x0"]))
    gruppen = []
    for w in ws:
        if gruppen and abs(gruppen[-1][0]["top"] - w["top"]) <= 2.5:
            gruppen[-1].append(w)
        else:
            gruppen.append([w])
    for g in gruppen:
        g.sort(key=lambda w: w["x0"])
        teile = []
        for w in g:
            t = f"{w['text']}@{w['x0']:.0f}"
            if fonts:
                t += f"[{w['fontname'].split('+')[-1]} {w['size']:.1f}]"
            teile.append(t)
        print(f"{min(w['top'] for w in g):6.1f} | {g[0]['x0']:5.1f} | " + "  ".join(teile))
