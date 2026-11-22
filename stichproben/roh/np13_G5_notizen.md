# G5 – Notizen (NP13, Gegenprüfung Runde 10, Regeln 11–13)

## Bilanz
- 6 Dateien, alle **ohne kritischen Fehler** im Stand jetzt: D140969, D2643, D3190, D32837, D3672, D3943.
- Diff-Einheiten beurteilt: 42 Zeilen in G5_urteile.csv (Sammelzeilen für D32837). Ergebnis: alle «besser» oder «gleich», keine «schlechter».
- Altzeilen: 7 behoben (K61, K71, K128, K129, K130, K131, K136), 2 teilweise mit nicht kritischem Rest (K121, K163).
- Neue Funde: 0 kritisch, 1 mittel (G5-1, vor Runde 10), 2 gering (G5-2 vor Runde 10, G5-3 Runde 10 Regel 12).

## Vorgehen
- Diff je Datei Zeile für Zeile am PDF (pdftotext, Zeilen-Cache).
- Eigene Skripte in tmp_G5/skripte, alle mit `python -I`:
  - gliederung.py: Eltern-Präfix, Ebene = Eltern-Ebene + 1, Nummernfolge, Teilfolge.
  - teile2.py: difflib-Abgleich aller Signaturzeilen des PDF mit «Nr. im PDF» in Excel-Folge.
  - zeilencheck.py: Jede PDF-Zeile wird der Einheit der vorangehenden Signaturzeile zugeordnet. Geprüft wird, ob ihre Wörter dort stehen.
  - inhaltvgl.py: Vergleich alt↔neu nach Signatur/Titel/Darin, ohne Teilnummer und Ebene.
- D32837: Gliederung ganz per Skript, ohne Abweichung. Alle 267 Signaturzeilen S.5–57 decken sich in der Folge mit der Excel; neu ist nur 1. Zeilencheck S.5–57: kein Text in fremder Einheit, es fehlen nur Datumswörter (stehen in von/bis), Trennfehler im PDF und der Schlussteil S.57 (jetzt Info). Von Hand geprüft: S.1, 3–5, 7–8, 14–15, 18, 51, 56–57.
- D32837: Von 219 GEÄ sind 142 nur Ebene +1 unter 1.; dazu kommen 1.1.–1.8. mit neuem Elter 1. Die übrigen Einträge sind nur Teil-Verschiebungen (1.2.1.1. T16–T67, 4.4.1. T11–T16) mit gleichem Inhalt.

## Wichtigste Punkte
1. Regel 12 hat in meinen Dateien nichts doppelt oder erfunden:
   - D32837 1.: nur Vorbemerkung S.1 und Übersicht S.3, Detail beginnt mit 1.1.
   - D3672 X./X.1.–X.4.: nur im Inhaltsverzeichnis; alle anderen Einträge des Inhaltsverzeichnisses stehen im Detail.
   - D140969 57.: nur in der eingeschobenen Übersicht.
   - D2643: sieben «[Enthält …]» stehen bei der richtigen Einheit (3.9.1. unter Sozialdepartement).
   - D3190 9.: jetzt eine einzige Einheit aus dem Detail.
2. Regel 11 und 13 greifen richtig:
   - D32837 «IV.4.1. Mappe 9» ist jetzt ein eigener Teil; Mappe 8 ist bereinigt.
   - D3943 hat neun Unternummern mit Titel, Jahr in von/bis und richtigem Elter. Kein Text verloren: «flache»/«Taschenmesser» des Zeilenübergangs stehen in X.G.209.:2. Die Suche im ganzen PDF findet keine weiteren Unternummern.
3. Regel 2 (K131): Der Schlussteil S.57 steht ganz im Info. Zeitraum von 4.4.4. ist 1868–1973, von 4.4. 1840–1976, von 4. 1840–1978.

## Reste und Muster
- G5-1 (mittel, vor Runde 10): In D32837 haben 12 Teile von 1.2.1.1. den Titel «…, Programmhefte, Teil n», und «Programme JJJJ/JJ» steht als Darin 1. Bei Teil 51 und Teil 62 ist der Zeitraum aus dem Darin geschätzt (1917–1989, 1926–2000). Die Signaturzeilen sind gleich gesetzt wie bei den übrigen Teilen.
- K121-Rest (mittel, bekannt): X.G.200. und X.G.209. tragen den Titel der ersten Unternummer.
- K163-Rest (gering): 58. hat keinen Übersichtstitel, 57. keinen Umfang, die Übersichtszeilen 50–58 stehen weiter im Darin von 50-58. K71-Rest: 9. ohne Umfang «2 Schachteln» (laut Soll nur «zulässig»).
- Gering: G5-3 D32837 ID 1 hat PDF-Seite 1 und den Hinweis «Übersicht (S. 1)», S.1 ist aber die Vorbemerkung (Übersicht S.3). G5-2 D3943-Zeichenerklärung «*»/«**» im Darin der Bestandszeile.

## Unsicherheiten
- D3672 (1503 Einheiten) und D3943 sind ausserhalb der Diff nur per Skript-Zeilenabgleich geprüft, nicht Zeile für Zeile von Hand.
- Der Zeilenabgleich prüft Wörter je Einheit, nicht ihre Reihenfolge innerhalb des Darin.
- K129 (Regel 9) habe ich nur im Abgleich mitgesehen. Die Prüfsession hatte ihn schon geprüft.
