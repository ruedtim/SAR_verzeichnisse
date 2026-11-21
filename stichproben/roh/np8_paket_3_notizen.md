# Paket 3 – Nachprüfung 8 (D140969, D152817, D2737, D2745, D2687)

## Bilanz je Datei
- **D140969** (86 → 93): 92 Einheiten aus dem Vergleich (7 NEU, 85 GEÄ) in 19 Urteilszeilen, alle besser (Regel 10).
  - Die 7 Bereiche stehen so im PDF (S. 1, 2, 4, 5, 13, 13, 15), keiner ist erfunden. Jede Nummer hängt am engsten Bereich: 57-58 (12 pt statt 13,9 pt) liegt in 50-58, 58. auf E3. Die Signaturspalte ist mit dem PDF abgeglichen.
  - Die Zeiträume der Gruppen stimmen: 1-12 1936–1942 aus den Kindern, 13-34 1925–1940 aus dem Titel, 57-58 aus 58., 50-58 geschätzt 1915–2010; 35-49 und 59-81 haben keine Daten.
  - Die Gliederungszeilen sind aus Darin und Umfang von 12./34./49./56./58./81. vollständig umgezogen. «1 – 12 …» war vorher gar nicht importiert.
  - Neue Funde: 2 kritisch (vor Runde 7), 1 mittel (Regel 10).
- **D152817** (704 = 704): 38 GEÄ in 9 Zeilen, 36 besser, 2 gleich. 29 davon liegen in 7-19, 7 in 8-12, 2 haben nur einen neuen Hinweis.
  - 8-11 liegt jetzt in 8-12, mit den Schachteln 8–11. 7-15, 16-17 und 18-19 liegen jetzt in 7-19, mit ihren Schachteln, genau wie S. 33.
  - Alle 704 Signaturzeilen des PDF stehen genau einmal in der Excel.
  - Neue Funde: 1 kritisch (vor Runde 7), 2 gering (Reihenfolge).
- **D2737** (5 → 8): 7 besser (Regel 9). 3/4, 7/8 und 10/11 sind eigene Einheiten. «11. 2. 1987 / Hb» bleibt Schlussvermerk. 9. hat 1914–1987 (Fallset B), 6. jetzt 1942 ff. Keine neuen Funde.
- **D2745** (2 = 2): 3 besser (Regel 8). «7 Einladungen …» steht im Darin von 1., «2. Drucksachen» ist eigene Einheit. Keine neuen Funde.
- **D2687** (2 = 2): 3 besser (Regel 8). «3 Auszüge …» steht im Darin von 1., «2. Zeitungsausschnitte» ist eigene Einheit. 1 neuer Fund mittel (Beginn des Zeitraums).
- **Prüfwerkzeuge:** textverlust2 findet keinen Textverlust, nur Zählerstände im Info-Blatt («5», «10»). gliederung.py meldet im neuen Stand nur D2737 L1 «4. fehlt (vor 5.)», ein Artefakt von 3/4; vorher D140969 L1, D2745 L2, D2687 L1, D2737 L1.
- **Gesamt:** 143 Einheiten, 141 besser, 2 gleich, 0 schlechter. Runde 7 hat in diesen fünf Dateien keine Regression erzeugt.

## Wichtigste Funde
1. **D152817, kritisch, vor Runde 7:** Läuft ein Abschnitt über zwei Schachteln, wird er Eltern der Übersichts-Schachteln. Betroffen sind 5.:1-2 «f) Arbeitslosenfürsorge», 6.:4-5, 7.:1-2, 7.:2-3 und 7.:5-6.
   - Dadurch hängen a)–e) und g) unter f), «b) Hochbau» unter «c) Baupolizei» usw.: 5 Bereiche, 10 fremde Abschnitte.
   - Neu in Runde 7 ist nur der passende Hinweis bei 5.:1-2 und 7.:1-2.
2. **D140969, kritisch, vor Runde 7:** Drei Einheiten fehlen, ihr Text steht bei Nachbarn.
   - 50a (S. 6) steht im Darin von 50.; 50. reicht deshalb bis 2010.
   - 88 «Pläne» und 89 «Filmrollen» (S. 16–17): «88 Pläne» ist der Umfang von 87., der Rest steht im Darin von 87.
3. **D140969, mittel, Regel 10:** 87. steht neben 82-86, weil der Detailkopf «82 – 86» sagt. Die Übersicht S. 1 sagt «82 – 87».
4. **D2687, mittel:** 2. beginnt am 23.10.1927 statt am 19.10.1927. Das Datum ist umbrochen («19.» / «Oktober 1927»).
5. **D152817, gering:** Unter 8-12 steht Schachtel 12 jetzt vor 8-11 (Regel 10). 5.:3, 6.:13 und 7.:4 standen schon vorher vor ihren Nachbarbereichen; 6.:13 hat dazu den falschen Hinweis «nach 3 folgt 13».

## Altzeilen
- A9 (D140969 3:1-3/8:1-3/11:1-2 und Gliederungszeilen) behoben. A11 (D2737 3/4, 7/8, 10/11) behoben. A10 (14./17. nur Enddatum) teilweise. A8 (Titel 36a. ff. mit zweiter Zeile) offen.

## Unsicherheiten
- **D152817 6.:8 Teil 2 «Allgemeine Verwaltung» und 6.:11 Teil 2 «Gasversorgung»:** Beide hängen über ihre Schachteln jetzt unter «Wasserversorgung»; im PDF stehen sie daneben. Die Übersicht deckt das («e.1 (Wasserversorgung)», «e.4 (Wasser- und Gasversorgung)»), daher «gleich» und kein Fund.
- **Schwere bei D152817:** «kritisch» folgt der Definition (ganze Abschnitte falsch eingehängt). Es ist eine Grenze der Schachtel-Konvention, keine Regression.
- **D140969 57:** Das Detail hat keine Zeile «57», nur den Bereich «57 – 58» und die Übersichtszeile «57 Zeitungsausschnitte (1)». Dass es keine Einheit 57 gibt, ist nicht als Verlust gezählt.
- **Umfang in Klammern:** Er bleibt im Titel der Bereiche («(16 Bände in 4 Schachteln)», «(27 Schachteln)», «(2 Schachteln)»). Das ist ein bekannter offener Punkt und nicht gemeldet.
- **Kleinere Punkte:** Bei D2687 ist der Mechanismus des falschen Beginns nur vermutet. D2745 1. «von 1891» stammt aus einer alten Darin-Schätzung («Abgeordnetenversammlung von 1891/92», Eintrag undatiert) und ist nicht gemeldet.
