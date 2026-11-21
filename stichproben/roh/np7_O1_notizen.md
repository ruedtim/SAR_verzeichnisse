# np7 O1 – D149628 (VII.12.B. Stadttheater / Opernhaus), Stand 18:11 gegenüber 15:43

Grundlage: `$S/neu7/alle_excel/D149628_scope_import.xlsx` (Inhalt identisch mit `neu7/testdaten_excel/`), Vergleich mit
`$S/neu6/alle_excel/`, PDF `findmittel_pdf/pdf/D149628.pdf` (576 S.). Skript 18:11: `$S/neu7/findmittel_zu_scope.py`
(sha256 fde790ac…, 5943 Zeilen) – Zeilennummern unten beziehen sich darauf.

## Zahlen
- **Einheiten:** alle 154 Einheiten aus `O1_aenderungen.csv` beurteilt, **alle 154 am PDF**:
  - die 133 Teile von 27.1.4./27.1.5. (S. 563–569) Eintrag für Eintrag mit dem PDF-Text verglichen (Wortabgleich Titel +
    Darin gegen die PDF-Zeile, Datumsspalte gegen von/bis) und die 7 Seiten vollständig gelesen;
  - die übrigen 21 Einheiten einzeln am PDF.
  - Dazu die 4 Patch-Einheiten der beiden Fundzeilen (11.9.2., 18.1.4., 26.2.4., D4054 VII.151.:12.4. Teil 2).
- **Seiten:** 29 PDF-Seiten von D149628 für die geänderten Einheiten und die Fundzeilen: 10 (Inhaltsverzeichnis), 64, 80,
  158, 279, 285–286, 311, 338, 345–346, 365, 367, 500, 518, 540, 541, 543, 544, 552, 555, 560, 563–569. Dazu D4054
  S. 117–118 und für die Zeile «vor 15:43» die Belegseiten 21, 96, 119, 184–187, 226, 252, 285, 364, 389, 439, 469, 548,
  550 und 573.
- **Urteile:** besser 148 · gleich 5 · schlechter 1 · unklar 0.
  - Nach Ursache: 8e2bd7f9 144 (besser 138, gleich 5, schlechter 1) · Änderung 6: 6 · Änderung 8: 2 · Änderung 2: 1 ·
    Änderung 1: 1 (diese 10 alle besser).
  - Die Änderungen 3, 4, 5 und 9 wirken in D149628 nicht. Änderung 7 wirkt höchstens zusammen mit 6, bei 6.5.6. und
    20.1.2.6. (Bindestrich am Zeilenende in offener Anführung).
- **Fundzeilen Runde 6:** Z351 behoben, Z353 behoben (alle 3 Fälle, auch D4054). Beide Korrekturen stammen aus dem Patch.
- **Neue Zeilen:** 4.
  - Durch Änderungen seit 15:43: 1 mittel schlechter (23.4.4.3.); 1 mittel verschoben (Spaltenwert jetzt im Titel,
    4 Teile); 1 gering (« - » statt «-», 5 Fälle).
  - Schon vor 15:43: 1 mittel (30 weitere Spaltenwerte im Text, beim Prüfen gefunden).
  - Kritische Fehler: keine.
- **Textverlust:** 143 Stücke, **kein echter Verlust, keine falsche Zuordnung** (siehe unten).

## Verbesserungen (Hauptmuster)
1. **27.1.4. «Kartonierte kleine Plakate» (61 Teile) und 27.1.5. «Verschiedene kleine Plakate» (72 Teile)** – 8e2bd7f9,
   «Strich nach der Signatur fällt weg» (Z. 2443–2445, auch Z. 2206–2213).
   - Die PDF-Zeilen «27.1.4. - <Text> ¦ <Datum>» waren bis 15:43 Teile mit dem Füll-Titel «…, Teil n» und dem ganzen Text
     im Darin. Jetzt ist der Text der Titel des Teils.
   - Teil-Nummern, Reihenfolge, Stufe und Hierarchie sind unverändert. Der Text ist in allen 133 Teilen vollständig; nur
     Tagesdaten, die in von/bis stehen, fehlen im Titel.
   - 29 Teile haben jetzt einen genauen Tag bzw. Monat statt nur des Jahres, z. B. 27.1.4. Teil 2 «vom 25. Okt. 1902» →
     25.10.1902; 27.1.5. Teil 31 «17. – 19. Jan. 1989» → 17.01.–19.01.1989.
   - 2 Teile bekommen «undatiert» (27.1.4. Teil 5 «ohne Datum», 27.1.5. Teil 50); vorher hiess es «Kein Zeitraum gefunden».
   - Die Serien 27.1.4. (25.10.1902–1983) und 27.1.5. (30.10.1955–29.04.1996, Quelle jetzt sicher) sind genauer. Bei 27.1.
     zeigt ein neuer, richtiger Hinweis, dass Teil 38 (29. April 1996) über den Zeitraum 1891–1991 des
     Inhaltsverzeichnisses hinausgeht.
   - 27.1.5. Teil 13 «1. Opera-Mobile-Spielzeit …» ist dank Änderung 1 (Z. 3026–3036) ebenfalls Titel.
2. **Anführungen (Änderung 6):** 6 Einträge, die bis 15:43 am Strich in zwei Darin-Einträge zerfielen, sind wieder ganz:
   4.1.41., 4.1.55., 6.5.6., 16.8., 20.1.2.6., 20.1.2.13.
   - 16.8. ist genau wie im PDF: «sein Leben – sein Werk».
   - Bei den übrigen 5 Einträgen bleibt kosmetisch « - » statt «-» (siehe unten).
   - In D149628 gibt es am Stand 18:11 keine über zwei Einträge verteilte Anführung mehr (15:43: 6).
3. **Namenslisten (Änderung 8):** 14.5.2. «Evelyn» / «Brunner» und 14.5.6. «Göran» / «Franssson» sind wieder je ein Name.
4. **Nachbartitel (Änderung 2):** 23.2.1. Teil 29 (der zweite «Z»-Eintrag «Fotografien (19. Jh.) …»).
   - Er trägt jetzt den Titel der Einheit statt «Z Porträts …, Teil 29».
   - Er ist der einzige titellose Teil in D149628, der davon betroffen ist.
5. **Jubiläumsspannen (8e2bd7f9):** Bei 6 Titeln fällt die Spanne aus dem Titel weg und steht wörtlich in der Anm; der
   Zeitraum aus der Spalte bleibt.
   - Fälle: 25.2.7., 25.2.21., 25.3.65., 25.3.80., 25.5.3., 25.5.9.
   - 25.2.27. bekommt nur die Anm, die Spanne steht mitten im Titel: «gleich».
6. **Unterlagen nach dem Titel (8e2bd7f9):** 11.6.1.3. «Bewerbung … Schauspieler» / Darin «Briefe, Zeugnis, Repertoire,
   Fotos, Kritiken».

## Verschlechterungen und neue Fehler
- **23.4.4.3. (ID 4196, S. 518) – mittel, Zeitraum.**
  - Der Zeitraum war = 08.11.1959 und ist jetzt = 1959: ein genaues Datum wird ohne Grund zum Jahr.
  - Grund: Die Jubiläumsspanne «125 Jahre Stadttheater Zürich 1834 – 1959» zählt seit 8e2bd7f9 mit dem Endjahr
    (`jahre_im_text` Z. 596–599, `_jubilaeum_ende` Z. 576–578). Das Endjahr ist nur ein Jahr und verdrängt das genaue
    «8. November 1959» derselben Zeile.
  - Ausgerechnet diese Einheit nennt der Skriptkommentar als Beispiel der Regel.
  - Es ist der einzige «gleiche jahre, ungenauer»-Fall in `np7/zeitraum.csv`.
  - Vorschlag: Das Endjahr nicht verwenden, wenn im selben Jahr schon ein genaueres Datum steht.
- **Spaltenwert jetzt im Teil-Titel – mittel, Titel.**
  - Fälle: 27.1.5. Teile 10, 15, 34, 50 (IDs 5030, 5035, 5054, 5070), z. B. «Rezitationen von 1980 Uhland», «Neues vom
    undatiert Räuber Hotzenplotz».
  - Der Spaltenwert stand schon um 15:43 im Darin-Text; durch 8e2bd7f9 steht er jetzt im Titel.
  - Folgen: Der Zeitraum bleibt beim Jahr; bei 3 Teilen kommt der Hinweis «Mehrere Zeitangaben im Titel».
  - Urteil «gleich».
  - Ursache `_an_tabstopp` Z. 756–769: Nach «von/vom/im/bis/und …» wird nicht getrennt. Ist die Lücke zur Spalte klein
    (11–15 pt), bleibt der Wert im Text; bei grosser Lücke wird getrennt, z. B. 20.1.1.5. «im@440 1976-1984@493».
- **« - » statt «-» – gering, Darin, Änderung 6.**
  - Fälle: «„Theater - Illustrierte“» (4.1.41.), «„Tages - Anzeiger“» (4.1.55.), «„Bauschreck - Wettbewerb“» (6.5.6.),
    «„Die Niederdorf - Oper“» (20.1.2.6.), «(„Zürich - Bewachung“)» (20.1.2.13.).
  - Im PDF ist der Bindestrich ein eigenes Zeichen in anderem Schriftschnitt (BCDEEE statt BCDFEE), ohne Lücke (0,1–0,3 pt).
  - Er sollte ohne Leerzeichen angefügt werden.
- **Schon vor 15:43, beim Prüfen gefunden – mittel, eigene Zeile.**
  - Dieselbe Spaltenwert-Ursache steckt unverändert in 27 weiteren Titeln und 3 Darin-Einträgen von D149628, z. B.:
    - 7.2.2.1. Teile 3–14 «… Kollektivverträge und 1919-1921 Arbeiterkommission»;
    - 3.3.1.40./43./45. «mit Registerband und 1957-1958 Unterlagen»;
    - 9.3.3.4./5. «Radio- und 1946-1955 Theaterorchester»;
    - 30.2.1. Teil 24 «Choreographie von 1990 Uwe Scholz».
  - Jeder Fall ist am PDF belegt: Die Zeile endet mit Präposition und Spaltendatum, die Folgezeile setzt den Text fort.

## Die 143 Textstücke aus `O1_textverlust.csv`
| Gruppe | Zahl | Befund |
|---|---|---|
| «Kartonierte/Verschiedene kleine Plakate, Teil n» (27.1.4. Teile 2–62, 27.1.5. Teile 2–73) | 133 | nur der alte Füll-Titel; der Eintragstext ist jetzt Titel (+ Darin nach Doppelpunkt) – kein Verlust |
| «Z Porträts und einzelne Darstellerfotografien, Teil 29» (23.2.1.) | 1 | Nachbartitel durch den Einheitstitel ersetzt (Änderung 2); «Z» steht weiter als Darin-Eintrag – kein Verlust |
| «50 Jahre … 1920 – 1970» usw. (25.2.7., 25.3.65., 25.3.80., 25.5.3., 25.5.9.) | 5 | Spanne steht wörtlich in der Anm, Zeitraum = Spalte – kein Verlust |
| «Internationale Juni-Festwochen 1972 (Spielplan)» usw. (27.1.4. Teile 22, 37, 51, 52) | 4 | Jahr steht in von/bis (= Spalte) – kein Verlust |

## Bemerkungen ohne neue Zeile
- **Datumsreste in den neuen Teil-Titeln:** 3 Fälle, gleichartig zu den D151210-Fällen «Datumsreste in Titeln», die die
  Hauptsession bewusst offen lässt; deshalb nur hier.
  - 27.1.4. Teil 12 «… "Der Bettelstudent", 16. Januar»: Spalte 1971, besser wäre 16.01.1971.
  - 27.1.5. Teil 22 «… Ab 20. Januar 1986» und Teil 23 «…, ab 24. Januar 1986»: Zeitraum nur 1986.
  - Richtig sind dagegen die Teile 39/40 «27. Mai» / «ab 24. Aug.»: Sie haben kein Jahr und bleiben undatiert.
- **Doppelpunkt-Teilung** in 5 neuen Teil-Titeln von 27.1.4. (Teile 2, 6, 8, 9, 10).
  - Es geht nichts verloren.
  - Fraglich ist nur Teil 6: Dort steht das gespielte Stück («Wie es euch gefällt …») allein im Darin.
  - In 27.1.5. wird an Doppelpunkten richtig nicht geteilt (z. B. «Corso-Theater Zürich: Der schwarze Hecht»).
- **Jubiläums-Anm:** «1920 – 1970» neben = 1970 ist der Wortlaut aus dem Titel. Das ist so gewollt, kann aber als Laufzeit
  missverstanden werden.
- 27.1.4. Teile 37, 51, 52 heissen jetzt gleich («Internationale Junifestwochen (Spielplan)»). Man unterscheidet sie nur
  über den Zeitraum; das ist nach der Konvention kein Fehler.

## Auffällige Fälle ausserhalb der Änderungen (unverändert seit 15:43, bisher nicht erfasst)
- 25.2.2. (ID 4463, S. 540) «Fünfzig Jahre Häusermann’scher Privatchor 1897 – 1947» hat weiter 1897–1947 (Quelle Titel).
  - Die neue Jubiläumsregel sucht nur Ziffern («50 Jahre»), kein Zahlwort; richtig wäre = 1947.
- 14.5.12. (ID 2145, S. 312): «Robert Satanowski, Dirigent: Repertoire, Pressestimmen» und «Robert Stolz: Korrespondenz, …»
  sind ohne Trenner zu einem Eintrag verschmolzen.
- 4.1.41. (ID 278, S. 64): «Einladung zur Othmar-Schoeck-Feier zu seinem; 50. Geburtstag» – «; » steht mitten im Satz
  (gering).
- 5.4.1.19. (ID 472, S. 116): «„Pensions - und Hilfskasse“» statt «Pensions- und» (gering; in der Zeile zu « - » erwähnt).
