"""Wie viele Zeilen hat der Kopf-/Fusszeilen-Filter der Prüfmappe (gleicher Text bis auf Ziffern auf >= 3 Seiten)
verdeckt, die NICHT am Seitenrand stehen (y 80–780)? Aufruf: python -I verdeckt.py <cache> D [D ...]"""
import collections, json, re, sys
cache, *dd = sys.argv[1:]
tot = collections.Counter()
for d in dd:
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    kf = collections.defaultdict(set)
    for z in zz:
        if z["worte"]:
            kf[re.sub(r"\d+", "#", " ".join(x[0] for x in z["worte"]))].add(z["seite"])
    wied = {k for k, v in kf.items() if len(v) >= 3}
    gezeigt, verdeckt = set(), []
    for z in zz:
        if not z["worte"]:
            continue
        k = re.sub(r"\d+", "#", " ".join(x[0] for x in z["worte"]))
        if k in wied:
            if k in gezeigt and 80 <= z["top"] <= 780:
                verdeckt.append((z["seite"], " ".join(x[0] for x in z["worte"])[:60]))
            gezeigt.add(k)
    if verdeckt:
        tot[d] = len(verdeckt)
        arten = collections.Counter(re.sub(r"\d+", "#", t) for _, t in verdeckt)
        print(f"{d}: {len(verdeckt)} verdeckt, z. B. {arten.most_common(3)}")
print("Dateien mit verdeckten Inhaltszeilen:", len(tot), "Zeilen:", sum(tot.values()))
