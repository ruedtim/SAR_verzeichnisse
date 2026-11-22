"""Auszug je Datei: die Zeilen, die der alte Kopf/Fuss-Filter in der Prüfmappe verdeckt hatte, mit 2 Zeilen Umfeld aus der
korrigierten Prüfmappe (Stand jetzt). Aufruf: python -I verdeckt_auszug.py <cache> <mappen_korrigiert> <aus> D [D ...]"""
import collections, json, os, re, sys
cache, mo, aus, *dd = sys.argv[1:]
os.makedirs(aus, exist_ok=True)
for d in dd:
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    kf = collections.defaultdict(set)
    for z in zz:
        if z["worte"]:
            kf[re.sub(r"\d+", "#", " ".join(x[0] for x in z["worte"]))].add(z["seite"])
    wied = {k for k, v in kf.items() if len(v) >= 3}
    gezeigt, verd = set(), set()
    for z in zz:
        if not z["worte"]:
            continue
        k = re.sub(r"\d+", "#", " ".join(x[0] for x in z["worte"]))
        if k in wied:
            if k in gezeigt and 80 <= z["top"] <= 780:
                verd.add((z["seite"], round(z["top"])))
            gezeigt.add(k)
    m = open(f"{mo}/{d}.txt", encoding="utf-8").read().split("\n")
    kopf = [l for l in m[:4]]
    pdf = [(i, l) for i, l in enumerate(m) if re.match(r"^S\d+\s+\d+\s+\|", l)]
    treffer = set()
    for i, l in pdf:
        mm = re.match(r"^S(\d+)\s+(\d+)\s+\|", l)
        if (int(mm.group(1)), int(mm.group(2))) in verd:
            treffer.add(i)
    zeigen = sorted({j for i in treffer for j in range(i - 2, i + 3) if 0 <= j < len(m)})
    out = kopf + [f"== {len(treffer)} vorher verdeckte Zeilen (markiert mit «>>»), je mit 2 Zeilen Umfeld; Stand jetzt"]
    vor = None
    for j in zeigen:
        if vor is not None and j > vor + 1:
            out.append("   …")
        out.append((">> " if j in treffer else "   ") + m[j])
        vor = j
    open(f"{aus}/{d}.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(d, len(treffer))
