"""Suchlauf «Behälter-Verschiebung» (Muster D2363/D814): In Findmitteln ohne Signaturen, deren Einheiten aus Schachtel-
oder Mappennummern gebildet sind, gehört eine Folgezeile ohne Nummer zur Gruppe der Zeile darüber, wenn sie dicht darunter
steht (Zeilenabstand) und die nächste Nummernzeile weiter entfernt ist. Gemeldet wird eine Einheit, deren Titel mit so
einer Folgezeile beginnt (dann hat sie den Text der vorigen Schachtel).
Aufruf: python -I behaelter_scan.py <cache> <ordner> <aus.csv>"""
import collections, csv, glob, json, os, re, sys
import openpyxl
cache, o, aus = sys.argv[1:4]
def norm(s):
    return re.sub(r"\W+", "", str(s or "")).lower()
out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    beh = [e for e in ee if "Nummer der Schachtel" in str(e["Prüfhinweise"] or "") or "Nummer der Mappe" in str(e["Prüfhinweise"] or "")
           or re.match(r"(Schachtel|Mappe|Karton|Band)\s*\d", str(e["Nr. im PDF"] or ""))]
    if len(beh) < 3:
        continue
    try:
        zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    except FileNotFoundError:
        continue
    seiten = collections.defaultdict(list)
    for z in zz:
        if z["worte"]:
            seiten[z["seite"]].append(z)
    for e in beh:
        t = norm(e["Titel"])[:25]
        if len(t) < 8:
            continue
        zl = seiten.get(e["PDF-Seite"], [])
        for i, z in enumerate(zl):
            txt = norm(" ".join(w[0] for w in z["worte"]))
            if not txt.startswith(t[:20]):
                continue
            # Zeile mit Titelanfang: trägt sie selbst eine Nummer am Ende?
            letzte = z["worte"][-1][0]
            if re.fullmatch(r"\d{1,3}[a-z]?", letzte):
                break
            if i == 0:
                break
            oben, unten = zl[i - 1], (zl[i + 1] if i + 1 < len(zl) else None)
            d_oben = z["top"] - oben["top"]
            d_unten = (unten["top"] - z["top"]) if unten else 99
            oben_nr = re.fullmatch(r"\d{1,3}[a-z]?", oben["worte"][-1][0])
            if oben_nr and d_oben + 3 < d_unten:
                out.append({"datei": d, "id": e["ID"], "signatur": e["Signatur"], "seite": e["PDF-Seite"],
                            "titel": str(e["Titel"])[:60], "zeile_oben": " ".join(w[0] for w in oben["worte"])[:70],
                            "abstand_oben": round(d_oben, 1), "abstand_unten": round(d_unten, 1)})
            break
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "id", "signatur", "seite", "titel", "zeile_oben", "abstand_oben", "abstand_unten"], delimiter=";")
    w.writeheader(); w.writerows(out)
c = collections.Counter(x["datei"] for x in out)
print(len(out), "Verdachtsfälle in", len(c), "Dateien:", dict(c.most_common()))
for x in out[:40]:
    print(f"  {x['datei']:<8} ID {x['id']:<4} {x['signatur']:<22} | {x['titel'][:40]:<40} | oben: {x['zeile_oben'][:45]} ({x['abstand_oben']}/{x['abstand_unten']})")
