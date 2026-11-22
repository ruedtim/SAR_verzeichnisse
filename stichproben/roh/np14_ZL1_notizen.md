# ZL1 – D151210 (VII.200., Schauspielhaus Zürich AG), Vollprüfung am Stand Runde 11

## Bilanz
- 3161 Einheiten (1679 mit eigener Signaturzeile, 1482 Teile), 424 Seiten. Urteil: **kritisch, nur durch einen Grenzfall**
  (ZL1-01); ohne ihn ohne kritischen Fehler. Dazu 8 mittlere und 1 geringer Fund (ZL1-02 bis ZL1-10), alle vor Runde 11 entstanden.
- NP6-Kritisch 8.1.1.44. (S. 356, erfundener «Teil 6») bleibt **behoben**: Serie + Teil 1–5 in PDF-Folge, Teil 1 = «Don Carlos».
  Die übrigen NP6-Funde waren mittel/gering. 8 davon bestehen noch (Zeiträume aus Lebens-/Vermerkdaten, Ereignisdatum, Teil-Titel).

## Vorgehen (Hilfsdateien in tmp_ZL1/)
- `pdfsig.py`/`folge.py`: 3084 Signaturzeilen (x < 125, Zeilenanfang) + 10 Signaturen am Zeilenende (8.1.1.x) per difflib
  gegen die Excel-Folge. Keine Einheit fehlt, keine ist erfunden. Eingefügt sind nur gewollte Fälle: Sammeleinheit + «Teil 1» bei
  ausdrücklichem «Teil n» (3.3.3.2./10./21., 4.1.6.17./18., 63 × 8.1.1.x; `teile811.py`: Teil-Nummern PDF = Excel).
- `struktur_check.py`: Eltern = Präfix der Dezimalsignatur, Ebene, Stufe, übergeordnete Signatur, Teile direkt nach der ersten
  Nennung, Teil-Nummern lückenlos, keine Lücke und kein Rücksprung. Einzige Abweichung: 4.1.2.38.→4.1.3.38. (Tippfehlerregel).
- `wortcheck2.py`/`multiset.py`/`rueck.py`: Jede der 14036 PDF-Zeilen ab S. 10 geht an die Einheit ihrer letzten Signatur- bzw.
  «Teil n»-Zeile; die Wortmengen wurden in beide Richtungen verglichen. Abweichungen gibt es nur bei Bindestrich-/Klebefällen,
  «Schachtel n» (steht in der Schachtel-Spalte), übernommenen Titeln und den Schlussvermerken S. 424 (Info).
  Kein Text fehlt, keiner steht bei der Nachbareinheit, in Titel/Darin steckt keine Signatur.
- Strukturbericht: 271 [DOPPELT] = Teile von 31 langen Serien (z. B. 5.2.4.1. «1963–1970», 85 Teile), alle zusammenhängend.
  2 [DARIN] = Ordinalzahlen («20. und 21. Jahresbericht»). [OHNE] = die 1482 Teile, alle im Skript enthalten.
- Schachteln 11.1.–11.3. (71 Teile) am PDF geprüft: richtig. Vorspann S. 1–10 (Übersicht, Inhaltsverzeichnis): kein Stück
  ohne Nummer. Rund 40 Seiten Zeile für Zeile (Liste im Dateiurteil). Die volle Prüfmappe habe ich für S. 12, 24–25 und 144 gelesen.
  Ihre [VOR]/[NACH] sind Rauschen der Textsuche.

## Wichtigste Funde
1. **ZL1-01 (kritisch, Grenzfall), S. 420:** Das Plakat «Juni-Festwochen 1952 … (Entwurf von Honegger-Lavater)» steht ohne
   Nummer nach 13.4.7. und vor «13.5.». Es ist Darin von 13.4.7. (Einzelplakat von Häfelfinger), gehört aber zur Gruppe 13.4.
   Regel 9 greift nicht, weil der Abstand (30,7 pt) gleich gross ist wie zwischen den Unternummern. NP6 D4: «fraglich».
   Kein Fund nur, wenn das Plakat physisch in der Mappe 13.4.7. liegt.
2. ZL1-02: «Signatur nicht belegt (sec, 07.12.2023)» (7.3.50./51.) ergibt Genau 07.12.2023, 7.3. und 7. reichen bis 2023.
   Der Vermerk steht auf der Signaturzeile selbst, deshalb nicht K169.
3. Zeiträume aus Lebensdaten bzw. dem Ereignisdatum der Titelzeile (ZL1-05 bis ZL1-08); Listeneintrag als Teil-Titel (ZL1-09).

## Beobachtungen ohne Fund, Unsicherheiten
- 8.1.1.x: 37 Saisonvermerke («Die Aufführungsfotos „X“ … sind (nicht) vorhanden») stehen im Darin des letzten Teils, ohne
  grösseren Abstand, nach Konvention also richtig. Inhaltlich gelten sie für die Serie (8.1.1.44. T5 nennt «Hoffnung!?» aus T4).
  Höchstens mittel. Streuzahl «31» (S. 36) steht nur im Blatt Vollständigkeit; sie ist kein Inhalt.
- Die Zuordnung «letzte Signatur davor» deckt Gruppenende-Fälle nicht ab. Darum habe ich alle 24 Absätze vor einer höheren
  Nummer einzeln gesichtet (`gruppenende.py`). Nur 13.4.7. ist ein echter Kandidat.
