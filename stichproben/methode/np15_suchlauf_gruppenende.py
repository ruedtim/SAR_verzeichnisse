"""Suchlauf «Gruppenende» (NP14, Muster D2620/K196): Eine Zeile oder ein Block nach der letzten Untereinheit einer Gruppe, mit
grösserem Abstand als zwischen den Einträgen, steht im Darin der letzten Untereinheit. Oft gehört er zur ganzen Gruppe
(«Bibliographische und andere Notizen (1 Mäpplein)»), seltener zur Untereinheit. Gemeldet wird der Block zur Sichtung.
Bedingungen:
  - Die Gruppe g hat Untereinheiten; die letzte Untereinheit c (in PDF-Folge) liegt vor der nächsten Einheit gleicher oder
    höherer Ebene.
  - Zwischen der Signaturzeile von c und dieser nächsten Einheit gibt es eine Zeile mit einem Abstand nach oben, der grösser ist
    als das 1,3-fache des üblichen Abstands vor einem neuen Eintrag, und ihr Text steht im Darin von c.
NP15: Faktor als 4. Argument (Vorgabe 1,3); mit 1,0 kommen die Fälle mit gleichem Abstand wie zwischen den Einträgen dazu
(D3099/K205, D151210/K208 waren solche Grenzfälle).
Aufruf: python -I suchlauf_gruppenende.py <cache> <excel_ordner> <aus.csv> [faktor]"""
import collections, csv, glob, json, os, re, statistics, sys
import openpyxl

cache, o, aus = sys.argv[1:4]
FAKTOR = float(sys.argv[4]) if len(sys.argv) > 4 else 1.3


def nrn(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


def norm(s):
    return re.sub(r"[^0-9a-zäöüß]", "", str(s or "").lower())


out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    if not os.path.exists(f"{cache}/{d}.zeilen.json"):
        continue
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    if len(ee) < 3:
        continue
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    seiten = collections.defaultdict(list)
    for i, z in enumerate(zz):
        if z["worte"]:
            seiten[z["seite"]].append(i)
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
    if len(pos) < 3:
        continue
    idx = {e["ID"]: e for e in ee}
    kinder = collections.defaultdict(list)
    for e in ee:
        if e.get("Parent-ID") in idx and not e.get("Teil"):
            kinder[e["Parent-ID"]].append(e)
    # üblicher Abstand vor einem neuen Eintrag
    abst = []
    for i in pos.values():
        j = i - 1
        while j >= 0 and not zz[j]["worte"]:
            j -= 1
        if j >= 0 and zz[j]["seite"] == zz[i]["seite"]:
            abst.append(zz[i]["top"] - zz[j]["top"])
    if not abst:
        continue
    ueblich = statistics.median(abst)
    reihe = sorted((i, eid) for eid, i in pos.items())
    stelle = {eid: k for k, (i, eid) in enumerate(reihe)}

    def nachfahre(x, g):
        while x and x.get("Parent-ID") in idx:
            if x["Parent-ID"] == g:
                return True
            x = idx[x["Parent-ID"]]
        return False

    for g in ee:
        if g["ID"] not in pos or not kinder.get(g["ID"]):
            continue
        k = stelle[g["ID"]]
        ende = len(zz)
        letzte = None
        for (i, eid) in reihe[k + 1:]:
            x = idx[eid]
            if nachfahre(x, g["ID"]):
                letzte = (i, x)
                continue
            ende = i
            break
        if not letzte:
            continue
        i_c, c = letzte
        darin = norm(c.get("Darin"))
        if not darin:
            continue
        vor = i_c
        for i in range(i_c + 1, ende):
            z = zz[i]
            if not z["worte"] or z["top"] < 60 or z["top"] > 800:
                continue
            if zz[vor]["seite"] == z["seite"]:
                gap = z["top"] - zz[vor]["top"]
                text = " ".join(w[0] for w in z["worte"])
                if gap > FAKTOR * ueblich and len(norm(text)) >= 8 and norm(text) in darin:
                    out.append({"datei": d, "gruppe": f"{g['ID']} {g['Signatur']}", "letzte_untereinheit": f"{c['ID']} {c['Signatur']}",
                                "seite": z["seite"], "y": round(z["top"]), "abstand": round(gap, 1), "ueblich": round(ueblich, 1),
                                "zeile": text[:100]})
                    break
            vor = i
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "gruppe", "letzte_untereinheit", "seite", "y", "abstand", "ueblich", "zeile"],
                       delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Kandidaten in", len({x["datei"] for x in out}), "Dateien")
