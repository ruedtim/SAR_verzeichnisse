"""D3470: jede PDF-Zeile, die mit «Jahr.Laufnummer» (auch zweistellig, mit Buchstabe) beginnt, gegen die Einheiten.
Aufruf: python -I d3470_check.py <cache.json> <xlsx>"""
import collections, json, re, sys
import openpyxl
zz = json.load(open(sys.argv[1], encoding="utf-8"))["zeilen"]
rows = list(openpyxl.load_workbook(sys.argv[2], read_only=True)["scope-Import"].iter_rows(values_only=True))
h = rows[0]
einh = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
nr = collections.Counter((str(e["Nr. im PDF"] or "").rstrip("."), e["PDF-Seite"]) for e in einh)
pat = re.compile(r"^(\d{2}|\d{4})\.\d{1,4}[a-z]?\.?$")
xs = collections.Counter()
ohne, mit = [], 0
for z in zz:
    w = z["worte"]
    if not w or not pat.match(w[0][0]):
        continue
    xs[round(w[0][1])] += 1
    k = (w[0][0].rstrip("."), z["seite"])
    if nr[k]:
        mit += 1
    else:
        ohne.append((z["seite"], round(w[0][1]), " ".join(x[0] for x in w)[:90]))
print("Zeilen mit Jahr.Nr am Anfang:", mit + len(ohne), "davon mit Einheit:", mit, "ohne:", len(ohne))
print("x-Positionen:", xs.most_common(6))
for o in ohne[:60]:
    print("  ohne Einheit:", o)
# Einheiten mit Jahr.Nr-Signatur, deren Nr. auf der Seite nicht als Zeilenanfang steht
anf = collections.Counter((z["worte"][0][0].rstrip("."), z["seite"]) for z in zz if z["worte"])
erf = [(e["ID"], e["Signatur"], e["PDF-Seite"]) for e in einh if pat.match(str(e["Nr. im PDF"] or "")) and not anf[(str(e["Nr. im PDF"]).rstrip("."), e["PDF-Seite"])]]
print("Einheiten ohne Zeilenanfang:", len(erf), erf[:10])
ebenen = collections.Counter((e["Ebene"], e["Stufe"]) for e in einh)
print("Ebenen/Stufen:", ebenen)
hin = collections.Counter(str(e["Prüfhinweise"] or "")[:60] for e in einh)
print("häufigste Hinweise:", hin.most_common(8))
