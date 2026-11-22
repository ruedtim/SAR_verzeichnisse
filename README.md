# SAR-Findmittel → scope-Import

Wandelt die Findmittel-PDFs des Stadtarchivs Zürich (Bestände, die in scope noch nicht erschlossen sind) in
Excel-Dateien für den scope-Import um: eine Datei je Findmittel mit den Blättern «scope-Import», «Prüfliste»,
«Vollständigkeit» und «Info», dazu eine Übersicht über alle Findmittel.

## Inhalt

- `findmittel_zu_scope.py` – Umwandlung PDF → Excel.
- `findmittel_laden.py` – lädt das Verzeichnis und die Findmittel-PDFs aus dem Online-Archiv.
- `findmittel_pdf/verzeichnis.csv` – Verzeichnis der Findmittel (Signatur, Titel, Datei) aus dem Online-Archiv.
- `stichproben/` – Stichprobenprüfung und Nachprüfungen am PDF: Berichte, Fundlisten, Werkzeuge.
- `findmittel_excel/` – die Excel-Dateien aller 715 Findmittel und die Übersicht `uebersicht_scope_import.xlsx`.
- `testdaten_excel/` und `D151210_scope_import.xlsx` – Testdaten und das Findmittel VII.200.

Die Excel-Dateien sind mit dem Skript dieses Stands erzeugt (Runde 13, 22.11.2026). Diesen Stand prüft
`stichproben/nachpruefung16.md`:
- In der vierten Zufallsstichprobe ist keine von 60 Dateien kritisch.
- Offen sind 11 kritische Zeilen in `stichproben/offen_kritisch.csv`: 10 bewusst offen, dazu der Grenzfall K221.
- Mittlere Fehler (Titel, Zeitraum, Schachtel) kommen noch häufig vor, in der Stichprobe in fast jeder dritten Datei.

Die Vorstände prüfen `stichproben/nachpruefung8.md` bis `stichproben/nachpruefung15.md`. Seit NP12 ist jede der 715 Dateien
mindestens einmal ganz auf kritische Fehler geprüft. NP15 hat zudem Schluss und Blatt Info aller Dateien durchgesehen.
Änderungen und offene Punkte stehen in `stichproben/runde7/AENDERUNGEN_RUNDE7.md` bis
`stichproben/runde13/AENDERUNGEN_RUNDE13.md`.

Jede Excel-Datei enthält im Blatt «Prüfliste» die Einheiten mit Prüfhinweisen; sie gehören in die Nachkontrolle nach dem
Import. Stücke ohne Nummer stehen im Darin einer eigenen Zeile für den Bestand (Signatur = Bestand), es werden keine
Signaturen erfunden.

Nicht im Repository: die PDFs (Quelle: Online-Archiv des Stadtarchivs).

## Aufruf

```bash
uv run --with pdfplumber --with openpyxl python findmittel_zu_scope.py findmittel_pdf/pdf -o findmittel_excel \
    --cache cache --katalog findmittel_pdf/verzeichnis.csv
```
