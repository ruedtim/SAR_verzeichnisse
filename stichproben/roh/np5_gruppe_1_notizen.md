# Fünfte Nachprüfung, Gruppe 1: Notizen

Beurteilt wurde der Stand 13:15 (`$S/neu5`, Skript sha256 68ad815e…, 5076 Zeilen), verglichen mit dem Stand 11:30 (`$S/neu4`).

Das Paket hat 27 Zeilen:
- 7 behoben: Z135, Z284, Z286, Z302, Z305, Z308, Z341
- 5 teilweise: Z11, Z134, Z210, Z218, Z219
- 13 offen
- 2 schlechter: Z121, Z221

Dazu kommen 10 neue Zeilen, alle mittel. 6 davon stammen aus den Umbauten seit 11:30 (5 × Regel a, 1 × Regel d), 4 bestanden schon vor 11:30. Die Regelstichprobe umfasst 78 Zeilen.

## D1880.pdf – Regel d wirkt richtig, eine neue Folge im Zeitraum
- **«f. Heizamt» ist jetzt in allen drei Serien Hauptabteilung.** ID 72 hat f.I.–IV. und die Teile 2/3 (IDs 73–85). E.IV. ist weg, und E.I.–III. enthalten nur noch Kanzlei-Inhalt. D.III. und G.III. der 3. Serie stehen nach «I.-II. … [leer]» als Teil 3. Damit sind Z284 und Z286 behoben.
- **Abgleich ohne erfundene Signatur:** 194 Signaturzeilen im PDF, minus 41 bekannte a.–i. und 2 Bereichsmarken «I.-II.», ergeben die 151 Einheiten im Excel.
- **Übrige Änderungen:** Die Teil-Nummern (Regel c) sind lückenlos nach Serie vergeben. Die Hauptabteilungen umfassen jetzt die Zeiträume ihrer Teile (Regel b).
- **Neu falsch:** D.III. bekommt 1938–1948 nur aus seinem Teil 3. Dasselbe Muster bestand schon 11:30 bei B.III., B.V., D.IV., E.I., E.II. und F.I.
- **Weiter offen:** Z283 (Serienköpfe im Darin von R., jetzt zusätzlich Hinweis «1930–1936») und Z285 (Schachteln werden nicht weitergegeben, jetzt auch bei f.I.–IV.).

## D3018.pdf – Regel e richtig, Regel a gemischt
- **Regel e:** 02.3.l. ist weg. «Neubau Tonwarenfabrik» steht nur noch bei 02.3.1. (= 1953, Schachtel 4). Damit ist Z302 behoben.
- **Regel a richtig** (die meisten der übrigen 56 Änderungen): 01.1., 01.6., 05.2.1. und 05.7.2. umfassen jetzt alle Daten (Z219 teilweise). Richtig sind auch 02.2.7., 04.2.1. und «undatiert» bei 06.2.1., 06.3. und 06.7.6.
- **Regel a falsch:**
  - 02.3.1.21. und 02.3.1.22. bekommen Plannummern als Jahre (1274–1330 und = 1297). Vorher verhinderte das der Filter für den Bestandszeitraum.
  - 02.3.1.19. reicht jetzt bis 2028 (Z121 schlechter).
  - 06.7.5. hat 1935–1959 statt 03.1935–1960.
- **Regel n:** Sie lässt bei 06.1.4. und 06.6.9. das ganze Datum im Titel (Z221 schlechter).
- **04.1.1.:** 1819–1964 folgt einem wohl falschen Datum im PDF («1819 - 1964»). Das Skript gibt einen Hinweis aus, ich melde es nicht als Fund.

## D3089.pdf – Regel f richtig
- **Regel f:** XI. ist weg. Der Buchtitel «… X. und XI. Jahrbuch …, 1939» steht vollständig in einem Darin-Eintrag von X. Teil 2 (Z305 behoben). Im ganzen Vergleich entfernt Regel f sonst nichts.
- **Regel a besser:** I.2. und I.3.a.–c. (Z135 behoben, Z134 teilweise).
- **Regel a falsch:** X. steht jetzt auf 1837–1956. Grund: Die Textbücherliste von VIII.2. steht weiter bei X. (Z11 teilweise).
- **Schon vor 11:30 falsch und jetzt sichtbar:**
  - Der Schlussvermerk «Bestand geordnet … Caduff» steht im Darin von X. Teil 2.
  - Die Daten 3 und 4 der Bibliotheksberichte stehen in der Anmerkung von X.

## D3253.pdf – Regel g richtig
- **Regel g:** «Unidentifizierter Text ("Tirilin")» ist wieder der letzte Darin-Eintrag von 2. Die Folgezeile «3. Diverses» ist gleich gross. Der Hinweis bei 3. ist weg, «Nicht übernommen» sinkt von 25 auf 24 (Z308 behoben).
- **Weggefallene Zwischenüberschrift-Hinweise in allen Hinweisdateien:** nur drei, alle ohne Folgefehler:
  - D3253 (Regel g);
  - D1880 «f. Heizamt» (Regel d);
  - D3774 «Detailverzeichnis Archivbestand» (Regel t, die Überschrift steht jetzt im Vorspann).
- **Schon vor 11:30 falsch:** 1.1. beginnt mit 25.11.1934 statt 15.10.1934.

## D9983.pdf – Regel h richtig, Regel a mit zwei Rückschritten
- **Regel h:** Die 53 Darin-Einträge stehen wieder bei 5.6., 5. hat nur noch die Übersicht (Z341 behoben). VII.191. III.A. «Weitere Handschriften:» wird weiter zur Gruppe umgeleitet. Sonst zeigt kein PDF einen Darin-Umzug von der Eltern- zur Kindeinheit, der zu Regel h passt; die Umzüge in D3774 gehören zu Regel t.
- **Besser:** 5.5.6. (Regel i) und 5.8.1. (Regel n).
- **Regel a falsch:**
  - 5.6. hat 1834–03.1947 und den Titel «Journale 1834 – 1889» (Tippfehler «März 1947» im PDF).
  - 3.3.4. hat = 1860 statt 1849–1860.

## Wichtigste Punkte
1. **Die Regeln d–h tun, was angekündigt ist, ohne Nebenwirkung in anderen PDFs.**
   - **d** (`findmittel_zu_scope.py` Z. 1403–1412 und 916–920): nur D1880. Andere Strukturänderungen gibt es nur in D3271 und D3774 (Regeln q/t).
   - **e** (Z. 3455–3456): nur D3018 02.3.l.
   - **f** (Z. 1925–1929): nur D3089 XI. Keine andere entfernte Einheit mit römischer Zahl oder Initiale, auch keine Darin-Verschmelzung an «und II.».
   - **g** (Z. 2128–2131): nur D3253.
   - **h** (Z. 2250–2252): nur D9983. Die Umleitung bei VII.191. wirkt unverändert.
2. **Regel a: Die Datumsspalte des Darin wird ohne Prüfung übernommen.**
   - **Ursache** (Z. 3634–3640): Liefert `jahre_im_text` mit Bestandsrahmen nichts oder abweichende Jahre, nimmt Z. 3637–3639 `e.darin_spalte` ungefiltert.
   - **Plannummern als Jahre:** D3018 02.3.1.21. 1274–1330, 02.3.1.22. = 1297, 02.3.1.19. bis 2028 (nach heute).
   - **Bessere Schätzung aus dem Text verdrängt:** D3018 06.7.5. 1935–1959 statt 03.1935–1960; D9983 3.3.4. = 1860 statt 1849–1860.
   - **Vorschlag:** Den Rahmen und «nach heute» auch auf die Datumsspalte anwenden. Weichen die Jahre ab, die Vereinigung nehmen statt der Spalte.
3. **Regel a: Die reinen Jahreszeilen (Z. 2863–2865) zählen zu viel.**
   - Gezählt werden auch Fortsetzungszeilen («– 1860»), Serienköpfe (D1880 R. «… 1930 – 1936») und Tippfehler. Über Z. 3566–3569 erweitern sie sogar einen Titelzeitraum: D9983 5.6. bekommt so 1834–03.1947 mit «Quelle Titel».
   - Nebenbefund ausserhalb des Pakets: D151150 V.F.c.150.:9. hat 1517–1964 wegen der leeren Dossiernummer «1517» (PDF geprüft; die Datei liegt in Paket 5).
4. **Regel a: Das Titeldatum bleibt im Titel (Z. 3566–3569).** Wird der Titelzeitraum durch das Darin erweitert, bleibt das Datum im Titel und die Anmerkung leer.
   - Betroffen: D3018 02.2.1. «… 1898», 03.7.2. «… 1940 - 1952», 04.2.1. «… 1942 - 1964», D9983 5.6.
   - Das widerspricht der Konvention «kein Datum am Titelende» und der Ankündigung «Originalwortlaut bleibt in der Anmerkung».
   - Bitte entscheiden. Als Fund gemeldet ist nur D9983 5.6., weil dort auch der Zeitraum falsch ist.
5. **Regel n (Z. 3578–3579) greift zu weit.** Das Muster trifft auch Bereiche, deren erste Jahreszahl auf «-» endet («ca.1890-1964») oder deren Jahr auf «20. -» endet («1920. - 1963»). Dann bleibt das ganze Datum im Titel (D3018 06.1.4., 06.6.9.).
   - Vorschlag: Die Tageszahl nur ohne Ziffer davor zulassen, also `(?<!\d)\d{1,2}\.\s?[/–-]`, und die blosse Alternative `[/–-]` streichen.
6. **D1880: Serien ohne eigenes Datum bekommen nur den Zeitraum ihrer späteren Teile** (`ergaenze_zeitraeume` Z. 3620–3625).
   - Beispiele: D.III. 1938–1948 (neu), E.I. 1954–1955, F.I. 1945–1953.
   - Die Jahre der eigenen Akten (Hauptabteilung 1931–1936) fehlen, obwohl die Quelle «Untereinheiten» als sicher gilt.
