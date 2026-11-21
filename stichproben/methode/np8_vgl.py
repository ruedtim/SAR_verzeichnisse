"""Vergleich vorher/nachher einer Datei nach Signatur (normalisiert: ohne «:» und Leerzeichen) und n-tem Vorkommen.
Aufruf: python -I vgl.py <alt> <neu> <D> [breite]
Zeigt WEG/NEU/GEÄNDERT mit allen geänderten Feldern (Darin als Zeilendiff), Eltern als Signatur statt ID."""
import collections, difflib, re, sys
import openpyxl

alt, neu, d = sys.argv[1:4]
br = int(sys.argv[4]) if len(sys.argv) > 4 else 160
OHNE = {"ID", "Parent-ID"}


def norm(s):
    return re.sub(r"[\s:]", "", str(s or ""))


def lade(o):
    rows = list(openpyxl.load_workbook(f"{o}/{d}_scope_import.xlsx", read_only=True)["scope-Import"].iter_rows(values_only=True))
    h = [str(x) for x in rows[0]]
    rr = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    nach_id = {r["ID"]: r for r in rr}
    n, out = collections.Counter(), {}
    for r in rr:
        r["Eltern"] = (nach_id[r["Parent-ID"]]["Signatur"] + (f"/T{nach_id[r['Parent-ID']]['Teil']}" if nach_id[r["Parent-ID"]]["Teil"] else "")) if r["Parent-ID"] in nach_id else "-"
        k = norm(r["Signatur"])
        n[k] += 1
        out[(k, n[k])] = r
    return h, out, rr


h, a, ra = lade(alt)
_, b, rb = lade(neu)
print(f"### {d}: vorher {len(ra)} Einheiten, nachher {len(rb)} Einheiten")
felder = [c for c in h if c not in OHNE] + ["Eltern"]


def kurz(r):
    return (f"{r['Signatur']}{'/T' + str(r['Teil']) if r['Teil'] else ''} [ID {r['ID']}, {r['Stufe']}, E{r['Ebene']}, "
            f"Eltern {r['Eltern']}, S.{r['PDF-Seite']}] {str(r['Titel'])[:br]} | {r['Entstehungszeitraum'] or ''}")


for k in a:
    if k not in b:
        r = a[k]
        print("WEG ", kurz(r))
        if r["Darin"]:
            for z in str(r["Darin"]).split("\n")[:8]:
                print("        D:", z[:br])
            if str(r["Darin"]).count("\n") >= 8:
                print(f"        D: … ({str(r['Darin']).count(chr(10)) + 1} Zeilen)")
for k in b:
    if k not in a:
        r = b[k]
        print("NEU ", kurz(r))
        if r["Darin"]:
            for z in str(r["Darin"]).split("\n")[:8]:
                print("        D:", z[:br])
            if str(r["Darin"]).count("\n") >= 8:
                print(f"        D: … ({str(r['Darin']).count(chr(10)) + 1} Zeilen)")
        if r["Prüfhinweise"]:
            print("        H:", str(r["Prüfhinweise"])[:300])
for k in a:
    if k not in b:
        continue
    x, y = a[k], b[k]
    diffs = [c for c in felder if x.get(c) != y.get(c)]
    if not diffs:
        continue
    print("GEÄ ", kurz(y))
    for c in diffs:
        xs, ys = str(x.get(c) or ""), str(y.get(c) or "")
        if c == "Darin" or "\n" in xs or "\n" in ys:
            print(f"        [{c}]")
            for z in list(difflib.unified_diff(xs.split("\n"), ys.split("\n"), lineterm="", n=0))[2:]:
                if z.startswith("@@"):
                    continue
                print("          ", z[:br])
        else:
            print(f"        {c}: {xs[:br]!r} => {ys[:br]!r}")
