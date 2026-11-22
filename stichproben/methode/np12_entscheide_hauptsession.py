"""Nachtrag zu Nachprüfung 12: Entscheide der Hauptsession vom 22.11.2026 zu den Konventionsfragen in offen_kritisch.csv,
funde_nachpruefung12.csv und roh/np12_vorab_kritisch.csv eintragen. Die K-Nummern bleiben stabil, es wird nichts neu nummeriert.
Aufruf: python -I np12_entscheide_hauptsession.py <stichproben-Ordner>"""
import csv, sys

st = sys.argv[1]
E = "Entscheid Hauptsession 22.11.2026: "
R10 = " Umsetzung in Runde 10."

# K-Nummer -> (Art, Text). Art: «mittel» = fällt aus offen_kritisch, «bewusst» = bewusst offen, «kritisch» = bleibt kritisch
ENTSCHEID = {
    "K166": ("kritisch", E + "ja. Eine eigene Eintragszeile (Werktitel/Datierung) direkt vor der ersten Signatur ist ein Stück ohne "
                         "Nummer und kommt in die Bestandszeile (Regel 31)." + R10),
    "K171": ("mittel", E + "nein. Text in Einleitung, Übersicht oder einer Vorbemerkung in Prosa bleibt Vorspann im Blatt Info; das Info "
                       "ist die Quelle für die Bestandsebene und wird dort von Hand übernommen. Darum mittel."),
    "K176": ("mittel", E + "nein. Text in Einleitung, Übersicht oder einer Vorbemerkung in Prosa bleibt Vorspann im Blatt Info; das Info "
                       "ist die Quelle für die Bestandsebene und wird dort von Hand übernommen. Darum mittel."),
    "K162": ("kritisch", E + "Ein beschreibender Satz unter einer Gruppenzeile ohne Signatur (Satz in Klammern oder «Vgl. …») kommt ins "
                         "Darin jeder Einheit der Gruppe, bis zur nächsten Gruppenzeile bzw. zum Ende der Elterneinheit. Die Gruppenzeile "
                         "selbst bleibt Hinweis (K8). Soll danach gefasst." + R10),
    "K117": ("bewusst", E + "bewusst offen wie D2681 (Runde 7, «Bewusst offen»). Die zweite Schachtelfolge zählt dieselben Nummern; eine "
                        "Trennung bräuchte einen erfundenen Signaturteil. Die Teile tragen den Hinweis «Signatur taucht erneut auf …»."),
    "K115": ("kritisch", E + "bleibt kritisch (Vorbemerkung zu Schachteln)." + R10),
    "K116": ("kritisch", E + "bleibt kritisch (Vorbemerkung zu Schachteln)." + R10),
}
for k in ("K144", "K123", "K154", "K143", "K142", "K119", "K98"):
    ENTSCHEID[k] = ("kritisch", E + "nach bestehender Konvention kritisch, bestätigt." + R10)
SOLL_NEU = {
    "K162": "Die Beschreibungen unter den Gruppenzeilen ins Darin jeder Einheit der Gruppe: «(Die Bände enthalten Notizen vorwiegend "
            "zum Rechnungswesen, zu den Sitzungen verschiedener Gremien [bes. Baukommission], zu Handwerkeraufträgen und "
            "Kaufverträgen.)» (S. 11, y 546–574) ins Darin von 4.2.51. und 4.2.52.; «Vgl. die vollständige Serie der gedruckten "
            "Erfolgsrechnungen und Bilanzen in den Jahresberichten.» (S. 10, y 659–674) ins Darin jeder Einheit 4.2.22.–4.2.50. Die "
            "Gruppenzeilen selbst bleiben Hinweis bei der ersten Einheit (K8).",
}

lies = lambda f: list(csv.DictReader(open(f, encoding="utf-8"), delimiter=";"))


def schreibe(f, rows, felder):
    with open(f, "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=felder, delimiter=";", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def mit(alt, neu):
    alt = (alt or "").strip()
    return neu if not alt or alt.startswith(("Konventionsfrage", "Grenzfall")) else (alt + " " + neu)


# 1. offen_kritisch.csv
ok = lies(f"{st}/offen_kritisch.csv")
felder_ok = list(ok[0].keys())
schluessel = {}   # K -> (paket, pdf, signatur) bzw. k_alt
aus = []
for z in ok:
    k = z["nr"]
    if k in ENTSCHEID:
        art, text = ENTSCHEID[k]
        schluessel[k] = (z["paket"], z["datei"] + ".pdf", z["signatur_id"])
        z["entscheid"] = mit(z["entscheid"], text)
        if k in SOLL_NEU:
            z["soll"] = SOLL_NEU[k]
        if art == "bewusst":
            z["bewusst_offen"] = "ja"
        if art == "mittel":
            continue
    aus.append(z)
fehlt = set(ENTSCHEID) - set(schluessel)
assert not fehlt, f"K-Nummern nicht gefunden: {fehlt}"
schreibe(f"{st}/offen_kritisch.csv", aus, felder_ok)

# 2. funde_nachpruefung12.csv: dieselben Zeilen über k_alt oder (paket, pdf, signatur)
fu = lies(f"{st}/funde_nachpruefung12.csv")
felder_fu = list(fu[0].keys())
treffer = {}
for r in fu:
    for k, (pk, pdf, sig) in schluessel.items():
        if r.get("k_alt") == k or (r["paket"] == pk and r["pdf"] == pdf and r["signatur"] == sig and r["schwere"] == "kritisch"):
            art, text = ENTSCHEID[k]
            r["entscheid"] = mit(r.get("entscheid"), text)
            if k in SOLL_NEU:
                r["soll"] = SOLL_NEU[k]
            if art == "mittel":
                r["schwere"] = "mittel"
            treffer[k] = treffer.get(k, 0) + 1
assert set(treffer) == set(ENTSCHEID), f"Funde nicht gefunden: {set(ENTSCHEID) - set(treffer)}"
schreibe(f"{st}/funde_nachpruefung12.csv", fu, felder_fu)

# 3. roh/np12_vorab_kritisch.csv
vb = lies(f"{st}/roh/np12_vorab_kritisch.csv")
felder_vb = list(vb[0].keys())
aus = []
for r in vb:
    k = next((k for k, (pk, pdf, sig) in schluessel.items()
              if r["paket"] == pk and r["datei"] + ".pdf" == pdf and r["signatur_id"] == sig), None)
    if k:
        art, text = ENTSCHEID[k]
        r["entscheid"] = mit(r["entscheid"], text)
        if k in SOLL_NEU:
            r["soll"] = SOLL_NEU[k]
        if art == "mittel":
            continue
    aus.append(r)
schreibe(f"{st}/roh/np12_vorab_kritisch.csv", aus, felder_vb)

ok2 = lies(f"{st}/offen_kritisch.csv")
print("offen_kritisch:", len(ok2), "Zeilen in", len({z["datei"] for z in ok2}), "Dateien; bewusst offen:",
      sum(z["bewusst_offen"] == "ja" for z in ok2), "; nicht bewusst offen:", sum(z["bewusst_offen"] != "ja" for z in ok2), "in",
      len({z["datei"] for z in ok2 if z["bewusst_offen"] != "ja"}), "Dateien")
print("Funde angepasst:", dict(sorted(treffer.items(), key=lambda x: int(x[0][1:]))))
print("Vorabliste:", len(aus), "Zeilen")
