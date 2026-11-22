"""Suchlauf «Signatur ohne Einheit» über alle Dateien (Muster D3470 «1937.524a», D140969 «50a»).
Eine PDF-Zeile ist Kandidat, wenn
  - ihr erstes Wort an der x-Position der Signaturspalte steht (±3 pt, Spalte aus den Einheiten der Datei),
  - es dieselbe Form hat wie die Nummern der Einheiten (Ziffern → 9, Kleinbuchstaben → a; dazu Form + «a»),
  - es kein Datum ist und auf dieser Seite keine Einheit mit dieser Nummer steht,
  - und es in der Reihenfolge zwischen die vorige und die nächste Einheit passt («in Folge»).
Dann wird gesucht, wo der Text der Zeile in der Excel steht (Darin welcher Einheit, Blatt Vollständigkeit, nirgends).
Aufruf: python -I darin_signatur.py <cache> <ordner> <aus.csv> [D ...]"""
import collections, csv, glob, json, os, re, sys
import openpyxl

cache, o, aus, *nur = sys.argv[1:]
DATUM = re.compile(r"^\d{1,2}\.\d{1,2}\.(\d{2}|\d{4})$|^\d{1,2}\.\d{4}$|^(1[2-9]|20)\d\d$")


def norm(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


def form(t):
    t = re.sub(r"\d+", "9", norm(t))
    t = re.sub(r"[a-z]+", "a", t)
    return t


def schluessel(t):
    k = []
    for x in re.findall(r"\d+|[a-z]+|[A-Z]+", norm(t)):
        k.append((0, int(x), "") if x.isdigit() else (1, 0, x))
    return k


zeilen_aus = []
dateien = nur or sorted(os.path.basename(p).split("_")[0] for p in glob.glob(f"{o}/D*_scope_import.xlsx"))
for d in dateien:
    try:
        zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    except FileNotFoundError:
        continue
    wb = openpyxl.load_workbook(f"{o}/{d}_scope_import.xlsx", read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    voll = " \n".join(" ".join(str(c) for c in r if c is not None) for r in wb["Vollständigkeit"].iter_rows(values_only=True))
    info = " \n".join(" ".join(str(c) for c in r if c is not None) for r in wb["Info"].iter_rows(values_only=True))
    seiten = collections.defaultdict(list)
    for i, z in enumerate(zz):
        seiten[z["seite"]].append(i)
    # Zeile jeder Einheit finden
    pos = {}
    xs = collections.Counter()
    formen = set()
    for e in ee:
        nr, s = norm(e["Nr. im PDF"]), e["PDF-Seite"]
        if not nr or e["Teil"]:
            continue
        for i in seiten.get(s, []):
            t = norm(" ".join(w[0] for w in zz[i]["worte"][:3]))
            if t.startswith(nr) and not t[len(nr):len(nr) + 1].isdigit() and i not in pos:
                pos[i] = e
                xs[round(zz[i]["worte"][0][1])] += 1
                formen.add(form(zz[i]["worte"][0][0]))
                break
    spalten = [x for x, n in xs.items() if n >= 2]
    if not spalten:
        continue
    formen |= {f + "a" for f in formen}
    belegt = {(zz[i]["seite"], norm(zz[i]["worte"][0][0])) for i in pos}
    reihe = sorted(pos)
    for i, z in enumerate(zz):
        if i in pos or not z["worte"]:
            continue
        w0 = z["worte"][0]
        t = w0[0]
        if not any(abs(w0[1] - x) <= 3 for x in spalten) or form(t) not in formen or DATUM.match(norm(t)):
            continue
        if (z["seite"], norm(t)) in belegt or not re.search(r"\d", t):
            continue
        vor = [j for j in reihe if j < i]
        nach = [j for j in reihe if j > i]
        if not vor:
            continue
        a = pos[vor[-1]]
        b = pos[nach[0]] if nach else None
        ka, kt = schluessel(a["Nr. im PDF"]), schluessel(t)
        kb = schluessel(b["Nr. im PDF"]) if b else None
        in_folge = ka < kt and (kb is None or kt < kb)
        text = " ".join(w[0] for w in z["worte"])
        rw = [w[0] for w in z["worte"][1:]]
        while rw and re.fullmatch(r"[\d–\-/,.]+", rw[-1]):
            rw.pop()
        rest = " ".join(rw)[:40].rstrip(",;")
        wo = "nirgends"
        probe = rest if len(rest) >= 6 else text
        for e in ee:
            if probe and probe in str(e["Darin"] or ""):
                wo = f"Darin von {e['Signatur']} (ID {e['ID']})"
                break
            if probe and probe in str(e["Titel"] or ""):
                wo = f"Titel von {e['Signatur']} (ID {e['ID']})"
                break
        else:
            if probe and probe in voll:
                wo = "Blatt Vollständigkeit"
            elif probe and probe in info:
                wo = "Blatt Info"
        zeilen_aus.append({"datei": d, "seite": z["seite"], "x": round(w0[1]), "zeile": text[:100], "in_folge": "ja" if in_folge else "",
                           "vorige_einheit": a["Signatur"], "naechste_einheit": b["Signatur"] if b else "", "steht_in": wo})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "seite", "x", "zeile", "in_folge", "vorige_einheit", "naechste_einheit", "steht_in"], delimiter=";")
    w.writeheader(); w.writerows(zeilen_aus)
c = collections.Counter(z["datei"] for z in zeilen_aus if z["in_folge"])
print("Kandidaten:", len(zeilen_aus), "davon in Folge:", sum(c.values()), "in", len(c), "Dateien")
for d, n in c.most_common(40):
    print(f"  {d:<8} {n:>4}")
