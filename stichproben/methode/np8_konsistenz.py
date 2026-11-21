"""Innere Konsistenz der Hierarchie je Datei: Parent-ID vorhanden und vor dem Kind, Ebene = Eltern + 1,
Übergeordnete Signatur = Signatur der Eltern, Teile unter Teil 1 derselben Signatur, Stufe «Dossier» ohne Kinder
(ausser Teile), Zeitraum der Eltern umfasst die Kinder (nur Jahre, nur Hinweis).
Aufruf: python -I konsistenz.py <ordner> [D ...]"""
import collections, glob, os, re, sys
import openpyxl

o, *nur = sys.argv[1:]
summe = collections.Counter()
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    if nur and d not in nur:
        continue
    rows = list(openpyxl.load_workbook(p, read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    pos = {e["ID"]: i for i, e in enumerate(ee)}
    nach = {e["ID"]: e for e in ee}
    kinder = collections.Counter(e["Parent-ID"] for e in ee if e["Parent-ID"])
    f = collections.defaultdict(list)
    for e in ee:
        pid = e["Parent-ID"]
        if pid in (None, ""):
            if e["Ebene"] not in (1, "1"):
                f["Ebene ohne Eltern ≠ 1"].append(e["Signatur"])
            # (Übergeordnete Signatur ist hier der Bestand – Konvention, kein Fehler)
            continue
        par = nach.get(pid)
        if par is None:
            f["Parent-ID fehlt"].append(e["Signatur"]); continue
        if pos[pid] > pos[e["ID"]]:
            f["Eltern nach dem Kind"].append(e["Signatur"])
        if int(e["Ebene"]) != int(par["Ebene"]) + 1:
            f["Ebene ≠ Eltern+1"].append(f"{e['Signatur']} E{e['Ebene']} unter E{par['Ebene']}")
        if str(e["Übergeordnete Signatur"] or "") != str(par["Signatur"] or ""):
            f["Übergeordnete Signatur ≠ Eltern"].append(f"{e['Signatur']}: {e['Übergeordnete Signatur']} / {par['Signatur']}")
        if e["Teil"] and par["Signatur"] == e["Signatur"] and par["Teil"] not in (None, "", 1, "1"):
            f["Teil nicht unter Teil 1"].append(e["Signatur"])
    for e in ee:
        if e["Stufe"] == "Dossier" and kinder[e["ID"]] and not all(
                k["Signatur"] == e["Signatur"] for k in ee if k["Parent-ID"] == e["ID"]):
            f["Dossier mit Kindern"].append(e["Signatur"])
    if f:
        print(d, {k: len(v) for k, v in f.items()})
        for k, v in f.items():
            print("    ", k, "|", "; ".join(map(str, v[:4])))
            summe[k] += len(v)
print("Summe:", dict(summe))
