"""PDF-Zeilen (Cache) zeigen, die auf ein Muster passen, mit Umgebung.
Aufruf: python -I zeige.py <cache_ordner> <D-Nummer> <regex> [vor] [nach] [max_treffer]"""
import json
import re
import sys

cache, name, muster = sys.argv[1], sys.argv[2], re.compile(sys.argv[3])
vor = int(sys.argv[4]) if len(sys.argv) > 4 else 2
nach = int(sys.argv[5]) if len(sys.argv) > 5 else 2
maxt = int(sys.argv[6]) if len(sys.argv) > 6 else 6
zz = json.load(open(f"{cache}/{name}.zeilen.json", encoding="utf-8"))["zeilen"]
texte = [" ".join(w[0] for w in z["worte"]) for z in zz]
treffer = [i for i, t in enumerate(texte) if muster.search(t)]
print(f"{name}: {len(treffer)} Treffer")
gezeigt = set()
for i in treffer[:maxt]:
    print("-----")
    for j in range(max(0, i - vor), min(len(zz), i + nach + 1)):
        if j in gezeigt:
            continue
        gezeigt.add(j)
        z = zz[j]
        f = z["worte"][0][3].split("+")[-1][-12:]
        print(f"{'>>' if j == i else '  '} S{z['seite']:<3} {z['top']:6.1f} x0={z['worte'][0][1]:6.1f} {f:12s} "
              f"{z['worte'][0][4]:4.1f} | {texte[j][:110]}")
