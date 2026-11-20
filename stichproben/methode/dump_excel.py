"""Lesbarer Auszug aus einer *_scope_import.xlsx (nur lesen).

Aufruf:
  python3 -I dump_excel.py DATEI.xlsx                 # alle Einheiten
  python3 -I dump_excel.py DATEI.xlsx --seiten 12-14  # nur Einheiten, die auf PDF-Seite 12-14 beginnen
                                                      # (+ die letzte Einheit davor, falls sie hinüberläuft)
  python3 -I dump_excel.py DATEI.xlsx --voll          # zusätzlich Blatt «Vollständigkeit» (Zeilen mit Lücken)
  python3 -I dump_excel.py DATEI.xlsx --nurvoll       # nur Blatt «Vollständigkeit»
  python3 -I dump_excel.py DATEI.xlsx --sig VII.200.:2.1   # nur Signaturen, die so beginnen
  python3 -I dump_excel.py DATEI.xlsx --kurz          # nur Kopfzeile je Einheit (ohne Darin)
"""
import sys, argparse, openpyxl

ap = argparse.ArgumentParser()
ap.add_argument("xlsx")
ap.add_argument("--seiten")
ap.add_argument("--voll", action="store_true")
ap.add_argument("--nurvoll", action="store_true")
ap.add_argument("--sig")
ap.add_argument("--kurz", action="store_true")
ap.add_argument("--info", action="store_true", help="nur Blatt «Info» (u. a. Vorspann, Signaturen nur im Vorspann)")
ap.add_argument("--max-darin", type=int, default=400, help="max. Darin-Zeilen je Einheit (Standard 400)")
a = ap.parse_args()

wb = openpyxl.load_workbook(a.xlsx, read_only=True)
ws = wb["scope-Import"]
rows = list(ws.iter_rows(values_only=True))
kopf = [str(h) for h in rows[0]]
daten = [dict(zip(kopf, r)) for r in rows[1:] if any(v is not None for v in r)]

def s(v):
    return "" if v is None else str(v)

if a.info:
    for r in wb["Info"].iter_rows(values_only=True):
        if r and r[0] and r[0] not in ("Konventionen",) and not str(r[0]).startswith(("Hierarchie","Stufen","Teile","Zeitraum","Darin","Schachteln","Gliederung","Hilfsspalten","Datumsoperatoren")):
            print(f"{r[0]}: {r[1] if len(r) > 1 else ''}")
    sys.exit(0)

if not a.nurvoll:
    auswahl = daten
    if a.seiten:
        lo, _, hi = a.seiten.partition("-")
        lo, hi = int(lo), int(hi or lo)
        idx = [i for i, d in enumerate(daten) if d.get("PDF-Seite") is not None and lo <= int(d["PDF-Seite"]) <= hi]
        if idx and idx[0] > 0:
            idx = [idx[0] - 1] + idx
        elif not idx:
            vor = [i for i, d in enumerate(daten) if d.get("PDF-Seite") is not None and int(d["PDF-Seite"]) < lo]
            idx = vor[-1:]
        auswahl = [daten[i] for i in idx]
    if a.sig:
        auswahl = [d for d in auswahl if s(d.get("Signatur")).startswith(a.sig)]
    print(f"# {a.xlsx}: {len(daten)} Zeilen gesamt, {len(auswahl)} ausgegeben")
    for d in auswahl:
        zr = ""
        if d.get("Entstehungszeitraum"):
            op = "=" if str(d["Entstehungszeitraum"]).startswith("Genau") else "von/bis"
            zr = f"{op} {s(d.get('von'))}–{s(d.get('bis'))}"
        felder = [f"ID {s(d['ID'])}", f"P {s(d['Parent-ID'])}", f"Sig [{s(d['Signatur'])}]",
                  f"Stufe {s(d['Stufe'])}", f"Eb {s(d['Ebene'])}"]
        if d.get("Teil") not in (None, ""):
            felder.append(f"Teil {s(d['Teil'])}")
        felder.append(f"Über [{s(d['Übergeordnete Signatur'])}]")
        if zr:
            felder.append(f"Zeit {zr}")
        if d.get("Entstehungszeitraum, Anm."):
            felder.append(f"Anm [{s(d['Entstehungszeitraum, Anm.'])}]")
        if d.get("Umfang"):
            felder.append(f"Umfang [{s(d['Umfang'])}]")
        if d.get("Schachtel-Nr."):
            felder.append(f"Schachtel [{s(d['Schachtel-Nr.'])}]")
        felder.append(f"NrPDF [{s(d.get('Nr. im PDF'))}]")
        felder.append(f"S. {s(d.get('PDF-Seite'))}")
        if d.get("Zeitraum-Quelle"):
            felder.append(f"Quelle {s(d['Zeitraum-Quelle'])}")
        print("─" * 100)
        print(" | ".join(felder))
        print(f"  TITEL: {s(d['Titel'])}")
        if not a.kurz:
            darin = s(d.get("Darin"))
            if darin:
                zeilen = darin.split("\n")
                print(f"  DARIN ({len(zeilen)} Einträge):")
                for z in zeilen[: a.max_darin]:
                    print(f"    • {z}")
                if len(zeilen) > a.max_darin:
                    print(f"    … {len(zeilen) - a.max_darin} weitere Einträge")
            if d.get("Verwandte Verzeichnungseinheiten"):
                print(f"  VERWANDTE: {s(d['Verwandte Verzeichnungseinheiten'])}")
            if d.get("Prüfhinweise"):
                print(f"  HINWEISE: {s(d['Prüfhinweise']).replace(chr(10), ' / ')}")

if a.voll or a.nurvoll:
    wv = wb["Vollständigkeit"]
    print("\n=== Blatt Vollständigkeit ===")
    for r in wv.iter_rows(values_only=True):
        if any(v is not None for v in r):
            print(" | ".join(s(v) for v in r))
