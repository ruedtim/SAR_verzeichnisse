# R1 – vorher verdeckte Zeilen (NP12, Stand 66c0fb74)

## Bilanz
- 41 Dateien, 2'360 vorher verdeckte Zeilen. 2'087 davon sind im Auszug markiert, 273 sind in der korrigierten Mappe weiter verdichtet. Alle 2'360 habe ich am Zeilen-Cache gegen die Excel geprüft.
- **Alle 41 Dateien sind ohne kritischen Fehler, es gibt 0 kritische Funde.** Dazu 5 mittlere Funde (D1220 zweimal, D1584, D3945, D174277) und 2 geringe (D3363, D109662).
- Wo der Text steht: 1'322 in der Einheit des eigenen PDF-Abschnitts; 384 sind selbst Signaturzeilen; 98 in Teilen oder Bestandszeilen ohne Startzeile; 503 in der Bestandszeile von Findmitteln ohne Signaturen (D3087, D167, D2655, D2757, D3412); 17 ohne Datum, weil es in von/bis steht; 9 im Blatt Info.
- 27 nicht wiedergefunden: 15 Köpfe «Schachtel n» in D109666 (Nummer als Schachtel-Nr. der Teile T2–T20), 2 Signaturzeilen ohne Titel in D3470 (1954.1514, 1961.1813; die Einheiten gibt es), 10 Trennlinien in D3512.

## Methode (Skripte in tmp_R1/)
- `r1_pruef.py` findet die verdeckten Zeilen wie `verdeckt.py` und sucht ihren Text mit Ziffern in der Einheit ihres PDF-Abschnitts. Die Mappe ordnet nach ziffernlosem Text der nächsten Einheit zu; die [VOR]-Zeichen im Auszug sind darum fast alle Rauschen.
- `r1_zaehl.py` zählt je Einheit gleichlautende Zeilen im PDF und in der Excel. `r1_grenze.py` prüft die letzte Zeile vor jeder Signaturzeile. `r1_einheit.py` prüft Ebene, Eltern und Jahr der Signaturzeilen.
- Signaturen PDF ↔ Excel abgeglichen in D140947 (123/123), D1481 (70/70), D1706 (108/108), D1584, D2139, D3894, D3896, D3945, D3698 und D174277. Behälter- und Signaturformen einzeln angesehen.

## Ergebnis nach Art der Zeile
- **Signaturzeilen** (D140947, D1481, D1706, D3470, D3520, D150306, D174277, D1757, D109662, D2828, D4024): alle Einheiten da, Eltern, Ebene und Jahr stimmen. Keine verdeckte Signaturzeile ist im Darin gelandet.
- **Behälter:** «Schachtel n» ist in D109666 Schachtel-Nr. der Teile (Sch. 1–23 einzeln geprüft), in D4024 eigene Einheit. «n Band/Bände» und «n Schachtel(n)» stehen im Umfang. Keine Mappen-, Band- oder Schachtelzeile bräuchte eine eigene Einheit oder eine andere Zuordnung.
- **Inhaltszeilen** (Format, Alte Signatur, Siegel, Fotos/Diverses, Expl., Revers, (fehlt), Datums- und Anzahlzeilen) stehen in der richtigen Einheit.
- **Querverweise** wie «(Siehe auch: 4.2.2.6. Fotos.)», «[im Dossier „Seepark, 5.1.“]», «Petschaft X.D. n.» sind keine Einheiten und stehen bei der verweisenden Einheit (D3894: alle 59 Verweise wie im PDF).

## Wichtigste Funde (mittel)
1. **D1220 1.2.:** Zeitraum 1901 aus der Gesuchnummern-Tabelle («1901 – 2098 305»), auf 1. vererbt; Schachtel-Nr. 295-450 fehlt.
2. **D1584:** In 8 Einheiten steht «Hochbauamt» am Titelende statt im Darin wie die Architektenzeilen.
3. **D3945:** Der Tabellenkopf «Signatur Beschreibung Format» steht im Titel von X.H.13. und im Darin von X.H.28.; dem Titel von 28. fehlt dadurch «Mauerkrone».
4. **D174277 :6:** Der Unterkopf «Fotos» steht im Titel (diese Zeile war selbst nicht verdeckt).

## Bekannt, nicht neu
- **D2828:** «Pg» und «Format: …» gehören zu den Regesten I.A. 4862.–4865. des Anhangs im Blatt Info. Das ist das Mindest-Soll von K15; die Verteilung nach «in 17.6.»/«in 18.» ist laut NP11 mittel und offen.
- **D2139 39.:** Die letzte Titelzeile «Zürich» steht im Darin (NP11, mittel). **D446, D150306:** Umfang in Klammern nicht erkannt (bekannt offen).

## Unsicherheiten
- Kurze Zeilen wie «(5)», «1926» oder «Fotos» lassen sich am Text allein schlecht zuordnen. Geprüft über Zählprobe, Grenzzeilen und Stichproben; eine Verwechslung über eine Einheitengrenze fand ich nicht.
- **D3412** (nicht verdeckte Zeilen): «Nummer ¦ Bauherr/Bauprojekt/Adresse ¦ Jahr» mit «Nr. 15 …» steht als Bestandszeile. Lücken, «29A», zweimal «Nr. 204», «Nr. K.V.» und «Nr. -» sprechen für Projektnummern des Architekten (NP11: gering). Führt das Archiv sie als Signaturen, wäre das Muster 7 (vgl. Regel 12).
- **D3087 Bestandszeile:** Tabellenkopf «Zeit Autor Stück Ort» am Titelende (gering, nicht verdeckt).
