# Siebte Nachprüfung am Excel-Stand 20.11.2026, 18:11

Geprüft wurden `findmittel_excel/` vom 20.11.2026, 18:11, dazu `testdaten_excel/` und `D151210_scope_import.xlsx`.
- **Skript:** sha256 `fde790ac3da62433…`, 5943 Zeilen. Eingebaut sind der Patch der Prüfsession (B, C, A, E, N, O, dazu F und D3657)
  und die D151210-Runde der Hauptsession.
- **Schnappschuss «neu7»:** `/private/tmp/claude-501/-Users-stazh-Documents-GithubRemops-ruedtim-SAR-verzeichnisse/8676ca0a-ed31-46c1-8dba-a1d020906498/scratchpad/neu7/`.
- **Vergleich:** mit dem Stand 15:43 der sechsten Nachprüfung.
- **Stand beim Abschluss:** `findmittel_excel/`, `testdaten_excel/`, D151210 und das Skript im Projekt waren noch identisch mit dem
  Schnappschuss.
- **Belege:** Jedes Urteil ist am PDF belegt.

## Kurzfazit

- **Ergebnis für die Push-Entscheidung:** Der Stand 18:11 ist in allen geprüften Punkten besser als 15:43.
  - Es gibt keine neue kritische Verschlechterung, keinen Textverlust und keine Änderung an Bestandszeilen, Teil-Nummern oder
    Kennzahlen.
  - Die neuen Fehler sind mittel oder gering.
  - Die einzige grössere Verschlechterung betrifft 57 Teile in D151210. Dort stehen die Unterlagen nach «:» im Titel, das Darin
    ist leer; der Inhalt ist nicht verloren.
  - Aus Sicht der Prüfung ist die Fassung stabil genug für einen Push. Besser wäre es, vorher die Doppelpunkt-Abtrennung für Teile
    nachzuziehen (Punkt 1 der offenen Punkte).
- **Geänderte Einheiten am PDF beurteilt: 1'095, alle Änderungen seit 15:43 ausser denen des Patches.** 950 besser, 85 gleich,
  60 schlechter.
  - D151210: 775 Einheiten (665 besser, 54 gleich, 56 schlechter).
  - Übrige Dateien: 320 Einheiten (285 besser, 31 gleich, 4 schlechter).
- **D151210:** Alle 774 geänderten Einheiten und die eine weggefallene sind am PDF geprüft.
  - Die Titel vom Nachbarteil (Z291) sind ganz weg: 121 → 0. Die Teil-Nummern sind eindeutig (Z290).
  - 8.1.1.44. hat die Teile 1–5 ohne den erfundenen «Teil 6».
  - 671 Teile, die um 15:43 einen Sammel- oder Nachbartitel «…, Teil n» trugen, haben jetzt ihren eigenen Titel. Meist sind es
    Produktionen in 5.2.4.x/5.2.5.x, dann mit dem Premierendatum als Zeitraum.
  - Von den 76 Zeilen aus Runde 6 sind 21 behoben, 14 teilweise, 39 offen und 2 schlechter. 34 der 76 sind von der
    Hauptsession bewusst offen gelassen (29 offen, 5 teilweise).
- **Übrige 79 Dateien:**
  - Die 320 Einheiten mit Änderungen der Hauptsession sind am PDF geprüft.
  - Der Patch ist vollständig eingebaut; die Fallsets ergeben am Stand 18:11 dieselben Zahlen wie in der Prüfsession: A 11/12,
    B 37/38, C 10/12, F 5/7.
  - Von 50 Zeilen aus Runde 6 mit geänderten Einheiten sind 14 behoben, 21 teilweise, 14 offen und 1 schlechter, nämlich
    D3808 4., die Nebenwirkung des Patches.
- **Neue Fehler: 28**, davon 2 kritisch, 18 mittel und 8 gering.
  - Die beiden kritischen bestanden schon um 15:43 und sind jetzt erst erfasst: D3612 3.A./3.E. mit 7 erfundenen Einheiten und
    D3861 7.1. mit Bereichszeilen als Einheiten.
  - Durch Änderungen der Hauptsession: 20 Zeilen, nach Ursache:
    - 8e2bd7f9: 15 Zeilen, darunter die Sammelzeile mit den 57 Teilen;
    - Änderung 2 (Titel der Einheit für Teile ohne eigenen Titel): 2;
    - Änderung 6 (« - » in Anführungen): 2;
    - Änderung 5 (Rollenbücher): 1.
  - Durch den Patch: 1 (D3808 4.).
  - Schon um 15:43 vorhanden: 7.
- **Textverlust:** Die 335 Textstücke von 15:43 ohne wörtliches Gegenstück sind alle geprüft. Keines ist verloren oder falsch
  zugeordnet. Es sind entfernte Füll- und Nachbartitel, neu auf Titel, Darin und Zeitraum verteilter Text sowie Spannen, die
  jetzt in der Anmerkung stehen.
- **Kennzahlen:**
  - Einheiten: 49'331 → 49'330 (D3324: erfundene 2. weg).
  - «[ohne Titel]»: 35 → 34.
  - «Text erfasst» 100 %: 695 Dateien wie vorher.
  - Doppelte Schlüssel: 10 überzählige Zeilen, nur D2681.

## Methode

1. **Schnappschuss «neu7».** Kopiert sind nach `…/scratchpad/neu7/`:
   - `findmittel_excel/` (716 Dateien, alle 18:11) und `testdaten_excel/` (13);
   - `D151210_scope_import.xlsx` (sha256 2e045b60…);
   - `findmittel_zu_scope.py`.

   Die sha256 aller Dateien stimmen mit der Quelle überein.
2. **Vergleich 15:43 ↔ 18:11.**
   - Inhaltlich geändert sind 80 Dateien in `findmittel_excel/` (Vergleich aller Blätter ohne die Zeile «Erzeugt»). Das ist
     genau die Liste in `zellvergleich_1543_1811.txt`.
   - Bei den Testdateien sind es 5: D149628, D151210, D177460, D3031 und D3186.
   - Einheitenvergleich über (Signatur, n-tes Vorkommen): 48'178 unverändert, 1'151 geändert, 2 entfernt, 1 neu.
   - Dazu ausgewertet wurden die Art jeder Zeitraum-Änderung, Text von 15:43 ohne Gegenstück (335 Stücke), gekürzte Titel,
     Teil-Nummern, Bestandszeilen und die Kennzahlen.
3. **Herkunft der Änderungen.** In den 79 Dateien ausser D151210 kommt jede Änderung von einer von drei Stellen:
   - aus den Änderungen der Hauptsession bis 8e2bd7f9 (229 Einheiten, davon 144 in D149628);
   - aus dem Patch der Prüfsession (81 Einheiten, an den Fallsets aus Runde 6 geprüft);
   - aus den Änderungen der Hauptsession nach 8e2bd7f9 (91 Einheiten).

   Dafür habe ich drei Läufe verglichen: 15:43 gegen 8e2bd7f9, 8e2bd7f9 gegen 8e2bd7f9 mit Patch, und 8e2bd7f9 mit Patch
   gegen 18:11. Der Patch ist vollständig eingebaut. Nur bei D2857 2.1. hat eine spätere Änderung noch das Darin verändert;
   O2 hat das geprüft.
4. **D151210.** Seit 15:43 haben sich 774 von 3'161 Einheiten auf 150 Seiten geändert, eine Einheit ist weggefallen.
   - Je Seite gibt es eine Vergleichsdatei: PDF-Text, alle Einheiten 18:11 und bei geänderten Einheiten den Wert von 15:43
     (`…/np7/d151210/seiten/`).
   - Vier Prüfer (D1–D4, S. 1–200, 201–223, 224–245 und 246–424, je rund 190 geänderte Einheiten) haben jede geänderte Einheit
     am PDF beurteilt.
   - Alle 76 D151210-Zeilen aus `funde_nachpruefung6.csv` haben einen Status bekommen. 37 davon betreffen laut Abgleich nur
     unveränderte Einheiten.
5. **Übrige 79 Dateien.** Zwei Prüfer haben jede Einheit am PDF beurteilt, deren Wert eine Änderung der Hauptsession verändert
   hat: O1 die 154 in D149628, O2 die 166 in 48 weiteren Dateien.
   - Sammlungen gleichartiger Teile (D1437, D3231, D32837, D3357) hat O2 an allen Kopfzeilen und an Stichproben der Darin-Listen
     geprüft.
   - Dazu kamen die 50 Zeilen aus Runde 6, deren Einheiten sich geändert haben, und die 197 Textstücke ohne Gegenstück.
6. **Eigene Prüfungen (Gruppe 0):**
   - Kennzahlen mit zwei Zählweisen;
   - Fallsets aus Runde 6 am Stand 18:11;
   - Einbau des Patches;
   - Testdaten;
   - Gegenprobe an 8 zufälligen D151210-Einheiten und an zwei gemeldeten Verschlechterungen;
   - Suchlauf nach Teilen mit «…: Unterlagen» im Titel und leerem Darin.
7. **Zusammenführen** mit `methode/np7_zusammenfuehren.py`.
   - Die Spalten sind wie in `funde_nachpruefung6.csv`; `ist` ist der Stand 15:43, `neu_ist` der Stand 18:11.
   - D151210-Zeilen tragen vorn in der Bemerkung ihre Nummer «#n» aus der D151210-Liste der Runde 6. Die von der Hauptsession
     bewusst offen gelassenen beginnen in `neu_ist` mit «[bewusst offen (Hauptsession)]».
   - Anleitung: `methode/ANLEITUNG_NACHPRUEFUNG7.md`.

## D151210

**Urteile je Bereich** (geänderte bzw. weggefallene Einheiten, am PDF):

| Bereich | Einheiten | besser | gleich | schlechter |
|---|---:|---:|---:|---:|
| D1: S. 1–200 | 201 | 192 | 0 | 9 |
| D2: S. 201–223 | 188 | 179 | 7 | 2 |
| D3: S. 224–245 | 194 | 156 | 3 | 35 |
| D4: S. 246–424 (mit dem weggefallenen «Teil 6» von 8.1.1.44.) | 192 | 138 | 44 | 10 |
| **Summe** | **775** | **665** | **54** | **56** |

Von den 35 «schlechter» in D3 sind 29 Teile mit Unterlagen im Titel (siehe unten), in D1 und D4 stecken weitere.

**Was jetzt stimmt:**
- **Z290, Z291:** Die Teil-Nummern sind eindeutig und in PDF-Reihenfolge. Die Titel vom Nachbarteil sind ganz weg: 121 Teile
  um 15:43 (D1 29, D2 47, D3 10, D4 35), jetzt keiner.
- **Eigene Titel:** Die Teile der Produktionslisten 5.2.4.x und 5.2.5.x haben fast alle ihren eigenen Titel statt «Produktionen des
  Schauspielhauses und nicht realisierte Projekte, Teil n». Das Premierendatum ist der Zeitraum (D1: 189 Teile, D2: 135, D3: 181).
  - Beispiel ID 1234, 5.2.4.12. Teil 13: «John Gabriel Borkman, Schauspiel von Henrik Ibsen», = 11.10.1979, Darin «Bühnenpläne» /
    «Korrespondenz, …».
- **8.1.1.44.:** Die Teile 1–5 sind richtig, es gibt keinen erfundenen «Teil 6» mehr. Die angeklebten Signaturen am Darin-Ende
  sind weg.
- **Fotolisten 8.1.1.x:** Die «Titel von Autor»-Listen sind meist richtig getrennt: Regel 4 behebt 20 von 28 bzw. 10 von 14
  Fällen. Bei den Negativen 8.3.x und den Plakatlisten wirkt sie nicht.
- **Kein Text verloren:** Alle 138 Textstücke ohne Gegenstück sind geprüft.

**Zeilen aus Runde 6 (76):**

| | behoben | teilweise | offen | schlechter | Zeilen |
|---|---:|---:|---:|---:|---:|
| von der Hauptsession bewusst offen | – | 5 | 29 | – | 34 |
| übrige | 21 | 9 | 10 | 2 | 42 |
| **Summe** | **21** | **14** | **39** | **2** | **76** |

- **Behoben:** #1 (Z290), #2 (Z291), #6, #9, #10, #12, #17, #19, #22, #31, #38–#46, #54, #55. Darunter ist der kritische Fall
  #55 (8.1.1.44. Teil 6).
- **Teilweise:** #13, #15, #16, #21, #23, #27, #29, #30, #48, #52, #53, #56, #65, #75.
- **Offen** (ohne die bewusst offenen): #8, #24, #28, #32, #36, #57–#60, #62.
- **Schlechter:**
  - #33, 5.2.5.14. Teil 2: neu falsch getrennt «… „Briefwechsel Dürrenmatt» / «Frisch“ …».
  - #47, 6.53. Teil 3: Die Verschmelzung «Dürrenmatt, Friedrich: Der Meteor Dürrenmatt-Lesung, diverse Texte» ist jetzt der
    Teil-Titel.

**Neue Fehler in D151210: 17 Zeilen, keine kritisch, 11 mittel, 6 gering.** Nach Ursache: 8e2bd7f9 11, Änderung 2 1,
Änderung 5 1, vor 15:43 4.

- **Unterlagen nach «:» im Titel, Darin leer (mittel, 8e2bd7f9).** Das ist die Sammelzeile aus dem eigenen Suchlauf.
  - Am Stand 18:11 haben 59 Teile «…: Korrespondenz, …» bzw. «…: Briefe, …» im Titel und kein Darin. Um 15:43 waren es 6, davon
    sind 4 inzwischen richtig; 57 sind neu, meist in 5.2.4.x (31) und 5.2.5.x (25).
  - Beispiele:
    - ID 60, 2.3.2.3. Teil 3: «Nachtessen aus Anlass des Rücktrittes des Direktors …: Einladung, Menü-Karte, Tischordnung».
    - 5.2.4.15. Teil 10: «Polenaktion. … Matinee: Korrespondenz, Programm der Matinee».
    - 5.2.4.32. Teil 9: «Wolfgang Stendar liest Sigmund Freud, Lesung: Mitteilung».
  - Um 15:43 standen diese Teile unter dem Sammeltitel, die ganze Zeile im Darin; der eigene Titel ist ein Gewinn, die Grenze
    ist falsch.
  - Ursache laut D3: Für Teile läuft `kopf_und_rumpf` ohne Doppelpunkt-Regel. Die Ersatzregel trennt nur, wenn vor dem «:» «von X»
    steht oder ein Premierendatum folgt (`UNTERLAGEN_DOPPELPUNKT`; dort fehlt auch «Brief» neben «Briefe»).
  - Der Art nach entspricht das den bewusst offenen #20/#30; die Prüfer D3 und D4 haben es nur in den Notizen gezählt.
- **Unterlagen nach einem Tabulator auf der Titelzeile bleiben im Titel (mittel, 8e2bd7f9).** IDs 1261, 1274, 1293, 1344,
  1365 und 1167, zum Beispiel «Antonius und Kleopatra, Drama von William Shakespeare Briefe, Aufführungsfotos».
- **Zeitraum aus dem Werktitel oder einem einzelnen Darin-Jahr (mittel, 8e2bd7f9).** Um 15:43 galt die Spielzeit.
  - ID 1296 «Aus dem Leben der Regenwürmer. Ein Familiengemälde von 1856, …»: 1856–01.04.1984.
  - ID 1343 «… Landi-Wiese 1939–1945, diverse Projekte»: 1939–1945.
  - ID 1155 «… (Wiederaufnahme von 1973)»: = 1973.
  - ID 1183 «… Zürich 1917 …»: 1917–03.02.1977.
  - ID 1717: 1848–1900 aus einem Ausstellungstitel.
  - ID 1716: = 1948 aus «Die Verborgenen 1948».
  - ID 1842: = 1991.
  - Dazu 6 Teile in D3 mit einem einzelnen Darin-Jahr statt der Spielzeit (1493, 1569, 1578, 1611, 1614, 1615). Ursache: Teile
    mit eigenem Titel erben die Spielzeit erst nach der Darin-Schätzung.
  - In Serien folgen daraus falsche Hinweise. Die beiden ersten habe ich am PDF-Text nachgeprüft.
- **Erster Listenpunkt als Teil-Titel (mittel, 8e2bd7f9).** IDs 1826, 1847 und 1849 sowie ID 60/62 (ein eingerückter
  Strichpunkt, der die Liste des Vorteils fortsetzt). Ursache: `_liste_folgt` sieht nur 4 Zeilen weit, die Rollenbuchregel
  verlangt zwei «Name: Werk».
- **Fortsetzungsteile tragen den Serientitel (mittel, Änderung 2).** ID 61, ID 93 («Harry Buckwitz …, Teil 3» statt
  «Korrespondenz und Akten, Teil 3») und ID 141.
- **Rollenbücher (mittel, Änderung 5):** ID 2123, 6.51. Teil 4, zwei Rollenbücher sind verschmolzen.
- **Gering:**
  - Unterzeilen sind ohne «; » verbunden: 14 Teile in 5.2.4.1.–11. und 28 Teile in 5.2.4.27.–34., schon um 15:43; dazu 5.2.4.35.
  - ID 1410: «diverse» bei der falschen Zeile, schon um 15:43.
  - IDs 1604 und 1622: eine Zeilengrenze im Darin ist verloren, 8e2bd7f9.

## Übrige 79 Dateien

| Prüfer | Einheiten | besser | gleich | schlechter |
|---|---:|---:|---:|---:|
| O1: D149628 | 154 | 148 | 5 | 1 |
| O2: 48 Dateien | 166 | 137 | 26 | 3 |
| **Summe** | **320** | **285** | **31** | **4** |

- **Verbesserungen:**
  - D149628 27.1.4./27.1.5.: 133 Teile haben ihren eigenen Titel statt «…, Teil n», 29 davon mit genauerem Tag oder Monat.
  - Anführungen und Namenslisten sind wieder ganz.
  - Die Jubiläumsspanne steht jetzt in der Anmerkung (D149628, D177460 VII.267.).
  - D1395 15.1. Teil 5 «Walensee», ein bisher bewusst offener Fall, ist behoben.
  - Die Teile von D3231, D32837 und D3357 tragen nicht mehr den Titel des Nachbarteils.
- **Verschlechterungen und neue Fehler (11 Zeilen):**
  - D149628 23.4.4.3. (mittel, 8e2bd7f9): = 1959 statt = 08.11.1959. Das Jubiläums-Endjahr aus «125 Jahre Stadttheater Zürich
    1834 – 1959» verdrängt das genaue Datum derselben Zeile (`jahre_im_text`); das ist der einzige Fall «gleiche Jahre,
    ungenauer».
  - D149628 27.1.5. Teile 10/15/34/50 (mittel): Ein Wert aus der Datumsspalte steht mitten im Titel («Rezitationen von 1980
    Uhland»). Er stand schon um 15:43 im Text, mit 8e2bd7f9 rückte er in den Titel.
  - Dieselbe Ursache (`_an_tabstopp` trennt nach «von/im/bis/vom/und» nicht ab) steckt seit vor 15:43 in 30 weiteren Fällen in
    D149628, zum Beispiel 7.2.2.1. Teile 3–14 (eigene Zeile).
  - D176795 2.2.2. (mittel, 8e2bd7f9): «Ludwig Heinrich Friedrich von Podewils (-1838)» ergibt 1810–1838 statt = 1810;
    `PERSON_RE` kennt «(-JJJJ)» nicht.
  - D3793 5.9.3. (mittel, 8e2bd7f9, Strich nach der Signatur): Der Titel ist jetzt richtig, aber das Datum 14.08.1938 fehlt; die
    Serie 5.9. endet deshalb 1932.
  - D3861 7.1. Teil 2 (mittel, Änderung 2): trägt den Titel von Teil 3 «Johannes Weber …», weil `ergaenze_titel` auf den
    ersten Teil mit Titel zurückfällt.
  - D3808 4. (mittel, Patch): 1906–07.03.1946 durch die falsch zugeordneten Beilagen (Z350); Z320 ist deshalb schlechter.
  - Gering, Änderung 6:
    - In fünf Anführungen in D149628 (4.1.41., 4.1.55., 6.5.6., 20.1.2.6., 20.1.2.13.) steht jetzt « - » statt «-»
      («„Tages - Anzeiger“»).
    - D3709 2.2.: «Volley - Ball».
  - Kritisch, aber schon um 15:43 vorhanden:
    - D3612 VII.37.:3.A./3.E.: 7 erfundene Einheiten aus den Folgezeilen «A. Bodmer» und «E. Hafner-Tobler»; 46 Schreiben stehen
      bei der falschen Einheit.
    - D3861 7.1.: Die Bereichszeilen «7.1.–26.» und «7.1.–8.» werden zu Einheiten; Änderung 1 behebt das nicht.
- **Zeilen aus Runde 6 (50):** 14 behoben, 21 teilweise, 14 offen, 1 schlechter (Z320 D3808).
  - Die meisten Wechsel kommen aus dem Patch, zum Beispiel D175994 IV.A.65., D1877 2.1., D176151 2.3., D3063 40.1., D3067
    VIII.B.8., D452 7., D3828 3.1./3.16., D3324 2., D3657 6., D3718 4.2.6. und D149628 11.9.2./26.2.4.
  - Von der Hauptsession kommen D1395 15.1. («Walensee») und die Jubiläumsfälle.
- **Textverlust:** keiner unter den 143 bzw. 54 Stücken.

## Neue Fehler nach Ursache

| Ursache | kritisch | mittel | gering | Zeilen |
|---|---:|---:|---:|---:|
| 8e2bd7f9 (Änderungen der Hauptsession bis 16:15) | – | 13 | 2 | 15 |
| Änderung 2 (Titel der Einheit für Teile) | – | 2 | – | 2 |
| Änderung 5 (Rollenbücher) | – | 1 | – | 1 |
| Änderung 6 (« - » in Anführungen) | – | – | 2 | 2 |
| Patch der Prüfsession (D3808 4.) | – | 1 | – | 1 |
| schon um 15:43 vorhanden | 2 | 1 | 4 | 7 |
| **Summe** | **2** | **18** | **8** | **28** |

D149628 27.1.5. ist hier unter 8e2bd7f9 gezählt, weil die Ursache vor 15:43 liegt, der Fehler im Titel aber seit 8e2bd7f9.

## Gegenprobe

- 8 zufällig gezogene geänderte Einheiten in D151210 habe ich selbst am PDF-Text geprüft:
  - 6 sind klar besser: IDs 1234, 1323, 1424, 1486, 2395 und 2430 – eigener Produktionstitel mit Premierendatum, Fotolisten
    getrennt.
  - 2 sind besser mit Restfehler: ID 1566 «Lesung: Mitteilung» im Titel (gehört zur Sammelzeile), ID 1635 mit zwei verbundenen
    Darin-Zeilen.
  - Das deckt sich mit den Urteilen der Prüfer.
- Am PDF-Text bestätigt sind auch die von D2 gemeldeten Zeitraumfehler 1296 («Familiengemälde von 1856») und 1343
  («Landi-Wiese 1939–1945»).

## Wichtigste offene Punkte (für die nächste Runde der Hauptsession)

1. **Doppelpunkt-Abtrennung für Teile:**
   - 57 Teile in D151210 haben die Unterlagen nach «:» im Titel; dazu kommen die Tabulator-Fälle 1261 u. a.
   - Die Unterlagen-Regel sollte auch ohne «von X» vor dem «:» greifen, wenn nach dem «:» typische Unterlagen folgen; «Brief»
     gehört in die Wortliste.
2. **Zeitraum der Teile mit eigenem Titel:**
   - Jahre aus dem Werktitel («von 1856», «Landi-Wiese 1939–1945», «Wiederaufnahme von 1973») und einzelne Darin-Jahre sollten
     nicht vor der Spielzeit der Serie zählen.
   - Vorschlag: Wenn es ein Premierendatum gibt, gilt nur dieses; sonst die Spielzeit der Einheit vor der Darin-Schätzung.
3. **Änderung 2 bei Fortsetzungen:**
   - D151210 IDs 61, 93, 141 und D3861 7.1. Teil 2: Ein Fortsetzungsteil soll den Titel des fortgesetzten Teils tragen, nicht
     den Serientitel.
   - `ergaenze_titel` soll nicht auf einen späteren Teil zurückfallen.
4. **Erster Listenpunkt als Teil-Titel:** D151210 1826, 1847, 1849, 60/62 (`_liste_folgt`, Rollenbuchregel).
5. **Einzelfälle:**
   - D149628 23.4.4.3.: Das Jubiläums-Endjahr soll das genaue Datum derselben Zeile nicht ersetzen.
   - D176795 2.2.2.: «(-1838)» als Lebensdaten erkennen.
   - D3793 5.9.3.: Datum hinter dem Strich nach der Signatur.
   - Änderung 6: « - » nur, wo im PDF ein Strich mit Leerzeichen steht.
6. **Schon vor 15:43, jetzt erst erfasst:**
   - D3612 3.A./3.E. (kritisch) und D3861 7.1. (kritisch);
   - die Datumsspalte mitten im Titel in D149628 (30 Fälle, `_an_tabstopp`);
   - die verbundenen Unterzeilen in D151210 (gering).
7. **D3808 4.:** Die Beilagen nach der letzten Einheit gehören nicht ins Darin von 4. (Z350). Seit dem Patch verfälschen sie den
   Zeitraum.

## Dateien

- `stichproben/nachpruefung7.md` – dieser Bericht.
- `stichproben/funde_nachpruefung7.csv`: 154 Zeilen.
  - Die 76 D151210-Zeilen aus Runde 6 (#1–#76) stehen vorn, dann 50 Zeilen aus Runde 6 in den übrigen geänderten Dateien, zuletzt
    die 28 neuen.
  - Spalten wie in Runde 6; `ist` = Stand 15:43, `neu_ist` = Stand 18:11; Status behoben / teilweise / offen / schlechter / neu.
- `stichproben/methode/`: `ANLEITUNG_NACHPRUEFUNG7.md`, `np7_zusammenfuehren.py`.
- `stichproben/roh/`: `np7_d151210_D1` … `D4` und `np7_O1`, `np7_O2`, je mit `_urteile.csv` (1'095 Urteile) und `_notizen.md`;
  `np7_gruppe_0.csv`.
- Scratchpad `…/np7/`:
  - `diff/`, `diff_test/`, `zeitraum.csv`, `textverlust.csv`, `teile.json`, `gesamt.json`;
  - `d151210/seiten/` (Vergleichsdatei je Seite), `pakete/`;
  - `teil1_1543_8e2b.csv`, `teil2_patch.csv`, `teil3_8e2bpatch_1811.csv` (Herkunft der Änderungen).
