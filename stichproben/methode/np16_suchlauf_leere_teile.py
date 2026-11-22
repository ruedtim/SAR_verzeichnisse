"""Suchlauf «leere Teile» (NP16, Muster K220 D845): Eine Signatur steht zuerst in einer Übersicht (erste Nennung, sie bekommt die
Untereinheiten) und später noch einmal als fetter Kopf eines Unterverzeichnisses. Der Kopf wird dann ein Teil ohne Darin und ohne
Kinder, und die Untereinheiten stehen im PDF erst nach diesem Kopf.
Gemeldet werden:
  KOPF  Teil ohne Darin und ohne Kinder; die erste Nennung steht auf einer früheren Seite und hat eigene Untereinheiten (ohne
        Teile), von denen mindestens 80 % im PDF auf oder nach der Seite des Teils stehen.
  LEER  übrige Teile ohne Darin, ohne Kinder, ohne Schachtel, ohne Zeitraum und ohne Umfang (zur Sichtung; Titel «[leer]» aus dem
        PDF zählt nicht).
Aufruf: python -I suchlauf_leere_teile.py <excel_ordner> <aus.csv>"""
import collections, csv, glob, os, sys
import openpyxl

o, aus = sys.argv[1:3]
out = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    idx = {e["ID"]: e for e in ee}
    kinder = collections.defaultdict(list)
    for e in ee:
        if e.get("Parent-ID") in idx:
            kinder[e["Parent-ID"]].append(e)
    for t in ee:
        if not t.get("Teil") or str(t.get("Teil")).strip() in ("", "1"):
            continue
        leer = not str(t.get("Darin") or "").strip() and not kinder.get(t["ID"])
        if not leer:
            continue
        erst = idx.get(t.get("Parent-ID"))
        if erst and erst.get("Signatur") != t.get("Signatur"):
            erst = None
        uk = [k for k in kinder.get(erst["ID"], []) if not k.get("Teil")] if erst else []
        s_t = t.get("PDF-Seite") or 0
        nach = sum(1 for k in uk if (k.get("PDF-Seite") or 0) >= s_t)
        if erst and uk and (erst.get("PDF-Seite") or 0) < s_t and nach >= 0.8 * len(uk):
            art = "KOPF"
        elif not t.get("Schachtel-Nr.") and not t.get("von") and not t.get("bis") and not t.get("Umfang") \
                and "[leer]" not in str(t.get("Titel") or ""):
            art = "LEER"
        else:
            continue
        out.append({"datei": d, "art": art, "id": t["ID"], "signatur": t["Signatur"], "teil": t["Teil"], "seite": s_t,
                    "titel": str(t.get("Titel") or "")[:80], "erste_nennung": f"{erst['ID']} S.{erst.get('PDF-Seite')}" if erst else "",
                    "untereinheiten": len(uk), "davon_nach_dem_teil": nach})
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["datei", "art", "id", "signatur", "teil", "seite", "titel", "erste_nennung", "untereinheiten",
                                      "davon_nach_dem_teil"], delimiter=";")
    w.writeheader(); w.writerows(out)
c = collections.Counter(x["art"] for x in out)
print(len(out), "Teile:", dict(c), "| KOPF in", sorted({x["datei"] for x in out if x["art"] == "KOPF"}), "| LEER in", len({x["datei"] for x in out if x["art"] == "LEER"}), "Dateien")
