# Nachprüfung 14: Gegenprüfung der Runde 11, Suchläufe und zweite Zufallsstichprobe (22.11.2026)

Geprüft sind:
- **Runde 11:** Skript `94ff40ba…` gegen 424a9976 (Runde 10), an den 18 geänderten Dateien und den Testdateien D152810 und
  D177470. Das ist der Stand jetzt im Projekt.
- **Suchläufe über alle 715 Dateien:** Tippfehler in Dezimalsignaturen, Stück ohne Nummer im Blatt Info, «n.a» als Kind,
  Buchstaben in der Titelspalte, neu «Gruppenende» und «Nummern im Darin».
- **Zweite Zufallsstichprobe:** 60 Dateien nach der vor Runde 11 festgelegten Regel, je ganz geprüft.

Die Ergebnisse stehen hier:
- `offen_kritisch.csv`: nachgeführt, mit stabilen K-Nummern, neu K203–K208, 16 Zeilen;
- `funde_nachpruefung14.csv`: 92 Zeilen;
- Rohdaten in `roh/np14_*`;
- Methode in `methode/ANLEITUNG_NACHPRUEFUNG14.md` und `methode/np14_*`.

## Kurz

- **Runde 11 wirkt vollständig.**
  - Alle 20 K-Zeilen in den geänderten Dateien sind behoben: die 19 der NP13 und K199 (D177470).
  - K200–K202 (D3012, D3038, D3089) entfallen nach dem Entscheid der Hauptsession: Buchstaben mit eigener Schachtel bleiben
    Einheiten.
  - Keine der 18 Dateien und keine Testdatei hat einen kritischen Fehler. Fehlgriffe der Regeln 2, 4, 5 und 9: keine.
  - Ein kleiner Rückschritt (mittel): In D177470 sind die Titel von 15. und 24. gekürzt.
- **Zweite Zufallsstichprobe: 3 von 60 Dateien haben einen kritischen Fehler (5 %, 95%-KI 2–14 %).**
  - Zusammen mit der ersten Stichprobe (NP13) sind es **7 von 120 (5,8 %, KI 2,9–11,6 %)**.
  - Hochgerechnet auf die 628 Dateien der Grundgesamtheit sind das etwa 31 Dateien (KI 11–86).
  - Einer der drei Fälle ist ein Grenzfall (D151210). Ohne ihn sind es 2 von 60.
  - Alle drei Fehler sind älter als Runde 11. Zwei sind Stücke ohne Nummer, die nur im Blatt Info stehen, in einer Form, die
    Regel 4 nicht kennt (D1729, D2502).
- **Suchläufe:**
  - Tippfehler, «Nummern im Darin», «n.a als Kind» und Buchstaben in der Titelspalte ergeben an Runde 11 nichts Neues.
  - «Gruppenende» findet 3 kritische Fälle: einen Bearbeitervermerk im Darin (D175949) und zwei Zeilen, die zur Gruppe
    gehören (D2951, D3099 als Grenzfall).
  - Der erweiterte Suchlauf «Stück ohne Nummer im Info» findet die Form der Stichprobenfälle nur in D1729 und D2502.
- **Offene kritische Fehler** (`offen_kritisch.csv`, Stand 94ff40ba): 16 Zeilen in 16 Dateien.
  - 10 sind bewusst offen.
  - Nicht bewusst offen sind 6 Zeilen in 6 Dateien, alle neu (K203–K208).
- **Einschätzung:** Die bekannten Fehler sind fast abgearbeitet. Die Stichproben zeigen aber, dass in etwa jeder zwanzigsten
  Datei ohne bekannte K-Zeile noch ein kritischer Fehler steckt. Es sind meist Einzelformen, die keine Regel kennt. Wie man
  sie gezielter findet, steht unter «Nächste Nachprüfung».

## Stände und Nachrechnung

| Stand | Lauf zellgleich | geändert gegenüber 424a9976 | Einheiten | Fallsets |
|---|---|---|---:|---|
| 94ff40ba (Runde 11) | ja, auch Testdaten und D151210 | 18 Dateien (= `runde11/geaenderte_dateien.txt`), Testdaten D152810 und D177470, D151210 unverändert | 51'602 (+94) | A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38 (unverändert) |

`runde11/vorher/` ist zellgleich mit meinem Lauf der Runde 10.

## Gegenprüfung der Runde 11 (G1, G2)

| Paket | Regeln | Dateien | Urteile | K-Zeilen erledigt | neu kritisch |
|---|---|---:|---|---|---:|
| G1 | 1, 5, 6, 7, 8, 9, 11 | 11 | 24: 23 besser, 1 gleich | 9 von 9 | 0 |
| G2 | 2, 3, 4, 10, Konvention 2 | 7 + 2 Testdateien | 113 Einträge: 110 besser, 1 gleich, 2 schlechter (mittel) | 11 von 11 | 0 |

- **D151150 (Regeln 1 und 5):** Die ganze Folge 9.144.–9.2501. ist per Skript gegen die PDF-Zeilen geprüft: 292 Einträge,
  292 Einheiten. Nummer, Titel, Jahre, Schachtel und Eltern stimmen. 9.501. «Mietauto für Fleischschau» ist eine eigene
  Einheit, die zweite 501 ist Teil 2 mit Hinweis.
  - Neu mittel: Bei Einträgen mit zwei Nummern in einer Zeile bleibt die zweite unerkannt (1516/1517, 1523/1524; bekannt
    412/415).
  - 9.1386. steht zweimal, und 1387 fehlt. Ich zähle das nicht als Fund, weil die Liste überall Lücken hat. Eine fehlende
    Nachbarnummer zeigt hier keinen Tippfehler an.
- **Regel 9 (Gruppenende):** Sie greift nur in D2620, dort richtig. Sonst hat sie nirgends gegriffen, auch nicht falsch. Sie
  ist aber zu eng (siehe Suchlauf «Gruppenende»).
- **Regeln 6–8, 11:**
  - D3412 hat eine Bestandszeile mit den 19 Einträgen, und 146/148 ist eine Einheit.
  - Die drei «lose verschachtelt»-Sätze stehen in Bestandszeilen.
  - «chr Stand» steht in D3808 und D3781 nur noch im Info.
- **Regel 2 (D3472):** 1952.9 und 1952.15 sind richtig. Die Regel hat keine echte Doppelnummer umgedeutet; die übrigen 37 Teile
  in D3472 und D3470 sind geprüft.
- **Regel 4:** Alle neuen Geschwister in D152817, D152810, D150589 und D3067 sind eigene Gegenstände mit eigenen Angaben.
- **Regel 10 (D10744):** Alle 156 Ebenen stimmen, 710 ist ein gewöhnlicher Code.
- **Konvention 2 (D177470):** Bei 27. und 28. fehlt in a)–h) nichts.
  - **Rückschritt (mittel):** Die Titel von 15. und 24. sind gekürzt, ihre zweite Titelzeile steht im Darin. Die neuen
    Darin-Zeilen verschieben den geschätzten rechten Rand der Textspalte.
- **Weitere mittlere Funde:**
  - D3470: Die Jahres-Tippfehlerregel aus Runde 8 ändert elf Signaturen samt Zeitraum, obwohl die Nummer durch den ganzen
    Bestand läuft. Das ist derselbe Grund wie bei Regel 3.
  - D2620 1.14.: Titel am Gedankenstrich abgebrochen.
  - D3774 6.4.: Schachtel 7, obwohl der Plan unter «Grossformate» steht.

## Suchläufe über alle 715 Dateien

| Suchlauf | Werkzeug | an Runde 10 (Probe) | an Runde 11 | Ergebnis |
|---|---|---|---|---|
| Tippfehler in Dezimalsignaturen | `methode/np13_suchlauf_tippfehler.py` | 7 Teil-Zeilen | 5 Teil-Zeilen | kein Fund (K135 mittel, Planlisten) |
| Nummern im Darin (Muster K144) | `methode/np14_suchlauf_nummern_im_darin.py` | 7 Läufe, darunter K144 mit genau 105 Zeilen | 6 Läufe | kein Fund (Übersichten, D3612 Liste wie NP12, D3828 Fehlanker) |
| Buchstaben in der Titelspalte | `methode/np13_suchlauf_buchstaben_titelspalte.py` | 27 Einheiten in 4 Dateien | 11 in 3 Dateien | kein Fund (eigene Schachtel: D3012, D3038, D3089) |
| «n.a» als Kind | `methode/np14_suchlauf_na_kind.py` | 52 Treffer | 29 Treffer | kein Fund (S1: Teile derselben Sache) |
| Gruppenende (Muster K196) | `methode/np14_suchlauf_gruppenende.py` | 17 Kandidaten, darunter K196 | 16 Kandidaten | 3 kritisch (S1) |
| Stück ohne Nummer im Info | `methode/np14_suchlauf_info_stuecke.py` | – | 24 Sätze | nur D1729 und D2502 (Stichprobe) |

- **Korrektur am Werkzeug:** «Nummern im Darin» konnte die Dossiers von D151150 zuerst nicht verankern. «Nr. im PDF» heisst
  dort «9.144.», im PDF steht aber nur «144». Mit einer dritten Verankerungsstufe (letzte Stelle) trifft der Suchlauf an
  Runde 10 genau die 105 Zeilen von K144 und an Runde 11 nichts mehr.
- **Gruppenende, Urteile von S1** (36 Kandidaten, davon 20 «n.a als Kind»):
  - **K203 D175949 Q.1 (kritisch):** Der Bearbeitervermerk «17. April 1998 béatrice wiggenhauser» steht im Darin der letzten
    Einheit, wie K169. Die Zeile «Letzte Ergänzung …» darunter steht richtig im Info.
  - **K204 D2951 2.14. (kritisch):** «N.B. Damit schliesst diese Briefsammlung. Nach der alten Numerierung fehlen die Briefe …»
    samt Folgeabsatz gehört zur Gruppe 2.
  - **K205 D3099 7.3.7. (kritisch, Grenzfall):** Der Filmvermerk «Enthält u.a. eine Filmrolle … zu Magazin „Klus“ und Werkplatz
    „Ennetbuck“ von 1941 …» steht auf der Höhe der Untereinheiten. Er ist nicht eingerückt wie eine Beschreibung von 7.3.7. und
    nennt auch 7.3.6. Er gehört wohl zur Gruppe 7.3. Bei 7.3.7. ergibt er zudem den Zeitraum 1941.
  - Kein Fund: die übrigen 13 Gruppenende-Kandidaten (gehören zur Untereinheit). Gering bis mittel: D152817 «[… nicht belegte
    Signaturen]» im Darin der vorigen Einheit, einmal im Titel von 97.
- **«n.a» als Kind:** Alle 20 Treffer sind Teile derselben Sache (D845 «124. Winter-Olympiade 1976» a)–g), D3161, D3470
  13.92.) oder Untergruppen ohne eigene Angaben bei «n.» (D3089 IV.2a/b).

## Zweite Zufallsstichprobe

- **Festgelegt vor Runde 11** (`np14/VORBEREITUNG14.md` im Scratchpad, Regel auch in `methode/ANLEITUNG_NACHPRUEFUNG14.md`):
  die ersten 60 Dateien ab Rang 74 der Reihenfolge der NP13. Ausgeschlossen sind die erste Stichprobe, die von Runde 11
  geänderten Dateien und die Dateien in `offen_kritisch.csv`.
  - Gezogen sind die Ränge 74–136 aus einer Grundgesamtheit von 628 Dateien (`roh/np14_zufall60_2.txt`).
- **Umfang:** 60 Dateien mit 6'854 Einheiten:
  - Z1–Z3: 57 kleinere Dateien mit 1'159 Einheiten;
  - ZL1: D151210 mit 3'161 Einheiten;
  - ZL2: D175996 mit 1'337 und D3466 mit 1'197 Einheiten.
- **3 kritisch:**
  - **K206 D1729:** «Der Archivbestand enthält noch eine Schachtel Hilfsregister Personalgeschäfte 1972 bis 1990.» steht nach
    der Bandliste nur im Blatt Info. Es fehlt eine Bestandszeile.
  - **K207 D2502:** «Der Bestand V.L.1. [Feuerassekuranz 1782 - 1925] umfasst neben den Brandassekuranzbüchern … noch 5
    Schachteln Assekuranzscheine, Tabellen und Rechnungen.» steht nach der Liste nur im Blatt Info. Gleich wie K119.
  - **K208 D151210 (Grenzfall):** Das Plakat «Juni-Festwochen 1952 … (Entwurf von Honegger-Lavater)» steht ohne Nummer nach
    13.4.7. Es ist kein Abstimmungsplakat wie 13.4.1.–7. und steht mit dem Abstand eines neuen Eintrags als letzter Eintrag
    der Gruppe 13.4. Unter 13.5. stehen solche Einträge ohne Nummer im Darin der Gruppe. Im Excel steht es im Darin von
    13.4.7. NP6 hatte den Fall als «fraglich» nicht gemeldet.
- **Sonst ohne kritischen Fehler:**
  - D175996 und D3466: Alle Signatur- bzw. Nummernzeilen entsprechen eins zu eins den Einheiten.
  - D151210: Alle Signaturzeilen sind Einheiten, in derselben Folge. Der Wortabgleich aller 14'036 PDF-Zeilen findet keinen
    Text bei einer fremden Einheit.
  - Früher kritische Fälle in Stichprobendateien sind behoben (K2, K106, K143, K150, K164, K174; D3466 :251., :168.).
- **Mittlere Funde** (47 Zeilen in der Stichprobe, davon etwa 14 neu, die übrigen aus NP6–NP12 bekannt):
  - Zeiträume aus Jahreszahlen, die kein Entstehungsdatum sind (Lebensdaten, Werktitel, «Vgl.»-Verweise, Lückenvermerke);
  - Titel am Seitenumbruch (D3466: Nummer als letzte Zeile einer Seite);
  - Bestandstitel mit dem Datum aus dem Katalog (D3533, D3684).
- **Zur Abstimmung vor dem Gesamtimport** (mittel, nicht gezählt):
  - D176824: Der Bestand heisst VII.308.A. statt VII.308. Hängt scope die Zeilen über die übergeordnete Signatur ein, stünden
    B.–I. unter A.
  - D2921 «7. Korrespondenzen»: Die nummerierten Briefgruppen stehen wie in D3612 als Liste im Darin.

## Neue kritische Zeilen (K203–K208)

| Muster | Zeilen | Fälle |
|---|---:|---|
| Stück ohne Nummer nur im Blatt Info (Form unbekannt) | 2 | K206 D1729, K207 D2502 |
| Zeile am Gruppenende bei der letzten Untereinheit | 3 | K204 D2951, K205 D3099 (Grenzfall), K208 D151210 (Grenzfall) |
| Bearbeitervermerk im Darin | 1 | K203 D175949 |

Alle sechs bestanden schon vor Runde 11.

## Hinweise zu Entscheiden der Hauptsession

- **Buchstaben mit eigener Schachtel bleiben Einheiten (K200–K202 entfallen):** In D3012 haben 1.b., 1.c. und 8.a. keine
  eigene Schachtel, nur ihre Geschwister. Ich habe «D3012 wie bisher» für die ganze Gruppe übernommen.
- **Regel 17:** wie entschieden. D151150 9.1386. ist wegen der vielen Lücken kein Fund.

## Vorschläge für Runde 12

1. **Regel 4, Stück ohne Nummer im Schlussteil** (K206, K207): auch «enthält noch …» und «umfasst neben … noch n Schachteln …».
   Allgemeiner: Ein Satz nach der letzten Einheit, der Archivgut mit Menge oder Behälter nennt (Schachtel, Band, Mappe,
   Ordner), kommt in die Bestandszeile. Ausnahme: Er verweist auf Material ausserhalb des Bestands (Bibliothek, andere
   Institution, anderer Bestand).
2. **Bearbeitervermerk «Datum Name»** am Schluss, ohne «/» (K203), ins Blatt Info.
3. **Regel 9, Gruppenende, erweitern:**
   - «N.B. …» in der Nummernspalte nach einer mehrzeiligen letzten Unternummer (K204);
   - ein Vermerk auf der Höhe der Unternummern, nicht eingerückt wie deren Beschreibung (K205);
   - ein Eintrag ohne Nummer nach der letzten Unternummer, der ein anderer Gegenstand ist (K208, Grenzfall). Gemeint ist ein
     anderes Plakat statt eines weiteren Abstimmungsplakats.
4. **D177470 15./24.:** den rechten Rand der Textspalte ohne die angehängten Buchstabenzeilen schätzen (mittel).
5. **Jahres-Tippfehlerregel der Runde 8:** wie Regel 9 nicht anwenden, wenn die Nummer durch den ganzen Bestand läuft
   (D3470, mittel).
6. **Zwei Nummern in einer Zeile** in einer Nr.-Spalte (D151150 1516/1517, 1523/1524) wie Regel 7 (mittel).
7. **Kleinere Fälle:** D3466 Nummer als letzte Zeile einer Seite (Titel aus der Folgeseite), D152817 Lückenvermerke, D3412
   «Nr.-», D2620 1.14. Titel, D3774 6.4. Schachtel.

## Nächste Nachprüfung (NP15)

- **Gegenprüfung der Runde 12** an den geänderten Dateien, mit K203–K208 als Altzeilen.
- **Gezielte Durchsicht statt Stichwortsuche:** Die Stichprobenfälle sind Einzelformen, die kein Suchwort trifft. Darum:
  - alle Sätze im Blatt Info aller 715 Dateien, die keine Bearbeitungsvermerke sind, einmal ganz durchsehen und einordnen
    (Stück des Bestands → Bestandszeile, Verweis, Geschichte);
  - das Darin der letzten Einheit jeder Datei auf Vermerke mit Datum und Name durchsehen;
  - alle Gruppenende-Kandidaten mit dem Abstand eines neuen Eintrags (nicht nur grösserem) sichten.
- **Dritte Zufallsstichprobe** von 60 Dateien ab Rang 137 derselben Reihenfolge. Zusammen sind es dann 180 Dateien, das
  Intervall wird enger.

## Dateien

- `offen_kritisch.csv`: 16 Zeilen.
  - Die K-Nummern bleiben; neu sind K203–K208.
  - 20 behobene Zeilen und K200–K202 (entfällt) sind entfernt. Die Liste davor (33 Zeilen) liegt in
    `roh/np14_offen_kritisch_vorher.csv`.
- `funde_nachpruefung14.csv`: 92 Zeilen, mit Paket, K-Nummer und Entscheid.
- `roh/np14_*`:
  - Pakete G1, G2, Z1–Z3, ZL1, ZL2, S1 (Funde, Urteile, Dateiurteile, Notizen, Kandidaten);
  - `np14_dateien_urteil.csv`, Vergleiche Runde 10 → 11 in `np14_vgl/`;
  - Suchläufe an Runde 10 und 11;
  - Stichprobe `np14_zufall60_2.txt`, `np14_geaendert_r11.txt`, `np14_vorfunde.md`, `np14_AUFTRAG14.md`.
- `methode/ANLEITUNG_NACHPRUEFUNG14.md` und `methode/np14_*` (Suchläufe, Zusammenführen, Ablaufskripte).
