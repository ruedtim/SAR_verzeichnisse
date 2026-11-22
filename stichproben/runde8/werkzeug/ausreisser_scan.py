"""Ausreisser-Signaturen: (1) einzelne Signatur einer anderen Art unter Geschwistern (ein Buchstabe unter Zahlen),
(2) Nummernsprung unter Geschwistern, nach dem die Folge wieder anschliesst, (3) Komponenten mit führender Null
und 3+ Stellen. Aufruf: python -I ausreisser_scan.py <ordner>"""
import collections, glob, os, re, sys
import openpyxl

def art(k):
    if re.fullmatch(r"\d{1,4}[a-z]?", k): return "zahl"
    if re.fullmatch(r"[IVXL]+[a-z]?", k): return "roem"
    if re.fullmatch(r"[A-Z]", k): return "gross"
    if re.fullmatch(r"[a-z]", k): return "klein"
    return "wort"

for p in sorted(glob.glob(f"{sys.argv[1]}/D*_scope_import.xlsx")):
    name = os.path.basename(p).split("_")[0]
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    rows = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    funde = []
    kinder = collections.defaultdict(list)
    for r in rows:
        if r["Teil"]:
            continue
        s = str(r["Signatur"] or "")
        lokal = s.split(":", 1)[1] if ":" in s else s
        k = [x for x in re.split(r"[.:]", lokal) if x]
        if not k:
            continue
        if any(re.fullmatch(r"0\d{2,}", x) for x in k[1:]):
            funde.append(f"N {s}")
        kinder[r["Parent-ID"]].append((k[-1], s, r))
    for pid, ks in kinder.items():
        arten = collections.Counter(art(k) for k, _, _ in ks)
        if len(ks) >= 4:
            for k, s, r in ks:
                a = art(k)
                if arten[a] == 1 and arten.most_common(1)[0][1] >= 3 and a in ("gross", "klein", "roem") and k not in ("A", "a", "I"):
                    funde.append(f"A {s} ({a} unter {dict(arten)}) | {str(r['Titel'])[:50]}")
        zahlen = [(int(re.match(r"\d+", k).group(0)), s) for k, s, _ in ks if art(k) == "zahl"]
        for (a, sa), (b, sb), (c, sc) in zip(zahlen, zahlen[1:], zahlen[2:]):
            if b - a > 20 and 0 < c - a <= 3:
                funde.append(f"S {sb} (zwischen {sa} und {sc})")
    if funde:
        print(name, len(funde))
        for f in funde[:4]:
            print("   ", f[:150])
