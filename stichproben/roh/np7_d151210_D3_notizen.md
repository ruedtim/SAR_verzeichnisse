# D151210 (VII.200., Schauspielhaus Zürich AG) – siebte Nachprüfung, Bereich D3, PDF-Seiten 224–245

Beurteilt: `$S/neu7/D151210_scope_import.xlsx` (Stand 18:11) am PDF `$P/D151210.pdf`, Vergleich mit 15:43
(`$S/neu6/…`). Skriptzeilen beziehen sich auf `$S/neu7/findmittel_zu_scope.py` (fde790ac…). Hilfsdateien in
`$S/np7/tmp_D3/`.

## Vorgehen

- Die PDF-Zeilen kommen aus pdfplumber, mit den gleichen Parametern wie `lese_zeilen`. Jede Zeile hat x-Position und
  Schrift (kursiv/fett).
- Die 201 Signaturzeilen der Seiten sind in PDF-Folge den 201 Excel-Einheiten zugeordnet. Alle Nr. im PDF stimmen.
- Jede geänderte Einheit habe ich am PDF gelesen: Titel, Darin, Zeitraum, Verwandte und Prüfhinweise. Dazu kamen
  automatische Prüfungen:
  - Wortabgleich PDF ↔ Excel: kein Wort fehlt.
  - Analyse jeder Zeilenfuge, also wie zwei PDF-Zeilen im Excel verbunden sind.
  - Premierendatum gegen von/bis.
  - Teil-Nummern.
- Für die Ursache habe ich die Zwischenstände der Prüfsession verglichen: `$S/verb/aus_basis` = 8e2bd7f9,
  `aus_arbeit8` = Patch, `aus_haupt_neu`/`aus_haupt_f3` = Hauptsession.

## Zahlen

**Umfang**
- 22 Seiten, alle mit geänderten Einheiten.
- 201 Einheiten, IDs 1418–1618:
  - 9 Serienköpfe 5.2.4.26.–5.2.4.34.;
  - 192 Teile, Produktionen der Spielzeiten 1989/90 bis 1998/99.
- Geändert: 194 Einheiten, nämlich 192 Teile und 2 Serien, bei denen sich nur der Prüfhinweis geändert hat (1421, 1585).
- Unverändert: 7 Serienköpfe.
- Neu: 0. Weggefallen: 0.
- Parent, Stufe, Ebene, Teil-Nummer, Signatur, Schachtel und Umfang sind im ganzen Bereich unverändert und richtig.

**Urteile (194)**
- besser 156, gleich 3, schlechter 35, unklar 0.
- Ursache:
  - 8e2bd7f9: 191;
  - Änderung 9: 2 (1541 «Die neue Schweiz», 1564 Theater-Labor-Tage);
  - Änderung 1: 1 (1536 «85. Geburtstag …»).
- Der Patch wirkt im Bereich nicht: Kein Feld hat seinen Wert von 18:11 erst mit `aus_arbeit8` bekommen.
- Die Änderungen 2–8 der Hauptsession wirken hier ebenfalls nicht. Zu Änderung 2: Es gibt keine titellosen Teile mehr.

**Die 35 Urteile «schlechter»**
- 6 haben eine neue Zeile (Zeitraum-Sammelzeile).
- 29 gehören zu bewusst offenen Arten und haben deshalb keine Zeile in `np7_d151210_D3.csv`; sie sind unten gezählt:
  - 28 mit Unterlagen im Titel (Art #20);
  - ID 1589 mit dem Zeitraum aus Titeljahren (Art #64).

**Status der Runde-6-Zeilen**
- N375/#21 teilweise (bewusst offen; 3 von 4 behoben, 1824 offen).
- N376/#22 behoben.
- N377/#23 teilweise (7 von 14 behoben, 7 offen).
- N378/#24 offen.

**Neue Zeilen: 3**
- kritisch 0.
- mittel 1: Zeitraum aus Darin-Jahr statt Spielzeit, 6 Fälle.
- gering 2:
  - Darin-Unterzeilen verschmolzen, 28 Fälle, vor 15:43;
  - ID 1604, Fuge seit 8e2bd7f9.

**Textverlust (18 Stücke): kein echter Verlust, keine Fehlzuordnung**
- 11 Stücke sind nur neu auf Titel, Darin und Zeitraum verteilt: 1418, 1419, 1432, 1444, 1476, 1477, 1491, 1520, 1568,
  1580, 1605.
- 7 Stücke sind der alte Nachbartitel «Prinz Friedrich … (30.09.1990) Bühnenpläne und Skizzen, Teil 13–19» von
  1433–1439. Sie fehlen zu Recht; der Text steht bei 1432.
- Der Wortabgleich über alle 201 Einheiten findet sonst nur die entfernte verrutschte Signatur «5.2.4.25.» in 1420. Dazu
  gibt es einen Hinweis.

**Z291/#2 (Titel vom Nachbarteil) im Bereich: behoben**
- 15:43 trugen 10 Teile den Nachbartitel:
  - 1418–1420 «Tell gegen Hitler …, Teil 19–21»;
  - 1433–1439 «Prinz Friedrich von Homburg …, Teil 13–19».
- 18:11 sind es 0. Kein Titel endet mehr auf «, Teil n», kein Teiltitel kommt innerhalb einer Serie doppelt vor.
- Die 181 Teile mit «Produktionen des Schauspielhauses und nicht realisierte Projekte, Teil n» tragen jetzt alle ihren
  eigenen Produktionstitel. Das bewirkt 8e2bd7f9 (Strich nach der Signatur fällt weg), nicht Änderung 2.

**Z290/#1 (Teil-Nummern)**
- Unverändert.
- In allen 10 Serien des Bereichs lückenlos 2…n in PDF-Folge, zum Beispiel 5.2.4.30. mit Teil 2–28.

## Verbesserungen (Hauptmuster)

**Eigener Produktionstitel für 192 Teile**
- 159 Titel sind einwandfrei, zum Beispiel:
  - 1418 «Am Ziel von Thomas Bernhard»;
  - 1453 «Party Time: Genau – Noch einen Letzten – Party Time, Stücke von Harold Pinter». Der Doppelpunkt im kursiven
    Werktitel bleibt.
  - 1528 «Der Reigen von Arthur Schnitzler / Der reizende Reigen … von Werner Schwab im Schauspielhaus-Keller».
- Zweizeilige Titel sind richtig verbunden, zum Beispiel 1437 und 1584.
- Unterlagen nach «von …:» wandern ins Darin, zum Beispiel:
  - 1476 «Zorn, Stück von Ria Endres» / «Korrespondenz, …»;
  - 1490 «Oleanna, …: Korrespondenz,» / «Aufführungsvertrag, Aktennotizen».

**Zeitraum**
- 42 Premierendaten «(TT.MM.JJJJ)» sind jetzt Genau-Zeitraum mit Quelle Titel. Alle liegen in der Spielzeit der Serie.
- Eigene Aktenangaben gelten jetzt (N375):
  - 1423 «(Akten 1989–1991)» → 1989–1991;
  - 1435 → 1989–1991;
  - 1439 «… 1990–1992» → 1990–1992.
- 1488 Dürrenmatt-Tage → 25.03.–27.03.1994.
- 1428 «Akten ab 1990» → «ab 1990», wörtlich, mit Hinweis auf das offene Ende.
- 137 Teile ohne eigenes Datum behalten die Spielzeit.

**Darin**
- Die Unterzeilen sind jetzt eigene Einträge.
- Die Runde-6-Zeile #16 (Paket D2, S. 214–230) ist im Bereich S. 224–230 ganz behoben: 10 von 10. Betroffen waren 1424,
  1432, 1436, 1441, 1443, 1445, 1446, 1452, 1460, 1472.
- «Siehe auch Sign. VII.200. 5.2.5.» steht jetzt in «Verwandte», bei 1420 und 1439.

**Änderungen 1 und 9 bewähren sich**
- Änderung 1, ID 1536: Bei 8e2bd7f9 trug der Teil noch den Nachbartitel «Hexenbrände …, Teil 6». Jetzt heisst er «85.
  Geburtstag von Fritz Hochwälder, …».
- Änderung 9, ID 1541 «Die neue Schweiz: Kulturnation …, Koproduktion mit DRS2» mit Darin «Ablaufplan, …».
- Änderung 9, ID 1564: Bei 8e2bd7f9 war der Titel nach «… und dem» abgeschnitten und das Darin leer.

## Verschlechterungen (Hauptmuster)

### 1. Unterlagen nach «:» im Titel, Darin leer (Art #20) – 29 Teile, davon 28 schlechter

**Muster**
- Die Produktionszeile endet auf «:» und hat kein «von …». Dann hängt die Unterlagenzeile (x 141) am Titel.
- Auch Unterlagen direkt hinter dem Doppelpunkt auf der Titelzeile bleiben im Titel.
- Um 15:43 war das kein Fund: Der Titel lautete «Produktionen …, Teil n», das ganze Darin war ein Eintrag, und das
  entsprach dem Soll aus Runde 6.
- Die Art entspricht genau #20 («Tell gegen Hitler …: Informationsblatt, Gesprächsnotizen»). Sie ist bewusst offen und
  deshalb keine neue Zeile.
- Seit 8e2bd7f9 ist aber aus einem Einzelfall ein Muster geworden.

**Alle 29 Fälle**
- S. 224/226: 1426 «Abermals ein neues Jahr, Silvestergala: Briefe, …», 1439.
  - Bei 1439 ist das Gesamturteil trotzdem besser, weil Nachbartitel und Zeitraum behoben sind.
- S. 231–232: 1480 «Schauspielhaus-Tram-Projekt: Korrespondenz, …», 1483, 1484, 1485, 1487, 1488.
  - 1488 hat zusätzlich das Datum im Titel.
- S. 234–235: 1504, 1506, 1508, 1509, 1510, 1514, 1517.
- S. 236–237: 1527, 1532, 1533, 1534, 1537, 1538, 1539.
- S. 238–240: 1552, 1559, 1563, 1566, 1567.
- S. 242: 1587, 1588.

**Ursache**
- `kopf_und_rumpf` läuft für Teile mit `doppelpunkt=False` (Z. 3059, Aufruf Z. 3202/3205). Die Doppelpunkt-Regel in
  Z. 3111 greift deshalb nicht.
- Die Ersatzregeln greifen nur in zwei Fällen:
  - mit «von» vor dem Doppelpunkt und einem Wort aus `UNTERLAGEN_DOPPELPUNKT` (Z. 3019, Z. 3292). «Brief» fehlt dort, nur
    «Briefe» steht drin; deshalb bleiben 1527 und 1552 trotz «von» im Titel.
  - bei Titeln über 160 Zeichen (`teile_langen_titel` Z. 3148/3154). So werden 1461, 1516, 1518, 1584 und 1604 richtig
    geteilt.
- Auch S. 223 (Bereich D2) hat zwei Fälle dieser Art: 1413 «Circus Helvetia, Projekt: Konzept, …» und 1416
  «Autoren-Reden, …: Korrespondenz, …».

### 2. Zeitraum aus einem Jahr im Darin statt der Spielzeit – 6 Teile, neue Zeile (mittel)

**Fälle**
- 1493: = 17.05.1994, Datum eines Klausurpapiers; Spielzeit 1993/94.
- 1569: = 1982, aus «Korrespondenz ab 1982»; das «ab» geht verloren.
- 1578: 1997–1998, aus «Gastspiele 1997/98»; die Produktionsspielzeit 1996/97 fällt weg.
- 1611: = 1893, aus «Kopien der Radierung … von 1893».
- 1614 und 1615: = 1999, aus dem Gastspieljahr; Spielzeit 1998/99.

**Ursache**
- Mit eigenem Titel gilt der Teil nicht mehr als «Titel übernommen» (Z. 4297).
- Die Schätzung aus dem Darin (Z. 4308–4313) kommt dann vor der Spielzeit der Serie (Z. 4318–4319).
- Um 15:43 stimmte die Spielzeit.
- Abhilfe: Bei Teilen einer Serie mit ausdrücklichem Zeitraum die Spielzeit vor der Darin-Schätzung nehmen. Höchstens
  eine ausdrückliche Aktenangabe soll sie erweitern («Akten 1989–1991», «ab 1982»).

**Gleich gebaut, aber anderer Mechanismus: ID 1589 (S. 242), nur hier gezählt**
- Der Zeitraum 1933–1968 kommt aus dem Untertitel «… in der Geschichte des Schauspielhauses 1933–1968». Die Jahre fehlen
  dafür im Titel.
- Das ist Art #64 «Jahre im Titel = Gegenstand» und bewusst offen. Es ist aber eine Verschlechterung, denn 15:43 galt
  die Spielzeit 1997–1998.
- Folge: Die Serie 1585 bekommt den Hinweis «Untereinheiten reichen über den Zeitraum hinaus (1933–1998)».

### 3. Darin-Fuge verloren – ID 1604 (S. 244), neue Zeile (gering)
- 15:43 stand «… Mitteilungen; Programm, Flugblatt», 18:11 steht «… Mitteilungen Programm, Flugblatt».
- Grund: Der Block wird erst Titel und dann von `teile_langen_titel` geteilt; der abgetrennte Rest ist mit Leerzeichen
  zusammengesetzt.
- Einziger Fall im Bereich.

## Alte Fehler, jetzt sichtbar (neue Zeile, gering, vor 15:43)

- In 28 Teilen sind insgesamt 31 Unterzeilen mit Leerzeichen an die nächste Unterzeile gehängt. Typisch sind Zeilen, die
  bei x 420–530 enden und nicht auf Komma enden.
- Beispiele:
  - 1453/1464/1467 «… Fotos von Leonard Zubler Korrespondenz, …»;
  - 1574 «… Aktennotizen Bühnenpläne und Skizzen, …, Programm Informationsblatt …».
- Ursache ist der Breitentest in `ist_umbruch` (Z. 2583 ff.), wie bei #10/#16.
- Um 15:43 lagen sie im einen Darin-Eintrag je Produktion. Runde 6 hat nur die erste Unterzeile nach der Produktionszeile
  erfasst (#16).
- Kein Fund dagegen bei 1422 «Bühnenpläne und Skizzen Aufführungsvertrag, …», 1547, 1549 und 1551: Dort steht die
  Verbindung schon so in einer PDF-Zeile.

## Bewusst offene Arten (nur gezählt, keine neuen Zeilen)

**Titel über mehrere Zeilen: 31**
- 29 × Unterlagen im Titel (siehe oben).
- 1435: Titel «Chlaus Lymbacher, … (02.10.1990), Akten»; die Folgezeile der Titelspalte «1989–1991:» steht als
  Darin-Anfang (zugleich N377).
- 1562: kursiver Untertitel «Ferdinand Rieser und das Schauspielhaus Zürich» im Darin, Titelende am Strich (= N378).

**Datumsreste im Titel: 5**
- 1423 «… (Akten 1989–1991)»
- 1428 «… (14.03.1991), Akten»
- 1435 «… (02.10.1990), Akten»
- 1439 «… Schauspielhaus-Keller 1990–1992: …»
- 1488 «… 25. – 27. März 1994 (Koproduktion): …»
- Der Zeitraum stimmt jeweils.

**Inhaltliche Zeitraumfälle: 1**
- 1589 (siehe oben).
- 1428 «ab 1990» lässt die Premiere 14.03.1991 aus. Die Angabe ist wörtlich und unbedenklich.

**Nicht als Fund gewertet**
- Serie 5.2.4.26. (1421): Sie behält 1990–1991 aus «1990/91». Der neue Hinweis «Untereinheiten reichen über den Zeitraum
  hinaus (1989–1992)» trifft zu.
- 1557: «Nicht realisierte Projekte und Produktionen Akten» – «Akten» steht im PDF in derselben Zeile.

## Auffälliges ausserhalb des Bereichs (für D2/D4)

- **1821 (S. 277) und 1830 (S. 279), 5.4.4.21./5.4.4.23. Teil 2:**
  - Die ganze Namensliste «Gastspiele von Maria Becker, …» ist jetzt Titel (516 bzw. 809 Zeichen), das Darin ist leer.
  - Um 15:43 hiessen die Teile «Korrespondenz und Akten über Gastspiele, Teil 2».
  - Herkunft: 8e2bd7f9 machte die Zeile nach «- » zum Titel; Änderung 8 verbindet die Liste über den Umbruch.
  - Verschlechterung (Titel/Darin). Der «; »-Fehler aus N377 ist dort dagegen weg.
- **N377-Fälle, die noch offen sind (D4-Bereich):** 1766, 1771, 1782, 1791, 1794, 1833, alle unverändert «Wort; Wort».
- **1824 (S. 278):** weiter = 1988 statt 1987–1988 (N375).
- **1413 und 1416 (S. 223):** Art #20, wie oben.
