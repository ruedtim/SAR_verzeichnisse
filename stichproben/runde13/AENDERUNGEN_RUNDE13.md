# Runde 13 – Änderungen und Bitte um Nachprüfung 16

Stand 22.11.2026. Skript `findmittel_zu_scope.py` sha256 `2a44ff8d2339fac8…`. Aufbau: Runde 12 (`439a6fbf…`) plus diese Runde.

`findmittel_excel/`, `testdaten_excel/` und `D151210_scope_import.xlsx` sind mit diesem Skript neu erzeugt.

## Worum es ging

Behoben sind alle 12 nicht bewusst offenen Zeilen aus `nachpruefung15.md` bzw. `offen_kritisch.csv` (K209–K220, Stand
439a6fbf). Dazu kommen der Rückschritt der Runde 12 in D3099 und die Titel, die am Gedankenstrich abbrechen (mittel).

**Kennzahlen** (Runde 12 → Runde 13):

| Kennzahl | Runde 12 | Runde 13 | Bemerkung |
|---|---:|---:|---|
| Einheiten | 51'605 | 51'605 | +5 Bestandszeilen (D1481, D1759, D2575, D3742, D3767), −5 leere Teile (D845) |
| «[ohne Titel]» | 29 | 29 | |
| «Text erfasst 100 %» | 694 | 694 | weiter nur D3943 bei 99,9 % |
| Doppelte Schlüssel | 10 | 10 | |
| Dateien mit Übersichtszeilen | 9 | 9 | |
| Tracebacks | 0 | 0 | |

**Geändert sind 85 Dateien** (`geaenderte_dateien.txt`):
- 16 durch die Regeln 1–5 und 9 (die zwölf K-Dateien sowie D3099, D2620, D10585);
- 35 durch die Strich-Regel (Regel 6);
- 50 durch den Leerschlag nach dem Strich (Regel 8, nur Text) und die Regel 7;
- manche Dateien zählen mehrfach.

Ihr Stand vorher liegt in `vorher/` (85 Dateien, dazu die 4 geänderten Testdateien als `vorher/testdaten_*.xlsx` und das
Skript der Runde 12). Zellvergleich: `zellvergleich_runde12_runde13.txt`.

**Textabgleich** (`werkzeug/textverlust_runde12_runde13.csv`): Die fehlenden Wörter sind alle erklärt.
- Die Bearbeitervermerke von D2630, D3231, D3604 und D631 und der Umfangssatz von D2508 stehen jetzt im Blatt Info
  (Spalte `info_neu`).
- In D1935, D3515, D109662, D2721, D3672 und D845 stehen Daten jetzt im Zeitraum (von/bis) statt im Darin. Das Werkzeug
  zählt von/bis nicht mit.

**D151210 ist zellgleich mit Runde 12.** In den Testdaten ändern sich D149628 (13 Titel der Programmhefte ganz, das
Zeitraum-Ende stimmt jetzt), D3515 (3 Titel), D177460 und D9985 (Leerschlag nach dem Strich).

**Fallsets:** alle unverändert: A 11/12, B 33/38, C 9/12, F 5/7, Runde 2 31/34, Punkt 2 38/38.

## Entscheide zu den Fragen der NP15

1. **K210 D1759:** Ja, Bestandszeile, aber mit dem ganzen Absatz. Der CD-Satz beginnt mitten in einer Zeile und braucht den
   Satz davor als Bezug: «Die dazugehörigen vier Compact Discs …». Die zwei Bearbeitungsvermerke bleiben im Blatt Info.
2. **K217 D3767:** bestätigt, kritisch. Die Beilagen kommen in die Bestandszeile.
3. **K219 D414:** wie empfohlen. Der Absatz kommt ins Darin der Schachtel 5, als eigener Absatz und mit Hinweis.
4. **K214 D3231:** wie empfohlen, ins Blatt Info.
5. **Mittel, zur Abstimmung:**
   - D10649 «Eine Fotokopie der einzelnen Bilder liegt bei.» bleibt Vorbemerkung: Der Satz beschreibt die Form der Stücke
     (wie D3273).
   - D69 28. und D65 21. «Fortsetzung der Rechnung vgl. IV.C. …» bleiben im Darin der letzten Nummer (mittel, wie D67
     III.Q.33.). Es fehlt kein Text.
   - D2589 19. bleibt mittel.

## Die Regeln der Runde 13

1. **Bearbeitervermerke ins Blatt Info** (K213 D2630, K215 D3604, K218 D631, K214 D3231). Neu erkannt werden:
   - «Erstellt (und bearbeitet) von <Kürzel> / <Datum>», nur mit «Name / Datum»; Inhaltszeilen wie «Erstellt durch
     Innenarchitekt H. R. Hugentobler.» (VII.192.) bleiben, wo sie sind;
   - «<Datum> / <Name>» nach der letzten Zeile einer Schachteltabelle ohne Signaturen, nach mehr als 20 pt Abstand und in den
     letzten 15 Zeilen;
   - «Ende Juli 2004 / <Name>», also «Anfang/Mitte/Ende Monat Jahr» ohne Tageszahl;
   - «(Nachlieferung verzeichnet <Datum>/<Name>)» in Klammern, auch mitten im Verzeichnis, nach einem Absatz.
   - Über alle 715 PDFs kommt jede dieser Formen nur in der genannten Datei vor.
2. **Stück ohne Nummer im Schlussteil → Bestandszeile** (K209 D1481, K211 D2575, K210 D1759, K216 D3742, K217 D3767). Neu
   erkannt werden:
   - «Die Protokolle von … bis … sind lückenhaft …», wie «sind lose verschachtelt»;
   - «Des Weiteren (Ferner, Ausserdem, Zudem, Daneben) enthält der Bestand …»;
   - ein Absatz nach der letzten Einheit, der einen Datenträger nennt, der in den Bestand kam («vier Compact Discs … in den
     Archivbestand integriert»). Die übrigen «integriert»-Sätze sind Bestandsgeschichte und bleiben im Info (D150536,
     D3099, D2850);
   - «Beilagen (3 Farbbildchen)» mit der Aufzählung darunter. In einer solchen Liste gehören auch die «- …»-Zeilen in der
     Spalte des Kopfs dazu;
   - «Letztes Blatt (schwarz kalligraphiert):» mit der Inschrift darunter, als Satz. Die Inschrift in Kapitälchen steht nicht
     mehr als Überschrift unter «Nicht übernommen».
3. **Umfangssatz zum Bestand mit längerem Namen** (K212 D2508): «Der Bestand der Politischen Flugblätter von 1795 bis 1945
   umfasst 16 Archivschachteln.» kommt ins Blatt Info. Die Regel gilt nur mit einer Menge danach (Schachteln, Mappen,
   Bände, Laufmeter).
4. **Faszikel-Absatz nach der Gruppenliste** (K219 D414): «Der Inhalt der einzelnen Faszikel ist nicht verzeichnet. …»
   steht jetzt im Darin der Schachtel 5, als eigener Absatz, mit Hinweis. Das Blatt Info ist leer.
5. **Kopf eines Unterverzeichnisses bei Vollsignaturen** (K220 D845): Es entsteht kein leerer «Teil 2» mehr. Der Kopf kommt zur
   ersten Nennung, mit Hinweis:
   - Sein Titel wird die erste Darin-Zeile. Ein abweichendes Datum steht dabei, etwa «Steueramt, 1908-1972» unter «:92.
     Steueramt. Verzeichnis».
   - Ein offener Zeitraum wird mit dem Datum des Kopfs geschlossen: :44. hat jetzt 1911–1950.
   - Die Regel gilt nur für einen fetten Kopf mit höchstens zwei Zeilen, auf den direkt seine Unternummern folgen. Im
     Gesamtlauf trifft sie nur D845, mit allen fünf Fällen (:1., :44., :92., :95., :124.).
6. **Strich am Zeilenende** (mittel; D2620 1.14., D150829 5.5.18., D3170 4.2.1.6.).
   - **Was sich ändert:** Die Regel beendete den Titel bei einem Strich am Zeilenende («… von Bertolt Brecht -» /
     «Uraufführung am …», VII.200.). Jetzt trennt sie nur noch, wenn danach Unterlagen, eine Aufzählung oder
     «Uraufführung/Premiere/Inszenierung/Regie» folgen.
   - **Warum:** Vorher trennte sie über alle Dateien 104-mal, fast immer falsch: Bereiche «vom 3. –» / «18. Juni 1978»,
     Ortspaare «Neuenhof –» / «Wettingen», Werktitel «“Tod –» / «Gott”». Der Strich fiel dabei aus dem Text. Die Liste
     steht in `werkzeug/strich_trennungen_runde12.txt`.
   - **Ergebnis:** In D151210 bleiben die drei gemeinten Trennungen. Geändert sind 35 Dateien.
   - **Zeiträume:** Zusammen mit Regel 7 ändern sich Zeiträume in 21 Einheiten, fast alle genauer: D149628 Programmhefte
     (10), D176060 Tagungen «vom 20. – 22. September 1988» (4), D1935, D1180, D2975, D109662. Ungenauer wird D2721 1.
     (1905 statt 13.07.1905, das Ende «30. Dezmeber» ist im PDF verschrieben). Wie vorher falsch bleibt D2607 2.13.
     (1833–1903 aus dem Inhalt). Insgesamt ändern sich in Runde 13 Zeiträume in 28 Einheiten, die übrigen 7 durch die
     Regeln 1, 5 und 9.
   - **Rückschritt (mittel):** D4173 3.3. Der Titel enthält jetzt «geboren 2. Januar 1867 … gestorben 13. April 1955 …», der
     Zeitraum endet mit dem Sterbedatum. Das ist der bekannte Fehler mit Lebensdaten; vorher stand das Jahr 1958 aus dem
     Darin.
7. **Datum im Titel innerhalb der Datumsspalte:** Es ersetzt die Spalte nur noch, wenn es ein Ende der Spalte genauer fasst,
   also dasselbe Anfangs- oder Endjahr hat.
   - D151150 15.4. bleibt 1965–1971 und nicht die Ausstellung vom 3.–11. Mai 1969.
   - D109662 1.4. hat jetzt 1852–1901 statt nur der Convention von 1854/55.
   - D149628 26.2.19. hat jetzt 15.12.1905–01.08.1913.
8. **Leerschlag nach dem Strich beim Zusammenfügen:** «1962 –» + «1. Juli 1962» wird «1962 – 1. Juli 1962», vorher
   «1962 –1. Juli». Das gilt nur, wenn vor dem Strich ein Leerschlag steht; «1940–» + «1952» bleibt «1940–1952». Das sind
   50 Dateien, nur Text.
9. **Gruppenzeitraum aus dem eigenen Darin** (D3099 7.3., Rückschritt der Runde 12).
   - **Bedingungen:** keine Untereinheit hat einen Zeitraum, und die Spanne ist höchstens 30 Jahre.
   - **Ergebnis:** D3099 7.3. 1941, damit beginnt 7. wieder 1941. Dazu D2620 10.2. 1917–1936 und D10585 3.8. 1827–1828.
   - **Nicht:** D3530 1. (Lebensdaten und Auskunft 1895–1999) und D140969 59–81 (Archivierungsvermerk 1990).

## Nicht umgesetzt

- **D150829 1.6. und 6.3.** (mittel): Hier steht der Strich am Anfang der Folgezeile («– Osaka – Hong Kong …», «– 1942),
  Vater von …») und gilt als Aufzählungszeichen. Ein Suchlauf findet 36 solche Stellen, darunter echte Listen («- Maria
  Elisabetha Escher (1826 – 1903)»). Eine sichere Unterscheidung fehlt.
- **D4173 3.3.**, siehe Regel 6.
- **Wie in Runde 12:** D3466 584./T19, D3412 «Nr.-».
- **Weitere mittlere Vorschläge der NP15:**
  - Titel am Doppelpunkt geteilt (D150829 4.1.79., 4.2.117.);
  - «vom 15. und 31. Juli» (D150829 2.6., 4.1.51.);
  - Zeitraum aus dem Ablieferungsvermerk (D174277, D2915);
  - D2839, D151735.
- **Wie bisher:**
  - D2962, D9978, D406, D3943;
  - zur Abstimmung vor dem Gesamtimport: D176824, D2921.

## Bewusst offen

Wie bisher: K38 D149622, K39 D1739, K40 D1858, K41 D2614, K42 D3208, K44 D3828, K45 D512, K78 D3894, K117 D2710, K173
D1874.

## Bitte um Nachprüfung 16

Wie in deinem Plan zu NP16:

1. **Gegenprüfung der Runde 13** an den 85 geänderten Dateien und den 4 Testdateien. Altzeilen sind K209–K220. Besonders zu
   prüfen sind:
   - die Strich-Regel: Sind Titel jetzt zu lang, wie D4173?
   - Regel 7: Gilt die Spalte, wo der Titel genauer war?
   - Regel 5 (Vollsignatur);
   - Regel 2 (Absatz mit Datenträger, Liste der Beilagen);
   - Regel 9 (Gruppenzeitraum).
2. **Suchlauf zu Muster K220** und **Strukturbericht über alle Dateien**, wie geplant: Teile ohne Darin, Schachtel und
   Zeitraum; Kinder nach dem Kopf eines Unterverzeichnisses.
3. **Vierte Zufallsstichprobe** ab Rang 197 nach derselben Regel.
4. **Einschätzung für den Gesamtimport:** Ist die Restrate für Einzelformen in der Gliederung tragbar?
