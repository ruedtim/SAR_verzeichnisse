"""Zeigt für die Einheiten einer Diff-Datei (pdf;id;...) Titel, Zeitraum und Darin-Unterschiede zwischen zwei Läufen.
Aufruf: python -I zeige_diff.py <diff.csv> <ordner_alt> <ordner_neu> [pdf ...] (Ordner mit vollem Pfad)"""
import csv, difflib, sys, openpyxl
diff, alt, neu, nur = sys.argv[1], sys.argv[2], sys.argv[3], set(sys.argv[4:])
rows = list(csv.DictReader(open(diff, encoding="utf-8"), delimiter=";"))
cache = {}
def lade(lauf, pdf):
    if (lauf, pdf) not in cache:
        wb = openpyxl.load_workbook(f"{lauf}/{pdf}_scope_import.xlsx", read_only=True)
        ws = wb["scope-Import"]
        it = ws.iter_rows(values_only=True)
        kopf = next(it)
        cache[(lauf, pdf)] = (kopf, {r[0]: r for r in it if r and r[0] is not None})
    return cache[(lauf, pdf)]
for r in rows:
    if nur and r["pdf"] not in nur: continue
    i = int(r["id"])
    kopf, a = lade(alt, r["pdf"]); _, b = lade(neu, r["pdf"])
    ra, rb = a.get(i), b.get(i)
    print(f"=== {r['pdf']} {r['signatur']} (id {i})")
    if ra is None or rb is None:
        print("   fehlt in", alt if ra is None else neu); continue
    for k, (x, y) in enumerate(zip(ra, rb)):
        if x == y: continue
        name = kopf[k]
        xs, ys = str(x or ""), str(y or "")
        if "\n" in xs or "\n" in ys or len(xs) > 160 or len(ys) > 160:
            print(f"   [{name}]")
            for d in difflib.unified_diff(xs.split("\n"), ys.split("\n"), lineterm="", n=0):
                if d.startswith(("---", "+++", "@@")): continue
                print("     ", d[:230])
        else:
            print(f"   [{name}] {xs!r} → {ys!r}")
