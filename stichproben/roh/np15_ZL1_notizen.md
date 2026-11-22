# ZL1 – D150829 (VII.231., Werner Müller, 518 E.) und D3170 (VII.209., Theater am Neumarkt, 385 E.), Stand Runde 12

## Bilanz
- Beide Dateien **ohne kritischen Fehler**. Keine Einheit fehlt, keine ist erfunden, Eltern und Ebenen stimmen, kein Text fehlt,
  kein Inhalt steht bei einer fremden Einheit, es gibt kein Stück ohne Nummer, die Schlussvermerke stehen im Blatt Info.
- 9 mittlere und 3 geringe Funde (ZL1-01 bis ZL1-12), alle schon vor Runde 12 da. Runde 12 ändert keine der beiden Dateien.
  `bekannt.csv` enthält keine Zeile zu diesen Dateien.

## Vorgehen (Hilfsdateien in tmp_ZL1/)
- Beide Kompaktmappen ganz gelesen. Jede EINHEIT-Zeile, jedes Warnzeichen und jedes «?» einzeln geprüft: am Excel-Dump
  (`dump.py`, alle Felder ungekürzt), an der vollen Prüfmappe und, wo nötig, am PDF.
- `sigfolge.py`: alle Signaturzeilen des Zeilen-Caches gegen die Einheiten, nach Seite und «Nr. im PDF», in Folge.
  D150829: 518 = 518, übrig bleiben nur Mengenzeilen («6 Pläne …») und der Datumsrest «1961». D3170: 382 Einheiten und
  3 Teile, übrig bleiben die Übersicht S. 1–2 und die Darin-Titel «1 Polarabend» und «6. Heidelberger Stückemarkt».
- `luecken.py` (Eltern als Präfix, Ebene, Lücken, Doppelte): D150829 ohne Abweichung. D3170: 7.2.1.a.–f. mit Hinweis unter
  7.2. (7.2.1. fehlt im PDF), dazu 6.3.0. und die Teile 2.1./2.4./2.5.
- Strukturbericht: D150829 leer; die 13 Markierungen in D3170 einzeln geprüft, keine ist ein Fund.

## Wichtigste Funde (mittel)
1. **ZL1-01**, D150829 5.1. Seepark: Zeitraum 1899–2000 statt 1956–1990. Die Datumsspalte steht auf der ersten
   Beschreibungszeile und landet am Ende von Darin 1; die Schätzung nimmt «Zürich 1899» (Broschüre) und «2000 Autos».
   Folgefehler: 5. Projekte. Kein Werktitel-Fall, denn die Datumsspalte ist da.
2. Titel am Gedankenstrich abgebrochen, Rest im Darin: ZL1-04 (1.6., dazu «1964 + 1984» mitten im Titel), ZL1-07 (5.5.18.),
   ZL1-08 (6.3.), ZL1-09 (D3170 4.2.1.6.). Das bekannte D2620 1.14. hat dasselbe Muster, die Stellen hier sind neu.
3. ZL1-02/03 «vom 15. und 31. Juli 1980», «vom 7. und 14. April 1972»: Das letzte Datum fehlt, der Titel endet auf «… und»,
   der Zeitraum nennt nur den zweiten Tag.
4. ZL1-05/06: Titel am Doppelpunkt geteilt (4.1.79., 4.2.117.).

## Ohne Fund
- D3170 2.1./2.4./2.5.: Fette Gruppenzeile und Eintrag tragen dieselbe Nummer → Serie mit Teil 2 (Konvention «wiederholte
  Signatur»), ohne Hinweis; ein Tippfehler ist es nicht. 7.2.1.d. hat «(2 Schachteln)» zweimal, so steht es im PDF.
- D3170 6.4. Plakate ist eine Einheit mit 233 Darin-Zeilen; die Überschriften «Spielzeit …» haben keine Nummer.
- [VOR] (D150829: 20, D3170: 28) kommt von wortgleichen Zeilen («[im Dossier „Seepark, 5.1.“]», «Hope and Glory», «Polly»,
  «(2 Schachteln)»); jede dieser Zeilen steht bei ihrer eigenen Einheit.
- Bekannt, nicht neu gemeldet (Zeiträume aus Werktiteln oder Lebensdaten), alle D150829: 4.1.62. 1991 statt 02.10.1982;
  4.1.75. bis 2000, darum auch 4.1. und 4. bis 2000; 5.6.30. 1992, im PDF «o.D.»; 6.3. 1877.

## Unsicherheiten
- Ursache von ZL1-06 unklar: Andere Titel mit «:» mitten in der Zeile bleiben ganz.
- ZL1-11/12 sind Sammelzeilen; nicht jeder Listenumbruch in den Zweispalten-Programmen 6.3.x ist einzeln aufgeführt.
