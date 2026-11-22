# S1 – Sichtung «leere Teile» (NP16, Stand Runde 13)

## Bilanz
- 148 Kandidaten (alle LEER, kein KOPF) in 9 Dateien: **145 kein Fund, 3 Funde** – 1 kritisch (D3099), 2 mittel (D149628). Keine Zeile aus `bekannt.csv` betroffen.
- Kein Kandidat ist ein Kopf, eine Überschrift oder eine Übersichtszeile. Bei keinem steht sein Inhalt bei einer anderen Einheit, und nirgends fehlt Text.
- Methode: Prüfmappe r13 und Zeilen-Cache. Für alle 148 habe ich Titel + Darin gegen die PDF-Zeilen abgeglichen: Signaturzeile ohne Nummer und Datumsspalte, dazu die eingerückten Folgezeilen bis zur nächsten Signaturzeile (`tmp_S1/vergleich.py`). 146 stimmen wörtlich. Bei 2 (D1880 B.V., D.III.) weicht nur der Trennstrich ab; von Hand geprüft.
- D149628 (118): 18 genau (Mappe, Cache, Nachbarzeilen), der Rest als Sammelurteil nach Muster. D1880 (15): alle genau an den PDF-Zeilen S. 12–19. Die übrigen 15 einzeln.

## Muster der Kandidaten (alle «kein Fund»)
- **D149628:** Listen, in denen jedes Stück die Signatur wiederholt: 27.1.4. (4), 27.1.5. (35), 30.2.2. (77). Jede Zeile ist ein Plakat oder Aushangbild mit «undatiert» (steht in «Entstehungszeitraum, Anm.»). Echte Stücke mit nur Titel.
- **D1880:** Positionen der 2. und 3. Serie. Jede Serie hat ein eigenes Detailverzeichnis nach demselben Registraturplan; leere Positionen tragen dort «[leer]». Diese Positionen haben weder «[leer]» noch eine «- …»-Zeile, sind also Akten mit nur einem Titel. Sie stehen als Teil unter der Position der 1. Serie (Konvention).
- **Doppelte Nummer hintereinander, Nachbarnummern vorhanden** (Hinweis «Tippfehler?»): D2857 1.2.2., 1.2.4., 1.2.17. (je das einzige Blatt des Projekts), D3186 10. (Inhaltsdossier unter dem fetten Kopf «10.»), D847 30, 271. Nach Konvention kein Fund.
- **Einzelstücke:**
  - D141020 1.24. (I) (Partitur);
  - D151210 2.3.2.7. «Zeitungsartikel …», 13.5. «Plakat ohne Text», 3.3.3.2./10./21. «…, Teil 2» (Teil 1 wird mit `spalte_teil1_ab` bewusst abgespalten);
  - D3589 11 (der Eintrag bricht schon im PDF bei «von 19» ab);
  - D847 2c (zweites «2c» nach 2d, Tippfehler im PDF, wohl 2e; nicht hintereinander, also Teil nach Grundregel).

## Funde
- **S1-1 kritisch, D3099 1.2.5. Teil 2 «6. Generation: Hansjürg Diener».**
  - Die beiden 1.2.5. sind Geschwister (Reihe 1.2.1.–1.2.5., parallel zu 2.1.1.–2.1.6.). 1.2.6. fehlt in der ganzen Datei.
  - Nach der Konvention müsste die zweite Nennung 1.2.6. werden (E3 unter 1.2.). Sie hängt aber als Teil (E4) unter 1.2.5., und 1.2.5. wird dadurch «Serie».
  - Ursache vor Runde 13: Der Teil ist bewusst so gebaut; der Skriptkommentar nennt VII.199. als Beispiel. `korrigiere_doppelnummern` setzt die fehlende Nummer nur bei einstufigen Nummern und Jahr.Laufnummern mit Lücke (n, n, n+2).
- **S1-2 und S1-3 mittel, D149628 23.2.1. «Y» und 23.5.2. «K».** Die einzige Inhaltszeile («Doris Young», «Die Kaiserin») folgt mit Absatzabstand (17,8 pt), steht aber im Titel statt im Darin. Runde 12 war gleich. Ein Suchlauf über die ganze Datei (`tmp_S1/einzeiler.py`) findet nur diese zwei; Titelfortsetzungen liegen dort bei 13,4–15,9 pt.

## Zusatz-Suchlauf über alle 715 Dateien (`tmp_S1/doppel_nachbar.py`)
- Gesucht: Teile mit dem Hinweis «zweimal hintereinander», bei denen die nächste oder vorige Nummer fehlt. Ergebnis: 4 Fälle.
  - D3099 1.2.5. (= S1-1);
  - D2979 1.8. «Hülfsverein Wiedikon» / «Jahresrechnungen, Nr. 2 (Band)»: Kopf und Inhalt, der Teil ist richtig;
  - D151150 9.1386. (die Nummern haben dort ohnehin Lücken; nicht geprüft);
  - D3470 1956.1585 (Jahr.Laufnummer, ausgenommen durch Regel 3 der Runde 11).
- Eine reine Zahlenregel am Gruppenende würde D2979 falsch machen. Für D3099 spricht nur die Geschwisterreihe im Titel («5./6. Generation»).

## Beobachtungen ohne Meldung, Unsicherheiten
- D1880: Den Teilen der 2. und 3. Serie fehlt die Schachtel, obwohl sie zwischen zwei Schachtelangaben stehen (z. B. A.IV. T2 in Sch. 45). Bekannt seit NP10 (mittel).
- D1880: Die Serienköpfe sind Teile ohne Kinder (z. B. A. T2 «Allgemeines», Sch. 45-46). Das folgt aus der Teil-Konvention. Der Suchlauf meldet sie nicht als KOPF, wegen der 80-%-Regel.
- D149628: «23.2.1. Z» (S. 500 y650) mit den «Fotografien (19. Jh.)» wird ein eigener Teil 29 mit gebildetem Titel. Das PDF setzt nur hier die Signatur, sonst steht der Buchstabe allein. Nicht gemeldet.
- Unsicher ist nur S1-1: Gilt «Nachbarnummer fehlt» auch am Gruppenende? Das muss die Hauptsession entscheiden. Bis dahin werte ich es nach dem Wortlaut der Konvention als kritisch.
- Rauschen der Prüfmappe: Bei kurzen Folgezeilen («Brecht», «Bruggmann», «Auber», «Die Kaiserin») steht «→ ID n Titel [NACH]». Am Excel geprüft: Der Text steht jeweils im Titel des Kandidaten.
