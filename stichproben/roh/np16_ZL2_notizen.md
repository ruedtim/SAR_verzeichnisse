# NP16 – Paket ZL2 (D141020, D2935) – Notizen

## Bilanz
- 2 Dateien ganz geprüft (601 + 240 Einheiten). Beide sind **ohne kritischen Fehler**. Es gibt 0 neue kritische Funde.
- 8 mittlere Funde (D2935 6, D141020 2) und 5 geringe. Alle haben die Ursache «vor Runde 13»: Keine der beiden Dateien wurde in Runde 13 geändert.
- In `bekannt.csv` gibt es keine K-Zeile zu diesen Dateien. Aus der Liste «Bekannt, nicht neu melden» kommen nur die Werktitel-Zeiträume vor (siehe unten).
- Das Ergebnis stimmt mit NP12 (L1) überein: beide Dateien ohne kritischen Fehler. Diese Prüfung findet zusätzlich mittlere Befunde (siehe unten).

## Vorgehen (je Datei ganz)
- Kompaktmappe ganz gelesen, Strukturbericht (D141020: DARIN 1, OHNE 4; D2935: HINWEIS 1) jede Markierung einzeln geprüft.
- Excel aller Einheiten mit allen Darin-Zeilen gesehen, PDF-Text an den Zweifelsstellen sowie an Vorspann und Schluss.
- Unabhängige Skriptprüfungen mit dem Zeilen-Cache (`tmp_ZL2/`):
  - Signaturliste PDF↔Excel: alle Signaturen vorhanden, keine Lücke, keine doppelte.
  - Jede PDF-Zeile wortweise in der Einheit ihrer vorangehenden Signaturzeile gesucht: alles gefunden. Ausnahmen sind nur Schachtelmarken, die Zwischenüberschrift 8.7.–8.11. (D2935) und die Schlussvermerke (Info).
  - Eltern, Ebene, Stufe und «Übergeordnete Signatur» sind stimmig.
- D141020 hat nur zwei Spalten (Signatur x 71, Inhalt x 152). Es gibt also kein Gruppenende-Problem. Im Detail stehen keine Schachteln, die leere Schachtel-Nr. ist daher richtig.

## Wichtigste Funde (mittel)
- **D2935 7.–7.2. und 9.–9.5.:** Die Schachtel-Nr. ist leer, richtig wären 6 bzw. 8. Eine Schachtelmarke gilt nur im eigenen Hauptabschnitt, obwohl die Zählung durchläuft. Schon in NP12 gemeldet, weiter offen.
- **D2935 3.14. und 3.19.:** Der Zeitraum reicht bis 25.03.1992, weil das Datum aus dem Revisionsvermerk «(fehlt, 25. März 1992)» stammt. Neu.
- **D2935 1.28.:** Zeitraum 1934 aus dem Vermerk «[… Vorgeschichte der Eingemeinung von 1934.]», richtig wäre 1926. Neu.
- **D2935 3.68. und 3.83.:** Der Titel ist am Doppelpunkt abgeschnitten («… Stadt Zürich 1», Massstab «1 : 30'000»; «handschriftlich:»), der Rest steht im Darin. Neu.
- **D2935 6.3., 3.19., 8.6., 9.4.:** Die Aufzählungen stehen im Titel, 6.3. hat zudem den Zeitraum 1803–1887. Die ersten drei sind aus NP12 bekannt, 9.4. ist neu.
- **D2935 2.22.:** «2 Exemplare» steht im Titel. Bekannt seit der ersten Nachprüfung.
- **D141020 2.17.1. und 2.21.1.:** Als Titel steht der Gruppentitel («Leonore 40/45 (inkl. Opernsuite)», «Penelope»), die eigene Zeile «Basel 25.3.1952 (Uraufführung)» bzw. «Salzburg, … 17.8.1954 (Uraufführung)» steht im Darin 1. Neu. Die Ursache im Skript ist unklar.
- **D141020, 18 Aufführungen mit «d./d.m.yyyy»** (z. B. 2.4.6. «6./7.9.1970»): Erfasst ist nur der letzte Tag, als «Genau». Das ist Muster M12. Mit Monatswechsel stimmt der Zeitraum.

## Bekannt bzw. Konvention, nicht gemeldet
- Zeiträume aus Werktiteln:
  - D2935: 1.18., 1.19., 1.23., 2.7. (1869 aus «Staatsverfassung vom 18. April 1869»), 2.32., 3.47., 5.3. (aus dem «Vgl.»-Titel).
  - D141020: 4.6.4.3. (1875), 6.1.2.1. (1913, geht weiter an 6.1.2. und 6.1.), 6.1.2.5. (1940), 6.2.4. (1937, geht weiter an 6.2.).
- D2935 2.1. und 2.7. «1899» sind Tippfehler im PDF (gemeint ist wohl 1889).
- D2935 S. 2 «Bemerkung zu Abschnitt 6./8.» ist Prosa im Vorspann. Die Übersicht in D141020 S. 1 nennt Schachtelzahlen (9, 13, 29 …). Beides gehört zum Vorspann bzw. zur Übersicht und wird nach Konvention nicht importiert.
- D141020 1.21./1.24. «(I)»/«(II)»: Nach Konvention sind das Teile mit «(I)» im Titel. Die [OHNE]- und [SIG?]-Markierungen sind Rauschen der Mappe.
- D141020 [DARIN] 4.6.4.2. «100. Geburtstag des Palais Garnier» ist Text und keine Signatur.

## Unsicherheiten
- D141020 1.21. (II) und 1.24. (II): Libretto und Opernsuite stehen im Teil (II). Das PDF trennt hier nicht eindeutig; die Reihenfolge spricht für (II). Kein Fund.
- D2935: «Protokolle (8.1. bis 8.6.)» steht im Darin von 8., «Akten und Materialien (8.7. bis 8.11.)» nur als Hinweis bei 8.7. Das ist uneinheitlich, aber beides konventionsgemäss.
- Die geringen Funde (Darin-Zeilen getrennt oder zusammengefügt, ungenaue Tagesdaten, Untertitel im Titel) sind nur gezählt, nicht vollständig erhoben.
