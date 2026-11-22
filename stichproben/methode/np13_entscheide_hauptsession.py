"""Nachtrag zu Nachprüfung 13: Entscheide der Hauptsession vom 22.11.2026 zu den drei Konventionsfragen in offen_kritisch.csv,
funde_nachpruefung13.csv und roh/np13_dateien_urteil.csv eintragen. Die K-Nummern bleiben stabil, neue Zeilen bekommen die
nächsten Nummern (K199 ff.).
- K135 / Regel 17: bestätigt (Teil mit Hinweis, wenn die Nachbarnummern da sind); fehlt die Nachbarnummer, wird die zweite
  Nennung zur fehlenden Nummer (K183, K184).
- Buchstaben in der Titelspalte einer Gruppe sind Darin-Einträge der Gruppe, auch mit eigenem Datum; eigene Einheiten nur in
  einer eigenen Spalte. Betroffen laut Suchlauf `np13_suchlauf_buchstaben_titelspalte.py`: D177470 (Stichprobe Z2), D3012,
  D3038, D3089.
- K178: Gruppe wird ein Code nur nach der Schrift (14 pt gegen 12 pt); 710 ist ein gewöhnlicher Code.
Aufruf: python -I np13_entscheide_hauptsession.py <stichproben-Ordner>"""
import csv, math, sys

st = sys.argv[1]
E = "Entscheid Hauptsession 22.11.2026: "
R11 = " Umsetzung in Runde 11."
lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8"), delimiter=";"))


def schreibe(f, rows, felder):
    with open(f, "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=felder, delimiter=";", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def mit(alt, neu):
    alt = (alt or "").strip()
    return neu if not alt else alt + " " + neu


TEXT = {
    "K178": E + "keine Zehnergruppen nach der Nummer allein; Gruppe wird ein Code nur nach der Schrift (14 pt gegen 12 pt). 710 ist ein gewöhnlicher Code." + R11,
    "K183": E + "Steht eine Signatur zweimal hintereinander mit anderem Titel und fehlt die Nachbarnummer, wird die zweite Nennung zur fehlenden Nummer, mit Hinweis." + R11,
    "K184": E + "Steht eine Signatur zweimal hintereinander mit anderem Titel und fehlt die Nachbarnummer, wird die zweite Nennung zur fehlenden Nummer, mit Hinweis." + R11,
    "K135": E + "bestätigt: Sind die Nachbarnummern da, bleibt die zweite Nennung ein Teil mit dem Hinweis «Tippfehler?»; mittel.",
}
BU = E + "Buchstaben a)–h) in der Titelspalte einer Gruppe (nicht in der Signaturspalte) sind Darin-Einträge der Gruppe, auch mit eigenem Datum; eigene Einheiten nur in einer eigenen Spalte."
BESTAETIGEN = " Hier sind es Untergruppen mit eigener Schachtel und Bandliste: bitte bestätigen, dass der Entscheid auch dafür gilt."
NEU = [
    {"datei": "D177470", "signatur_id": "VII.249.:27.a.–27.h. (IDs 28–35), VII.249.:28.a.–28.h. (IDs 37–44)", "seite": "2–3",
     "feld": "Einheit, Darin", "paket": "Z2",
     "befund_jetzt": "16 Einheiten (Dossier E2) unter 27. «Dokumentationen» (ID 27) und 28. «Ausbildung und Berufstätigkeit von Frau Ruth Reinhard» (ID 36). Die Buchstaben a)–h) stehen in der Titelspalte der Gruppe (x 99–101 wie der Titel von 27./28.; Signaturspalte x 71).",
     "soll": "27. und 28. sind Dossiers mit den Einträgen a)–h) im Darin («a) Familie Guldener von Albisrieden» … «h) Ergänzung zu den Archivalien Punkt 1 - 26.» bzw. «a) Hans R. Reinhard; Zeichnen am Seminar Küsnacht …» … «h) Ruth Guldener; …»), Daten im Text, Zeitraum aus den Einträgen; keine Einheiten 27.a.–h. und 28.a.–h. (wie D3826 8. und 14.).",
     "entscheid": BU + R11 + " Zählt in der Zufallsstichprobe (Z2)."},
    {"datei": "D3012", "signatur_id": "VII.170.:1.a.–1.c. (IDs 2–4), VII.170.:8.a.–8.c. (IDs 12–14)", "seite": "1–2",
     "feld": "Einheit, Darin", "paket": "S",
     "befund_jetzt": "6 Einheiten unter 1. «Oberstadtgass» (ID 1) bzw. 8. «Polizist Wäckerli» (ID 11). Die Buchstaben stehen in der Titelspalte der Gruppe (x 99 wie der Titel von 1./8.; Signaturspalte x 71).",
     "soll": "1. und 8. mit den Einträgen a)–c) im Darin («a) Hörspielfolge: 10 Sendungen 1955-1956 Schachtel 01», «b) Drehbuch: …», «c) Presseorientierung 27.09.1956» bzw. «a Rollenbuch [Hörspiel Radio] ohne Datum», «b) Rollenbuch [Fernsehspiel] … Schachtel 06», «c) Diverse Drehbücher von: 1955-1970 Schachtel 07»); keine Einheiten 1.a.–c., 8.a.–c.",
     "entscheid": BU + R11},
    {"datei": "D3038", "signatur_id": "VII.181.:I.a. (ID 2), VII.181.:I.b. (ID 3)", "seite": "1", "feld": "Einheit, Darin", "paket": "S",
     "befund_jetzt": "2 Einheiten (Dossier E2, Schachtel 1) unter I. «Protokolle, Korrespondenz» (ID 1): «a) Protokolle Vorstandssitzungen 1930-1987», «b) Protokolle Generalversammlungen 1930-1986». Die Buchstaben stehen in der Titelspalte (x 113 wie der Titel von I.; Signaturspalte x 71).",
     "soll": "Die Einträge a) und b) samt «Anmerkung: 1930-1951 alle Protokolle in einem Buch gebunden zusammen.» im Darin der Einheit für Schachtel 1 unter I.; keine Einheiten I.a., I.b.",
     "entscheid": BU + BESTAETIGEN + R11},
    {"datei": "D3089", "signatur_id": "VII.197.:I.3.a.–I.3.c. (IDs 5–7)", "seite": "3–4", "feld": "Einheit, Darin", "paket": "S",
     "befund_jetzt": "3 Einheiten (Dossier E3) unter I.3. «PROTOKOLLE» (ID 4, Serie): a) Vorstandsprotokolle (Sch. 4, 13 Darin-Zeilen), b) Generalversammlungsprotokolle (Sch. 7), c) Sitzungsprotokolle (Sch. 8-15). Die Buchstaben stehen in der Titelspalte (x 113 wie der Titel von 3.; Signaturspalte x 71).",
     "soll": "I.3. als Dossier mit den Einträgen a)–c) und ihren Bandzeilen im Darin (Schachteln 4–15 im Text); keine Einheiten I.3.a.–c.",
     "entscheid": BU + BESTAETIGEN + R11},
]

# 1. offen_kritisch.csv
ok = lies(f"{st}/offen_kritisch.csv")
felder = list(ok[0].keys())
for z in ok:
    if z["nr"] in TEXT:
        z["entscheid"] = mit(z["entscheid"], TEXT[z["nr"]])
nr = max(int(z["nr"][1:]) for z in ok)
vorhanden = {(z["datei"], z["signatur_id"]) for z in ok}
neue = []
for n in NEU:
    if (n["datei"], n["signatur_id"]) in vorhanden:
        continue
    nr += 1
    neue.append(dict({k: "" for k in felder}, nr=f"K{nr}", status="neu", erstmeldung="NP13", muster="Einheit erfunden",
                     ursache="vor Runde 10; Konventionsentscheid der Hauptsession vom 22.11.2026", **n))
ok += neue
schreibe(f"{st}/offen_kritisch.csv", ok, felder)

# 2. funde_nachpruefung13.csv
fu = lies(f"{st}/funde_nachpruefung13.csv")
ffu = list(fu[0].keys())
for r in fu:
    if r.get("k_alt") in TEXT:
        r["entscheid"] = mit(r["entscheid"], TEXT[r["k_alt"]])
    if r["paket"] == "G3" and r["pdf"] == "D3472.pdf" and r["schwere"] == "kritisch" and r["status"] == "neu":
        r["entscheid"] = mit(r["entscheid"], TEXT["K183"])
for z in neue:
    fu.append({"pdf": z["datei"] + ".pdf", "seite": z["seite"], "signatur": z["signatur_id"], "feld": z["feld"], "schwere": "kritisch",
               "soll": z["soll"], "ist": z["befund_jetzt"], "bemerkung": "Ursache: " + z["ursache"] + " (Suchlauf «Buchstaben in der Titelspalte»)",
               "status": "neu", "neu_ist": z["befund_jetzt"], "muster": "Einheit erfunden", "paket": z["paket"], "k_alt": z["nr"],
               "entscheid": z["entscheid"]})
schreibe(f"{st}/funde_nachpruefung13.csv", fu, ffu)

# 3. Dateiurteile und Restrate
du = lies(f"{st}/roh/np13_dateien_urteil.csv")
fdu = list(du[0].keys())
okdat = {z["datei"] for z in ok}
for r in du:
    if r["datei"] in okdat:
        r["urteil_jetzt"] = "kritisch"
schreibe(f"{st}/roh/np13_dateien_urteil.csv", du, fdu)


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0, c - h), min(1, c + h)


zd = [r for r in du if r["paket"].startswith("Z")]
k = sum(r["urteil_jetzt"] == "kritisch" for r in zd)
lo, hi = wilson(k, len(zd))
print("neue Zeilen:", [z["nr"] + " " + z["datei"] for z in neue])
print(f"offen_kritisch: {len(ok)} Zeilen in {len(okdat)} Dateien; bewusst offen {sum(z['bewusst_offen'] == 'ja' for z in ok)}; "
      f"nicht bewusst offen {sum(z['bewusst_offen'] != 'ja' for z in ok)} in {len({z['datei'] for z in ok if z['bewusst_offen'] != 'ja'})} Dateien")
print(f"Stichprobe: {k}/{len(zd)} kritisch ({k / len(zd):.1%}, KI {lo:.1%}–{hi:.1%}); auf 642: {k / len(zd) * 642:.0f} (KI {lo * 642:.0f}–{hi * 642:.0f})")
print("Funde:", len(fu))
