"""Umbrochene Datumsspanne in der Datumsspalte: PDF-Zeile endet mit «1953 –», die nächste Zeile ist nur «1956» (rechte
Spalte). Steht die Spanne a–b irgendwo in der Excel derselben Datei (Text «a – b», «a–b», «a-b» oder von/bis = a/b)?
Aufruf: python -I datumsumbruch.py <cache> <ordner> [D ...]   (ohne D: alle Dateien des Ordners)"""
import collections, glob, json, os, re, sys
import openpyxl

cache, o, *nur = sys.argv[1:]
START = re.compile(r"(1[5-9]\d\d|20\d\d)\s*[–-]$")
ENDE = re.compile(r"^(1[5-9]\d\d|20\d\d)$")
gesamt = collections.Counter()
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    if nur and d not in nur:
        continue
    try:
        zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    except FileNotFoundError:
        continue
    paare = []
    for i in range(len(zz) - 1):
        t = " ".join(w[0] for w in zz[i]["worte"])
        n = " ".join(w[0] for w in zz[i + 1]["worte"])
        m, e = START.search(t), ENDE.match(n.strip())
        ww = zz[i]["worte"]
        xs = ww[-2][1] if len(ww) > 1 and ww[-1][0] in ("–", "-") else ww[-1][1]
        if m and e and zz[i + 1]["worte"][0][1] > 300 and abs(zz[i + 1]["worte"][0][1] - xs) < 25:
            paare.append((zz[i]["seite"], m.group(1), e.group(1), t[-70:]))
    if not paare:
        continue
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    text = "\n".join(str(e[k] or "") for e in ee for k in ("Titel", "Darin", "Entstehungszeitraum, Anm.", "Umfang"))
    vb = {(str(e["von"] or "")[-4:], str(e["bis"] or "")[-4:]) for e in ee}
    fehlt = [x for x in paare if not re.search(rf"{x[1]}\s*[–-]\s*(?:\n\s*)?{x[2]}", text) and (x[1], x[2]) not in vb]
    gesamt["Paare"] += len(paare)
    gesamt["ohne Spanne"] += len(fehlt)
    if fehlt:
        gesamt["Dateien"] += 1
        print(f"{d}: {len(fehlt)} von {len(paare)} ohne Spanne, z. B. " + "; ".join(f"S.{s} «…{t[-45:]}» / «{b}»" for s, a, b, t in fehlt[:2]))
print(dict(gesamt))
