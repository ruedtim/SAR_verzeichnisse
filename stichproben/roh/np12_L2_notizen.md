# L2 – Notizen (Nachprüfung 12, grosse Dateien)

## Bilanz
- 14 Dateien, 11'379 Einheiten: **9 ohne kritischen Fehler**, **5 mit kritischem Fehler** (D4054, D10585, D3472, D175996, D151150).
- `L2_funde.csv`: 26 Zeilen (8 kritisch, 15 mittel, 3 gering), alle neu, Ursache jeweils vor Runde 9.
- Nicht neu gemeldet (bekannt, offen): D3472 1952.8/1952.14 Teil 2, D10675 712-Überschriften, D152817 D.7.:11 «1013/14»,
  D845 1.2 Zeitraum, D10585 Titel «…, in».

## Vorgehen
- Skripte in `tmp_L2/`: `abgleich2.py` (Zeilen-Cache ↔ Excel für alle Einheiten: jede Signaturzeile = Einheit/Teil, Text jeder
  PDF-Zeile bei der laufenden Einheit, Überschriften-Kandidaten), `sandwich.py` (Einheit zwischen Geschwistern eines anderen
  Zweigs bzw. vor ihren Eltern), `jahrlauf.py` (Jahr/Laufnummer-, Schachtel-, Teil-Folge), `schluss.py` (Text nach der letzten Einheit).
- Strukturberichte ganz; Kompaktmappen (neu) gefiltert (EINHEIT, Warnzeichen, nicht importiert, fett, erste/letzte zwei Seiten); je Datei
  ≥ 5 Seiten volle Mappe/PDF. Die verdeckten Zeilen der alten Mappen betreffen den Cache-Abgleich nicht; Vergleich alt ↔ neu ohne neuen Fund.

## Wichtigste Funde (kritisch)
1. **D4054, Tippfehler in der Signatur:** «10.8.2.10. Michel Plasson» (zwischen 10.3.2.9. und 10.3.2.11.) und «10.8.4. F» (mitten in
   den Teilen der Saison 1981/82 von 10.3.4.) hängen unter 10.8. «Pressekonferenzen», mit den Hinweisen «Übergeordnete Signatur
   fehlt» bzw. «beginnt bei 4».
2. **D4054 S. 152:** Der Bestandsumfang nach «Der Bestand umfasst:» (7 Zeilen lfm) steht im Darin von 21.5.3.; die Überschrift im Blatt Info.
3. **D10585:** «7. 2.3.» (Leerzeichen) steht als Darin-Zeile in 7.2.2.; die kursiven Ortsüberschriften Zug, Olten, Graubünden,
   Thurgau und Freiburg i. Br. stehen im Darin der vorigen Einheit.
4. **D3472 1966.19:** Aus der Aufzählung a)/b)/c) in der Textspalte werden drei Unterstufen; die Eltern werden Teilbestand.
5. **D175996:** IV.B.1.a), 460.a), 460.b) sind eingeschobene eigene Rechnungen, hängen aber als Kinder unter 1. bzw. 460.
6. **D151150 9. «nummerierte Dossiers»:** 293 Dossiers mit Nummer in der Signaturspalte und eigener Schachtel nur im Darin (Muster 8).

## Muster
- Tippfehler in Dezimalsignaturen («10.8.» statt «10.3.») → Kind einer fremden Gruppe; erkennbar an «Übergeordnete Signatur fehlt» /
  «Nummerierung beginnt bei n» mitten in einer anderen Reihe – Suchlauf über alle Dateien lohnt sich.
- Eine Schlussüberschrift wird erkannt, ihre Folgezeilen nicht. Kursive Zwischenüberschriften in der Textspalte landen im Darin der vorigen Einheit.
- Elterntitel statt eigenem Titel («Kein eigener Titel»): D149888 (23 Einheiten), D3793 5.3.21.
- Zeitraum aus Jubiläumsjahren («1291 – 1891», «1755 – 1955»), aus Bibliothekssignaturen «(Bb 1686)», aus «vor 1933» und
  «seit 1939 s. …» sowie «(bis 1985)» als «Genau 1985».

## Unsicherheiten
- **D151150 9.:** Konventionsfrage. NP5/NP6 haben das Darin hingenommen (dort ging es nur um den Zeitraum); nach Muster 8 und
  Regel 14 wären die Nummern Signaturen.
- **D175996:** Falls «n.a) = Kind» gewollt ist (Regel 25 betrifft nur gleichen Titel), nur mittel; die Stufe Teilbestand bleibt falsch.
- **D3472 1966.19:** Gelten a)–c) als echte Unterdossiers, bleibt nur die falsche Stufe Teilbestand (mittel).
- Teile mit anderem Objekt unter derselben Nummer (D3482, D3466, D149888 14.20.) habe ich nach Konvention nicht kritisch gewertet.
