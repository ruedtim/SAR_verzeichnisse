"""Prüfseiten je Stichproben-PDF (fester Startwert).
Regel: bis 4 Seiten alles; ab 5 Seiten 3 Zufallsseiten aus den Seiten, auf denen Einheiten beginnen
(bei Findmitteln mit wenigen, langen Einheiten – unter 30 Einheiten – aus allen Seiten ab der ersten Einheit);
Ausnahme: «ohne Signaturen» bis 10 Seiten ganz. Dazu immer alle Seiten mit Lücken laut Blatt «Vollständigkeit»."""
import csv, random, sys, openpyxl, collections
SEED = 20261119
EX = "/Users/stazh/Documents/GithubRemops_ruedtim/SAR_verzeichnisse/findmittel_excel/"
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter=";"))
rng = random.Random(SEED)
out = []
for r in rows:
    stem = r["PDF"][:-4]
    wb = openpyxl.load_workbook(EX + stem + "_scope_import.xlsx", read_only=True)
    ws = wb["scope-Import"]
    it = ws.iter_rows(values_only=True)
    kopf = list(next(it))
    iS = kopf.index("PDF-Seite")
    seiten = collections.Counter(row[iS] for row in it if row[iS] is not None)
    wv = wb["Vollständigkeit"]
    luecken, start = [], False
    for row in wv.iter_rows(values_only=True):
        if row[0] == "PDF-Seite":
            start = True; continue
        if start and row[3]:
            luecken.append(row[0])
    lseiten = sorted(set(luecken))
    n = int(r["Seiten"])
    if n <= 4 or (r["Gliederung"] == "ohne Signaturen" and n <= 10):
        wahl = "alle"
    else:
        if int(r["Einheiten"]) < 30:
            kand = list(range(min(seiten), n + 1))
        else:
            kand = sorted(seiten)
        wahl = ",".join(map(str, sorted(rng.sample(kand, min(3, len(kand))))))
    out.append([r["Nr"], r["PDF"], r["Bestand"], r["Gliederung"], n, r["Einheiten"], r["Status"], r["Text erfasst"],
                f"{min(seiten)}–{max(seiten)}", wahl, len(luecken), ",".join(map(str, lseiten)), r["Schicht"]])
w = csv.writer(sys.stdout, delimiter=";")
w.writerow(["Nr","PDF","Bestand","Gliederung","Seiten","Einheiten","Status","Text erfasst","Seiten mit Einheiten",
            "Prüfseiten (Zufall)","Lückenzeilen","Seiten mit Lücken","Schicht"])
w.writerows(out)
