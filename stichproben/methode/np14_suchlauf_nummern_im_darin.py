"""Suchlauf «Nummern im Darin» (NP14, Muster D151150/K144): Läufe von mindestens drei PDF-Zeilen, die in der Signaturspalte mit
einer Nummer beginnen, keine Einheit sind und zwischen zwei Einheiten stehen. Ihr Text steht dann meist im Darin der vorigen
Einheit, obwohl es eigene Einheiten sein müssten (Nummern, die wie Jahreszahlen aussehen; Nummern ohne Punkt; Signaturform nicht
erkannt). Nur Läufe, deren Nummern steigen und grösser sind als die letzte Stelle der vorigen Einheit (Fortsetzung der
Signaturfolge, nicht eine eigene Liste «1., 2., 3.» im Darin); Datumszeilen («22. Oktober …») zählen nicht. Gemeldet wird je Lauf: Datei, vorige Einheit, Zahl der Zeilen, erste und letzte Zeile.
Signaturspalte = x der Signaturzeilen der Datei (häufigste x-Positionen der verankerten Einheiten, ±3 pt).
Aufruf: python -I suchlauf_nummern_im_darin.py <cache> <excel_ordner> <aus.csv> [min_lauf]"""
import collections, csv, glob, json, os, re, sys
import openpyxl

cache, o, aus = sys.argv[1:4]
MIN = int(sys.argv[4]) if len(sys.argv) > 4 else 3
NUM = re.compile(r"^\d{1,5}[a-z]?\.?$")


def nrn(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    if not os.path.exists(f"{cache}/{d}.zeilen.json"):
        continue
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    seiten = collections.defaultdict(list)
    for i, z in enumerate(zz):
        if z["worte"]:
            seiten[z["seite"]].append(i)
    belegt, pos = set(), {}
    for streng in (True, False, "letzte"):
        for e in ee:
            nr = nrn(e.get("Nr. im PDF"))
            if streng == "letzte":   # «9.144.» in «Nr. im PDF», im PDF nur «144» (D151150)
                nr = nr.split(".")[-1] if "." in nr else ""
            if not nr or e["ID"] in pos:
                continue
            for i in seiten.get(e.get("PDF-Seite"), []):
                if i in belegt:
                    continue
                kette = ""
                for w in zz[i]["worte"][:6]:
                    kette += re.sub(r"\s+", "", w[0])
                    if len(kette) >= len(nr):
                        break
                ok = (kette.startswith(nr) and re.fullmatch(r"[.):,;\]]*", kette[len(nr):]) is not None) if streng in (True, "letzte") else \
                    (kette.startswith(nr) and not re.match(r"\.?\d", kette[len(nr):]))
                if ok:
                    pos[e["ID"]] = i; belegt.add(i); break
    if len(pos) < 3:
        continue
    xs = collections.Counter(round(zz[i]["worte"][0][1]) for i in pos.values())
    spalten = [x for x, c in xs.items() if c >= max(2, len(pos) // 20)]
    anker = sorted((i, eid) for eid, i in pos.items())
    groesse = sorted(zz[i]["worte"][0][4] for i in pos.values())[len(pos) // 2]   # Schriftgrösse der Signaturzeilen (Median)
    idx = {e["ID"]: e for e in ee}
    for (i1, eid), (i2, _) in zip(anker, anker[1:] + [(len(zz), None)]):
        lauf = []
        for i in range(i1 + 1, i2):
            w = zz[i]["worte"]
            if not w or i in belegt or zz[i]["top"] < 60 or zz[i]["top"] > 800:
                continue
            text = " ".join(x[0] for x in w)
            if re.search(r"\.{5,}|…{2,}", text) or w[0][4] < groesse - 1:
                continue   # Inhaltsverzeichnis mit Punktlinie, Fussnote in kleinerer Schrift
            if NUM.match(w[0][0]) and any(abs(w[0][1] - x) <= 3 for x in spalten) and len(w) >= 2:
                lauf.append(i)
        if len(lauf) >= MIN:
            e = idx[eid]
            # nur Läufe, die die Nummer der vorigen Einheit fortsetzen (nicht eine eigene Liste «1., 2., 3.» im Darin)
            mm = re.search(r"(\d+)[a-z]?\.?$", str(e["Signatur"] or ""))
            n0 = int(mm.group(1)) if mm else None
            zahlen = [int(re.match(r"\d+", zz[i]["worte"][0][0]).group(0)) for i in lauf]
            steigend = sum(b > a for a, b in zip(zahlen, zahlen[1:])) >= 0.9 * (len(zahlen) - 1)
            monat = re.compile(r"^(Jan|Feb|Mär|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)", re.I)
            datum = sum(1 for i in lauf if len(zz[i]["worte"]) > 1 and monat.match(zz[i]["worte"][1][0])) > len(lauf) / 3
            if n0 is None or zahlen[0] <= n0 or not steigend or datum:
                continue
            t = lambda i: " ".join(x[0] for x in zz[i]["worte"])[:80]
            out.append({"datei": d, "vorige_einheit": f"{eid} {e['Signatur']}", "zeilen": len(lauf),
                        "seiten": f"{zz[lauf[0]]['seite']}–{zz[lauf[-1]]['seite']}", "erste": t(lauf[0]), "letzte": t(lauf[-1])})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "vorige_einheit", "zeilen", "seiten", "erste", "letzte"], delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Läufe in", len({x["datei"] for x in out}), "Dateien")
