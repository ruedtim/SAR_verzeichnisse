"""Pakete A1–A5 (Gegenprüfung Runde 8) mit Dateiliste und Altzeilen aus funde_nachpruefung9.csv und offen_kritisch.csv.
Aufruf: python -I pakete_bauen.py <stichproben> <population.csv> <pakete_ordner>"""
import csv, sys
stp, pop, aus = sys.argv[1:4]
A = {
 "A1": "D1746 D1880 D3012 D3060 D3105 D10744 D151150 D176795 D2894 D2962 D3161 D3221 D3231 D3256 D3405",
 "A2": "D3018 D3089 D3271 D3462 D3826 D152781 D151730 D65 D69 D71",
 "A3": "D3470 D1924 D3566 D3727 D3313 D1180 D2620",
 "A4": "D845 D134644 D140969 D847 D149825 D152817 D2850 D152404 D1874",
 "A5": "D1116 D1341 D1387 D151733 D1761 D1793 D1820 D1856 D1858 D1967 D2137 D2143 D2147 D2378 D263 D2630 D3077 D3774 D3810 D3842 D789",
}
nie = {r["datei"]: r for r in csv.DictReader(open(pop, encoding="utf-8"), delimiter=";")}
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8"), delimiter=";"))
k = {(r["datei"], r["signatur_id"], r["soll"]): r["nr"] for r in lies(f"{stp}/offen_kritisch.csv")}
f9 = lies(f"{stp}/funde_nachpruefung9.csv")
bn = 0
for p, dd in A.items():
    dd = dd.split()
    with open(f"{aus}/{p}_dateien.txt", "w", encoding="utf-8") as f:
        for d in dd:
            x = nie[d]
            f.write(f"{d}\t{x['einheiten']} Einheiten\t{'ERSTPRÜFUNG (nie in einer Fundliste)' if not x['geprueft'] else 'schon geprüft'}\n")
    zeilen = []
    for r in f9:
        d = r["pdf"].replace(".pdf", "")
        if d not in dd or r["status"] in ("behoben", "entfällt"):
            continue
        bn += 1
        st = r["status"]
        ist = r["neu_ist"] if st != "ungeprüft" else (r["ist"] + " [NP9 ungeprüft: " + r["neu_ist"] + "]")
        bem = r["bemerkung"]
        if bem.startswith("[B"):
            bem = bem.split("] ", 1)[-1]
        zeilen.append({"nr": f"B{bn}", "k_nr": k.get((d, r["signatur"], r["soll"]), ""), "quelle": "NP9", "pdf": r["pdf"],
                       "seite": r["seite"], "signatur": r["signatur"], "feld": r["feld"], "schwere": r["schwere"],
                       "soll": r["soll"], "ist": ist, "bemerkung": bem, "status": st, "neu_ist": ""})
    with open(f"{aus}/{p}_altzeilen.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["nr", "k_nr", "quelle", "pdf", "seite", "signatur", "feld", "schwere", "soll", "ist",
                                          "bemerkung", "status", "neu_ist"], delimiter=";")
        w.writeheader(); w.writerows(zeilen)
    print(p, len(dd), "Dateien,", sum(1 for d in dd if not nie[d]["geprueft"]), "Erstprüfungen,", len(zeilen), "Altzeilen,",
          sum(1 for z in zeilen if z["k_nr"]), "davon K:", ",".join(z["k_nr"] for z in zeilen if z["k_nr"]))
