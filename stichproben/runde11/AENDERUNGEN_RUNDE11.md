# Runde 11 – Änderungen und Bitte um Nachprüfung 14

Stand 22.11.2026. Skript `findmittel_zu_scope.py` sha256 `94ff40ba00ed18ca…`. Aufbau: Runde 10 (`424a997636eb557a…`) plus
diese Runde.

`findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind mit diesem Skript neu erzeugt.

## Worum es ging

Behoben sind alle 19 nicht bewusst offenen Zeilen aus `nachpruefung13.md` bzw. `offen_kritisch.csv` (Stand 424a9976).
Dazu kommen die drei Konventionsentscheide der NP13 und einige kleinere Vorschläge.

**Kennzahlen** (Runde 10 → Runde 11):

| Kennzahl | Runde 10 | Runde 11 | Bemerkung |
|---|---:|---:|---|
| Einheiten | 51'508 | 51'602 | +106 in D151150, −16 in D177470, +4 Bestandszeilen |
| «[ohne Titel]» | 29 | 29 | |
| «Text erfasst 100 %» | 694 | 694 | weiter nur D3943 bei 99,9 % |
| Doppelte Schlüssel | 10 | 10 | |
| Dateien mit Übersichtszeilen | 10 | 9 | D151150, siehe K189 |
| Tracebacks | 0 | 0 | |

**Geändert sind 18 Dateien** (`geaenderte_dateien.txt`).
- Ihr Stand vorher liegt in `vorher/`, dazu die zwei geänderten Testdaten als `vorher/testdaten_*.xlsx` und das Skript der
  Runde 10.
- Zellvergleich: `zellvergleich_runde10_runde11.txt`.
- Textabgleich: `werkzeug/textverlust_runde10_runde11.csv`. Das Werkzeug `werkzeug/textverlust.py` weist Zahlen jetzt
  getrennt aus (Spalte `fehlende_zahlen`), wie in NP13 vorgeschlagen. Die fehlenden Wörter sind alle erklärt:
  - «Schachtel» in D151150 steht jetzt in der Schachtelspalte der 105 neuen Dossiers;
  - «chr Stand» in D3808 und D3781 steht jetzt im Blatt Info;
  - die Sätze «Die Protokolle von … sind lose verschachtelt.» stehen jetzt in der Bestandszeile statt im Info.

**D151210 ist zellgleich mit Runde 10.** In den Testdaten ändern sich nur D152810 (K187, K188) und D177470 (Konvention 2).

**Fallsets:** alle unverändert: A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38.

## Konventionsentscheide zu den Fragen der NP13

1. **K135 / Regel 17:** bestätigt.
   - Steht eine Signatur zweimal hintereinander mit anderem Titel und sind die Nachbarnummern da, bleibt die zweite ein Teil
     mit dem Hinweis «Tippfehler?». K135 ist mittel.
   - Fehlt die Nachbarnummer, wird die zweite Nennung zur fehlenden Nummer (Regel 2 unten).
2. **Buchstaben in der Titelspalte einer Gruppe** («27. Dokumentationen» / «a) Familie Guldener …» … «h)»): Sie sind
   Darin-Einträge der Gruppe, auch mit eigenem Datum, wie in D3826. Das ist D177470 27. und 28.
   - Eigene Einheiten bleiben sie nur, wenn sie eine eigene Schachtel haben («1. Oberstadtgass» / «a) Hörspielfolge ¦ 01»;
     D3012, D3089, D3038 wie bisher). Das deckt sich mit «Kein Fund» der NP13 zu D3012 und D3089.
   - Über alle 715 Dateien betrifft das nur D177470.
3. **K178 D10744:** keine Zehnergruppe nach der Nummer allein. Gruppe wird ein Code nur in grösserer Schrift als seine Codes
   (14 pt gegen 12 pt). 710 ist ein gewöhnlicher Code unter 700.

## Die Regeln der Runde 11

1. **Nummerierte Dossiers, die wie Monat.Jahr aussehen** (K144 D151150): «9.1208. Viehzählung» nach «9.1194. …» wurde als
   «Monat.Jahr» verworfen. Mit Punkt am Ende und derselben ersten Stelle wie die laufende Einheit gilt es jetzt als
   Signatur. Damit sind alle Dossiers 9.144. … 9.2501. Einheiten; die 105 Zeilen stehen nicht mehr im Darin von 9.1194.
2. **Doppelte Jahr.Laufnummer, die nächste Nummer fehlt** (K183, K184 D3472): Bei «1952.8 Hochwald …» / «1952.8 Horgen …» /
   «1952.10 …» wird die zweite Nennung zu 1952.9, mit Hinweis; «Nr. im PDF» bleibt «1952.8». Ebenso 1952.14 → 1952.15.
   - Das gilt nur, wenn die beiden Titel verschiedene erste Wörter haben. Teile derselben Sache wie «175.» in 13 Teilen
     (VII.308.C.a.) bleiben Teile.
3. **Regel 9 (Tippfehler-Nachbarregel) zurückgenommen** für «Jahr.Laufnummer» mit laufender Nummer ab 100. In D3470 bleiben
   «40.430.» und «41.436.» so, wie sie im PDF stehen; die erste Nummer ist dort laut Vorspann frei gewählt.
4. **Buchstaben als Geschwister (Regel 10) erweitert** (K185–K188, K194, K195, K197). «n.a» ist auch dann Geschwister von
   «n.», wenn:
   - «n.» eigene Bände «:1–:n» davor hat: VI.SB.C.33.a (D152817), Testdatei D152810 VI.HO.C.32.a und 75.a;
   - beide nur eine eigene Schachtel haben: D3470 11.43.a. und 11.44.a.;
   - das Datum nur im Titeltext steht: D150589 2.2.1.8.a. und 2.2.9.12.a., D3067 IV.A.5.a.;
   - der Buchstabe später verstreut folgt: D3067 IV.A.5.b. nach 6.
   - Voraussetzung bleibt, dass «n.» selbst eigene Angaben hat (Datum, Umfang, Schachtel). Teile derselben Sache wie D3012
     «1. Oberstadtgass» / «1.a. Hörspielfolge» bleiben Kinder.
5. **Eine Zeile mitten in einer Dossierliste ist keine Übersichtszeile** (K189 D151150): «501 Mietauto für Fleischschau ¦
   1934 ¦ 45» hat eigenes Jahr und eigene Schachtel und bleibt Einheit 9.501. Die zweite «501 …» nach 518 ist Teil 2, mit
   Hinweis.
6. **Stück ohne Nummer:**
   - «Die Protokolle von … bis … sind lose verschachtelt.» kommt in die Bestandszeile (K192 D151756, K193 D152383, K198
     D151759). Über alle 715 Dateien gibt es nur diese drei Sätze.
   - Einträge ohne Nummer «Nr. K.V. …» und «Nr. - …» nach der letzten Einheit kommen in die Bestandszeile, je als eigene
     Darin-Zeile (K190 D3412). «Nr. -» bleibt dabei zusammen.
7. **Zweizeiliger Eintrag mit zwei Nummern** (K191 D3412): «Nr. 146/ Erben Walter Egli, …, Rainstrasse, 1963» / «Nr. 148
   Stäfa» ist eine Einheit VII.287.:146/148. (wie «602/603» in D10675). Ihr Titel endet auf «…, Rainstrasse, Stäfa».
8. **Schlussvermerk mit Kürzel** «chr Stand: 02.09.1992» kommt ins Blatt Info und nicht in die Bestandszeile (K156 D3808,
   ebenso D3781 VII.5.:14).
9. **Gruppenende** (K196 D2620): Eine Zeile nach der letzten Unternummer und vor der nächsten höheren Nummer kommt ins Darin
   der Gruppe, mit Hinweis. Beispiel: «Bibliographische und andere Notizen (1 Mäpplein)» nach 1.22. und vor «2.».
   - Die Zeile muss eingerückt sein wie die Beschreibung der Gruppe und mit grösserem Abstand stehen als die Unternummern.
   - Nicht gemeint ist eine Umfangsangabe in Klammern wie «(1 Mappe)» unter 1.8.3. (D150689).
10. **Registraturgruppen nur nach Schrift** (K178 D10744, siehe Konvention 3).
11. **Kleinere:**
    - D149888 13.1.: kein Hinweis «zweimal hintereinander» bei einem Teil aus einer Schachtelangabe.
    - In einer Liste von «Nr.»-Einträgen beginnt jede «Nr. n»-Zeile einen neuen Eintrag. Das betrifft auch D3774 4.3. «Nr.
      13 1. Rechnung 1866*» / «Nr. 13 2.-55. Rechnung …».
    - D2894 2.: nur der Hinweistext, die Signatur war schon richtig.

## Bewusst offen

Wie bisher: K38 D149622, K39 D1739, K40 D1858, K41 D2614, K42 D3208, K44 D3828, K45 D512, K78 D3894, K117 D2710, K173
D1874.

## Nicht umgesetzt (mittel)

- D2962 7.–10. Schachtel 3, D9978 28.4.25. Zeitraum aus der Notiz «1982/84».
- D406 Fehlbestand-Vermerk nur im Hinweis bei :56.; nach Soll zulässig.

## Bitte um Nachprüfung 14

Wie in deinem Plan zu NP14:
1. **Gegenprüfung der Runde 11** an den 18 geänderten Dateien und den zwei Testdateien. Altzeilen sind die 19 Zeilen von
   NP13. Besonders zu prüfen sind Fehlgriffe der Regeln 2, 4, 5 und 9 (Gruppenende).
2. **Suchläufe über alle 715 Dateien:**
   - Tippfehler, Stück ohne Nummer im Info und «n.a» als Kind;
   - «Gruppenende»;
   - Nummern in Nr.-Spalten, die wie Jahreszahlen aussehen.
3. **Zweite Zufallsstichprobe** von 60 Dateien ab Rang 74 der festen Reihenfolge.
