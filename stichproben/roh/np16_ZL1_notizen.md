# ZL1 – NP16, Zufallsstichprobe 4: D3482 (Firmenarchiv Locher, Hochbau und Eisenbeton, Akten, VII.308.C.a.)

## Bilanz
- 1 Datei, 1929 Einheiten, ganz geprüft. **Ohne kritischen Fehler.** Neu: 0 kritisch, 4 mittel (ZL1-01, -02, -03, -05), 3 gering.
- In `bekannt.csv` steht nichts zu D3482. Die früheren Gesamtscan-Funde (Schachtel ≥ 1000 als Jahr; Teile mit fremdem Titel)
  bleiben behoben: alle 1929 Schachteln stimmen, jeder Teil hat seinen eigenen Text.

## Vorgehen
- Skript `tmp_ZL1/vergleich.py`: alle 1929 Signaturzeilen des Zeilencaches gegen die Excel, nach Signatur und n-tem Vorkommen.
  - Geprüft: Teil, Eltern, Ebene, Stufe, Schachtel, Seite, Nr. im PDF, Zeitraum, Wörter je Einheit und Reihenfolge.
  - Gegenprobe mit `pdftotext`: die Folge (Signatur, Schachtel) ist gleich.
- Alle 1185 Markierungen einzeln (`tmp_ZL1/marker_pruefung.csv`); [VOR] 330, [NACH] 201, «?» 484: jeder Text in seiner Einheit (Rauschen).
- Zeile für Zeile, PDF neben Excel: S. 2, 8, 14, 22, 27, 34, 43, 55, 62, 72, 84, 97, 104, 111, 120, 121, dazu Vorspann S. 1.

## Struktur (kein Fund)
- Die Liste ist nach Schachtel und Ort sortiert. Daher kommen 76 [RÜCK] und 67 [LÜCKE].
  - Die Schachteln 535–1434 laufen lückenlos, und jede Nummer liegt in zusammenhängenden Schachteln.
- [DOPPELT] 1957.18 T17–22: eine Sammelmappe mit 22 Objekten in Sch. 824–826. Die Teile sind richtig.
- Echte Nummernlücken: 1947.3, 1951.1, 1953.22, 1970.3, 1972.2, 1980.11, 1985.1–3/5, 1987.1–2; 1986 fehlt ganz.
  - Kein Fall der Regel 2 (R11): Die Nachbarn haben dasselbe erste Wort (1951.2 ×2, 1970.4 ×5: «Zürich») oder denselben Titel
    (1972.1 ×2 «Matrizen 1 / 72»).
  - Kein Tippfehler-Muster wie in D3472, denn keine Wiederholung liegt fern von ihrer ersten Nennung.
- Vorspann: Prosa zur Signaturbildung, ohne Stück. Der Schlussvermerk «Archivierung … 2002 / …» steht im Info.

## Wichtigste Funde (alle vor Runde 13; Runde 13 ändert D3482 nicht)
- Zeitraum aus Zahlen, die keine Jahre sind:
  - 1952.6 T2 «… Tuberogruppe 2000 KW» bekommt 2000, die Serie 1952.6 übernimmt 2000 (ZL1-01).
  - 1978.21 bekommt 1979 aus «(siehe auch 1979.3)» (ZL1-03); der Verweis gehört in «Verwandte VE» (ZL1-04).
- Die Serie 1955.1 nimmt 1958–1959 nur aus Teil 7, obwohl ihre Nennung und sechs Teile ca. 1955 sind (ZL1-02).
- 1953.10 T3: Der zweizeilige Ort «La Paz (Baja / California)» ist in den Titel gemischt (ZL1-05).
- Gering:
  - « - » trennt Darin-Einträge, 8 Mal: «Axen P» / «Y», «Escher» / «Wyss» (ZL1-06).
  - Rund 80–90 Darin-Zeilen fassen Objekt und «Pläne …» zusammen, 36 Titel enden auf «Pläne …» (ZL1-07). Der Text ist vollständig.

## Muster / Unsicherheiten
- Zahlen im Text wiegen schwerer als das Signaturjahr, und eine Serie erbt den Zeitraum eines Teils (Suche in D3466, D3468, D3472, D3484?).
- Vertretbar, nicht gemeldet:
  - Zeiträume aus dem Darin: 1955.1 T7 «Sihlkellererweiterung 1958 / 1959», 1972.19 «Büro- und Lagerneubau 1974 / 1975».
  - Zeitraum aus dem Titel: 1977.20 «Siloschalungen 1959 – 1963». So steht es im PDF.
- Bei Sammelmappen (1946.2: vier Bauten) nennt der Serientitel nur das erste Objekt. Das ist die Teil-Konvention.
