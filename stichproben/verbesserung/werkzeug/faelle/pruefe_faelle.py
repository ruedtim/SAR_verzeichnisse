"""Vergleicht Soll-Zeiträume (Jahre) aus einer Fallliste mit den Excel-Ausgaben eines oder mehrerer Läufe.
Aufruf: python -I pruefe_faelle.py faelle.csv ordner1 [ordner2 …]"""
import csv, re, sys, openpyxl
faelle = list(csv.DictReader(open(sys.argv[1], encoding="utf-8", newline=""), delimiter=";"))
ordner = sys.argv[2:]
cache = {}
def zeile(o, pdf, id_):
    k = (o, pdf)
    if k not in cache:
        ws = openpyxl.load_workbook(f"{o}/{pdf}_scope_import.xlsx", read_only=True)["scope-Import"]
        cache[k] = {r[0]: r for r in ws.iter_rows(min_row=2, values_only=True) if r and r[0] is not None}
    return cache[k].get(int(id_))
def jahr(s):
    m = re.search(r"\d{4}", str(s or ""))
    return m.group(0) if m else ""
def ok(soll, ist):
    return soll == "*" or ist in soll.split("|")
gut = [0] * len(ordner)
for f in faelle:
    teile = []
    for n, o in enumerate(ordner):
        r = zeile(o, f["pdf"], f["id"])
        if r is None:
            teile.append("FEHLT"); continue
        v, b = jahr(r[9]), jahr(r[10])
        t = ok(f["soll_von"], v) and ok(f["soll_bis"], b)
        gut[n] += t
        teile.append(f"{'ok ' if t else 'XX '}{r[9] or '–'}–{r[10] or '–'} [{(r[11] or '')[:45]}]")
    sig = (zeile(ordner[0], f["pdf"], f["id"]) or [None] * 3)[2]
    print(f"{f['pdf']:8} {f['id']:>5} {str(sig)[:24]:24} soll {f['soll_von']}–{f['soll_bis']:9} | " + " | ".join(teile) + f"   ({f['notiz']})")
print("richtig:", " / ".join(f"{g} von {len(faelle)}" for g in gut))
