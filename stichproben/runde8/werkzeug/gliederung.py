"""Gliederungsprüfung über einen Ausgabeordner (alle *_scope_import.xlsx).
Aufruf: python -I gliederung.py <ordner> [--details DATEI,...] [--csv out.csv]

Signale je Einheit (Kürzel in Klammern):
  titelsig (T)  Titel beginnt mit einer Dezimal-Signatur «2.38. Belege …» – Signatur nicht erkannt
  darinsig (D)  Darin-Zeile beginnt mit einer Signatur derselben Hauptnummer, die als Einheit fehlt
  eltern   (E)  Signatur der Eltern ist kein Präfix der eigenen Signatur (nur Dezimal-Signaturen)
  selbst   (S)  Teil hängt unter einer Einheit mit derselben Signatur
  folge    (F)  Geschwister-Signatur kleiner als die vorige (PDF-Reihenfolge, ohne Teile)
  luecke   (L)  fehlende Nummer in einer Geschwisterfolge, die als Text (Titel/Darin/Info) vorkommt
  form     (:)  gleiche Stufe teils mit, teils ohne «:» zwischen Bestand und Nummer
  datum    (J)  Jahreszahl als Komponente der Signatur
  schluss  (Z)  viele Schlussvermerk-Zeilen (Blatt Vollständigkeit)
"""
import collections
import csv
import glob
import os
import re
import sys

import openpyxl

args = [a for a in sys.argv[1:] if not a.startswith("--")]
ordner = args[0]
details = set()
csv_aus = None
for i, a in enumerate(sys.argv):
    if a == "--details":
        details = set(sys.argv[i + 1].split(","))
    if a == "--csv":
        csv_aus = sys.argv[i + 1]

SIG_ZEILE = re.compile(r"^\s*(\d{1,3}(?:\.\d{1,3})+)\.?\s+[A-ZÄÖÜ„\"«(]")
MONAT = re.compile(r"^\s*[\d.]+\s*(?:Jan|Feb|März|Mär|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez|Jahr|Zeilen|Exemplar|"
                   r"Sitzung|Stück|Fotos?|Bl\b)")


def komp(lokal: str) -> list[str]:
    return [k for k in lokal.split(".") if k]


def ist_dezimal(k: list[str]) -> bool:
    return bool(k) and all(re.fullmatch(r"\d{1,4}[a-z]?", x) for x in k) and not k[0].startswith("0")


def zahl(x: str) -> int:
    return int(re.match(r"\d+", x).group(0))


ergebnis = []
csv_zeilen = []
for p in sorted(glob.glob(f"{ordner}/*_scope_import.xlsx")):
    name = os.path.basename(p).split("_")[0]
    if name.startswith("uebersicht"):
        continue
    wb = openpyxl.load_workbook(p, read_only=True)
    if "scope-Import" not in wb.sheetnames:
        continue
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    rows = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    if not rows:
        continue
    voll = {str(x[0]): x[2] for x in wb["Vollständigkeit"].iter_rows(values_only=True) if x and x[0]}
    m = re.match(r"(\d+) Zeilen", str(voll.get("Schlussvermerke", "")))
    n_schluss = int(m.group(1)) if m else 0
    info = [str(c) for x in wb["Info"].iter_rows(values_only=True) for c in x if c][2:]
    nach_id = {r["ID"]: r for r in rows}
    for r in rows:
        s = str(r["Signatur"] or "")
        r["_doppel"] = ":" in s
        r["_lokal"] = s.split(":", 1)[1] if ":" in s else s
        r["_k"] = komp(r["_lokal"])
    funde = collections.defaultdict(list)

    # Bestandssignatur (Präfix vor dem Doppelpunkt) und Signaturen ohne Doppelpunkt: lokalen Teil abtrennen
    praefixe = collections.Counter(str(r["Signatur"]).split(":", 1)[0] for r in rows if r["_doppel"])
    bestand = praefixe.most_common(1)[0][0] if praefixe else ""
    if bestand:
        for r in rows:
            s = str(r["Signatur"] or "")
            if not r["_doppel"] and s.startswith(bestand) and len(s) > len(bestand):
                r["_lokal"] = s[len(bestand):]
                r["_k"] = komp(r["_lokal"])
                r["_ohne"] = True
    vorhanden = {".".join(r["_k"]) for r in rows}

    # form: Einheiten ohne «:», obwohl die Mehrheit «Bestand:» hat
    ohne = [r for r in rows if r.get("_ohne")]
    if bestand and ohne:
        for r in ohne:
            funde[":"].append((r, f"{r['Signatur']} (Bestand {bestand}:…)"))

    for r in rows:
        t = str(r["Titel"] or "")
        k = r["_k"]
        m = re.match(r"^(\d{1,3}(?:\.\d{1,3})+)\.?\s+\S", t)
        if m and not re.match(r"^\d{1,2}\.\d{1,2}\.(?:\d{2,4}|\s*(?:Jan|Feb|Mär|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez))", t):
            funde["T"].append((r, t[:70]))
        if any(re.fullmatch(r"(?:18|19|20)\d\d", x) for x in k):
            funde["J"].append((r, str(r["Signatur"])))
        par = nach_id.get(r["Parent-ID"])
        if par is not None:
            pk = par["_k"]
            if r["Teil"] and par["Signatur"] == r["Signatur"]:
                pass  # normale Teile hängen unter Teil 1
            elif ist_dezimal(k) and ist_dezimal(pk) and pk and k[:len(pk)] != pk and not r["Teil"]:
                funde["E"].append((r, f"{'.'.join(k)}. unter {'.'.join(pk)}."))
        if ist_dezimal(k):
            for z in str(r["Darin"] or "").split("\n"):
                mm = SIG_ZEILE.match(z)
                if not mm or MONAT.match(z):
                    continue
                sk = komp(mm.group(1))
                if sk[0] == k[0] and ".".join(sk) not in vorhanden and len(sk) >= 2:
                    funde["D"].append((r, z[:70]))

    # Geschwisterfolge
    kinder = collections.defaultdict(list)
    for r in rows:
        if not r["Teil"] and ist_dezimal(r["_k"]):
            kinder[r["Parent-ID"]].append(r)
    texte = [str(r["Titel"] or "") for r in rows] + [z for r in rows for z in str(r["Darin"] or "").split("\n")] \
        + [z for t in info for z in t.split("\n")]
    # alle vorhandenen Nummern je Präfix, Bereiche «2-4» / «6-7a» ausgeschrieben
    belegt = set()
    for r in rows:
        k = r["_k"]
        if not k:
            continue
        mb = re.fullmatch(r"(\d+)[a-z]?\s*-\s*(\d+)[a-z]?", k[-1])
        if mb:
            for n in range(int(mb.group(1)), int(mb.group(2)) + 1):
                belegt.add(tuple(k[:-1]) + (str(n),))
        elif re.match(r"\d", k[-1]):
            belegt.add(tuple(k[:-1]) + (str(zahl(k[-1])),))
    for pid, ks in kinder.items():
        vor = None
        for r in ks:
            if vor is not None and len(vor["_k"]) == len(r["_k"]) and vor["_k"][:-1] == r["_k"][:-1]:
                a, b = zahl(vor["_k"][-1]), zahl(r["_k"][-1])
                if b < a:
                    funde["F"].append((r, f"{'.'.join(r['_k'])}. nach {'.'.join(vor['_k'])}."))
                elif b > a + 1:
                    pfx = "".join(f"{x}." for x in r["_k"][:-1])
                    for n in range(a + 1, min(b, a + 30)):
                        if tuple(r["_k"][:-1]) + (str(n),) in belegt:
                            continue
                        pat = re.compile(rf"(?:^|\s){re.escape(pfx)}{n}\.?\s+[A-ZÄÖÜ„\"«(]")
                        if any(pat.search(x) for x in texte):
                            funde["L"].append((r, f"{pfx}{n}. fehlt (vor {'.'.join(r['_k'])}.)"))
            vor = r
    if len(funde.get("J", [])) > len(rows) / 3:  # Locher-Signaturen mit Jahrgang: gewollt
        del funde["J"]
    if n_schluss >= 40:
        funde["Z"].append((rows[0], f"{n_schluss} Schlussvermerk-Zeilen"))
    gewicht = {"T": 3, "D": 1, "E": 2, "S": 3, "F": 2, "L": 3, ":": 1, "J": 1, "Z": 1}
    score = sum(gewicht[a] * len(v) for a, v in funde.items() if a != "Z") + (5 if funde.get("Z") else 0)
    if funde:
        ergebnis.append((score, name, len(rows), funde))
        for a, v in funde.items():
            for r, txt in v:
                csv_zeilen.append([name, a, r["ID"], r["Signatur"], r["Teil"] or "", txt])

ergebnis.sort(key=lambda x: -x[0])
summe = collections.Counter()
dateien = collections.Counter()
for score, name, n, funde in ergebnis:
    for a, v in funde.items():
        summe[a] += len(v)
        dateien[a] += 1
print("Signal  Funde  Dateien")
for a in "TDESFL:JZ":
    print(f"  {a}    {summe[a]:6} {dateien[a]:6}")
print()
for score, name, n, funde in ergebnis:
    kurz = " ".join(f"{a}{len(v)}" for a, v in sorted(funde.items()))
    print(f"{name:9} {n:5} {score:5}  {kurz}")
    if details and name not in details and "alle" not in details:
        continue
    if not details and score < 6:
        continue
    for a, v in sorted(funde.items()):
        for r, txt in v[: (None if name in details else 3)]:
            print(f"      {a} ID{r['ID']} {str(r['Signatur'])[-22:]:22} {txt}")
print(len(ergebnis), "Dateien mit Funden")
if csv_aus:
    with open(csv_aus, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Datei", "Signal", "ID", "Signatur", "Teil", "Text"])
        w.writerows(csv_zeilen)
