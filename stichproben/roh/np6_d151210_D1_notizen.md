# D151210 (VII.200., Schauspielhaus Zürich AG) – Vollprüfung D1, PDF-Seiten 1–106, Stand 15:43

Skript `$S/neu6/findmittel_zu_scope.py` (sha256 c7c28ce2…, 5475 Zeilen), Excel `$S/neu6/D151210_scope_import.xlsx`.

## Überblick

- **Geprüft:** alle 106 Seiten («ja»), alle 547 Einheiten mit PDF-Seite 10–106 einzeln gegen den PDF-Text; Vorspann
  S. 1–9 gegen Teilbestände und Signaturen. Zusätzlich eigene Abgleiche über den ganzen Bereich: Signaturen PDF ↔ Excel
  je Nummer (auch stark eingerückte Nummern), Parent/Ebene/Übergeordnete Signatur, Stufe, Teil-Nummern und «…, Teil n»,
  Darin-Trenner (« - », «; »), Titelenden mit Restzeilen, Darin-Jahre ausserhalb des Zeitraums; Einzüge/Schrift mit
  pdfplumber.
- **Ergebnis:** kein kritischer Fehler. Gliederung, Signaturen, Hierarchie, Ebenen, Stufen und Teil-Nummern sind auf
  S. 1–106 fehlerfrei; keine Teile mit dem Titel eines Nachbarteils (M13). **10 Fundzeilen, 16 Einheiten:** 8 mittel
  (6 × Zeitraum, 1 × Titel/Darin, 1 × Darin-Sammelzeile mit 5 Fällen), 2 gering (Zeitraum; «; »-Sammelzeile mit 3
  Fällen). Alle Fehler bestanden schon um 13:15 (Regel: «vor 13:15»); keine Regression durch A–P.
- **Seit 13:15 im Bereich geändert (12 Einheiten):** Regel G – 2.3.2.3. (IDs 59–62), 2.3.2.9. (IDs 92/93), 2.4.2.1.
  (IDs 138–141): Teil-Nummern jetzt in PDF-Reihenfolge, «…, Teil n» passend → besser (für S. 1–106 ist der Befund
  «Teil-Nr. nicht eindeutig» aus Runde 5 behoben). Regel F – 3.6.5.3. (ID 504), 3.6.6.3. (ID 512): Anm «erste Nennung:
  …», Zeitraum umfasst die gleichnamigen Fortsetzungen → richtig.

## Vorspann S. 1–10, Übersicht, Info

- Das Detailverzeichnis beginnt richtig: S. 10 «DETAILVERZEICHNIS» (nicht importiert), erste Einheit 1. Der Vorspann
  ist Übersicht (S. 1–2) + Inhaltsverzeichnis (S. 3–9) + Überschrift; dort stehen keine eigenen Einheiten. Der Info-Text
  «Titelblatt, Einleitung, Inhaltsverzeichnis» ist generisch – eine Einleitung gibt es nicht.
- **Alle 208 Nummern** der Übersicht und des Inhaltsverzeichnisses sind Einheiten im Excel («Signaturen nur im Vorspann:
  –» stimmt). Wortlaut weicht teils ab (2.2.1., 2.2.2., 2.2.4., 3.3.4.; 2.3.2. «Direktoren der Neuen Schauspiel AG» ↔
  Detail «… des Schauspielhauses Zürich») – der Detailtitel gilt, kein Fund.
- **Übersicht ↔ Teilbestände:** Die Übersicht hat nicht nur 1.–11., sondern auf S. 2 auch 12.–15.; das Excel hat genau
  15 Teilbestände (Ebene 1, Parent leer, Übergeordnete Signatur VII.200.). Titel nach dem Detail, Zeiträume aus der
  Übersicht (Quelle «Inhaltsverzeichnis», Anm mit Spielzeiten, 11. «ca. 1930–1988/89») stimmen; 14./15. ohne Datum in der
  Übersicht → aus den Untereinheiten.
- **Blatt Info:** Schlussvermerke (5 Zeilen von S. 424) vollständig; «Nicht übernommen: nichts» und «Zeilen mit fehlenden
  Wörtern: keine» – auf S. 10–106 fand ich keinen verlorenen Text. «Kopf-/Fusszeilen, die nur einmal vorkommen: 1» ist
  wohl die Streuzahl «31» auf S. 36 (10 pt, rechter Rand) – kein Inhalt.

## Fehler nach Art (mit Ursache)

### Zeitraum (mittel)
1. **Datum des ersten Dokuments gilt für die ganze Mappe** – IDs 14, 15 (2.1.1. Teile 3/4, S. 12), 359 (3.3.5.2.
   Teil 2, S. 70). Beispiel ID 14: Titel «Auszug aus dem Handelsregisteramt … vom 15. Okt. 1952, Abschrift» → Genau
   15.10.1952, das zweite Stück derselben Mappe im Darin ist «… Generalversammlung … vom 6. Febr. 1967». ID 359: «Budget
   1961/62» wird Titel und Zeitraum 1961–1962, die Mappe enthält Stücke von 1963, 1964, 1968. Ursache: Ereignisdatum der
   Titelzeile wird gesetzt, bevor das Darin geschätzt würde (Z. 3906–3907); Regel B erweitert nur mit Spaltendaten und
   Jahreszeilen (`darin_daten` Z. 3065–3085), nicht mit Daten im Text der Einträge – in D151210 gibt es keine
   Datumsspalte, Regel B greift hier nie.
2. **Todesdatum im Nachruf fällt weg** – ID 50 (2.3.2.1. Teil 4 «Zum Tod von Oskar Wälterlin», S. 18): 1933–1945 aus
   den Inhaltsjahren zweier Listen; «Nachruf: Oskar Wälterlin 30. August 1895–4. April 1961» wird ganz verworfen
   (`jahre_im_text` Z. 560–562), die Regel «nur das Todesjahr» (Regel A, Z. 3067–3069) gilt nur für Spaltendaten.
   Folge: Serie ID 47 endet 1955.
3. **Titelloser Fortsetzungsteil: Titel vom vorherigen Teil, Zeitraum nicht** – ID 93 (2.3.2.9. Teil 3, S. 24):
   «Korrespondenz und Akten, Teil 3» (Fortsetzung von «Korrespondenz und Akten 1970–1981»), aber Genau 02.11.1957 aus der
   Kopie eines Ehevertrags. `ergaenze_titel` nimmt den Titel des vorherigen Teils (Z. 4157), der Zeitraum kommt nur vom
   Knoten und nur bei Quelle Titel/Datumsspalte/Inhaltsverzeichnis (Z. 3873–3874, 3908–3909). Widerspricht dem Info-Text
   «… übernehmen den Titel … des vorherigen Teils … und deren Zeitraum». (ID 141 2.4.2.1. Teil 5: 1951–1952 statt
   1950–1955, plausibel, nicht gemeldet.)
4. **Inhaltsverzeichnis-Zeitraum ohne Abgleich mit dem Darin** – ID 182 (2.5.1., S. 45): 1938–1960 (Inhaltsverzeichnis),
   Darin «… Ein Rückblick, Schauspielhaus Zürich 1992–1999», kein Hinweis (Z. 3861–3867). Schwächer: ID 18 (2.1.3.
   Teil 2) erbt 1953–1991, Darin «… vom 15. Juli 1946».

### Titel/Darin (mittel)
- ID 95 (2.3.2.9. Teil 5, S. 24): Titel «Zum Tod von Harry Buckwitz Todesanzeigen». «Todesanzeigen» ist eingerückt wie
  Aufzählungstext (x 152.7, Titel x 138.4) und die letzte Zeile der Seite. Ursache: «kurzer Rest nach hartem Umbruch
  gehört zum Titel» (≤ 2 Wörter, Z. 2959–2963) ohne Einzugsprüfung. Einziger Fall auf S. 1–106 (Abgleich aller Titelenden
  mit Restzeilen).

### Darin falsch getrennt (mittel, Sammelzeile)
- 5 Fälle, je zwei Einträge verschmolzen, weil `teile_inline` « - » nur vor Grossbuchstaben/Anführungszeichen trennt
  (Z. 2655): IDs 99 (S. 25 «… des Burgtheaters - einzelne Zeitungsartikel …»), 147 (S. 34), 216 (S. 51), 261 (S. 58), 424
  (S. 81). Mit Grossbuchstaben wird richtig getrennt (z. B. ID 87, 134, 164).

### Gering
- ID 80 (2.3.2.7. Teil 3 «Zum Tod von Teo Otto», S. 22): kein Zeitraum, weil «16. Heft 1967/68» als Heftnummer gilt
  (`NICHT_JAHR_VOR_RE` «Heft», Z. 347).
- «; » mitten in Namen/Adressen (Sammelzeile, 3 Fälle): IDs 287 «Opernhauses; Zürich», 452 «Englischviertelstrasse; 9:»,
  534 «Friedrich; Schütze». Die Folgezeile steht auf dem Textzug der Aufzählung, gilt aber als Unterzeile, weil ihr
  erstes Wort noch auf die kurze Vorzeile gepasst hätte (`ist_umbruch` Z. 2534, `baue_eintraege` Z. 2636–2642).

## Beobachtungen ohne Fundzeile (evtl. Entscheid der Hauptsession)

- **Titel-/Ereignisjahr enger als die Daten der Darin-Einträge** (Text, keine Spalte), Zeitraum folgt aber der
  Titel-Konvention: 2.2.7.2. (ID 32) Genau 1971 bei Dokumenten 1969–1970; 2.2.7.6. (ID 36) Genau 1971 / «Zeitungsberichte
  1970–1971»; 3.5.6.4. (ID 466) 12.1975 / 1974–1975; 3.5.6.6. (ID 468) 01.1978 / «Presseberichte 1975–1978»; 3.5.8.
  (ID 474) Genau 1976 / «Korrespondenz … 1975–1978»; 3.5.11.1. (ID 480) Genau 1995 / 1993–1994. Gleiche Ursache wie
  Punkt 1 – sollte Regel B auch Textdaten nehmen (≤ 35 J.), würden diese Fälle mit behoben.
- Ältere Beilagen ausserhalb eines Titel- oder Inhaltsverzeichnis-Bereichs (z. B. 3.6.2. ID 496 «von1949», 3.6.4. ID 500
  «von 1955», 2.4.1.2.-Teile mit Beilagen aus Vorjahren) sind üblich und nicht gemeldet.
- 2.3.1.1. Emil Oprecht (ID 39): Genau 04.1990 aus dem einzigen datierten Stück (Nachruf seiner Frau); Todesanzeige und
  Trauerfeier (1952) sind undatiert. Schätzung nach Regel, Hinweis vorhanden.
- 3.3.3.2., 3.3.3.10., 3.3.3.21. «…, Teil 1» / «…, Teil 2»: im PDF 2 Zeilen, im Excel Sammeleinheit (Serie) + Teil 1 +
  Teil 2 – gewollt (`spalte_teil1_ab` Z. 3587–3601 nennt genau dieses Beispiel), keine erfundene Signatur.
- **Teile mit Nachbartitel:** auf S. 1–106 keine. Alle 14 Teile mit übernommenem Titel sind echte Fortsetzungen
  (2.1.3. T2/T3, 2.3.2.3. T3–T5, 2.3.2.9. T3, 2.4.2.1. T5, 3.5.4.4. T2; 3.3.3.x T1/T2 im PDF benannt). Die rund 120
  Fälle aus Runde 5 liegen ab S. 179 (5.2.4.x, 5.2.5.x, 6.4. …).
- ID 547 (4.1.2.38., S. 115, Tippfehler für 4.1.3.38., Hinweis «Nummerierung springt») steht in der Excel-Reihenfolge
  direkt nach 4.1.2.4. von S. 106 – Entscheid 5, Bereich D2.
- Fehler im PDF (kein Fund): fehlende Aufzählungsstriche (2.4.1.2. T6/T12/T17, 2.4.3.2., 3.2.3.9., 3.1.1.10. über den
  Seitenwechsel), Strich mitten im Eintrag («- Direktion: …» in 1.3., «- Personenangeben von 1972» in 3.3.5.3.),
  «Scheiben des Bundesamtes», «Externisten1938–1948», Streuzahl «31».

## Wichtigste Punkte

1. **Regel B wirkt in D151210 nicht** (keine Datumsspalte): Zeiträume aus Titel/Ereignisdatum werden nie durch datierte
   Darin-Einträge erweitert. Klar falsch, wo die Titelzeile nur das erste Dokument einer Mappe ist (IDs 14, 15, 359:
   z. B. Genau 15.10.1952 statt 1952–1967); dieselbe Ursache macht Ereignistitel zu eng (IDs 32, 36, 466, 468, 474, 480).
   Ursache Z. 3906–3907 + `darin_daten` Z. 3065–3085.
2. **Nachrufe in der Text-Schätzung:** Lebensdaten mit Tagesdatum fallen ganz weg (Z. 560–562), Regel A nur für Spalten
   (Z. 3067–3069) – ID 50 «Zum Tod von Oskar Wälterlin» 1933–1945, Serie ID 47 ohne 1961.
3. **Titelloser Fortsetzungsteil bekommt den Titel, aber nicht den Zeitraum des vorherigen Teils** – ID 93 Genau
   02.11.1957 statt 1970–1981 (Z. 3873–3874/3908–3909 ↔ Z. 4157).
4. **Darin-Trennung bei « - » + Kleinbuchstabe fehlt** (5 Fälle, `teile_inline` Z. 2655) und **Titel nimmt eine
   eingerückte Ein-Wort-Zeile auf** (ID 95, Z. 2959–2963).
5. Gliederung, Signaturen, Hierarchie, Teil-Nummern (Regel G) und Vorspann-Grenze sind auf S. 1–106 richtig; die 15
   Abschnitte der Übersicht entsprechen den 15 Teilbeständen.
