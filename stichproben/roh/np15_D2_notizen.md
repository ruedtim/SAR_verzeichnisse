# D2 – Durchsicht Schluss und Info, Teil 2 (143 Dateien, Runde 12)

## Bilanz
- An den geprüften Stellen: 141 Dateien ohne kritischen Fehler, 2 mit (D1759 neu D2-1; D1739 bekannt K39, noch da).
- Neue Funde (`D2_funde.csv`): 1 kritisch, 1 mittel, 4 gering.
- Bekannte K-Zeilen: K39 noch da; K203 (D175949) und K206 (D1729) behoben. Ebenfalls behoben: K109 (D175454), K172
  (D175994), K76 (D152398), Anhang D175827.
- Vorgehen: teil_2.txt ganz gelesen; jeden Verdacht an `mappen_r12` und am PDF geprüft; frühere Funde über
  `tmp_D2/alt.sh` abgeglichen; alle Info-Sätze der 143 Dateien noch einmal gelesen (`tmp_D2/info_d2.tsv`).

## Wichtigster Fund: D2-1 D1759, Stück ohne Nummer nur im Info (kritisch, Konventionsfall)
- S. 9 nach 6.2.3.: «… Die dazugehörigen vier Compact Discs wurden in den Archivbestand integriert.» Keine Einheit nennt
  die CDs, und es gibt keine Bestandszeile. Soll: Bestandszeile V.G.c.118. mit dem Absatz im Darin, wie K206.
- Vorgeschichte: K110 (NP11/12) setzte als Soll das Blatt Info, damals gegen das Darin von 6.2.3. Erst die heutige
  Konvention «Stück ohne Nummer im Schlussteil» macht daraus einen Fund. Bitte bestätigen.
- Ursache: Regel 1 der Runde 12 und die Filter kennen nur Behälter und die Verben «enthält noch» / «umfasst neben» /
  «liegen bei». Datenträger und «integriert» trifft keins; auch `info_menge_runde11.csv` und `info_stuecke_r12.csv` haben
  D1759 nicht.
- Vorschlag: Suchlauf über alle Info-Blätter nach CD, DVD, Diskette, Datenträger, Film, Video, Tonband und «in den
  (Archiv)Bestand integriert/aufgenommen/eingereiht».

## Weitere Funde
- D2-2 (mittel), D174277 :6–:34: Der Zeitraum ist das Ablieferungsdatum aus dem Titel; die Einträge reichen bis 1967/1979
  zurück. 29 Einheiten, gleicher Mechanismus wie D176151 16.20. (bekannt, mittel).
- Gering, Darin-Zeilen ohne Textverlust: D2-3 D152401 und D2-4 D175994 (zwei Listeneinträge in einer Zeile); D2-5 D167
  («A - D» als Spiegelstrich gelesen, 6×); D2-6 D175480 (18 Einträge am kleinen Spiegelstrich zerrissen, Verweis
  «vgl. auch …» im Darin).

## Kein Fund (geprüft)
- Info: Verweise (D151730, D152400), Literatur (D152781, D175454, D175827), Zusammenfassungen («Der Bestand umfasst …»,
  D1618, D152401) und Bearbeitungsvermerke (D175996, D176551).
- Bestandszeilen nach Konvention: D151756, D151759, D152383, D1726, D1729, D152401.
- Nicht übernommen: nur Titelblätter, Köpfe, Zwischenüberschriften und Silbenreste; dazu die Lückenvermerke D152817.
- Rauschen der Prüfmappe ohne Fehler: D176551, D1686, D152390, D152398, D152781.

## Unsicherheiten
- D2-1 ist ein Konventionsfall. Nicht neu gemeldet: D176726 «NACHWEISE» im Darin der Bestandszeile (NP11 gering,
  streng gelesen mehr); D152390 Überleitungssatz (NP12 mittel).
- D152401: «Total: 20 Schachteln» = :1–:6 (13+2+1+1+2+1), also ohne die zusätzliche Schachtel. Entscheid 1 der Runde 12
  begründet das umgekehrt; das Ergebnis bleibt richtig.
