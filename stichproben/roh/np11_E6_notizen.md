# E6 – Notizen (Nachprüfung 11, erste Prüfung, Stand efe92c5f)

## Bilanz
- 44 Dateien, 895 Einheiten: 40 ohne kritischen Fehler, 4 kritisch (D2733, D3503, D3343, D403), je 1 kritischer Fund.
- Funde in `E6_funde.csv`: 4 kritisch, 20 mittel, 1 gering. Urteile für alle 44 Dateien in `E6_dateien_urteil.csv`.
- Prüfumfang:
  - Jede Prüfmappe ganz gelesen; Dateien über 60 Einheiten (D2104, D1389, D2040, D3512) alle Seiten Zeile für Zeile.
  - Jedes Warnzeichen nachgesehen; [VOR]/[NACH] zusätzlich per Skript gegen die Einheit in PDF-Reihenfolge (`tmp_E6/vorcheck.py`).
  - Darin aller Dateien nach Signaturformen durchsucht (`tmp_E6/darinscan.py`).
- Suchlauf nach den Hinweisen des Koordinators:
  - durchlaufende Nummern über Schachteln, Signaturspalte mit blossem Bestand: in E6 kein Fall, ausser den Fremdbeständen der
    D2733-Verweise (= Fund 1);
  - D2733 (Positionen je Schachtel) und D1389 3. (Unterpunkte) sind wie gemeldet kein Fehler.

## Kritische Funde
1. **D2733 V.L.71.:3:** Der Block «Verweise auf andere Bestände» (S. 2, 14 pt; V.E. c.48. Nr. 7, V.F. c.19. Nr. 54, V.G. c.70. Nr. 10)
   steht im Darin der letzten Schachtel, daher auch der Zeitraum 1893–1933. Regel 4/34 erkennen nur «Anhang».
2. **D3503 VII.312.:4.5.:** Der Absatz zur Vereinsgeschichte nach der letzten Einheit («1928 wurde der Verein … gegründet …») steht im
   Darin von 4.5. Der Schlussblock beginnt erst auf S. 3. Gegenstück: D3437 «Der Verein Pro Vorderberg bestand …» steht richtig im Info.
3. **D3343 VII.266.:2. Teil 2:** Die zweite Nennung «2. … (alphabetisch nach Autor)» ist dieselbe Liste anders sortiert (117 von 117
   Einträgen gleich). Daraus entsteht eine erfundene Einheit mit doppeltem Darin. Formal greift die Teil-Regel → evtl. Entscheid Nutzer.
4. **D403:** «a) Gebühren, Formelles» und «b) Informationen betreffend Bürgerrecht» stehen unter der einzigen Nummer «V.B. c.12.:1
   Allgemeines». In der Excel hängen sie als V.B.c.27.:a./:b. auf E1 am Bestand; Soll: 1.a/1.b unter 1.
   Dazu mittel: Signatur V.B.c.12.:1 nicht zu V.B.c.27.:1 berichtigt.

## Muster der mittleren Funde
- **Zeitspalte im Titel:** zweizeilige Titel (D1578, D1608 «Ingenieurabtei- 1883 lung»); Bandzusatz «1913 (I)», «1990 I», «1969 I»
  (D1593, D2104, D2040). Gleicher Aufbau ohne Zusatz geht (D1582, D1692).
- **Tabellenspalte nicht erkannt:** Schachtel bei D176186 und D1220 («… 1990 – 1993 452 …»), Stückzahl bei D2268.
- **Schachtel nicht an Geschwister weitergegeben:** D3606 («Schachtel 1» bei 1. gilt bis 5.).
- **Zeitraum:** Lebensdaten in der Personenüberschrift (D3512), Gesuchnummern als Jahr «1901» (D1220), Amtszeit «[1914-1918]»
  (D2704), Enddatum mit Tippfehler (D2721).
- **Titel:** Folgezeile im Darin (D2268 4./6., D174277 2.), Zwischenzeile im Titel (D174277 6.), Elterntitel statt «Plakat: …»
  (D3437 5.3.), Gruppenzeilen am falschen Eintrag (D1389 29.).

## Unsicherheiten
- D403: Die Lesart «a)/b) unter 1» stützt sich nur auf die Anordnung im Scan (eine Nummer, a)/b) in derselben Spalte darunter); keine
  Gegenprobe in scope.
- D3343: Nach der Schwere-Regel «Einheit erfunden» kritisch, obwohl die Teil-Konvention formal erfüllt ist.
- Nach Konvention nicht gemeldet: Einleitungen vor dem Detailverzeichnis (D3606, D2566, D2704), Jahresüberschrift D840.
