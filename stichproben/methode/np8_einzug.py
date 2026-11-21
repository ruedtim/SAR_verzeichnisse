"""Signal «eingerückte Geschwister»: Folgen von mindestens 3 Geschwistern (gleiche Eltern, keine Teile), deren
Nummer im PDF deutlich weiter rechts steht (>= 20 pt) als bei der Mehrheit der Geschwister – typisch für eine
nummerierte Liste im Inhalt, die als Einheiten gelesen wurde (D3810 8.–21. unter 7.).
Aufruf: python -I einzug.py <cache> <ordner> [D ...]"""
import collections, glob, json, os, re, statistics, sys
import openpyxl

cache, o, *nur = sys.argv[1:]


def norm(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


treffer = 0
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    if nur and d not in nur:
        continue
    try:
        zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    except FileNotFoundError:
        continue
    seiten = collections.defaultdict(list)
    for z in zz:
        seiten[z["seite"]].append(z)
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    gruppen = collections.defaultdict(list)
    for e in ee:
        if e["Teil"]:
            continue
        nr, s = norm(e["Nr. im PDF"]), e["PDF-Seite"]
        x = None
        for z in seiten.get(s, []):
            if norm(" ".join(w[0] for w in z["worte"][:4])).startswith(nr) and nr:
                x = z["worte"][0][1]
                break
        gruppen[e["Parent-ID"]].append((e, x))
    for pid, gg in gruppen.items():
        xs = [x for _, x in gg if x is not None]
        if len(xs) < 4:
            continue
        med = min(xs)
        lauf = []
        for e, x in gg + [(None, None)]:
            if e is not None and x is not None and x - med >= 20:
                lauf.append(e)
                continue
            if len(lauf) >= 3:
                treffer += 1
                print(f"{d}: {len(lauf)} Geschwister eingerückt (x ≥ links {med:.0f} + 20): "
                      f"{lauf[0]['Signatur']} … {lauf[-1]['Signatur']} (S.{lauf[0]['PDF-Seite']}–{lauf[-1]['PDF-Seite']})")
            lauf = []
print("Folgen:", treffer)
