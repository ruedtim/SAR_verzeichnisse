# Runde 8 – Änderungen und Bitte um Nachprüfung 10

Stand 22.11.2026. Skript `findmittel_zu_scope.py` sha256 `7fa7e1613a528651…`. Aufbau: Stand nach dem Nachtrag zu
Runde 7 (`e896fb6c…`, gepusht als main 844ccb6) plus diese Runde.

`findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind mit diesem Skript neu erzeugt.

## Worum es ging

Ziel des Users: weiter verbessern, bis die Nachprüfung keine kritischen Fehler mehr findet. Grundlage ist
`stichproben/offen_kritisch.csv` aus Nachprüfung 9 (K1–K29). Behoben sind:

- alle 22 kritischen Fälle, die nicht bewusst offen sind: K1–K11 und K19–K29;
- ein neuer kritischer Fall aus einem eigenen Suchlauf: D3470, 1391 Einheiten fehlten;
- ein Einzelfall aus demselben Suchlauf: D1924, Schachtel «101»;
- einige mittlere Funde aus Nachprüfung 9, die dieselbe Ursache hatten.

Weiter bewusst offen sind K12–K18 (D149622, D1739, D1858, D2614, D3208, D3828 3.4., D512).

Kennzahlen:

- Einheiten 48'920 → 50'387. Das Plus kommt aus D3470 (+1388), D1880 (+41), D1746 (+19), D3012 (+9) usw.
- «[ohne Titel]» 30 = 30.
- «Text erfasst 100 %» 695 = 695.
- Doppelte Schlüssel 10 = 10.
- Tracebacks 0.

**Geändert sind 59 Dateien** (`geaenderte_dateien.txt`, Zellvergleich in `zellvergleich_runde7_runde8.txt`). Ihr
Stand vorher liegt in `vorher/` (nicht im Repository), der neue in `findmittel_excel/`.

**D151210 und alle Testdaten sind zellgleich mit vorher.**

Fallsets gegenüber `e896fb6c`:

- unverändert: A 11/12, C 9/12, F 5/7, Punkt 2 38/38.
- B 36 → 34 und Runde 2 33 → 31. Die vier Fälle sind beabsichtigt:
  - B D3089 X. und B D3012 c.: Das Werkzeug vergleicht über die ID, und die IDs haben sich verschoben. X. hat jetzt
    1866–1956, wie es Nachprüfung 9 verlangt.
  - Runde 2 D1880 H.II.: «Bullinger-Denkmal …» steht jetzt in H.II.h. Teil 2 (dritte Ebene, K2).
  - Runde 2 D3089 X.: «Detailverzeichnisse zu den Rollenbüchern …» ist Überschrift mit Hinweis bei VIII.1. (K6 d).
- Runde 2 steht seit Runde 7 bei 33/34; das war beabsichtigt (D149835: Nc-Block im Blatt Info).

## Regeln (mit Beispiel und Datei)

### A. Ältere kritische Fälle aus Nachprüfung 8 (K19–K29)

1. **D845 «V.C: c.52.:1.2» (K29).** Ein Doppelpunkt statt Punkt nach dem Bestandskürzel vor einem Kleinbuchstaben
   gilt als Punkt. 1.2 ist Einheit.
2. **D134644 2. (K19).** Eine Nummer ist Listeneintrag im Inhalt, wenn dieselbe Nummer bald danach in grösserer
   Schrift folgt (mindestens 1,5 pt). Gezählt wird nur die nächste nahe Nummer (n bis n+3), ohne Datumszeilen
   («75. Geburtstag»).
3. **D134644 11.1. (K20).** «11.1. Stadt Zürich» direkt unter «10.» und vor «10.1.1.» ist 10.1. (Tippfehler, so auch
   im Inhaltsverzeichnis), mit Hinweis. 10.1.1.–10.1.4. hängen darunter; «11.1. Gottfried Keller» ist Dossier unter 11.
4. **Anhang am Schluss (D151730 19.5. K23, D3462).** Die Überschrift «Anhang» auf der letzten oder vorletzten Seite,
   fett oder ab 13 pt, beginnt den Schlussblock. Was folgt, steht im Blatt Info.
5. **D3826 20. (K28).**
   - «Weitere Diplome befinden sich …» ist Schlussnotiz.
   - Der Schlussblock läuft in grösserer Schrift weiter (ab 13,5 pt). Nebenbei D152781: «Bibliografie» (14 pt) nach
     dem Schlussvermerk hängt nicht mehr am Darin von 5.2.
   - Die fette Überschrift ohne Signatur nach der letzten Einheit bleibt im Darin, mit Hinweis.
6. **D140969 50a, 88, 89 (K21, K22).**
   - «50a» mit Grossbuchstabe danach ist Signatur, wenn das Findmittel ohne Punkt nummeriert.
   - «89 2 Filmrollen» ist Signatur 89; «88 Pläne (…)» ist Signatur 88, nicht Umfang von 87.
   - Nebenbei D847 (2a–2d, 160a–160c) und D149825 (154a): bisher im Darin, jetzt Einheiten.
7. **D152817 (K25).** Ein Buchstabenabschnitt wird nur Eltern einer Schachtel, die genau diesen Buchstaben umfasst.
8. **D2850 55/56 (K27).** Die Briefliste ist nach Anfangsbuchstaben auf 55 (A–M) und 56 (N–Z) verteilt, mit Hinweis.
9. **D152404 :VIII., :VIIIa. (K24).** Römische Zahlen mit vier bis sechs Zeichen, auch mit Buchstabe, sind Teil
   einer Vollsignatur.
10. **D1874 Reg. (K26).** Eine Wortsignatur zwischen «1.» und «1.1.» hängt unter 1., mit Hinweis.

### B. Neue kritische Fälle aus Nachprüfung 9 (K1–K11)

11. **D1746 (K1).** Steht eine fette römische Stufe «II)» in der Signaturspalte, so sind in derselben Spalte auch nicht
    fette «A)» … «O)» und «1)», «2)» Gliederungsstufen.
    - II.A.–II.O. sind Einheiten unter II.; VII.1. und VII.2. unter VII.
    - Gleiche Lage: VI.1.–VI.11. (TA-Gliederung) sind Einheiten.
    - Nummern «1.» in der Textspalte sind dann Liste im Inhalt. II.1. und VII.2.–VII.4. sind weg; ebenso V.i.1.–4.,
      die jetzt im Darin von V.i. stehen. Nicht bei Doppelmarken «III) B)» (D3067 bleibt gleich).
    - Eine eigene Schachtel plus lückenlos anschliessende Schachteln der Inhaltszeilen ergeben einen Bereich:
      II.C. 9–13. Das gilt auch in 13 weiteren Dateien (z. B. D151150 2.3. 3–11, D3231, D3018, D176795).
12. **D1880 (K2).** Kursive «a.» … «i.» (12 pt) in der Signaturspalte sind eine dritte Ebene unter der römischen Stufe.
    - F.III.a.–h. und H.II.a.–h. sind Einheiten; die zweite und dritte Serie stehen als Teile 2/3.
    - F.III.i. ist eigene Einheit. Der Titel von F.III. hat das angehängte «a. …» nicht mehr.
13. **D3012 (K3).**
    - Fette «1)» … «8)» über eingerückten «a)» sind die oberste Stufe, als «1.» … «8.».
    - «a Rollenbuch» ohne Klammer direkt vor «b)» ist 8.a., mit Hinweis.
    - 14 statt 5 Einheiten, «Oberstadtgass» ist 1.
14. **D3018 (K4).** «Nicht im Detail verzeichnet (Vgl. Zusammenfassung vorn.)» auf der letzten Seite beendet die
    letzte Einheit. Die Kurzliste danach steht im Blatt Info; 08.9. und 09. kommen wie bisher aus der Zusammenfassung.
    08.8. hat nur noch die Alben, Sch. 75.
15. **D3060 (K5).** Ein Block ohne Überschrift nach grossem Abstand am Ende einer Detail-Schachtel gehört zu einer
    Schachtel nur aus der Zusammenfassung, wenn er mit deren Titel mindestens zwei Wörter teilt. «Porträtbild von Anna
    Asper 1964 …» steht jetzt bei Schachtel 10, mit Zeitraum 1964 und Hinweis.
16. **D3089 (K6).** Detailverzeichnisse nach der letzten Einheit, die nur über die Schachtelnummer verbunden sind,
    werden zeilenweise der Einheit zugeordnet, deren Schachteln die Nummer enthalten. Zugeordnet wird über die
    Schachtelspalte und über die Köpfe «… TEXTBÜCHERN Schachtel 62» und «Verzeichnis zu Schachtel 70».
    - VIII.1. Sch. 55–61 bekommt die Rollenbücher, VIII.2. Sch. 62–67 die Textbücher (mit Teil 2).
    - X. Sch. 68–73 hat nur noch die eigenen Zeilen und «BÜCHER DER BIBLIOTHEK», mit Zeitraum 1866–1956.
    - Der Kopf S. 16 ist Überschrift, sein Text steht im Hinweis bei VIII.1.
    - «Bestand geordnet und verzeichnet von …» ist Schlussvermerk.
17. **D3105 (K7).** «Band 1» ist ein Behälter neben «Schachtel 1/2», wenn die Marke fett in derselben Spalte steht.
    Die Signatur ist VII.2.:Bd.1. «0354B/1/rpt Stand: 05.07.1994» ist Schlussvermerk.
18. **D3271 (K8).** Eine Gruppenzeile mit Bandzahl («Kassenbelege (2 Bände)») als eigener Absatz direkt vor dem
    ersten Glied der Gruppe («4.2.6. Bd. 1: …», «4.2.8. a. …») ist Zwischenüberschrift, Hinweis bei der folgenden
    Einheit. Die Bedingung «erstes Glied» schliesst «1937-1948 gebunden (6 Bände)» (D2962) und «(2 Bände)» (D2979)
    aus. 11 Gruppen in 4.2.
19. **D3566 (K9, K10).**
    - «S. Vögelin, …» (Initiale, Nachname, Komma) ist keine Buchstabensignatur, wenn noch kein Buchstabe vorkam und
      der Buchstabe weit hinter A liegt. :S. und :S.3. sind weg, «3.» ist wieder 3.
    - «max / 28. März 2000» (Kürzel / Datum) ist Schlussvermerk; 3. hat 02.12.1829–28.03.1832.
20. **D3727 (K11).** «01.12.0982» (Jahr mit führender Null oder ein zweites Datum danach) ist keine Signatur.
    - Die Einheiten 47–49 sind weg; ihr Text steht im Darin von 10.3.
    - «3 Fotos» tief in einer Liste ist Stückzahl, nicht Umfang von 10.3.

### C. Eigener Suchlauf über alle 715 Ausgaben

21. **D3470 (neu, kritisch).** Ab S. 23 wechselt die Signatur von «45.0» zu «1933.416». Signaturen «Jahr.Laufnummer»
    gelten jetzt auch in einem dezimalen Findmittel, das solche Zeilen hat. 1391 Einheiten 1933.416–1964.1971 stehen
    nicht mehr im Darin von 45.0. Im Korpus betrifft das nur diese Datei.
22. **D1924 Schachtel «101».** Eine einzelne Zeile «101» zwischen Zeilen der Schachtel 10, weit über der höchsten
    übrigen Nummer, gehört zu 10, mit Hinweis.

### D. Mittlere Funde aus Nachprüfung 9

23. **Schachtelüberschrift bei flacher Nummerierung.** Ohne Unternummern und ohne römische oder Buchstaben-Stufen in
    der Signaturspalte gilt «Schachtel II» bis zur nächsten Schachtelüberschrift. Betroffen sind D3810 3.–6. (II) und
    20 weitere Dateien mit «Schachtel I:» / 1 … 13 / «Schachtel II:» / 14 …, darunter D1116, D1341, D263, D789 und
    D151730.
    - Bitte prüfen: D3774 6. «Pläne» erbt Schachtel 7.
24. **D3842 1.** Eine Zahl unter dem Tabellenkopf «Schachtel» («Nr. Titel Schachtel Jahre») ist Schachtel-Nr., auch
    wenn nur eine Zeile eine hat.
25. **Laufzeit in Klammern nach einem Jahr des Namens.** «Jahrgängerverein 1786 (1834 – 1863)»: die Klammer ist die
    Laufzeit. Betroffen: D3313 1.–4., D1180 1., D2620 11.2.; die Regel gilt auch im Inhaltsverzeichnis.

### E. Vollständigkeitsprüfung

26. «Schachtel 42» gilt als gefunden, wenn die Schachtel-Nr. der Einheit sie als Bereich enthält («42-43»,
    «55-61, 68-73»). Zeilen im Blatt Info schreiben die Schachtel als «Schachtel 76», nicht als blosse Zahl.

## Weiter offen (mittel/gering)

- D3566 1. und 2.: geschätzte Zeiträume aus Literaturangaben und Zitaten (1519–1953, 1336–1962).
- D3810 1. und 7.: mehrzeilige Titel sind abgeschnitten (Zusammenführen über Zeilen war in Runde 5 verworfen).
- D3190: die Übersichtszeile 9. steht als Teil 1 von 9. zwischen 1. und 2.
- D3012 8.a.: Sch. 05 statt 04–05; 8.: Sch. 04 statt 04–07.
- D1746 II.D.: Sch. 9 statt 13.
- D3472 «1952.111» steht so im PDF (wohl 1952.11).
- D3470: die 539 Signaturen «42.446» (zweistelliges Jahr) haben weiter den Hinweis «Keine übergeordnete Signatur».

## Bitte an die Nachprüfung 10

1. Gegenprüfung der 59 geänderten Dateien gegen `vorher/`: besser, gleich oder schlechter, und neue kritische Fehler.
2. Für die 509 Dateien, die noch in keiner Fundliste standen: Stichprobe mit allen Treffern aus `roh/np9_verdacht.csv`
   und einer Zufallsauswahl nach Gliederungsart und Umfang. Findet sie kritische Fehler, wird die Prüfung ausgeweitet.

## Nachtrag 1 nach Nachprüfung 10 (22.11.2026)

Skript sha256 `efe92c5ff93c2800…`. `findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind neu
erzeugt. Gegenüber `7fa7e161` sind 14 Dateien geändert, dazu `testdaten_excel/D177460`
(`geaenderte_dateien_nachtrag1.txt`, `zellvergleich_nachtrag1.txt`). Der Stand vorher liegt in `vorher_r8b/`.
D151210 ist zellgleich.

Kennzahlen:

- Einheiten 50'387 → 50'902.
- «[ohne Titel]» 30 → 33; die drei neuen sind D3470 1953.1419, 1954.1514 und 1961.1813, im PDF ohne Titel.
- «Text erfasst 100 %» 695.
- Fallsets wie vorher; einzelne Abweichungen sind nur ID-Verschiebungen (z. B. B D2960 ID 11 → 11. hat weiter
  1883–1892).

Behoben (K-Nummern der neuen `offen_kritisch.csv`):

27. **Nummer mit angehängtem Buchstaben** in allen Formen:
    - Gliederung mit Punkt: «3a.», «5a.» (D2960, K49/K50);
    - dezimal: «1.23a.» (D2951, K48), «430.1.733.1a» (D10744, K47);
    - Registraturcode: «730a» (D10675, K46);
    - Jahr.Laufnummer: «1973.9a» (D3472, K58), «1937.524a/b», «1938.583a/b», «12.53a» (D3470, K53–K57).
28. **Bereich «1-3. Sitzungsprotokolle»** über «1. Band» … «3. Band» (D2960, K51). «3a.» bleibt ausserhalb des
    Bereichs, weil das Bereichsende keinen Buchstaben hat.
29. **Erstes Kind mit blossem Zeitraum als Titel:** «2.6.1. 1937 – 1943» (D434, K59). Drei Stellen sind nie ein Datum.
30. **Angeklebter Titel nach einer Buchstabenstelle:** «7.2.1.c.1967/68» ist 7.2.1.c. (D3170, K52). Eine Zeile
    «7.2.1.» gibt es im PDF nicht, darum der Hinweis «Übergeordnete Signatur 7.2.1. fehlt».
31. **Jahr.Laufnummer nur mit Schachtel, ohne Titel:** «1953.1419 ¦ 121» (D3470, K25–K27).
32. **Bestandsteil mit einem Zeichen Abweichung**, wenn die Nummer die Folge fortsetzt. «V.G. c.45.:10.» in V.H.c.45.
    wird V.H.c.45.:10. (D2137, K9). Nebenwirkung **D260** (K60): Ab :26 steht durchgehend «V.B. c.23.» statt «V.A.».
    Die 95 Einheiten :26–:120 standen bisher im Darin von :25.
33. **Übersprungene Hauptnummer:** «32. Verkommniss …» nach «30.» ist Signatur (D2828, K14). Bedingung: gleiche
    Spalte und Schrift, Datumsspalte, keine Fortsetzung einer Liste (D3828 bleibt gleich).
34. **«Anhang: Titel»** (fett, ohne Signatur danach) beginnt den Schlussblock, auf jeder Seite (D2828 K15, D175827 K6).
    Nebenwirkung D175827: 6 Darin-Verbindungen ändern sich, weil die Bibliografie nicht mehr den Rand der Textspalte
    bestimmt.
35. **Signaturen nur in Klammern bei den Behältern:** «Schachtel 1 (V.F. c.18.:1)» … «Mappe (V.F. c.18.:3)». Die
    Nummern 1.–31. sind Positionen im Darin (D1387, K2). Im Korpus nur diese Datei.
36. **Dritte Stufe «X n:m»:** «D 1:1 Protokolle …» unter «D 1» (D177460, K8; Testdaten). 167 → 596 Einheiten.

## Nachtrag 2 nach Nachprüfung 10 (22.11.2026)

Skript sha256 `bb4c958822bb50a3…`. `findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind neu
erzeugt. Gegenüber Nachtrag 1 (`efe92c5f`) sind 32 Dateien geändert (`geaenderte_dateien_nachtrag2.txt`,
`zellvergleich_nachtrag2.txt`). Der Stand vorher liegt in `vorher_r8c/`. D151210 und alle Testdaten sind zellgleich.

Kennzahlen:

- Einheiten 50'902 → 50'935.
- «[ohne Titel]» 33.
- «Text erfasst 100 %» 695.

Fallsets: Runde 2 31 → 30. Das ist D2853: Das Fallset erwartet 14 Einheiten, nach Nachprüfung 10 sind 8 richtig. Das
Fallset ist anzupassen. Sonst unverändert.

Behoben (K-Nummern aus `offen_kritisch.csv`, Stand Nachprüfung 10):

37. **D2853 (K19–K21).**
    - Eine einzige, nicht fette römische Marke («I. Verzeichniss der … Subscriptionen …» unter «4. Drucksachen») ist
      Text, keine Gliederungsstufe. Das gilt in 6 Dateien mit genau einer solchen Marke.
    - Die Schachtelübersicht «Aufteilung des Bestandes in Schachteln:» / «Schachtel 1: 1. Protokoll» … wird nicht
      importiert. Ihre Schachteln gelten für die genannten Nummern: 1., 2. Sch. 1; 3. Sch. 1-4; 4. Sch. 4; 5. und
      5.1.–5.3. Sch. 5.
    - Ergebnis 8 Einheiten.
38. **D3089 IV.2a, IV.2b (K23).** Unterpunkte «2a», «2b» ohne Punkt direkt unter «2.» sind Einheiten unter 2.
    Bedingung: «2a» steht gleich nach der Titelzeile von «2.», «2b» folgt auf «2a». Die Aktenplan-Tabelle in D2853 bleibt
    davon unberührt.
39. **D175949 «A.1» … «Q.1» (K7).** Buchstabe der laufenden Gruppe, Punkt, Nummer ist eine Einheit unter dem Buchstaben:
    41 statt 16 Einheiten.
40. **D2363, D814 (K10–K13, K30).** Steht über einer Behälterliste der Tabellenkopf «… Schachtel-Nr.», gehört die Nummer
    zur ersten Zeile eines Eintrags, nicht zur letzten.
41. **D3898 (K29), D3896.** Kurze fette Ortsüberschriften in der Textspalte («Fluntern» / «X.E. 18. …») gelten als
    Zwischenüberschrift der folgenden Einheit. Ausgenommen sind Klammerbemerkungen und Spaltenköpfe.
42. **D3271 «Buchhaltungsjournal (2 Bände)» (K1).** Eine Gruppenzeile mit Bandzahl gilt auch ohne Absatz davor, wenn die
    Zeile davor einen Satz abschliesst und ein Absatz vor dem ersten Glied folgt.
43. **D2850 «SATUS» (K18).** Ein Name in Grossbuchstaben mitten in einer Liste (gleiche Spalte, Folgezeile ohne Absatz,
    keine Signatur danach) ist keine Zwischenüberschrift. Nebenbei D4173: «ALFRED» in einem Zitat.
44. **D3018 «Cakeplatte» (K22).** Posten der Kurzliste nach «Nicht im Detail verzeichnet», die in der Zusammenfassung
    fehlen, kommen mit Hinweis ins Darin der letzten übernommenen Einheit (09.).
45. **Jahr.Laufnummer mit Tippfehler im Jahr (K24, K28).** Ein Jahr, das von beiden Nachbarn abweicht, wird als deren
    Jahr gelesen, mit Hinweis. Bedingungen: Die Nachbarn haben dasselbe Jahr, das Jahr ist ein Zahlendreher davon oder
    weicht um ein Zeichen ab, und die Laufnummer passt zwischen die Nachbarn.
    - D3468: «1947.7» zwischen 1974.7 und 1974.8 wird 1974.7 Teil 2.
    - D3472: «1967.18» zwischen 1969.17 und 1969.19 wird 1969.18.
46. **D2834 a)–c) (K16, K17).** Stehen die Behälter eingerückt unter den Buchstaben («Sch. Bez. Inhalt Jahre» / «a)
    Beilagen …» / «Schachtel 1 1913-1922»), sind a)–c) die Einheiten.
47. **D847 (K31–K35).**
    - «1Aa», «1Ab», «1B» … «1E» sind Einheiten.
    - «38 1. Legat …» ist Signatur 38 mit Ordnungszahl im Titel.
    - «9 Orgelfonds Enge» zwischen 91 und 93 wird 92, mit Hinweis.
    - Die erste Nummer «1 Liste der …» gilt, wenn die nächste Zeile die Liste fortsetzt.
    - 292 Einheiten = Signaturzeilen.
48. **D8947 (K36, K37).** Zwei, drei gleich betitelte Nummern («1. Kuvert (Seidenkuvert)», «2. Kuvert …») nach einer
    langen Objektbeschreibung zählen Stücke auf. Das Findmittel gilt dann als eines ohne Signaturen: eine Zeile für den
    Bestand mit der ganzen Beschreibung.
49. **D152817 «VI.SB.103.» (K5).** Fehlt der Abschnittsbuchstabe zwischen «C.102.:3» und «C.103.:1», wird «C.103.»
    gelesen, mit Hinweis.
50. **D149825 (K3, K4).** Für Stücke ohne Nummer werden keine Signaturen erfunden. Der Text kommt mit Hinweis ins Darin
    der benachbarten Einheit, wie bei D3826 20.:
    - die Beschreibung vor der ersten Signatur (mit Datum und Umfang, bis zur nächsten Überschrift) zu 1.;
    - der Absatz in der Signaturspalte nach der letzten Einheit zu 272.
    - Der zweite Hinweis erscheint auch in 13 weiteren Dateien, wo ein solcher Absatz im Darin der letzten Einheit steht
      (z. B. D67 «Neu erfasst am 20. Januar 2004 / RD», D1439, D175454). Das ist ein Prüfsignal, kein neuer Fehler.
