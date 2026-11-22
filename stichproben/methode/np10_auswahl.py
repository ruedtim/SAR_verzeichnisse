"""Stichprobe aus den nie geprüften Dateien: alle Verdachtsfälle aus np9_verdacht.csv (ohne die in Runde 8 geänderten,
die in der Gegenprüfung stecken) plus eine Zufallsauswahl, geschichtet nach Gliederung und Umfang (Einheiten),
proportional mit mindestens einer Datei je Gliederungsart. Aufruf: python -I auswahl.py <population.csv> <n_zufall> <seed> <aus.csv>"""
import collections, csv, random, sys
pop, n, seed, aus = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
r = list(csv.DictReader(open(pop, encoding="utf-8"), delimiter=";"))
nie = [x for x in r if not x["geprueft"]]
def kl(e):
    e = int(e)
    return "a ≤10" if e <= 10 else "b 11–50" if e <= 50 else "c 51–200" if e <= 200 else "d >200"
verd = [x for x in nie if x["verdacht"] and not x["geaendert_r8"]]
rest = [x for x in nie if not x["verdacht"] and not x["geaendert_r8"]]
schicht = collections.defaultdict(list)
for x in rest:
    schicht[(x["gliederung"], kl(x["einheiten"]))].append(x)
for k in schicht:
    schicht[k].sort(key=lambda x: x["datei"])
# proportionale Zuteilung (grösster Rest), dann mindestens 1 je Gliederungsart
quote = {k: n * len(v) / len(rest) for k, v in schicht.items()}
zu = {k: int(q) for k, q in quote.items()}
for k in sorted(quote, key=lambda k: quote[k] - zu[k], reverse=True)[: n - sum(zu.values())]:
    zu[k] += 1
for g in sorted({k[0] for k in schicht}):
    if not any(zu[k] for k in schicht if k[0] == g):
        k = max((k for k in schicht if k[0] == g), key=lambda k: len(schicht[k]))
        zu[k] += 1
rnd = random.Random(seed)
wahl = []
for k in sorted(schicht):
    for x in rnd.sample(schicht[k], min(zu[k], len(schicht[k]))):
        wahl.append(dict(x, grund=f"zufall {k[0]} {k[1]}"))
for x in verd:
    wahl.append(dict(x, grund=f"verdacht {x['verdacht']}"))
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(wahl[0]), delimiter=";")
    w.writeheader(); w.writerows(sorted(wahl, key=lambda x: x["datei"]))
print(len(nie), "nie geprüft;", len(verd), "Verdacht (ohne Runde-8-Dateien);", len(rest), "Rest; Zufall", sum(1 for x in wahl if x["grund"].startswith("zufall")))
for k in sorted(schicht):
    print(f"  {k[0]:<20} {k[1]:<9} {len(schicht[k]):>4}  gezogen {zu[k]}")
