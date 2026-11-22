# Nachprüfung 15: Gegenprüfung der Runde 12, Durchsicht aller Dateien am Schluss und im Info, dritte Zufallsstichprobe (22.11.2026)

Geprüft sind:
- **Runde 12:** Skript `439a6fbf…` gegen 94ff40ba (Runde 11), an den 18 geänderten Dateien. Die zwei geänderten Testdateien
  (D151210, D177470) sind zellgleich mit diesen Dateien. Das ist der Stand jetzt im Projekt.
- **Durchsicht aller 715 Dateien** an den Stellen, an denen die zuletzt übersehenen Fehler sassen:
  - alle PDF-Zeilen ab der letzten Einheit mit ihrem Ort in der Excel;
  - alle Schlussvermerke im Blatt Info;
  - alle nicht übernommenen Zeilen (Text vor der ersten Signatur, Überschriften ohne Signatur, Zeilen mit fehlenden Wörtern).

  Das ist kein Suchlauf mit Muster, sondern eine Durchsicht jeder Datei (Pakete D1–D8).
- **Suchläufe über alle 715 Dateien:**
  - die bisherigen;
  - neu «Gruppenende mit dem Abstand eines neuen Eintrags», mit engem Filter, wie von der Hauptsession gewünscht;
  - neu «Bearbeitervermerk im Darin».
- **Dritte Zufallsstichprobe:** 60 Dateien nach der vor Runde 12 festgelegten Regel, je ganz geprüft.

Die Ergebnisse stehen hier:
- `offen_kritisch.csv`: nachgeführt, mit stabilen K-Nummern, 22 Zeilen. Behoben sind K203–K208, neu sind K209–K220.
- `funde_nachpruefung15.csv`: 109 Zeilen.
- Rohdaten in `roh/np15_*`. Darunter sind die Pakete, die Dateiurteile aller 715 Dateien (`roh/np15_dateien_urteil.csv`)
  und die vor Runde 12 festgelegte Kandidatenliste der Stichprobe (`roh/np15_kandidaten_ab137.txt`).
- Methode in `methode/ANLEITUNG_NACHPRUEFUNG15.md` und `methode/np15_*`.

## Kurz

- **Runde 12 wirkt vollständig.**
  - K203–K208 sind behoben und am PDF bestätigt.
  - Keine der 18 Dateien hat einen kritischen Fehler.
  - Fehlgriffe der Regeln 1–9 gibt es keine. Besonders geprüft sind Gruppenende (a) und (b), zwei Nummern, Lückenvermerke
    und Seitenwechsel.
  - Ein Rückschritt ist mittel: In D3099 hat die Gruppe 7.3. keinen Zeitraum mehr, und 7. beginnt erst 1963 statt 1941.
    Seit der Filmvermerk im Darin der Gruppe steht, fehlt er der Schätzung; Gruppen schätzen nie aus dem eigenen Darin.
- **Die Durchsicht findet 11 neue kritische Zeilen in 11 Dateien** (K209–K219).
  - 7 davon waren früher als mittel gemeldet oder gewertet. Nach den heutigen Konventionen sind sie kritisch: K169
    (Bearbeitervermerk im Darin) und Bestandszeile für Stücke ohne Nummer.
  - Ein Fall ist ein Konventionsfall (D1759).
  - Zwei Fälle waren früher gesehen, aber nicht als Fehler gewertet (D1481, D414).
  - Nur ein Fall ist ganz neu (D2575).
  - Alle Fälle stehen am Schluss der Datei, also dort, wohin die Durchsicht zielte.
  - In den 60 Stichprobendateien fand die Durchsicht nichts. Das deckt sich mit der Stichprobe.
- **Dritte Zufallsstichprobe: 1 von 60 Dateien hat einen kritischen Fehler (1,7 %, 95%-KI 0,3–8,9 %).** Es ist D845 (K220):
  fünf erfundene leere Teile aus den Köpfen der Unterverzeichnisse.
  - Alle drei Stichproben zusammen ergeben **8 von 180 (4,4 %, KI 2,3–8,5 %)**.
  - Hochgerechnet auf die 572 Dateien der Grundgesamtheit der dritten Stichprobe sind es etwa 10 Dateien (KI 2–51).
- **Suchläufe:**
  - Die bisherigen Suchläufe bringen nichts Neues.
  - Der enge Filter «Gruppenende» enthält an Runde 10 alle fünf bekannten Fälle. An Runde 12 ist kein Kandidat ein Fund.
  - In den vier gleichmässig gesetzten Dateien sind dazu alle 497 Gruppenenden abgesucht. Dort steht nur K208, und das ist
    behoben.
- **Offene kritische Fehler** (`offen_kritisch.csv`, Stand 439a6fbf): 22 Zeilen in 22 Dateien.
  - 10 sind bewusst offen.
  - Nicht bewusst offen sind 12 Zeilen in 12 Dateien, alle neu (K209–K220).
- **Einschätzung:**
  - Mit Runde 13 sind die bekannten Fehler abgearbeitet. Schluss, Blatt Info und Gruppenenden sind dann in allen Dateien
    systematisch geprüft.
  - Übrig bleiben Fehler in der Gliederung in Einzelformen. In den Stichproben waren es 3 von 180 (D3067 «n.a», D177470
    Buchstaben, D845 leere Teile; 1,7 %, KI 0,6–4,8 %).
  - Auf die rund 500 nie ganz in einer Stichprobe geprüften Dateien gerechnet, sind das etwa 9 Dateien (KI 3–25).

## Stände und Nachrechnung

| Stand | Lauf zellgleich | geändert gegenüber 94ff40ba | Einheiten | Fallsets |
|---|---|---|---:|---|
| 439a6fbf (Runde 12) | ja, auch Testdaten und D151210 | 18 Dateien (= `runde12/geaenderte_dateien.txt`), Testdaten D177470, D151210 (nur 13.4./13.4.7.) | 51'605 (+3 Bestandszeilen) | A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38 (unverändert) |

`runde12/vorher/` ist zellgleich mit meinem Lauf der Runde 11.

## Gegenprüfung der Runde 12 (G1, G2)

| Paket | Regeln | Dateien | Urteile | K-Zeilen erledigt | neu kritisch |
|---|---|---:|---|---|---:|
| G1 | 3b, 4, 5, 6, 8, 9 | 6 (D151150, D151210, D3466, D3470, D177470, D3774) | 34 Einheiten: 30 besser, 3 gleich, 1 schlechter (gering, angekündigt) | K208 | 0 |
| G2 | 1, 2, 3a, 7 | 12 | 47 Einträge: 44 besser, 4 gleich, 1 schlechter (mittel) | K203–K207 | 0 |

- **Regel 3, Gruppenende:**
  - (a) D2951 2.: Umgehängt ist genau der Vermerk samt Folgezeilen. 2.4. und 2.9. sind zellgleich mit Runde 11.
  - (a) D3099 7.3.: ebenso. Der Schlussvermerk «Ergänzung (7.3., 7.5.1.), 27. März 2013» bestätigt die Zuordnung.
  - (b) D151210 13.4.: Umgehängt sind genau die zwei Plakatzeilen. 13.5. und der Rest der Datei sind unverändert.
  - Neu mittel, Ursache Regel 3: In D3099 fehlt der Zeitraum von 7.3., und 7. beginnt 1963 statt 1941. Gruppen schätzen
    ihren Zeitraum nicht aus dem eigenen Darin (0 Fälle in 715 Dateien). Dasselbe gab es in NP3 als M09; in NP4 war es
    behoben.
- **Regel 6, zwei Nummern (D151150):** 412/415, 1516/1517 und 1523/1524 sind je eine Tabellenzeile mit einem Titel, einem
  Zeitraum und einer Schachtel. Die Titel sind ganz. Ein Skript findet keinen weiteren solchen Fall.
- **Regel 7, Lückenvermerke:** Alle 16 Vermerke stehen als Hinweis bei der nächsten Nummer. Kein Inhalt fehlt.
- **Regel 8, Seitenwechsel (D3466):**
  - Bei allen 10 Einheiten ist die erste Zeile der neuen Seite Inhalt. Grenzfall ist nur 132./T4, höchstens gering.
  - Ein Skript hat alle 69 Einheiten geprüft, die über einen Seitenwechsel reichen. Die erste neue Zeile steht noch zweimal im
    Titel, beide bekannt: 584./T19, und 131./T5 aus dem Muster «1921 &» (mittel seit NP4).
  - Fälle, an denen die Regel hätte greifen müssen und nicht griff, gibt es also keine.
- **Regel 5 (D3470):** Die 11 Signaturen stehen wie im PDF; der Zeitraum ist das Jahr der Signatur. Die Laufnummer läuft in
  64 von 66 Jahreswechseln weiter.
- **Regeln 1, 2, 4, 9:**
  - Die Bestandszeilen in D1729, D2502 und D152401 enthalten den ganzen Satz, und das Blatt Info stimmt.
  - Zu Entscheid 1: In D152401 ist das Total 20 die Summe ohne die zusätzliche Schachtel. Die Begründung «zählt die Schachtel
    zum Total» trifft also nicht zu, das Ergebnis bleibt richtig.
  - Regel 4: D177470 15. und 24. sind wieder ganz, 27. c) ist richtig zusammengefügt.
  - Regel 9: D3774 6.4. hat keine Schachtel mehr.
- **Gering:**
  - D177470 28. e) und f): das «; » fehlt, angekündigt.
  - Das Zitat im Hinweis bei D151210 13.4. und D2951 bricht nach 60 Zeichen mitten im Wort ab.

## Durchsicht Schluss und Info (D1–D8)

Für jede der 715 Dateien gab es einen Block (`methode/np15_durchsicht_schluss_info.py`). Er enthält alle Zeilen der Prüfmappe
ab der Signaturzeile der letzten Einheit, mit ihrem Ort in der Excel und der Marke «⇣» für einen grossen Abstand. Dazu kommen
die letzte Einheit, die Bestandszeile, die übrigen Schlussvermerke, die Liste «Nicht übernommen» und «Signaturen nur im
Vorspann». Das sind 1,18 Mio. Zeichen in 8 Teilen. Jeder Verdacht wurde an der Prüfmappe und am PDF bestätigt.

| Paket | Dateien | kritisch (neu / bekannt) | neu kritisch |
|---|---:|---|---|
| D1 | 100 | 1 / 1 (K38) | D1481 |
| D2 | 143 | 1 / 1 (K39) | D1759 |
| D3 | 121 | 2 / 2 (K40, K173) | D2575, D2508 |
| D4 | 75 | 1 / 2 (K41, K117) | D2630 |
| D5 | 70 | 1 / 1 (K42) | D3231 |
| D6 | 60 | 0 / 0 | – |
| D7 | 63 | 3 / 2 (K44, K78) | D3604, D3742, D3767 |
| D8 | 83 | 2 / 1 (K45) | D631, D414 |

Die 10 bewusst offenen Zeilen sind alle noch da. Die behobenen K203–K207 sind auch in der Durchsicht weg.

**Die neuen kritischen Zeilen nach Art:**

| K | Datei | Art | Befund | früher |
|---|---|---|---|---|
| K209 | D1481 | Stück ohne Nummer nur im Info | «Die Protokolle von 1971 bis 1987 sind lückenhaft in einer Archivschachtel.» (Familie der Regel 6 der Runde 11) | NP11 als Bestandsnotiz durchgelassen |
| K210 | D1759 | Stück ohne Nummer nur im Info | «Die dazugehörigen vier Compact Discs wurden in den Archivbestand integriert.» | Konventionsfall: K110 (NP12) hatte als Soll den ganzen Schlussabsatz im Info |
| K211 | D2575 | Stück ohne Nummer nur im Info | «Des Weiteren enthält der Bestand vereinzelte Dokumente, die nicht ins „Acten-Verzeichnis“ aufgenommen wurden.» | neu |
| K212 | D2508 | Umfangssatz im Darin der letzten Schachtel | «Der Bestand der Politischen Flugblätter … umfasst 16 Archivschachteln.» (SCHLUSS_RE erlaubt nur 3 Wörter zwischen «Der Bestand» und «umfasst») | NP10 mittel; wie K75 |
| K213 | D2630 | Bearbeitervermerk im Darin der letzten Einheit | «Erstellt und bearbeitet von cca / 20. Juni 2000» | NP12 mittel, vor K169; auch mein Vorfund V1 |
| K214 | D3231 | Bearbeitervermerk im Darin, Grenzfall | «(Nachlieferung verzeichnet 29.3.1993/Anna Pia Maissen)» mitten im Verzeichnis bei 2.8. Teil 12; bestimmt dessen Zeitraum | NP12 nur der Zeitraum als mittel |
| K215 | D3604 | Bearbeitervermerk im Darin der letzten Schachtel | «13. September 2002 / lic. phil. Karin Beck» | NP10 mittel |
| K216 | D3742 | Albumschluss bei Porträt 22, Inschrift weg | «Letztes Blatt (schwarz kalligraphiert):» im Darin von 22., «AUSGEFÜHRT / VON R. GANZ PHOT. / ZÜRICH» nur im Blatt Vollständigkeit | NP10 mittel |
| K217 | D3767 | Beilagen des Albums beim letzten Foto | «Beilagen (3 Farbbildchen)» mit drei Bildern im Darin von 37. (Signalwort nur «Beilagen:» mit Doppelpunkt) | NP11 von der Hauptsession herabgestuft, vor dem Entscheid zur Bestandszeile |
| K218 | D631 | Bearbeitervermerk im Darin der Bestandszeile | «Ende Juli 2004 / Dr. Robert Dünki» (SCHLUSS_DATUM_RE verlangt eine Tageszahl) | NP12 mittel |
| K219 | D414 | Absatz zu den Faszikeln nur im Info, Grenzfall | «Der Inhalt der einzelnen Faszikel ist nicht verzeichnet. Ein rotes D + Datum …» mit 36 Sitzungstagen, nach XV.; beschreibt I.–XV. von Schachtel 5 | seit NP13 als «Schlussabsatz im Info» bekannt |

**Kein Fund, aber zur Kenntnis:**
- D3273 «Alle Dokumente liegen in Photokopie bei.» gehört zur Vorbemerkung und beschreibt die Form der Stücke, kein weiteres
  Stück.
- D140969 «(neu archiviert von Prof. Werner G. Zimmermann im August 1990)» steht unter dem Kopf der Gruppe 59–81, also richtig.
  Anders ist es bei K214, wo der Vermerk mitten in der Liste steht und dem falschen Teil zugeschlagen wird.

## Suchläufe über alle 715 Dateien

| Suchlauf | Werkzeug | Runde 11 | Runde 12 | Ergebnis |
|---|---|---|---|---|
| Tippfehler in Dezimalsignaturen | `methode/np13_suchlauf_tippfehler.py` | wie NP14 | unverändert | nichts Neues |
| Stück ohne Nummer im Info | `methode/np14_suchlauf_info_stuecke.py` | 24 Sätze | 21 Sätze in 17 Dateien | D1729, D2502 weg (behoben) |
| Buchstaben in der Titelspalte | `methode/np13_suchlauf_buchstaben_titelspalte.py` | 11 | 11 (D3012, D3038, D3089) | Konvention, kein Fund |
| «n.a» als Kind | `methode/np14_suchlauf_na_kind.py` | wie NP14 | unverändert | nichts Neues |
| Nummern im Darin | `methode/np14_suchlauf_nummern_im_darin.py` | 6 Läufe | 6 Läufe, gleich | kein Fund (wie NP14) |
| Gruppenende, Faktor 1,3 | `methode/np15_suchlauf_gruppenende.py` | 16 | 11 | weg sind K203, K204, K205 und die 2 Lückenvermerke in D152817 |
| **Gruppenende, enger Filter** (neu) | `methode/np15_suchlauf_gruppenende_eng.py` | 198 (R10: 199) | 192 | S1: kein Fund |
| **Bearbeitervermerk im Darin** (neu) | `methode/np15_suchlauf_vermerk_im_darin.py` | 225 | 224 | D2630 (K213); die übrigen meist Werktitel «bearbeitet von …» |
| Datenträger und «integriert» im Info und in «Nicht übernommen» | einmalig | – | 31 | nur D1759 (K210) |

**Gruppenende mit engem Filter, für die Hauptsession:**
- **Das Werkzeug:** Es nimmt alle Zeilen nach der letzten Untereinheit mit dem Abstand eines neuen Eintrags (Faktor 1,0) und
  bestimmt ihre Lage gegenüber Signatur, Titelspalte und Zeilen davor.
  - Weg fallen Zeilen, die wie die Zeilen davor oder wie der Inhalt der Geschwister stehen.
  - Gemeldet werden A «links vom Text», B «Textspalte, gleich nach der Untereinheit», B2 «eingerückt wie davor, aber neuer
    Absatz» und E «sonst».
- **An Runde 10:** 199 Kandidaten. Darunter sind alle fünf bekannten Fälle: K196 B, K203 A, K204 A, K205 A, K208 B2.
- **An Runde 12:** 192 Kandidaten, davon 150 in vier gleichmässig gesetzten Dateien. S1 hat jeden Kandidaten geprüft; kein
  Fund.
- **Noch engerer Filter, Vorschlag von S1** (q = Abstand / üblicher Abstand):
  - A nur mit q ≥ 1,5 und (Geschwister nur ein Absatz oder Zeilen davor);
  - B nur mit q ≥ 1,3 und Geschwister nur ein Absatz;
  - B2 nur, wenn die Geschwister nur einen Absatz haben;
  - E weglassen.

  An Runde 10 bleiben damit 8 von 199 Kandidaten, darunter alle fünf bekannten und die 2 Lückenvermerke. An Runde 12 bleibt
  einer, D151730 8.2., und der ist kein Fund. Der Filter ist an nur 5 Fällen geeicht; er taugt zum Sichten, nicht als Regel.
- **Lücke des Suchlaufs:** Er meldet je Gruppe nur die erste passende Zeile. In gleichmässigen Dateien ist das immer der
  eigene erste Absatz der Untereinheit.
  - S1 hat darum in D141020, D149628, D4054 und D151210 alle 497 Gruppenenden abgesucht. Bei den 115 mit mehreren Absätzen
    hat S1 den letzten Absatz angesehen.
  - Gefunden hat S1 nur K208, behoben.

**Bearbeitervermerk im Darin:** Der Suchlauf findet die Form «Erstellt und bearbeitet von <Kürzel> / <Datum>» (D2630).
Diese Formen findet er nicht; die Durchsicht hat sie gefunden:
- «<Datum> / lic. phil. <Name>» (D3604);
- «Ende Juli 2004 / <Name>» (D631);
- «(Nachlieferung verzeichnet <Datum>/<Name>)» (D3231).

## Dritte Zufallsstichprobe

- **Regel:** vor Runde 12 festgelegt (`roh/np15_VORBEREITUNG15.md`, Kandidatenliste `roh/np15_kandidaten_ab137.txt`,
  sha256 `0dc385e7…`).
  - Gezogen wurden die ersten 60 Dateien ab Rang 137 derselben Reihenfolge, die nicht in Stichprobe 1 oder 2 sind, nicht in
    `offen_kritisch.csv` (Stand NP14) stehen und von Runde 12 nicht geändert sind.
  - Das sind die Ränge 137–196 (`roh/np15_zufall60_3.txt`).
  - Grundgesamtheit: 715 − 120 − 16 − 10 = 572 Dateien.
- **Umfang:** 60 Dateien mit 2'627 Einheiten, je ganz geprüft:
  - Z1: 20 Dateien mit 575 Einheiten;
  - Z2: 19 Dateien mit 575 Einheiten;
  - Z3: 19 Dateien mit 574 Einheiten;
  - ZL1: D150829 mit 518 und D3170 mit 385 Einheiten.
- **1 kritisch (1,7 %, KI 0,3–8,9 %): D845 (K220).**
  - Die «Übersicht» :1.–:124. auf S. 1–5 trägt die Unternummern.
  - Die fetten Köpfe der Unterverzeichnisse zu :1., :44., :92., :95. und :124. werden je eine leere Einheit «Teil 2», ohne
    Darin und ohne Kinder (ID 2, 95, 148, 156, 196).
  - Die Regel «erste Nennung war nur eine Übersichtszeile» gilt nur im Modus dezimal; D845 läuft als Vollsignatur. Derselbe
    Fall war D3190 9. (NP11 kritisch, behoben).
  - Ein Suchlauf über alle Dateien findet sonst nur D1880. Dort haben die Teile eigene Schachteln oder «[leer]» aus dem PDF;
    das ist kein Fund.
- **Hochrechnung:** 1/60 auf 572 Dateien gibt etwa 10 (KI 2–51). Alle drei Stichproben zusammen: 8 von 180 (4,4 %, KI
  2,3–8,5 %).
- **Nach Art der Fehler in den 8 Stichprobenfällen:**
  - Schluss oder Info: D151759, D1729, D2502. Diese Stellen sind jetzt in allen Dateien durchgesehen.
  - Gruppenende: D2620, D151210. Die Gruppenenden sind jetzt mit dem engen Filter und in den gleichmässigen Dateien ganz
    abgesucht.
  - Gliederung in Einzelformen: D3067, D177470, D845.
- **Mittel und gering:** 53 mittlere und 37 geringe Fundzeilen in allen Paketen, die meisten aus NP9–NP12 bekannt und offen.
  Häufigstes Muster ist «Titel falsch»: Folgezeilen der Titelspalte im Darin oder erste Unterzeile am Titel.
  - **Titel am Gedankenstrich abgebrochen,** wie D2620 1.14.: neu in D150829 1.6., 5.5.18., 6.3. und D3170 4.2.1.6.
  - **Weitere neue mittlere Fälle:**
    - D150829 5.1. «Seepark»: Zeitraum 1899–2000 aus dem Darin statt 1956–1990 aus der Datumsspalte;
    - D150829 2.6. und 4.1.51.: «vom 15. und 31. Juli»;
    - D150829 4.1.79. und 4.2.117.: am Doppelpunkt geteilt;
    - D3548 6.13. und 6.21.: Zeiträume;
    - D174277 :6–:34: Zeitraum aus dem Ablieferungsdatum, 29 Einheiten;
    - D3089 VIII.2.: Schachtelköpfe verworfen;
    - D2839: Tag und Monat aus der Datumsspalte entfallen, seit dem 19.11. bekannt;
    - D151735: Inhaltsangabe für 12 Schachteln nur in «Nicht übernommen».

## Neue kritische Zeilen (K209–K220)

| K | Datei | Muster | Paket | Status |
|---|---|---|---|---|
| K209 | D1481 | Text weg (Bestandszeile fehlt) | D1 | neu bewertet (NP11 durchgelassen) |
| K210 | D1759 | Text weg (Bestandszeile fehlt) | D2 | Konventionsfall |
| K211 | D2575 | Text weg (Bestandszeile fehlt) | D3 | neu |
| K212 | D2508 | Inhalt bei falscher Einheit | D3 | Umwertung (NP10 mittel) |
| K213 | D2630 | Inhalt bei falscher Einheit | D4 (auch V1) | Umwertung (NP12 mittel) |
| K214 | D3231 | Inhalt bei falscher Einheit | D5 | Grenzfall |
| K215 | D3604 | Inhalt bei falscher Einheit | D7 | Umwertung (NP10 mittel) |
| K216 | D3742 | Inhalt bei falscher Einheit, Text weg | D7 | Umwertung (NP10 mittel) |
| K217 | D3767 | Inhalt bei falscher Einheit | D7 | Umwertung (NP11 herabgestuft) |
| K218 | D631 | Inhalt bei falscher Einheit | D8 | Umwertung (NP12 mittel) |
| K219 | D414 | Text weg | D8 | Grenzfall (seit NP13 gesehen) |
| K220 | D845 | Einheit erfunden | Z1 | neu |

## Fragen an die Hauptsession

1. **K210 D1759:** Die vier CDs, «in den Archivbestand integriert», nennt keine Einheit. Gehören sie nach Entscheid 1 der
   Runde 12 in eine Bestandszeile? Die Soll von K110 (NP12) war der ganze Absatz im Info. Ich empfehle die Bestandszeile, nur
   für den CD-Satz.
2. **K217 D3767:** In NP11 hast du die Beilagen herabgestuft, vor dem Entscheid zur Bestandszeile. Nach heutiger Konvention
   ist es kritisch. Bitte bestätigen.
3. **K219 D414 (Grenzfall):** Der Absatz nach XV. beschreibt die Faszikel I.–XV. von Schachtel 5: was nicht verzeichnet ist,
   was die Markierung bedeutet, 36 Sitzungstage. Ich empfehle das Darin von Schachtel 5, mit Hinweis, wie beim Gruppenende.
4. **K214 D3231 (Grenzfall):** Der Vermerk steht mitten im Verzeichnis, am Ende des Blocks 2.8. Ich empfehle das Blatt Info
   wie K169, wenigstens nicht bei Teil 12.
5. **Mittel, zur Abstimmung:**
   - D10649 «Eine Fotokopie der einzelnen Bilder liegt bei.» ist ein Satz der Vorbemerkung. Als Beilage wäre er kritisch.
   - D69 28. und D65 21.: Der Verweis «Fortsetzung der Rechnung vgl. IV.C. …» steht im Darin der letzten Nummer, gehört aber
     zur Gruppe bzw. zum Bestand. Es ist derselbe Fall wie D67 III.Q.33., der bisher mittel ist.
   - D2589 19.: «Gedruckte Exemplare (Lichtdruck):» ist das einzige Darin. NP12 wertete es als mittel, Grenzfall.

## Vorschläge für Runde 13

1. **Bearbeitervermerke am Schluss oder mitten im Verzeichnis** (K213, K215, K218, K214) ins Blatt Info. Diese Formen sind
   neu:
   - «Erstellt und bearbeitet von <Kürzel> / <Datum>»;
   - «<Datum> / lic. phil. <Name>» in einer Schachteltabelle ohne Signaturen;
   - «Ende Juli 2004 / <Name>», also ohne Tageszahl, in der Bestandszeile;
   - «(Nachlieferung verzeichnet <Datum>/<Name>)» in Klammern mitten im Verzeichnis.
2. **Stück ohne Nummer im Schlussteil** (K209, K210, K211, K217) in die Bestandszeile. Neu sind:
   - «Die Protokolle von … bis … sind lückenhaft in einer Archivschachtel.»;
   - «Die dazugehörigen vier Compact Discs wurden in den Archivbestand integriert.» (nur dieser Satz; der Rest des Absatzes
     bleibt im Info);
   - «Des Weiteren enthält der Bestand vereinzelte Dokumente, die nicht ins „Acten-Verzeichnis“ aufgenommen wurden.»;
   - «Beilagen (3 Farbbildchen)» ohne Doppelpunkt, mit Aufzählung.
3. **Umfangssatz zum Bestand** (K212): Bei «Der Bestand … umfasst n Archivschachteln.» kann der Bestandsname länger sein als
   drei Wörter. Der Satz kommt ins Info.
4. **Albumschluss** (K216): «Letztes Blatt (…):» mit der Inschrift danach gehört in die Bestandszeile. Die Inschrift in
   Kapitälchen ist keine Überschrift.
5. **Absatz am Dateiende, der die Faszikel einer Gruppe beschreibt** (K219): ins Darin der Gruppe, mit Hinweis. Regel 3 der
   Runde 12 greift nur vor einer nächsten Nummer.
6. **Übersicht mit Unterverzeichnissen im Modus Vollsignatur** (K220): Die Köpfe der Unterverzeichnisse sind keine Teile.
   Die Regel «erste Nennung war nur eine Übersichtszeile» sollte auch hier gelten.
7. **Mittel:**
   - D3099 7.3.: Eine Gruppe sollte ihren Zeitraum auch aus dem eigenen Darin schätzen, wenn es keine Kinder mit Zeitraum gibt.
     Das ist der Rückschritt der Runde 12.
   - Gedankenstrich am Zeilenende (D2620 1.14., D150829 1.6., 5.5.18., 6.3., D3170 4.2.1.6.): Die fünf Fälle zusammen sind
     vielleicht genug für eine enge Regel, die D151210 nicht berührt.
   - Titel am Doppelpunkt geteilt (D150829 4.1.79., 4.2.117.).
   - Ereignisdatum mit zwei Tagen «vom 15. und 31. Juli» (D150829 2.6., 4.1.51.).
   - Zeitraum aus dem Ablieferungsvermerk: D174277 mit 29 Einheiten, D2915 9.1./9.2.

## Nächste Nachprüfung (NP16)

1. **Gegenprüfung der Runde 13** an den geänderten Dateien, Altzeilen K209–K220.
2. **Suchlauf zu Muster K220** (leere Teile aus Köpfen von Unterverzeichnissen) und **Strukturbericht über alle Dateien**:
   - Teile ohne Darin, Schachtel und Zeitraum;
   - Einheiten, deren Kinder nach dem Kopf eines Unterverzeichnisses stehen.
3. **Vierte Zufallsstichprobe** ab Rang 197 nach derselben Regel. Mit 240 Dateien wird das Intervall für die Restrate
   enger.
4. **Für den Gesamtimport ist zu entscheiden,** ob die Restrate für Einzelformen in der Gliederung tragbar ist. Heute sind es
   etwa 1,7 %, also rund 9 Dateien (KI 3–25). Der Rest ist systematisch geprüft.

## Dateien

- `offen_kritisch.csv` (22 Zeilen); Stand vorher: `roh/np15_offen_kritisch_vorher.csv`.
- `funde_nachpruefung15.csv` (109 Zeilen: 12 neu kritisch, 1 entfällt (doppelt), 6 behoben, 53 mittel, 37 gering).
- `roh/np15_dateien_urteil.csv`: Dateiurteile aus G, Z und allen 715 Dateien der Durchsicht.
- **`roh/np15_*`:**
  - Pakete G1, G2, D1–D8, Z1–Z3, ZL1, S1 und V1 (Funde, Urteile, Dateiurteile, Notizen, Kandidaten);
  - Auftrag `np15_AUFTRAG15.md`;
  - Suchlaufergebnisse an Runde 12;
  - Vorbereitung und Kandidatenliste der Stichprobe.
- **`methode/np15_*`:**
  - `start15.sh`, `mappen15.sh`;
  - `durchsicht_schluss_info.py`;
  - `suchlauf_gruppenende.py` (mit Faktor), `suchlauf_gruppenende_eng.py`, `suchlauf_vermerk_im_darin.py`;
  - `zusammen15.py`.
