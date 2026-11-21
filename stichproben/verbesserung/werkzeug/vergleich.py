"""Einheitenvergleich zweier Läufe (gleiche IDs): geänderte Felder je Einheit, Art der Zeitraum-Änderung.
Aufruf: python -I vergleich.py <alt> <neu> <ausgabe.csv>"""
import csv, glob, os, re, sys, collections, openpyxl
alt, neu, aus = sys.argv[1:4]
def lies(p):
    wb = openpyxl.load_workbook(p, read_only=True)
    ws = wb["scope-Import"]
    rows = list(ws.iter_rows(values_only=True))
    kopf = [str(k) for k in rows[0]]
    einh = {r[0]: dict(zip(kopf, r)) for r in rows[1:] if r and r[0] is not None}
    pl = {}
    if "Prüfliste" in wb.sheetnames:
        prow = list(wb["Prüfliste"].iter_rows(values_only=True))
        pk = [str(k) for k in prow[0]] if prow else []
        for r in prow[1:]:
            d = dict(zip(pk, r))
            if d.get("ID") is not None:
                pl[d["ID"]] = d
    return kopf, einh, pl
def j(s):
    m = re.search(r"(\d{4})", str(s or "")); return int(m.group(1)) if m else None
def schl(s, ende=False):
    s = str(s or "")
    m = re.fullmatch(r"(?:(\d{2})\.)?(?:(\d{2})\.)?(\d{4})", s)
    if not m: return None
    t, mo, y = m.group(1), m.group(2), m.group(3)
    if t and not mo: mo, t = t, None
    return (int(y), int(mo) if mo else (12 if ende else 1), int(t) if t else (31 if ende else 1))
zeilen, arten, dateien = [], collections.Counter(), 0
for pa in sorted(glob.glob(f"{alt}/*_scope_import.xlsx")):
    name = os.path.basename(pa)
    if name.startswith("uebersicht"): continue
    pn = f"{neu}/{name}"
    ka, ea, pla = lies(pa); kn, en, pln = lies(pn)
    geaendert = False
    for i in sorted(set(ea) | set(en)):
        a, n = ea.get(i), en.get(i)
        if a is None or n is None or a.get("Signatur") != n.get("Signatur"):
            zeilen.append(dict(pdf=name[:-18], id=i, signatur=(a or n).get("Signatur"), art="Struktur", felder="", alt="", neu=""))
            arten["Struktur"] += 1; geaendert = True; continue
        felder = [k for k in ka if a.get(k) != n.get(k)]
        ha, hn = (pla.get(i) or {}), (pln.get(i) or {})
        pf = [k for k in set(ha) | set(hn) if k not in ("ID",) and ha.get(k) != hn.get(k)]
        if not felder and not pf: continue
        geaendert = True
        art = ""
        if "von" in felder or "bis" in felder:
            va, vn = schl(a.get("von")), schl(n.get("von"))
            ba, bn = schl(a.get("bis") or a.get("von"), True), schl(n.get("bis") or n.get("von"), True)
            frueher = va and vn and vn < va; spaeter = ba and bn and bn > ba
            enger = (va and vn and vn > va) or (ba and bn and bn < ba)
            art = "weiter" if (frueher or spaeter) and not enger else "enger" if enger and not (frueher or spaeter) else "anders"
            if not (a.get("von") or a.get("bis")): art = "neu"
            if not (n.get("von") or n.get("bis")): art = "weg"
        elif felder:
            art = "nur " + "/".join(felder)
        else:
            art = "nur Prüfliste"
        arten[art] += 1
        zeilen.append(dict(pdf=name[:-18], id=i, signatur=a.get("Signatur"), art=art, felder="/".join(felder + ["P:" + k for k in pf]),
                           alt=f"{a.get('von') or ''}–{a.get('bis') or ''} [{a.get('Entstehungszeitraum, Anm.') or ''}]",
                           neu=f"{n.get('von') or ''}–{n.get('bis') or ''} [{n.get('Entstehungszeitraum, Anm.') or ''}]"))
    dateien += geaendert
with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "id", "signatur", "art", "felder", "alt", "neu"], delimiter=";")
    w.writeheader(); w.writerows(zeilen)
print("Dateien geändert:", dateien, "| Einheiten:", len(zeilen), dict(arten.most_common()))
