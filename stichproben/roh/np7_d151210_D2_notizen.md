# Nachprüfung 7, D151210, Gruppe D2 (S. 201–223), Stand 18:11

## Zahlen

- **Seiten:** 23 (S. 201–223), alle mit geänderten Einheiten.
  - Je Seite geprüft: PDF-Text (`pdftotext -layout`) und Wortpositionen (pdfplumber, Parameter wie `lese_zeilen`).
  - Dazu S. 224 für den Übergang zu D3 und S. 224–230 für die IDs von N370.
- **Einheiten:** 188 geändert, 0 neu, 0 weggefallen.
  - 186 Teile von 5.2.4.11.–5.2.4.25.
  - 2 Serien (5.2.4.19., 5.2.4.21.), bei denen sich nur der Prüfhinweis geändert hat.
  - Die 14 unveränderten Einheiten des Bereichs habe ich mitgesehen: 12 Serien sowie die Teile 1370 und 1412.
- **Prüfweg:**
  - Jede Einheit am PDF verglichen.
  - Zusätzlich automatisch je Teil:
    - Titel = Text der Produktionszeile bis zum Premierendatum;
    - von = Premierendatum;
    - Titel + Datum + Darin ergeben lückenlos den Eintragstext;
    - Darin-Grenzen gegen die PDF-Zeilen geprüft.
  - Alle Abweichungen habe ich einzeln angesehen.
- **Urteile (188):** besser 179, gleich 7 (1261, 1263, 1274, 1283, 1293, 1295, 1328), schlechter 2 (1296, 1343), unklar 0.
- **Ursache:** alle 188 Änderungen kommen schon aus **8e2bd7f9**.
  - Der Lauf mit 8e2bd7f9 (`$S/verb/aus_basis/D151210_scope_import.xlsx`, Skript `verb/basis`, sha256 8e2bd7f9…) stimmt für jede Einheit von S. 201–223 mit 18:11 überein.
  - Verglichen habe ich Titel, Zeitraum, Anm., Quelle, Darin, Hinweise, Teil, Parent, Stufe und Ebene.
  - Die Änderungen 1–9 der Hauptsession und der Patch wirken in diesem Bereich nicht.
- **Fundzeilen aus Runde 6 (5):**

  | Zeile | Status | Kurz |
  |---|---|---|
  | N369 #15 | teilweise | bewusst offen; ID 1332 behoben, 1726/1987 unverändert |
  | N370 #16 | teilweise | 33 von 34 behoben, offen ID 1366 |
  | N371 #17 | behoben | |
  | N373 #19 | behoben | |
  | N374 #20 | offen | bewusst offen |

- **Neue Zeilen:** 3 (2 mittel, 1 gering).
  - Jahr aus dem Werktitel als Zeitraum (2 Fälle, Verschlechterung).
  - Unterlagen nach Tabulator im Titel (5 Fälle).
  - ID 1410: «diverse» verrutscht (vor 15:43).
- **Textverlust (47 Stücke):** kein echter Verlust und keine falsche Zuordnung.
  - 7 Inhaltsstücke stehen jetzt aufgeteilt in Titel, Zeitraum und Darin derselben Einheit (IDs 1230, 1239, 1255, 1315, 1382, 1414, 1415).
  - 40 Stücke sind entfernte Nachbartitel:
    - «Der Kaufmann von Venedig …, Teil 6–17»;
    - «Die Insel …, Teil 7–21»;
    - «Harry Buckwitz zur Erinnerung, Matinee, Teil 6–18».
  - Die Originale stehen weiter bei ID 1332, 1350 und 1370.

## Z291 (Titel vom Nachbarteil, im Paket Z261) für S. 201–223

- **15:43:** 47 Teile trugen den Titel eines anderen Teils:
  - 5.2.4.13. Teil 15 (1);
  - 5.2.4.21. Teil 6–17 (12);
  - 5.2.4.22. Teil 7–21 (15);
  - 5.2.4.23. Teil 6–18 (13);
  - 5.2.4.24. Teil 16 (1);
  - 5.2.4.25. Teil 14–18 (5). Teil 19–21 stehen auf S. 224 (D3) und sind dort ebenfalls behoben.
- **18:11:** 0 Teile mit Nachbartitel. Alle 47 tragen den eigenen Produktionstitel.
  - Auch die 135 Teile mit «Produktionen des Schauspielhauses und nicht realisierte Projekte, Teil n» haben jetzt ihren eigenen Titel.
  - Im Bereich hat kein Teil mehr einen Titel «…, Teil n».
- **Was bei den 47 bleibt:**
  - Bei 9 stehen die Unterlagen noch im Titel:
    - 7 von der Art #20 (1351, 1352, 1356, 1372, 1383, 1413, 1416);
    - 2 nach Tabulator (1344, 1365, neue Zeile).
  - Bei 1 ist der Zeitraum falsch (1343, neue Zeile).

## Verbesserungen (Hauptmuster)

1. **Produktionszeile als eigener Teil-Titel, Premierendatum als Zeitraum, Unterzeilen als eigene Darin-Einträge.**
   - Das gilt für 144 Teile mit Datum.
   - Beispiel ID 1216 (S. 201):
     - Titel «Liebelei, Schauspiel von Arthur Schnitzler»;
     - Zeitraum Genau 08.03.1979;
     - Darin «Bühnenpläne und Skizzen» • «Korrespondenz, …».
     - Vorher: «Produktionen …, Teil 11», 1978–1979, die ganze Produktionszeile im Darin.
   - Titel über zwei Zeilen werden richtig zusammengesetzt, z. B. 1218, 1223, 1287, 1302, 1340, 1390, 1393.
   - Steht die erste Unterzeile auf der Datumszeile, wird sie richtig abgetrennt: 1255, 1265, 1296, 1304, 1390, 1398.
2. **Unterlagen nach «… von X:» kommen ins Darin**, z. B. 1217, 1240, 1257, 1258, 1273, 1339, 1359, 1374, 1414, 1415, 1417.
   - Ebenso nach einem Zeilenumbruch, z. B. 1232, 1235, 1252, 1262, 1284, 1348, 1349, 1386.
   - Bei Teilen ohne Datum bleibt der Zeitraum die Spielzeit.
3. **Fälle aus Runde 6 erledigt:**
   - N371 (1350) und N373 (1398, 1399);
   - N369 bei 1332;
   - N370 bei 33 von 34 Teilen;
   - ausserhalb des Pakets N366 bei 1251 und N364 für die 26 IDs auf S. 201–211 (siehe unten).
4. **Teile mit Projekten bekommen die Spielzeit als Titeldatum** (Anm «1983/84», Quelle Titel) statt «übergeordnete Einheit»: 1312, 1274, 1293, 1344, 1365, 1383. Die Werte sind gleich geblieben.

## Verschlechterungen

1. **Jahr aus dem Werktitel als Zeitraum** (2 Fälle, mittel, neue Zeile).
   - **ID 1296** (S. 209, 5.2.4.19. Teil 2), «… Ein Familiengemälde von 1856, Stück von Per Olov Enquist (01.04.1984)»:
     - jetzt 1856–01.04.1984 mit Hinweis «Mehrere Zeitangaben im Titel»;
     - 15:43: 1983–1984.
   - **ID 1343** (S. 215, 5.2.4.21. Teil 16), «… Landi-Wiese 1939–1945, diverse Projekte»:
     - jetzt 1939–1945; «1939–1945» fehlt im Titel;
     - 15:43: 1985–1986.
   - Folge: neue Prüfhinweise bei den Serien 1295 «(1856–1984)» und 1328 «(1939–1986)». Höhere Ebenen sind unverändert.
   - **Ursache:** Der Teil-Titel ist jetzt die Produktionszeile. `zeitraum_aus_titel` vereinigt alle Zeitangaben des Titels (Z. 4206).
     - Der Rahmenfilter (Z. 4162, `RAHMEN_VORLAUF` = 150) lässt 1856 stehen.
   - Der Art nach wie die bewusst offenen inhaltlichen Zeitraumfälle #64 und #71. Als neue Zeile gemeldet, weil der Zeitraum um 15:43 noch stimmte.
2. **Unterlagen nach Tabulator auf der Titelzeile bleiben im Titel** (5 Fälle, mittel, neue Zeile).
   - Die Fälle:
     - 1261 «Antonius und Kleopatra, Drama von William Shakespeare Briefe, Aufführungsfotos»;
     - 1274 «Projekte und Besetzungen 1981/82 inkl. Gastspiele Korrespondenz, Dispositionen und Aktennotizen»;
     - 1293 «diverse Projekte 1982/83: Informationsmaterial»;
     - 1344 und 1365 «Verschiedene Projekte 1985/86 (1986/87) Korrespondenz».
   - Das Darin ist leer; die Spielzeit steht mitten im Titel.
   - **Ursache:** `verarbeite` Z. 3292–3300 trennt die Unterlagen nur ab, wenn ein «… von X: » (m_u) oder ein Premierendatum (m_k) davor steht. Die Lücke von 19–26 pt vor den Unterlagen wird nicht ausgewertet.
   - Urteil:
     - «gleich» bei 1261, 1274, 1293, die um 15:43 einen allgemeinen Titel und das ganze Darin hatten;
     - «besser» bei 1344, 1365, die vorher den Nachbartitel trugen.
3. **Kosmetik, vor 15:43** (gering, neue Zeile):
   - ID 1410 (S. 223): «Skizzen zum Bühnenbild diverse» • «Fotoaufnahmen; Korrespondenz, …».
   - Das verrutschte «diverse» gehört zu «Fotoaufnahmen».

## Bewusst offen – gleichartige Fälle (nicht neu gemeldet)

- **Titel über mehrere Zeilen: 11 Fälle.**
  - **Art #20** – «Titel:» plus Unterlagenzeile im Titel, Darin leer: 8 Fälle.
    - IDs 1263, 1351, 1352, 1356, 1372, 1383, 1413, 1416.
    - Alle ohne «von X» vor dem Doppelpunkt, darum greift m_u nicht.
    - #20 selbst (ID 1412) ist unverändert.
  - **Art #35** – kurze Unterzeile an die Titelfortsetzung gehängt: 1 Fall.
    - ID 1283 «… Kongresshaus, Theaterball Briefe, Besetzungsliste».
  - **Art #34** – Titelfortsetzung im Darin: 2 Fälle.
    - ID 1281 «Familie Chäller …:» / «Züglete … (16.10./01.12.1982)» als 1. Darin-Eintrag, Quelle Darin (geschätzt). Der Zeitraum stimmt.
    - ID 1308: «Komödie von Fritz von Herzmanovsky-Orlando:» steht im PDF erst nach «Bühnenpläne und Skizzen» und landet im Darin.
- **Datumsreste im Titel: 1 eigener Fall**
  - ID 1277 «… (Koproduktion mit der Schauspiel-Akademie, 16.12.1982)».
  - Dazu 5 Fälle, in denen die Spielzeit nur deshalb mitten im Titel steht, weil die Unterlagen im Titel stehen: 1274, 1293, 1344, 1365, 1383.
- **Inhaltliche Zeitraumfälle:**
  - 2 Fälle (1296, 1343). Sie sind gleicher Art, aber als Verschlechterung gemeldet (siehe oben).
  - Sonst keine weiteren.

## Sonst beobachtet (kein Fund)

- **Fehlende Kommas am Zeilenende im PDF:** Die Folgezeile ist mit Leerzeichen verbunden, wie schon um 15:43.
  - Beispiele: «Aktennotizen Informationsblatt …» (1226, 1234, 1236, 1259 u. a.), «Probendisposition zwei Fotoaufnahmen eines Balkons» (1247), «… Fred Tanner Besetzungslisten» (1223).
- **Stärker eingerückte Folgezeilen** sind nach der Konvention mit «; » angehängt (1305, 1329, 1371).
- **PDF-Eigenheiten richtig übernommen:**
  - «Informationsblatt der G Gesellschaft» (1360, Streuzeichen x 509 im PDF);
  - «SchauspielhausKeller» (1401);
  - «Altwiibersumme r» wird zu «Altwiibersummer» (1334);
  - Premiere 25.05.1982 in der Spielzeit 1982/83 (1290, Datum laut PDF).
- **Premieren am 31.12.** (1236, 1266, 1280, 1287, 1308, 1321, 1341, 1373, 1397, 1407): Das Datum steht so im PDF (Silvesterpremieren).

## Ausserhalb meines Bereichs

- **D1-Zeilen:**
  - N366 #12: ID 1251 (S. 204, 5.2.4.13. Teil 14) ist behoben. Titel ohne «(07.02.1981) Bühnenpläne», Genau 07.02.1981, Darin «Bühnenpläne».
  - N364 #10: Die 26 IDs auf S. 201–211 (1219 … 1314) sind behoben. Die erste Unterzeile ist jetzt ein eigener Darin-Eintrag, die Produktionszeile ist der Titel.
- **D3, S. 224:**
  - Die Teile 5.2.4.25. 19–21 (1418–1420) haben eigene Titel.
  - ID 1420: «Siehe auch Sign. VII.200. 5.2.5.» steht jetzt in «Verwandte Verzeichnungseinheiten» statt im Darin; das ist plausibel.
  - ID 1423 (5.2.4.26. Teil 3) hat jetzt 1989–1991, Quelle Titel (betrifft N375 #21).
- **N370:** Auch die IDs auf S. 224–230 (1424, 1432, 1436, 1441, 1443, 1445, 1446, 1452, 1460, 1472) sind behoben. Gezählt in N370.
