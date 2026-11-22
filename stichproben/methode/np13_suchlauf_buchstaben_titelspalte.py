"""Suchlauf «Buchstaben in der Titelspalte» (NP13, nach dem Entscheid der Hauptsession vom 22.11.2026): a)–h) in der
Titelspalte einer Gruppe sind Darin-Einträge der Gruppe, auch mit eigenem Datum; eigene Einheiten nur in einer eigenen Spalte.
Gemeldet wird jede Einheit, deren Signatur auf einen Buchstaben endet und deren Buchstabe im PDF dort steht, wo bei der
übergeordneten Einheit der Titel beginnt (±4 pt), statt in der Signaturspalte.
Aufruf: python -I suchlauf_buchstaben_titelspalte.py <cache> <excel_ordner> <aus.csv>"""
import collections, csv, glob, json, os, re, sys
import openpyxl

cache, o, aus = sys.argv[1:4]
out = []


def nrn(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    if not os.path.exists(f"{cache}/{d}.zeilen.json"):
        continue
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    if not any(re.search(r"[.:\s][a-h][.)]?$", str(e["Signatur"] or "")) for e in ee):
        continue
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    seiten = collections.defaultdict(list)
    for i, z in enumerate(zz):
        if z["worte"]:
            seiten[z["seite"]].append(i)
    idx = {e["ID"]: e for e in ee}
    belegt, pos = set(), {}
    for e in ee:
        nr = nrn(e.get("Nr. im PDF"))
        if not nr or e.get("Teil"):
            continue
        for i in seiten.get(e.get("PDF-Seite"), []):
            if i in belegt:
                continue
            kette = ""
            for w in zz[i]["worte"][:6]:
                kette += re.sub(r"\s+", "", w[0])
                if len(kette) >= len(nr):
                    break
            if kette.startswith(nr) and re.fullmatch(r"[.):,;\]]*", kette[len(nr):]):
                pos[e["ID"]] = i; belegt.add(i); break
    for e in ee:
        s = str(e["Signatur"] or "")
        if not re.search(r"[.:\s][a-h][.)]?$", s) or e["ID"] not in pos:
            continue
        par = idx.get(e.get("Parent-ID"))
        if not par or par["ID"] not in pos:
            continue
        wl, wp = zz[pos[e["ID"]]]["worte"], zz[pos[par["ID"]]]["worte"]
        if len(wp) < 2:
            continue
        x_buchst, x_sig, x_titel = wl[0][1], wp[0][1], wp[1][1]
        if abs(x_buchst - x_titel) <= 4 and abs(x_buchst - x_sig) > 4:
            out.append({"datei": d, "id": e["ID"], "signatur": s, "titel": str(e.get("Titel") or "")[:70],
                        "eltern": f"{par['ID']} {par['Signatur']}", "seite": e.get("PDF-Seite"),
                        "x_buchstabe": round(x_buchst), "x_titel_eltern": round(x_titel), "x_signatur_eltern": round(x_sig)})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "id", "signatur", "titel", "eltern", "seite", "x_buchstabe", "x_titel_eltern",
                                      "x_signatur_eltern"], delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Einheiten in", len({x["datei"] for x in out}), "Dateien:", dict(collections.Counter(x["datei"] for x in out)))
