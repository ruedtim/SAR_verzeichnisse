"""Geschichtete Stichprobe mit festem Startwert."""
import csv, random, sys
SEED = 20261119
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter=";"))
def f(x):
    try: return float(x)
    except: return None
ok = [r for r in rows if r["Status"] != "Fehler"]
for r in ok:
    r["seiten_n"] = int(r["Seiten"])
    r["groesse"] = "klein" if r["seiten_n"] == 1 else ("gross" if r["seiten_n"] >= 50 else "mittel")
rng = random.Random(SEED)
auswahl = {}
def nimm(r, grund):
    if r["PDF"] not in auswahl:
        auswahl[r["PDF"]] = (r, grund)
# Schicht A: alle mit Text erfasst < 100 %
for r in sorted(ok, key=lambda r: r["PDF"]):
    if f(r["Text erfasst"]) is not None and f(r["Text erfasst"]) < 1:
        nimm(r, "A: Text erfasst < 100 %")
# Schicht B: Locher VII.308 – je 1 gross und 1 kleiner/mittel
loc = sorted([r for r in ok if r["Bestand"].startswith("VII.308")], key=lambda r: r["PDF"])
for gr in ("gross", None):
    pool = [r for r in loc if (r["groesse"] == "gross") == (gr == "gross") and r["PDF"] not in auswahl]
    nimm(rng.choice(pool), "B: Firmenarchiv Locher VII.308")
# Schicht C: je Gliederung × Grösse (nur 100 %-PDFs, ohne Locher)
plan = [("Vollsignatur","klein",2),("Vollsignatur","mittel",1),("Vollsignatur","gross",1),
        ("dezimal","klein",1),("dezimal","mittel",1),("dezimal","gross",1),
        ("fortlaufend","klein",2),("fortlaufend","mittel",1),
        ("ohne Signaturen","klein",1),("ohne Signaturen","mittel",1),
        ("römisch/Buchstaben","klein",1),("römisch/Buchstaben","mittel",1),
        ("Mappen/Schachteln","klein",1),("Mappen/Schachteln","mittel",1),
        ("Buchstabe+Nr.",None,1)]
for gl, gr, n in plan:
    pool = sorted([r for r in ok if r["Gliederung"] == gl and (gr is None or r["groesse"] == gr)
                   and f(r["Text erfasst"]) == 1 and not r["Bestand"].startswith("VII.308")
                   and r["PDF"] not in auswahl], key=lambda r: r["PDF"])
    if len(pool) < n:
        print("zu wenig:", gl, gr, len(pool), file=sys.stderr)
    for r in rng.sample(pool, min(n, len(pool))):
        nimm(r, f"C: {gl}, {gr or 'alle Grössen'}")
w = csv.writer(sys.stdout, delimiter=";")
w.writerow(["Nr", "PDF", "Bestand", "Gliederung", "Seiten", "Grösse", "Einheiten", "Status", "Text erfasst", "Schicht"])
for i, (r, g) in enumerate(auswahl.values(), 1):
    w.writerow([i, r["PDF"], r["Bestand"], r["Gliederung"], r["Seiten"], r["groesse"], r["Einheiten"], r["Status"], r["Text erfasst"], g])
