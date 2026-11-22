"""Suchlauf «Nummer mit Kleinbuchstabe» (3a., 1937.524a, 430.1.733.1a, 730a): PDF-Zeilen, deren erstes Wort so aussieht,
an einer x-Position der Signaturspalten der Datei (±3 pt), ohne Einheit mit dieser Nr. im PDF.
Aufruf: python -I buchstabe_scan.py <cache> <ordner> <aus.csv>"""
import collections, csv, glob, json, os, re, sys
import openpyxl
cache, o, aus = sys.argv[1:4]
PAT = re.compile(r"^\d{1,4}(?:\.\d{1,4})*[a-h]\.?$")
def norm(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")
out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    try:
        zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    except FileNotFoundError:
        continue
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    nrs = {norm(e["Nr. im PDF"]) for e in ee}
    seiten = collections.defaultdict(list)
    for z in zz:
        if z["worte"]:
            seiten[z["seite"]].append(z)
    xs = collections.Counter()
    for e in ee:
        nr = norm(e["Nr. im PDF"])
        for z in seiten.get(e["PDF-Seite"], []):
            if norm(z["worte"][0][0]) == nr:
                xs[round(z["worte"][0][1])] += 1
                break
    spalten = [x for x, n in xs.items() if n >= 2]
    for z in zz:
        if not z["worte"]:
            continue
        w0 = z["worte"][0]
        if not PAT.match(w0[0]) or not any(abs(w0[1] - x) <= 3 for x in spalten):
            continue
        if norm(w0[0]) in nrs:
            continue
        text = " ".join(w[0] for w in z["worte"])
        darin = ""
        probe = " ".join(w[0] for w in z["worte"][1:4])
        for e in ee:
            if probe and probe in str(e["Darin"] or ""):
                darin = f"{e['Signatur']} (ID {e['ID']})"; break
        out.append({"datei": d, "seite": z["seite"], "x": round(w0[1]), "groesse": w0[4] if len(w0) > 4 else "", "zeile": text[:110], "im_darin_von": darin})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "seite", "x", "groesse", "zeile", "im_darin_von"], delimiter=";")
    w.writeheader(); w.writerows(out)
c = collections.Counter(x["datei"] for x in out)
print(len(out), "Zeilen in", len(c), "Dateien")
for x in out:
    print(f"{x['datei']:<8} S.{x['seite']:<3} x{x['x']:<4} {str(x['groesse']):<5} {x['zeile'][:80]:<80} | {x['im_darin_von']}")
