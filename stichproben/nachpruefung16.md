# Nachprüfung 16: Gegenprüfung der Runde 13, leere Teile, vierte Zufallsstichprobe und Einschätzung für den Gesamtimport (22.11.2026)

Geprüft sind:
- **Runde 13:** Skript `2a44ff8d…` gegen 439a6fbf (Runde 12).
  - Gegenprüft sind die 46 Dateien mit sachlicher Änderung. Die übrigen 39 der 85 geänderten Dateien ändern sich nur im
    Leerschlag nach dem Strich; das ist per Skript belegt, fünf davon auch am PDF.
  - Die vier geänderten Testdateien sind zellgleich mit ihren Gegenstücken in `findmittel_excel/`.
- **Suchläufe über alle 715 Dateien:** alle bisherigen, dazu neu «leere Teile» (Muster K220) mit Sichtung aller 148 Treffer.
- **Vierte Zufallsstichprobe:** 60 Dateien nach der vor Runde 13 festgelegten Regel, je ganz geprüft.

Die Ergebnisse stehen hier:
- `offen_kritisch.csv`: nachgeführt, mit stabilen K-Nummern, 11 Zeilen. Behoben sind K209–K220, neu ist K221.
- `funde_nachpruefung16.csv`: 102 Zeilen.
- Rohdaten in `roh/np16_*`. Darunter sind die Pakete, die Einordnung jeder geänderten Zelle (`roh/np16_aenderungen_r13.csv`)
  und die vor Runde 13 festgelegte Kandidatenliste der Stichprobe (`roh/np16_kandidaten_ab197.txt`).
- Methode in `methode/ANLEITUNG_NACHPRUEFUNG16.md` und `methode/np16_*`.

## Kurz

- **Runde 13 wirkt vollständig.**
  - K209–K220 sind behoben und am PDF bestätigt, so wie du zu K210, K214, K217 und K219 entschieden hast.
  - Die geänderten Dateien haben keinen neuen kritischen Fehler aus Runde 13.
  - Die Regeln 6 und 7 (Strich, Titeldatum) bringen 7 mittlere Rückschritte, davon 2 angekündigt (D4173, D2721). Einige alte
    Trennungen bleiben stehen.
- **Vierte Zufallsstichprobe: 0 von 60 Dateien kritisch (95%-KI 0–6,0 %).**
  - Alle vier Stichproben zusammen ergeben 8 von 240 (3,3 %, KI 1,7–6,4 %).
  - Die letzten beiden zusammen, also der Stand nach den systematischen Durchsichten der NP15: 1 von 120 (0,8 %, KI 0,1–4,6 %).
- **Leere Teile:** Kein Kopf eines Unterverzeichnisses ist mehr ein Teil. Unter 148 Teilen ohne Angaben ist ein Grenzfall,
  D3099 1.2.5. (K221).
- **Offene kritische Fehler** (`offen_kritisch.csv`, Stand 2a44ff8d): 11 Zeilen in 11 Dateien. 10 sind bewusst offen, dazu
  kommt der Grenzfall K221.
- **Einschätzung:** Für kritische Fehler ist der Stand für den Gesamtimport tragbar. Mittlere Fehler (Titel, Zeitraum,
  Schachtel) sind häufig: In der Stichprobe hat fast jede dritte Datei mindestens einen neuen. Siehe den Abschnitt
  «Einschätzung für den Gesamtimport».

## Stände und Nachrechnung

| Stand | Lauf zellgleich | geändert gegenüber 439a6fbf | Einheiten | Fallsets |
|---|---|---|---:|---|
| 2a44ff8d (Runde 13) | ja, auch Testdaten und D151210 | 85 Dateien (= `runde13/geaenderte_dateien.txt`), davon 39 nur Leerschlag; Testdaten D149628, D3515, D177460, D9985; D151210 unverändert | 51'605 | A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38 (unverändert) |

`runde13/vorher/` ist zellgleich mit meinem Lauf der Runde 12. Die Einordnung der 428 geänderten Zellen ergibt 147 reine
Leerschlag-Zellen, 43 Prüfhinweise und 238 sachliche Zellen (`methode/np16_klassifiziere_aenderungen.py`).

## Gegenprüfung der Runde 13 (G1–G3)

| Paket | Inhalt | Dateien | Urteile | K-Zeilen | neu kritisch |
|---|---|---:|---|---|---:|
| G1 | Regeln 1–5 und 9, die 12 K-Dateien und D3099, D2620, D10585 | 15 | 30: 26 besser, 4 gleich | K209–K220 alle behoben | 1 (K221, Grenzfall, älter) |
| G2 | Regeln 6–8 in D149628, D176060, D150589, D3468 | 4 | 35 Zeilen zu 158 Zellen: 27 besser, 5 gleich, 3 schlechter (mittel) | – | 0 |
| G3 | Regeln 6–8 in 27 Dateien, dazu 5 reine Leerschlag-Dateien | 32 | 40 Einheiten: 36 besser, 4 schlechter (2 angekündigt) | – | 0 |

- **Regeln 1–5 und 9 (G1):**
  - Die fünf neuen Bestandszeilen enthalten genau das Stück, ohne fremden Text. Bearbeitervermerke und die «Anmerkung» bleiben
    im Info, und das Darin der letzten Einheit ist vollständig.
  - D845: Alle fünf Köpfe stehen bei der richtigen ersten Nennung; :44. ist 1911–1950.
  - Regel 9: Die Spannen sind belegt. D3099 7.3. ist 1941, 7. wieder 1941–1988. D2620 10.2. ist 1917–1936, D10585 3.8. ist
    1827–1828.
  - Neu mittel: D10585 3.8.1.–3.8.3. haben keinen Zeitraum, obwohl «(1827)» bzw. «(1828)» im Titel steht. Erst der neue Hinweis
    macht die alte Lücke sichtbar.
- **Regel 6 (Strich):** 42 von 43 alten Trennungen in den Dateien von G2 sind behoben, kein Strich beginnt dort eine Liste.
  Fehlgriffe, alle mittel:
  - D3468 1971.6: «Vertragsmappe Baulose» steht jetzt im Titel. Nach dem Zusammenfügen hängt die Regel für kurze Reste die
    Inhaltszeile an.
  - D149825 263.: Ein «-» aus der Datums- oder Schachtelspalte gilt als Titelstrich. Der Vermerk «Diese Nummer wurde aufgehoben;
    vgl. unter Nr. 257.» hängt jetzt am Titel; in Runde 12 war es richtig. Kosmetisch dasselbe bei D10675 742.96.
  - D3672 2.1.144.: Der zusammengefügte Titel hat 172 Zeichen und wird danach am ersten «: » geteilt. Der Titel heisst nur noch
    «The New York Times», der Artikeltitel steht im Darin. Die Teilung am Doppelpunkt trifft auch Titel mit offener Klammer
    oder Anführung (G2).
  - Angekündigt: D4173 3.3. (Lebensdaten im Titel) und D2721 1.
  - Nicht gegriffen: D10675 711.8 und 711.9 bleiben getrennt, der Strich fehlt. Aus derselben Liste sind auch D1746 VI.6., D1589
    :15, D821 :9. und D4175 2.B.1. noch getrennt; sie sind in Runde 13 unverändert. Die Aussage «nur D151210 bleibt getrennt»
    stimmt also nicht ganz.
- **Regel 7 (Titeldatum gegen Spalte):** fast überall plausibel; D149628 26.2.19. ist 1905–1913 wie die Spalte. Mittel:
  - D176060 12.4 ist zu eng: 20.–22.09.1988, obwohl die Studie vom 26. Juli 1988 in der Einheit liegt.
  - D150589 16.2.4 ist jetzt offen «ab 1955» statt genau 1955.
- **Regel 8 (Leerschlag):** In den fünf Probedateien ändert sich je genau eine Zelle, und der Text ist am PDF richtig. Die
  übrigen Leerschlag-Zellen in den G-Dateien sind ebenfalls richtig.
- **Schon vorher da, jetzt sichtbar (mittel):** In D149628 steht in 94 Titeln das Spaltendatum mitten im Titel. Bei 8 davon ist
  das Tagesdatum dadurch ein Jahr zu früh.

## Suchläufe über alle 715 Dateien

| Suchlauf | Runde 12 | Runde 13 | Ergebnis |
|---|---|---|---|
| Tippfehler in Dezimalsignaturen | wie NP15 | unverändert | nichts Neues |
| Stück ohne Nummer im Info | 21 Sätze | 20 | D414 weg (K219 behoben) |
| Buchstaben in der Titelspalte | 11 | 11 | Konvention, kein Fund |
| «n.a» als Kind | wie NP15 | gleich (D845 nur neue IDs) | nichts Neues |
| Nummern im Darin | 6 Läufe | 6 | kein Fund (wie NP14) |
| Gruppenende Faktor 1,3 / enger Filter | 11 / 192 | 11 / 192 | unverändert, in NP15 gesichtet |
| Bearbeitervermerk im Darin | 224 | 222 | D2630 weg (K213 behoben) |
| **Leere Teile** (neu, `methode/np16_suchlauf_leere_teile.py`) | KOPF 5 (D845), LEER 148 | KOPF 0, LEER 148 | S1: 1 Grenzfall (K221), 2 mittel |

**Leere Teile (S1):**
- Alle 148 Titel sind mit den PDF-Zeilen verglichen: 146 wörtlich gleich, 2 nur mit anderem Trennstrich.
- Kein Teil ist ein Kopf, eine Überschrift oder eine Übersichtszeile, und kein Inhalt steht bei einer anderen Einheit.
- In D149628 hat S1 18 Kandidaten genau angesehen und die übrigen nach Muster beurteilt (Plakatlisten). In D1880 sind alle 15
  genau angesehen: Es sind Positionen der 2. und 3. Serie, nur mit Titel.
- Mittel: D149628 23.2.1. «Y» und 23.5.2. «K»: Die einzige Inhaltszeile steht im Titel statt im Darin.
- **Grenzfall D3099 (K221):** Das PDF druckt «1.2.5.» zweimal, das zweite Mal mit «6. Generation: Hansjürg Diener». 1.2.6. gibt
  es nicht, und die Parallelliste hat 2.1.6. «6. Generation».
  - Heute ist die zweite Nennung Teil 2 (E4) unter 1.2.5., und 1.2.5. ist deshalb «Serie».
  - Nach deinem Entscheid zu Regel 17 (NP13: fehlt die Nachbarnummer, wird die zweite Nennung zur fehlenden Nummer) wäre sie
    1.2.6. (E3 unter 1.2.).
  - Das Skript macht hier aber bewusst einen Teil; der Kommentar bei der Teil-Regel nennt VII.199. Die Regel «fehlende
    Nachbarnummer» ist nur für einstufige Nummern und Jahr.Laufnummern umgesetzt.
  - G1 hat den Fall unabhängig ebenfalls gefunden. Ein Suchlauf über alle Dateien findet 4 Teile mit fehlender Nachbarnummer;
    nur D3099 ist ein Geschwisterfall.

## Vierte Zufallsstichprobe

- **Regel:** vor Runde 13 festgelegt (`roh/np16_VORBEREITUNG16.md`, Kandidaten `roh/np16_kandidaten_ab197.txt`, sha256
  `b3bd7213…`).
  - Gezogen wurden die ersten 60 Dateien ab Rang 197, die nicht in den Stichproben 1–3 und nicht in `offen_kritisch.csv`
    (Stand NP15) stehen und die Runde 13 nicht ändert.
  - Das sind die Ränge 197–261 (`roh/np16_zufall60_4.txt`).
  - Grundgesamtheit: 715 − 180 − 22 − 54 = 460 Dateien.
- **Umfang:** 60 Dateien mit 4'123 Einheiten, je ganz geprüft:
  - Z1: 18 Dateien mit 451 Einheiten;
  - Z2: 19 Dateien mit 451 Einheiten;
  - Z3: 20 Dateien mit 451 Einheiten;
  - ZL1: D3482 mit 1'929 Einheiten (jede Signaturzeile per Skript gegen die Einheiten, 16 Seiten Zeile für Zeile);
  - ZL2: D141020 mit 601 und D2935 mit 240 Einheiten.
- **0 kritisch (KI 0–6,0 %).** Die Gliederung stimmt in allen 60 Dateien. Frühere kritische Funde in diesen Dateien sind weiter
  behoben, und Schluss, Info und Gruppenende stimmen überall.
- **Mittel:** 46 neue mittlere Funde in 18 der 60 Dateien. Dazu kommen bekannte, die nicht neu gezählt sind. Die Muster:
  - Schachtel nicht weitergegeben: D2894 (28 Einheiten), D3405, D2653, D1746, D2935;
  - Datums-, Schachtel- oder Umfangsspalte im Titel, Titel falsch getrennt: D1591, D175561, D1791, D148468, D2953, D176721,
    D3405, D3512, D2937;
  - Zeitraum aus Jahresklammer ohne Lebensdaten verkürzt: D3561 6.2. «(1940 – 1947)» → 1945, D3512 1.1.1. → 1967;
  - Zeitraum aus Vermerken: D2935 «(fehlt, 25. März 1992)»;
  - Doppeldatum «6./7.9.1970» nur mit dem letzten Tag (D141020, 18 Aufführungen);
  - D3482: Zeitraum aus «2000 KW» und aus einem Verweis.
- **Grenzfall, als mittel gewertet:** D2894 «Akten zur Archivübernahme im Jahr 1980 wurden in Schachtel 1 abgelegt.» steht nur
  in der Vorbemerkung und wird nicht importiert. Nach der Konvention «Prosa in der Vorbemerkung» ist das mittel. NP12 hatte den
  Satz als kritisch gemeldet, weil er den Inhalt von Schachtel 1 nennt.

## Neue kritische Zeile (K221)

| K | Datei | Muster | Pakete | Status |
|---|---|---|---|---|
| K221 | D3099 1.2.5. Teil 2 | Eltern/Ebene falsch | G1, S1 | Grenzfall, älter als Runde 13 |

## Fragen an die Hauptsession

1. **K221 D3099:** Bleibt der Teil mit Hinweis (dann mittel), oder wird die zweite Nennung 1.2.6.? Ich empfehle 1.2.6., wie
   es dein Entscheid zu Regel 17 vorsieht. Die Nummer fehlt, und die Parallelliste 2.1. hat 2.1.6.
2. **D2894 (mittel):** Kommt der Vorbemerkungssatz zu Schachtel 1 ins Darin von Schachtel 1? Ich empfehle mittel stehen zu
   lassen, wie D10649 und D3273.
3. **D3896 (gering):** Die Lückenvermerke «X.D. 31. bis X.D. 39. offene Signaturen» erkennt Regel 7 der Runde 12 nicht. Sie
   stehen im Darin von X.D.30. und X.D.42.

## Einschätzung für den Gesamtimport

**Kritische Fehler: tragbar.**
- **Abdeckung:**
  - Jede der 715 Dateien ist mindestens einmal ganz am PDF geprüft (NP11/NP12).
  - Seit NP15 sind Schluss, Blatt Info und die nicht übernommenen Zeilen aller Dateien durchgesehen.
  - Die Gruppenenden sind mit dem engen Filter und in den gleichmässigen Dateien ganz abgesucht.
  - Suchläufe decken alle bisherigen Fehlerarten ab: Tippfehler in Dezimalsignaturen, «n.a» als Kind, Buchstaben in der
    Titelspalte, Nummern im Darin, Bearbeitervermerke, Stück ohne Nummer im Info, leere Teile. An Runde 13 treffen sie nur
    noch Bekanntes.
- **Stichproben:** Die Raten fallen von Stichprobe zu Stichprobe, 4 → 3 → 1 → 0 von je 60. Jeder Fund wurde in der nächsten
  Runde behoben, und zu seiner Art kam ein Suchlauf über alle Dateien.
  - Heute: 0 von 60 (KI 0–6 %). Die letzten beiden Stichproben zusammen: 1 von 120 (0,8 %, KI 0,1–4,6 %).
  - Hochgerechnet auf die rund 460 nicht erneut ganz geprüften Dateien sind das etwa 4 Dateien mit einem übersehenen
    kritischen Fehler (KI 0,5–21).
  - Was übrig bleibt, sind Einzelformen in der Gliederung, wie D3067, D177470, D845 und jetzt D3099. Jede trifft eine oder wenige
    Dateien.
- **Bekannte offene Fehler:** 10 bewusst offene Zeilen (K38–K45, K78, K117, K173) und K221. Sie sind dokumentiert und lassen
  sich nach dem Import von Hand nachführen.
- **Bedingung:** Die Prüfhinweise und das Blatt «Prüfliste» jeder Datei gehören in die Nachkontrolle nach dem Import. Die
  Einzelformen, die durchrutschen, zeigen sich dort am ehesten, etwa bei «Signatur taucht erneut auf» oder «Tippfehler?».

**Mittlere Fehler: häufig, aber nicht blockierend.**
- In der vierten Stichprobe hat fast jede dritte Datei (18 von 60) mindestens einen neuen mittleren Fehler. Es geht um Titel
  (Spalteninhalt im Titel, falsch getrennt), Zeitraum (aus Vermerken, Klammern, Doppeldaten) und Schachtel (nicht
  weitergegeben).
- Kein Text fehlt, und alles steht bei der richtigen Einheit. Die Fehler betreffen die Genauigkeit der Felder.
- Wenn die Genauigkeit von Titel und Zeitraum für den Import wichtig ist, lohnt eine Runde nur für die häufigsten mittleren
  Muster (siehe unten). Kritische Fehler lassen sich mit weiteren Nachprüfungen kaum noch finden: Die letzte Stichprobe fand
  keinen.

**Meine Empfehlung:**
1. K221 entscheiden. Wenn 1.2.6.: die kleine Ergänzung der Regel «fehlende Nachbarnummer» für Dezimalnummern am Listenende.
2. Optional eine Runde 14 nur für mittlere Muster. In der Reihenfolge des Nutzens:
   - Schachtel weitergeben über Abschnittsgrenzen (D2894, D3405, D2653, D1746, D2935);
   - die Fehlgriffe der Strich-Regel (D149825 Strich aus der Nachbarspalte, D3672 Doppelpunkt nach dem Zusammenfügen, D3468
     kurzer Rest) und die restlichen Trennungen (D10675 711.8/711.9, D1746 VI.6., D1589, D821, D4175);
   - Jahresklammern ohne Lebensdaten (D3561, D3512) und Zeiträume aus Vermerken (D2935, D3482);
   - Spaltendatum mitten im Titel (D149628: 94 Titel).
3. Danach den Gesamtimport. Für eine Runde 14 genügt eine Gegenprüfung ihrer Änderungen; eine weitere Zufallsstichprobe braucht
   es dafür nicht.

## Dateien

- `offen_kritisch.csv` (11 Zeilen); Stand vorher: `roh/np16_offen_kritisch_vorher.csv`.
- `funde_nachpruefung16.csv` (102 Zeilen: 1 neu kritisch, 1 entfällt (doppelt), 12 behoben, 62 mittel, 26 gering).
- `roh/np16_dateien_urteil.csv`: Dateiurteile aus G und Z.
- **`roh/np16_*`:**
  - Pakete G1–G3, Z1–Z3, ZL1, ZL2, S1 (Funde, Urteile, Dateiurteile, Notizen, Kandidaten, Änderungslisten);
  - Auftrag `np16_AUFTRAG16.md`;
  - Suchlaufergebnisse an Runde 13;
  - Vorbereitung und Kandidatenliste der Stichprobe.
- **`methode/np16_*`:** `start16.sh`, `mappen16.sh`, `klassifiziere_aenderungen.py`, `suchlauf_leere_teile.py`, `zusammen16.py`.
