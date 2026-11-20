"""Vergleicht zwei Stände einer *_scope_import.xlsx (alt = 21:02, neu = 23:05) Einheit für Einheit.

Nur lesen. Aufruf:
  uv run --with openpyxl python -I diff_stand.py ALT.xlsx NEU.xlsx [--seiten 5,7,9 | --seiten alle] [--stat]

Ausgabe: je Einheit, die sich geändert hat, ein Block
  = unverändert (nur gezählt)
  ~ geändert    (Kopfzeile neu, darunter die geänderten Zeilen mit - alt / + neu)
  - entfernt    (nur im alten Stand)
  + neu         (nur im neuen Stand)
Abgleich über die Folge der Schlüssel (Signatur, Teil). IDs und Parent-IDs werden durch die Signatur der
Elterneinheit ersetzt, damit verschobene IDs keine Unterschiede erzeugen. Prüfhinweise werden nicht verglichen.
Mit --seiten werden nur Einheiten berücksichtigt, die auf diesen PDF-Seiten beginnen (alt: alte Seite,
neu: neue Seite), plus jeweils die letzte Einheit vor einer Prüfseite (läuft evtl. hinein).
"""
import sys, argparse, difflib, openpyxl

ap = argparse.ArgumentParser()
ap.add_argument("alt"); ap.add_argument("neu")
ap.add_argument("--seiten", default="alle")
ap.add_argument("--stat", action="store_true")
a = ap.parse_args()


def s(v):
    return "" if v is None else str(v)


def lies(pfad):
    wb = openpyxl.load_workbook(pfad, read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    kopf = [str(h) for h in rows[0]]
    daten = [dict(zip(kopf, r)) for r in rows[1:] if any(v is not None for v in r)]
    nach_id = {s(d["ID"]): d for d in daten}
    for d in daten:
        p = nach_id.get(s(d.get("Parent-ID")))
        d["_psig"] = (s(p["Signatur"]) + (f" (Teil {s(p['Teil'])})" if p and p.get("Teil") not in (None, "") else "")) if p else ""
    return daten


def seite(d):
    try:
        return int(d.get("PDF-Seite"))
    except (TypeError, ValueError):
        return None


def filtere(daten, seiten):
    if seiten is None:
        return daten
    keep = set()
    for i, d in enumerate(daten):
        if seite(d) in seiten:
            keep.add(i)
    # letzte Einheit vor jeder Prüfseite
    for p in seiten:
        vor = [i for i, d in enumerate(daten) if seite(d) is not None and seite(d) < p]
        if vor:
            keep.add(vor[-1])
    return [daten[i] for i in sorted(keep)]


def block(d):
    zr = ""
    if d.get("Entstehungszeitraum"):
        op = "=" if s(d["Entstehungszeitraum"]).startswith("Genau") else "von/bis"
        zr = f"{op} {s(d.get('von'))}–{s(d.get('bis'))}"
    kopf = [f"Sig [{s(d['Signatur'])}]", f"Stufe {s(d['Stufe'])}", f"Eb {s(d['Ebene'])}"]
    if d.get("Teil") not in (None, ""):
        kopf.append(f"Teil {s(d['Teil'])}")
    kopf.append(f"Über [{s(d['Übergeordnete Signatur'])}]")
    if d["_psig"] != s(d["Übergeordnete Signatur"]):
        kopf.append(f"Parent-Sig [{d['_psig']}]")
    if zr:
        kopf.append(f"Zeit {zr}")
    for k, n in (("Entstehungszeitraum, Anm.", "Anm"), ("Umfang", "Umfang"), ("Schachtel-Nr.", "Schachtel")):
        if d.get(k):
            kopf.append(f"{n} [{s(d[k])}]")
    kopf.append(f"NrPDF [{s(d.get('Nr. im PDF'))}]")
    kopf.append(f"S. {s(d.get('PDF-Seite'))}")
    if d.get("Zeitraum-Quelle"):
        kopf.append(f"Quelle {s(d['Zeitraum-Quelle'])}")
    zeilen = [" | ".join(kopf), f"TITEL: {s(d['Titel'])}"]
    darin = s(d.get("Darin"))
    if darin:
        zeilen += [f"• {z}" for z in darin.split("\n")]
    if d.get("Verwandte Verzeichnungseinheiten"):
        zeilen.append(f"VERWANDTE: {s(d['Verwandte Verzeichnungseinheiten'])}")
    return zeilen


alt, neu = lies(a.alt), lies(a.neu)
seiten = None if a.seiten == "alle" else {int(x) for x in a.seiten.split(",") if x.strip()}
fa, fn = filtere(alt, seiten), filtere(neu, seiten)
ka = [(s(d["Signatur"]), s(d.get("Teil"))) for d in fa]
kn = [(s(d["Signatur"]), s(d.get("Teil"))) for d in fn]
sm = difflib.SequenceMatcher(a=ka, b=kn, autojunk=False)
zahl = {"=": 0, "~": 0, "-": 0, "+": 0}
aus = []
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal":
        for x, y in zip(fa[i1:i2], fn[j1:j2]):
            bx, by = block(x), block(y)
            if bx == by:
                zahl["="] += 1
                continue
            zahl["~"] += 1
            aus.append(f"~ GEÄNDERT  ID neu {s(y['ID'])} (alt {s(x['ID'])})")
            if bx[0] == by[0]:
                aus.append("    " + by[0])
            for z in difflib.unified_diff(bx, by, lineterm="", n=0):
                if z.startswith(("---", "+++", "@@")):
                    continue
                aus.append("    " + z)
    else:
        for x in fa[i1:i2]:
            zahl["-"] += 1
            aus.append(f"- ENTFERNT  ID alt {s(x['ID'])}")
            aus += ["    " + z for z in block(x)]
        for y in fn[j1:j2]:
            zahl["+"] += 1
            aus.append(f"+ NEU       ID neu {s(y['ID'])}")
            aus += ["    " + z for z in block(y)]
print(f"# {a.neu.split('/')[-1]}  Seiten: {a.seiten}  alt {len(fa)} / neu {len(fn)} Einheiten  "
      f"unverändert {zahl['=']}, geändert {zahl['~']}, entfernt {zahl['-']}, neu {zahl['+']}")
if not a.stat:
    print("\n".join(aus))
