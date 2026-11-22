# NP15 – Vorbereitung (22.11.2026, während der Installation von Runde 12)

Ohne Blick auf Runde 12 geschrieben. Gearbeitet wurde nur mit der eigenen Kopie von Runde 11 (`np14/aus_neu`, Skript 94ff40ba),
nicht mit `findmittel_excel/`.

## Dritte Zufallsstichprobe (festgelegt vor dem ersten Blick auf Runde 12)

- **Reihenfolge:** dieselbe wie in NP13 und NP14 (`np14/zufall_reihenfolge.txt`, `random.Random(20261122)` über die 715 Dateien).
  Stichprobe 1 belegt die Ränge 1–73, Stichprobe 2 die Ränge 74–136.
- **Kandidaten:** `kandidaten_ab137.txt` (auch `stichproben/roh/np15_kandidaten_ab137.txt`), sha256 `0dc385e7b2b1688a…`.
  - Das sind 568 Dateien ab Rang 137, ohne Stichprobe 1 und 2 und ohne die 16 Dateien in `offen_kritisch.csv` (Stand NP14).
  - Ab Rang 137 fallen dadurch D2614, D3828, D1739, D175949, D2951, D3099, D149622, D2710, D1858, D3208 und D3894 weg.
- **Stichprobe 3:** die ersten 60 Kandidaten, die Runde 12 nicht ändert (`mappen15.sh` zieht sie).
- **Prüfung:** ganz, wie Z1–Z3 der NP13 und ZL1/ZL2 der NP14.
- **Grundgesamtheit:** 715 − 120 (Stichproben 1 und 2) − 16 (offen_kritisch) = 582 Dateien, davon abgezogen die Dateien, die
  Runde 12 ändert.
- **Auswertung:** Rate der Stichprobe 3 allein und mit 1 und 2 zusammen (180 Dateien), Wilson-Intervall.

## Neu in NP15: Durchsicht aller 715 Dateien am Schluss und im Blatt Info

Das ist kein Suchlauf mit Muster. Die übersehenen Fehler der NP14 waren Einzelformen, die kein Muster traf. Darum werden alle
Dateien einmal ganz durchgesehen, aber nur an den Stellen, an denen diese Formen sitzen.

- **Werkzeug:** `durchsicht_schluss_info.py`. Es schreibt je Datei einen Block mit
  - `[Schluss]`: den Zeilen der Prüfmappe ab der letzten Einheit, mit ihrem Ort in der Excel und der Marke «⇣» für einen
    grossen Abstand;
  - `[Letzte]`: der letzten Einheit (Eltern, Schachtel, Zeitraum, Titel, Darin, Hinweise);
  - `[Bestand]`: der Bestandszeile;
  - `[Info]`: den Schlussvermerken, die nicht schon im Schluss stehen;
  - `[Nicht übernommen]`: der Liste im Blatt Vollständigkeit (Text vor der ersten Signatur, Überschriften ohne Signatur, Zeilen
    mit fehlenden Wörtern), ohne Tabellenköpfe;
  - `[Vorspann]`: «Signaturen nur im Vorspann».
- **Umfang:** 715 Blöcke, an Runde 11 1,18 Mio. Zeichen, aufgeteilt in 8 Teile à etwa 150'000 Zeichen (Pakete D1–D8).
  - Grundlage sind die Prüfmappen aller 715 Dateien. Für Runde 12 werden die Runde-11-Mappen übernommen und nur die geänderten
    Dateien neu gerechnet. Das ist zulässig, weil `zellen.py` alle Blätter ausser «Erzeugt» vergleicht.
- **Probe an Runde 11:** Die bekannten Fälle erscheinen in den Blöcken:
  - D175949 (K203): der Bearbeitervermerk steht mit «⇣» im Darin von Q.1;
  - D1729 (K206) und D2502 (K207): der Stück-Satz steht als Schlussvermerk im Info.
- **Was zu beurteilen ist:**
  - Gehört jede Zeile nach der letzten Einheit dorthin, wo sie steht? Darin der letzten Einheit, Darin der Gruppe, Bestandszeile
    oder Info.
  - Nennt ein Info-Satz oder eine nicht übernommene Zeile Archivgut, das keine Einheit ist? Das wäre ein Stück ohne Nummer.
  - Ist eine Überschrift ohne Signatur in Wahrheit eine Einheit oder eine Gruppe?

## Gruppenende mit gleichem Abstand

`suchlauf_gruppenende.py` hat jetzt einen Faktor als viertes Argument (Vorgabe 1,3).
- An Runde 11 ergibt Faktor 1,3 dieselben 16 Kandidaten wie in NP14. Faktor 1,0 ergibt 289 Kandidaten; davon sind 273 neu, 171
  ohne Spiegelstrich, in 34 Dateien.
- 107 davon stehen in vier Dateien mit gleichmässigem Zeilenabstand: D141020, D4054, D149628 und D151210. Dort steht auch K208.
- Drei Stichproben an Runde 11 sind kein Fund, die Zeile ist jeweils die eigene Beschreibung der Untereinheit:
  - D149888 10.4.3. «Provenienz des gesamten Materials in dieser Schachtel …»;
  - D150829 5.8.;
  - D3718 5.2.10.
- Die Kandidaten bei 1,0 werden gesichtet. Massstab ist Regel 9 der Runde 11: Die Zeile ist eingerückt wie die Beschreibung
  der Gruppe, nicht wie die der Untereinheit.

## Ablauf nach «Runde 12 installiert»

1. `bash start15.sh`:
   - Stand sichern, Gesamtlauf, Testdaten, D151210;
   - Zellvergleiche (Projekt = eigener Lauf? Runde 11 → 12);
   - Fallsets (alt = `np14/aus_neu`);
   - alle Suchläufe;
   - Prüfmappen und Durchsichtsblöcke.
2. `stichproben/runde12/` lesen; `vorher/` gegen `np14/aus_neu` vergleichen.
3. `bash mappen15.sh`: Stichprobe 3 ziehen, Vergleiche, Kompaktmappen und Strukturberichte.
4. Prüfpakete:
   - G für die von Runde 12 geänderten Dateien und die Testdateien, Altzeilen K203–K208;
   - D1–D8 für die Durchsicht;
   - Z für Stichprobe 3;
   - S für die Suchläufe mit der Sichtung «Gruppenende 1,0».
5. Zusammenführen mit `zusammen15.py` (aus `np14/zusammen14.py`, K-Nummern stabil, neue ab K209).

## Ablauf am 22.11.2026 (nach «Runde 12 installiert»)

1. `np15_start15.sh`:
   - Stand sichern, Gesamtlauf, Testdaten, D151210;
   - Zellvergleiche, Fallsets, alle Suchläufe;
   - Prüfmappen aller 715 Dateien: die Mappen der Runde 11 übernommen, die 18 geänderten neu;
   - Durchsichtsblöcke, 8 Teile.

   Ergebnis:
   - Der Lauf ist zellgleich.
   - Geändert sind 18 Dateien, gleich der Liste der Hauptsession.
   - `runde12/vorher/` ist zellgleich mit dem eigenen Lauf der Runde 11.
   - Die zwei geänderten Testdateien sind zellgleich mit ihren Gegenstücken in `findmittel_excel/`.
2. `np15_mappen15.sh`:
   - Stichprobe 3 nach der festen Regel: Ränge 137–196, Grundgesamtheit 572 Dateien;
   - Vergleiche, Kompaktmappen, Strukturberichte.
3. **Neue Werkzeuge:**
   - `np15_suchlauf_gruppenende_eng.py`: Gruppenende mit dem Abstand eines neuen Eintrags, nach Lage gefiltert. Probe an
     Runde 10: alle 5 bekannten Fälle in der Liste.
   - `np15_suchlauf_vermerk_im_darin.py`: Bearbeitervermerke im Darin. Probe: findet K203 an Runde 11; findet D2630.
4. **Pakete nach `roh/np15_AUFTRAG15.md`:**
   - G1, G2: Gegenprüfung, Altzeilen K203–K208;
   - D1–D8: Durchsicht aller 715 Dateien;
   - Z1–Z3, ZL1: Stichprobe 3;
   - S1: 192 Kandidaten «Gruppenende, gleicher Abstand»;
   - V1: Vorfund der Prüfsession, D2630.
5. `np15_zusammen15.py <pakete> <offen_kritisch_alt.csv> <aus>`:
   - K-Nummern bleiben stabil, neue ab K209.
   - Doppelte neue Funde werden zusammengelegt, mit Vorrang G > Z > D > S > V. D2630: D4 bleibt, V1 entfällt.
   - Notizen der Prüfsession zu Umwertungen und Grenzfällen stehen im Dict NOTIZ.
