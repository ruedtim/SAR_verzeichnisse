# A3 – Nachprüfung 10 (Runde 8: Signaturerkennung und Zeiträume)
Urteile: 23 Zeilen, 1413 Einheiten des diff, alle «besser». Altzeilen: 6 behoben (B40, B41, B42/K9, B43/K10, B44,
B47/K11), B46 offen, B45 ungeprüft (Einheit unverändert). Neue Funde: 8 kritisch, 9 mittel, 3 gering.
## D3470 (Regel 21, Erstprüfung, 1942 Einheiten, 80 S.)
- Struktur ganz per Skript (tmp_A3/struktur.py, inhalt.py, zeitraum.py): 1950 Signaturzeilen (x 74) in
  Reihenfolge = 1924 Einheiten + 18 Teile, 1:1 bis auf 8 Zeilen. Je Block alle PDF-Wörter in Titel/Darin, sonst keine
  fremden Wörter; Schachtel = rechte Spalte (ausser 1938.582); Zeitraum = Signaturjahr 1379 / Datumsspalte 98 /
  leer 462; kein Eintrag über einen Seitenwechsel. Einheit für Einheit: S. 1, 12, 23, 40, 56, 71, 80.
  Vollständigkeit (21 Vorspannzeilen S. 1) und 3 Schlussvermerke S. 80 im Info richtig.
- Die 8 Zeilen = 8 kritische Funde «Einheit im Darin». Soll: je eigene E1-Einheit.
  - 12.53a «Vaujours Gipsfabrik» Sch 11 (vor Runde 8).
  - 1937.524a/b Sch 44, 1938.583a/b Sch 47/48 (Buchstabenzusatz, Regel 21).
  - 1953.1419 Sch 121, 1954.1514 Sch 126, 1961.1813 Sch 158: nur Signatur + Schachtel → «[ohne Titel]».
  - Folgen: 1938.582 Sch «47-48» statt 47; 5 Einheiten Zeitraum «Darin (geschätzt)».
- 45.0. (S. 22): nur die eigene Zeile, Dossier, Sch 35. Leerer Zeitraum richtig, 45 ist kein Jahr («39.416
  Feuerthalen» = «1933.416 Feuerthalen»; «44.448 Altenrhein» hat 1935).
- Zweistellige «42.446»: flache Liste ohne Köpfe «14.» usw. → E1, Eltern leer richtig, Hinweis nur Rauschen.
  11.43.a., 11.44.a., 13.92.a.–8. als E2 vertretbar (13.92 «Diverse Arbeiten» ist ein Sammelkopf).
- Mittel durch Regel 21: 1861.1845/1846 Zeitraum 1861 (Tippfehler für 1961); 1961.1823 «Expo 1964» → Titel
  «Expo», Zeitraum 1964 statt 1961.
- Mittel vor Runde 8: Datum mitten im Titel (12); Ortsumbruch im Titel (13, davon 10 neue Einheiten); 13.82.
  Zeitraum 11.02.2026 aus «(nicht vorhanden: …)». Gering: Signaturform uneinheitlich.
## Übrige Dateien
- D1924 (Regel 22): bestätigt. «Winkler, D. 1879 101» steht im Darin von 10 an der PDF-Stelle, mit Hinweis.
  Signal Z (82 «ohne Zeilenanfang») = Rauschen («Schachtel n», Findmittel ohne Signaturen). Schachtelspalte ganz
  geprüft (Zeilen je Schachtel = PDF; «80a & 80b», «33-34», «79a» echt). Gering: in 81 zwei Zeilen verbunden.
- D3566 (Regel 19): :S./:S.3. weg, 3. E1, Nummer 12 + S. Vögelin im Darin von 2., «max / 28. März 2000» im Info,
  3. = 02.12.1829–28.03.1832. Weiter falsch: 1. 1519–1953, 2. 1336–1962.
- D3727 (Regel 20): K11 behoben; Wortfolge S. 11–69 = Darin 10.3. T1+T2; «3 Fotos» Stückzahl im Darin, Umfang leer.
  Mittel vor Runde 8: 3. 10.10.2005 aus der Chronologie S. 4 «3. – 10. Oktober 2005» (Soll 1940–1981, Zeile in
  keinem Feld); Titel 5.1. mit «Enthält …»; Darin 10.5. mit Schlussnotiz «Das Planarchiv …».
- D3313 (Regel 25): 1. 1834–1863, 2. 1854, 3. 1885–1887, 4. 1858–1895 (Inhalt von 4. reicht 1838–1898).
- D1180 1. 1919–1935 besser; «(JJJJ – JJJJ)» ohne Namensjahr gibt weiter keinen Zeitraum: 16 Einheiten + Folgefehler
  2., 5., 8., 12., 14. (mittel, vor Runde 8).
- D2620 11.2. 1969–1977 besser; neuer Hinweis «weicht vom Inhaltsverzeichnis ab (1977)» unbegründet (gering).
## Unsicherheiten
- Zeilen nur mit Signatur + Schachtel werte ich als Einheiten «[ohne Titel]» (kassierte Nummern fehlen ganz).
- Weitere PDF-Ausreisser, nicht gemeldet: 1947.744 zwischen 1942.743/745, 1956.1936–1938 vor 1957.1640.
- sigliste.py sieht die D3470-Fälle nicht (Nummernmuster ohne 4-stellige Gruppe und ohne «12.53a»).
