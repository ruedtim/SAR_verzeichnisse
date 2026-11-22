# D4 – Durchsicht Schluss und Info, Teil 4 (75 Dateien, D2587 … D2828)

## Bilanz
- Alle 75 Blöcke von `teil_4.txt` gelesen. Jeden Verdacht in der vollen Prüfmappe, der Excel (`sig.py`, Info, Vollständigkeit)
  und im PDF (`pdftotext`, `rawlines.py`) geprüft und mit NP10–NP14 abgeglichen. Runde 12 ändert keine dieser Dateien.
- **72 ohne kritischen Fehler, 3 kritisch:** D2630 (neu), D2614 (bekannt K41), D2710 (bekannt K117).
- **Neue Funde:** 1 kritisch und 3 gering, siehe `D4_funde.csv`.

## Wichtigster Fund
- **D4-1 D2630 V.L.186.:9. (kritisch wie K169/K203):** Der Bearbeitervermerk «Erstellt und bearbeitet von cca / 20. Juni 2000»
  (S. 1 y724, nach einer Leerzeile unter der Liste) steht als Darin 8 von 9. «Varia». Das Info zeigt «–».
  - NP12 (P3) meldete ihn mit der Schachtel als mittel, vor K169. In `bekannt.csv` fehlt er.
  - Ursache: «… von <Kürzel> / <Datum>» trifft keine Schlussregel. SCHLUSS_RE kennt nur «Bearbeitet von», SCHLUSS_DATUM_RE nur
    «Datum / Name» oder «Kürzel / Datum» am Zeilenanfang, SCHLUSSNOTIZ_RE verlangt einen grossgeschriebenen Namen.
  - In allen 715 Prüfmappen kommt die Form nur hier vor.

## Gering (neu)
- **D4-2 D2704:** «Vgl. auch … Dokument 0474B …» ist Darin 7 der Bestandszeile, gehört ins Info.
- **D4-3 D2657:** «Die Dokumentation kann erweitert werden.» ist Darin 16 der Bestandszeile, gehört ins Info.
- **D4-4 D2763 9.:** Darin 5 enthält zwei Einträge in einer Zeile.

## Bekannt und noch da (nicht neu gemeldet)
- **bekannt K41 D2614:** 12 Bestände und die Beschreibungen von V.L.156./162. nur als «Text vor der ersten Signatur» (89 Zeilen).
- **bekannt K117 D2710:** Jahresdokumentation Sch. 1/2 als Teil 2 unter den allgemeinen Schachteln.
- **D2589 19.:** Einziges Darin ist «Gedruckte Exemplare (Lichtdruck):», der Kopf des Verweisblocks; der Rest steht im Info.
  NP12 G1 wertete das als mittel (Grenzfall). Nach «Inhalt bei falscher Einheit» und dem «⇣»-Hinweis wäre auch kritisch
  vertretbar. Entscheid der Hauptsession.
- **Weitere:** mittel D2828 K15 (Rest laut Entscheid), D2759 K99 (Rest), D2630 Schachtel bei 9., D2751 4.4.; gering D2754,
  D2757, D2763 :5.; D2681 bewusst offen seit Runde 7; D2657 Titelblatt im Darin (Kosmetik).

## Muster
- «Datum / Name»-Vermerke stehen überall richtig im Info. Nur D2630 hat die umgekehrte Form.
- Kein Info-Satz nennt Archivgut über das Verzeichnete hinaus. Umfangssätze und «Lagerung» fassen nur zusammen; die übrigen
  Sätze sind Verweise auf andere Bestände, Bibliothek oder Literatur.
- Keine Signatur steht nur im Vorspann. In D2609 ist «64.» der Titel des Turnfests.

## Unsicherheiten
- D2710: Den Einleitungssatz «Die Schachteln 1 und 2 enthalten in loser Folge:» werte ich nicht als Fund (höchstens gering).
- D2641: «fehlt: ohne/datum» ist ein Fehlalarm, der Text steht im Titel.
