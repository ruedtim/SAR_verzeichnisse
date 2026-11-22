"""Strukturbericht für grosse Findmittel: listet nur Auffälligkeiten, die auf kritische Fehler deuten können.
  [ELTERN]   Dezimalsignatur, deren Präfix nicht die Signatur der Eltern ist (z. B. 4.2.3. unter 4.1.)
  [LÜCKE]    Sprung in der Nummernfolge unter denselben Eltern (4.2.1., 4.2.2., 4.2.5.)
  [RÜCK]     Nummer kleiner als die vorige unter denselben Eltern
  [DOPPELT]  gleiche Signatur zweimal ohne Teil-Kennung, oder Teil weit weg von Teil 1 (>= 2 Seiten)
  [HINWEIS]  Prüfhinweis zu Struktur/Signatur (übergeordnet, Nummerierung, erneut, Tippfehler, Teil, Überschrift, Stück ohne Nummer)
  [DARIN]    Darin-Zeile, die mit einer Signaturform der Datei beginnt (mögliche Einheit im Darin)
  [OHNE]     Einheit ohne eigene PDF-Zeile (aus der Prüfmappe)
Aufruf: python -I strukturbericht.py <excel_ordner> <mappen_ordner> <aus_ordner> D [D ...]"""
import collections, os, re, sys
import openpyxl

o, mo, aus, *dd = sys.argv[1:]
os.makedirs(aus, exist_ok=True)


def lokal(sig, bestand):
    s = str(sig or "")
    if ":" in s:
        return s.split(":", 1)[1]
    b = str(bestand or "")
    return s[len(b):] if b and s.startswith(b) else s


def teile(l):
    return [x for x in re.split(r"[.\s]+", l.strip(".").strip()) if x]


def zahl(x):
    m = re.match(r"(\d+)", x)
    return int(m.group(1)) if m else None


for d in dd:
    wb = openpyxl.load_workbook(f"{o}/{d}_scope_import.xlsx", read_only=True)
    info = {}
    for x in wb["Info"].iter_rows(values_only=True):
        if x and x[0]:
            info.setdefault(str(x[0]), x[1])
    best = str(info.get("Bestand") or "")
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    idx = {e["ID"]: e for e in ee}
    out = [f"### {d} – {info.get('Gliederung')} – {len(ee)} Einheiten – Bestand {best}"]
    formen = collections.Counter(re.sub(r"\d+", "9", str(e["Nr. im PDF"] or "").strip()) for e in ee if not e.get("Teil"))
    haeufig = {f for f, n in formen.items() if n >= 3}
    zaehler = collections.Counter()
    kinder = collections.defaultdict(list)
    erste = {}
    for e in ee:
        L = lokal(e["Signatur"], best)
        if e.get("Teil"):
            t1 = erste.get(e["Signatur"])
            if t1 and abs((e["PDF-Seite"] or 0) - (t1["PDF-Seite"] or 0)) >= 2:
                out.append(f"[DOPPELT] ID {e['ID']} {e['Signatur']} Teil {e['Teil']} S.{e['PDF-Seite']} – Teil 1 ID {t1['ID']} S.{t1['PDF-Seite']} | {str(e['Titel'])[:60]}")
                zaehler["DOPPELT"] += 1
            continue
        if e["Signatur"] in erste:
            out.append(f"[DOPPELT] ID {e['ID']} {e['Signatur']} ohne Teil, schon ID {erste[e['Signatur']]['ID']} | {str(e['Titel'])[:60]}")
            zaehler["DOPPELT"] += 1
        erste.setdefault(e["Signatur"], e)
        kinder[e["Parent-ID"]].append(e)
        # Eltern-Präfix bei Dezimalsignaturen
        tt = teile(L)
        if len(tt) >= 2 and all(re.fullmatch(r"\d+[a-z]?", x) for x in tt) and e["Parent-ID"]:
            p = idx.get(e["Parent-ID"])
            pl = teile(lokal(p["Signatur"], best)) if p else []
            if p and pl and tt[:len(pl)] != pl and tt[:-1] != pl:
                out.append(f"[ELTERN] ID {e['ID']} {e['Signatur']} unter ID {p['ID']} {p['Signatur']} (S.{e['PDF-Seite']}) | {str(e['Titel'])[:60]}")
                zaehler["ELTERN"] += 1
        hw = str(e.get("Prüfhinweise") or "")
        if re.search(r"übergeordnete Signatur|Nummerierung|erneut auf|Tippfehler|Stück ohne Nummer|Überschrift|nach der letzten Einheit", hw, re.I):
            out.append(f"[HINWEIS] ID {e['ID']} {e['Signatur']} S.{e['PDF-Seite']} | {hw[:140].replace(chr(10), ' / ')}")
            zaehler["HINWEIS"] += 1
        for i, dz in enumerate(str(e.get("Darin") or "").split("\n")):
            w = dz.strip().split(" ")[0] if dz.strip() else ""
            if w and re.sub(r"\d+", "9", w) in haeufig and re.search(r"\d", w):
                out.append(f"[DARIN] ID {e['ID']} {e['Signatur']} Darin {i + 1}: {dz[:100]}")
                zaehler["DARIN"] += 1
    for pid, ks in kinder.items():
        vor = None
        for e in ks:
            tt = teile(lokal(e["Signatur"], best))
            n = zahl(tt[-1]) if tt else None
            if n is None:
                vor = None
                continue
            if vor is not None:
                if n < vor:
                    out.append(f"[RÜCK] ID {e['ID']} {e['Signatur']} nach Nummer {vor} (Eltern {pid}) S.{e['PDF-Seite']}")
                    zaehler["RÜCK"] += 1
                elif n > vor + 1:
                    out.append(f"[LÜCKE] {vor + 1}–{n - 1} fehlen vor ID {e['ID']} {e['Signatur']} (Eltern {pid}) S.{e['PDF-Seite']}")
                    zaehler["LÜCKE"] += 1
            vor = n
    try:
        mt = open(f"{mo}/{d}.txt", encoding="utf-8").read()
        teil = mt.split("== Excel:", 1)[1] if "== Excel:" in mt else ""
        for l in teil.splitlines()[1:]:
            if l.startswith("ID "):
                out.append("[OHNE] " + l[:160])
                zaehler["OHNE"] += 1
    except FileNotFoundError:
        pass
    out.insert(1, "Zusammenfassung: " + (", ".join(f"{k} {v}" for k, v in sorted(zaehler.items())) or "keine Auffälligkeiten"))
    open(f"{aus}/{d}.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(d, len(ee), dict(zaehler))
