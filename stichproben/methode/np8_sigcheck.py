"""Grobe Gegenprobe Einheiten <-> PDF-Zeilen (Zeilen-Cache).
(1) erfunden?: Einheit, deren «Nr. im PDF» auf ihrer PDF-Seite an keinem Zeilenanfang steht.
(2) verloren?: PDF-Zeile, deren erstes Wort wie eine Nummer aussieht und an einer x-Position steht, an der sonst
    Signaturen stehen (±3 pt), ohne Einheit mit dieser Nummer auf dieser Seite.
Aufruf: python -I sigcheck.py <cache> <ordner_alt> <ordner_neu> D [D ...]"""
import collections, json, re, sys
import openpyxl

cache, alt, neu, *dd = sys.argv[1:]
NUM = re.compile(r"^(?:[IVX]+\.|[A-Z]\.|\d{1,3}(?:\.\d{1,3})*\.?|\d{1,3}[a-z]\.?|\d{1,3}\s*-\s*\d{1,3}[a-z]?)$")


def norm(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


def einheiten(o, d):
    ws = openpyxl.load_workbook(f"{o}/{d}_scope_import.xlsx", read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True))
    h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]


def pruefe(o, d, zz):
    ee = einheiten(o, d)
    seiten = collections.defaultdict(list)
    for z in zz:
        seiten[z["seite"]].append(z)
    erfunden = []
    xs = collections.Counter()
    belegt = set()
    for e in ee:
        nr, s = norm(e["Nr. im PDF"]), e["PDF-Seite"]
        if not nr:
            continue
        treffer = None
        for z in seiten.get(s, []):
            t = norm(" ".join(w[0] for w in z["worte"][:4]))
            if t.startswith(nr):
                treffer = z
                break
        if treffer is None:
            erfunden.append(f"{e['Signatur']}{'/T' + str(e['Teil']) if e['Teil'] else ''} (Nr. {e['Nr. im PDF']!r}, S.{s})")
        else:
            xs[round(treffer["worte"][0][1])] += 1
            belegt.add((s, nr))
    spalten = {x for x, n in xs.items() if n >= 2}
    verloren = []
    for z in zz:
        w0 = z["worte"][0]
        if not NUM.match(w0[0]):
            continue
        if not any(abs(w0[1] - x) <= 3 for x in spalten):
            continue
        if (z["seite"], norm(w0[0])) in belegt:
            continue
        # Nummern, die als Teil einer längeren Nummer belegt sind (z. B. «VII. 47.1.») nicht melden
        t = norm(" ".join(w[0] for w in z["worte"][:3]))
        if any(s == z["seite"] and t.startswith(n) for s, n in belegt):
            continue
        verloren.append(f"S.{z['seite']} x{w0[1]:.0f}: {' '.join(w[0] for w in z['worte'])[:80]}")
    return len(ee), erfunden, verloren


for d in dd:
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    na, ea, va = pruefe(alt, d, zz)
    nn, en, vn = pruefe(neu, d, zz)
    print(f"### {d}: Einheiten {na} -> {nn}; ohne Zeilenanfang {len(ea)} -> {len(en)}; Nummernzeilen ohne Einheit {len(va)} -> {len(vn)}")
    for x in en:
        if x not in ea:
            print("   + erfunden?", x)
    for x in ea:
        if x not in en:
            print("   - (vorher ohne Zeilenanfang)", x)
    for x in vn:
        if x not in va:
            print("   + verloren?", x)
    for x in va:
        if x not in vn:
            print("   - (vorher Nummer ohne Einheit)", x)
